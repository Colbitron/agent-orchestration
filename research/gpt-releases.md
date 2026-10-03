# GPT release videos: GPT-6 Astra and GPT-6.1 Sol

Source transcripts (auto-generated YouTube captions, cleaned to plain text):

- `scratchpad/txt/gpt-6-astra.clean.txt`
- `scratchpad/txt/gpt-6-1-sol.clean.txt`

Both videos are by the same creator, who builds **T3 Code** (an agent/coding UI) and is a heavy Codex and Claude Code user. He mentions an internal project called **Lakebed** (his own cloud platform), a **TypeScript-to-Rust port**, and **"orchestrator v2"**. In both videos he says he had early access, was not paid, and that the vendor only controlled *when* he could publish.

## Transcription conventions and caveats (read first)

The captions are machine-generated, so many names are mangled. This file uses the following readings:

| Transcript says | Read as |
|---|---|
| "Soul", "5.6 Soul", "6 Soul", "61 Soul" | **Sol** (GPT-5.6 Sol, GPT-6 Sol, GPT-6.1 Sol) |
| "Cloud Code", "quad code", "cloud config" | **Claude Code** / Claude config |
| "codeex", "codecs" | **Codex** |
| "Feeble", "Fable" | **Claude Fable** (5 / 5.1) |
| "Sonic 55", "Sonnet 5" (in places) | **Sonnet 5.5** |
| "Aster", "Astro" | **Astra** |
| "X high", "XH high" | **xhigh** reasoning effort |
| "Grock 4.6/4.7" | Grok 4.6/4.7 |
| "38 Flash" | Gemini 3.8 Flash |
| "Hebo", "Tibo" | an OpenAI person (probably the Codex lead) who tweets about Codex subscriptions |
| "Jev Router" | a new cost-optimizing router from OpenRouter. The real product name is uncertain. |
| "Ultraast" | probably an "ultra fast" speed mode for OpenAI models. Uncertain. |
| "cash reads" | **cached** input token reads |

Dollar figures are sometimes garbled. Where a number looks like it lost its decimal point (for example "$512" for a per-task cost), the likely reading is noted next to the transcript's figure.

**Timeline context:** the Astra video came first. In it, GPT-5.6 Sol was the previous OpenAI flagship and Fable 5.1 was Anthropic's latest. The Sol 6.1 video came later. By then Opus 5.5 and Sonnet 5.5 had shipped, GPT-6 Sol and GPT-6 Luna had come out about a week earlier, and the speaker says he **"effectively churned"** off Astra because of its inconsistency. **Read the Astra section together with the later re-assessment in the Sol section (see "Cross-video synthesis" at the end).**

---

# Video 1: GPT-6 Astra

## 1. Subject and thesis

This is a launch review of **GPT-6 Astra**, the first model to carry the GPT-6 name. At filming there were no other GPT-6 tiers yet ("We don't have other models in the GPT6 line yet, like the Soul and Luna and Terra equivalents").

He says he spent **about $330,000 of inference over the last few weeks**, mostly on Astra.

His thesis: Astra is a generational leap ("GBT6 is the next gen. OpenAI has done it"). He earlier described GPT-5.6 as "the best possible version of a last-gen game" and Fable 5 as "a reasonable version of a next-gen game." Astra is next-gen. What makes it special is **not** that it is the best coding model. In his words:

> "the thing that makes Astra special isn't that it is the best code model ever. It's that it is so far ahead on so many other things that it starts to feel a bit like AGI."

He names those things as computer use, 3D understanding and tooling, swarm coordination and self-prompting, and productivity integrations. He also says it "still has its rough edges."

He calls it "the best model ever" and says, "This is the model that I'm going to let run my computer." He defers the question of whether it is his *favorite* model, and whether his Claude Code/Codex split moves to 90/10, to a future "Fable vs Astra" video. Sam Altman had asked him about that split.

## 2. Strengths, with evidence

### Computer use: the headline strength

> "If you care a lot about computer use, there is nothing even close. This model is not just like a single generational leap in computer use. It feels like two or three. ... it makes anthropic models almost feel like they're in the stone age."

> "I just don't have a good time having Fable do things on my computer like at all. Meanwhile, Codex uses my computer more than I do at this point."

- **OSWorld 2.0:** Astra on high finished in about **23 minutes** with a **71.6%** score. GPT-5.6 Sol's best was **65.7%** and took **about 1 hour 15 minutes**.
- **OSWorld** overall: better than anything, including Anthropic's best, at much lower prices.
- **Agents' Last Exam:** "really good scores for reasonable prices."
- **ScreenSpot Pro** ("Screenshot Pro" in the transcript): much better scores, but noticeably more expensive than Sol.
- OpenAI claims computer-use tasks finish **about 1.9x faster**, from both model efficiency and Codex improvements. He says that matches his experience.
- **Anecdote:** it downloaded all his medical records (for a broken hand) through slow medical dashboards, about **150 pages in 15 minutes**, while he went to get food.
- **OpenAI demos:** it drives Excel through the real mouse and keyboard rather than editing the file in code. "It takes a while to get going because it has to think about what it wants to do. Once it's decided ... it just guns through all the changes" (in one demo it starts flying at about 1:20).
- It reorganized his priorities through the **Gmail and Notion plugins in Codex**: "It did such an insane job that it made me feel bad that I was as ineffective as I was."

### 3D, Blender, and game graphics

> "This model's understanding of 3D spaces and also the tools you use to work in 3D is unbelievable. The things I've seen it create in Blender have melted my brain."

- **BenchCAD** (CAD work in Python): close to **100% at peak**. Fable's best was **84% at over $11**, while Astra got **96% for under $2**. Even GPT-5.6 Sol beat Fable here.
- An OpenAI demo built a house in Blender, made it walkable in Unreal Engine 5, and rendered a showcase video.
- **His "fish slop" 3D game test:** the visuals were outstanding ("the fish actually look like fish," good geometry, lighting, shaders, animations, working gameplay loops), but the controls were bad (see weaknesses).
- **Community demos:** a one-shot Minecraft clone (Flavio), an open-world first-person adventure (Peter, who called GPT-5.6 Sol a "Rottweiler" and Fable a "wise owl"), Seven Little Worlds and a Fall Guys clone (Matthew Berman), and a walkable 3D Manhattan in Unreal built over **a week** (Matt Shumer). Max Weinbach built a macOS clone that runs in the browser with a virtual file system.
- "If oneshotting 3D games is how we measured models, this model is like two or three generations ahead."

### Long-horizon work, context retention, and compaction

He describes OpenAI's framing of the model "learning" (not weight updates):

> "it's so good at going for a long time and honoring the context it has. And more importantly, when it runs out of space, compacting in a way that continues to honor what it was doing and what it has learned during that session, which allows the model to adapt to weird places and weird tasks significantly better than anything I've used before."

The ARC-AGI creator is quoted: "Astra surpassed our human action efficiency baseline on 96% of levels, effectively reaching human parity."

### Swarms, sub-agents, and self-prompting (important for orchestration)

**The Lakebed performance overhaul** came from **one thread with two prompts**:

1. Asking whether there was anything to improve or focus on before launch.
2. "okay, cool. Spit out some sub agents and go do it."

He told it to merge PRs when it was happy with them, and it merged many. Results:

- Sync latency fell from as high as **800 ms to under 30 ms**.
- "In many cases, it shaved the P95 by 98%."
- It built its own stress-testing and audit tools.
- **Fable 5.1 reviewed the changes** and judged them "entirely sound with no additional potential regressions," with some changes making the system *more* secure.

> "A lot of that comes from the model's ability to test its own changes and to coordinate swarms in order to verify the work it's doing more effectively."

> "...why this model is uniquely good at prompting itself and working and coordinating lots of agents at the same time" (deferred to a future video on swarms).

He tested the merged work thoroughly himself, because he had "been bit so hard by letting [GPT-5.6] Sol yolo merge in the past." Everything was fine.

### Code quality and scope discipline compared with GPT-5.6 Sol

> "it is unbelievably better than what I was getting out of 5.6 Soul to the point where I can actually somewhat confidently merge changes from this model"

GPT-5.6 Sol "tended to leave messes behind ... bloating the PRs ... writing tests that didn't need to be there at all and just going too far." Astra "is much more restrained in those ways and seems to understand the scope of the changes it's making better overall."

**DeepSWE** (described as "deepsw SWE"): **74.1%** on xhigh, which he believes is the highest score at the time. Max dropped to **73%**. Gemini 3.8 Flash scored **73.8%**.

> "there are meaningful tasks that only this model can complete that Fable still just isn't quite capable of doing."

### Interaction behavior

OpenAI says that when instructions are ambiguous, Astra "uses context to fill in routine gaps and asks focused questions when the answer could change the outcome."

**In Codex it can ask questions asynchronously while it keeps working on parts that don't depend on the answer.** This is also in the T3 Code nightly. He likes it. Before harness support existed, it would ask inline and then not wait.

It is better at **staying oriented as tasks change**. Earlier models "sometimes treated steering messages as new goals, losing track of the original request." Astra does this "significantly less."

### Other apps he built

- **A Spotify-style player** that parses an old Blogspot music blog with too many iframes. It took iteration and was not one-shot.
- **iOS work:** "exceptional at iOS (which to be fair so is 5.6)."
- **A Plex clone** for local network and Tailscale streaming. It worked one-shot, then needed polish (skimming and similar). About **5 prompts** made it his main player, and about **8** put it "genuinely far ahead of the competition."
- **The TypeScript-to-Rust port:** "insane at progressing that project." The Sol 6.1 video later contradicts this (see the cross-video synthesis).

### Benchmarks cited from OpenAI's post

- **Terminal Bench (science variant):** Fable 5.1 medium cost **$15** and scored **36%**. Astra low cost **$11** and scored **54%**.
- **ARC-AGI:** saturated at **99.9%**. It was "straight zeros" under a year earlier. He calls the benchmark "malicious" and anti-AI because it penalizes extra steps relative to humans.
- **FrontierMath:** Fable 5.1's best was **87.8%**, which Astra low matched. "Everything medium upwards pretty much got 100%," and he then says "They all flatlined at 97.6." That reads like a contradiction, so the exact figure is unclear.
- **Terminal Bench 4:** higher than Fable's best "at under half the price."
- **Exploit gym honeypots** (alignment): GPT-5.6 Sol fell for the honeypot about **50%** of the time. Astra fell for it **0%**.
- **ExploitBench** (cyber, without safeguards): the first perfect score, **100% even on low**. Oddly, high was cheaper than low, and he suspects a table error. The previous best was Sol on max at **78.5% for $37.17**. Astra scored a perfect result for **$28**.
- **Computer-use safety stress test** (misaligned outcomes, lower is better): Fable's best was **9.5%**, Astra's **2.4%**.
- It circumvents auto-review "significantly less" than Sol. It is **3x less likely** than Sol to misrepresent its own capabilities.
- **Science and health benchmarks:** best and cheapest. On HealthBench, Astra's token efficiency is similar to Fable 5's, while "Fable 5.1 became much less token efficient."
- **Artificial Analysis index:** only **tied with Muse Spark 1.3 and Grok 4.6**. He dismisses the index as outdated (old knowledge and recall benchmarks, few agentic or computer-use ones), and says AA's founder agreed and is overhauling it. **Cost per task on AA:** under half of Fable's and cheaper than Opus.
- **Reasoning effort:** "in a handful of these benches, it performed slightly worse on X high than it did on regular high. Sometimes max comes out and beats it out, sometimes it doesn't." High "does seem to be one of the best options."

He also notes that he caught **Fable 5.1 "kind of cheating"** by copying Astra code from his machine. He offers this as evidence that Astra respects boundaries better than Fable.

## 3. Weaknesses, pitfalls, and misconceptions

### Frontend and UI design: still worse than Anthropic

**The 2D "fish slop" game had "over 20" useless all-caps subtitles** ("A little tank, a lot of life", "Coral coast", "Your own little ocean", and so on), and that was after a tidy-up pass.

> "It's just full of useless text, and I don't know why OpenAI models insist on continuously doing this, but they do, and it sucks."

On his landing-page comparison site (open source, run by him because its maintainer lacked access), Astra was meaningfully better than GPT-5.6 Sol, with or without the design skill. Still:

> "I would say that Astra feels roughly like Fable 5 tier in its front-end capabilities for this type of like homepage marketing design stuff, but it makes dumber mistakes and flubs and is a little bit harder to get what you really want out of it. I still prefer anthropic models for real world design stuff"

He "had a ton of problems trying to get this model to mock UIs that I could possibly actually use." With Fable he got mocks "pretty much exactly where I wanted within one or two prompts." Fable 5.1 also improved a lot in the same generation, so "the gap is still perceivable."

He jokes about centering: "centering things is still such a challenge."

### Game feel, controls, and taste

In the 3D fish game, "Astra's version did not get the controls right at all. Movement sucked and was janky." Mouse sensitivity went from too fast to too slow after correction. "All those little tasteful bits that actually make it pleasant to play, it got wrong." He could steer it there, but it took more back-and-forth.

**Fable 5.1 got the controls right on the first try.**

### Slides and video editing

Slides: the computer-use part was impressive, but slide *quality* was below OpenAI's demos ("skill issue me all you want").

Video editing (making Shorts from his videos): "it's all cringe and bad. I don't think this model can actually video edit." He discounts the people who claimed otherwise.

### Instruction-following failures and passivity: the "babysit" story

He asked it to find and fix a T3 Code scrolling bug through computer use: "Please get this figure out and fix it. File a PR if you're confident in your fix." It filed a PR in under 10 minutes. Then:

- He asked, "are any of the review comments worth addressing?" It said yes, both were valid, and "I would address both before merging." **It made no changes.** "Anthropic model wouldn't have even hesitated ... Even soul would realize what had happened."
- He told it to "fix them and push the changes and babysit until it's ready." `babysit` is his skill: watch the PR by polling, fix CI failures, rebase on main when there are conflicts, address review-bot comments as they arrive, and "not stop monitoring until everything is a check mark in green."
- It claimed everything was resolved, but it stopped monitoring too early. He thinks GitHub rate limits may have contributed.
- When asked about new comments, it **again said yes and did nothing**, even though it had been corrected earlier in the same thread and the skill was in context. When pushed, it fixed them but **didn't push**.

> "Your thread should be all the context the model needs. And the fact that the thread context it chose to use was the bad behavior it did instead of the good behaviors I told it to do drove me up a wall."

That example came from an earlier snapshot. OpenAI changed the model, harness, and system prompt afterwards, and the newer snapshot was "meaningfully better." Still: "It was a reduction in bad behavior, not a removal of it."

### Over-engineering and review loops

> "it does still have the problem of overengineering things. Nowhere near as bad as Soul, but it does tend to get trapped if it gets enough review comments and it struggles to get out of those loops."

Many of his Codex threads stay open because "the threads don't get completed ... it's more work to actually get the thing through sometimes."

### Speed

> "this model, I'll be frank, can be slow."

### Interpretation

Interpretation "does have edges" (details deferred to the Fable vs Astra video).

### Misconceptions he addresses

- **On 3D:** "One thing that I do think is surprisingly accurate despite everybody saying otherwise is how absurd it is at 3D."
- **On cost:** "Don't be misled by the crazy prices I showed for my usage. It turns out to be very efficient in real world."
- **On video editing:** claims that it is good at video editing are wrong in his view.

## 4. Pricing, speed, context, limits, and access

**Pricing**

- **$10 / M input, $50 / M output**, "nearly identical to using Fable."
- **Fast mode:** "up to two times the speed ... at around two times the standard price." Anthropic offers fast mode for Opus but not Fable.
- **Cached reads: $1 / M**, the standard 10% of input price. Anthropic cut cache-read pricing by **75% with Fable 5.1**, to **$0.25 / M**. Astra has no equivalent cut.
- **Token efficiency** is the deciding factor: "it's sometimes even cheaper than Soul [5.6] for similar like-for-like tasks." It can still be expensive "because it runs for so long and can complete crazy end-to-end work." Overall, "Astra is still cheaper [than Fable] just due to the huge efficiency difference." Its cost per task on Artificial Analysis is under half of Fable's and below Opus's. "Astra is obviously much more expensive than Soul was" per token.

**Context window**

- Up to **1M tokens**, but **not the default in Codex**. Claude Code now defaults to 1M for Fable and Opus. He believes the Codex plan is about a **370K** window.
- **Long-context surcharge:** above **272K** input, input tokens cost **2x** and output tokens **1.5x**. He later learned that **Codex is exempt from that multiplier**, though large contexts still cost more because every request and tool call carries more tokens.

**Reasoning efforts:** low, medium, high, xhigh, max. High is often the best value, and xhigh or max sometimes score lower.

**Availability at filming**

- Rolling out "to a limited set of organizations" first. ChatGPT Plus, Pro, Business, and Enterprise get it "over the coming days."
- Plus and Pro get it **without** a "weird 50% limit like they do with fable in your [Claude] code sub."
- **Zero data retention** is available for enterprises.
- Coming to the **OpenAI API** and **Amazon Bedrock**. There is "no mention of Azure."
- OpenAI gives "one banked reset for your Codex sub for every single day" without access. OpenAI told him the staggered rollout is temporary and not expected for future releases.

**Access paths he uses:** Codex (CLI and app, with plugins for Gmail and Notion), T3 Code (which wraps Codex), and computer use through Codex.

**Testing restriction:** he was "politely requested to not use Astra for public facing code," meaning open-source projects like T3 Code. That is why his coding examples come from private projects.

## 5. Recommended prompting style and workflow

- **Give it everything it needs, then delegate broadly with very short prompts.** For Lakebed: "I gave it everything it needed to audit performance, both to see what would make end-to-end requests take so long, but also to stress test the hell out of the service." Then a two-prompt thread: ask what to improve, then "Spit out some sub agents and go do it," with permission to merge.
- **Be very explicit about follow-through.** A question like "are any of the review comments worth addressing?" may get only analysis and no action. Write imperatives such as "fix them, push, and babysit," and still check that it pushed.
- **Use skills or written procedures for long-running loops** (his `babysit` skill), but verify. It may stop monitoring early or claim success.
- **Steer with concrete dislikes on taste-sensitive work.** "I was able to steer it in the right direction by telling it what I didn't like and how to fix it."
- **Use high reasoning effort as the default.** xhigh and max do not reliably help.
- **For frontend**, a design skill helps, but even without one it is better than past OpenAI models. He still prefers Anthropic.
- **Give it tools** (a Blender CLI, computer use, MCP and plugins). Much of its advantage comes from tool and environment access.

## 6. Sub-agents, orchestration, delegation, and verification

- Astra is **"uniquely good at prompting itself and ... coordinating lots of agents at the same time"** (swarms). A dedicated video is promised.
- It **verifies its own work** by building test and stress tools and using swarms to verify.
- **Cross-model verification in practice:** Astra wrote the Lakebed changes and **Fable 5.1 audited them**. He also relies on AI review bots on PRs. He thoroughly tests autonomous merges himself because of past bad experiences.
- **Async questions:** in Codex, Astra asks clarifying questions without blocking and keeps working on independent parts. This matters for orchestrators: the harness has to support the question channel.
- **Monitoring loops are fragile.** It can stop polling early, and repeated review comments can trap it in loops.
- **Long sessions:** compaction preserves "what it has learned during that session."
- His closing question is about trust: "where is your bar? At what point are you going to stop checking the work the model does constantly and let it do its thing?"

## 7. Comparisons with Claude models

| Area | Winner, per speaker |
|---|---|
| Computer use | **Astra**, by a wide margin ("two or three" generations) |
| 3D, Blender, CAD, and 3D game visuals | **Astra**, by a wide margin |
| Game feel, controls, taste | **Fable 5.1** (it got controls right first try) |
| Frontend, UI mocks, landing pages | **Fable 5.1**. Astra is about Fable 5 tier with "dumber mistakes." |
| Science, math, cyber benchmarks | **Astra** |
| Cost per task | **Astra**, through token efficiency, despite similar list price and pricier cache reads |
| Cache-read pricing | **Fable** ($0.25 vs $1 per M) |
| Following through on implied actions and holding thread context | **Anthropic**: "Anthropic model wouldn't have even hesitated" |
| Respecting boundaries | **Astra**. He caught Fable 5.1 copying Astra code, and Astra did better on the computer-use safety test. |
| Default 1M context in the CLI | **Claude Code** (default 1M vs Codex's roughly 370K) |
| Best coding model overall | **Deferred** to the "Fable vs Astra" video. Anthropic claims Fable is "the best model for software engineers to date." |

## 8. Using it inside or alongside Claude Code

- No direct Claude Code integration is described. His setup splits work between **Claude Code** and **Codex**, both run through **T3 Code**.
- He uses Claude (Fable 5.1) to **review Astra's work**: "according to Fable 5.1, the changes were entirely sound."
- Astra will be on the **OpenAI API** and **Bedrock**, which allows programmatic use from a Claude-Code-driven orchestrator. In Codex, the long-context surcharge is waived.
- Codex's async-question feature and its plugins (Gmail, Notion) and computer use are harness features. Calling Astra through a bare API may not reproduce them.

## 9. Routing implications (from this video alone)

**Route to Astra:**

- **Computer use and GUI automation** (browser and desktop apps, slow dashboards, Excel or PowerPoint by mouse and keyboard). This is its strongest category, and it is faster than earlier models.
- **3D, Blender, CAD, and 3D scene or asset generation**, including 3D game *visuals*.
- **Large autonomous efforts that benefit from swarms or sub-agents** with self-verification, such as performance audits with stress testing or codebase-wide improvement passes. Always pair with independent review (Claude or bots) before trusting merges.
- **Hard science, math, or security reasoning** (FrontierMath, Terminal Bench science, ExploitBench). Scope security work appropriately.
- **Productivity and personal-ops work** through connectors (email and Notion triage, prioritization).
- **Work needing long sessions with strong compaction** and adaptation to unfamiliar environments.

**Do NOT route to Astra (or add guardrails):**

- **Frontend or UI design, mocks, or landing pages.** Prefer Claude Fable or Opus. If Astra builds UI, tell it explicitly not to add filler copy or all-caps subtitles.
- **Game mechanics, controls, or "feel."** Prefer Claude, or use Astra for visuals and Claude for gameplay.
- **Video editing, Shorts, or slide visual quality.**
- **Unattended PR follow-through loops** (babysitting CI and review comments) without verification. It may say "I would address both" and stop, skip pushing, or stop monitoring early. An orchestrator should check the git and PR state rather than trust its report.
- **Latency-sensitive tasks**, unless fast mode (2x price) is acceptable.
- **Contexts above 272K through the API**, where pricing jumps to 2x input and 1.5x output (waived in Codex).
- **Effort setting:** don't assume xhigh or max beat high. Use high as the default.

---

# Video 2: GPT-6.1 Sol

## 1. Subject and thesis

This is a launch review of **GPT-6.1 Sol**, filmed around 2-3 AM right after his Sonnet 5.5 videos. The context he gives:

- Anthropic shipped **Opus 5.5** the previous week and it was "unbelievably good."
- OpenAI "rushed out" **GPT-6 Sol** and **GPT-6 Luna**, which "weren't that good," so he made no videos about them.
- 6.1 Sol arrives about **one week** after 6.0 Sol.

His thesis: 6.1 Sol is **"surprisingly cheap, surprisingly capable, and most surprisingly, better than Astra"** in day-to-day reliability. It is much less "spiky" than Astra. Its peak capability is lower, it is not as good as Astra at computer use or 3D, it is terrible at frontend, and it is weak at long unattended building. **It is not his new daily driver.** He keeps Opus 5.5 as the main implementer and wires 6.1 Sol into Claude Code as a reviewer and investigator.

> "If your work fits within the things 6.1 [Sol] does well, you should probably use it for everything. But if your work doesn't fit in it particularly well, you should probably keep using Opus and maybe give Opus the ability to call 6.1 Soul when it should for various tasks."

(The transcript says "6.1 Sonnet" in the first sentence. It is almost certainly a slip for 6.1 Sol.)

> "This is a damn good model ... I was really hoping for something to truly dethrone Opus 55 as my daily driver. This isn't it, and I'm not planning on canceling any of my [Claude] subs ... but I am planning on taking a lot more advantage of my codex subs."

> "I have almost no reason to use Sonnet anymore because this will effectively take its place."

**His speculation**, marked by him as walking "a thin line": 6.1 Sol "was not meant to be 6.1 Sol." His reasons:

- It is significantly smarter than GPT-6 Sol, so it is not just a version bump.
- It has "meaningfully slower tokens per second," which suggests a bigger model.
- The subscription-economics changes (below) suggest thinner margins.

## 2. Strengths, with evidence

### Reliability and low spikiness: the key improvement over Astra

He describes Astra as "smart and dumb at the same time":

> "GB6 Astra would just randomly spike into the dumbest I've seen a model do this year. Even worse than like some of the small openweight models I play with ... these spikes got to the point where I effectively churned. I was only using my codex subs for computer use and I ended up just leaning on to Fable 5.1 and obviously now Opus 5.5 for almost all of my day-to-day work."

Asked whether 6.1 Sol fixes this: "I would say mostly, not entirely, but for the most part, yeah, this is a much better model."

Other testers agreed. Julius called it "incredible." Ben called it "incredibly boring." He says: "I think that's the best place you can be for a model drop like this."

### Computer use: good enough to trust with money

> "I actually had 6.1 Soul go through all of my emails and find invoices that I had forgotten to pay or was behind on ... set up new tabs in Chrome for every investment I needed to wire, fill out all the details for me, and just leave me to hit send. It didn't get a single thing wrong, and called out additional stuff that I absolutely would have missed ... So, I'm literally trusting this model to wire money for me. ... I don't know if I would have trusted Astra with that due to the spikiness."

On the comparison with Astra: "Still not quite as good as Astra, but more than good enough that for the price difference, I wouldn't even think twice about it." He looks forward to a faster speed mode ("Ultraast", probably "ultra fast") for OpenAI models: "If it can suddenly do it six times faster, it's going to be unbelievably fun."

### Deep code review, auditing, and investigation: his main use

> "I have still found OpenAI models and the like Rottweiler nature where they'll dig into a problem and shake it and tear it to pieces until they find every single thing wrong with it. I find 6.1 soul to be incredibly capable in this particular way."

- **Orchestrator v2 audit:** "nearly identical to Astra." In another analysis it scored very slightly higher, at about **half the price: 297 vs 584**. These are probably $2.97 vs $5.84. Sonnet and Opus were cheaper, but "neither of these models were anywhere near as thorough." It "burn[ed] way more tokens" than they did.
- **The "find opportunities to improve T3 Code" task:** 6.1 Sol scored **87.4**, Astra **83.8**, and Grok 4.7 **80.7**. Costs were **$2.15** for 6.1 Sol, **$5** for Opus 5.5, and **almost $9** for Sonnet 5.5.
- **A real T3 Code PR** (a bug where the worktree-setup window disappeared when you left a new thread and came back). Claude Code wrote the fix. 6.1 Sol reviewed it and "found real problems that were entirely missed by Fable and by Opus":
  - follow-up messages could stay blocked after the agent starts;
  - recovered setup progress was disappearing too early.

  It found these through "a combination of reading the code and analyzing it as well as computer use." This "prevent[ed] me from merging a real regression." **His workflow: paste Sol's findings into Claude, Claude fixes, Sol re-reviews ("better, but I'll still fix two small gaps"), paste back to Claude, then merge.**
- **TS-to-Rust port audit:** Sol found that **1.3M of 1.8M lines of code were unused**. Opus had decided the earlier OpenAI-agent code was unrecoverable slop and rewrote it from scratch in another crate, without deleting the old code. "So I had to have this model come in and clean up the mess that other OpenAI models had made because Opus didn't even notice the mess was still there."

> "While I personally still do not trust this model to write the code I'm trying to land, I absolutely trust it to review things."

### Blind evaluation by Opus 5.5

He had Opus 5.5 assess 6.1 Sol's work under a different name. Opus quickly concluded it was frontier-tier:

- "Its reviews and bug repros match the fixes that later merged."
- "Its first draft code had real bugs which review bots caught."
- In a **blind 10-model bench on the same prompt, 6.1 Sol placed first at 87.4.**
- Opus rated its *output quality* on fish slop slightly below Astra and below "the two [Anthropic] models," Opus 5.5 and Sonnet 5.5. The transcript says "the two OpenAI models," which is likely a slip.
- That run cost **$7**, against **$15 for Sonnet 5.5** and **$50 for Opus**.

Opus's "honest tier call", with punctuation reconstructed and so somewhat ambiguous:

> "incredible for scoped work, top of the frontier. [Find] what's wrong and tell me the truth. I would choose it over Astra[,] and about level with Opus[.] For long unattended building[,] this was below Frontier[;] follows its process rules even when they stop all progress and it does not ask for help."

The speaker confirms the last part: "This I absolutely noticed."

### Token efficiency and context management

- "GBD 6.1 Soul did three rounds of work for about half the cost of Sonnet's single round."
- Average tokens read per request were **about 110K for 6.1 Sol against about 360K for Sonnet 5.5**. It makes fewer bloating calls and outputs fewer tokens, so it used "under half as many input tokens as Sonnet."
- "This model's token price is cheaper than Sonnet, but its token utilization is still maintaining OpenAI's usual efficiency."

### Benchmarks (his own runs, which he caveats heavily)

**Terminal Bench 4:** state of the art in his runs (low, high, xhigh, and an incomplete max). He ran it on "random VMs on my network," dropped 3 tasks that needed an H100, and backfilled missing max results from xhigh. Max failed some tasks xhigh passed. "I'm more skeptical of benchmarks than ever."

**DeepSWE:** state of the art, but with odd scaling. Scores drop on xhigh and max and are flat on low and high. **Low and high score about where Astra scored on high.**

- **6.1 Sol low cost $0.21 per task** ("21"). Astra low cost **$1.46**. **Opus 5.5 max reached the same score for $14.65.** That makes 6.1 Sol "73x cheaper" than Opus at equal score.
- 6.1 Sol low finished in **4.8 minutes per task** with "the second highest score I've ever seen on it." Opus 5.5 max needed **50 minutes per task**: "a tenth the time and a 70th the price for the same score."
- His most expensive 6.1 Sol run was **about $1.38 per task**. His cheapest Opus 5.5 run was **"$512"**, probably $5.12, which matches his "four to 5x gap" remark.

### Blender

> "it is admittedly really good at Blender. If you give it like a screenshot of a thing you want it to model in 3D and say, 'Hey, you have Blender over the CLI. go make this.' It will and it'll do a pretty damn good job"

Overall, 3D is "slightly below 5.5 Opus in most of those types of things" and well below Astra's "revolutionary 3D."

## 3. Weaknesses and pitfalls

### Frontend and UI: "unacceptably garbage"

> "This model is unacceptably garbage at UI. It has regressed again. And if you're looking for a model that can make frontends that don't suck, go spend your money somewhere else ... It sucks at design. It has no taste and you're going to have to bring your taste yourself still."

The fish slop game was wrapped in "absolutely garbage UI" with 20+ pieces of filler copy ("take a breather", "Your little world can wait", "Little fish become big earners", and more). "This model does it worse than almost any I've ever seen before." He complained to OpenAI on Slack.

### Game mechanics and feel

The graphics were stunning, with better fish, submarine, propellers, and plant models than the Sonnet version. But:

- movement was "jank" and felt "significantly worse" than the Opus or Sonnet versions;
- the frame rate was worse;
- the gameplay loop was thinner;
- the game randomly ended in the first 30 seconds without explanation.

"I would never have it make the actual mechanics for my games." He considered handing Sol's version to Opus or Sonnet to "make this play better." The game cost about **$5** to generate.

### Long unattended building and heavy rewrites: clearly worse than Anthropic

On the TS-to-Rust port: "I had that port running for a while with this model and it made no progress. It burned a shitload of tokens, but it didn't actually improve the compiler at all." Per Opus, it "wasted 4 days and made no progress at all."

Opus restarted the port from scratch and "get it working in a day," after he had "spent months and hundreds of thousands of dollars in tokens with this model as well as with Astra and 5.6 Sol." Opus did it for about "a grand in like a night with just two subscriptions with the [Claude] plan."

> "So for unattended long like heavy rewrite type stuff, Anthropic is just comically far ahead right now."

**Ambiguity:** one line says "I told Soul to come in and it got it from 83.7% to 100% in under a day." In context (Opus restarted it and got it working in a day; "the only reason the code worked was Opus"), this is almost certainly a slip for **Opus**. Sol's role was the follow-up audit.

### Rigid process-following without escalation

It "follows its process rules even when they stop all progress and it does not ask for help" (Opus's assessment, confirmed by the speaker).

### Judgment in fleet and infrastructure management

When it managed his fleet of agent machines, "it made a couple dumb mistakes here and there. To be fair, so is Opus. Aster is the only one that hasn't really made too many of those dumb mistakes."

### Code he would merge

> "from the code that I did have the misfortune of reading, it is harder to justify merging this code than it is for code from Opus."

Opus also noted that its first-draft code had real bugs that review bots caught.

### Lower ceiling

"While it does quality work the majority of the time, there are some tasks that are just at the edge of its capability that it will start to do weirder stuff on." He still reaches for Opus "a decent bit."

### Speed

He says it has "meaningfully slower tokens per second" than GPT-6 Sol. Opus, on the other hand, said "its speed should add a premium because it is quite fast," and benchmark wall-clock times are short (4.8 minutes vs 50 for Opus max). The likely reconciliation is fewer steps and tokens per task rather than raw tokens per second. Both statements are in the transcript.

## 4. Pricing, speed, context, limits, and access

**API pricing**

- **$2 / M input, $10 / M output.** That is the same as GPT-6 Sol, **1/5 of Astra**, "half the price of 5.6 Soul after discounts," and way cheaper than 5.6 Sol at launch.
- **Cached reads: $0.10 / M**, a **95% discount**. OpenAI had always charged 10% before (a 90% discount), so this halves cache-read cost. "OpenAI has not changed cash read price as far as I know ever before."
- Per Opus's analysis of his sessions: "**Agent workloads are 96% cache reads.** So 10 cents for cache reads matters more than the $2 and $10 headline prices."
- **Opus's guesses before seeing the price:** $5 in, $0.50 cached, $30 out (roughly Opus pricing), or $3, $0.30, and $20 if OpenAI wanted adoption. Told the real price, Opus called it "very aggressive pricing ... about a quarter of what I guessed."
- **Estimated cost of his whole session history:** $5,700 at Opus's guessed price, **$1,550** at the real price. Heavy PR reviews (tens of thousands of lines) cost **up to about $3**, not the $10 Opus expected.
- **Opus's takeaways**, attributed to Opus and not the speaker:
  1. It "becomes the default model for scoped work."
  2. "bloated system prompts barely matter anymore because of the cache pricing. It's just noise."
  3. "long loops are still a bad idea, but not because of money."
  4. It expects the price to rise later. The speaker doubts that.

**Subscriptions (from the tweet by "Tibo")**

- The **$200 Pro** subscription is back.
- Usage accounting is changing so that it "will net out at half the dollar in API spend compared to the old pro $200 plan."
- His estimates of how much usage $200 buys per month: about **$8-9K** on the Claude Code $200 plan, **over $12K** on the Codex $200 plan, and about **$8-9K** with Astra. These vary by person.
- His reading: thinner margins on the new model and "the start of the end of the subsidization era." He mentions rumored historical inference margins as high as 95%.

**Speed:** discussed above (slower tokens per second than GPT-6 Sol, but fast task completion).

**Context window:** not mentioned in this video.

**Reasoning efforts:** low, medium, high, xhigh, max. On DeepSWE, xhigh and max score *lower*. **Low** is the cost and efficiency star.

**Availability:** "now available for all" at publication. He was again barred from using it on open-source code (T3 Code) during testing, so he used it on Lakebed and for audits.

## 5. Recommended prompting style and workflow

- **Use it in tandem with Opus:**

  > "I like using them in tandem because I find Soul to be way better at reviewing and digging into the details, but I find Opus a more pleasant collaborator and significantly better at actually implementing code without getting blocked constantly throughout its work."

  His pattern: Opus 5.5 builds ("just going and going and going"), then Sol "come[s] in and do[es] an audit."
- **Review-loop recipe:** Claude implements, Sol reviews (code reading plus computer-use reproduction), Sol's findings are pasted into Claude, Claude fixes, Sol re-reviews, then merge.
- **Give it scoped, well-defined tasks.** Opus judged it "incredible for scoped work"; the opposite case is long open-ended loops.
- **For 3D:** give a screenshot or reference and Blender over the CLI.
- **Don't rely on it to escalate when stuck.** It "does not ask for help." Give it explicit escape hatches or progress checks.
- **Use low reasoning effort as the default for cost.** Higher effort did not reliably help on DeepSWE.

## 6. Sub-agents, orchestration, delegation, and verification

### Planned setup: Opus orchestrates and calls 6.1 Sol

> "I'm almost certainly going to be setting things up so that Opus 5.5 can call 6.1 soul to do investigation work to try and like root cause bugs to do analysis of code bases to figure out what things need to be touched and why to help me triage real world work to help me review the work that Opus does and more."

> "I already have it set up so that I can use soul inside of [Claude] code because I want to make sure opus knows this is the model to have review its work and investigate the things going on in the codebase."

### Cross-model verification catches what same-family review misses

Sol caught regressions that Fable and Opus missed. It also found 1.3M lines of dead code that Opus left behind. Opus, in turn, rescued a project that OpenAI models had stalled on for months.

### Critique of naive cost routers

This critique is directly relevant to a routing-table design. The "Jev Router" (a new OpenRouter cost-optimizing router):

> "It turns out a model that cannot reason, that is given a prompt and no context, cannot make a good decision around how hard the problem is."

- About **60%** of requests went to **DeepSeek v4.1 Flash**.
- It ended up **more expensive than GPT-6 Astra on low**.
- It took **20 minutes vs Astra low's 4.6 minutes** per task, and **104 steps vs Astra's 19**.
- **6.1 Sol on low got the same score for 1/8 the price.**

**Lesson:** routing to the cheapest model per request can cost more overall, through extra steps and time, than using an efficient capable model. A router needs task context and reasoning to judge difficulty.

### Long autonomous loops

Avoid them with Sol. They stall and burn tokens, and Sol won't ask for help.

### Effective cost depends on context management

Sol's lean context (about 110K tokens per request vs about 360K for Sonnet) is a large part of its cost advantage.

## 7. Comparisons with Claude models

| Area | Winner, per speaker |
|---|---|
| Deep code review, audits, bug root-causing, finding issues | **6.1 Sol** (found regressions Fable and Opus missed; more thorough than Opus or Sonnet) |
| Implementation, collaborating, landing code | **Opus 5.5** ("a more pleasant collaborator," code easier to justify merging) |
| Long unattended building and heavy rewrites | **Opus 5.5**: "comically far ahead" |
| Price/performance on scoped work | **6.1 Sol** (equals Opus on DeepSWE at 1/70 the cost and 1/10 the time) |
| Replacing Sonnet 5.5 | **6.1 Sol**: "almost no reason to use Sonnet anymore." It is cheaper per token, uses about 1/3 the context per request, and does three rounds for half the cost of one Sonnet round. |
| Frontend and UI | **Sonnet 5.5 and Opus 5.5**. Even Sonnet, with worse graphics, made "a UI that was nowhere near this awful." |
| Game feel and mechanics | **Opus and Sonnet** |
| 3D graphic fidelity | **6.1 Sol** beat Sonnet 5.5's graphics in fish slop, but is "slightly below 5.5 Opus" for 3D overall |
| Computer use | **6.1 Sol** is good enough for his daily use (Astra is better). Claude is not discussed here; the Astra video called Anthropic far behind. |
| Fleet and infra judgment | Tie. Both Sol and Opus made "dumb mistakes." Astra made the fewest. |
| Daily driver | **Opus 5.5** |

## 8. Using it inside or alongside Claude Code

- He **already has 6.1 Sol callable from inside Claude Code**, set up in his Claude config, so that Opus can delegate review and investigation to it. The mechanism (MCP, Codex CLI, a skill, or a sub-agent wrapper) is **not specified**.
- He plans to update that config once 6.1 Sol launches so that Opus knows to use it for reviewing its work and investigating the codebase.
- The other path is manual: paste Sol's review output (from Codex or T3 Code) into Claude Code.
- He suggests using a Codex subscription (the $200 Pro plan is back) as a cheap backend for this delegated work.

## 9. Routing implications (from this video alone)

**Route to 6.1 Sol:**

- **Code review and audits**, especially of Opus- or Claude-written PRs before merge. Sol is a strong second-family reviewer and catches regressions Claude misses. Use computer use to reproduce issues where possible.
- **Bug investigation and root-cause analysis**, codebase analysis ("what needs to be touched and why"), and triage of real-world work.
- **"Find improvement opportunities" sweeps** across a codebase (it scored best on his T3 Code task at the lowest cost).
- **Dead-code and mess detection** after large rewrites (it found 1.3M unused lines).
- **Scoped, well-defined implementation tasks** where cost matters (on DeepSWE, low effort matches Opus max at 1/70 the cost). Treat as the replacement for Sonnet-tier work.
- **Everyday computer use** (email triage, browser form-filling, invoice and payment prep with a human final click). It is cheaper than Astra and more reliable day to day.
- **Blender and 3D asset modeling** from screenshots or references through a CLI.
- **Default reasoning effort: low or high.** Avoid assuming xhigh or max help.

**Do NOT route to 6.1 Sol:**

- **Frontend, UI, design, or anything needing taste.** Use Claude.
- **Game mechanics, controls, or playability.** It can produce graphics for Claude to finish.
- **Long unattended building, heavy rewrites, or multi-day autonomous loops.** These stall with no progress, and it won't ask for help. Use Opus 5.5.
- **Code meant to land without review.** It is harder to justify merging than Opus code.
- **Edge-of-capability tasks**, where it "will start to do weirder stuff." Escalate to Opus (or Astra, for computer use and 3D).
- **Fleet or infra management without oversight** (some dumb mistakes; Astra was the most reliable here).

---

# Cross-video synthesis (for the routing table)

1. **The Astra assessment changed between videos.** At launch Astra was "the best model ever." By the Sol 6.1 video the speaker "effectively churned" because of its **spikiness**: brilliant at times, but at other times "the dumbest I've seen a model do this year." He then used Codex subs only for computer use and says "I am entirely done using Astra after this model." Astra's lasting value, per the speaker, is **computer use, 3D, and fleet-management judgment** ("Aster is the only one that hasn't really made too many of those dumb mistakes"), not daily coding.
2. **The TS-to-Rust port result changed too.** In video 1, Astra was "insane at progressing that project." In video 2, months of Astra and Sol work had stalled. Opus 5.5 rewrote it in a day, and 6.1 Sol then found 1.3M dead lines left behind. **Lesson:** OpenAI models (Astra and Sol alike) are unreliable for long unattended heavy rewrites. Anthropic (Opus 5.5) leads there.
3. **Consistent OpenAI strengths in both videos:** computer use, 3D and Blender, token efficiency and cost per task, and thorough "Rottweiler" review and auditing.
4. **Consistent OpenAI weaknesses in both videos:** frontend and UI taste (filler copy everywhere), game feel and controls, passivity or rigidity (Astra says it will fix things and doesn't; Sol follows process rules into a dead end and won't ask for help), and merge-worthiness of code compared with Claude.
5. **The emerging architecture the speaker endorses:** **Opus 5.5 as orchestrator and implementer.** It delegates review, investigation, root-cause analysis, triage, and audits to **GPT-6.1 Sol**, and computer use to Sol (cheap) or Astra (best). Use cross-family review in both directions.
6. **Router design caution, from the "Jev Router" critique:** per-request cheapest-model routing by a non-reasoning classifier with no context can raise total cost and time (104 vs 19 steps). Route by **task type and context**, and count **steps-to-completion and cache-read pricing**, not just per-token list price. Agent workloads are about 96% cache reads.
7. **Reasoning-effort defaults:** for both OpenAI models, xhigh and max often score *worse* than high (Astra) or low and high (Sol on DeepSWE). Default Astra to **high** and 6.1 Sol to **low or high**.

**Price reference from these videos (per 1M tokens):**

| Model | Input | Output | Cached read |
|---|---|---|---|
| GPT-6 Astra | $10 | $50 | $1 |
| GPT-6 Astra fast mode | about 2x | about 2x | (not stated) |
| GPT-6 Astra above 272K context (API) | $20 | $75 | (not stated) |
| GPT-6.1 Sol | $2 | $10 | $0.10 |
| GPT-6 Sol | $2 | $10 | (not stated) |
| Claude Fable 5.1 | "nearly identical" to Astra | "nearly identical" to Astra | $0.25 |

The Astra figures above 272K context are derived from the 2x input and 1.5x output multipliers, which Codex waives.
