---
id: claude-sonnet-5-5
name: Claude Sonnet 5.5
vendor: anthropic
family: claude
status: current
released: null
as_of: 2026-10-19
confidence: medium

api_ids: [claude-sonnet-5-5]
access:
  subscriptions: [claude-pro, claude-max]
  api: true
  harnesses: [claude-code, cursor, opencode, t3-code, openclaw, hermes]
  invoke_via: [claude-cli, cursor-cli, openclaw-cli, hermes-cli]   # openclaw, hermes / openclaw-cli, hermes-cli added 2026-10-19: API key in both; Claude subscription OAuth is restricted or disallowed there, see the bridges

pricing_per_mtok:
  input: 2
  output: 10
  cache_read: 0.10
  cache_write: 2.50
context_window: 1000000
notes_on_cost: >
  Half Opus's price on every line item since cache reads were cut to $0.10/M in
  October 2026 (they were $0.20/M, the same as Opus). In agentic loops cache reads
  dominate, and it is the most token-hungry model measured (272K tokens per Cursor
  Bench task; about 360K tokens read per request vs 110K for 6.1 Sol). It is cheaper
  than Opus only while it reads less than about twice Opus's tokens, so like-for-like
  coding work lands at roughly Opus's cost with a slower wall clock (inference; no
  like-for-like run since the cut). It is clearly cheap on short, bounded
  investigations (about 5 minutes).

effort:
  levels: [low, medium, high, xhigh, max]
  default: high
  avoid: [low, max]
  notes: >
    high or xhigh; xhigh beat max on Frontier Code. medium is 'fine-ish' but noticeably
    weaker than Opus-medium. low drops sharply; max is the most expensive setting.

scores:
  intelligence: 7
  taste: 4
  floor: 6
  thoroughness: 6
  cost_efficiency: 6
  speed: 6
  computer_use: 4
  orchestration: 3

tasks:
  quick-fix:      {fit: ok, note: "Anthropic positions it for 'well scoped everyday tasks', but the speaker would 'just use Opus': even after the cache-read cut, like-for-like cost is about Opus's for a weaker result."}
  feature:        {fit: poor, note: "Do not route main implementation here when Opus is available; about the same cost after the cache-read cut, less capable, slower wall clock."}
  long-run:       {fit: poor, note: "Long tool-heavy loops are where token hunger eats its discount: the cache-read cut makes it half Opus's price per token, but it read 1.25x to 3.5x Opus's tokens; 43 vs 36 min wall clock vs Opus on Fish Slop."}
  frontend:       {fit: poor, note: "'Hideous', 'boring', 'awful' animations, scroll bugs; weakest of the Claude trio. Use Fable, then Opus."}
  review:         {fit: ok, note: "Not tested as a PR reviewer; 6.1 Sol was far more thorough on audits. Same-family as Claude authors, so use OpenAI for review."}
  investigate:    {fit: good, note: "Bounded investigations with a clear deliverable: finding specific behaviours, confirming a hunch about an API or code path."}
  analyze:        {fit: best, note: "Beat Opus at about half the price in about 5 minutes on the speaker's decomposition bench ('best value I've seen'). Astra made the best plan; 6.1 Sol may now be cheaper."}
  bulk:           {fit: ok, note: "Claimed good at documents, slides and spreadsheets (lightly evidenced); token hunger hurts high-volume work. Haiku 5.5 (shipped October 2026) now takes bounded, verifiable high-volume work as a subagent; see claude-haiku-5-5.md."}
  research:       {fit: good, note: "Scoping research and hunch-checking for an orchestrator; external web research specifically is not covered in research."}
  computer-use:   {fit: poor, note: "Much improved (OS World 'neck and neck' with Opus 5.5; beat Pokemon Red from screenshots), but the speaker still uses Astra almost exclusively."}
  copy:           {fit: ok, note: "Writes 'way more clearly' than the previous generation with Claude-isms removed; no copy-specific test in research."}
  3d-games:       {fit: good, note: "Fish Slop 3D was 'one of the best I've ever seen' (Blender models, 120 FPS), but took about 40 min and about $16 at API prices (before the cache-read cut)."}
  prompt-writing: {fit: unknown, note: "Not covered in research."}
  babysit:        {fit: poor, note: "Not tested directly; babysitting is a long poll-and-fix loop, where its token hunger costs most even at the new $0.10/M cache-read price (inference from the cost evidence)."}
  orchestrate:    {fit: poor, note: "Positioned as a tool other models call, not a lead; no evidence of it orchestrating."}

role_hints:
  as_primary: "Not recommended as a primary or human-selected model; 'useful as long as you're not the one sending it prompts.'"
  as_subagent: "Bounded analysis subagent dispatched by an Opus or Fable lead: codebase deep dives, decomposition research, behaviour-finding, hunch confirmation."
  never_for: ["primary or interactive model", "low effort", "max effort", "front-end or UI design", "long agentic loops or multi-hour runs", "main implementation when Opus is available"]
---

## Summary

A subagent for bounded investigation and analysis, dispatched by an Opus or
Fable lead: deep dives into a codebase, decomposition research, confirming
hunches. On those it gave the best cost per point the speaker had seen. Do not
select it as a primary model, for implementation, for front end, or for any long
agentic loop. Cache reads now cost half what Opus pays, but it burns more tokens
and more wall clock, so there it costs about the same as Opus for weaker work.

## Strengths

- **Bounded codebase analysis.** On the speaker's "big deep audit" bench
  (propose how to land T3 Code's huge orchestrator-v2 PR in pieces, scored by an
  automated judging panel), Sonnet scored slightly above Opus at about half the
  price, in about 5 minutes; Opus took "almost twice as long". "The cost per
  point here is insane. It is like the best value I've seen in this bench by
  far" ([SON55 23:46](https://youtu.be/8WbW_n95wc4?t=1426)). Astra still produced "by far the best plan".
- **Designed to be called by other models.** "If you give Opus or Fable a big
  task and they want to analyze the codebase before starting, they can now call
  on Sonnet to do that and get results that they're more than happy with. This
  is huge" ([SON55 24:16](https://youtu.be/8WbW_n95wc4?t=1456)).
- **Reads thread context faithfully.** Given an ambiguous prompt in the wrong
  thread, it answered within that thread's frame instead of guessing: "I was
  about to crash out about it not understanding my intent but it totally does"
  ([SON55 26:05](https://youtu.be/8WbW_n95wc4?t=1565)).
- **Fewer dumb spikes than Astra.** The speaker "would take Sonnet over Astra for
  my day-to-day code work" but "would just use Opus" (same section). It feels
  like "slightly dumber, way faster versions of Fable".
- **3D game build.** Fish Slop 3D was "one of the best I've ever seen ... in some
  ways it is better than the Opus one", with Blender-made models at 120 FPS.
- **Benchmarks.** Terminal Bench 4: 70.6% (up from 10.3% for Sonnet 5; the
  speaker is sceptical of the bench). Frontier Code: xhigh above Sol, max below.
  OS World "neck and neck with Opus 5.5". At xhigh it is "roughly Astra level" on
  AA intelligence.
- **Raw throughput.** About 94 TPS via OpenRouter (Opus about 70, Astra about
  30); about 150 TPS on the speaker's subscription vs about 100 for Opus.
- **Clearer writing** than the previous generation, with Claude-isms removed.

## Weaknesses and failure modes

- **Not meaningfully cheaper than Opus in loops.** Until October 2026 its
  cache reads cost $0.20/M, the same as Opus, and made up "like 50 plus" percent
  of Sonnet's agentic cost (about 20% for Opus, under 5% for Fable). On that
  pricing, "Sonnet consistently comes out as if not more expensive than opus
  does" on like-for-like code tasks ([SON55 10:50](https://youtu.be/8WbW_n95wc4?t=650)). Anthropic has since cut Sonnet's
  cache reads to $0.10/M, so it is now half Opus's price on every line item.
  Token hunger (next bullet) still eats much of that: like-for-like it should
  land at about Opus's cost rather than above it (inference; no like-for-like
  run since the cut). On AA it cost roughly the same as Fable 5.1, mostly
  because of max; AA has since repriced it and it "shifted quite a bit to the
  left" on Theo's chart ([H55 19:14-19:30](https://youtu.be/38_6C0dkKmU?t=1154)).
- **Token-hungry.** Cursor Bench: 271,920 tokens per task, the most ever
  recorded (Opus 218K), "more than 5x" Sol and Astra. In Fish Slop it used more
  than 3.5x Opus's input tokens. About 360K tokens read per request vs about 110K
  for 6.1 Sol ([SOL61 19:16](https://youtu.be/vu8X3YroB-w?t=1156)).
- **Slower wall clock despite faster tokens.** Fish Slop: 43 min vs 36 min for
  Opus (39 vs 27 min generating). "It's faster, but actually slower because of
  the token differences."
- **Weak front end.** "A bit opinionated", "rough", "hideous", "boring", "awful"
  animations, scroll bugs; worse than Opus and "significantly worse" than Fable.
  Anthropic's "sharp eye for design" claim is disputed. 6.1 Sol's UI was worse
  still ([SOL61 22:28](https://youtu.be/vu8X3YroB-w?t=1348)).
- **Medium is weak.** "Medium is a lot stronger with Opus than it is with
  Sonnet"; Frontier Code shows "pretty big drops" at medium and low.
- **Max and low.** Max is the most expensive setting and xhigh beat it on
  Frontier Code; max "can often actually hurt performance because ... it's going
  to start second guessing itself." "I don't think you should use any anthropic
  model on low right now."
- **Dumber than Opus at every AA level.** "More expensive and dumber than Opus
  5.5 at every single level" on the AA Intelligence Index.
- **Less thorough than OpenAI auditors.** On the speaker's audits, "neither
  [Sonnet nor Opus] were anywhere near as thorough" as 6.1 Sol
  ([SOL61 13:48](https://youtu.be/vu8X3YroB-w?t=828)).
- **Topic changes.** Because it reads the thread's frame faithfully, a new topic
  in a long-running thread must be flagged explicitly.
- **May be displaced.** After 6.1 Sol shipped: "I have almost no reason to use
  Sonnet anymore because this will effectively take its place"
  ([SOL61 29:35](https://youtu.be/vu8X3YroB-w?t=1775)).

## How to prompt it

The research contains no Sonnet-specific prompt guide. The speaker's rule is
that humans should not prompt it at all: "We shouldn't be calling Sonnet
directly. It should be used as one of many things that Opus or Fable will
orchestrate." Dispatch prompts are therefore written by the orchestrator.

What the dispatch prompt should contain (from the speaker's examples):
- One well-scoped, investigatory question with a clear deliverable: "deep dives
  into your codebase to find specific behaviors or characteristics", "confirming
  a hunch it has about some thing that you found in an API", analysis that helps
  the orchestrator "plan and scope work".
- What done means and when to stop, using the three-part structure from
  Anthropic's Opus 5.5 guide (what you want, what "done" means, the out). The
  guide's verbatim example, as a pattern (tested on Opus, not Sonnet):

  > Migrate the payments endpoint from the old client to the new one. Done means
  > every endpoint uses the new client, the old one is deleted, and the test
  > suite passes. Stop and ask me only if a test fails for a reason that you
  > can't explain.

- An explicit statement that the task is read-only analysis, so it stays short
  and bounded. Its cost advantage shrinks to about nothing in long loops.
- When reusing a long-running Sonnet thread, say explicitly that the topic has
  changed.

Instructions carried over from the other Claude 5.x guides (verbatim, but
validated on Fable or Opus, not on Sonnet):
- Anthropic's Fable 5.1 anti-scope-creep instruction, which the research
  recommends for narrow subagent tasks:

  > If while working or testing you find pre-existing bugs, performance
  > concerns, or behaviors the task doesn't mention, don't fix, optimize, or
  > extend it in this change unless the requested behavior cannot work without
  > it. Report it as a follow-up in your summary.

- Ask it to mark claims it could not confirm, with the reason (Theo's review
  guidance in [OPUSG 24:45](https://youtu.be/ejjBbaq9RmY?t=1485)).
- Leave out "think hard" and "show your reasoning" (general Claude 5.x guidance
  from the same video).

Effort: send high, or xhigh for harder analysis. Never low or max; do not assume
medium behaves like Opus-medium.

## Routing guidance

Route here for (as a subagent only):
- Codebase exploration and deep-dive analysis before a lead starts work.
- Decomposition research ("how could this giant change be split?").
- Locating specific behaviours; verifying hunches about APIs or code.
- Scoping and planning research for the orchestrator.
- Documents, slides, spreadsheets and screenshot understanding (Anthropic's
  claims, lightly evidenced).

Do not route here for:
- Primary or interactive use; humans should not pick it in Claude Code.
- Main implementation or day-to-day coding when Opus is available.
- Front-end or UI design.
- Long agentic loops, babysitting, multi-hour runs.
- Exhaustive review or "best possible plan" (Astra, 6.1 Sol).
- Computer use (OpenAI).

Handoff patterns:
- **Opus or Fable dispatches Sonnet for analysis.** The lead sends a bounded
  question, Sonnet returns findings, and the lead plans and implements. "If you
  set Opus up properly to use Sonnet at the right times for these sub agents ...
  the result will be Opus feeling way faster and getting real work done for
  slightly cheaper."
- **6.1 Sol as the alternative analysis subagent.** If the user has a Codex
  subscription, the speaker now prefers 6.1 Sol for review and investigation: it
  did three rounds of work for about half the cost of one Sonnet round. Keep
  Sonnet as the analysis subagent for Claude-only users.
- **Haiku 5.5 (shipped October 2026)** costs $0.10 / $0.50 per M in/out for
  prompts up to 100K tokens and 5x that above. It is a subagent for bounded,
  verifiable work: file search, data gathering, categorisation, reading docs,
  many cheap attempts. It takes the high-volume part of Sonnet's bulk slot, not
  its analysis role. See `core/models/claude-haiku-5-5.md`.
- **Opus plus Haiku may leave no room for Sonnet (Theo's opinion).** In the
  Haiku 5.5 video, after AA repriced Sonnet for the cache-read cut, Theo reads
  the Anthropic Pareto line on his chart of Artificial Analysis aggregate data
  as "all of Haiku for the cheap and most of Opus for the less cheap". Sonnet
  "offers nothing now. Maybe just barely on high", and "you can avoid Sonnet
  entirely and just use Opus and Haiku"
  ([H55 37:22-37:45](https://youtu.be/38_6C0dkKmU?t=2242)). This is
  his reading of aggregate benchmark data, not a task test. The kit keeps
  Sonnet as the analysis subagent above: Haiku does not replace judgment work,
  and analysis that needs judgment stays with Sonnet or Opus.

## Cost notes

- $2 / $10 per M in/out, cache writes $2.50/M, cache reads $0.10/M since
  October 2026 (Anthropic pricing page, fetched 2026-10-08). Before the cut
  cache reads were $0.20/M, the same as Opus, so the discount skipped the line
  item that dominates agentic bills. Now every line item is half Opus's.
- In a cache-read-dominated loop Sonnet is cheaper than Opus only while it
  reads less than twice Opus's tokens. It used 1.25x Opus's tokens on Cursor
  Bench and 3.5x Opus's input tokens on one Fish Slop build, which puts it
  between about 0.6x and 1.75x Opus's cost (arithmetic in
  `core/strategies/cost-model.md` §5).
- Clearly cost-effective for short, bounded investigations that finish quickly
  (about 5 minutes on the audit bench). Long loops eat most of the saving.
- AA cost per run (before the cache-read cut): max $7.60 (vs Astra max $3.26); xhigh "pretty close to
  Astra's price"; high and medium transcribed as "$18 and 59", probably $1.18
  and $0.59 (ambiguous).
- Conflicting cost data. The Sonnet video has Sonnet at about half Opus's cost
  on the orchestrator-v2 audit. The 6.1 Sol video has Sonnet at "almost $9" vs
  Opus at $5 on the "find opportunities to improve T3 Code" task, and $15 vs
  Opus $50 on a Fish Slop run (the Opus run was contaminated by a Fable
  subagent). These are different tasks; the research does not reconcile them.
  All of these runs predate the cache-read cut.
- Subscription: about $2,300/week of API-equivalent usage on the $200 plan.
  Other Claude plans are not covered in research.
- Effort for value: high. xhigh for harder analysis; it beat max on Frontier
  Code.

## Evidence

- SON55: "OpenAI should be scared of this one", Theo (t3.gg), YouTube, https://youtu.be/8WbW_n95wc4
- OPUS55: "My new favorite model.", Theo (t3.gg), YouTube, https://youtu.be/jgGyX7MPPVg (Sonnet 5.5 announced as "coming weeks").
- SOL61: "OpenAI fights back", Theo (t3.gg), YouTube, https://youtu.be/vu8X3YroB-w (token
  comparison, audit costs, "almost no reason to use Sonnet anymore").
- FVA: "Fable Vs Astra Debate Is Over", Theo (t3.gg), YouTube, https://youtu.be/P7bxbDSnZRM says "Sonnet's hilariously bad", but this is unversioned and
  predates Sonnet 5.5; not used for scores.
- OPUSG: "Getting the most out of Opus 5.5", Theo (t3.gg), YouTube, https://youtu.be/ejjBbaq9RmY
- FABG: "So I was using Fable wrong...", Theo (t3.gg), YouTube, https://youtu.be/-XWSJM-Ue-o
  Neither covers Sonnet; prompting snippets
  above are carried over from these Opus and Fable videos and marked as such.
- API id and 1M context come from the bundled Claude API reference (model table
  cached 2026-09-25), not from `research/`. Data retention / ZDR for Sonnet is
  not covered in research.
- Cache-read price of $0.10/M: Anthropic pricing page, fetched 2026-10-08
  ("Cache hits and refreshes on Claude Opus 5.5 and Claude Sonnet 5.5 are
  priced at 0.05x the base input price"). Opus 5.5 stays at $0.20/M.
- H55: "finally a good small model", Theo (t3.gg), YouTube, https://youtu.be/38_6C0dkKmU (Theo's Haiku 5.5 launch
  video, about 2026-10-07): cache-read cut at [H55 4:36](https://youtu.be/38_6C0dkKmU?t=276), AA repricing at
  [H55 19:07-19:30](https://youtu.be/38_6C0dkKmU?t=1147), Pareto-line view at [H55 37:22-37:45](https://youtu.be/38_6C0dkKmU?t=2242).
- Release month: not stated (`released: null`).
- Confidence is medium: one dedicated video plus comparisons in the Sol video,
  with conflicting cost data; no Anthropic prompt guide for Sonnet in research.

### Score rationale

| Axis | Score | Why |
|---|---|---|
| intelligence | 7 | "Dumber than Opus 5.5 at every single level" on AA; about Astra level at xhigh; "slightly dumber ... versions of Fable". |
| taste | 4 | Weakest front end of the trio ("hideous", "awful" animations); clearer prose than Sonnet 5 and a good 3D game, but no code-style or copy evidence lifts it. |
| floor | 6 | "Fewer dumb spikes" than Astra and good intent tracking, but only evidenced on bounded tasks; no long-run evidence. Scored conservatively. |
| thoroughness | 6 | Slightly above Opus on the decomposition bench (Opus is 5), but far less thorough than 6.1 Sol and Astra on audits. |
| cost_efficiency | 6 | Raised from 5 on 2026-10-08. The 5 rested on cache reads costing the same as Opus; the cut to $0.10/M halves the line item that dominates its agentic bill, AA repriced it "quite a bit to the left", and bounded analysis (already its best cost per point) got cheaper. Not above Opus (6): record token use and slower wall clock put like-for-like loops at about parity, and on the AA Pareto line it "offers nothing now. Maybe just barely on high" (Theo). |
| speed | 6 | Highest raw TPS of the trio and about 2x faster than Opus on the 5-minute audit, but slower wall clock than Opus on the 40-minute build. |
| computer_use | 4 | Much improved and level with Opus on OS World; Astra still preferred. Same score as Fable and Opus. |
| orchestration | 3 | No evidence of it leading; the speaker positions it strictly as a tool other models call. |
