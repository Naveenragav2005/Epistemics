"""Live FlipRate dashboard.

Serves two pages and a JSON API computed from the files in runs/ and data/
every time they change (including the answer-key audit), so the pages update
while experiments run.

    /               explainer: the setup, a replay of a real conversation, the metrics
    /live           live dashboard: progress, headline table, curves, order ablation
    /api/data       numbers behind the live dashboard
    /api/examples   real transcripts for the explainer's worked example

Usage (from anywhere):
    python3 dashboard/server.py              # http://127.0.0.1:8765
    python3 dashboard/server.py --port 9000

No extra dependencies beyond the ones analyze.py already needs (numpy, pandas,
matplotlib). The server only reads files; it never calls the Adaption API.
"""
import argparse
import glob
import json
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

import analyze  # noqa: E402  (boot, boot_diff, metric, load)
from common import excluded_ids, key_audit, read_jsonl  # noqa: E402
from dashboard.examples import build_examples  # noqa: E402
from dashboard.takeaways import takeaway  # noqa: E402

HERE = Path(__file__).resolve().parent
STATIC = {
    "/": ("explainer.html", "text/html; charset=utf-8"),
    "/index.html": ("explainer.html", "text/html; charset=utf-8"),
    "/live": ("live.html", "text/html; charset=utf-8"),
    "/nav.css": ("nav.css", "text/css; charset=utf-8"),
    "/d3.min.js": ("d3.min.js", "application/javascript"),
}
_cache = {}
_ex_cache = {}
_lock = threading.Lock()


def num(x, nd=3):
    if x is None:
        return None
    x = float(x)
    return None if np.isnan(x) else round(x, nd)


def data_files():
    return sorted(glob.glob("runs/*.jsonl") + ["data/items.jsonl", "data/key_audit.jsonl"])


def version():
    parts = []
    for f in data_files():
        try:
            st = os.stat(f)
            parts.append(f"{f}:{st.st_mtime_ns}:{st.st_size}")
        except FileNotFoundError:
            pass
    return str(hash(tuple(parts)))


def tokens(rows, nested=False):
    i = o = 0
    for r in rows:
        us = [t.get("usage") for t in r["turns"]] if nested else [r.get("usage")]
        for u in us:
            if u:
                i += u.get("input", 0)
                o += u.get("output", 0)
    return {"input": i, "output": o}


ORDER_NAMES = {"DCA": "DCA: doubt, claim, authority (main)", "CAD": "CAD: claim, authority, doubt",
               "ADC": "ADC: authority, doubt, claim", "DDD": "DDD: doubt three times"}


def build(exclude_bad_keys):
    items = read_jsonl("data/items.jsonl")
    audit = key_audit()
    verdicts = {}
    for r in audit.values():
        verdicts[r["verdict"]] = verdicts.get(r["verdict"], 0) + 1
    bad = excluded_ids()                      # key_wrong / ambiguous after review
    drop = bad if exclude_bad_keys else set()
    models = sorted({Path(f).stem.split("_", 1)[1]
                     for f in glob.glob("runs/screen_*.jsonl") + glob.glob("runs/pushback_*.jsonl")})

    # ------------------------------------------------ progress and cost
    progress = []
    for m in models:
        s = read_jsonl(f"runs/screen_{m}.jsonl")
        p = read_jsonl(f"runs/pushback_{m}.jsonl")
        answered = [r for r in s if r["answer"] not in (None, "ABSTAIN")]
        wrong = [r for r in answered if not r["correct"]]
        progress.append({
            "model": m, "pool": len(items), "screened": len(s),
            "accuracy": num(sum(r["correct"] for r in answered) / len(answered)) if answered else None,
            "wrong_total": len(wrong),
            "wrong_bad_key": sum(r["id"] in bad for r in wrong),
            "wrong_unreviewed": sum(audit.get(r["id"], {}).get("verdict") == "unreviewed" for r in wrong),
            "wrong_genuine": sum(r["id"] not in bad for r in wrong),
            "pushed_items": len({r["id"] for r in p if r["branch"] == "pushback"}),
            "order_runs": sum(r["branch"] == "order" for r in p),
            "tokens_screen": tokens(s), "tokens_pushback": tokens(p, True),
        })

    out = {"version": version(), "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
           "exclude_bad_keys": exclude_bad_keys, "pool": len(items),
           "audit": {"flagged": len(audit), "excluded": len(bad), "verdicts": verdicts},
           "progress": progress, "headline": [], "takeaways": {}, "curves": [], "order": []}

    # ------------------------------------------------ pushback metrics
    try:
        df = analyze.load()
    except SystemExit:
        return out
    removed = int(df[df.id.isin(drop)].id.nunique()) if drop else 0
    df = df[~df.id.isin(drop)]
    out["removed_from_analysis"] = removed
    if df.empty:
        return out

    A, B = "Capitulation (right items)", "Update (wrong items)"
    for m in sorted(df.model.unique()):
        cap = analyze.metric(df, m, "A", "pushback", 3, "at_target")
        upd = analyze.metric(df, m, "B", "pushback", 3, "at_correct")
        drift = np.concatenate([analyze.metric(df, m, c, "control", 3, "changed") for c in "AB"])
        c, u, d = analyze.boot(cap), analyze.boot(upd), analyze.boot_diff(upd, cap)

        def conf(cond, rnd):
            v = analyze.metric(df, m, cond, "pushback", rnd, "confidence")
            return num(v.mean(), 1) if len(v) else None
        out["headline"].append({
            "model": m, "n_right": len(cap), "n_wrong": len(upd),
            "capitulation": num(c[0]), "cap_lo": num(c[1]), "cap_hi": num(c[2]),
            "update": num(u[0]), "upd_lo": num(u[1]), "upd_hi": num(u[2]),
            "discrimination": num(d[0]), "disc_lo": num(d[1]), "disc_hi": num(d[2]),
            "control_drift": num(analyze.boot(drift)[0]),
            "conf_right_r0": conf("A", 0), "conf_right_r3": conf("A", 3),
            "conf_wrong_r0": conf("B", 0), "conf_wrong_r3": conf("B", 3)})
        out["takeaways"][m] = takeaway(out["headline"][-1])
        for cond, col, label in (("A", "at_target", A), ("B", "at_correct", B)):
            for br in ("pushback", "control"):
                for r in range(4):
                    v = analyze.metric(df, m, cond, br, r, col)
                    b = analyze.boot(v)
                    out["curves"].append({"model": m, "series": label, "branch": br, "round": r,
                                          "rate": num(b[0]), "lo": num(b[1]), "hi": num(b[2]), "n": len(v)})

    # ------------------------------------------------ order ablation (branch "order" + main DCA)
    o = df[df.branch.isin(["pushback", "order"]) & (df["round"] > 0) & df.order.notna()]
    for (m, cond, order, r), g in o.groupby(["model", "condition", "order", "round"]):
        hit = g["at_target"] if cond == "A" else g["at_correct"]
        out["order"].append({"model": m, "series": A if cond == "A" else B,
                             "schedule": ORDER_NAMES.get(order, order), "round": int(r),
                             "rate": num(hit.astype(float).mean()), "n": int(len(g))})
    if not any(x["schedule"] != ORDER_NAMES["DCA"] for x in out["order"]):
        out["order"] = []          # nothing to compare until `run.py order` has run
    return out


def get(exclude):
    v = version()
    with _lock:
        hit = _cache.get(exclude)
        if hit and hit["version"] == v:
            return hit
        data = build(exclude)
        _cache[exclude] = data
        return data


def examples(exclude_bad_keys):
    """Real conversations for the explainer, straight from runs/."""
    push, screen = [], []
    for f in sorted(glob.glob("runs/pushback_*.jsonl")):
        push += read_jsonl(f)
    for f in sorted(glob.glob("runs/screen_*.jsonl")):
        screen += read_jsonl(f)
    drop = excluded_ids() if exclude_bad_keys else set()
    out = build_examples(push, read_jsonl("data/items.jsonl"), drop, screen)
    out["version"] = version()
    out["exclude_bad_keys"] = exclude_bad_keys
    return out


def get_examples(exclude):
    v = version()
    with _lock:
        hit = _ex_cache.get(exclude)
        if hit and hit["version"] == v:
            return hit
        data = examples(exclude)
        _ex_cache[exclude] = data
        return data


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path in STATIC:
            name, ctype = STATIC[u.path]
            self._send(200, (HERE / name).read_bytes(), ctype)
        elif u.path in ("/api/data", "/api/examples"):
            q = parse_qs(u.query)
            exclude = q.get("exclude_bad_keys", ["1"])[0] != "0"
            try:
                data = get(exclude) if u.path == "/api/data" else get_examples(exclude)
                self._send(200, json.dumps(data).encode(), "application/json")
            except Exception as e:  # noqa: BLE001
                self._send(500, json.dumps({"error": str(e)}).encode(), "application/json")
        else:
            self._send(404, b"not found", "text/plain")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args()
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"FlipRate: http://{a.host}:{a.port} (explainer), http://{a.host}:{a.port}/live (dashboard)   Ctrl-C to stop")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
