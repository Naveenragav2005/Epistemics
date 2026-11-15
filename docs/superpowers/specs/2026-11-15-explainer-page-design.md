# Explainer page + two-page dashboard — design

## Intent and why
The live dashboard shows numbers but assumes the reader already knows what capitulation, R2 or DDD mean. Audience is researchers. Add an explainer page built around a real worked example, so a reader sees what "a model flipped" looks like before reading the tables.

## Goals
- `/` explainer page; `/live` the existing dashboard; shared nav bar.
- Worked example: replay of a real conversation from `runs/`, round by round, with answer and confidence per turn and the control branch alongside.
- Explain setup (conditions A/B, R1–R3, control, order ablation), metrics (discrimination scale), and caveats (MMLU-Pro source, key audit, sample size).
- Live page: a "what you're seeing" caption per chart and a data-generated takeaway line per model.

## Non-goals / anti-goals
- No changes to `run.py`, `analyze.py`, or any API calls; server stays read-only.
- No build step or new dependencies (stdlib server, vendored d3, plain CSS).
- Must not read as cherry-picked: examples are illustrative, the tables are the evidence.

## Constraints
- Current runs are small (about 3–6 condition-B items per model), so both pages carry an "early data, n shown on every cell" note.

## Approaches
1. **Two routes in the existing server, examples served from `runs/` via `/api/examples` (chosen).** Real transcripts stay in sync with data; no duplication.
2. Static explainer with hand-copied transcript. Simpler, but goes stale and risks looking cherry-picked.
3. Separate static site. Extra deploy surface, loses the live link to the data.

## Decisions
- Move current `index.html` to `/live` with caption additions; new `explainer.html` at `/`.
- Example picker: dropdown by model and case type (capitulation A, hold A, update B). Defaults chosen by rule (e.g. first A item that flips with initial confidence ≥80), not by hand.
- Takeaway lines generated from the same computed data as the tables.

## Left to the builder
Visual design, exact caption wording, stepper interaction details, and the diagram style for the A/B setup.
