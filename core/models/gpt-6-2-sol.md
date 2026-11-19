---
id: gpt-6-2-sol
name: GPT-6.2 Sol
vendor: openai
family: gpt
status: current
released: 2026-11                # 2026-11-17, alongside GPT-6.2 Astra
as_of: 2026-11-19
confidence: low                  # no hands-on review yet; scores and fits carried from gpt-6-1-sol at the same price

api_ids: [gpt-6.2-sol]
access:
  subscriptions: [chatgpt-plus, chatgpt-pro]   # OpenAI's Codex page doesn't name plans; assumed same as GPT-6.1 Sol
  api: true                      # Responses, Chat Completions, Batch; not Realtime, Assistants or fine-tuning
  harnesses: [codex, cursor, opencode, t3-code, openclaw, hermes]   # codex confirmed (`codex -m gpt-6.2-sol`); the rest inherited from GPT-6.1 Sol, unverified for 6.2; cursor access to OpenAI models reportedly revoked (see gpt-6-1-sol.md)
  invoke_via: [codex-cli, cursor-cli, opencode-cli, openclaw-cli, hermes-cli, openai-api]   # openai-api added now that the API id is confirmed; the others unverified for 6.2

pricing_per_mtok:
  input: 2
  output: 10
  cache_read: 0.10
  cache_write: 2.50              # 30-minute retention; 5 for 12-hour
context_window: 1050000          # 922K max input, 128K max output; Codex defaults to 500K
notes_on_cost: >
  Same price as GPT-6.1 Sol: $2 / $10, cache reads $0.10. It cost about 1/8
  of Fable 5.2 to run Theo's benches, where it placed a close second to 6.2
  Astra. Above 272K input, input and cache double and output is 1.5x. Fast
  mode 2x; Ultrafast 3x until 2027-02-28, then 6x; Batch half. Cache reads
  dominate agent workloads, so the $0.10 matters more than the headline. On a
  Codex subscription the marginal cost is close to zero.

effort:
  levels: [low, medium, high, xhigh, max]
  default: low                   # carried from 6.1 Sol; OpenAI's API pages don't state one, and new ChatGPT Sol chats reportedly start at Light on consumer plans (summary of OpenAI's Codex models page, unverified)
  avoid: [xhigh, max]
  notes: >
    Carried from 6.1 Sol: low for scoped and bulk work, high for review and
    investigation. Not yet measured on 6.2 Sol; OpenAI's charts show xhigh and
    max dips for 6.2 Astra, as 6.1 Sol had.

scores:                          # all carried from gpt-6-1-sol; re-score once there is a hands-on review
  intelligence: 7
  taste: 2
  floor: 6
  thoroughness: 9
  cost_efficiency: 10
  speed: 8
  computer_use: 8
  orchestration: 4

tasks:
  quick-fix:      {fit: good, note: "carried from 6.1 Sol; cheapest strong option for scoped, specified changes; keep a Claude review before merge"}
  feature:        {fit: ok,   note: "carried from 6.1 Sol; prefer Opus or Fable"}
  long-run:       {fit: poor, note: "carried from 6.1 Sol (stalls, never escalates); 6.2 Astra's blocking and looping may share the cause"}
  frontend:       {fit: poor, note: "carried from 6.1 Sol"}
  review:         {fit: best, note: "carried from 6.1 Sol, the proven cheap cross-family reviewer; 6.2 Astra is the stronger finder at 4x the price"}
  investigate:    {fit: best, note: "carried from 6.1 Sol; have Claude restate its root cause if the report is hard to read"}
  analyze:        {fit: good, note: "carried from 6.1 Sol"}
  bulk:           {fit: best, note: "carried from 6.1 Sol; lowest cost per completed task on mechanical work"}
  research:       {fit: ok,   note: "no direct evidence"}
  computer-use:   {fit: good, note: "carried from 6.1 Sol; escalate hard flows to 6.2 Astra"}
  copy:           {fit: poor, note: "carried from 6.1 Sol"}
  3d-games:       {fit: ok,   note: "carried from 6.1 Sol"}
  prompt-writing: {fit: unknown, note: "no evidence"}
  babysit:        {fit: ok,   note: "carried from 6.1 Sol; needs anti-scope-creep rules and an escape hatch"}
  orchestrate:    {fit: poor, note: "carried from 6.1 Sol"}

role_hints:
  as_primary: "Primary only if the work is mostly review, investigation, and scoped or bulk tasks; otherwise keep a Claude driver that calls it."
  as_subagent: "Cheap cross-family reviewer and investigator, scoped implementer, routine computer-use operator. Treat as 6.1 Sol until measured."
  never_for: ["frontend, UI, or user-facing copy", "game mechanics and feel", "long unattended builds", "leading other agents", "xhigh or max effort"]
---

## Summary

GPT-6.2 Sol is OpenAI's "efficient, versatile model for everyday work",
released with 6.2 Astra at 6.1 Sol's price. There is almost no hands-on
evidence yet. Theo placed it "a very close second" to 6.2 Astra on his
benches at about 1/8 of Fable 5.2's cost. OpenAI's post says many employees
use it as their default, and Theo hears they use it more than Astra. Until someone reviews it properly, this
profile treats it as GPT-6.1 Sol: the cheap reviewer, investigator and scoped
implementer, kept away from UI, copy, long runs and leading agents. Every
score and task fit is carried over from `gpt-6-1-sol.md`.

## Strengths

- **Bench results at a low price.** "62 Souls a very close second place at a
  way cheaper price," costing "almost as low as an eighth" of Fable 5.2 to run
  his benches. ([AS62 0:38](https://youtu.be/9KvI-zg4mfo?t=38))
- **Preferred inside OpenAI.** "Many employees at OpenAI are using Soul as
  their default model for both technical and non-technical tasks," mostly in
  an ultra-fast mode. ([AS62 15:10](https://youtu.be/9KvI-zg4mfo?t=910);
  [AS62 15:19](https://youtu.be/9KvI-zg4mfo?t=919))
- **Same price as 6.1 Sol**, with a larger Codex default context (500K vs
  Astra's 272K). (OpenAI pricing and model pages, fetched 2026-11-19.)
- Everything else in `gpt-6-1-sol.md § Strengths` is assumed, not shown.

## Weaknesses and failure modes

- **Unmeasured.** No review, UI, long-run, or computer-use evidence for 6.2.
  Theo: "I have spent much less time with Soul than I have with Astra."
  ([AS62 4:11](https://youtu.be/9KvI-zg4mfo?t=251))
- **Assume 6.1 Sol's failure modes:** poor UI and filler copy, stalls on long
  unattended builds without asking for help, code harder to merge than
  Opus's. See `gpt-6-1-sol.md § Weaknesses and failure modes`.
- **Watch for 6.2 Astra's problems.** 6.2 Astra asks the human about
  subagent-level details and writes hard-to-parse reports. Whether 6.2 Sol
  shares this is unknown; check the first few reports by hand.
- **Simon Willison** found it weaker than Fable 5.2 on his coding test
  ([simonwillison.net](https://simonwillison.net/2026/Nov/17/gpt62-astra-and-sol/)).

## How to prompt it

Use `gpt-6-1-sol.md § How to prompt it` unchanged: simple and literal, scoped
tightly, an explicit escape hatch because it won't ask for help, "nothing
found" as a valid answer, and unconfirmed findings marked. Add the 6.2
Astra line until its reports prove readable:

> "Start your final message with the answer in one or two plain sentences.
> Don't ask the reader about internal details they haven't seen."

## Routing guidance

Route it as 6.1 Sol (see `gpt-6-1-sol.md § Routing guidance`):

- **Route here for:** review of Claude-written code, investigation and
  triage, scoped and bulk implementation where cost matters, routine computer
  use.
- **Do not route here for:** frontend, copy, game feel, long unattended
  builds, leading agents, edge-of-capability work (escalate to Opus, or to
  6.2 Astra for computer use and 3D).
- **6.1 Sol or 6.2 Sol?** Same price and, for now, the same scores, so the
  generator lists 6.1 Sol first and 6.2 Sol as its fallback (ties fall back to
  the profile id). That is the right order until 6.2 Sol has evidence of its
  own: 6.1 is the measured one. Neither is deprecated.

## Cost notes

- **API:** $2 in, $10 out, $0.10 cache read, $2.50 cache write (30 minutes)
  or $5 (12 hours). Above 272K input: $4 / $0.20 / $15.
- **Modes:** fast 2x ($4 / $0.20 / $20); Ultrafast 3x through 2027-02-28,
  then 6x; Batch half ($1 / $0.05 / $5).
- **Versus 6.2 Astra:** a quarter of the price per token and per cache read.
  On Simon Willison's single max-effort prompt, 13.69¢ vs 88.71¢.
- **Effort for value:** low for scoped and bulk work, high for review and
  investigation (carried from 6.1 Sol).

## Evidence

- AS62: "Astra 6.2 Is Unusable", Theo (t3.gg), YouTube,
  https://youtu.be/9KvI-zg4mfo, `research/gpt-releases.md` Video 3 § 5: the
  only first-hand 6.2 Sol remarks (bench placing and cost, OpenAI staff
  preference).
- OpenAI model page for `gpt-6.2-sol`, the pricing page and the deprecations
  page, fetched 2026-11-19: API id, prices, limits, effort levels, Codex
  default context, and that GPT-6.1 Sol is still listed at the same price
  and not deprecated.
- Simon Willison, https://simonwillison.net/2026/Nov/17/gpt62-astra-and-sol/:
  price, per-prompt cost, and a weaker result than Fable 5.2 on his coding test.
- **Everything else is inherited from `gpt-6-1-sol.md` and unverified for 6.2.**
  Re-score when a hands-on review appears; Theo offered to make one.

### Score rationale

All eight scores are copied from `gpt-6-1-sol.md`; nothing in the 6.2
evidence moves any axis yet.

- **intelligence 7:** 6.1 Sol's. "A very close second" to 6.2 Astra on
  Theo's benches fits it; one sentence is not enough to raise it.
- **taste 2:** 6.1 Sol's; no 6.2 UI or copy evidence.
- **floor 6:** 6.1 Sol's; no 6.2 evidence either way.
- **thoroughness 9:** 6.1 Sol's; no 6.2 review evidence.
- **cost_efficiency 10:** same price as 6.1 Sol, and about 1/8 of Fable
  5.2's cost on Theo's benches.
- **speed 8:** 6.1 Sol's; no 6.2 speed figures.
- **computer_use 8:** 6.1 Sol's; no 6.2 evidence.
- **orchestration 4:** 6.1 Sol's; no 6.2 evidence.
