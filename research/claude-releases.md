# Claude 5.x Release Videos: Detailed Summaries

Source: three auto-generated YouTube transcripts (plain text) by the same speaker. He identifies himself as "Theo" in the Sonnet video and refers to his products T3 Code and Lakebed. Files:

- `scratchpad/txt/claude-fable-5-1.clean.txt`
- `scratchpad/txt/claude-opus-5-5.clean.txt`
- `scratchpad/txt/claude-sonnet-5-5.clean.txt`

## Transcription notes (read first)

The transcripts are speech-to-text and contain systematic mis-hearings. This document reads them as follows:

| Transcript text | Interpreted as |
|---|---|
| "cash", "cashed", "cash reads/rights" | cache, cached, cache reads/writes |
| "Soul", "5.6 soul", "GPT6 Soul" | OpenAI's "Sol" model. The Fable video says "5.6 soul" and the Opus/Sonnet videos say "GPT6 Soul". The exact version is ambiguous: it may be GPT-5.6 Sol in the Fable video and GPT-6/6.1 Sol later. |
| "Astra", "Aster", "Astro", "GBD6 Astra" | GPT-6 Astra (OpenAI) |
| "Luna" | an OpenAI cheap model released alongside GPT-6 Sol ("GPT6 Soul and Luna") |
| "Halo 5.1" (one occurrence), "Babel 5.1", "table 5.1", "Able 5" | Fable 5.1 / Fable 5 |
| "Sonet 55", "Opus 55", "Haiku 55" | Sonnet 5.5, Opus 5.5, Haiku 5.5 |
| "Gro/Grock/Rock 4.7" | Grok 4.7 (xAI) |
| "Gemini 38 Flash" | probably Gemini 3.8 Flash |
| "Cloud Code", "quad code", "CloudMD", "Claude MD" | Claude Code, CLAUDE.md |
| "X high", "XH high", "XI", "Xigh" | the `xhigh` effort level |
| "codeex" | Codex (OpenAI) |
| "Witchai" | a design-comparison site made by someone called "Dra" (name uncertain) |
| "fish slop" / "Fishlop 3D" | the speaker's personal game-generation test |
| "3JS" | three.js |

None of the videos mentions Haiku 4.5. The Opus 5.5 and Sonnet 5.5 videos say that **Haiku 5.5 is "coming in the next few weeks"** and is "built for high volume and cost-sensitive applications".

---

# Video 1: Claude Fable 5.1 (and Mythos 5.1)

## 1. Subject and overall thesis

This is a launch and review video for **Claude Fable 5.1 / Claude Mythos 5.1**. The speaker had used it heavily for about 24 hours before recording. He calls it "a meaningful jump from Fable 5" and a "fantastic update to what was my favorite model": "This is the first DOT update you've had in a while that is a universal easy to agree on huge win."

He also calls it "a bit confusing a release because in some ways it's more expensive, but in others it's cheaper. In some ways, it follows instructions better, in other ways, it does it worse. It benches higher for the most part with a couple strange exceptions."

His central claim is that 5.1 "changed the unit of work". He says it behaves like a maintainer that can audit, take over, correct and land several PRs in one session. He is not claiming a faster code generator. He quotes a GPT/Sol-written analysis of his PR data that he endorses:

> "Fable 5.1 changed the unit of work. It acted less like a fast code generator and more like a maintainer that could audit, take over, correct, and land several lines of work in one session... 5.1 did not win by being faster at the first response. It won today by carrying more work through the review and merge tail."

Context: his team landed "89 PRs in 24 hours" (later "90 PRs land in a 24-hour window") with this model. He explicitly wants to avoid repeating the mistake he made with Opus 5, which "seemed totally good... and it killed it in the benchmarks, but then when you actually started merging the code, it was nowhere near as nice to use."

**Fable vs Mythos.** "Fable and Mythos are the same model. The only difference is what happens when you send a request, not the actual weights underneath." Fable is generally available. Mythos is available only through trusted-access programs, with safeguards tuned for cybersecurity and life-sciences work. Fable has filters "in front of it preventing certain requests from going in and certain responses from coming out."

## 2. Strengths (with evidence)

**Agentic, long-running maintainer-style coding**
- He took over PRs that other agents had left stuck in loops: "a poll request that gets pretty far and then an agent pushes it up and all of a sudden it gets a bunch of responses from AI review agents and it gets stuck in this loop of fixing things constantly and then 30 commits later you have way more code than you intended and nothing actually ends up shipping. I had this model take a look at a bunch of those... pretty much all of them ended up landing." He attributes this to the model being "just barely better enough to push through that friction."
- Examples:
  - A T3 Code PR fixing how Claude Code skills are picked and managed. The `$` trigger for user-invocable skills was "finally fixed", even though "Anthropic's official SDK fights you every step along the way".
  - A streaming-projection / catch-up PR that had failed in more than 8 earlier attempts landed with "only like 450 lines of code".
  - It fixed "nastier issues" in the Grok integration that "other agents were missing".
- **Slop audit of Lakebed.** The model categorized the problems and proposed "nine PRs ordered so the deletions land first and each later PR is a smaller PR as a result." He then told it to spin up Fable 5.1 subagents, babysit the PRs through CI and review bots, and merge the simple wins. Result: "all 10 PRs are merged. Everyone went green on CI, code rabbit, cursor bugbot, and macroscope... with every bot thread answered or fixed before merge. Net across the batch was 340 files, and it deleted 13K lines net." He adds that this "seems to have actually improved how agents contribute to the codebase".
- **Quality audit.** It gave the codebase a "5.8 out of 10" with concrete suggestions. He then told it to "spin up Fable 5.1 sub agents to break up the work", which produced 7 parallel PRs. A *separate* agent monitored the repo's PRs and merged them or took them over. Some of the worst-case paths became "85 to 90% faster". "I shipped so much work in Lake the last few days, and I didn't even look at a line of it."
- **Codebase audit / V2 proposal.** It audited T3 Code and proposed "a V2. If we were to start from scratch, what would we do differently?" He said it had "great suggestions".
- **PR triage and merge judgment.** It found contributor PRs worth merging, vetted and tested them, and gave him "a good gut feel if they were ready to go or not". "I'm telling this model more often to merge the PR when it decides it's ready, and I've yet to be burned by that, despite it doing it dozens of times... 5.1 is picky enough about what it thinks is good enough that I trust it to do that."

**Real-world metrics.** The model compared its own first 24 hours against his *best* 24-hour windows with Fable 5 and with 5.6 Sol, across T3 Code and Lakebed:

| Metric | Fable 5.1 | Fable 5 | Sol |
|---|---|---|---|
| PRs in the window | 13, median 489 LOC | (fewer, smaller) | |
| Packages touched per PR | up to 4 ("would make the changes in all the places it mattered") | usually 1 | usually 1 |
| Files per PR (avg) | 11 | 4 | 4 |
| High-severity review-bot findings per 1K LOC | **0.4** | 2.06 | 1.02 |
| Commits pushed after PR opened | 24 | 60+ | n/a |
| PRs closed as slop or superseded | 0 | n/a | n/a |
| Time to merge | "up to 50 minutes" | 47 min | 30 min ("the whole loop was just closed more") |
| PR filed to merged, after clear implementation instructions | median 14m41s | | |

The merge-time row is ambiguous in the transcript. He says "up to 50 minutes... compared to 47 minutes with Able 5. Slightly faster", which is self-contradictory.

- He says it "writes way more code per minute" but takes longer to run. "Quality signal stayed strong when the PR size was going up."
- **Sol vs Fable 5.1 per the analysis:** Sol "could go deep but often turn into scope creep with a lot of PRs getting bigger and bigger that weren't really ready to go." Fable 5 "was faster to first draft at its peak and soul could solve hard mechanisms".

**Benchmarks cited from the official post**
- **Terminal Bench (Science, v0.1):** "performs almost twice as well at any given level", and is cheaper because of the cache-read cut.
- **Terminal Bench 4 (agentic terminal coding):**
  - Low: 40% vs 21.5% for Fable 5, at $5.70 vs $12.30.
  - Max: 55.8 vs 45.8, costing "under $20 instead of over 26".
  - Mythos scores above Fable here because "Fable 5.1 flags a handful of things in terminal bench 4, which results in it falling back to Opus, which hurts its scores."
- **Humanity's Last Exam:** better and slightly cheaper, but "I do see it stalling out a bit after high... It doesn't seem to benefit as much going beyond high."
- **Cursor Bench:** about 73% vs just over 70 for Fable 5's peak. The most expensive run fell to $9.64 per task from $17.32. "It is kind of crazy that on low it's still more expensive than high with Soul, but it also is performing better... Fable 5.1 on low does seem like a very compelling option for a lot of work."
- **Artificial Analysis (AA) Intelligence Index:** "scored higher than they've ever measured before", ahead of Opus 5, Fable 5, 5.6 Sol and Grok 4.6. About 4% of output tokens in the run were served by an Opus 5 fallback.
- **AA intelligence vs output tokens:** "every model variant scoring higher than 5.6 soul medium on the intelligence index is matched or beaten by a fable 5.1 effort level on both intelligence and token usage." He stresses this is output tokens, not cost.
- **AA Omniscience (hallucination bench):** "Anthropic has everything above" Sol, which is in the 60% range. His interpretation: "Anthropic really wants the model to always be accurate when it gives information. OpenAI wants the model to be able to find and create new information a little more readily."

**Science (Mythos 5.1)**
- Protein binder design (adaptive bio design competition): hit rate "10 times higher than the best design submissions" on 3 targets, and "nearly 50% across 12 targets" against a typical 10 to 15%.
- A Venus map built from 30-year-old NASA radar data, more accurate than existing maps, released under Creative Commons.
- A GPU kernel that speeds up open-source computational-biology deep-learning models "by up to 2.5x with the same quality of output".

**Front-end / UI design**
- He calls it "a generational leap in homepage design at the absolute least". Animations were "really good... tasteful", for example cards flying in and transit lines animating.
- **Skill dependence:** designs with Anthropic's front-end design skill were much better. "When I switch off of the design skill, it's so much uglier." Designs with "the taste skill were all pretty bad and boring." Before this release he had "pretty much entirely stopped using" the design skill because it "hurt as much as it helped", but "I guess that design skill is really back."
- He admits: "I have not had a chance to really push it for front-end work yet myself."

**Games, 3D and tool use**
- The fish-slop 2D rebuild had excellent animation easing, sound design and polish.
- For the 3D version he "told it to use Blender and it did". The results were "way better than I've seen from existing models", with biologically plausible fish. Controls were mis-mapped, but the movement feel was "the most workable starting point I've seen so far".
- He credits much of this to "improvements they made to how well the model can use tools like Blender". He cites Alex from Anthropic's demo, in which the model designed a house for a plot of land, rendered it, and produced a cinematic walkthrough.

**Writing quality**
- The release "addressed a lot of the feedback on the Fable and Opus slop of just like weird technical jargon being spit out constantly, and it's much more readable."
- The prompt guide says it has "fewer stock phrases and less unexplained jargon".

## 3. Weaknesses, pitfalls and misconceptions

- **Misconception:** Fable and Mythos are not different models (see section 1).
- **Safeguard fallback to Opus.** Flagged requests fall back to Opus, which lowers scores on some benches: Terminal Bench 4, and about 4% of output tokens on AA. Personally he hit a safeguard flag only once despite "drain[ing] the majority of the limit in most of my five accounts in just 24 hours". Anthropic claims a 60% reduction in false positives.
- **Token-hungry and verbose.** "This model yaps a bit more." AA measured 1.7x the output tokens of Fable 5. Max cost $3.76 per index task, "20% more than Fable 5". In another passage he quotes "$3.69 per task versus $3.14 for Fable 5 versus 95 for 5.6 soul on max"; the numbers in the transcript are inconsistent. He says it is "still nowhere near the levels of token efficiency that we would expect from OpenAI": "even normal high is further than max is with soul and medium is further than X high is with Soul." Advice: "I wouldn't use this model for really long oneshot tasks that could be done by other things." The savings come from agentic, cache-heavy work.
- **Physics reasoning:** Sol still leads. "Even 5.5 Pro is tied with Fable 5.1."
- **Low hallucination comes at the cost of experimentation.** Anthropic's anti-hallucination focus "seems to result in the model being less able to experiment and try things that aren't in its weights."
- **Computer use:** "I'm just generally not that impressed with computer use with Claude models. It's nowhere near as far along as OpenAI stuff is there."
- **Intent misread (his only real failure example).** On `high` effort, running for 8 minutes, it audited PR auto-linking and reported "nothing links a PR to a thread automatically", which was wrong. It had treated the branch lookup as something other than auto-linking. "It just didn't get my intent here." He calls it "pretty much the only one I have."
- **Low effort misses hidden complexity.** "If you have a task that you think is simple, but there's some tiny piece you forgot about that makes it complex, low will miss that."
- **Behavioral quirks from the official prompt guide:**
  - It gives fewer user-facing progress updates during long tool-call turns. One run of his lasted 24m28s with over 60 tool calls, including a stretch of more than 30 with no text output.
  - Prose can be denser than Fable 5's: longer sentences and fewer paragraph breaks.
  - In summaries it may reproduce source passages without marking them as quotations.
  - It sometimes stops to ask permission ("shall I apply this?") instead of finishing.
  - Scope overreach: it "sometimes will try to fix nearby code, extend behavior that the task didn't mention, or commit more test files than the change actually warrants."
- **Append-only history (API).** New accounts can no longer edit prior turns. Editing earlier context now "breaks the thread entirely and will kill all of the reasoning data". This is an anti-distillation measure. It is rolling out gradually and "in the future it will apply to all accounts". He notes it hurts products with branching features (he names "the PI team").
- **Data retention.** Fable and Mythos have no zero data retention (ZDR); Anthropic must store requests and responses. Many enterprises therefore cannot use them and use Opus or OpenAI instead. The new "Enterprise Frontier Safeguards" is a provisioned box that customers run on their own infrastructure (AWS etc.) to perform Anthropic's checks. He expects it to be expensive.
- **Watermarks.** These are added for EU AI Act compliance, and an API to detect Claude-generated text is coming.

## 4. Pricing, speed, context and limits

- **Price:** "$10 per million input tokens and $50 per million output tokens" (unchanged). **Cache reads are $0.25/M, down from $1, a 75% cut.**
  - The Sonnet video later describes this as a "90%" drop, which contradicts the 75% figure here. The figures ($1 to $0.25) support 75%.
- **Official claims:** about 25% less than Fable 5 for typical token-billed workloads, and "up to 45%" for highly agentic work.
- **Why caching matters.** Every tool call stops and restarts generation, so the whole history is re-read each time. His own Claude Code usage over the period:
  - 42.8B cached input tokens vs 710M uncached.
  - About $15K at API prices, about $25K total. Without caching it would have cost "135,000 additional dollars".
- **His Fable 5.1 spend breakdown** (about $2,000): cache writes about $1,200 (nearly 60%), outputs about $500, cache reads $264, uncached input $4. "Writing to cache costs money... I hope that in the future there are better ways."
- **Cache TTL:** "These caches only live for 5 minutes by default. Longer times is way more expensive." For single-shot chat with one or two tool calls, the cache discount matters much less.
- **Subscriptions:** "One of those $200 a month subs from Claude Code can get you up to $8,000 a month of usage." He has five accounts and drained most of their limits in 24 hours. "This model is definitely going to burn through your limits faster, not because it's less efficient, but because you're going to have it do more and let it go further."
- **Effort levels:** low, medium, high (default), xhigh, max.
- **Speed:** he gave no TPS figure. The model takes longer per PR but writes more code per minute.
- **Context window:** not stated in this video. Compaction steering is discussed (section 5).

## 5. Recommended prompting style and workflow

From the official Fable 5.1 prompt-engineering guide (which he endorses) and his own practice:

- **Prune CLAUDE.md.** "This is definitely one of those model releases where you should go look at your Claude MD and see what is deletable. Try deleting everything, see how it behaves, and then add parts back as it makes sense to."
- **Effort.** Start at the default, `high`, then test other levels against your own evals. "High is a great default. Low is surprisingly capable and worth trying out." Going beyond `high` brings diminishing returns.
- **Progress updates.** Ask for them explicitly if you want them. Remove old anti-chatter lines such as "hold all findings for the final response", because they may now suppress output you want. Official example: *"Before you start, say in a line what you're about to do. Brief updates while you work help the user follow along. Close with a short recap that stands on its own."*
- **Writing density.** Use the anti-"mannered prose" instruction. Paraphrased from the guide: metaphors "drag connotations the writer did not choose and cannot control. The fix is to say what you mean... when a literal phrase is available, use it." Short version: "Please remove all mannered prose." He found that his own "unslop" skill plus 5.1's defaults were already readable without tuning.
- **Formatting.** 5.1 uses bold and bullets less. If CLAUDE.md contains old anti-formatting rules, "it's basically never going to do it", so remove them if you want some formatting.
- **Quotations.** Give a complete example of a correct response in the system prompt to stop unmarked reproduction of source text.
- **Autonomy / finishing.** Set a clear end point. Official system-prompt text:
  > "You are operating autonomously. The user is not watching in real time and cannot answer questions mid task. So asking 'want me to' or 'shall I' will block the work. Reversible actions that follow from the original request proceed without asking. Stop only for destructive actions or genuine scope changes the user must decide on."
- **Compaction steering.** Tell the model what to preserve in compaction summaries, either in user prompts ("these things are important, make sure you don't forget them") or in the system prompt. This is useful for client-side compaction.
- **Scope control.** "It responds well to explicit instructions about what to leave out", for example limiting how many test files to add.
- **Append-only histories** when you build on the API.
- **His delegation prompt (verbatim, lightly cleaned):**
  > "I trust your judgment here. These all seem like real things worth cleaning up. Spin up some sub agents using Fable 5.1 and get all this work up. When you file PRs, make sure to babysit them until they pass all the different checks and review agents that come in to leave their thoughts. Let me know when all the PRs are in a good state. Any of them are simple wins. Just merge them. I trust your judgment."
  This was safe for him because the project "doesn't auto ship to prod".
- **"Takeover" skill.** Instead of copying review feedback between agents, hand the PR to a new agent: "Hey, here's a PR. Get the branch on your work tree and it's yours. Push it, maintain it, manage it so that it actually lands." You can optionally ask the original agent afterwards how it feels about the changes.

## 6. Subagents, orchestration, delegation and verification

- Fable 5.1 as orchestrator: "if you let it spin up all the sub agents that it can now orchestrate better because it prompts itself better too. It's going to burn more because it's just doing more."
- Pattern 1: audit, then a written plan ("proposed order of work", deletions first so that later PRs are smaller), then human approval, then parallel Fable 5.1 subagents each owning a PR, then babysitting CI and review bots (CodeRabbit, Cursor Bugbot, Macroscope), then merge.
- Pattern 2: a separate "merge monitor" agent watches all PRs on the repo, merges those that are ready, and "take[s] over if they weren't progressing fast enough".
- Verification is delegated to CI plus third-party AI review bots. The model must answer or fix every bot thread before merge.
- His trust ladder: tab completion, then pointing agents at files, then reviewing only PRs, then models summarizing and reviewing PRs, then models choosing which PRs to merge, and now "I tell it to find them, fix them, and merge them for me", especially "bug fixes and performance improvements". Product-opinion changes stay with the human.
- Model comparison: Sol is faster to close the merge loop (30 min) but prone to scope creep. Fable 5 was faster to first draft. Fable 5.1 carries the work through review and merge.
- He used Sol (or another GPT model; the transcript implies Sol) to analyze and compare model performance from PR history.

## 7. Claude Code specifics

- CLAUDE.md: prune it, and remove anti-update and anti-formatting rules (section 5).
- Skills: Anthropic's official front-end design skill markedly improves 5.1's designs; the "taste skill" does not. He uses his own "unslop" skill and his own "takeover" skill.
- He fixed `$`-invoked user-invocable skills in T3 Code's Claude Code integration. The Claude Agent SDK "fights you every step along the way".
- Subscription economics: $200/month gives up to about $8K/month of API-equivalent usage.
- He did not discuss hooks, MCP or plugins.

## 8. Routing-table implications (Fable 5.1)

- **Route to Fable 5.1:** long-horizon, multi-package agentic coding that must survive review and land. This includes taking over stuck or looping PRs and cross-cutting changes (11 files and 4 packages per PR on average) with low high-severity defect rates.
- **Route to Fable 5.1 as orchestrator** for large cleanups and audits that decompose into parallel PRs. It plans well (ordered PRs, deletions first) and prompts its own subagents well.
- **Route to Fable 5.1:** PR triage, vetting and merge decisions for bug fixes and performance work, where its pickiness is an asset.
- **Route to Fable 5.1 (with the design skill loaded):** front-end, marketing-page and animation-heavy design work, and 3D or Blender-assisted creative builds.
- **Default effort `high`.** Try `low` for routine tasks, where it is "surprisingly capable", but not where hidden complexity is likely. Avoid going beyond `high` without evidence, because returns diminish.
- **Do not route to Fable 5.1:** long one-shot, non-agentic generation that another model could do. Its cost advantage comes from cache reads in agentic loops, and it is verbose (1.7x output tokens).
- **Do not route to Fable 5.1:** computer-use tasks (OpenAI models are better) or physics-heavy reasoning (Sol leads).
- **Do not route to Fable/Mythos:** workloads needing ZDR or strict data retention. Use Opus instead, unless Enterprise Frontier Safeguards is in place. Expect occasional safeguard fallbacks to Opus on security- or bio-adjacent tasks.
- **Prompting rules for this model:** state an explicit end condition and the autonomy policy, ask for progress updates if a human is watching, state what is out of scope (no nearby fixes, limited test files), and keep histories append-only.
- **Ambiguous intent:** its rare failures are definitional misreads of intent. For audit-style questions, define terms precisely in the prompt.

---

# Video 2: Claude Opus 5.5

## 1. Subject and overall thesis

This is a day-one review of **Claude Opus 5.5**. The speaker, burned by Opus 5 ("the model felt more like a liability than an actual thing you could rely on"), finds 5.5 "blowing me away": "They made it cheaper. They made it less bad at writing. They made it way better at code and following instructions." He is not yet sure it is a "Fable killer". Anthropic's headline: "It performs at the level of Fable 5.1 on most work and it costs 40% less to run than Opus 5."

His bottom line: "I think Opus is probably the right default for the vast majority of stuff. But you should not be as scared to reach to Fable for front end still." He also warns: "this model is smaller. It is dumber. It will make mistakes. So will Fable, just less so."

Context: four major model drops landed within two days (Grok 4.7, Opus 5.5, GPT-6 Sol and Luna). This was "the first release since they called for pacing the frontier."

## 2. Strengths (with evidence)

- **Anthropic claims:**
  - A tester "completed a 680,000 line of code migration in less than a day".
  - Strong at fixing inefficiencies in software. He agrees, having thrown it at "pretty brutal" performance optimizations.
- **Benchmarks:**
  - It wins almost all of Anthropic's charts. The exceptions are Terminal Bench Science (agentic scientific research) and Automation Bench (business workflows).
  - **Terminal Bench 4:** "Opus 5.5 Medium is scoring higher than Fable did on max", at **$2.94 vs $20** for Fable 5.1 max. There is "a slight dip on max."
  - **Frontier Code:** new all-time highs at medium and at max. Its best score came at medium. He calls the bench "weird".
  - **Cursor Bench:** medium beats Fable 5.1 max. Astra is no longer included because "OpenAI has banned Cursor from using their models."
  - **AA Intelligence Index:** "a massive lead", a 5-point jump over Fable 5.1. He thinks this "more so showcases how bad these benchmarks are."
  - **AA at high:** Opus 5.5 scores 53 vs 50.9 for GPT-6 Astra on high, at a higher cost.
  - **AA Pareto frontier:** "Opus 5.5 has swept this line. It is the best price for all of these scores in the 50 plus range." Edwin (quoted) says medium is "Fable 5.1 level intelligence"; the speaker thinks "that's a bit of a reach". Medium costs $1.34 per task vs "6 plus for Fable".
  - **Knowledge work** (Excel etc.): improved. He doesn't personally care about it.
- **Communication and writing:** "my favorite change by far." It "puts the most important information up front". A tester said "It writes the way I do." Example from the post: Opus 5 produced jargon-laden, em-dash-heavy text, while Opus 5.5 gave a clear dollar-attributed explanation of a billing bug with before and after. He **deleted his "unslop" instructions from CLAUDE.md** and doesn't plan to add them back.
- **Real day-one work:**
  - Built an improved Artificial Analysis visualizer, scraping the data from AA's homepage. It "was actually very pleasant to do this type of thing with". He ported the visualizer several times and used computer use to verify it.
  - An autonomous bug fix: "go through my computer, find the repo, and make a PR". It found the repo, noticed the local clone was stale, updated it, made a worktree, filed the PR, verified the fix, and got it merged. "All of this combined was 1% of my weekly."
- **3D and games:**
  - Fish-slop 3D ran at 120 FPS at default `medium`. He then had it "refine and make it as visually appealing as possible" at `xhigh`. Results included a rigged stingray and a working gameplay loop: "the first version of Fishlop 3D I've had any model generate where I had to like remind myself it's just a demo."
  - Community demos: a Dark Souls clone, a flight sim, and a Tony Hawk-style skater in C++ with no engine.
  - It "seems much better at things like 3JS than native tech". It is "surprisingly capable of using computer use to identify these things [visual flicker] and fix them, but not always."
- **Code-review / deep-audit bench (his own):** Opus 5.5 nearly doubled Opus 5's "accuracy and reliability of its findings". It still trails Grok 4.7 and Sol on this task (section 3).
- **PR quality (about 5 PRs, so limited data):** "similar to lower rates of egregious high severity issues... with a similar to slightly higher number of small issues and nitpicks compared to... Fable 5.1." His gut feel: "very similar to Fable 5.1's performance here with slightly higher overall quality, especially if you care about the quality of the prose... but it spikes down definitely go a little lower than fables do too."
- **HTML generation:** Mia ran 100 HTML page generations and said it "is the best model that she's ever tested". The speaker partially disagrees (section 3).

## 3. Weaknesses, pitfalls and misconceptions

- **Not more token-efficient; actually less.**
  - "This model is cheaper, but it's not because it's more efficient. In fact, this model is meaningfully less efficient than Opus 5."
  - AA max tokens per task: Opus 5 73K, Fable 78K, **Opus 5.5 about 120K**, GPT-6 Astra 27K. "There is really a 4x gap in efficiency."
  - AA max cost per run: Opus 5 $5.86, Opus 5.5 "almost six bucks", Fable $7.63. "Opus 5.5 comes close to being the most expensive model that artificial analysis has run simply because of how many tokens it is using." AA notes it would have been 80% more expensive without the price and cache cuts.
- **Effort-level hazards: avoid `low` and `max`.**
  - "Low is really bad... I think low is pretty stupid. It's just not that capable considering the price."
  - "It feels like low and max are dangerous and generally best avoided, but medium, high, XH high, those all have seemed really good."
  - Max loops: "I had a thread go for 6 hours and 30 minutes writing a markdown plan because I had it on max and it just ran in loops forever." He stopped it, switched to xhigh and asked for an update; it was about halfway done.
  - Skatebench: xhigh used about 330 reasoning tokens per question; max used almost 5,000 ("over a 10x gap") for about a 1% score bump. It also "scored worse than Opus 5 did on Skatebench".
  - "Don't use Max on this model. It's not worth it unless you just want to watch tokens burn."
- **Thorough code review and sweeping audits are weaker than OpenAI's.** On his bench for diving into big codebases and suggesting real quality improvements, Grok 4.7 (likely helped by Cursor/Bugbot review data) and Sol do better: "Opus and Fable less." "If you're planning on using this model to very thoroughly review code and find every single thing wrong with it or suggest sweeping improvements to your codebase, might not be as strong at those things as OpenAI's Frontier is." He notes this is an occasional task for him, "once every two or so weeks".
- **Thoroughness ranking:** "Fable is still slightly more thorough. Astra is still the most thorough, but it's also very spiky and weird."
- **Front-end design is weaker than Fable 5.1.**
  - Demos are "not sloppy, but okay. Yeah, they're a little sloppy." "Half of them are Tailwind templates, the other half are this very specific... color pastel with the big shadows."
  - With the official Claude Code design skill it does about the same as without it ("a little bit better [without], but not a lot better").
  - "Fable still is the GOAT for a handful of things." Mia's 100-generation result is a dissenting data point.
- **Context-window paranoia.** "One of the most frustrating ones for me." While monitoring another Opus 5.5 instance, it reported that "its context is 10% from autocompact... if it crashed that work would be lost". He calls this nonsense: "None of this is stuff the model should think about or care about." He attributes it to older training where running out of context meant failure. "OpenAI has entirely beat this out of the models... They will trust compaction." Anthropic "relied more on that million token context window where OpenAI caps it to 272K."
- **Dumb spikes and "small model feel".** "It still does give you that small model feel and smell when you hit these edges because I would not expect Fable to say something nonsense like this. Astra perhaps, but not Fable." Its discernment weakens when things are already in a bad state, for example when auditing why a job is slow.
- **Long jobs raise failure risk.** "As we're doing longer and longer jobs with more and more work, the likelihood you hit one of those failures goes up, not down." The model may "get stuck repairing things it doesn't need to when you send it off on some performance work."
- **Slow to commit.** A performance run had "almost three hours" of changes still local and uncommitted.
- Visual bugs persist in 3D (lighting blend, transparency).

## 4. Pricing, speed, context and limits

- **Price:** "$4 per mill in and $20 per mill out" (20% less than Opus 5). **Cache reads $0.20/M**, which is "60% cheaper". Cache writes are $5/M (from the Sonnet video).
- **Cost vs Opus 5:** 40% less on typical workloads at default settings.
- **AA cost per task by effort:**
  - Medium about **$1.34** vs $3.26 for Astra (max) and about $6 for Opus 5.5 max.
  - High is "about half the price of Astra on Max".
  - Xhigh is "a lot closer to Astra's costs".
- **Speed:** "about 30% faster" than Opus 5. The Sonnet video adds about 70 TPS via OpenRouter (Anthropic) and about 100 TPS in his subscription use.
- **Context:** Anthropic leans on a 1M-token context window (vs OpenAI's usual 272K cap). Compaction is "way faster" now and "handles compaction" well.
- **Cache-friendly effort switching:** "Now you can change reasoning levels midsession without busting cash." Previously the effort level sat in the system prompt and invalidated the cache.
- **Default effort appears to be `medium`.** "I was running on medium reasoning... this is the default reasoning level for the model."
- **Usage limits:** a full day of heavy use cost about 20% of one account's weekly limit. The autonomous bug-fix PR cost 1% of weekly. Anthropic "bump[ed] the five hour limit", which he "haven't come close to hitting". "The amount of value you get out of your $200 sub in Claude, it is running laps around our friends at OpenAI", at least for subscriptions, "maybe not in the pure API prices".
- **ZDR:** zero data retention can be applied to Opus but not to Fable/Mythos. "This model is almost immediately going to become the most popular for coding with AI by far just from this one particular detail."
- Sonnet 5.5 and Haiku 5.5 were announced as "coming weeks". Haiku 5.5 would be "our first Haiku release in a year".

## 5. Recommended prompting style and workflow

- **Use `medium`, `high` or `xhigh`. Never `low` or `max`.** Medium is the cost-efficiency sweet spot. Raise to xhigh for quality refinement passes; the fish-slop "make it as visually appealing as possible" pass used xhigh.
- **A medium-to-xhigh refinement loop:** draft at the default, then a polish pass at higher effort.
- **Drop anti-slop instructions.** "I actually took the time to go delete my unslop stuff from my agents in CloudMD... I don't think I'm going to bother readding it."
- **Effort can be changed mid-session** without losing the cache. Escalate or de-escalate effort within a thread rather than starting over.
- **For a run that seems stuck on max:** stop it, switch to xhigh, and ask for a status update.
- **For performance work and long jobs:** watch for unnecessary repair loops and context-anxiety; it may help to tell it explicitly to commit frequently. That last point is an inference from his "slow to commit" complaint, not a stated tip.
- **For front end:** steer it with explicit design direction, or use Fable. (The Sonnet video says Opus is "relatively steerable towards good designs and it follows instructions around design much better.")

## 6. Subagents, orchestration, delegation and verification

- Cross-machine orchestration: "I had this Claude Code on my machine SSH into another machine to trigger Claude Code, which it was able to do." He then used it to monitor that remote instance's progress, which is where the context-anxiety report came from.
- Self-verification: it verified the visualizer and visual fixes with computer use, and verified its own PR fix before merge.
- Model choice:
  - Opus is the default for most work.
  - Fable for front end, marketing pages, big design overhauls, and when thoroughness matters.
  - Astra (or Grok/Sol) for exhaustive code review and sweeping-improvement audits.
  - Fable is less likely to produce "nonsense" in degraded states.
- The Sonnet video adds that his Opus fish-slop run "did actually use a Fable 5.1 sub agent at some point", so Opus will spawn Fable subagents if allowed, which affects cost.

## 7. Claude Code specifics

- CLAUDE.md: he removed his "unslop" instructions.
- The official Claude Code design skill gave Opus 5.5 only marginal gains.
- Effort switching mid-session no longer busts the cache, because the effort level moved out of the cached system-prompt prefix.
- Claude Code desktop app usage was mentioned.
- Claude Code can SSH and remotely launch Claude Code on another machine.
- Auto-compaction exists and works, but the model is anxious about it.
- He did not discuss hooks, MCP or plugins.

## 8. Routing-table implications (Opus 5.5)

- **Default workhorse.** Route most day-to-day coding, bug fixing, feature work, migrations and performance optimization to Opus 5.5 at `medium`/`high`. On many coding benches medium matches or beats Fable 5.1 max at a fraction of the cost.
- **Enterprise / ZDR-constrained workloads** must route to Opus, not Fable or Mythos.
- **Effort policy:** default `medium`; `high` for normal complex work; `xhigh` for refinement or quality passes. **Never `low`** (poor value) and **never `max`** (over 10x tokens, loops, 6.5-hour runaway plan).
- **User-facing writing, explanations and status reports** go to Opus 5.5. Its communication is clear, leads with the most important information, and needs no anti-slop prompting.
- **3D, three.js and web-game builds:** strong, especially in the browser.
- **Do not route** exhaustive code review, "find everything wrong" audits or sweeping architecture critiques to Opus. Prefer Astra, Sol or Grok 4.7 for those, or Sonnet 5.5 for cheap deep-dive analysis (see Video 3).
- **Do not route** high-taste front-end or marketing-page design to Opus when Fable is available.
- **For very long or degraded-state jobs** (multi-hour performance work, auditing why something is stuck), consider Fable or add guardrails. Opus has dumb spikes, context-window paranoia and unnecessary repair loops, and failure probability rises with job length.
- **Cost control:** watch whether Opus spawns Fable subagents, which inflates cost. Constrain the subagent model explicitly in the routing config.
- Prefer a subscription over API billing for Opus-heavy usage. The value is driven by subscription limits rather than per-token price, because Opus 5.5 is token-hungry (about 120K tokens per AA task at max vs 27K for Astra).

---

# Video 3: Claude Sonnet 5.5

## 1. Subject and overall thesis

This is a review of **Claude Sonnet 5.5**, "the second model in the 5.5 family". On the numbers alone it disappoints: on the AA Intelligence Index it "comes out as more expensive and dumber than Opus 5.5 at every single level". The speaker nonetheless calls it "an incredible model", but only as a **tool that other models call**, not one a human should select:

> "If you are presented options inside of Claude Code between Fable, Opus, and Sonnet, I really don't think many people should be picking Sonnet."

> "Its strengths come as a tool for our other models to use. We shouldn't be calling Sonnet directly. It should be used as one of many things that Opus or Fable will orchestrate when it's trying to break up real complex work."

> "This model is useful as long as you're not the one sending it prompts."

He also says: "I haven't chosen Fable for any tasks for over a week now", because Opus 5.5 has taken over his workflows. He sees the release as "strategically targeted to screw over OpenAI", specifically GPT-6 Sol, which he considers "kind of just DOA".

## 2. Strengths (with evidence)

- **Anthropic positioning:**
  - "Opus is built for complex work requiring careful judgment. Sonnet 5.5 is strongest at well scoped everyday tasks."
  - Also "good for fixing bugs and creating polished documents, slides, and spreadsheets".
  - Claimed "sharp eye for design". He disputes this (section 3).
- **Benchmarks:**
  - **Terminal Bench 4:** 70.6%, up from 10.3% for Sonnet 5 ("seven times better"). This is the highest score to date on that bench, which makes him "skeptical of terminal bench". Notably, Sonnet max outperformed Opus max there, but Sonnet max is also more expensive than Opus max.
  - **GDPval:** slightly below Opus 5.5.
  - Strong on "long horizon work and image understanding". It is the first Sonnet to beat Pokémon Red working only from screenshots.
  - **OS World computer use:** much better than before, "neck and neck with Opus 5.5". He still uses Astra "almost exclusively for computer use".
  - **Frontier Code:** xhigh scored *higher* than max. Max put it below Sol, xhigh above Sol.
  - **Cursor Bench:** Sonnet on high "does complement the Opus 5.5 curve relatively well".
- **Feel:** "Now these just feel like slightly dumber, way faster versions of Fable." He speculates that Anthropic has improved at distilling its own models: "It really feels like they saw everybody else distilling anthropic models, got jealous, and decided to do it themselves."
- **Writing and collaboration:** it "writes way more clearly than their previous generation"; Anthropic has removed the "clawisms" (Claude-isms).
- **Deep-dive codebase analysis (key strength).** On his "big deep audit" bench, the models had to analyze T3 Code's huge "orchestrator v2" PR (hundreds of thousands of LOC) and propose a strategy for landing it in pieces. Results were scored by "my automated judging panel":
  - Astra was "by far the best plan" and is "uniquely willing to dig into the details".
  - Opus ranks below Astra. Fable rose after a judging overhaul but is still below Opus.
  - **Sonnet scored slightly better than Opus at about half the price, in about 5 minutes.** Opus took "almost twice as long" and Astra "almost three times as long". Sol was faster "but at like half the score".
  - "The cost per point here is insane. It is like the best value I've seen in this bench by far."
  - He frames this as "not traditional code work... much more analytical... trying to make good architectural decisions and comprehend what's going on in a codebase."
- **Context and intent tracking.** In the wrong T3 Code thread he asked "should have lots of legacy stuff cleared out". It answered in the frame of that thread (numbers) rather than guessing. "It was able to make what I would consider a pretty logical decision based on what the contents of the thread are... I was about to crash out about it not understanding my intent but it totally does."
- **Fish-slop 3D game:** "One of the best I've ever seen... in some ways it is better than the Opus one and in all ways it is better than everything I've gotten out of Astra." It had good Blender-made models, 120 FPS, and the "best looking" alien. It took about 40 minutes; at API prices it would have cost about $16.
- **Speed (raw):** OpenRouter shows about 94 TPS via Anthropic, vs about 70 for Opus 5.5 and about 30 for Astra. In his subscription use he saw about 150 TPS for Sonnet vs about 100 for Opus.
- He "would take Sonnet over Astra for my day-to-day code work" because Sonnet "does have fewer dumb spikes", but "I would just use Opus."

## 3. Weaknesses, pitfalls and misconceptions

- **Misconception: Sonnet is cheaper than Opus in practice.** It usually isn't for agentic coding.
  - The cache-read price **was not cut**: $0.20/M, the same as Opus 5.5. Input, output and cache-write prices are half of Opus's, but cache reads cost the same.
  - In agentic work cache reads dominate the bill. Uncached input is "barely touched" and output is "a very small portion". So the cache-read share of cost "rounds out to under 5% with fable... closer to 20% with Opus and... like 50 plus with Sonnet."
  - "I've looked at the numbers for doing like-for-like work with opus versus sonnet for real code tasks and sonnet consistently comes out as if not more expensive than opus does."
  - On AA, "Sonnet 5.5 cost roughly the same as Fable 5.1", "neck and neck with Fable 5.1 for the most expensive run they've ever done", though mostly because of `max`.
  - In fish slop, Sonnet used more than 3.5x the input tokens of Opus at similar total cost. The Opus run was contaminated by an accidental Fable subagent, so Opus "would have even been cheaper".
- **Not token-efficient.** On Cursor Bench it used 271,920 tokens per task, the most ever recorded, vs Opus 218K and Gemini 3.8 Flash 162K. That is "more than 5x the number of tokens that GPT 5.6 Sol and also 6 Astra used."
- **Faster TPS but slower wall-clock.** Fish slop took 43 min on Sonnet vs 36 min on Opus. Time spent generating was 39 vs 27 min. "It's faster, but actually slower because of the token differences."
- **Weak front-end design.** Examples were "a bit opinionated", "rough", "hideous", "boring", with "awful" animations and scroll bugs. It is worse than Opus and "significantly worse" than Fable. "Not the model I'd reach to for front end", especially since like-for-like Opus costs about the same.
- **Medium is weaker on Sonnet than on Opus.** "Medium is a lot stronger with Opus than it is with Sonnet." Frontier Code shows "pretty big drops" at medium and low.
- **Effort-level warnings, which apply to all Anthropic models:**
  - **Max:** "Don't use it... Pretend it doesn't exist."
  - His explanation: effort levels are budgets, i.e. ceilings, but max effectively raises the *floor*: "It's effectively telling the model it's not done until it does a certain number of reasoning tokens."
  - He has seen benches where going from low to xhigh added about 5 to 8% tokens, and going from xhigh to max added "a 1,500% increase".
  - Max "can often actually hurt performance because... it's going to start second guessing itself."
  - **Low:** "I don't think you should use any anthropic model on low right now." Anthropic removed the no-reasoning (instant) option on Opus, and presumably on Sonnet, "because these models suck without reasoning".
  - "Generally avoid low, avoid max. And for the most part, medium's fine-ish."
- Anthropic's charts show score vs cost but never score vs tokens; he implies this is deliberate.
- Anthropic's "30% faster / up to 30% cheaper" claims vs Sonnet 5 are "intentionally dancing around" max-effort and cache-read realities.

## 4. Pricing, speed, context and limits

- **Price:** $2/M input, $10/M output (same as Sonnet 5). Cache reads $0.20/M. Cache writes $2.50/M.
  - For comparison he gives Opus 5.5 at $4 / $20 / cache read $0.20 / cache write $5, and Fable 5.1 at $10 / $50 / cache read $0.25. He says Fable's cache read is "only 25% more" than Opus's.
- **Claims vs Sonnet 5:** "30% faster and up to 30% cheaper for most work."
- **AA cost per run:**
  - Max $7.60 vs Astra max $3.26.
  - Xhigh is "pretty close to Astra's price... cheaper".
  - High and medium are "crazy low prices, $18 and 59 respectively". This is probably $1.18 and $0.59; the transcript is ambiguous.
  - At xhigh, Sonnet is "roughly Astra level" on intelligence. At max it was about 3 points above Astra.
- **TPS:** about 94 on OpenRouter (Anthropic), Opus 70, Astra 30. On his subscription, about 150 Sonnet and about 100 Opus.
- **Subscription value:** "You get around $2,300 a week of usage on the $200 plan. That puts you at almost 10 grand a month." He now has six Claude accounts and "killed three accounts in the past few days". Compare the Fable video's figure of up to about $8K a month.
- Context window: not stated in this video.
- Haiku 5.5 is coming "in the next few weeks" for "high volume and cost-sensitive applications."

## 5. Recommended prompting style and workflow

- **Don't prompt it yourself; have Opus or Fable call it.** "I would bet that if you set Opus up properly to use Sonnet at the right times for these sub agents that the result will be Opus feeling way faster and getting real work done for slightly cheaper."
- **Effort:** use `high` or `xhigh`. Avoid `max` and `low`. Medium is "fine-ish" but noticeably weaker on Sonnet than on Opus.
- **Give it well-scoped, investigatory tasks with a clear deliverable.** His examples: "deep dives into your codebase to find specific behaviors or characteristics", "confirming a hunch it has about some thing that you found in an API", and analysis that helps the orchestrator "plan and scope work".
- **It reads the thread's context faithfully.** Prompts to a long-running Sonnet thread are interpreted in that thread's frame, so be explicit when changing topic.

## 6. Subagents, orchestration, delegation and verification

This is the core of the video:

- Sonnet 5.5 is positioned as a **subagent / research tool for Opus or Fable orchestrators**: "If you give Opus or Fable a big task and they want to analyze the codebase before starting, they can now call on Sonnet to do that and get results that they're more than happy with. This is huge."
- Suitable subagent jobs: codebase deep dives, behavior-finding, hunch confirmation, scoping and planning research, and "real world documents, office, and all that type of stuff". It is **not** for front-end building or day-to-day coding.
- His planning/decomposition bench (breaking a giant PR into landable pieces) ranks:
  - Astra best overall plan.
  - Sonnet best value and speed, slightly above Opus.
  - Fable below Opus, though it improved after a judging overhaul.
  - Sol fast but weak.
  - Grok 4.7 once outperformed Fable on an earlier version of this bench.
- He uses an "automated judging panel" to score proposals "on various axes", i.e. model-graded evaluation of planning outputs.
- Orchestration anecdotes:
  - He is using Opus 5.5 to rewrite the TypeScript compiler in Rust (for WASM). It "has fully unblocked" the project after Astra and Sol left "millions of lines" of slop. He told Opus to "halt and go clean up all of the legacy slop", and about 1.6M lines were deleted during filming.
  - He monitors the work from a separate T3 Code thread.
  - **Cost caution:** the Opus fish-slop run spawned a Fable 5.1 subagent unintentionally, which inflated its cost.
- He claims Anthropic now leads "the best model for calling other models".

## 7. Claude Code specifics

- Model picker: he advises humans not to pick Sonnet in Claude Code; let Opus or Fable delegate to it.
- Subscription economics: about $2,300 a week of usage on the $200 plan.
- He describes no specific subagent configuration syntax, skills, hooks, MCP or plugins. The recommendation is conceptual: configure Opus to use Sonnet subagents "at the right times".

## 8. Routing-table implications (Sonnet 5.5)

- **Route to Sonnet 5.5 as a subagent** (dispatched by an Opus or Fable orchestrator), not as a primary or interactive model.
- **Route to Sonnet:** codebase exploration and deep-dive analysis, architectural comprehension, decomposition research ("how could this giant change be split?"), locating specific behaviors, and verifying hunches about APIs or code. It gave the best cost per point and was about 2x faster than Opus on his audit bench.
- **Route to Sonnet:** document, slide and spreadsheet generation, and image or screenshot understanding (claimed strengths, lightly evidenced in the video).
- **Do not route** main implementation or day-to-day coding to Sonnet when Opus is available. Like-for-like it costs about the same or more, because cache reads cost the same $0.20 and it uses about 25% more tokens than Opus on Cursor Bench (272K vs 218K). Its wall-clock time is also worse.
- **Do not route** front-end or UI design to Sonnet. It is the weakest of the three Claude models there; use Fable first, then Opus.
- **Effort:** `high` (or `xhigh` for harder analysis). **Never `max`**: it is the most expensive setting, and on Frontier Code xhigh beat max. **Never `low`**. Treat `medium` as weaker than Opus-medium.
- **Cost model caveat:** Sonnet's per-token discount applies to uncached input, output and cache writes, but not to cache reads. Long, tool-heavy agentic loops are where cache reads dominate, so they erode its savings. Sonnet is most cost-effective for **short, bounded investigations** that finish quickly (about 5 minutes in his bench), not multi-hour agent loops.
- **For exhaustive code review or a "best possible plan"**, Astra still leads. Use Sonnet when cost and speed of analysis matter more than squeezing out the last bit of thoroughness.
- **Future slot:** Haiku 5.5 (not yet released) is intended for high-volume, cost-sensitive work. None of the transcripts evaluates Haiku 4.5.

---

# Cross-video synthesis (for the routing table)

| Dimension | Fable 5.1 | Opus 5.5 | Sonnet 5.5 |
|---|---|---|---|
| Price in / out / cache read / cache write ($/M) | 10 / 50 / 0.25 / not stated | 4 / 20 / 0.20 / 5 | 2 / 10 / 0.20 / 2.50 |
| Speaker's role for it | Hardest long-horizon work, PR takeovers, orchestration, front-end design | **Default daily driver**; ZDR-compliant | **Subagent for analysis / research**; not human-selected |
| Effort guidance | Default `high`; `low` often fine; little gain beyond `high` | `medium` (default) / `high` / `xhigh`; avoid `low` and `max` | `high` / `xhigh`; avoid `low` and `max`; `medium` weaker than Opus's |
| Token efficiency | Poor vs OpenAI; 1.7x Fable 5 output | Poor: about 120K tokens per AA task at max (vs Astra 27K) | Worst: 272K tokens per Cursor Bench task |
| Front-end taste | Best (with design skill) | OK and steerable; design skill doesn't help | Weak |
| Exhaustive review / audit | Better than Opus, below Astra | Below Fable, Astra, Sol, Grok 4.7 | Slightly above Opus on his decomposition bench, at half the cost |
| Known quirks | Few progress updates; dense prose; asks permission; scope creep (nearby fixes, extra tests); safeguard fallback to Opus | Context-window anxiety; dumb spikes; repair loops; slow to commit; runaway at `max` | Faster TPS but slower wall-clock; cache-read pricing makes it no cheaper for long agentic loops |
| Data retention | No ZDR (Enterprise Frontier Safeguards option) | ZDR available | Not discussed |

Points stated across videos:

- **Never use `max`** on any of these models. In both later videos it is shown to raise the reasoning *floor*, causing more than 10x token blowups and loops, sometimes with worse scores.
- Cache-read pricing, not headline input/output price, decides cost in agentic loops.
- Computer use is better routed to OpenAI (Astra). Anthropic models lag there per the speaker, though Sonnet and Opus are now "neck and neck" on OS World.
- The best exhaustive planner/reviewer in his tests is GPT-6 Astra: "most thorough" but "spiky and weird".
