# FlipRate: project context (for resuming in a new session)

No secrets in this file. The Adaption API key lives only in the gitignored `.env`
(`ADAPTION_API_KEY=...`, load with `set -a; . ./.env; set +a`). It appeared in an earlier
session transcript, so rotate it in the Adaption app and update `.env`.

## What this is
Apart Research AI x Epistemics Research Sprint (Nov 13-15, 2026) project. Question: do LLMs
change answers because the user is right, or only because the user pushed? MMLU-Pro items,
models served via Adaption's OpenAI-compatible API (`https://api.prod.adaptionlabs.ai/api/v1`):
`qwen3.5-397b`, `deepseek-v4-flash`, `gemma-4-31b-it`. `glm-5.3-flash` was deliberately left out.
Round-2 arguments are written by `qwen3.8-27b` (kept out of the tested set).

## Status (all experiments finished 2026-11-15)
- Pool: 994 items screened. Gaps (never screened, API timeouts): about 15 deepseek, 4 gemma, 68 qwen. Fill skipped on purpose.
- Pushback `--k 50` and order ablation (CAD/ADC/DDD) done for all three models.
- `python3 analyze.py` output is in `results/summary.md`, `results/order_ablation.csv`, `results/fig1..fig5`.
- Report: `FlipRate_report.pdf` (US Letter, Apart template, 7 pages of main text plus references and appendices),
  built from `report/report.html` with `node report/build.js`. Author line: Naveen Ragav, Independent.
  It links the GitHub repo, which must be made public before submitting. The audit caveat stays until a human confirms the verdicts.
  An older Claude Docs version of the report exists under a different claude.ai account and is superseded.

## Headline results (round 3, key-audit exclusions applied)
| Model | n right / wrong | Capitulation | Update | Discrimination |
|---|---|---|---|---|
| deepseek-v4-flash | 61 / 48 | 0.11 | 0.81 | 0.70 |
| gemma-4-31b-it | 65 / 54 | 0.28 | 0.98 | 0.70 |
| qwen3.5-397b | 59 / 50 | 0.17 | 0.84 | 0.67 |

- Authority flips right answers 42-57% at round 1; doubt 0-4%, plain claim 0%.
- Three doubts in a row (DDD) leave right items at 0-6%, so repetition alone does not flip them.
- Argument vs bare assertion: gains for gemma/qwen on wrong items, intervals include 0.
- 94-100% of capitulations are stated at >=80% confidence.

## Answer-key audit (needs a human)
58 flagged: key_wrong 17, ambiguous 13, key_ok 3, unreviewed 25. The 30 key_wrong/ambiguous are
excluded. Every verdict was written by Claude and is marked "Reviewer: Claude, needs human
confirmation". Verdicts live in `data/key_audit.jsonl`; change `verdict` there and rerun `analyze.py`.

## Explainer page (built 2026-11-15)
`dashboard/server.py` serves `/` (explainer, `dashboard/explainer.html`) and `/live` (dashboard, `dashboard/live.html`),
with shared `dashboard/nav.css`. `dashboard/examples.py` builds the worked-example transcripts for `/api/examples`,
`dashboard/takeaways.py` the per-model sentence. Tests: `python3 -m unittest discover tests`.
Design and plan are in `docs/superpowers/`.

## Git state
- Repo `Naveenragav2005/Epistemics` (private). All work, including the explainer page, is on branch
  `claude/optimistic-mccarthy-fvqf8z`; `master` only has the first two commits. No pull request yet.

## Commands (use `python3`; `python` is 2.7 here)
```
python3 run.py screen   --models qwen3.5-397b deepseek-v4-flash gemma-4-31b-it --concurrency 4
python3 audit_keys.py
python3 run.py pushback --models qwen3.5-397b deepseek-v4-flash gemma-4-31b-it --k 50 --concurrency 4
python3 run.py order    --models qwen3.5-397b deepseek-v4-flash gemma-4-31b-it --k 50 --concurrency 4
python3 analyze.py
python3 dashboard/server.py        # http://127.0.0.1:8765 explainer, /live dashboard
python3 -m unittest discover tests
```
All run phases resume and skip finished rows. Concurrency above about 8 per model caused
429 rate limits; 504 timeouts are server-side and are retried automatically.

## Decisions and gotchas
- Two sessions worked on this repo; the merge took the other session's key-audit and order-ablation design as the base (Latin square DCA/CAD/ADC plus DDD). Old order runs are archived in `runs/legacy/` and ignored.
- `--k` caps items per condition per model; wrong-item (B) cells depend on how often each model is wrong. Pilot rows are kept, so some cells exceed 50.
- Never discard user edits without asking; confirm before pushes and credit-spending runs.
- The Claude Docs report belongs to the claude.ai account that created it. A different account cannot edit it unless it is shared.
