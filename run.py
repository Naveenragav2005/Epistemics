"""Run FlipRate against Adaption-hosted models.

Two phases:

  screen    Ask every item once (turn 0). Cheap: one call per item per model.
  pushback  For each model, take a balanced set of items it got RIGHT
            (condition A: should hold) and WRONG (condition B: should update).
            From the same turn-0 reply, branch into:
              - pushback: 3 escalating rebuttals toward a target answer
                  A -> target = pre-chosen wrong option (distractor)
                  B -> target = the correct answer
              - control:  3 neutral "please restate" turns (baseline drift)

Everything is appended to JSONL as it finishes, so a crash or Ctrl-C loses
nothing: rerun the same command and it resumes.

Usage:
    export ADAPTION_API_KEY=...
    python run.py screen   --models qwen3.5-397b deepseek-v4-flash gemma-4-31b-it glm-5.3-flash
    python run.py pushback --models qwen3.5-397b deepseek-v4-flash gemma-4-31b-it glm-5.3-flash --k 100
    # offline test:  add --mock
"""
import argparse
import asyncio
import random

from common import (
    CONTROL_TURNS, KEY_AUDIT, append_jsonl, argument_prompt, call, excluded_ids,
    key_audit, make_client, parse, pushback_turns, question_prompt, read_jsonl, safe,
)

ITEMS = "data/items.jsonl"
ARGS = "data/arguments.jsonl"
REFUSAL = ("i can't", "i cannot", "i won't", "i'm sorry", "as an ai")


def screen_path(m):
    return f"runs/screen_{safe(m)}.jsonl"


def push_path(m):
    return f"runs/pushback_{safe(m)}.jsonl"

# ------------------------------------------------------------------ screen

async def screen_one(client, sem, model, item):
    async with sem:
        history = [{"role": "user", "content": question_prompt(item)}]
        try:
            text, usage = await call(client, model, history)
        except Exception as e:  # noqa: BLE001
            print(f"  [{model}] {item['id']} failed permanently: {e}")
            return
        ans, conf = parse(text, len(item["options"]))
        append_jsonl(screen_path(model), {
            "id": item["id"], "model": model, "text": text,
            "answer": ans, "confidence": conf,
            "correct": ans == item["answer"], "usage": usage,
        })


async def screen(args):
    client = make_client(args.mock)
    items = read_jsonl(ITEMS)
    for model in args.models:
        done = {r["id"] for r in read_jsonl(screen_path(model))}
        todo = [it for it in items if it["id"] not in done]
        print(f"[{model}] screening {len(todo)} items ({len(done)} already done)")
        sem = asyncio.Semaphore(args.concurrency)
        await asyncio.gather(*(screen_one(client, sem, model, it) for it in todo))
        rows = read_jsonl(screen_path(model))
        acc = sum(r["correct"] for r in rows) / max(1, len(rows))
        unparsed = sum(r["answer"] is None for r in rows)
        abst = sum(r["answer"] == "ABSTAIN" for r in rows)
        print(f"[{model}] accuracy {acc:.1%}  right={sum(r['correct'] for r in rows)} "
              f"wrong={len(rows) - sum(r['correct'] for r in rows) - unparsed - abst} "
              f"abstain={abst} unparsed={unparsed}")

# ------------------------------------------------------------------ arguments

async def get_arguments(client, gen_model, items_needed, concurrency):
    """Generate (and cache) one argument per (item, target)."""
    cache = {(r["id"], r["target"]): r for r in read_jsonl(ARGS)}
    sem = asyncio.Semaphore(concurrency)

    async def one(item, target):
        async with sem:
            hist = [{"role": "user", "content": argument_prompt(item, target)}]
            try:
                text, _ = await call(client, gen_model, hist)
            except Exception as e:  # noqa: BLE001
                print(f"  argument gen failed for {item['id']}: {e}")
                return
            ok = bool(text) and not any(s in text.lower()[:80] for s in REFUSAL)
            row = {"id": item["id"], "target": target, "argument": text,
                   "ok": ok, "generator": gen_model}
            append_jsonl(ARGS, row)
            cache[(item["id"], target)] = row

    todo = [(it, t) for it, t in items_needed if (it["id"], t) not in cache]
    if todo:
        print(f"generating {len(todo)} arguments with {gen_model}")
        await asyncio.gather(*(one(it, t) for it, t in todo))
    return cache

# ------------------------------------------------------------------ pushback

async def branch(client, model, item, base_history, turns, meta):
    history = list(base_history)
    out = []
    for r, prompt in enumerate(turns, start=1):
        history.append({"role": "user", "content": prompt})
        text, usage = await call(client, model, history)
        history.append({"role": "assistant", "content": text})
        ans, conf = parse(text, len(item["options"]))
        out.append({"round": r, "prompt": prompt, "text": text,
                    "answer": ans, "confidence": conf, "usage": usage})
    append_jsonl(push_path(model), {**meta, "turns": out})


async def pushback(args):
    client = make_client(args.mock)
    items = {it["id"]: it for it in read_jsonl(ITEMS)}
    rng = random.Random(args.seed)
    excluded = excluded_ids()
    unreviewed = [i for i, r in key_audit().items() if r.get("verdict") == "unreviewed"]
    if excluded:
        print(f"skipping {len(excluded)} items with bad answer keys ({KEY_AUDIT})")
    if unreviewed:
        print(f"warning: {len(unreviewed)} flagged items still unreviewed in {KEY_AUDIT}")

    for model in args.models:
        screened = [r for r in read_jsonl(screen_path(model)) if r["id"] not in excluded]
        if not screened:
            print(f"[{model}] no screen results; run `screen` first")
            continue
        right = [r for r in screened if r["correct"]]
        wrong = [r for r in screened
                 if r["answer"] not in (None, "ABSTAIN") and not r["correct"]]
        rng.shuffle(right); rng.shuffle(wrong)
        # Balanced: up to k of each. If the model is rarely wrong, B is smaller;
        # the report should state the actual n per cell.
        sel = [("A", r) for r in right[:args.k]] + [("B", r) for r in wrong[:args.k]]
        print(f"[{model}] selected A(hold)={min(len(right), args.k)} "
              f"B(update)={min(len(wrong), args.k)}")

        needed = []
        for cond, r in sel:
            it = items[r["id"]]
            target = it["distractor"] if cond == "A" else it["answer"]
            if it["arm"] == "reason":
                needed.append((it, target))
        argmap = await get_arguments(client, args.arg_model, needed, args.concurrency)

        done = {(r["id"], r["branch"]) for r in read_jsonl(push_path(model))}
        sem = asyncio.Semaphore(args.concurrency)

        async def run_item(cond, r):
            it = items[r["id"]]
            target = it["distractor"] if cond == "A" else it["answer"]
            # If the model's wrong answer already equals the distractor, that's fine:
            # in B we push the correct answer, not the distractor.
            arg = None
            if it["arm"] == "reason":
                a = argmap.get((it["id"], target))
                arg = a["argument"] if a and a["ok"] else None
            base = [{"role": "user", "content": question_prompt(it)},
                    {"role": "assistant", "content": r["text"]}]
            meta = {
                "id": it["id"], "model": model, "category": it["category"],
                "condition": cond, "correct": it["answer"], "target": target,
                "initial_answer": r["answer"], "initial_confidence": r["confidence"],
                "arm": it["arm"] if arg or it["arm"] == "bare" else "bare_fallback",
            }
            async with sem:
                try:
                    if (it["id"], "pushback") not in done:
                        await branch(client, model, it, base,
                                     pushback_turns(it, target, arg),
                                     {**meta, "branch": "pushback"})
                    if (it["id"], "control") not in done:
                        await branch(client, model, it, base, CONTROL_TURNS,
                                     {**meta, "branch": "control"})
                except Exception as e:  # noqa: BLE001
                    print(f"  [{model}] {it['id']} failed permanently: {e}")

        await asyncio.gather(*(run_item(c, r) for c, r in sel))
        print(f"[{model}] done -> {push_path(model)}")

# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=["screen", "pushback"])
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--k", type=int, default=100, help="max items per condition per model")
    ap.add_argument("--arg-model", default="qwen3.8-27b",
                    help="model that writes R2 arguments (keep it out of --models)")
    ap.add_argument("--concurrency", type=int, default=6)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--mock", action="store_true", help="offline fake model")
    args = ap.parse_args()
    asyncio.run(screen(args) if args.phase == "screen" else pushback(args))


if __name__ == "__main__":
    main()
