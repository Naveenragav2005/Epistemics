"""Live FlipRate dashboard.

Serves dashboard/index.html and a JSON API computed from the files in runs/ and
data/ every time they change, so the page updates while experiments run.

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
from common import read_jsonl  # noqa: E402

PAGE = Path(__file__).resolve().parent / "index.html"
SCHEDULE_NAMES = {"default": "Default (doubt, claim, authority)",
                  "reversed": "Reversed (authority first)",
                  "repeat_doubt": "Doubt three times"}
_cache = {}
_lock = threading.Lock()


def num(x, nd=3):
    if x is None:
        return None
    x = float(x)
    return None if np.isnan(x) else round(x, nd)


def data_files():
    return sorted(glob.glob("runs/*.jsonl") + ["data/items.jsonl", "data/suspect_items.jsonl"])


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


def build(exclude_suspects):
    items = read_jsonl("data/items.jsonl")
    suspects = read_jsonl("data/suspect_items.jsonl")
    bad = {r["id"] for r in suspects} if exclude_suspects else set()
    models = sorted({Path(f).stem.split("_", 1)[1]
                     for f in glob.glob("runs/screen_*.jsonl") + glob.glob("runs/pushback_*.jsonl")})

    # ------------------------------------------------ progress and cost
    progress = []
    for m in models:
        s = read_jsonl(f"runs/screen_{m}.jsonl")
        p = read_jsonl(f"runs/pushback_{m}.jsonl")
        o = read_jsonl(f"runs/order_{m}.jsonl")
        answered = [r for r in s if r["answer"] not in (None, "ABSTAIN")]
        sus = {r["id"] for r in suspects}
        wrong = [r for r in answered if not r["correct"]]
        progress.append({
            "model": m, "pool": len(items), "screened": len(s),
            "accuracy": num(sum(r["correct"] for r in answered) / len(answered)) if answered else None,
            "wrong_total": len(wrong),
            "wrong_suspect": sum(r["id"] in sus for r in wrong),
            "wrong_genuine": sum(r["id"] not in sus for r in wrong),
            "pushed_items": len({r["id"] for r in p if r["branch"] == "pushback"}),
            "order_runs": len(o),
            "tokens_screen": tokens(s), "tokens_pushback": tokens(p, True), "tokens_order": tokens(o, True),
        })

    out = {"version": version(), "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
           "exclude_suspects": exclude_suspects, "pool": len(items),
           "suspects": len(suspects), "progress": progress,
           "headline": [], "curves": [], "order": []}

    # ------------------------------------------------ pushback metrics
    try:
        df = analyze.load()
    except SystemExit:
        return out
    removed = int(df[df.id.isin(bad)].id.nunique()) if bad else 0
    df = df[~df.id.isin(bad)]
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
            return num(analyze.metric(df, m, cond, "pushback", rnd, "confidence").mean(), 1) \
                if len(analyze.metric(df, m, cond, "pushback", rnd, "confidence")) else None
        out["headline"].append({
            "model": m, "n_right": len(cap), "n_wrong": len(upd),
            "capitulation": num(c[0]), "cap_lo": num(c[1]), "cap_hi": num(c[2]),
            "update": num(u[0]), "upd_lo": num(u[1]), "upd_hi": num(u[2]),
            "discrimination": num(d[0]), "disc_lo": num(d[1]), "disc_hi": num(d[2]),
            "control_drift": num(analyze.boot(drift)[0]),
            "conf_right_r0": conf("A", 0), "conf_right_r3": conf("A", 3),
            "conf_wrong_r0": conf("B", 0), "conf_wrong_r3": conf("B", 3)})
        for cond, col, label in (("A", "at_target", A), ("B", "at_correct", B)):
            for br in ("pushback", "control"):
                for r in range(4):
                    v = analyze.metric(df, m, cond, br, r, col)
                    b = analyze.boot(v)
                    out["curves"].append({"model": m, "series": label, "branch": br, "round": r,
                                          "rate": num(b[0]), "lo": num(b[1]), "hi": num(b[2]), "n": len(v)})

    # ------------------------------------------------ order ablation
    rows, order_ids = [], {}
    for f in glob.glob("runs/order_*.jsonl"):
        for rec in read_jsonl(f):
            if rec["id"] in bad:
                continue
            order_ids.setdefault((rec["model"], rec["condition"]), set()).add(rec["id"])
            tgt = rec["target"] if rec["condition"] == "A" else rec["correct"]
            for r, t in enumerate(rec["turns"], start=1):
                rows.append((rec["model"], rec["condition"], rec["schedule"], r, t["answer"] == tgt))
    pb = df[(df.branch == "pushback") & (df["round"] > 0)]
    for x in pb.itertuples():
        if x.id in order_ids.get((x.model, x.condition), set()):     # compare on the same items
            rows.append((x.model, x.condition, "default", int(x.round),
                         bool(x.at_target if x.condition == "A" else x.at_correct)))
    agg = {}
    for m, c, s, r, hit in rows:
        agg.setdefault((m, c, s, r), []).append(hit)
    for (m, c, s, r), v in sorted(agg.items()):
        out["order"].append({"model": m, "series": A if c == "A" else B,
                             "schedule": SCHEDULE_NAMES[s], "round": r,
                             "rate": num(np.mean(v)), "n": len(v)})
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
        if u.path in ("/", "/index.html"):
            self._send(200, PAGE.read_bytes(), "text/html; charset=utf-8")
        elif u.path == "/d3.min.js":
            self._send(200, (PAGE.parent / "d3.min.js").read_bytes(), "application/javascript")
        elif u.path == "/api/data":
            q = parse_qs(u.query)
            exclude = q.get("exclude_suspects", ["1"])[0] != "0"
            try:
                body = json.dumps(get(exclude)).encode()
                self._send(200, body, "application/json")
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
    print(f"FlipRate dashboard: http://{a.host}:{a.port}   (Ctrl-C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
