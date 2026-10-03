---
id: grok-4-7
name: Grok 4.7
vendor: xai
family: grok
status: current
released: 2026-09                # 2026-09-21
as_of: 2026-10-02
confidence: medium               # ID, price, context from xAI docs; review results from Theo's transcripts; speed sources conflict

api_ids: [grok-4.7]              # no aliases
access:
  subscriptions: [supergrok, supergrok-heavy, x-premium-plus]   # unverified (third-party); also included in Cursor (all plans) and GitHub Copilot Pro and up
  api: true
  harnesses: [grokbuild, cursor, opencode]
  invoke_via: [grok-cli, xai-api]

pricing_per_mtok:
  input: 2                       # doubles at 200K tokens or more; US regional endpoint +10%
  output: 6
  cache_read: 0.50
  cache_write: null
context_window: 500000           # xAI docs: "no text output limit"
notes_on_cost: >
  Cheap list price, expensive tasks. It is very verbose: about 81K output tokens
  per Artificial Analysis task at xhigh (+196% vs GPT-6 Astra), so AA cost per
  task is $3.74, about 2x Opus 5.5 at high. Cache reads at $0.50 are 5x Sol's.
  Prices double for requests of 200K tokens or more. A "fast" variant (2x price)
  exists only in Cursor and Grok Build. Inside Cursor or Copilot plans the
  per-token cost is hidden, which is where it is cheapest to use.

effort:
  levels: [low, medium, high, xhigh]
  default: high
  avoid: [xhigh]
  notes: >
    high is the vendor default. AA's 81K tokens per task was measured at xhigh;
    avoid it unless a review needs the extra depth. No kit-specific evidence for
    low or medium.

scores:
  intelligence: 6
  taste: 4
  floor: 5
  thoroughness: 7
  cost_efficiency: 3
  speed: 5
  computer_use: 3
  orchestration: 3

tasks:
  quick-fix:      {fit: ok,      note: "Works as a second-opinion implementer; token hunger makes it poor value next to Sol at low or Opus at medium."}
  feature:        {fit: ok,      note: "AA Coding Agent Index 56 in Grok Build (4th, behind Fable, Astra, Opus 5); use for arena runs, not as the implementer of record."}
  long-run:       {fit: unknown, note: "xAI says it was trained on 'work that takes many hours'; no hands-on evidence, floor unknown."}
  frontend:       {fit: unknown, note: "No evidence; AA notes a presentation-quality regression."}
  review:         {fit: good,    note: "Second overall on Theo's review bench (8 supported findings); a third-family opinion beside Sol/Astra. Token-hungry: cap effort at high."}
  investigate:    {fit: ok,      note: "Arena-style second opinion on hard bugs; single-pass accuracy trails Claude Code and Codex (third-party)."}
  analyze:        {fit: good,    note: "80.7 on the 'improve T3 Code' bench vs 87.4 Sol and 83.8 Astra; avoid long-document or large-spec reading (LCR regression)."}
  bulk:           {fit: poor,    note: "Verbosity makes it about 2x Opus 5.5's cost per task; use a cheap tier."}
  research:       {fit: ok,      note: "Strong on agentic knowledge work (AA-Briefcase near Opus 5 and Fable 5.1), but regressed on long-document reasoning."}
  computer-use:   {fit: unknown, note: "No evidence."}
  copy:           {fit: unknown, note: "No evidence."}
  3d-games:       {fit: unknown, note: "No evidence."}
  prompt-writing: {fit: unknown, note: "No evidence."}
  babysit:        {fit: unknown, note: "No evidence; token hunger makes polling loops costly on API."}
  orchestrate:    {fit: poor,    note: "No evidence of leading agents; Grok Build has a subagent view, but the model is untested as a lead."}

role_hints:
  as_primary: "Not a primary model in this kit."
  as_subagent: "Third-family code reviewer and auditor beside Sol/Astra, and an arena competitor on hard bugs."
  never_for: ["bulk or cheap work", "long-document or large-spec reading", "sole reviewer of record", "leading other agents", "xhigh effort on API billing"]
---

## Summary

Grok 4.7 is xAI's current model and, in this kit, a third-family reviewer: it
placed second on Theo's code-review bench and scored 80.7 on his "improve T3
Code" audit, behind 6.1 Sol and Astra. Use it for a review or audit opinion from
a lab other than Anthropic and OpenAI, and as an arena competitor on hard bugs.
It is very token-hungry, so it is not a cheap or bulk model despite its list
price. This profile comes mostly from vendor docs and aggregators, plus two
review results from Theo's transcripts, not hands-on testing; test it on your own
tasks before trusting it.

## Strengths

- **Review.** On Theo's informal review bench it had 8 supported findings and
  "came second overall, which surprised him" (`research/claude-supplemental.md §
  Video 1 › 5. Subagents, orchestration, delegation, verification, review, model
  choice`). "Consider using Grok for your reviews, too" (same section). It does
  better than Opus and Fable at finding improvements, "likely helped by
  Cursor/Bugbot review data" (`research/claude-releases.md § Video 2: Claude Opus
  5.5 › 3. Weaknesses, pitfalls and misconceptions`).
- **Audit bench.** 80.7 on "find opportunities to improve T3 Code" vs 87.4 for 6.1
  Sol and 83.8 for Astra (`research/gpt-releases.md § Deep code review, auditing,
  and investigation: his main use`).
- **Decomposition planning.** Grok 4.7 "once outperformed Fable on an earlier
  version of" Theo's PR-decomposition bench; it is not ranked on the current
  version (`research/claude-releases.md § Video 3: Claude Sonnet 5.5 › 6.
  Subagents, orchestration, delegation and verification`).
- **Coding agent index.** AA Coding Agent Index 56 in Grok Build, 4th behind Fable
  5.1, GPT-6 Astra and Opus 5 (`research/model-gaps.md § 3a. Grok 4.7`).
- **Other benches.** AA Intelligence Index 46; DeepSWE about 71–73%;
  Terminal-Bench 4.0 33%; Senior SWE-Bench pass@3 40.0% (Snorkel, 6th);
  CursorBench 4.0 46.3% (same section).
- **Agentic knowledge work.** AA-Briefcase just behind Opus 5 and Fable 5.1.
- **Long runs (vendor claim).** xAI trained it on "work that takes many hours".
  No hands-on confirmation.
- **Wide availability.** Cursor (all plans), GitHub Copilot Pro and up, Grok
  Build, OpenCode and Pi.

## Weaknesses and failure modes

- **Token hunger.** About 81K output tokens per AA task at xhigh (+125% vs Grok
  4.6); AA cost per task $3.74, about 2x Opus 5.5 at high. "The cheap list price
  does not mean cheap tasks" (`research/model-gaps.md § 3a`).
- **Long-document regression.** AA-LCR down 3.7 points; research says not to use
  it to read long documents or review large specs.
- **Presentation quality regressed** (AA).
- **Single-pass accuracy trails Claude Code and Codex** (third-party review,
  WinBuzzer; unverified).
- **Precision vs Claude.** OpenAI models "and even Grok 4.7 find more issues";
  Claude models find fewer but well-vetted ones
  (`research/claude-supplemental.md § 7. Model comparisons`). Expect some noise;
  have a Claude model or the implementer filter findings.
- **Speed is unclear.** AA's leaderboard shows 79 tok/s at xhigh; AA's launch
  article says about 188. Conflict, unverified.
- **Lower floor expected.** Theo: the higher floor "is the thing that you don't
  get as much from ... other labs other than anthropic and open AI generally"
  (`research/model-selection.md § Video 1 › 2. Models mentioned`). General, not
  measured on 4.7.

## How to prompt it

No Grok-specific prompting evidence. From the review guidance that applies to
every reviewer in the kit:

- Name the review target (diff, branch, PR) and the question.
- Ask it to mark what it could not confirm, and give it a way to verify (tests,
  a running app) (`research/claude-supplemental.md § Video 1 › 5`).
- Make "nothing found" a valid answer.
- Cap effort at `high` and bound the scope, to limit token use.
- Headless: `grok -p "<task>" -m grok-4.7 --output-format streaming-json`. API is
  OpenAI-compatible at `https://api.x.ai/v1/chat/completions`; the
  `reasoning_effort` field name is unverified for xAI.

## Routing guidance

Route here for:
- A third-family code review or audit of Claude- or OpenAI-written code, beside
  or instead of 6.1 Sol / Astra.
- Arena or second-opinion runs on hard bugs, where model diversity helps.
- Long runs only if the user already pays for Cursor or Copilot and wants to
  try it there (unverified; no hands-on evidence).

Do not route here for:
- Bulk, cheap or high-volume work.
- Reading long documents or large specs.
- Being the only reviewer, or the implementer of record for code that must land.
- Leading other agents.

Handoff patterns:
- **Claude builds, Sol and Grok review.** Send the same diff to 6.1 Sol and Grok
  4.7; the implementer (Opus/Fable) judges the merged findings.
- **Grok as the Sol substitute.** If the user has no OpenAI access, Grok is the
  cross-family reviewer for Claude-written code.

## When this beats the frontier

- When a review needs a lab other than Anthropic and OpenAI; it finds things
  same-family reviewers miss and placed above Fable and Opus at finding issues.
- When it is bundled in a Cursor or Copilot plan the user already pays for, so
  its token hunger costs nothing extra.

## Cost notes

- $2 / $0.50 / $6 per MTok under 200K tokens; double at 200K or more; US regional
  endpoint +10%.
- AA: $3.74 per task at xhigh, about 2x Opus 5.5 at high. Use `high` to cut that.
- Cheapest through bundles: Cursor (all plans), GitHub Copilot Pro/Pro+/Max/
  Business/Enterprise, or a SuperGrok plan (tiers and prices unverified: X
  Premium+ $40, SuperGrok $30, SuperGrok Heavy $299 per month).
- The "fast" variant costs 2x (1.5x for long context) and is only in Cursor and
  Grok Build.
- **grok-build-0.1** ($1 / $0.20 / $2, 256K) is a separate cheaper coding model
  with no independent benchmarks; it is not this profile and needs its own trial.

## Evidence

- `research/model-gaps.md § Naming corrections` (Grok 4.7 current; Grok Build is
  the CLI; grok-build-0.1 is a separate model; "SpaceXAI" branding),
  `§ At-a-glance comparison`, `§ 3a. Grok 4.7`, `§ 3b. Grok Build (agent CLI) and
  grok-build-0.1 (model)`, `§ Suggested routing-table shortlist`.
- `research/claude-supplemental.md § Video 1 › 5. Subagents, orchestration,
  delegation, verification, review, model choice` (review bench, "Grok second")
  and `§ 7. Model comparisons`.
- `research/gpt-releases.md § Deep code review, auditing, and investigation: his
  main use` (80.7).
- `research/claude-releases.md § Video 2: Claude Opus 5.5 › 3. Weaknesses,
  pitfalls and misconceptions` (Grok above Opus/Fable on the audit bench) and
  `§ Video 3: Claude Sonnet 5.5 › 6. Subagents, orchestration, delegation and
  verification` (decomposition bench).
- URLs: [xAI Grok 4.7 docs](https://docs.x.ai/developers/grok-4-7),
  [xAI models and pricing](https://docs.x.ai/docs/models),
  [AA: Benchmarking Grok 4.7](https://artificialanalysis.ai/articles/benchmarking-grok-4-7),
  [AA leaderboard](https://artificialanalysis.ai/leaderboards/models),
  [WinBuzzer](https://winbuzzer.com/2026/09/23/grok-4-7-coding-gains-higher-token-use-a004-xcxwbn/),
  [Snorkel Senior SWE-Bench](https://snorkel.ai/blog/grok-4-7-on-senior-swe-bench-strong-pass3-cheaper-cost/),
  [Oracle OCI model page](https://docs.oracle.com/en-us/iaas/Content/generative-ai/x-ai-grok-4-7.htm),
  [ai-tldr](https://ai-tldr.dev/models/grok-4-7/),
  [Grok Build docs](https://docs.x.ai/build/overview),
  [Developers Digest guide](https://www.developersdigest.tech/blog/grok-build-developer-guide-2026),
  [OpenCode providers](https://opencode.ai/docs/providers/).
- **Unverified:** speed (79 vs 188 tok/s); subscription tiers (third party);
  `reasoning_effort` field name on the xAI API; single-pass accuracy claim
  (WinBuzzer); `grok exec/plan/goal/arena` subcommands. The review-bench rank is
  from one informal bench "in quotes" and the exact rank order beyond "second" is
  not stated.

### Score rationale

| Axis | Score | Why |
|---|---|---|
| intelligence | 6 | AA 46 vs 54 for Opus 5.5; Coding Agent Index 4th behind the frontier; Terminal-Bench 4.0 33%. |
| taste | 4 | No design evidence; AA notes a presentation-quality regression. |
| floor | 5 | No hands-on long-run evidence; Theo expects lower floors outside Anthropic/OpenAI; single-pass accuracy trails (unverified). |
| thoroughness | 7 | Second on Theo's review bench (8 supported findings) and 80.7 on the audit bench, above Opus/Fable but below Sol (9) and Astra (10). |
| cost_efficiency | 3 | $3.74 per AA task, about 2x Opus 5.5 at high, despite low list prices; better only inside bundled plans. |
| speed | 5 | Sources conflict (79 vs 188 tok/s) and verbosity adds wall-clock. |
| computer_use | 3 | No evidence. |
| orchestration | 3 | No evidence of leading agents. |
