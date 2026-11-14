"""Build the item pool from MMLU-Pro (TIGER-Lab/MMLU-Pro, test split).

Each item gets, fixed in advance and independent of any model:
  - distractor: a random wrong option, the push target when the model is right
  - arm:        'reason' or 'bare', which R2 rebuttal the item receives

Usage:
    python data.py --n 600              # stratified sample across 14 categories
    python data.py --synthetic --n 40   # fake items for offline testing
"""
import argparse
import random

from common import LETTERS, append_jsonl

OUT = "data/items.jsonl"


def load_mmlu_pro():
    from datasets import load_dataset
    ds = load_dataset("TIGER-Lab/MMLU-Pro", split="test")
    for r in ds:
        yield {
            "id": f"mmlupro-{r['question_id']}",
            "question": r["question"],
            "options": list(r["options"]),
            "answer": r["answer"],
            "category": r["category"],
        }


def synthetic(n):
    for i in range(n):
        yield {
            "id": f"syn-{i}",
            "question": f"Synthetic question {i}?",
            "options": [f"option {c}" for c in "ABCDE"],
            "answer": "A",
            "category": random.choice(["math", "law", "physics"]),
        }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=600)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--synthetic", action="store_true")
    a = ap.parse_args()
    rng = random.Random(a.seed)

    pool = list(synthetic(a.n) if a.synthetic else load_mmlu_pro())
    # Stratify: equal share per category, so no single domain dominates.
    by_cat = {}
    for it in pool:
        by_cat.setdefault(it["category"], []).append(it)
    per = max(1, a.n // len(by_cat))
    chosen = []
    for cat in sorted(by_cat):
        items = by_cat[cat]
        rng.shuffle(items)
        chosen += items[:per]
    rng.shuffle(chosen)

    import os
    if os.path.exists(OUT):
        os.remove(OUT)
    for it in chosen:
        k = len(it["options"])
        wrong = [L for L in LETTERS[:k] if L != it["answer"]]
        it["distractor"] = rng.choice(wrong)
        it["arm"] = rng.choice(["reason", "bare"])
        append_jsonl(OUT, it)
    print(f"wrote {len(chosen)} items across {len(by_cat)} categories -> {OUT}")


if __name__ == "__main__":
    main()
