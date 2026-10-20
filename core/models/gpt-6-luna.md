---
id: gpt-6-luna
name: GPT-6 Luna
vendor: openai
family: gpt
status: current
released: 2026-09                # about 2026-09-22, alongside GPT-6 Sol (from Theo's GPT-6.1 Sol video)
as_of: 2026-10-19
confidence: low                  # web research only; one aggregator number; Theo: 6.0 Sol and Luna "weren't that good"

api_ids: [gpt-6-luna]
access:
  subscriptions: [chatgpt-plus, chatgpt-pro]   # unverified: research does not confirm Luna in ChatGPT/Codex plans
  api: true
  harnesses: [codex, cursor, opencode, openclaw, hermes]          # codex and cursor availability unverified for Luna specifically
  invoke_via: [codex-cli, openai-api, openclaw-cli, hermes-cli]   # openclaw, hermes / openclaw-cli, hermes-cli added 2026-10-19: OpenAI provider (ChatGPT OAuth or API key); this model's availability there unverified

pricing_per_mtok:
  input: 0.10
  output: 0.50
  cache_read: null               # unverified: not found
  cache_write: null
context_window: 1050000          # 128K max output
notes_on_cost: >
  The cheapest decent model Artificial Analysis has measured: Intelligence Index
  38 at max effort for about $0.07 per index task, vs $0.32 for GPT-6.1 Sol (50)
  and $1.82 for Opus 5.5 at high (54). Cache-read price is unverified, which
  matters because agent workloads are mostly cache reads. Cheap per task only
  holds while it finishes in few steps; on hard multi-step work a low-index
  model can take more steps and cost more than Sol.

effort:
  levels: [none, low, medium, high, xhigh, max]   # "none through max"; intermediate levels assumed to match GPT-5.6, unverified
  default: high
  avoid: [none, max]
  notes: >
    No effort-specific evidence. Start at high (kit default for unprofiled
    models). AA's 38 was measured at max, so high may score somewhat lower;
    max still breaks the kit's never-max rule. none drops reasoning entirely.

scores:
  intelligence: 4
  taste: 2
  floor: 4
  thoroughness: 4
  cost_efficiency: 8
  speed: 6
  computer_use: 3
  orchestration: 2

tasks:
  quick-fix:      {fit: ok,      note: "Narrow, fully specified edits with a test to prove them; review before merge. Sol at low is the safer cheap choice."}
  feature:        {fit: poor,    note: "Must-land and wide; AA 38 and Theo's 'not that good'. Opus or Sol."}
  long-run:       {fit: poor,    note: "No evidence; low-index models lose long runs."}
  frontend:       {fit: poor,    note: "Inferred from the OpenAI family's weak UI taste (Sol, Astra); no direct evidence."}
  review:         {fit: poor,    note: "Use 6.1 Sol, which is cheap and proven; Luna at most as a lint-like pre-pass."}
  investigate:    {fit: poor,    note: "No evidence; root-causing needs a higher ceiling."}
  analyze:        {fit: ok,      note: "Cheap first-pass summaries of large codebases (1M context); verify conclusions with a stronger model."}
  bulk:           {fit: good,    note: "Mechanical, clear-spec, verifiable work: codemods, data munging, log digging, large-document reading. Check output programmatically."}
  research:       {fit: ok,      note: "Cheap summarisation of supplied docs; no evidence on web research."}
  computer-use:   {fit: unknown, note: "Not stated whether Luna supports the computer-use tool."}
  copy:           {fit: poor,    note: "Inferred from OpenAI filler-copy tendencies; no direct evidence."}
  3d-games:       {fit: unknown, note: "No evidence."}
  prompt-writing: {fit: unknown, note: "No evidence."}
  babysit:        {fit: poor,    note: "Must-land loop; needs a higher floor."}
  orchestrate:    {fit: poor,    note: "Not a lead model."}

role_hints:
  as_primary: "Not a primary model."
  as_subagent: "Cheap fan-out worker for bulk mechanical work, log digging and large-document reading where output is verified programmatically."
  never_for: ["anything that must land without review", "code review of record", "frontend, UI or copy", "long unattended runs", "leading other agents", "max effort"]
---

## Summary

GPT-6 Luna is OpenAI's very cheap tier: AA Intelligence Index 38 for about $0.07
per task, the cheapest decent model measured. In this kit it is a fan-out worker
for bulk, mechanical, verifiable work: codemods, log digging, reading large
documents, data munging. It is not for anything that must land, for review, or
for leading agents. This profile comes from vendor docs and aggregators, not
hands-on testing; test it on your own tasks before trusting it. The only
hands-on comment in the research is Theo's that 6.0 Sol and Luna "weren't that
good".

## Strengths

- **Price.** $0.10 in / $0.50 out per MTok, 1/20 of 6.1 Sol's list price
  (`research/model-gaps.md § 5. OpenAI Sol naming › GPT-6 Luna`).
- **Measured cost per task.** About $0.07 per AA task at index 38, "the cheapest
  decent model measured" (same section; `§ At-a-glance comparison`). Unverified
  beyond AA.
- **Large window.** 1.05M context and 128K output, the same limits as 6.1 Sol.
- **Full effort range.** `none` through `max`, so it can be tuned down for
  trivial transforms.
- **OpenAI tooling.** Same API and (per the caller's bridge set) Codex CLI as
  Sol, so a Sol bridge can drop to Luna by changing the model id.

## Weaknesses and failure modes

- **Low index.** 38 vs 50 for 6.1 Sol and 54 for Opus 5.5. Expect it to miss on
  anything that needs judgment.
- **Theo's verdict.** OpenAI "rushed out" GPT-6 Sol and GPT-6 Luna, which "weren't
  that good", so he made no videos about them ([SOL61 0:11](https://youtu.be/vu8X3YroB-w?t=11)). This is one line, not an evaluation.
- **Cheap per token is not cheap per task on hard work.** OpenRouter's cost
  router sent most traffic to a cheap model, took 104 steps vs 19 for Astra low,
  and cost more ([SOL61 19:42](https://youtu.be/vu8X3YroB-w?t=1182)).
  That test did not use Luna, but the risk applies to any low-index model.
- **Behind Haiku 5.5 on Anthropic's launch benchmarks.** Terminal-Bench 4.0: Luna
  16.4% vs Haiku 5.5 39.2%. OSWorld 2.1: Luna 48.9% vs Haiku 5.5 72.4% partial
  credit. These are Anthropic's numbers, unverified ([H55 9:18](https://youtu.be/38_6C0dkKmU?t=558);
  [H55 9:55](https://youtu.be/38_6C0dkKmU?t=595)).
- **Unknowns.** Cache-read price, speed, Codex availability and computer-use
  support are not confirmed.
- **Family traits (inferred).** Sol and Astra have weak UI taste and write filler
  copy; assume Luna does too until shown otherwise.

## How to prompt it

No Luna-specific evidence. Treat it like Sol, only more so:

- Simple, literal prompts: the target, the task, the done state. "The prompt
  should be much simpler" than a Claude prompt (said of Codex models;
  `core/models/gpt-6-1-sol.md § How to prompt it`).
- One mechanical transformation per call, with an exact output format (JSON
  schema, patch, list).
- Make "nothing found" or "cannot do" a valid answer, and give a step or time
  budget.
- Verify every result programmatically (tests, type-check, schema validation,
  diff checks) before anything uses it.

## Routing guidance

Route here for:
- Bulk mechanical edits with a clear spec and a programmatic check.
- Log digging, grep-and-summarise, reading large documents or many files and
  extracting facts.
- Cheap subagent fan-out where many short tasks matter more than depth and a
  stronger model or a test suite judges the results.

Do not route here for:
- Anything that must merge or ship without review.
- Review, investigation, planning, frontend, copy, long runs, leading agents.
- Hard multi-step agent tasks where step count drives cost; use 6.1 Sol at low.

Against Haiku 5.5:
- Theo's Haiku video places Luna as "cheaper always, dumber always" than Haiku
  5.5 on Artificial Analysis cost vs intelligence. His cross-vendor value line
  runs Luna, then GPT-6.1 Sol, then Opus 5.5. In an Anthropic-only environment,
  Haiku 5.5 now fills Luna's slot ([H55 16:00](https://youtu.be/38_6C0dkKmU?t=960); [H55 17:09](https://youtu.be/38_6C0dkKmU?t=1029)).

Handoff patterns:
- **Luna gathers, Opus/Sol ship.** Luna reads and extracts; Sol or Opus decides
  and implements ("cheap models gather information, expensive models ship",
  `docs/ARCHITECTURE.md`).
- **Escalate on miss.** If Luna's output fails the check once, rerun on 6.1 Sol
  (same CLI, same prompt) rather than retrying Luna.
- **Compare before committing.** Research suggests testing it against DeepSeek
  V4.1 Flash and Gemini 3.8 Flash on the user's own bulk tasks
  (`research/model-gaps.md § 5 › Routing`).

## When this beats the frontier

- High-volume, programmatically verified transforms where per-call cost
  dominates and each call is short.
- Reading and summarising very large inputs (up to about 1M tokens) for an
  orchestrator that will act on the summary.
- Wide fan-out of trivial subagent calls on an API budget.

## Cost notes

- $0.10 / $0.50 per MTok; cache-read and cache-write prices unverified.
- AA: about $0.07 per task at max effort. Kit default is high, which should be
  cheaper still; measure on your tasks.
- On a ChatGPT/Codex subscription the marginal cost may be near zero, but Luna's
  inclusion in Codex is unverified. If Codex is available, 6.1 Sol at low is
  already "effectively free" there and is the stronger choice.
- Count steps to completion, not list price; abandon Luna for any task class
  where it needs retries.

## Evidence

- `research/model-gaps.md § Naming corrections` (GPT-6 Luna "worth a profile of
  its own"), `§ At-a-glance comparison`, `§ 5. OpenAI Sol naming: GPT-5.6 Sol vs
  GPT-6.1 Sol (plus GPT-6 Luna)`, and `§ Suggested routing-table shortlist`
  (cheap/bulk tier).
- [SOL61 0:11](https://youtu.be/vu8X3YroB-w?t=11)
  ("weren't that good") and [SOL61 19:42](https://youtu.be/vu8X3YroB-w?t=1182).
- [H55 9:18](https://youtu.be/38_6C0dkKmU?t=558); [H55 9:55](https://youtu.be/38_6C0dkKmU?t=595) (Anthropic's Haiku 5.5 launch benchmarks
  vs Luna) and [H55 16:00](https://youtu.be/38_6C0dkKmU?t=960); [H55 17:09](https://youtu.be/38_6C0dkKmU?t=1029) (Luna "cheaper always, dumber always" than Haiku 5.5;
  cross-vendor value line).
- [OPUS55 3:29](https://youtu.be/jgGyX7MPPVg?t=209) ("Luna" = OpenAI cheap model
  released alongside GPT-6 Sol).
- URLs: [OpenAI models](https://developers.openai.com/api/docs/models),
  [AA leaderboard](https://artificialanalysis.ai/leaderboards/models),
  [Codex non-interactive docs](https://learn.chatgpt.com/docs/non-interactive-mode).
- **Unverified:** cached-input price; speed; AA figures (single aggregator);
  release date (from the video, not a vendor page); effort level list beyond "none through max";
  availability in Codex, Cursor and ChatGPT plans; computer-use support.

### Score rationale

| Axis | Score | Why |
|---|---|---|
| intelligence | 4 | AA 38 vs 54 for Opus 5.5; Theo: "weren't that good". |
| taste | 2 | No evidence; the OpenAI family scores 2–4 here and Luna is the smallest tier. |
| floor | 4 | No hands-on evidence; low-index models are inconsistent on anything wide. |
| thoroughness | 4 | No review evidence; cheap enough to sweep large inputs, but shallow. |
| cost_efficiency | 8 | About $0.07 per AA task, the cheapest decent model measured; held below Sol's 10 because step counts on hard work and cache pricing are unknown. |
| speed | 6 | No measured speed; small tiers are usually fast, so neutral until measured. |
| computer_use | 3 | Not stated whether it supports the tool; Sol (8) and Astra (10) lead the family. |
| orchestration | 2 | No evidence; not a lead model. |
