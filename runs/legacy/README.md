# Legacy order-ablation runs (not used by analyze.py)

`order_*.jsonl` here come from an earlier, separate implementation of the order
ablation, run on the 56-item pilot before the answer-key audit. They are kept
for reference only and are NOT read by `analyze.py` or the dashboard because
the rebuttal wording differs from the current design:

| legacy `schedule` | what it was                                   | current design        |
|-------------------|-----------------------------------------------|-----------------------|
| `reversed`        | authority, claim, doubt (ACD)                 | not in the Latin square (CAD, ADC) |
| `repeat_doubt`    | the *identical* doubt sentence three times    | DDD uses paraphrased doubts |
| `default`         | doubt, claim, authority                       | DCA                   |

The wrong-item (condition B) rows also include items with wrong answer keys.
