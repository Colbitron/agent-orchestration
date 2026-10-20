---
id: claude-haiku-5-5
name: Claude Haiku 5.5
vendor: anthropic
family: claude
status: current
released: 2026-10
as_of: 2026-10-19
confidence: medium               # official specs and prices (high); one launch-day video with a few hands-on runs; vendor benchmarks; no AA index number found

api_ids: [claude-haiku-5-5]      # Bedrock and Vertex ids not checked
access:
  subscriptions: [claude-pro, claude-max]   # Max verified (Theo used it on his Claude Code sub); Pro unverified
  api: true
  harnesses: [claude-code, cursor, opencode, t3-code, openclaw, hermes]   # claude-code verified on camera; cursor, opencode, t3-code unverified for this model
  invoke_via: [claude-cli, cursor-cli, openclaw-cli, hermes-cli]   # openclaw, hermes / openclaw-cli, hermes-cli added 2026-10-19: API key in both; Claude subscription OAuth is restricted or disallowed there, see the bridges

pricing_per_mtok:                # prompt <= 100K tokens; see notes_on_cost for the > 100K tier
  input: 0.10
  output: 0.50
  cache_read: 0.01
  cache_write: 0.125             # 5-minute write; 1-hour write is $0.20; batch $0.05 / $0.25
context_window: 1000000          # 128K max output
notes_on_cost: >
  Two price tiers. A request whose prompt is 100K tokens or less pays $0.10 in, $0.50 out,
  $0.01 cache read, $0.125 (5m) or $0.20 (1h) cache write. A request over 100K pays 5x on
  every line: $0.50 in, $2.50 out, $0.05 cache read, $0.625 / $1.00 cache write, batch
  $0.25 / $1.25. The prompt length counts cache reads and writes, and each request is priced
  on its own, so a long agent session crosses the line on every turn after it fills up.
  It is the only current Anthropic model without flat 1M-context pricing. The newer
  tokenizer counts about 30% more tokens than Haiku 4.5 for the same text. Claude Code
  writes 1-hour cache entries. Cheap per token is not cheap per completed task: when it
  cannot solve a problem it can burn more tokens than Opus would have used to solve it.

effort:
  levels: [low, medium, high, xhigh, max]
  default: high                  # kit default for subagent work (effort-levels.md §3); the API default is medium
  avoid: [max]
  notes: >
    Keep reasoning on; never pass thinking {type: disabled}. The API defaults to medium,
    which is enough for plain categorisation and reads; the kit routes Haiku subagents at
    high and tries xhigh for harder gathering and computer use. Theo's AA
    chart shows xhigh and max as the best value in Anthropic's range, but the kit's
    never-max rule stands until tested. low is untested for this model.

scores:
  intelligence: 5
  taste: 4
  floor: 3
  thoroughness: 3
  cost_efficiency: 7
  speed: 8
  computer_use: 3
  orchestration: 2

tasks:
  quick-fix:      {fit: poor, note: "Must land. Theo would not use it for code. Exception: a lead may fan out several Haiku attempts when a script can check each one."}
  feature:        {fit: poor, note: "Must land and wide. Terminal-Bench 4.0 39.2% vs Sonnet 5.5 70.6%; Anthropic says Sonnet and Opus stay better for complex agentic coding."}
  long-run:       {fit: poor, note: "Cornered itself on a rate limit and stalled; long sessions cross the 100K price tier on every turn; cost inversion when it fails slowly."}
  frontend:       {fit: poor, note: "With the Claude design skill 'usable, not great'; without it 'classic LLM design'. Fable or Opus."}
  review:         {fit: poor, note: "Called PRs 'merge ready' because GitHub checks were green; 'it didn't seem to audit them thoroughly itself'. Never a merge gate."}
  investigate:    {fit: ok,   note: "As an evidence gatherer for a lead's hypotheses ('vet four things to confirm it'), not as the root-causer. Lead owns the conclusion."}
  analyze:        {fit: ok,   note: "Codebase exploration and file finding for a lead, and categorising large sets (PRs, issues). Plans, decomposition and audits stay with Opus or Sol."}
  bulk:           {fit: good, note: "Categorisation, summaries, data gathering, many-attempts work with cheap programmatic verification. Reasoning on, prompt under 100K, check output by script."}
  research:       {fit: good, note: "Reading documentation, comparing open-source projects, gathering facts for a lead ('that is when Haiku is incredible'). Lead verifies before use."}
  computer-use:   {fit: ok,   note: "Trial only. OSWorld 2.1 72.4% partial credit at max (53.3% at medium) but 37.1% strict, below Opus 53.2%; vendor numbers; Theo had not tried it."}
  copy:           {fit: unknown, note: "No evidence. User-facing prose must land; Opus is the copy model."}
  3d-games:       {fit: poor, note: "Fish Slop: no mouse look, no sound, broken corners, wrong enemy timing. 'Its highs are a tenth as high' as Astra's."}
  prompt-writing: {fit: poor, note: "No direct evidence; inferred. Prompts and skills shape every later run and should come from a frontier model."}
  babysit:        {fit: poor, note: "Must-land poll loop. It said it would wait for a quota reset and never resumed, and it trusts green CI."}
  orchestrate:    {fit: poor, note: "Not a lead. Run as lead on the PR audit it stalled; Opus leading Haiku workers handled the same job."}

role_hints:
  as_primary: "Never. Theo: 'I won't be the one to pick it'; let Opus or Sonnet call it."
  as_subagent: "Cheap, fast, parallel worker for bounded, verifiable jobs: file search, data gathering, categorisation, reading docs, many attempts with programmatic checks. Reasoning on, prompt under 100K."
  never_for: ["primary or interactive model", "anything that must land without a stronger model's review", "code review or merge gating", "trusting CI status as an audit", "reasoning-off calls", "long agentic loops", "leading other agents", "max effort"]
---

## Summary

Haiku 5.5 is a subagent and an in-app worker, not a model to pick by hand. A
lead (Opus or Sonnet) sends it bounded, verifiable, parallel jobs: finding
files, gathering data, categorising, reading docs, and many cheap attempts
that a script can check. It is not for work that must land, for review as a
merge gate, for long loops, or as a primary model. Theo's verdict: "Anthropic
now has one small model that is sometimes worth using" ([H55 40:16](https://youtu.be/38_6C0dkKmU?t=2416)).

## Strengths

- **Price under 100K.** $0.10 in, $0.50 out, $0.01 cache read: 10x cheaper
  than Haiku 4.5 on input and output and 20x cheaper than Sonnet 5.5
  (Anthropic pricing page;
  [H55 6:07-6:32](https://youtu.be/38_6C0dkKmU?t=367)). Anthropic says it is "on average about 75% less money to run"
  than Haiku 4.5 ([H55 4:29](https://youtu.be/38_6C0dkKmU?t=269)).
- **Fast.** 100-200 tok/s depending on provider ([H55 10:16](https://youtu.be/38_6C0dkKmU?t=616)); Theo saw about 180
  tok/s in Claude Code on his subscription with reasoning on ([H55 11:34](https://youtu.be/38_6C0dkKmU?t=694)).
- **Parallel attempts beat one careful attempt on the right work.** Anthropic's
  egg-drop demo (single vendor run): Opus 5.5 alone took about 3.5 minutes, 25
  attempts, $0.47; Opus 5.5 with 10 Haiku 5.5 subagents took under a minute,
  86 attempts, $0.14 ([H55 22:17-23:20](https://youtu.be/38_6C0dkKmU?t=1337)). Theo: "for the subset of tasks where more
  attempts is more valuable than smart attempts ... Haiku 55 is going to
  slaughter. This is a small subset of work" ([H55 23:34-24:06](https://youtu.be/38_6C0dkKmU?t=1414)).
- **Gathering and checking for a smarter model.** "When the model is unsure
  about a theory and it wants to vet four things to confirm it or wants to go
  look at eight apps ... or read through a bunch of documentation ... That is
  when haiku is incredible" ([H55 33:16-33:41](https://youtu.be/38_6C0dkKmU?t=1996)).
- **Designed to be called.** "The best use cases for Haiku 55 aren't clicking
  it in the UI or selecting it in Cloud Code ... It's letting your agents use
  it and letting your applications use it" ([H55 22:00-22:17](https://youtu.be/38_6C0dkKmU?t=1320)). Anthropic names
  summaries, compactions, database queries, classification, subagent work for
  Opus and Sonnet, live support and browser use ([H55 4:05-4:29](https://youtu.be/38_6C0dkKmU?t=245)).
- **Large jump over Haiku 4.5 on vendor benchmarks.** Terminal-Bench 4.0 39.2%
  (Haiku 4.5 0.0%, GPT-6 Luna 16.4%); OSWorld 2.1 72.4% partial credit at max
  vs 15.7% for Haiku 4.5 and 48.9% for Luna (Anthropic numbers, not
  independently verified; [H55 9:03-10:09](https://youtu.be/38_6C0dkKmU?t=543)).
- **On the cheap end of the cost/intelligence chart.** On Theo's Slopalytics
  chart (Artificial Analysis data) it is "neck and neck" with GPT-6 Luna; with
  Luna it forms the cheap end of the Pareto line ([H55 15:53-16:19](https://youtu.be/38_6C0dkKmU?t=953); [H55 39:49-40:12](https://youtu.be/38_6C0dkKmU?t=2389)).
  Within Anthropic's lineup, "all of Haiku for the cheap and most of Opus for
  the less cheap" ([H55 37:22](https://youtu.be/38_6C0dkKmU?t=2242)).
- **Some taste for its size.** A community video demo cost about $0.60 and was
  "insanely impressive for the money" ([H55 24:52-25:08](https://youtu.be/38_6C0dkKmU?t=1492)). Front end with the Claude
  design skill was "usable" for a model this cheap and far better than Grok 4.7
  ([H55 25:25-27:25](https://youtu.be/38_6C0dkKmU?t=1525)).

## Weaknesses and failure modes

Each item is a guardrail the orchestrator must apply.

- **Corners itself and stops without saying so.** On a PR audit it fired
  parallel fetches that used most of GitHub's 5,000 requests per hour, saved
  the error bodies as if they were API data, and failed on jq. It then said it
  would wait for the quota reset and refetch, but never scheduled anything to
  wake itself up; "this thread is just done until I tell it to keep going".
  Theo's GitHub integration in T3 Code was locked out for about 50 minutes.
  "Small models will corner themselves like this, make something harder for
  not just themselves, but for me" ([H55 33:46-34:56](https://youtu.be/38_6C0dkKmU?t=2026)). Guardrail: give
  it a valid "rate-limited / cannot / nothing found" return, forbid
  self-waiting, share one rate-limit budget across parallel workers, and have
  the orchestrator own retries.
- **Trusts CI status instead of auditing.** It marked PRs "merge ready" because
  GitHub's checks were clean: "it thinks that they're ready just cuz GitHub
  said so. It didn't seem to audit them thoroughly itself" ([H55 30:47-30:55](https://youtu.be/38_6C0dkKmU?t=1847)). Guardrail: never treat its output as a review; green CI is not
  an audit; a stronger model or a human decides what is mergeable.
- **Bad with reasoning off.** ThePrimeagen swapped GPT-6 Luna for Haiku 5.5 with
  reasoning off in automations and got a worse pass rate, a much higher fail
  rate, and slower runs. Theo: "Anthropic has trained their models to be bad
  at that ... you always have to let it reason at least a little bit"
  ([H55 10:23-11:08](https://youtu.be/38_6C0dkKmU?t=623)). Guardrail: reasoning on. For
  reasoning-off categorisation, use OpenAI's cheap model (transcribed "Jev",
  exact name unclear) or Luna, unless vision is needed ([H55 11:08-11:25](https://youtu.be/38_6C0dkKmU?t=668)).
- **The 5x price tier above 100K.** Every request over 100K prompt tokens pays
  5x on every line, cache hits included. Its Fish Slop build cost about $1:
  9.73M cache-read tokens, only 102 uncached input tokens, about $0.30 of
  output, and 47 of 51 requests over 100K ([H55 30:11-30:35](https://youtu.be/38_6C0dkKmU?t=1811)).
  Guardrail: cap context near 100K and size batches to fit.
- **Cost inversion on work it cannot do.** "If Opus can solve a problem in 100K
  tokens and Haiku burns a million before it figures out it can't, Haiku ends
  up more expensive" ([H55 36:23-36:48](https://youtu.be/38_6C0dkKmU?t=2183)). Guardrail: a token or time
  budget per job; kill and escalate to Opus when it runs long without a
  checkable result.
- **Not a coder for work that lands.** "Would I use this model for code? No"
  ([H55 31:29-31:37](https://youtu.be/38_6C0dkKmU?t=1889)). Terminal-Bench 4.0 39.2% vs 70.6% for Sonnet 5.5; Anthropic
  itself says Sonnet and Opus remain better for complex agentic coding.
- **Mediocre highs on wide builds.** Fish Slop had no mouse look, no sound, bad
  corner geometry and wrong enemy timing. "Its lows aren't as low as Astra's,
  but its highs are a tenth as high" ([H55 28:23-30:04](https://youtu.be/38_6C0dkKmU?t=1703)).
- **Front end without the design skill** falls back to "classic LLM design"
  ([H55 26:11-26:24](https://youtu.be/38_6C0dkKmU?t=1571)).
- **Lead-model mistakes.** On the PR audit it was the lead and stalled. Told to
  use Haiku for everything, an Opus lead proposed about 100 Haiku agents for
  1,495 PRs ([H55 35:42-35:58](https://youtu.be/38_6C0dkKmU?t=2142)); the orchestrator, not the lead, should cap agent
  count.
- **Computer use is unproven.** Vendor OSWorld 2.1 strict pass rate is 37.1%,
  below Sonnet 5.5 (48.8%) and Opus 5.5 (53.2%); the 72.4% headline is partial
  credit at max effort. Theo: "I haven't tried it yet. I've heard good things"
  ([H55 10:09](https://youtu.be/38_6C0dkKmU?t=609)).
- **Token efficiency.** Theo: GPT-6.1 Sol on low "is as cheap as haiku on low,
  largely due to the token efficiency difference" ([H55 12:58](https://youtu.be/38_6C0dkKmU?t=778)). Transcription is
  unclear here; treat as a hint, not a number.

## How to prompt it

Haiku 5.5 is prompted by a lead model, so the lead's subagent prompt must carry
the guardrails. Follow the kit's what / done / out shape and add these:

- **Reasoning on.** Use effort (medium default; try xhigh for harder jobs).
  Never pass `thinking: {type: "disabled"}`; the API accepts it at high or
  below, but the model is worse with it. `budget_tokens` returns a 400 on this
  model.
- **One bounded job, under 100K tokens of prompt.** Name the inputs, the exact
  output shape (JSON, a list, a label set) and the stopping point. Split large
  sets into batches that fit (Opus chose about 15 PRs per Haiku agent,
  [H55 35:42-35:58](https://youtu.be/38_6C0dkKmU?t=2142)).
- **"Cannot" is a valid answer.** Tell it to return early on rate limits,
  missing data or errors it cannot fix, and not to wait or loop.
- **Check what it fetched.** Ask it to validate response shape before saving
  (the failed audit stored error bodies as data), and have the lead re-check
  the output with a script.
- **No merge verdicts.** Ask for facts (what changed, what CI says, what looks
  risky), not "merge ready".
- **Reads, not plans.** Hand it a hypothesis to check or a set to categorise;
  keep the plan and the conclusion with the lead.

Kit-written guardrail block for a Haiku subagent prompt (not tested on camera):

> Return one JSON object per input with the fields listed above. If you hit a
> rate limit, an auth error, or anything you cannot fix, stop and return
> {"status": "rate_limited" | "cannot" | "nothing_found", "detail": "..."}
> instead. Do not wait for a reset, do not retry in a loop, and do not say you
> will continue later. Before saving any API response, check that it is the
> shape you expected; never save an error body as data. Do not judge whether
> anything is ready to merge; green CI is not a review.

Lead prompt that worked better than running Haiku as the lead (Theo, [H55 35:13-35:27](https://youtu.be/38_6C0dkKmU?t=2113),
on Opus):

> Use lots of subagents and workflows to review these PRs and use Haiku 5.5 for
> all subagents throughout the work. Minimize work that you do yourself outside
> of actually getting the data and orchestrating the subagents.

Add an agent-count cap and a shared rate-limit budget to that prompt
(`core/strategies/parallelism.md`).

In Claude Code, set Haiku 5.5's autocompact window to 100K so sessions stay in
the cheaper tier. An Anthropic employee recommended this, and Theo reports it
is "saved per model", so it would apply to Haiku subagents only ([H55 8:31-8:55](https://youtu.be/38_6C0dkKmU?t=511)). Per-model persistence is unverified.

Differences from prompting Opus 5.5: do not drop reasoning to save money, keep
each job small and closed, and never let it own the done state.

## Routing guidance

Route here for:
- File and code search a lead needs when a plain ripgrep will not do
  ([H55 23:27-23:34](https://youtu.be/38_6C0dkKmU?t=1407)).
- Data gathering: fetching and summarising many items (PRs, issues, logs),
  with a shared rate-limit budget.
- Categorisation and summarisation, in agents or inside applications, with
  reasoning on.
- Reading documentation or comparing other projects to answer a lead's
  question.
- Vetting a lead's hypotheses in parallel during an investigation.
- Many attempts where each one is checked by running code.
- Cheap browser or desktop flows, on trial only, with a verification step.

Do not route here for:
- Anything that must land without a stronger model's review: features,
  quick fixes, babysitting, front end, copy.
- Code review or deciding what is merge-ready.
- Primary or interactive use; long agentic loops; leading other agents.
- Reasoning-off calls (use an OpenAI cheap model or Luna).
- Jobs where a wrong attempt is expensive to detect.

Handoff patterns:
- **Opus leads, Haiku gathers.** Opus plans and writes code; Haiku collects
  context, reads docs and categorises. "When Opus needs to go collect a bunch
  of data or read through tons of [stuff] or just categorize things, Haiku is
  going to be an incredible addition" ([H55 39:08-39:23](https://youtu.be/38_6C0dkKmU?t=2348)).
- **Opus and Sol stay the core pair.** Theo keeps Opus coding and 6.1 Sol as
  auditor; Sol is "a different family with similar intelligence", not a tier
  between Haiku and Opus ([H55 37:53-38:59](https://youtu.be/38_6C0dkKmU?t=2273)).
- **Haiku triages, Opus lands.** Haiku produced the performance-PR shortlist;
  Theo pasted a PR into Opus and told it to verify, fix and merge if confident
  ([H55 30:42-31:20](https://youtu.be/38_6C0dkKmU?t=1842)).
- **Within Anthropic, Opus plus Haiku.** "You can avoid Sonnet entirely and
  just use Opus and Hiku" on the AA Pareto line ([H55 37:37-37:53](https://youtu.be/38_6C0dkKmU?t=2257)). Sonnet 5.5 is
  still the kit's bounded-analysis subagent; this profile does not change that.
- **Cross-vendor.** On the AA chart, Luna is "cheaper always" and "dumber
  always" than Haiku, and 6.1 Sol costs about the same per AA task as Haiku
  with "a huge jump in intelligence" ([H55 16:44-17:09](https://youtu.be/38_6C0dkKmU?t=1004)). In a mixed kit, Luna or Sol
  may be better per dollar. Haiku's case is staying inside Anthropic: one
  provider, a Claude subscription without Codex, or Opus prompting a same-family
  worker ([H55 17:42-18:12](https://youtu.be/38_6C0dkKmU?t=1062)).

## Cost notes

- Under 100K prompt tokens: $0.10 in, $0.50 out, $0.01 cache read, $0.125 (5m)
  or $0.20 (1h) cache write, batch $0.05 / $0.25. Over 100K: 5x on every line
  ($0.50 / $2.50 / $0.05 / $0.625 / $1.00; batch $0.25 / $1.25). Each request
  is priced on its own and cache reads count toward the threshold (Anthropic
  pricing page).
- Claude Code writes 1-hour cache entries ([H55 30:20](https://youtu.be/38_6C0dkKmU?t=1820)), so in Claude Code the cache
  write price is $0.20 (or $1.00 above 100K).
- The newer tokenizer counts about 30% more tokens than Haiku 4.5, so the 100K
  line arrives sooner than a Haiku 4.5 token count suggests.
- Fish Slop: about $1 total, 47 of 51 requests in the higher tier. "If I had
  capped the context, the game probably would have come out much worse, but it
  would have been way cheaper" ([H55 30:35-30:42](https://youtu.be/38_6C0dkKmU?t=1835)).
- AA cost per task (Theo's chart, approximate): Haiku at about $0.213 vs 6.1
  Sol at about $0.214 ([H55 16:52](https://youtu.be/38_6C0dkKmU?t=1012)), probably Haiku at max since only xhigh and max
  had been measured then. Opus 5.5 low vs Haiku 5.5 max: "20 cents to 55 ...
  around 2x more money for Opus" ([H55 36:56-37:07](https://youtu.be/38_6C0dkKmU?t=2216)); read as Haiku max about $0.20
  and Opus low about $0.55, but the word order is ambiguous.
- Effort for value: medium by default. Theo's chart puts xhigh and max as the
  best value in Anthropic's range ([H55 14:01-14:13](https://youtu.be/38_6C0dkKmU?t=841)). The kit's never-max rule stands
  until a local test shows max is worth it; xhigh is the setting to trial.
- Cost inversion: a Haiku job that fails slowly can cost more than Opus
  succeeding. Set a budget per job and escalate.
- Subscription credit (reported, unverified): Theo says the launch notes give
  20x Max users $200 and 5x Max users $100 of API credit a month ([H55 20:12-20:36](https://youtu.be/38_6C0dkKmU?t=1212)).
  A secondary source (the-decoder) describes it as a credit for programmatic
  use (Agent SDK, `claude -p`, GitHub Actions, third-party apps), billed at API
  rates, dating from 2026-06-15. If true, `claude -p` bridge calls may draw from
  that credit rather than plan quota. Check the account before relying on it.

## Evidence

- H55: "finally a good small model", Theo (t3.gg), YouTube, https://youtu.be/38_6C0dkKmU
  (launch day, about 2026-10-07/08). Timestamps in this profile are from that
  video. Caption mishearings read as follows ("cash" = cache, "Soul" = Sol, "Raichu" / "Hiku" / "ha coup" =
  Haiku, "Slopalytics" = Theo's dashboard on Artificial Analysis data).
- [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing),
  fetched 2026-10-08: both price tiers, the 100K rule, batch prices, the Sonnet
  5.5 cache-read cut to $0.10.
- Model facts (id, 1M context, 128K output, effort levels and medium default,
  adaptive thinking, disabled thinking only at high or below, `budget_tokens`
  400, no server-side refusal fallback, tokenizer +30%, compaction, task
  budgets, computer use via `computer_toolset_20260801`): Claude API reference
  cache dated 2026-10-06, as relayed in the orchestrator's evidence packet.
- Vendor benchmarks (Terminal-Bench 4.0, OSWorld 2.1, egg-drop demo, "75% less
  money"): Anthropic, not independently verified.
- Artificial Analysis Intelligence Index for Haiku 5.5: not found as of
  2026-10-08 (one web search; AA pages found only for Haiku 4.5). Theo's chart
  gives relative positions only.
- **Unverified:** the per-model autocompact setting; Pro plan access; cursor,
  opencode and t3-code availability; the subscription API credit and whether
  `claude -p` draws from it; the AA per-task costs above (read off a chart in a
  video); Theo's "Sol on low is as cheap as Haiku on low" (garbled); the
  computer-use fit (no hands-on run).

### Score rationale

| Axis | Score | Why |
|---|---|---|
| intelligence | 5 | "Slightly smarter" than Luna (4) on AA; Terminal-Bench 4.0 39.2% vs Sonnet 5.5 70.6%; far below Opus 5.5 (8). No AA index number found. |
| taste | 4 | Usable front end with the design skill and a strong cheap video demo, but "classic LLM design" without the skill and a weak Fish Slop. Level with Sonnet. |
| floor | 3 | Cornered itself on a rate limit, stored errors as data, promised to wait and stalled; trusted green CI. Fewer wild lows than Astra on Fish Slop, but not trusted on anything wide. |
| thoroughness | 3 | "Didn't seem to audit them thoroughly itself" on the PR audit; good for reads a lead checks, not for finding what others missed. |
| cost_efficiency | 7 | About 10x under Haiku 4.5 per token and neck and neck with Luna on AA, but Luna is cheaper, Sol costs about the same per AA task and is much smarter, and the 5x tier and cost inversion bite in long sessions. |
| speed | 8 | 100-200 tok/s by provider, about 180 in Claude Code; parallel fan-out finished the egg-drop task in under a minute. Slower than Luna with reasoning off (Prime). Gemini 3.8 Flash is faster. |
| computer_use | 3 | Vendor OSWorld 2.1 strict 37.1%, below Sonnet (48.8%) and Opus (53.2%), which score 4; 72.4% is partial credit at max. No hands-on evidence. |
| orchestration | 2 | Stalled as the lead on the PR audit; Opus leading Haiku workers was Theo's fix. Built to be called, not to lead. |
