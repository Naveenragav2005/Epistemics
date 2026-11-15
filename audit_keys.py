"""Flag likely answer-key errors for human review.

An item is flagged when every screened model gives the same answer and that
answer is not the MMLU-Pro key. Consensus against the key is a cheap signal of
a bad key, but not proof: models can share a misconception. So flags are NOT
dropped automatically. Each one gets a row in data/key_audit.jsonl with
verdict "unreviewed"; a person sets it to one of

    key_wrong   the key is wrong            -> item excluded
    ambiguous   more than one option is defensible -> item excluded
    key_ok      the key is right (models share an error) -> item kept

Only the turn-0 screen is used, never pushback outcomes, so the filter is
independent of the update/capitulation metrics it protects.

Run after `run.py screen` and before `run.py pushback`, so the pushback budget
is not spent on bad items. `run.py pushback` and `analyze.py` both skip
excluded items.

Usage:
    python audit_keys.py            # writes data/key_flags.md, adds stubs to the audit
"""
import argparse
import glob
from pathlib import Path

from common import (
    EXCLUDE_VERDICTS, KEY_AUDIT, LETTERS, VERDICTS, append_jsonl, consensus_flags,
    key_audit, read_jsonl,
)

ITEMS = "data/items.jsonl"
SHEET = "data/key_flags.md"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-models", type=int, default=2,
                    help="minimum screened models needed to flag an item")
    a = ap.parse_args()

    items = {it["id"]: it for it in read_jsonl(ITEMS)}
    screens = {}
    for f in sorted(glob.glob("runs/screen_*.jsonl")):
        rows = read_jsonl(f)
        if rows:
            screens[rows[0]["model"]] = rows
    if len(screens) < a.min_models:
        raise SystemExit(f"need screens from >= {a.min_models} models; found {len(screens)}")

    flags = consensus_flags(items, screens, a.min_models)
    audit = key_audit()
    bad = [r for r in audit.values() if r.get("verdict") not in VERDICTS]
    if bad:
        raise SystemExit(f"unknown verdict in {KEY_AUDIT}: {bad[0]}")

    new = [i for i in flags if i not in audit]
    for iid in sorted(new):
        append_jsonl(KEY_AUDIT, {"id": iid, "key": items[iid]["answer"],
                                 "consensus": flags[iid], "verdict": "unreviewed",
                                 "note": ""})
    audit = key_audit()

    lines = [f"# Answer-key flags\n",
             f"{len(flags)} of {len(items)} items: all {len(screens)} screened models "
             f"({', '.join(screens)}) agree on a non-key answer.\n",
             f"Set each verdict in `{KEY_AUDIT}`. Excluded verdicts: "
             f"{', '.join(sorted(EXCLUDE_VERDICTS))}.\n"]
    for iid in sorted(flags, key=lambda i: (audit[i]["verdict"], i)):
        it, r = items[iid], audit[iid]
        k, c = it["answer"], flags[iid]
        lines += [f"## {iid} ({it['category']}): **{r['verdict']}**\n",
                  it["question"].strip() + "\n",
                  f"- Key ({k}): {it['options'][LETTERS.index(k)]}",
                  f"- Models ({c}): {it['options'][LETTERS.index(c)]}"]
        if r.get("note"):
            lines.append(f"- Note: {r['note']}")
        lines.append("")
    Path(SHEET).write_text("\n".join(lines))

    counts = {}
    for i in flags:
        counts[audit[i]["verdict"]] = counts.get(audit[i]["verdict"], 0) + 1
    print(f"flagged {len(flags)} items ({len(new)} new) -> {SHEET}")
    print("verdicts:", ", ".join(f"{v}={n}" for v, n in sorted(counts.items())))
    if counts.get("unreviewed"):
        print(f"review the 'unreviewed' rows in {KEY_AUDIT} before running pushback")


if __name__ == "__main__":
    main()
