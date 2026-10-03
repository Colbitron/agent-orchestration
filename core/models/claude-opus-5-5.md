---
id: claude-opus-5-5
name: Claude Opus 5.5
vendor: anthropic
family: claude
status: current
released: null
as_of: 2026-10-02
confidence: high

api_ids: [claude-opus-5-5]
access:
  subscriptions: [claude-pro, claude-max]
  api: true
  harnesses: [claude-code, cursor, opencode, t3-code]
  invoke_via: [claude-cli, cursor-cli]

pricing_per_mtok:
  input: 4
  output: 20
  cache_read: 0.20
  cache_write: 5
context_window: 1000000
notes_on_cost: >
  Cheaper per token than Opus 5 (20% list cut, cache reads $0.20/M) but less
  token-efficient: about 120K tokens per AA task at max vs 27K for Astra. Cache reads
  are about 20% of its agentic bill. Best value is on a Claude subscription, where it
  draws on the non-Fable half of the quota; a full day of heavy use cost about 20% of
  one account's weekly limit. Effort can change mid-session without busting the
  cache. Watch for unrequested Fable subagents, which inflate cost.

effort:
  levels: [low, medium, high, xhigh, max]
  default: high
  avoid: [low, max]
  notes: >
    high for normal work; medium is the cost sweet spot (often matches Fable 5.1 max on
    coding benches); xhigh for refinement passes. low is poor value; max loops (a 6.5-hour
    runaway) for ~1% gain. The API and Claude Code default is medium, so set it explicitly.

scores:
  intelligence: 8
  taste: 7
  floor: 7
  thoroughness: 5
  cost_efficiency: 6
  speed: 7
  computer_use: 4
  orchestration: 7

tasks:
  quick-fix:      {fit: best, note: "Default daily driver; narrow, specified tickets clear the bar at medium/high for a fraction of Fable's cost and quota."}
  feature:        {fit: best, note: "PR quality close to Fable 5.1 (similar high-severity rate, slightly more nitpicks); escalate to Fable for wide cross-package work or if output misses the bar."}
  long-run:       {fit: good, note: "Rewrote a stalled TS-to-Rust port in a day; testers ran a 680K-LOC migration. Needs named stops and 'do all phases' or it stops between phases; failure odds rise with run length."}
  frontend:       {fit: ok, note: "Falls back on default styles without direction; good only with an explicit list of styles to avoid. Prefer Fable for open-ended design."}
  review:         {fit: ok, note: "About twice as good as Opus 5 with no contradicted findings, but finds less than Fable, Astra, 6.1 Sol and Grok 4.7. Never the only reviewer of Claude-written code."}
  investigate:    {fit: ok, note: "Discernment weakens when the system is already in a bad state; 6.1 Sol found regressions Opus missed. Delegate root-causing to Sol or Sonnet."}
  analyze:        {fit: good, note: "Ranked above Fable on the decomposition bench, below Astra and slightly below Sonnet (which cost about half). Not for sweeping 'find everything' audits."}
  bulk:           {fit: good, note: "Medium effort is cheap per task on AA ($1.34); 6.1 Sol is far cheaper on scoped work if the user has a Codex sub."}
  research:       {fit: good, note: "Clear, front-loaded reports; external web research specifically is not covered in research."}
  computer-use:   {fit: poor, note: "Verified its own web work 'surprisingly' well but 'not always'; weak on macOS. Route GUI work to OpenAI; if used, run on an isolated machine."}
  copy:           {fit: best, note: "Writing is the speaker's 'favorite change by far': leads with the important information, no anti-slop prompting needed."}
  3d-games:       {fit: good, note: "Strong in three.js/browser 3D and gameplay loops (Fish Slop 3D 'had to remind myself it's just a demo'); weaker on native tech; visual bugs persist."}
  prompt-writing: {fit: ok, note: "Not covered in research for this model; human-audit any prompt or skill it writes."}
  babysit:        {fit: good, note: "Took a bug from repo discovery to merged PR autonomously. Slow to commit and may stop to report; tell it to commit often and not to stop until green."}
  orchestrate:    {fit: good, note: "The speaker's preferred lead in the Opus + Sol/Sonnet setup, but reluctant to spawn subagents unless granted; constrain the subagent model so it doesn't pick Fable."}

role_hints:
  as_primary: "Default daily driver for most coding, writing and multi-phase implementation work, and the lead orchestrator that calls Sol/Sonnet/Fable."
  as_subagent: "Implementation subagent and the ZDR-compatible substitute for Fable."
  never_for: ["low effort", "max effort", "sole reviewer of Claude-written code", "open-ended front-end design without a style spec", "unsupervised macOS computer use"]
---

## Summary

The recommended default for most work: implementation, features, migrations,
writing, and leading other agents, at the best cost per completed task of the
Claude trio on a subscription. It is not the right model for open-ended front-end
design (use Fable), exhaustive review or deep investigation (use an OpenAI
model), or computer use. It needs explicit structure to run long: named stops,
"do all phases", and a subagent grant.

## Strengths

- **Default driver.** "I think Opus is probably the right default for the vast
  majority of stuff"; Anthropic says it "performs at the level of Fable 5.1 on
  most work and it costs 40% less to run than Opus 5"
  (`research/claude-releases.md § Video 2: Claude Opus 5.5 › 1. Subject and
  overall thesis`). By the Sonnet video the speaker "hasn't chosen Fable for any
  tasks for over a week" (`research/claude-releases.md § Video 3: Claude Sonnet
  5.5 › 1. Subject and overall thesis`).
- **Benchmarks at low cost.** Terminal Bench 4: medium beats Fable 5.1 max at
  $2.94 vs $20. Cursor Bench: medium beats Fable max. AA: it "swept" the Pareto
  frontier in the 50+ range; medium costs about $1.34 per task
  (`research/claude-releases.md § Video 2 › 2. Strengths (with evidence)`). The
  speaker thinks these benches flatter it.
- **Long unattended rewrites.** It restarted the TS-to-Rust port after months of
  stalled Astra/Sol work and "get it working in a day", for about "a grand in
  like a night with just two subscriptions": "for unattended long like heavy
  rewrite type stuff, Anthropic is just comically far ahead right now"
  (`research/gpt-releases.md § Video 2: GPT-6.1 Sol › 3. Weaknesses and
  pitfalls`). It also deleted about 1.6M lines of legacy slop when told to
  (`research/claude-releases.md § Video 3 › 6. Subagents, orchestration,
  delegation and verification`).
- **Communication and writing.** "My favorite change by far": it "puts the most
  important information up front". The speaker deleted his unslop instructions
  and won't re-add them. Reports state "what they did, what they found, and what
  it needs from you in plain language" (`research/claude-releases.md § Video 2 ›
  2. Strengths`; `research/claude-supplemental.md § Video 1: Getting the most out
  of Opus 5.5 › 5. Subagents, orchestration, delegation, verification, review,
  model choice`).
- **PR quality.** About 5 PRs: high-severity issue rate similar to Fable 5.1,
  slightly more nitpicks, "slightly higher overall quality, especially if you
  care about the quality of the prose" (`research/claude-releases.md § Video 2 ›
  2. Strengths`). Limited data.
- **End-to-end autonomy.** "Go through my computer, find the repo, and make a
  PR": it found the repo, refreshed the stale clone, made a worktree, filed and
  verified the PR, got it merged, for 1% of the weekly limit (same section).
- **Performance work and 3D.** Strong at "pretty brutal" performance
  optimisation; Fish Slop 3D at 120 FPS with a working gameplay loop; better at
  three.js than native tech.
- **Design when directed.** "If you tell it what you want, and more importantly,
  also tell it what you don't want, it can make really good designs"
  (`research/claude-supplemental.md § Video 1 › 3. Prompting guidance`).
- **ZDR available.** Zero data retention applies to Opus but not Fable/Mythos,
  which the speaker expects to make it "the most popular for coding with AI"
  (`research/claude-releases.md § Video 2 › 4. Pricing, speed, context and
  limits`).
- **Steering and collaboration.** It handles mid-run follow-ups as additions,
  not replacements; the speaker calls it "a more pleasant collaborator" than 6.1
  Sol and "significantly better at actually implementing code without getting
  blocked" (`research/gpt-releases.md § Video 2 › 5. Recommended prompting style
  and workflow`).

## Weaknesses and failure modes

- **Context anxiety.** While monitoring another instance it reported its
  "context is 10% from autocompact ... if it crashed that work would be lost".
  The speaker: "None of this is stuff the model should think about or care
  about." It should trust compaction, which works and is fast
  (`research/claude-releases.md § Video 2 › 3. Weaknesses, pitfalls and
  misconceptions`). Tell it compaction is handled and not to stop for it.
- **Stops between phases.** Anthropic's guide: "On long tasks, it'll sometimes
  stop to report instead of going on: a summary that names the next step without
  taking it, an offer to continue, or a list of choices that don't actually block
  the work." An explicit "follow its phase 0 to 7 in order" prompt still stopped
  after phase 0 (`research/claude-supplemental.md § Video 1 › 4. Pitfalls and
  misconceptions corrected`). Name the stops; auto-reply "continue" to
  non-blocking "Want me to continue?" endings.
- **Reluctant to spawn subagents.** "Opus 5.5 seems less willing to spin up
  subagents unless you tell it that it can ... Even then it doesn't always do
  it" (Theo, not the guide; `research/claude-supplemental.md § Video 1 › 5.
  Subagents ...`). For known-parallel work, instruct it directly.
- **Slow to commit.** One performance run held "almost three hours" of changes
  local and uncommitted. Telling it to commit frequently is an inference from
  this, not a stated tip (`research/claude-releases.md § Video 2 › 5.
  Recommended prompting style and workflow`).
- **Runaway at max.** A max-effort thread ran 6.5 hours "writing a markdown plan
  ... in loops forever"; switched to high and asked for status, it finished in
  about 10 minutes. SkateBench: max used 13x the cost, 15x the tokens, 20x the
  worst-case latency for one extra correct answer
  (`research/claude-supplemental.md § Video 1 › 4. Pitfalls`).
- **Low is poor.** "Low is really bad ... not that capable considering the
  price"; no no-reasoning mode exists because "these models suck without
  reasoning".
- **Dumb spikes and "small model feel".** "This model is smaller. It is dumber.
  It will make mistakes. So will Fable, just less so." Discernment weakens in
  degraded states, and on performance work it may "get stuck repairing things it
  doesn't need to". Failure odds rise with job length
  (`research/claude-releases.md § Video 2 › 3. Weaknesses`). In fleet management
  it made "a couple dumb mistakes" (`research/gpt-releases.md § Video 2 › 3.
  Weaknesses and pitfalls`).
- **Misses mess and regressions.** It rewrote the Rust port in a new crate
  without deleting the old 1.3M unused lines; 6.1 Sol found regressions "entirely
  missed by Fable and by Opus" (`research/gpt-releases.md § Video 2 › 2.
  Strengths, with evidence`).
- **Weaker reviewer and auditor.** Below Grok 4.7, Sol and Astra on the
  speaker's audit bench; "Fable is still slightly more thorough"
  (`research/claude-releases.md § Video 2 › 3. Weaknesses`).
- **Front end without direction.** "Half of them are Tailwind templates, the
  other half are this very specific ... color pastel with the big shadows"; the
  design skill barely helps (same section). Mia's 100-page HTML test ranked it
  best ever, a dissenting data point.
- **Token-hungry.** "Meaningfully less efficient than Opus 5"; it came close to
  the most expensive AA run "simply because of how many tokens it is using".
- **Will spawn Fable subagents.** The Fish Slop run used a Fable 5.1 subagent
  unintentionally, inflating cost (`research/claude-releases.md § Video 3 › 3.
  Weaknesses, pitfalls and misconceptions`).
- **Safeguards.** First Opus with Fable-level bio and cyber safeguards; flagged
  messages move to older models. Avoid "show your reasoning" wording, which
  risks a flag (`research/claude-supplemental.md § Video 1 › 3. Prompting
  guidance`).
- **Computer use on macOS.** "As long as you don't use Macs." Run long or
  computer-use agents on remote machines.

## How to prompt it

Every prompt states three things: what you want, what "done" means, and the out
(Theo: "the perfect simple one two three"). Give the whole task in one message,
pre-authorise expected risky actions, and say what you don't want ("being
explicit about what you don't want is even better").

**Canonical three-part prompt** (Anthropic Opus 5.5 guide by Addy Osmani):

> Migrate the payments endpoint from the old client to the new one. Done means
> every endpoint uses the new client, the old one is deleted, and the test suite
> passes. Stop and ask me only if a test fails for a reason that you can't
> explain.

**Named-stops rule for CLAUDE.md** (Anthropic guide; Theo pasted it under his
"approvals" section). "It follows instructions that name the stops":

> When a step doesn't need my input, keep going. Put status notes in the same
> message as your next action. Stop and ask only when you can't continue without
> me or before anything destructive: deleting data, force pushing, or changing
> anything outside of this repo.

For pair programming, the guide suggests the reverse: "a one-line plan before
it starts and a short recap at the end."

**Subagent grant** (Theo; append to lead-agent prompts):

> Use subagents and workflows however you choose. I trust your judgment there.

For work that is known to parallelise (mass PR review, codebase audits), state
it directly: "use subagents".

**Multi-phase continuation** (Theo, after the phase-0 stop):

> I want you to hold off on all questions until the very end when you get
> through to phase 7 in completion. I don't want you to stop after every phase to
> ask for permission to continue. I want you to do the whole thing. Continue
> working on this port until the entirety of it is completed and don't inform me
> until you have a Tailscale link I can click on. That is the complete rewrite so
> I can test it and make sure everything works. Don't worry about how it's
> hosted. Don't worry about how it's built. Just worry about completing the work
> as assigned.

**The out** (Theo calls it "what might be the most important piece"): end
long-run prompts with "If anything does not work as expected ..., don't hesitate
to ask questions". Models are "RL'd to hell and back to not give up", and this
gives permission to stop and ask.

**Design prompts** (Anthropic guide): "A general instruction like avoid generic
looks will mostly just swap one default for another. A list of specific patterns
will work much better."

> Build a personal website with placeholder content. Don't use a cream or
> off-white background, italic accent words in headings, numbered 1, 2, 3 section
> labels, monospace labels, or pill-shaped buttons.

Iterate by adding each disliked element to the list, or paste an annotated
screenshot with "This sucks. Make it better."

**End-of-run reporting:**
- The guide suggests ending every run with three headings: **Blocked on me,
  Changed, Found.** The orchestrator reads "Blocked on me" first.
- Theo's check-ins: "What's the status of this work? What do you need from me?"
  and "What are the risks of merging this code today?"
- For reviews: ask it to mark what it could not confirm, and why.

**Leave out:**
- "Think hard / think carefully" lines ("Don't tell it to think hard, it will
  anyways").
- "Show your reasoning"; ask "explain why you made these changes" instead.
- Anti-slop or unslop instructions (no longer needed).

**Other rules:**
- Steer a running thread with follow-ups instead of restarting it.
- Attach screenshots and charts rather than pasting errors.
- If a max run seems stuck: stop it, switch to high/xhigh, ask "what's the state
  of the work", then say "continue".
- Tell it compaction is handled, to counter context anxiety.
- Constrain which model its subagents may use.

Compared with Fable 5.1, Opus needs more explicit structure (named stops,
"do all phases", subagent grant, design negatives) and no anti-slop prompting.

## Routing guidance

Route here for:
- Day-to-day coding, bug fixes, features, migrations and performance work.
- Long, multi-phase implementation runs and heavy rewrites (with named stops).
- User-facing writing, explanations and status reports.
- Leading multi-agent work as the orchestrator, with explicit grants.
- Any coding workload that requires zero data retention.
- three.js and browser-game builds.

Do not route here for:
- Open-ended front-end or marketing design without a style spec (Fable).
- Exhaustive code review, "find everything wrong" audits or sweeping
  architecture critiques (6.1 Sol, Astra, Grok 4.7).
- Deep root-cause hunts in degraded systems (6.1 Sol, or Fable for wide fixes).
- Computer use, especially on macOS (OpenAI via Codex).
- Low or max effort, ever.

Handoff patterns:
- **Opus delegates review to OpenAI.** Opus implements; 6.1 Sol reviews (reading
  code and reproducing with computer use); findings go back to Opus; Opus fixes;
  Sol re-reviews; then merge. The speaker already has Sol callable from inside
  Claude Code for this (`research/gpt-releases.md § Video 2 › 8. Using it inside
  or alongside Claude Code`).
- **Opus delegates investigation.** Root-causing, triage and "what needs to be
  touched and why" go to 6.1 Sol; bounded codebase deep dives go to Sonnet 5.5,
  which "will result in Opus feeling way faster" (`research/claude-releases.md §
  Video 3 › 5. Recommended prompting style and workflow`).
- **Opus escalates design to Fable** for front-end and marketing pages, and for
  wide work where its output missed the bar.
- **Opus rescues stalled OpenAI rewrites** (the TS-to-Rust port), then Sol
  audits the result for dead code.
- **Opus as Fable's fallback.** It serves Fable's safeguard-flagged requests and
  replaces Fable where ZDR is required.
- **Opus as judge.** It blind-evaluated 6.1 Sol's work for the speaker.

## Cost notes

- $4 / $20 per M in/out, cache reads $0.20/M ("60% cheaper"), cache writes $5/M.
  Anthropic: 40% cheaper than Opus 5 on typical workloads.
- Cache reads are about 20% of its agentic bill (vs under 5% for Fable, 50%+ for
  Sonnet), per the Sonnet video. That is why Sonnet is not cheaper than Opus in
  long loops.
- AA per task: medium about $1.34, high about half of Astra max ($3.26), xhigh
  approaching Astra, max "almost six bucks" (about 120K tokens per task).
- Subscription is where it wins: "The amount of value you get out of your $200
  sub in Claude, it is running laps around our friends at OpenAI", "maybe not in
  the pure API prices". On API, 6.1 Sol matched Opus 5.5 max on DeepSWE at about
  1/70 of the cost (`research/gpt-releases.md § Video 2 › 2. Strengths, with
  evidence`).
- Effort can be raised or lowered mid-session without busting the cache. A
  value pattern: draft at medium/high, then a polish pass at xhigh.
- Fast mode exists for Opus (2x price per the bundled API reference); not
  discussed in research.
- Watch for, and forbid unless wanted, Fable subagents spawned by Opus.

## Evidence

- `research/claude-releases.md § Video 2: Claude Opus 5.5` (all sections),
  `§ Video 3: Claude Sonnet 5.5 › 3. Weaknesses, pitfalls and misconceptions`,
  `› 6. Subagents, orchestration, delegation and verification`, and
  `§ Cross-video synthesis (for the routing table)`.
- `research/claude-supplemental.md § Video 1: Getting the most out of Opus 5.5`
  (all sections; reads Anthropic's guide by Addy Osmani).
- `research/gpt-releases.md § Video 2: GPT-6.1 Sol` (sections 1–3, 5–9) and
  `§ Cross-video synthesis (for the routing table)`.
- `research/model-selection.md` covers only unversioned Opus / Opus 5 ("Opus
  sucks"); it does not apply to 5.5 and is not used for scores.
- API id, 1M context, medium as the API default effort and the fast-mode price
  come from the bundled Claude API reference (model table cached 2026-09-25),
  not from `research/`.
- Release month: not stated (`released: null`); the Sol video says it shipped
  "the previous week".
- Transcript ambiguities: the release video gives medium as the default effort,
  while the supplemental video's speaker leaves it on high or xhigh. This
  profile recommends high, with medium for cost. Edwin's "medium is Fable 5.1
  level intelligence" is disputed by the speaker ("a bit of a reach"). The Sol
  video's fish-slop costs ($50 for Opus) are contaminated by an accidental Fable
  subagent. The Opus review-bench finding count is not stated.

### Score rationale

| Axis | Score | Why |
|---|---|---|
| intelligence | 8 | Tops most coding benches and AA, but the speaker: "smaller ... dumber ... will make mistakes"; Fable and Astra handle harder unsupervised problems. |
| taste | 7 | Best prose of the trio and steerable design, but sloppy default front ends and the design skill barely helps; one step below Fable. |
| floor | 7 | Lands long rewrites and PR quality is close to Fable, but it has dumb spikes, context anxiety and repair loops, and "spikes down ... a little lower than Fable". |
| thoroughness | 5 | Below Fable, Astra, Sol and Grok 4.7 at finding issues; Sol found regressions it missed; precise (no contradicted findings) but not exhaustive. |
| cost_efficiency | 6 | Best cost per completed task in the Claude trio (medium about $1.34/task; Pareto sweep), strongest on subscription; token-hungry, and 6.1 Sol is far cheaper on scoped work. |
| speed | 7 | About 30% faster than Opus 5; about 70 TPS (API) and about 100 (subscription); beat Sonnet on wall-clock in Fish Slop (36 vs 43 min); took about 2x Sonnet's time on the bounded audit. |
| computer_use | 4 | Verified its own web work but "not always", weak on macOS; OS World "neck and neck" with Sonnet; OpenAI far ahead. |
| orchestration | 7 | Led the Rust rewrite and cross-machine work and is the speaker's planned lead, but must be granted subagents, stops between phases and may pick Fable subagents unasked. |
