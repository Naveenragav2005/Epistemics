# Explainer Page + Two-Page Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Add an explainer page (`/`) built around a replay of a real conversation, move the existing dashboard to `/live`, and add chart captions and generated per-model takeaway lines.

**Architecture:** `dashboard/server.py` gains routes and two pure data builders in a new `dashboard/examples.py` (example transcripts) and `dashboard/takeaways.py` (takeaway sentences), both unit-tested with stdlib `unittest` against synthetic rows. Pages are static HTML that fetch `/api/examples` and `/api/data`; a shared `nav.css`/nav markup keeps them consistent.

**Tech Stack:** Python stdlib server (existing), vendored d3, plain HTML/CSS/JS, `unittest`. No new dependencies, no build step.

**Spec:** `docs/superpowers/specs/2026-11-15-explainer-page-design.md`

## Global Constraints

- Server stays read-only; no Adaption API calls; `run.py` and `analyze.py` untouched.
- No build step, no new dependencies.
- Examples are real rows from `runs/`, never hand-copied text.
- Default example chosen by rule (first condition-A item that flips to the target with `initial_confidence >= 80`), not by hand.
- Both pages show an "early data, n shown on every cell" note.
- Page copy says examples are illustrative and the tables are the evidence.
- Existing `exclude_bad_keys` behavior applies to examples (excluded ids never offered).

## Review Focus

- No condition-A flip exists for a model: picker still renders, default falls back to first available case, empty state if no rows at all.
- A pushback row has no matching control row: example renders without control, no crash.
- A turn with `answer: null` or `ABSTAIN`: shown as "abstained/unparsed", not crashing the stepper.
- Item id in `runs/` missing from `data/items.jsonl` (pool changed): skipped silently.
- Model with zero n in condition B: takeaway line omits update claim instead of printing NaN or dividing by zero.

---

### Task 1: Example builder

**Files:**
- Create: `dashboard/examples.py`
- Test: `tests/test_examples.py`

**Interfaces:**
- Produces: `build_examples(pushback_rows, items, drop_ids) -> dict` with shape
  `{"models": {model: {"A_flip": [ex], "A_hold": [ex], "B_update": [ex]}}, "default": {"model": str, "case": str, "index": int} | None}`.
  Each `ex` is `{"id", "category", "question", "options": [str], "correct", "target", "condition", "arm", "initial_answer", "initial_confidence", "turns": [{"round", "kind": "doubt"|"claim"|"authority"|"restate", "prompt", "text", "answer", "confidence"}], "control": [same turn shape] | None}`.
  Turn `kind` for pushback comes from the round's rebuttal type; the plan relies on `common.pushback_turns` order (main order DCA: R1 doubt, R2 claim, R3 authority); control turns are `"restate"`.
  Case rules: `A_flip` = condition A and final pushback answer == `target`; `A_hold` = condition A and final answer == `correct`; `B_update` = condition B and final answer == `correct`.
  `default` = first `A_flip` item with `initial_confidence >= 80` for the first model (sorted) that has one, else first non-empty case, else `None`.

- [x] **Step 1: Write failing tests** in `tests/test_examples.py` (`unittest`, synthetic rows) with names and assertions:
  - `test_flip_case_classified`: A row ending at `target` lands in `A_flip`, not `A_hold`.
  - `test_default_prefers_confident_flip`: two A flips, only the second has confidence 95 → default points at it.
  - `test_default_falls_back_when_no_flip`: only a hold exists → `default["case"] == "A_hold"`.
  - `test_empty_returns_none_default`: no rows → `default is None`, `models == {}`.
  - `test_missing_item_skipped`: row id absent from items → not in output.
  - `test_dropped_ids_excluded`: id in `drop_ids` → not in output.
  - `test_missing_control_gives_none`: no control row → `ex["control"] is None`.
  - `test_null_answer_turn_kept`: a turn with `answer=None` appears with `answer is None`.
- [x] **Step 2: Run** `python3 -m unittest tests.test_examples -v` — expect ImportError/FAIL.
- [x] **Step 3: Implement** `build_examples` in `dashboard/examples.py` (pure function, no file I/O; join control rows to pushback rows by `(id, model)`; only use `branch == "pushback"` rows for cases; cap each case list at 10 per model).
- [x] **Step 4: Run** the tests — expect all PASS.
- [x] **Step 5: Commit** `git add dashboard/examples.py tests && git commit -m "feat: build worked-example transcripts from runs"`.

### Task 2: Takeaway builder

**Files:**
- Create: `dashboard/takeaways.py`
- Test: `tests/test_takeaways.py`

**Interfaces:**
- Consumes: a `headline` list item from `server.build()` (keys `model, n_right, n_wrong, capitulation, update, discrimination, conf_right_r0, conf_right_r3`).
- Produces: `takeaway(h: dict) -> str`, one sentence per model.

- [x] **Step 1: Write failing tests**:
  - `test_reports_capitulation_and_update`: `capitulation=0.27, n_right=15, update=1.0, n_wrong=4` → string contains `"27%"`, `"15"`, `"100%"`, `"4"`.
  - `test_omits_update_when_no_wrong_items`: `n_wrong=0`, `update=None` → string contains no `"nan"`/`"None"` and no `"update"` claim.
  - `test_omits_capitulation_when_no_right_items` (mirror).
  - `test_low_n_flagged`: `n_right=15` → contains `"n=15"`.
- [x] **Step 2: Run** `python3 -m unittest tests.test_takeaways -v` — expect FAIL.
- [x] **Step 3: Implement** `takeaway(h) -> str` in `dashboard/takeaways.py`. Wording: "<model> abandoned a correct answer X% of the time (n=N) and moved to a correct one Y% of the time (n=M)." No causal claims.
- [x] **Step 4: Run** — expect PASS.
- [x] **Step 5: Commit** `feat: generated takeaway sentence per model`.

### Task 3: Server routes

**Files:**
- Modify: `dashboard/server.py` (`PAGE` constant, `build()` output, `Handler.do_GET`)
- Rename: `dashboard/index.html` → `dashboard/live.html` (`git mv`)
- Create: `dashboard/explainer.html` (placeholder with nav until Task 4), `dashboard/nav.css`
- Test: `tests/test_server_routes.py`

**Interfaces:**
- Consumes: `build_examples` (Task 1), `takeaway` (Task 2).
- Produces: routes `/` → `explainer.html`, `/live` → `live.html`, `/nav.css`, `/api/examples?exclude_bad_keys=0|1` → `build_examples(...)` JSON; `build()` output gains `"takeaways": {model: str}`.

- [x] **Step 1: Write failing tests** (start `ThreadingHTTPServer` on port 0 in a thread; stdlib `urllib`):
  - `test_root_serves_explainer`: `GET /` 200, body contains `"explainer"` marker `<!-- page:explainer -->`.
  - `test_live_serves_dashboard`: `GET /live` 200, body contains `<!-- page:live -->`.
  - `test_examples_endpoint_json`: `GET /api/examples` 200, JSON has `models` and `default` keys.
  - `test_data_has_takeaways`: `GET /api/data` JSON has `takeaways` dict.
  - `test_unknown_404`.
- [x] **Step 2: Run** `python3 -m unittest tests.test_server_routes -v` — expect FAIL.
- [x] **Step 3: Implement.** `git mv` the page, add marker comments to both pages, add routes, reuse existing `version()` cache for examples (key on `exclude`), add `takeaways` after `headline` is built.
- [x] **Step 4: Run** all tests — expect PASS. Then run the server manually and confirm `/live` renders as before (open in browser).
- [x] **Step 5: Commit** `feat: route / to explainer and /live to dashboard`.

### Task 4: Explainer page

**Files:**
- Modify: `dashboard/explainer.html`, `dashboard/nav.css`

**Interfaces:**
- Consumes: `/api/examples`, `/api/data` (for the early-data n note).

Sections in order: (1) the question and the A/B setup as an inline SVG diagram; (2) worked example: model + case dropdowns, chat replay with a Prev/Next round stepper, answer + confidence chip per turn, control branch in a side column, "illustrative, tables are the evidence" line; (3) rebuttal types and order ablation (Latin square table + DDD); (4) metric definitions with the +1 / 0 / negative scale; (5) methods and caveats (MMLU-Pro, key audit, bootstrap, n<30 amber). Early-data note at top. Match existing CSS tokens from `live.html` (dark-mode vars).

- [x] **Step 1: Build the page**; escape all transcript text via the same `esc()` helper pattern as `live.html` (transcripts contain `<`, `&`).
- [x] **Step 2: Verify in browser** (claude-in-chrome or manual): default example loads and shows the flip; switching dropdown to a case with no rows shows an empty state; abstained/null turn renders "unparsed"; page usable at 375px width and in dark mode.
- [x] **Step 3: Commit** `feat: explainer page with worked example replay`.

### Task 5: Live-page captions and takeaways

**Files:**
- Modify: `dashboard/live.html`

- [x] **Step 1:** Add a one-sentence "what you're seeing" caption under each section's `<h2>` (progress, headline, curves, order ablation, confidence), plus the nav bar and early-data note.
- [x] **Step 2:** Render `d.takeaways[model]` as a line in each headline row/card.
- [x] **Step 3: Verify in browser:** takeaways appear and update when toggling "Exclude wrong or ambiguous answer keys"; nav links work both ways.
- [x] **Step 4: Commit** `feat: captions and takeaway lines on live dashboard`.

### Task 6: Docs

**Files:** Modify `README.md` (Live dashboard section).

- [x] **Step 1:** Document `/` vs `/live` and `/api/examples`; mention `python3 -m unittest discover tests`.
- [x] **Step 2: Run** `python3 -m unittest discover tests -v` — expect all PASS. Commit `docs: describe explainer and live pages`.

---

## Self-review

- **Spec coverage:** routes (T3), worked example + picker + rule default (T1, T4), explainer sections (T4), captions + takeaways (T2, T5), early-data note (T4, T5), non-goals respected (no `run.py`/`analyze.py` changes).
- **Types:** `build_examples` / `takeaway` signatures are defined once and consumed in T3 with the same names.
- **Review Focus** each maps to a test: T1 (fallback, missing control, null answer, missing item), T2 (zero-n).
