---
id: claude-fable-5-2
name: Claude Fable 5.2
vendor: anthropic
family: claude
status: current
released: 2026-11
as_of: 2026-11-13
confidence: medium

api_ids: [claude-fable-5-2]
access:
  subscriptions: [claude-pro, claude-max]
  api: true
  harnesses: [claude-code, cursor, opencode, t3-code, openclaw, hermes]
  invoke_via: [claude-cli, cursor-cli, openclaw-cli, hermes-cli]   # same reach as Fable 5.1; Claude subscription OAuth is restricted or disallowed in openclaw/hermes, see the bridges

pricing_per_mtok:
  input: 8
  output: 40
  cache_read: 0.20
  cache_write: 10
context_window: 1000000
notes_on_cost: >
  Every price is 20% below Fable 5.1 ($8 / $40, cache reads $0.20, 5-minute cache
  writes $10, 1-hour $16), and the full 1M window is at standard pricing. Cache reads
  now cost the same as Opus 5.5's; input, output and writes are still 2x Opus. Fast
  mode is 2x the price for up to 2.5x output speed. On a Claude subscription the 7-day
  Fable limit sits on top of the weekly limit: each Fable point also burns half a weekly
  point, so draining Fable on a $200 plan cuts API-equivalent value from about $14K a
  month (Opus only) to about $10K. Spend Fable quota on hard work, not routine features.

effort:
  levels: [low, medium, high, xhigh, max]
  default: high
  avoid: [max]
  notes: >
    high by default; xhigh tops Anthropic's Frontier Code chart at roughly Opus-max
    cost; max scores worse on most coding tasks on Anthropic's own chart, so never max.
    Default conflicts between sources (API high, Claude apps and Claude Code medium):
    set it explicitly.

scores:
  intelligence: 10
  taste: 8
  floor: 7
  thoroughness: 6
  cost_efficiency: 5
  speed: 7
  computer_use: 4
  orchestration: 8

tasks:
  quick-fix:      {fit: good, note: "Clears the bar, but Opus 5.5 does too at half the price and without burning Fable quota."}
  feature:        {fit: good, note: "Below Opus 5.5 on the speaker's own codebase benches and needs more supervision; Anthropic and the speaker both name Opus 5.5 the daily driver. Escalate here for hard or cross-package features."}
  long-run:       {fit: best, note: "Better at 'not getting blocked in long runs and solving hard problems in long runs', and stays more coherent over long runs; add checkpoints because it can spiral on an unimportant decision."}
  frontend:       {fit: best, note: "Best visuals available with Anthropic's design skill loaded ('Tailwind template slop' without); name every deliverable, because it misses implied ones (a diagram, a chart that shows the gap)."}
  review:         {fit: ok, note: "A ship-or-not gate, not an exhaustive finder: it lets slightly wrong code through more often than Opus or Sonnet on Theo's evals, but everything it called mergeable so far was. About 120 minutes for 8 PRs; too slow for a review loop."}
  investigate:    {fit: good, note: "Lead it on the root cause, not on building the repro: it gave the one-line root cause where Terra produced six rounds of noise and caught the flaw an Opus-built repro missed, but Opus 5.5 builds the more thorough repro or test environment, so have Opus build it and Fable work it. Give it the sources so it can disprove itself."}
  analyze:        {fit: ok, note: "Made 4 false claims of 61 (about $23) where 6.1 Sol made none of 38 ($4.19), and ranked third behind Opus 5.5 on T3 Code; in data analysis it jumps and skips outside context."}
  bulk:           {fit: poor, note: "Expensive and quota-capped; use cheaper models."}
  research:       {fit: ok, note: "Big vendor gains on agentic science research (74.6 vs 52.6 for Fable 5.1), but the speaker found research and analysis results mixed: novel ideas, unjustified jumps."}
  computer-use:   {fit: poor, note: "No new evidence for 5.2; Fable 5.1 trailed OpenAI models far behind."}
  copy:           {fit: good, note: "'Better at writing prose in general and talking to models'; still adds eyebrow text and subheadings until told not to."}
  3d-games:       {fit: good, note: "Better-looking and far smoother 3D than OpenAI builds, but 'Opus actually makes more fun games'; pair Fable visuals with Opus game feel."}
  prompt-writing: {fit: good, note: "Used to overhaul skills and copy and is better at 'talking to models'; human-audit any prompt or skill it writes."}
  babysit:        {fit: good, note: "Carried from Fable 5.1 (untested on 5.2); quota-expensive for long polling loops."}
  orchestrate:    {fit: best, note: "Anthropic positions it as orchestrator or adviser to smaller models; inherits Fable 5.1's subagent planning (untested on 5.2). Every Fable subagent burns Fable quota."}

role_hints:
  as_primary: "Hardest open-ended technical work and unprovable work (design, novel approaches, choosing among very different options): long autonomous runs, front-end design, hard bugs, non-coding science and engineering."
  as_subagent: "Adviser that an Opus 5.5 lead consults on hard problems, and design specialist for front-end work."
  never_for: ["max effort", "workloads requiring zero data retention (ZDR) without Anthropic's authorisation", "routine features when Fable quota is limited", "bulk mechanical work", "unsupervised taste-sensitive decisions", "unsupervised macOS computer use"]
---

## Summary

The most capable Claude model, and the step up from Opus 5.5, not a replacement
for it. Route the hardest open-ended work here: long runs that must not stall,
hard bugs, front-end design and non-coding science and engineering. Opus 5.5
stays the daily driver for features. Fable 5.2 makes occasional mistakes that
are obvious to a human and needs more supervision than Opus. It is also slow as
a reviewer and has no zero data retention without Anthropic's authorisation.

## Strengths

- **Benchmark leader.** It holds the top Artificial Analysis Intelligence Index
  score, 4.5 to 5 points ahead of Gemini 4 Carbon
  ([FAB52 0:52](https://youtu.be/yh5IAUow4Hc?t=52)). On Frontier Code 2 it scores
  70 vs 65 for GPT-6 Astra, and on agentic science research 74.6 vs 52.6 for
  Fable 5.1 and 68.1 for Astra
  ([FAB52 8:09](https://youtu.be/yh5IAUow4Hc?t=489);
  [FAB52 8:20](https://youtu.be/yh5IAUow4Hc?t=500)). It also posts big gains on
  CAD and robotics, and through Mythos on cyber and protein design. "A lot of
  the value in this model is in the sciences outside of computer science"
  ([FAB52 8:37](https://youtu.be/yh5IAUow4Hc?t=517)).
- **Long-run capability.** It is better at "not getting blocked in long runs and
  solving hard problems in long runs"
  ([FAB52 38:50](https://youtu.be/yh5IAUow4Hc?t=2330)) and "stays more coherent
  over long runs slightly" ([FAB52 45:23](https://youtu.be/yh5IAUow4Hc?t=2723)).
  "It actually unblocks itself quite well"
  ([FAB52 33:44](https://youtu.be/yh5IAUow4Hc?t=2024)).
- **Plain diagnosis.** Asked why one machine was slower, after Terra had given six
  rounds of noise: "Cup 2 is a VPS. The other three are physical machines with
  local NVME drives. That is the full reason"
  ([FAB52 35:20](https://youtu.be/yh5IAUow4Hc?t=2120)).
- **Pushback and self-correction.** It rejected an absurd MCP setup step that
  Opus 5.5 and another model had recommended for hours. When pointed at his
  history it disproved itself: "it's not scared to push back"
  ([FAB52 37:17](https://youtu.be/yh5IAUow4Hc?t=2237);
  [FAB52 37:56](https://youtu.be/yh5IAUow4Hc?t=2276)).
- **A trustworthy last review.** "If Fable thinks a PR is good to go. It'd be
  surprising if it isn't." It lets nitpicks slide and "doesn't get stuck anywhere
  near as bad as other models do"
  ([FAB52 21:30](https://youtu.be/yh5IAUow4Hc?t=1290);
  [FAB52 21:46](https://youtu.be/yh5IAUow4Hc?t=1306)).
- **Visual quality.** With the design skill loaded it produced
  polished pages and explainers
  ([FAB52 40:47](https://youtu.be/yh5IAUow4Hc?t=2447)). Fish Slop "looked quite
  a bit better" than the Opus build and ran "a hell of a lot better than anything
  I've gotten out of an OpenAI model"
  ([FAB52 43:36](https://youtu.be/yh5IAUow4Hc?t=2616)).
- **Writing.** It is "better at writing [prose] in general and talking to
  models" ([FAB52 34:22](https://youtu.be/yh5IAUow4Hc?t=2062)).
- **Speed.** 106 TPS against 81 to 84 for Fable 5.1 and 112 for Opus 5.5
  ([FAB52 28:22](https://youtu.be/yh5IAUow4Hc?t=1702)). Fast mode is available.

## Weaknesses and failure modes

- **Capability without autonomy.** "Much more capable, but it does not have
  much more autonomy". It is "not going to magically make tasteful decisions
  where other models wouldn't have"
  ([FAB52 38:39](https://youtu.be/yh5IAUow4Hc?t=2319);
  [FAB52 39:07](https://youtu.be/yh5IAUow4Hc?t=2347)).
- **Over-clever.** "Fable tries a little too hard to be clever"
  ([FAB52 45:53](https://youtu.be/yh5IAUow4Hc?t=2753)). It is the smart
  colleague who "occasionally will not understand the full situation" and says
  something from left field ([FAB52 10:40](https://youtu.be/yh5IAUow4Hc?t=640)).
- **Spirals on small decisions.** "It will make a decision that's not super
  important and then spiral down it in ways that are obviously wrong to a
  human." "I've had to be in the loop a lot more with this model"
  ([FAB52 33:22](https://youtu.be/yh5IAUow4Hc?t=2002);
  [FAB52 33:51](https://youtu.be/yh5IAUow4Hc?t=2031)).
- **Obvious mistakes.** A "safe mode" built to hide personal details for filming
  showed his email address in the banner announcing safe mode: "the types of
  mistakes I would never have expected even Opus to do"
  ([FAB52 38:31](https://youtu.be/yh5IAUow4Hc?t=2311)).
- **Missed deliverables.** A redesign that "does not very clearly visualize the
  gap between these numbers", the page's whole point, and also changed the
  screenshots unasked ([FAB52 22:42](https://youtu.be/yh5IAUow4Hc?t=1362)). An
  architecture explainer with "no diagram" after being told to update the last
  diagram ([FAB52 40:47](https://youtu.be/yh5IAUow4Hc?t=2447)).
- **Below Opus on the speaker's own benches.** "Underperforming Opus and Sonnet"
  on codebase analysis and PR review "in almost all of them"
  ([FAB52 9:53](https://youtu.be/yh5IAUow4Hc?t=593)). TS Rust: 61 claims, 4
  wrong, about $23, against 6.1 Sol's 38 claims, none wrong, $4.19. T3 Code:
  third, with 6 false claims of 83
  ([FAB52 20:18](https://youtu.be/yh5IAUow4Hc?t=1218);
  [FAB52 20:52](https://youtu.be/yh5IAUow4Hc?t=1252)).
- **Slow reviewer.** About 120 minutes of runtime for 8 PRs, against roughly 20 to
  30 for the GPT models ([FAB52 21:08](https://youtu.be/yh5IAUow4Hc?t=1268)).
- **Max effort is worse.** "Fable 52 Max will score worse on most coding tasks
  consistently and you should not use it as a developer"
  ([FAB52 12:04](https://youtu.be/yh5IAUow4Hc?t=724)).
- **Data-analysis jumps.** It makes "jumps sometimes that don't make real sense"
  and forgets to check events outside the data set
  ([FAB52 17:22](https://youtu.be/yh5IAUow4Hc?t=1042)).
- **UI tics.** Unneeded eyebrow text and subheadings
  ([FAB52 34:06](https://youtu.be/yh5IAUow4Hc?t=2046)). Without the design skill
  it produces "Tailwind template slop"
  ([FAB52 32:27](https://youtu.be/yh5IAUow4Hc?t=1947)).
- **Game feel trails Opus.** "Opus actually makes more fun games. Fable just
  makes them look a lot better" ([FAB52 45:23](https://youtu.be/yh5IAUow4Hc?t=2723)).
- **Data retention.** The model page says it "requires 30-day data retention and
  isn't available under zero data retention unless expressly authorized by
  Anthropic". The announcement says eligible customers can continue with ZDR.
  The speaker treats it as no ZDR
  ([FAB52 17:44](https://youtu.be/yh5IAUow4Hc?t=1064)). Enterprise Frontier
  Safeguards is in private beta.
- **Safeguards.** Fable refuses cyber and bio tasks; those need Mythos 5.2
  ([FAB52 8:56](https://youtu.be/yh5IAUow4Hc?t=536)).
- **Carried from Fable 5.1 (not retested):** few progress updates on long runs,
  dense prose, append-only history on the API, and scope overreach on narrow
  tasks. Keep the Fable 5.1 prompt blocks until shown unnecessary.

## How to prompt it

Start from the Fable 5.1 profile's blocks (autonomy, anti-scope-creep, progress
updates, mannered prose). They come from Anthropic's 5.1 guide and have not
been retested on 5.2. Then add:

- **Set effort explicitly** to `high` (or `xhigh` for one bounded hard pass).
  The default differs by surface: `high` on the API, `medium` in Claude Code.
- **Name every deliverable.** Write "include the architecture diagram" rather than
  "update the explainer". Implied deliverables are where it misses.
- **Hand it the evidence.** Point it at history, logs or data and ask it to check
  its own claim. It reliably disproves itself when given sources.
- **In data analysis, ask for outside context**, such as release dates or other
  events, before it explains a change in the numbers.
- **Kill the eyebrow text** with a CLAUDE.md or AGENTS.md rule. The speaker
  asked the model what it calls the pattern and wrote the rule in its words
  ([FAB52 34:15](https://youtu.be/yh5IAUow4Hc?t=2055)).
- **Load the front-end design skill** for any UI work.
- **Add checkpoints on long runs**, so a human or a cross-family reviewer catches
  a spiral on an unimportant decision early.

## Routing guidance

Route here for:
- Long, hard autonomous runs where getting unblocked matters more than speed.
- Front-end and visual work, with the design skill loaded.
- Hard bugs where a direct root cause beats a long report.
- Non-coding science and engineering: CAD and hardware, robotics, science
  research. Use Mythos 5.2 for cyber and bio if the organisation is verified.
- Adviser calls from an Opus 5.5 lead on problems Opus is stuck on.
- Unprovable work, where "you cannot objectively say this is better than
  that": graphics, a visualiser that doesn't look like every other one,
  infrastructure ideas, open-ended exploration. "Fable is going to find things
  opus never [will]" ([OVF 36:01](https://youtu.be/XtykeVoSmP8?t=2161)). The routing question: can the result be
  checked and hill-climbed? Yes goes to Opus 5.5; no goes to Fable.
- A wider spread of options when Opus's alternatives cluster around one idea
  ([OVF 38:28](https://youtu.be/XtykeVoSmP8?t=2308)).
- Leading orchestrated efforts, with subagents pinned to cheaper models.

Do not route here for:
- Routine features and quick fixes: Opus 5.5 is the daily driver per Anthropic
  and the speaker, at half the price and without Fable quota.
- Codebase analysis when GPT-6.1 Sol or Opus 5.5 is available (fewer false
  claims, far cheaper).
- Review loops: at about 15 minutes per PR, use it only as a final gate.
- Building exhaustive repro or test environments, or changes that must be
  perfect: it "did not have all the edges" where Opus did
  ([OVF 30:26](https://youtu.be/XtykeVoSmP8?t=1826)).
- Taste-sensitive product decisions without a human check.
- Max effort, bulk work, or workloads that need ZDR (use Opus 5.5).

Handoff patterns:
- **Opus leads, Fable advises.** Opus 5.5 does the bulk of the work and consults
  Fable 5.2 when stuck.
- **Fable designs, Opus tunes feel.** For games and interactive UI, combine Fable
  visuals with Opus gameplay and UX judgment ("a combination of Opus and Fable is
  the way to go", [FAB52 44:01](https://youtu.be/yh5IAUow4Hc?t=2641)).
- **Fable as the final PR gate** after a faster reviewer has cleared the loop.
  Its job there is "is this good enough to ship", not finding every issue: on
  Theo's evals it lets slightly wrong code through more often than Opus or
  Sonnet, but "everything Fable said was good to merge ended up being good to
  merge" ([OVF 40:46](https://youtu.be/XtykeVoSmP8?t=2446)).
- **Fable rescues stuck work** (carried from 5.1, confirmed on 5.2): when Opus
  has been running in circles on a branch, ask Fable to "audit the work that was
  done here and tell us what we should actually do next". It may fix what Opus
  could not, or rule that it is already fine and merge ([OVF 39:28](https://youtu.be/XtykeVoSmP8?t=2368),
  [OVF 41:33](https://youtu.be/XtykeVoSmP8?t=2493)).
- **Opus builds, Fable audits.** "Verify the work Opus did here … Then I want
  you to play with it and find the edges that actually cause problems and
  propose solutions" found a 150x payload cut Opus had missed
  ([OVF 29:50](https://youtu.be/XtykeVoSmP8?t=1790)).

## Cost notes

- Official prices, fetched 2026-11-11: $8 / $40 per M in/out, cache reads $0.20,
  5-minute cache writes $10, 1-hour writes $16, batch $4 / $20. Fast mode costs
  $16 / $80 and is not available on Batch or Bedrock. Fable 5.1 was $10 / $50 /
  $0.25.
- Fable 5.2 `high` costs about the same as Opus 5.5 `xhigh`, and Fable `xhigh`
  about the same as Opus `max`, on Frontier Code
  ([FAB52 12:44](https://youtu.be/yh5IAUow4Hc?t=764)). At equal spend, the
  choice is which model, not which effort level.
- Subscription ($200 plan, the speaker's math): about $14,062 a month of
  API-equivalent usage with Opus 5.5 only (73x). Fable to its limit and then Opus
  gives about $3K + $7K. Fable alone gives about $3K (15x)
  ([FAB52 26:24](https://youtu.be/yh5IAUow4Hc?t=1584);
  [FAB52 29:46](https://youtu.be/yh5IAUow4Hc?t=1786)). Each point of the 7-day
  Fable limit also uses half a weekly point. A launch reset restores both.
- Official plan wording conflicts: the announcement gives Pro and standard Team
  seats Fable "up to 50% of weekly usage limits", while claude.com/pricing lists
  Pro as "paid with usage credits". Check the plan.

## Evidence

- OVF: "I think I figured it out", Theo (t3.gg), YouTube,
  https://youtu.be/XtykeVoSmP8 (2026-11-12, two days into Fable 5.2). Digest:
  `research/claude-supplemental.md` Video 3.
- FAB52: "Nobody Is Competing With Anthropic", Theo (t3.gg), YouTube,
  https://youtu.be/yh5IAUow4Hc. Filmed after about 14 hours with the model and
  about 20 landed PRs, without early access. Digest:
  `research/claude-releases.md` Video 5.
- Official: "Introducing Claude Fable 5.2 and Claude Mythos 5.2" (2026-11-09),
  https://www.anthropic.com/claude-fable-and-mythos-5-2; model page
  https://platform.claude.com/docs/en/models/fable-5-2/overview; pricing
  https://platform.claude.com/docs/en/about-claude/pricing (all fetched
  2026-11-11). API id `claude-fable-5-2`; Mythos 5.2 is `claude-mythos-5-2`,
  verified organisations only. 1M context, 128K max output, adaptive thinking
  always on.
- Carried from the Fable 5.1 profile without new evidence: computer use,
  babysitting, orchestration mechanics and prompt quirks.
- Unresolved: the speaker says Fable is "massively outperforming OpenAI models"
  on his eval set ([FAB52 9:53](https://youtu.be/yh5IAUow4Hc?t=593)), but
  later shows 6.1 Sol beating it on TS Rust and Sol and Astra building "more
  cohesive understandings". This profile follows the numbers.

### Score rationale

| Axis | Score | Why |
|---|---|---|
| intelligence | 10 | Top of the AA index by 4.5 to 5 points and wins most of Anthropic's suite, including over GPT-6 Astra; the frontier as of 2026-11. |
| taste | 8 | Best visuals with the design skill and better prose, but misses implied deliverables, and Opus makes more fun games; "not going to magically make tasteful decisions". |
| floor | 7 | Down from Fable 5.1's 9: spirals on unimportant decisions, needs more supervision than Opus, and made a mistake "I would never have expected even Opus to do". Level with Opus 5.5; one day of evidence. |
| thoroughness | 6 | A "fine-tuned comb" reviewer that misses some issues; 4 to 6 false claims in codebase analysis. |
| cost_efficiency | 5 | 20% cheaper than Fable 5.1, with cache reads equal to Opus, but still 2x Opus otherwise, slow as a reviewer, and each Fable point burns half a weekly point on subscriptions. |
| speed | 7 | 106 TPS, within about 5% of Opus 5.5, plus fast mode; offset by 120-minute review runs. |
| computer_use | 4 | No new evidence; carried from Fable 5.1. |
| orchestration | 8 | Anthropic positions it as orchestrator and adviser; carried from Fable 5.1's demonstrated subagent planning, untested on 5.2. |
