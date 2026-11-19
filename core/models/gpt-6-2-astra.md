---
id: gpt-6-2-astra
name: GPT-6.2 Astra
vendor: openai
family: gpt
status: current
released: 2026-11                # 2026-11-17, alongside GPT-6.2 Sol
as_of: 2026-11-19
confidence: medium               # one launch review (early access, Astra-focused) plus OpenAI's model and pricing pages; the launch post was not readable

api_ids: [gpt-6.2-astra]
access:
  subscriptions: [chatgpt-plus, chatgpt-pro]   # OpenAI's Codex page says "supported plans" without naming them; assumed same as GPT-6 Astra
  api: true                      # Responses, Chat Completions, Batch; not Realtime, Assistants or fine-tuning
  harnesses: [codex, cursor, opencode, t3-code, openclaw, hermes]   # codex confirmed (`codex -m gpt-6.2-astra`); the rest inherited from GPT-6 Astra, unverified for 6.2; cursor access to OpenAI models reportedly revoked (see gpt-6-astra.md)
  invoke_via: [codex-cli, cursor-cli, opencode-cli, openclaw-cli, hermes-cli, openai-api]   # openai-api added now that the API id is confirmed; the others unverified for 6.2

pricing_per_mtok:
  input: 8
  output: 40
  cache_read: 0.40
  cache_write: 10                # 30-minute retention; 20 for 12-hour
context_window: 1050000          # 922K max input, 128K max output; Codex defaults to 272K
notes_on_cost: >
  Same list price as Fable 5.2 ($8 / $40), with cache reads at $0.40 (Fable
  5.2 $0.20, GPT-6 Astra $1). It cost about half of Fable 5.2 to run Theo's
  benches. Above 272K input, input and cache double and output is 1.5x. Fast
  mode is 2x; Ultrafast 3x until 2027-02-28, then 6x; Batch half. The real
  cost risk is not price but runs that ship nothing: 11 days on one goal
  without a single landed compiler improvement. On a Codex subscription the marginal cost is close to
  zero.

effort:
  levels: [low, medium, high, xhigh, max]
  default: high                  # the kit's default; OpenAI's API pages don't state one
  avoid: [max]
  notes: >
    High. OpenAI's own charts show xhigh below high on two science benches and
    max below lower efforts on "agents last exam", so don't assume more effort
    helps. Use xhigh only for a bounded exhaustive pass. Avoid fast mode
    (carried from GPT-6 Astra; the 6.2 video doesn't test it).

scores:
  intelligence: 9
  taste: 4
  floor: 3
  thoroughness: 10
  cost_efficiency: 7
  speed: 4
  computer_use: 10
  orchestration: 5

tasks:
  quick-fix:      {fit: ok,   note: "fine code on short tasks, but its explanation is harder to read than the diff; Opus 5.5 or Sol first"}
  feature:        {fit: ok,   note: "code quality up on GPT-6 Astra, still below Opus and Fable; Theo would not pick it over Opus 5.5 for any dev work"}
  long-run:       {fit: poor, note: "blocks itself on questions only it understands, and looped 11 days on a two-part goal without landing a compiler improvement; Opus then made it 50% faster in two days"}
  frontend:       {fit: poor, note: "OpenAI's best web design yet, still behind Fable 5.2; GPT UI-isms, filler subtitles in games, overused image gen"}
  review:         {fit: best, note: "near-perfect on Theo's evals and 'never lying'; have Claude restate findings in plain language before acting; 6.x Sol is cheaper for routine PRs"}
  investigate:    {fit: ok,   note: "finds things, but buries the root cause (four paragraphs of pnpm internals where Opus said 'the SSD is slow'); pair with a Claude summary"}
  analyze:        {fit: good, note: "thorough, but its reports are hard to parse; have a Claude model summarise"}
  bulk:           {fit: ok,   note: "works, but 4x Sol's per-token price for no gain on mechanical work"}
  research:       {fit: ok,   note: "best science model per OpenAI and Theo, but a research report is read by a human and its reports are hard to parse; have Claude summarise"}
  computer-use:   {fit: best, note: "'absolutely cracked', batches many actions per call; cap its disk and RAM use and check cleanup"}
  copy:           {fit: poor, note: "reads 'like somebody who doesn't speak English'; failed tone-matching after repeated instructions"}
  3d-games:       {fit: best, note: "visuals, 3D assets and play testing; level design, payoff and game feel go to Claude; no pixel-exact art"}
  prompt-writing: {fit: ok,   note: "'writes pretty good sub agent prompts', but its English is poor; fine for prompts other agents read, not for skills or user-facing text"}
  babysit:        {fit: poor, note: "blocks on nonsense questions; Theo runs agents on crons just to catch it stuck"}
  orchestrate:    {fit: ok,   note: "manages many subagents well but sends their questions to the human and blocks; needs a watcher and a Claude-written final report"}

role_hints:
  as_primary: "Not a daily coding driver. Lead only for computer use, 3D visuals, or science work."
  as_subagent: "Top reviewer and finder of problems, computer-use operator, 3D asset builder and play tester, one voice on a design council."
  never_for: ["long unattended or compound goals", "reports the human reads directly", "frontend, UI, copy, or dialogue", "game feel and level design", "machines without disk and RAM limits", "fast mode", "max effort"]
---

## Summary

GPT-6.2 Astra is OpenAI's frontier model as of 2026-11-17. On benchmarks it
is excellent: first on Theo's own benches at about half of Fable 5.2's cost,
the best science model he has seen, still the best at computer use, and the
best reviewer on his evals. To work with it is another matter. On long runs
it blocks itself on questions the human can't answer, loops on one half of a
two-part goal, and writes reports nobody can parse. Theo "would not choose
this over Opus 55 for any of my work as a dev." Use it as a reviewer,
computer-use operator, 3D builder and play tester under a Claude lead, and
have Claude write anything a human will read.

## Strengths

- **Review.** "It's a great reviewer. It catches things other models miss."
  On all his evals "it had a pretty much perfect score... and never lying,"
  where "every other model has a habit of fibbing a bit, especially Fable."
  His evals measure finding things, which is why it tops them.
  ([AS62 35:11](https://youtu.be/9KvI-zg4mfo?t=2111);
  [AS62 35:34](https://youtu.be/9KvI-zg4mfo?t=2134))
- **Computer use.** "Absolutely cracked. It flies. It's really good at like
  knowing what's going to come next and batching a ton of things in one
  call." ([AS62 16:57](https://youtu.be/9KvI-zg4mfo?t=1017))
- **3D and graphics.** Fish slop is "one of the best looking things I've ever
  seen in my browser." It may be his play tester, with Fable implementing.
  ([AS62 19:33](https://youtu.be/9KvI-zg4mfo?t=1173);
  [AS62 32:18](https://youtu.be/9KvI-zg4mfo?t=1938))
- **Science, math, security.** Terminal Bench Science 9 points above GPT-6
  Astra at under a third of the cost; "likely that Astra is the best science
  model ever." Per friends at Vercel, the 6.2 models top every security bench
  they run (secondhand).
  ([AS62 13:42](https://youtu.be/9KvI-zg4mfo?t=822);
  [AS62 17:42](https://youtu.be/9KvI-zg4mfo?t=1062))
- **Explores options Claude won't.** A reverse-proxy design for T3 Code that
  could save $25K a month, where Opus "didn't have the balls to explore enough
  options." Not shipped yet. ([AS62 35:41](https://youtu.be/9KvI-zg4mfo?t=2141))
- **Better than GPT-6 Astra** on code quality, subagent prompts, and web
  design ("significantly better than anything we've seen OpenAI models make
  ever"). In slides it beat Fable 5.2 by leaving out filler subtitles.
  ([AS62 36:03](https://youtu.be/9KvI-zg4mfo?t=2163);
  [AS62 12:43](https://youtu.be/9KvI-zg4mfo?t=763);
  [AS62 16:38](https://youtu.be/9KvI-zg4mfo?t=998))
- **Cost per run.** About half of Fable 5.2's cost on Theo's benches; "agents
  last exam" 78.3 vs Fable 5.2's 72.8 at about 5% of the cost (OpenAI's chart).
  ([AS62 0:38](https://youtu.be/9KvI-zg4mfo?t=38);
  [AS62 13:09](https://youtu.be/9KvI-zg4mfo?t=789))

## Weaknesses and failure modes

- **No idea what the human knows.** On long tasks it asks the human about
  internal details only a subagent could know, then blocks. Two hours into
  `/goal make a new level for Outer Wilds` it stopped to ask him to "compare
  R24 reviewer write permissions for its clips to these random file paths."
  It happened in Codex as well as T3 Code. OpenAI's release system-prompt
  changes and Theo's own T3 Code changes reduced it; it "still happens." **An orchestrator must watch an unattended
  Astra run for a blocking question and answer or kill it.**
  ([AS62 36:36](https://youtu.be/9KvI-zg4mfo?t=2196);
  [AS62 36:55](https://youtu.be/9KvI-zg4mfo?t=2215);
  [AS62 37:20](https://youtu.be/9KvI-zg4mfo?t=2240))
- **Unreadable reports.** "The most [unparsable] outputs of any LLM I've used
  this year." "It misses the forest for the trees." Asked why one machine's
  worktrees were slow, it wrote four paragraphs on pnpm internals; Opus 5.5
  said the SSD was slow. After the release prompt changes the answer was
  "better, but still bad." "It seems like you can't prompt this out." Theo
  has "built the habit" of switching to Opus at the end of a long Astra run
  for the summary. **Never
  relay its report to a human or merge on its say-so without a Claude
  restatement.** ([AS62 37:51](https://youtu.be/9KvI-zg4mfo?t=2271);
  [AS62 38:13](https://youtu.be/9KvI-zg4mfo?t=2293);
  [AS62 38:43](https://youtu.be/9KvI-zg4mfo?t=2323))
- **Loops on compound goals.** "Make it smaller and faster": it fixated on
  size, made the compiler 56% slower, and landed nothing in 7 days. Told to
  do speed only: 4 more days, zero changes. Opus 5.5 then made it 50% faster
  in two days. "Not capable of patting its head and rubbing its tummy at the
  same time." ([AS62 40:28](https://youtu.be/9KvI-zg4mfo?t=2428);
  [AS62 41:05](https://youtu.be/9KvI-zg4mfo?t=2465);
  [AS62 41:18](https://youtu.be/9KvI-zg4mfo?t=2478))
- **Wrecks the machine.** "No respect for your computer or the resources on
  it": wasted RAM, broke permissions, filled a nearly empty 8 TB drive with
  "disposable garbage", refused to clean up, and left another box with 15 GB
  free and one idle core. ([AS62 8:10](https://youtu.be/9KvI-zg4mfo?t=490);
  [AS62 8:36](https://youtu.be/9KvI-zg4mfo?t=516))
- **Spiky, defaulting low.** "It almost feels like it defaults to bad with
  random spikes into good and sometimes even great." Two failed demos for
  every one that worked. ([AS62 43:09](https://youtu.be/9KvI-zg4mfo?t=2589))
- **Regression to the mean.** Theo and Ben independently asked for a new
  game level and both got a water-and-bells level named "Bellweather"; other
  people's prompts got a "Bellweather Station" spy game and a monster named
  Bellweather. Its Outer Wilds planet
  looked stunning and had "no real payoff whatsoever."
  ([AS62 33:13](https://youtu.be/9KvI-zg4mfo?t=1993);
  [AS62 26:43](https://youtu.be/9KvI-zg4mfo?t=1603))
- **Copy and dialogue.** Reads "like somebody who doesn't speak English."
  It failed to match a game's dialogue tone after repeated instructions.
  Someone Theo found on Twitter, who works on model personification, got it
  right in a day (whether he used a model isn't said). ([AS62 5:36](https://youtu.be/9KvI-zg4mfo?t=336);
  [AS62 28:09](https://youtu.be/9KvI-zg4mfo?t=1689))
- **UI-isms and game feel.** Unnecessary subtitles, UI that shifts when
  clicked, odd controls; cringey generated images on web pages.
  ([AS62 19:07](https://youtu.be/9KvI-zg4mfo?t=1147);
  [AS62 12:12](https://youtu.be/9KvI-zg4mfo?t=732))
- **No pixel-exact art.** It "doesn't have the capability to generate pixel
  art in exact specific resolutions without doing weird scaling."
  ([AS62 22:19](https://youtu.be/9KvI-zg4mfo?t=1339))
- **Harness dependence.** The release mitigations live in Codex's system
  prompt ("write the final answer fresh for the reader", "ask before
  destructive or irreversible actions"). A bare API call or another harness
  may not carry them. ([AS62 11:23](https://youtu.be/9KvI-zg4mfo?t=683))
- **Safety blocks.** OpenAI tightened restrictions; "a meaningful number of
  people" report blocks, though Theo hasn't hit one since release.
  ([AS62 18:12](https://youtu.be/9KvI-zg4mfo?t=1092))

## How to prompt it

- **Keep GPT-family prompting.** Simple, literal, task plus target plus done
  state; no Claude-style essays (see `gpt-6-astra.md § How to prompt it`,
  which still applies).
- **One goal per run.** Split compound goals and verify each separately:
  > "Goal: reduce compile time on the bench in `bench/`. Do not trade speed
  > for size. Done means the bench is faster and every test passes."
- **Tell it who the human is and what they know:**
  > "The person reading your messages has not seen your tool calls or your
  > subagents' work. Don't ask them about internal details. If you are
  > blocked, say what you need in one plain sentence, or make the call
  > yourself and note it in your final report."
- **Ask for the answer first:**
  > "Start your final message with the answer in one or two plain sentences.
  > Details after."
  Expect only partial success; have a Claude model restate the report.
- **Bound the machine.** Give it a scratch directory and a disk budget, and
  tell it to delete what it created before finishing. Check yourself.
- **Make "nothing found" valid, and ask it to mark what it couldn't confirm**
  on reviews.
- **For UI it must touch,** forbid filler copy and subtitles explicitly.

## Routing guidance

**Route here for:**

- Reviewing Claude-written code, as the problem-finder. A Claude model
  restates and filters the findings before anything changes.
- Computer use, especially hard or long flows.
- 3D visuals, assets, and play testing, with Claude doing game feel.
- Science, math and security reasoning.
- A second opinion on open design questions ("council" member).

**Do not route here for:**

- Daily implementation. Opus 5.5 is preferred even where its code is fine.
- Long unattended or compound goals, or babysitting.
- Any report a human reads directly.
- Frontend, copy, dialogue, level design, game feel, pixel art.
- Running on a machine without disk and RAM limits.

**Handoff patterns:**

- **Claude builds, Astra reviews, Claude restates.** Opus or Fable
  implements; Astra reviews; the Claude model summarises the findings and
  decides what to fix.
- **Astra runs, Opus summarises.** At the end of any long Astra run, hand the
  thread to Opus for "a readable summary of what it did."
- **Astra explores, Claude decides.** Use it for unusual options (the reverse
  proxy); a Claude model judges and implements.
- **Astra for assets, Claude for play.** OpenAI model for asset generation
  and 3D, Anthropic model "to actually make the game pleasant to play."
- **Watch unattended runs.** Theo runs agents on crons to catch it blocked on
  a nonsense question.

## Cost notes

- **API:** $8 in, $40 out, $0.40 cache read, $10 cache write (30 minutes) or
  $20 (12 hours). Above 272K input: $16 / $0.80 / $60.
- **Modes:** fast 2x; Ultrafast 3x through 2027-02-28, then 6x; Batch half
  ($4 / $0.20 / $20). Flex is not listed for 6.2 Astra.
- **Versus Fable 5.2:** same list price, twice the cache-read price, about
  half the cost on Theo's benches, probably from fewer tokens (OpenAI claims
  fewer output tokens; the video gives no breakdown).
- **Versus GPT-6 Astra:** 20% cheaper per token and 60% cheaper on cache
  reads. GPT-6 Astra is still listed at $10 / $1 / $50.
- **Runs that ship nothing are the cost.** The video gives no dollar figure
  for the 11 looping days, but a run that lands nothing is pure waste at any
  per-token price.
- **Subscriptions:** on a Codex plan the marginal cost is close to zero; see
  `gpt-6-astra.md § Cost notes` for the plan figures, which this video does
  not update.

## Evidence

- AS62: "Astra 6.2 Is Unusable", Theo (t3.gg), YouTube,
  https://youtu.be/9KvI-zg4mfo (filmed the night of the 2026-11-17 release,
  early access; digest in
  `research/gpt-releases.md` Video 3). Mostly Astra; he says he spent much
  less time with 6.2 Sol.
- OpenAI model pages for `gpt-6.2-astra`, the models catalog, the pricing
  page and the deprecations page, fetched 2026-11-19: API id, prices, context
  and output limits, effort levels, Codex default context, and that GPT-6
  Astra is not deprecated. OpenAI's launch post returned 403, so its benchmark
  tables are known only as the video reads them.
- Simon Willison, https://simonwillison.net/2026/Nov/17/gpt62-astra-and-sol/:
  agrees on price; found neither 6.2 model as good as Fable 5.2 on his coding
  test; notes complaints that its "communication style can be confusing."
- **Unverified:** which ChatGPT plans include it; availability in Cursor,
  OpenCode, OpenClaw and Hermes; OpenAI's default effort; the "agents last
  exam" dollar figures (captions say "$289", read as $2.89 from "5% of the
  cost" of $60).

### Score rationale

- **intelligence 9:** "clearly super smart", top of Theo's benches, "likely"
  the best science model, and "neck and neck with the best" at math. Docked from 10 because the axis means unsupervised,
  and unsupervised it blocks or loops.
- **taste 4:** OpenAI's best web design and code quality yet, and no filler
  subtitles in slides, but copy, dialogue, UI-isms and unreadable reports keep
  it at GPT-6 Astra's level.
- **floor 3:** "defaults to bad with random spikes into good"; two failures
  per success; wrecked machines.
- **thoroughness 10:** near-perfect on his review evals, "never lying."
- **cost_efficiency 7:** about half of Fable 5.2's cost per bench run and
  60% cheaper cache reads than GPT-6 Astra. Not higher: cache reads cost 4x
  Sol's, and looping runs ship nothing.
- **speed 4:** no new speed figures; computer use "flies", but long runs take
  days to get nowhere. Kept at GPT-6 Astra's 4.
- **computer_use 10:** still best anywhere.
- **orchestration 5:** manages many subagents well and writes good subagent
  prompts, but pushes their questions up to the human and blocks the run, so
  it needs a watcher: "heavy guardrails" on the rubric. Down from GPT-6
  Astra's 10.
