"""Worked-example transcripts for the explainer page.

`build_examples` is a pure function over rows already read from `runs/` and
`data/items.jsonl`: no file I/O, no API calls. Every example is a real
conversation from the main pushback branch, joined to its control branch.
"""

KINDS = {"D": "doubt", "C": "claim", "A": "authority"}
MAIN_ORDER = "DCA"
CASES = ("A_flip", "A_hold", "B_update")
CAP = 10            # examples kept per case per model
CONFIDENT = 80      # default example: first right-answer flip stated at >= this


def _turns(row, kinds):
    out = []
    for i, t in enumerate(row.get("turns") or []):
        out.append({
            "round": t.get("round", i + 1),
            "kind": kinds[i] if i < len(kinds) else "restate",
            "prompt": t.get("prompt") or "",
            "text": t.get("text") or "",
            "answer": t.get("answer"),
            "confidence": t.get("confidence"),
        })
    return out


def _case(row):
    turns = row.get("turns") or []
    if not turns:
        return None
    final = turns[-1].get("answer")
    if row.get("condition") == "A":
        if final == row.get("target"):
            return "A_flip"
        if final == row.get("correct"):
            return "A_hold"
    elif row.get("condition") == "B" and final == row.get("correct"):
        return "B_update"
    return None


def build_examples(pushback_rows, items, drop_ids=(), screen_rows=()):
    """Group real pushback conversations into explainer cases.

    pushback_rows: rows from runs/pushback_*.jsonl (all branches, any models).
    items:         item dicts from data/items.jsonl (list, or {id: item}).
    drop_ids:      item ids never offered (wrong or ambiguous answer keys).
    screen_rows:   optional rows from runs/screen_*.jsonl; they supply the
                   text of the model's first reply, which pushback rows omit.

    Returns {"models": {model: {case: [example]}}, "default": {...} | None}.
    """
    if not isinstance(items, dict):
        items = {it["id"]: it for it in items}
    drop = set(drop_ids)
    first_reply = {(r.get("id"), r.get("model")): r.get("text") for r in screen_rows}
    controls = {}
    for r in pushback_rows:
        if r.get("branch") == "control":
            controls[(r.get("id"), r.get("model"))] = r

    models = {}
    for r in pushback_rows:
        if r.get("branch") != "pushback":
            continue
        iid, model = r.get("id"), r.get("model")
        item = items.get(iid)
        if item is None or iid in drop:
            continue
        case = _case(r)
        if case is None:
            continue
        bucket = models.setdefault(model, {c: [] for c in CASES})[case]
        if len(bucket) >= CAP:
            continue
        order = r.get("order") or MAIN_ORDER
        ctrl = controls.get((iid, model))
        bucket.append({
            "id": iid,
            "category": r.get("category") or item.get("category"),
            "question": item.get("question", ""),
            "options": list(item.get("options", [])),
            "correct": r.get("correct"),
            "target": r.get("target"),
            "condition": r.get("condition"),
            "arm": r.get("arm"),
            "initial_answer": r.get("initial_answer"),
            "initial_confidence": r.get("initial_confidence"),
            "initial_text": first_reply.get((iid, model)),
            "turns": _turns(r, [KINDS.get(k, "doubt") for k in order]),
            "control": _turns(ctrl, []) if ctrl else None,
        })

    return {"models": models, "default": _default(models)}


def _default(models):
    for model in sorted(models):
        for i, ex in enumerate(models[model]["A_flip"]):
            if (ex["initial_confidence"] or 0) >= CONFIDENT:
                return {"model": model, "case": "A_flip", "index": i}
    for model in sorted(models):
        for case in CASES:
            if models[model][case]:
                return {"model": model, "case": case, "index": 0}
    return None
