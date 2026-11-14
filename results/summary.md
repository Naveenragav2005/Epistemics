# FlipRate results

## Headline (round 3)

| Model | n A | n B | Capitulation (A) | Update (B) | Discrimination | Control drift | Parse fail |
|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 10 | 8 | 0.20 [0.00, 0.50] | 0.75 [0.38, 1.00] | 0.55 [0.12, 0.90] | 0.00 [0.00, 0.00] | 0.0% |
| gemma-4-31b-it | 10 | 10 | 0.30 [0.00, 0.60] | 0.70 [0.40, 1.00] | 0.40 [0.00, 0.80] | 0.00 [0.00, 0.00] | 0.0% |
| qwen3.5-397b | 10 | 6 | 0.00 [0.00, 0.00] | 0.50 [0.17, 0.83] | 0.50 [0.17, 0.83] | 0.00 [0.00, 0.00] | 0.0% |

## Per round (pushback branch)

| Model | Metric | R0 | R1 | R2 | R3 |
|---|---|---|---|---|---|
| deepseek-v4-flash | Capitulation (A) | 0.00 | 0.10 | 0.20 | 0.20 |
| deepseek-v4-flash | Update (B) | 0.00 | 0.75 | 0.75 | 0.75 |
| gemma-4-31b-it | Capitulation (A) | 0.00 | 0.00 | 0.00 | 0.30 |
| gemma-4-31b-it | Update (B) | 0.00 | 0.20 | 0.30 | 0.70 |
| qwen3.5-397b | Capitulation (A) | 0.00 | 0.00 | 0.00 | 0.00 |
| qwen3.5-397b | Update (B) | 0.00 | 0.00 | 0.17 | 0.50 |

## Argument vs bare assertion (round 2)

| Model | Cap. A, argument | Cap. A, bare | Upd. B, argument | Upd. B, bare | B gain from argument | A gain from argument |
|---|---|---|---|---|---|---|
| deepseek-v4-flash | 0.14 [0.00, 0.43] | 0.33 [0.00, 1.00] | 1.00 [1.00, 1.00] | 0.60 [0.20, 1.00] | 0.40 [0.00, 0.80] | -0.19 [-0.86, 0.29] |
| gemma-4-31b-it | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.40 [0.00, 0.80] | 0.20 [0.00, 0.60] | 0.20 [-0.40, 0.80] | 0.00 [0.00, 0.00] |
| qwen3.5-397b | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.20 [0.00, 0.60] | -0.20 [-0.60, 0.00] | 0.00 [0.00, 0.00] |

## Confidence

| Model | Mean conf R0 → R3, A pushback | B pushback | Control | Capitulations at ≥80% confidence |
|---|---|---|---|---|
| deepseek-v4-flash | 94 → 98 | 93 → 99 | 94 → 94 | 100% of 2 |
| gemma-4-31b-it | 98 → 100 | 94 → 99 | 96 → 96 | 100% of 3 |
| qwen3.5-397b | 98 → 98 | 97 → 97 | 98 → 98 | n/a |

## Abstention rate by round (pushback, A and B pooled)

| Model | R0 | R1 | R2 | R3 |
|---|---|---|---|---|
| deepseek-v4-flash | 0.00 | 0.00 | 0.00 | 0.00 |
| gemma-4-31b-it | 0.00 | 0.00 | 0.00 | 0.00 |
| qwen3.5-397b | 0.00 | 0.00 | 0.00 | 0.00 |
