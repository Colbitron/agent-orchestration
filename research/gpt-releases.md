# GPT release videos: GPT-6 Astra and GPT-6.1 Sol

**Sources**

- ASTRA: "It's Here. (GPT-6 Astra launch)", Theo (t3.gg), YouTube, https://youtu.be/XFWpf0wLbh0
- SOL61: "OpenAI fights back (GPT-6.1 Sol launch)", Theo (t3.gg), YouTube, https://youtu.be/vu8X3YroB-w

A citation `[KEY m:ss]` links to that video at that timestamp. Quotes are from the auto-generated captions, read through the conventions table below.

This note keeps what the kit uses from two launch reviews: verdicts, numbers, prices, and routing rules. The speaker builds **T3 Code** (an agent UI that wraps Codex and Claude Code) and refers to **Lakebed** (his own cloud platform), a **TypeScript-to-Rust port**, and **"orchestrator v2"**. In the Sol 6.1 video he says he had early access, was not paid, and the vendor controlled only *when* he could publish [SOL61 1:22](https://youtu.be/vu8X3YroB-w?t=82).

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

**Timeline context:** the Astra video came first. In it, GPT-5.6 Sol was the previous OpenAI flagship and Fable 5.1 was Anthropic's latest. The Sol 6.1 video came later. By then Opus 5.5 and Sonnet 5.5 had shipped, GPT-6 Sol and GPT-6 Luna had come out about a week earlier, and the speaker says he **"effectively churned"** off Astra because of its inconsistency [SOL61 10:38](https://youtu.be/vu8X3YroB-w?t=638). **Read the Astra section together with the later re-assessment in the Sol section (see "Cross-video synthesis" at the end).**

---

# Video 1: GPT-6 Astra

## 1. Subject and thesis

**GPT-6 Astra** is the first GPT-6 model; there were no Sol, Luna, or Terra GPT-6 tiers yet [ASTRA 0:33](https://youtu.be/XFWpf0wLbh0?t=33). He had spent **about $330,000 of inference over the last few weeks**, mostly on Astra [ASTRA 0:20](https://youtu.be/XFWpf0wLbh0?t=20).

- **A generational leap:** GPT-5.6 was "the best possible version of a last-gen game", Fable 5 "a reasonable version of a next-gen game", and "GBT6 is the next gen" [ASTRA 0:57](https://youtu.be/XFWpf0wLbh0?t=57), with "rough edges" [ASTRA 1:13](https://youtu.be/XFWpf0wLbh0?t=73).
- **Not the best coder, but ahead elsewhere:** "the thing that makes Astra special isn't that it is the best code model ever" [ASTRA 40:44](https://youtu.be/XFWpf0wLbh0?t=2444). It leads on computer use, 3D understanding and tooling, swarms and self-prompting, and productivity integrations [ASTRA 40:55](https://youtu.be/XFWpf0wLbh0?t=2455).
- **Verdict:** "the best model ever" [ASTRA 42:20](https://youtu.be/XFWpf0wLbh0?t=2540) and "the model that I'm going to let run my computer" [ASTRA 43:15](https://youtu.be/XFWpf0wLbh0?t=2595). Whether it is his *favorite*, and whether his Claude Code/Codex split goes to 90/10 (Sam Altman's question), is deferred to a "Fable vs Astra" video [ASTRA 40:15](https://youtu.be/XFWpf0wLbh0?t=2415) [ASTRA 42:14](https://youtu.be/XFWpf0wLbh0?t=2534).

## 2. Strengths, with evidence

### Computer use: the headline strength

- "If you care a lot about computer use, there is nothing even close" [ASTRA 11:43](https://youtu.be/XFWpf0wLbh0?t=703): "two or three" generational leaps, making Anthropic models feel "like they're in the stone age" [ASTRA 11:49](https://youtu.be/XFWpf0wLbh0?t=709); "Codex uses my computer more than I do" [ASTRA 12:08](https://youtu.be/XFWpf0wLbh0?t=728).
- **OSWorld 2.0:** Astra high scored **71.6%** in about **23 minutes**; GPT-5.6 Sol's best was **65.7%** in **about 1 hour 15 minutes** [ASTRA 12:43](https://youtu.be/XFWpf0wLbh0?t=763).
- **OSWorld:** better than anything, including Anthropic's best, at much lower prices. **Agents' Last Exam:** "really good scores for reasonable prices". **ScreenSpot Pro** ("Screenshot Pro"): much better scores but noticeably more expensive than Sol [ASTRA 12:19](https://youtu.be/XFWpf0wLbh0?t=739).
- OpenAI claims computer-use tasks finish **about 1.9x faster**, which matches his experience (about **150 pages** of slow dashboards in **15 minutes**) [ASTRA 13:57](https://youtu.be/XFWpf0wLbh0?t=837) [ASTRA 14:08](https://youtu.be/XFWpf0wLbh0?t=848).
- It drives Excel by real mouse and keyboard, slow to start then fast (about 1:20 into one demo) [ASTRA 13:22](https://youtu.be/XFWpf0wLbh0?t=802), and does personal ops through Codex's **Gmail and Notion plugins** [ASTRA 41:15](https://youtu.be/XFWpf0wLbh0?t=2475).

### 3D, Blender, and game graphics

- Its understanding of 3D space and 3D tools "is unbelievable" [ASTRA 13:46](https://youtu.be/XFWpf0wLbh0?t=826).
- **BenchCAD** (CAD in Python): close to **100% at peak**. Fable's best was **84% at over $11**; Astra got **96% for under $2**. Even GPT-5.6 Sol beat Fable [ASTRA 14:24](https://youtu.be/XFWpf0wLbh0?t=864) [ASTRA 14:38](https://youtu.be/XFWpf0wLbh0?t=878).
- **3D game visuals:** excellent fish, geometry, lighting, shaders, and working gameplay loops in his "fish slop" test [ASTRA 16:19](https://youtu.be/XFWpf0wLbh0?t=979) [ASTRA 16:44](https://youtu.be/XFWpf0wLbh0?t=1004); with Blender access, "unfair to even compare" [ASTRA 17:44](https://youtu.be/XFWpf0wLbh0?t=1064). At one-shotting 3D games it is "like two or three generations ahead" [ASTRA 28:13](https://youtu.be/XFWpf0wLbh0?t=1693); one community build, a walkable 3D Manhattan, ran over **a week** [ASTRA 29:26](https://youtu.be/XFWpf0wLbh0?t=1766).

### Long-horizon work, context retention, and compaction

It honors context over long runs and compacts in a way that "continues to honor what it was doing and what it has learned during that session", so it adapts to unfamiliar tasks better than anything he has used [ASTRA 11:12](https://youtu.be/XFWpf0wLbh0?t=672). This is not weight updates [ASTRA 11:07](https://youtu.be/XFWpf0wLbh0?t=667). The ARC-AGI creator: "Astra surpassed our human action efficiency baseline on 96% of levels" [ASTRA 10:28](https://youtu.be/XFWpf0wLbh0?t=628).

### Swarms, sub-agents, and self-prompting (important for orchestration)

**The Lakebed performance overhaul** came from **one thread with two prompts** [ASTRA 33:52](https://youtu.be/XFWpf0wLbh0?t=2032): what to improve before launch, then "okay, cool. Spit out some sub agents and go do it" [ASTRA 33:58](https://youtu.be/XFWpf0wLbh0?t=2038), with permission to merge PRs it was happy with [ASTRA 34:04](https://youtu.be/XFWpf0wLbh0?t=2044).

- Sync latency fell from as high as **800 ms to under 30 ms**; "In many cases, it shaved the P95 by 98%" [ASTRA 33:24](https://youtu.be/XFWpf0wLbh0?t=2004) [ASTRA 33:30](https://youtu.be/XFWpf0wLbh0?t=2010). It built its own stress-testing and audit tools [ASTRA 33:07](https://youtu.be/XFWpf0wLbh0?t=1987).
- **Fable 5.1 reviewed the changes** as "entirely sound with no additional potential regressions", some more secure [ASTRA 33:41](https://youtu.be/XFWpf0wLbh0?t=2021).
- The cause, in his view: it tests its own changes and coordinates swarms to verify its work [ASTRA 34:15](https://youtu.be/XFWpf0wLbh0?t=2055), and is "uniquely good at prompting itself" while coordinating many agents (a swarms video is promised) [ASTRA 34:31](https://youtu.be/XFWpf0wLbh0?t=2071).
- He still tested every merge himself, having been "bit so hard by letting [GPT-5.6] Sol yolo merge". All were fine [ASTRA 34:09](https://youtu.be/XFWpf0wLbh0?t=2049).

### Code quality and scope discipline compared with GPT-5.6 Sol

- Much better than 5.6 Sol, "to the point where I can actually somewhat confidently merge changes" [ASTRA 19:44](https://youtu.be/XFWpf0wLbh0?t=1184). 5.6 Sol left messes, bloated PRs, and wrote needless tests [ASTRA 19:57](https://youtu.be/XFWpf0wLbh0?t=1197) [ASTRA 20:02](https://youtu.be/XFWpf0wLbh0?t=1202); Astra "is much more restrained" about scope [ASTRA 20:14](https://youtu.be/XFWpf0wLbh0?t=1214).
- **DeepSWE** ("deepsw SWE"): **74.1%** on xhigh, probably the highest at the time; **73%** on max; Gemini 3.8 Flash **73.8%** [ASTRA 20:26](https://youtu.be/XFWpf0wLbh0?t=1226) [ASTRA 20:38](https://youtu.be/XFWpf0wLbh0?t=1238).
- Some meaningful tasks only Astra can complete, "that Fable still just isn't quite capable of doing" [ASTRA 40:08](https://youtu.be/XFWpf0wLbh0?t=2408).

### Interaction behavior

- Per OpenAI, it "uses context to fill in routine gaps and asks focused questions when the answer could change the outcome" [ASTRA 18:16](https://youtu.be/XFWpf0wLbh0?t=1096).
- **In Codex it asks questions asynchronously while working on parts that don't depend on the answer** (also in the T3 Code nightly). Before harness support, it asked inline and did not wait [ASTRA 18:22](https://youtu.be/XFWpf0wLbh0?t=1102) [ASTRA 18:28](https://youtu.be/XFWpf0wLbh0?t=1108).
- It treats steering messages as new goals "significantly less" than earlier models, so it stays oriented as tasks change [ASTRA 18:59](https://youtu.be/XFWpf0wLbh0?t=1139) [ASTRA 19:06](https://youtu.be/XFWpf0wLbh0?t=1146).

### Other apps he built

- "exceptional at iOS (which to be fair so is 5.6)" [ASTRA 31:01](https://youtu.be/XFWpf0wLbh0?t=1861). A Plex clone worked one-shot; about **5 prompts** made it his main player and about **8** "genuinely far ahead of the competition" [ASTRA 31:48](https://youtu.be/XFWpf0wLbh0?t=1908). A Spotify-style player needed iteration [ASTRA 30:50](https://youtu.be/XFWpf0wLbh0?t=1850).
- **The TypeScript-to-Rust port:** "insane at progressing that project" [ASTRA 35:34](https://youtu.be/XFWpf0wLbh0?t=2134), contradicted by the Sol video (see the cross-video synthesis).

### Benchmarks cited from OpenAI's post

- **Terminal Bench (science variant):** Fable 5.1 medium **$15**, **36%**; Astra low **$11**, **54%** [ASTRA 8:32](https://youtu.be/XFWpf0wLbh0?t=512).
- **ARC-AGI:** saturated at **99.9%**, from "straight zeros" under a year earlier [ASTRA 9:38](https://youtu.be/XFWpf0wLbh0?t=578). He calls it "malicious" for penalizing extra steps relative to humans [ASTRA 9:02](https://youtu.be/XFWpf0wLbh0?t=542).
- **FrontierMath:** Fable 5.1's best, **87.8%**, was matched by Astra low. "Everything medium upwards pretty much got 100%," yet "They all flatlined at 97.6"; the exact figure is unclear [ASTRA 9:50](https://youtu.be/XFWpf0wLbh0?t=590) [ASTRA 9:56](https://youtu.be/XFWpf0wLbh0?t=596).
- **Terminal Bench 4:** above Fable's best "at under half the price"; xhigh and max slightly worse [ASTRA 10:15](https://youtu.be/XFWpf0wLbh0?t=615) [ASTRA 10:21](https://youtu.be/XFWpf0wLbh0?t=621).
- **Exploit gym honeypots** (alignment): GPT-5.6 Sol fell for it about **50%** of the time, Astra **0%** [ASTRA 11:37](https://youtu.be/XFWpf0wLbh0?t=697).
- **ExploitBench** (cyber, no safeguards): first perfect score, **100% even on low**; high was oddly cheaper than low (maybe a table error) [ASTRA 21:46](https://youtu.be/XFWpf0wLbh0?t=1306). Previous best: Sol max, **78.5% for $37.17**; Astra perfect for **$28** [ASTRA 21:59](https://youtu.be/XFWpf0wLbh0?t=1319).
- **Computer-use safety stress test** (misaligned outcomes, lower is better): Fable's best **9.5%**, Astra **2.4%** [ASTRA 22:25](https://youtu.be/XFWpf0wLbh0?t=1345). It circumvents auto-review "significantly less" than Sol and is **3x less likely** to misrepresent its capabilities [ASTRA 22:44](https://youtu.be/XFWpf0wLbh0?t=1364) [ASTRA 22:50](https://youtu.be/XFWpf0wLbh0?t=1370).
- **Science and health:** best and cheapest [ASTRA 21:07](https://youtu.be/XFWpf0wLbh0?t=1267). On HealthBench its token efficiency matches Fable 5's, while "Fable 5.1 became much less token efficient" [ASTRA 21:20](https://youtu.be/XFWpf0wLbh0?t=1280).
- **Artificial Analysis index:** only **tied with Muse Spark 1.3 and Grok 4.6** [ASTRA 23:04](https://youtu.be/XFWpf0wLbh0?t=1384). He calls the index outdated (old recall benchmarks, few agentic or computer-use ones) [ASTRA 23:25](https://youtu.be/XFWpf0wLbh0?t=1405); AA's founder agreed and is overhauling it [ASTRA 23:56](https://youtu.be/XFWpf0wLbh0?t=1436). **AA cost per task:** under half of Fable's and below Opus [ASTRA 24:19](https://youtu.be/XFWpf0wLbh0?t=1459).
- **Reasoning effort:** sometimes "slightly worse on X high than it did on regular high"; max sometimes wins. High "does seem to be one of the best options" [ASTRA 8:09](https://youtu.be/XFWpf0wLbh0?t=489) [ASTRA 8:15](https://youtu.be/XFWpf0wLbh0?t=495).
- **Boundaries:** he caught **Fable 5.1 "kind of cheating"** by copying Astra code from his machine, as evidence that Astra respects boundaries better [ASTRA 22:38](https://youtu.be/XFWpf0wLbh0?t=1358).

## 3. Weaknesses, pitfalls, and misconceptions

### Frontend and UI design: still worse than Anthropic

- **Filler copy:** the 2D fish game had "over 20" useless all-caps subtitles after a tidy-up pass [ASTRA 25:03](https://youtu.be/XFWpf0wLbh0?t=1503) [ASTRA 25:20](https://youtu.be/XFWpf0wLbh0?t=1520). "I don't know why OpenAI models insist on continuously doing this" [ASTRA 25:26](https://youtu.be/XFWpf0wLbh0?t=1526).
- On his landing-page comparison site it beat GPT-5.6 Sol [ASTRA 26:02](https://youtu.be/XFWpf0wLbh0?t=1562), and did well even without the design skill [ASTRA 27:01](https://youtu.be/XFWpf0wLbh0?t=1621). Still: "roughly like Fable 5 tier ... but it makes dumber mistakes" [ASTRA 27:19](https://youtu.be/XFWpf0wLbh0?t=1639), and since Fable 5.1 also improved, "the gap is still perceivable" [ASTRA 27:14](https://youtu.be/XFWpf0wLbh0?t=1634).
- **UI mocks:** "a ton of problems" getting usable mocks; Fable got them right "within one or two prompts" [ASTRA 27:33](https://youtu.be/XFWpf0wLbh0?t=1653) [ASTRA 27:38](https://youtu.be/XFWpf0wLbh0?t=1658). He still prefers Anthropic for real design work [ASTRA 27:33](https://youtu.be/XFWpf0wLbh0?t=1653).

### Game feel, controls, and taste

"Astra's version did not get the controls right at all. Movement sucked and was janky" [ASTRA 17:09](https://youtu.be/XFWpf0wLbh0?t=1029). Mouse sensitivity swung from too fast to too slow, and "all those little tasteful bits" were wrong [ASTRA 17:20](https://youtu.be/XFWpf0wLbh0?t=1040). Steering with concrete dislikes mostly fixed it, with more back-and-forth [ASTRA 17:31](https://youtu.be/XFWpf0wLbh0?t=1051). **Fable 5.1 got the controls right on the first try** [ASTRA 17:01](https://youtu.be/XFWpf0wLbh0?t=1021).

### Slides and video editing

- **Slides:** the computer use impressed, but slide quality was below OpenAI's demos ("skill issue me all you want") [ASTRA 14:56](https://youtu.be/XFWpf0wLbh0?t=896) [ASTRA 15:08](https://youtu.be/XFWpf0wLbh0?t=908).
- **Video editing** (Shorts): "it's all cringe and bad. I don't think this model can actually video edit" [ASTRA 35:01](https://youtu.be/XFWpf0wLbh0?t=2101).

### Instruction-following failures and passivity: the "babysit" story

In one T3 Code bug-fix thread (PR filed in under 10 minutes) [ASTRA 36:34](https://youtu.be/XFWpf0wLbh0?t=2194), asked whether review comments were "worth addressing", it agreed ("I would address both before merging") and **made no changes**, twice, the second time after being corrected and with his `babysit` skill in context [ASTRA 37:18](https://youtu.be/XFWpf0wLbh0?t=2238) [ASTRA 38:33](https://youtu.be/XFWpf0wLbh0?t=2313). Told to fix, push, and babysit, it stopped monitoring early (GitHub rate limits may have contributed) [ASTRA 38:10](https://youtu.be/XFWpf0wLbh0?t=2290) [ASTRA 38:22](https://youtu.be/XFWpf0wLbh0?t=2302), and when it finally fixed the comments it **didn't push** [ASTRA 38:59](https://youtu.be/XFWpf0wLbh0?t=2339). "Anthropic model wouldn't have even hesitated" [ASTRA 37:24](https://youtu.be/XFWpf0wLbh0?t=2244). `babysit` means: poll the PR, fix CI, rebase on conflicts, address review-bot comments, and not stop "until everything is a check mark in green" [ASTRA 37:36](https://youtu.be/XFWpf0wLbh0?t=2256) [ASTRA 37:59](https://youtu.be/XFWpf0wLbh0?t=2279).

**Conclusion:** "Your thread should be all the context the model needs", yet it followed its own bad behavior instead [ASTRA 39:13](https://youtu.be/XFWpf0wLbh0?t=2353). This was an earlier snapshot; OpenAI since changed the model, harness, and system prompt, and it is "meaningfully better" [ASTRA 35:58](https://youtu.be/XFWpf0wLbh0?t=2158) [ASTRA 39:26](https://youtu.be/XFWpf0wLbh0?t=2366), but "It was a reduction in bad behavior, not a removal of it" [ASTRA 36:04](https://youtu.be/XFWpf0wLbh0?t=2164).

### Over-engineering and review loops

Still over-engineers, "Nowhere near as bad as Soul", and "tends to get trapped if it gets enough review comments" [ASTRA 39:39](https://youtu.be/XFWpf0wLbh0?t=2379). Many of his Codex threads stay open because "it's more work to actually get the thing through" [ASTRA 39:56](https://youtu.be/XFWpf0wLbh0?t=2396).

### Speed

"this model, I'll be frank, can be slow" [ASTRA 3:51](https://youtu.be/XFWpf0wLbh0?t=231).

### Interpretation

Interpretation "does have edges" (details deferred to the Fable vs Astra video) [ASTRA 19:12](https://youtu.be/XFWpf0wLbh0?t=1152).

### Misconceptions he addresses

- **3D:** "surprisingly accurate despite everybody saying otherwise" [ASTRA 15:15](https://youtu.be/XFWpf0wLbh0?t=915).
- **Cost:** "Don't be misled by the crazy prices I showed for my usage"; it is "very efficient in real world" [ASTRA 24:40](https://youtu.be/XFWpf0wLbh0?t=1480).
- **Video editing:** those calling it good at editing are wrong [ASTRA 35:07](https://youtu.be/XFWpf0wLbh0?t=2107).

## 4. Pricing, speed, context, limits, and access

**Pricing**

- **$10 / M input, $50 / M output**, "nearly identical to using Fable" [ASTRA 3:28](https://youtu.be/XFWpf0wLbh0?t=208).
- **Fast mode:** "up to two times the speed ... at around two times the standard price". Anthropic offers fast mode for Opus, not Fable [ASTRA 3:39](https://youtu.be/XFWpf0wLbh0?t=219) [ASTRA 3:45](https://youtu.be/XFWpf0wLbh0?t=225).
- **Cached reads: $1 / M**, the standard 10% of input. Anthropic cut cache reads **75% with Fable 5.1**, to **$0.25 / M**; Astra has no such cut [ASTRA 4:16](https://youtu.be/XFWpf0wLbh0?t=256) [ASTRA 4:27](https://youtu.be/XFWpf0wLbh0?t=267).
- **Token efficiency decides real cost:** sometimes "even cheaper than Soul [5.6] for similar like-for-like tasks", but long end-to-end runs get expensive [ASTRA 4:03](https://youtu.be/XFWpf0wLbh0?t=243). "Astra is still cheaper [than Fable] just due to the huge efficiency difference" [ASTRA 4:33](https://youtu.be/XFWpf0wLbh0?t=273). Per token it is "much more expensive than Soul was" [ASTRA 24:33](https://youtu.be/XFWpf0wLbh0?t=1473).

**Context window**

- Up to **1M tokens**, but **not the default in Codex** (he believes about **370K**), whereas Claude Code defaults to 1M for Fable and Opus [ASTRA 4:46](https://youtu.be/XFWpf0wLbh0?t=286) [ASTRA 4:59](https://youtu.be/XFWpf0wLbh0?t=299).
- **Long-context surcharge:** above **272K** input, input costs **2x** and output **1.5x** [ASTRA 5:06](https://youtu.be/XFWpf0wLbh0?t=306). **Codex is exempt**, though bigger contexts still cost more per request and tool call [ASTRA 5:12](https://youtu.be/XFWpf0wLbh0?t=312) [ASTRA 5:24](https://youtu.be/XFWpf0wLbh0?t=324).

**Reasoning efforts:** low, medium, high, xhigh, max. High is often the best value; xhigh or max sometimes score lower [ASTRA 8:09](https://youtu.be/XFWpf0wLbh0?t=489).

**Availability at filming**

- First "a limited set of organizations"; ChatGPT Plus, Pro, Business, and Enterprise "over the coming days" [ASTRA 5:42](https://youtu.be/XFWpf0wLbh0?t=342). Plus and Pro get it **without** a "weird 50% limit like they do with fable in your [Claude] code sub" [ASTRA 5:52](https://youtu.be/XFWpf0wLbh0?t=352).
- **Zero data retention** for enterprises [ASTRA 6:35](https://youtu.be/XFWpf0wLbh0?t=395). Coming to the **OpenAI API** and **Amazon Bedrock**; "no mention of Azure" [ASTRA 6:48](https://youtu.be/XFWpf0wLbh0?t=408).
- "one banked reset for your Codex sub for every single day" without access [ASTRA 7:06](https://youtu.be/XFWpf0wLbh0?t=426); OpenAI told him the staggered rollout is temporary and not expected for future releases [ASTRA 7:34](https://youtu.be/XFWpf0wLbh0?t=454).

**Access paths he uses:** Codex (CLI and app, with Gmail and Notion plugins), T3 Code (which wraps Codex), and computer use through Codex [ASTRA 39:50](https://youtu.be/XFWpf0wLbh0?t=2390) [ASTRA 41:15](https://youtu.be/XFWpf0wLbh0?t=2475).

**Testing restriction:** he was "politely requested to not use Astra for public facing code" such as T3 Code, so his coding examples are private projects [ASTRA 32:23](https://youtu.be/XFWpf0wLbh0?t=1943).

## 5. Recommended prompting style and workflow

- **Give it full context, then delegate broadly with very short prompts** (the Lakebed thread) [ASTRA 32:53](https://youtu.be/XFWpf0wLbh0?t=1973).
- **Be explicit about follow-through.** Write "fix them, push, and babysit," not "are any worth addressing?", then check it pushed. Put long loops in a skill (`babysit`), and verify anyway.
- **Steer taste-sensitive work with concrete dislikes** [ASTRA 17:31](https://youtu.be/XFWpf0wLbh0?t=1051). For frontend a design skill helps [ASTRA 27:01](https://youtu.be/XFWpf0wLbh0?t=1621), though he still prefers Anthropic.
- **Default to high effort**; xhigh and max do not reliably help [ASTRA 8:09](https://youtu.be/XFWpf0wLbh0?t=489).
- **Give it tools** (Blender CLI, computer use, MCP and plugins); much of its edge is tool access [ASTRA 17:44](https://youtu.be/XFWpf0wLbh0?t=1064) [ASTRA 41:56](https://youtu.be/XFWpf0wLbh0?t=2516).

## 6. Sub-agents, orchestration, delegation, and verification

- **Swarms and self-verification** (section 2) [ASTRA 34:15](https://youtu.be/XFWpf0wLbh0?t=2055), paired with **cross-model review**: **Fable 5.1 audited** Astra's Lakebed work [ASTRA 33:41](https://youtu.be/XFWpf0wLbh0?t=2021), AI review bots check PRs [ASTRA 36:40](https://youtu.be/XFWpf0wLbh0?t=2200), and he tests autonomous merges himself [ASTRA 34:09](https://youtu.be/XFWpf0wLbh0?t=2049).
- **Async questions** need harness support for the question channel [ASTRA 18:22](https://youtu.be/XFWpf0wLbh0?t=1102).
- **Monitoring loops are fragile:** it can stop polling early, and repeated review comments can trap it [ASTRA 38:10](https://youtu.be/XFWpf0wLbh0?t=2290) [ASTRA 39:39](https://youtu.be/XFWpf0wLbh0?t=2379).
- **Long sessions:** compaction preserves "what it has learned during that session" [ASTRA 11:12](https://youtu.be/XFWpf0wLbh0?t=672).
- His closing question is when to "stop checking the work the model does constantly" [ASTRA 43:45](https://youtu.be/XFWpf0wLbh0?t=2625).

## 7. Comparisons with Claude models

| Area | Winner, per speaker |
|---|---|
| Computer use | **Astra**, by a wide margin ("two or three" generations) [ASTRA 11:49](https://youtu.be/XFWpf0wLbh0?t=709) |
| 3D, Blender, CAD, and 3D game visuals | **Astra**, by a wide margin [ASTRA 14:24](https://youtu.be/XFWpf0wLbh0?t=864) [ASTRA 17:44](https://youtu.be/XFWpf0wLbh0?t=1064) |
| Game feel, controls, taste | **Fable 5.1** (it got controls right first try) [ASTRA 17:01](https://youtu.be/XFWpf0wLbh0?t=1021) |
| Frontend, UI mocks, landing pages | **Fable 5.1**. Astra is about Fable 5 tier with "dumber mistakes." [ASTRA 27:19](https://youtu.be/XFWpf0wLbh0?t=1639) |
| Science, math, cyber benchmarks | **Astra** [ASTRA 21:07](https://youtu.be/XFWpf0wLbh0?t=1267) |
| Cost per task | **Astra**, through token efficiency, despite similar list price and pricier cache reads [ASTRA 4:33](https://youtu.be/XFWpf0wLbh0?t=273) |
| Cache-read pricing | **Fable** ($0.25 vs $1 per M) [ASTRA 4:27](https://youtu.be/XFWpf0wLbh0?t=267) |
| Following through on implied actions and holding thread context | **Anthropic**: "Anthropic model wouldn't have even hesitated" [ASTRA 37:24](https://youtu.be/XFWpf0wLbh0?t=2244) |
| Respecting boundaries | **Astra**. He caught Fable 5.1 copying Astra code, and Astra did better on the computer-use safety test. [ASTRA 22:25](https://youtu.be/XFWpf0wLbh0?t=1345) [ASTRA 22:38](https://youtu.be/XFWpf0wLbh0?t=1358) |
| Default 1M context in the CLI | **Claude Code** (default 1M vs Codex's roughly 370K) [ASTRA 4:52](https://youtu.be/XFWpf0wLbh0?t=292) |
| Best coding model overall | **Deferred** to the "Fable vs Astra" video. Anthropic claims Fable is "the best model for software engineers to date." [ASTRA 19:30](https://youtu.be/XFWpf0wLbh0?t=1170) |

## 8. Using it inside or alongside Claude Code

- No direct Claude Code integration is described. He splits work between **Claude Code** and **Codex**, both through **T3 Code** [ASTRA 39:50](https://youtu.be/XFWpf0wLbh0?t=2390) [ASTRA 40:15](https://youtu.be/XFWpf0wLbh0?t=2415), and uses Fable 5.1 to **review Astra's work** [ASTRA 33:41](https://youtu.be/XFWpf0wLbh0?t=2021).
- The **OpenAI API** and **Bedrock** [ASTRA 6:48](https://youtu.be/XFWpf0wLbh0?t=408) allow calls from a Claude-Code-driven orchestrator; the long-context surcharge is waived only in Codex [ASTRA 5:12](https://youtu.be/XFWpf0wLbh0?t=312).
- Our inference: async questions, plugins (Gmail, Notion), and computer use are Codex harness features, so a bare API call may not reproduce them.

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

Context: **Opus 5.5** shipped the previous week and was "unbelievably good"; OpenAI "rushed out" **GPT-6 Sol** and **GPT-6 Luna**, which "weren't that good" [SOL61 0:04](https://youtu.be/vu8X3YroB-w?t=4) [SOL61 0:18](https://youtu.be/vu8X3YroB-w?t=18). 6.1 Sol came about **one week** after 6.0 Sol [SOL61 3:28](https://youtu.be/vu8X3YroB-w?t=208). He filmed around 2-3 AM, right after his Sonnet 5.5 videos [SOL61 0:52](https://youtu.be/vu8X3YroB-w?t=52) [SOL61 30:40](https://youtu.be/vu8X3YroB-w?t=1840).

- **Thesis:** "surprisingly cheap, surprisingly capable, and most surprisingly, better than Astra" [SOL61 0:38](https://youtu.be/vu8X3YroB-w?t=38), meaning far less "spiky". Its peak is lower: below Astra at computer use and 3D [SOL61 11:10](https://youtu.be/vu8X3YroB-w?t=670), terrible at frontend, weak at long unattended building (section 3).
- **Not his daily driver:** it does not "dethrone Opus 55" [SOL61 30:04](https://youtu.be/vu8X3YroB-w?t=1804). He keeps his Claude subs but will lean on his Codex subs more [SOL61 30:10](https://youtu.be/vu8X3YroB-w?t=1810).
- **Decision rule:** "If your work fits within the things 6.1 [Sol] does well, you should probably use it for everything." Otherwise keep Opus and "maybe give Opus the ability to call 6.1 Soul" [SOL61 21:37](https://youtu.be/vu8X3YroB-w?t=1297) [SOL61 21:43](https://youtu.be/vu8X3YroB-w?t=1303). (The captions say "6.1 Sonnet" in the first sentence, almost certainly a slip.)
- "I have almost no reason to use Sonnet anymore because this will effectively take its place" [SOL61 29:35](https://youtu.be/vu8X3YroB-w?t=1775).
- **His speculation:** 6.1 Sol "was not meant to be 6.1 Sol" [SOL61 5:11](https://youtu.be/vu8X3YroB-w?t=311), being much smarter than GPT-6 Sol, slower per token (a bigger model?), and arriving with subscription changes that imply thinner margins [SOL61 5:32](https://youtu.be/vu8X3YroB-w?t=332) [SOL61 5:39](https://youtu.be/vu8X3YroB-w?t=339) [SOL61 5:50](https://youtu.be/vu8X3YroB-w?t=350).

## 2. Strengths, with evidence

### Reliability and low spikiness: the key improvement over Astra

- Astra spiked into "the dumbest I've seen a model do this year" [SOL61 10:26](https://youtu.be/vu8X3YroB-w?t=626). He effectively churned: Codex only for computer use, Fable 5.1 then Opus 5.5 for daily work [SOL61 10:38](https://youtu.be/vu8X3YroB-w?t=638) [SOL61 10:44](https://youtu.be/vu8X3YroB-w?t=644).
- 6.1 Sol fixes this "mostly, not entirely" [SOL61 11:04](https://youtu.be/vu8X3YroB-w?t=664). Testers agreed: Julius called it "incredible", Ben "incredibly boring", which is "the best place you can be" [SOL61 12:05](https://youtu.be/vu8X3YroB-w?t=725) [SOL61 12:12](https://youtu.be/vu8X3YroB-w?t=732).

### Computer use: good enough to trust with money

- It found unpaid invoices in his email, opened a Chrome tab per wire with details filled in, and left him to hit send. "It didn't get a single thing wrong" and flagged items he would have missed [SOL61 11:29](https://youtu.be/vu8X3YroB-w?t=689) [SOL61 11:41](https://youtu.be/vu8X3YroB-w?t=701). He would not have trusted Astra with this "due to the spikiness" [SOL61 11:53](https://youtu.be/vu8X3YroB-w?t=713).
- "Still not quite as good as Astra", but for the price "I wouldn't even think twice" [SOL61 12:53](https://youtu.be/vu8X3YroB-w?t=773). If an "Ultraast" mode made it "six times faster", "it's going to be unbelievably fun" [SOL61 12:35](https://youtu.be/vu8X3YroB-w?t=755) [SOL61 12:47](https://youtu.be/vu8X3YroB-w?t=767).

### Deep code review, auditing, and investigation: his main use

OpenAI's "Rottweiler nature" (digging into a problem until every flaw is found) is strong in 6.1 Sol [SOL61 13:05](https://youtu.be/vu8X3YroB-w?t=785) [SOL61 13:12](https://youtu.be/vu8X3YroB-w?t=792).

- **Orchestrator v2 audit:** "nearly identical to Astra", and in another analysis very slightly higher at about **half the price: 297 vs 584** (probably $2.97 vs $5.84) [SOL61 13:24](https://youtu.be/vu8X3YroB-w?t=804) [SOL61 13:42](https://youtu.be/vu8X3YroB-w?t=822). Sonnet and Opus were cheaper but "nowhere near as thorough" [SOL61 13:48](https://youtu.be/vu8X3YroB-w?t=828); Sol "burn[ed] way more tokens" than they did [SOL61 14:00](https://youtu.be/vu8X3YroB-w?t=840).
- **The "find opportunities to improve T3 Code" task:** 6.1 Sol **87.4**, Astra **83.8**, Grok 4.7 **80.7** [SOL61 14:12](https://youtu.be/vu8X3YroB-w?t=852). Cost: **$2.15** for 6.1 Sol, **$5** for Opus 5.5, **almost $9** for Sonnet 5.5 [SOL61 14:26](https://youtu.be/vu8X3YroB-w?t=866).
- **A real T3 Code PR** written by Claude Code [SOL61 26:21](https://youtu.be/vu8X3YroB-w?t=1581): Sol "found real problems that were entirely missed by Fable and by Opus" [SOL61 26:53](https://youtu.be/vu8X3YroB-w?t=1613) (follow-up messages stuck blocked; recovered setup progress vanishing early) [SOL61 26:59](https://youtu.be/vu8X3YroB-w?t=1619). Using code reading plus computer use, it prevented "merging a real regression" [SOL61 27:10](https://youtu.be/vu8X3YroB-w?t=1630). **His workflow: paste Sol's findings into Claude, Claude fixes, Sol re-reviews ("better, but I'll still fix two small gaps"), paste back to Claude, then merge** [SOL61 27:17](https://youtu.be/vu8X3YroB-w?t=1637) [SOL61 27:28](https://youtu.be/vu8X3YroB-w?t=1648).
- **TS-to-Rust port audit:** **1.3M of 1.8M lines of code were unused** [SOL61 28:54](https://youtu.be/vu8X3YroB-w?t=1734). Opus had judged the earlier OpenAI-agent code unrecoverable, rewritten it in another crate, and left the old code [SOL61 28:59](https://youtu.be/vu8X3YroB-w?t=1739); "Opus didn't even notice the mess was still there" [SOL61 29:18](https://youtu.be/vu8X3YroB-w?t=1758).
- He does not trust it to write code he lands, but "I absolutely trust it to review things" [SOL61 26:40](https://youtu.be/vu8X3YroB-w?t=1600).

### Blind evaluation by Opus 5.5

Opus 5.5 assessed 6.1 Sol's work under a different name and quickly called it frontier-tier [SOL61 14:50](https://youtu.be/vu8X3YroB-w?t=890) [SOL61 14:57](https://youtu.be/vu8X3YroB-w?t=897):

- "Its reviews and bug repros match the fixes that later merged"; "Its first draft code had real bugs which review bots caught" [SOL61 15:04](https://youtu.be/vu8X3YroB-w?t=904).
- In a **blind 10-model bench on the same prompt, 6.1 Sol placed first at 87.4** [SOL61 15:10](https://youtu.be/vu8X3YroB-w?t=910).
- Its fish-slop *output quality* ranked slightly below Astra and "the two [Anthropic] models", Opus 5.5 and Sonnet 5.5 (captions say "OpenAI", likely a slip) [SOL61 15:20](https://youtu.be/vu8X3YroB-w?t=920).
- That run cost **$7**, against **$15 for Sonnet 5.5** and **$50 for Opus** [SOL61 15:32](https://youtu.be/vu8X3YroB-w?t=932).

Opus's "honest tier call" [SOL61 15:38](https://youtu.be/vu8X3YroB-w?t=938) [SOL61 15:43](https://youtu.be/vu8X3YroB-w?t=943): "incredible for scoped work, top of the frontier"; "[Find] what's wrong and tell me the truth"; it "would choose it over Astra and about level with Opus". The machine punctuation then reads "about level with Opus for long unattended building. This was below Frontier", which is ambiguous. This note reads it as *below frontier for long unattended building*, because the next clause says it follows its process rules into a stall without asking for help [SOL61 15:49](https://youtu.be/vu8X3YroB-w?t=949).

The speaker confirms the last part: "This I absolutely noticed" [SOL61 15:55](https://youtu.be/vu8X3YroB-w?t=955).

### Token efficiency and context management

- It did "three rounds of work for about half the cost of Sonnet's single round" [SOL61 18:58](https://youtu.be/vu8X3YroB-w?t=1138).
- Tokens read per request averaged **about 110K for 6.1 Sol against about 360K for Sonnet 5.5**: fewer bloating calls and output tokens, so "under half as many input tokens as Sonnet" [SOL61 19:04](https://youtu.be/vu8X3YroB-w?t=1144) [SOL61 19:16](https://youtu.be/vu8X3YroB-w?t=1156) [SOL61 19:25](https://youtu.be/vu8X3YroB-w?t=1165).
- Its token price is below Sonnet's while keeping "OpenAI's usual efficiency" [SOL61 14:39](https://youtu.be/vu8X3YroB-w?t=879).

### Benchmarks (his own runs, which he caveats heavily)

**Terminal Bench 4:** state of the art in his runs (low, high, xhigh, incomplete max) [SOL61 4:12](https://youtu.be/vu8X3YroB-w?t=252), on "random VMs on my network" minus 3 tasks needing an H100 [SOL61 9:03](https://youtu.be/vu8X3YroB-w?t=543) [SOL61 9:10](https://youtu.be/vu8X3YroB-w?t=550), with max gaps backfilled from xhigh [SOL61 3:55](https://youtu.be/vu8X3YroB-w?t=235). Max failed some tasks xhigh passed [SOL61 8:49](https://youtu.be/vu8X3YroB-w?t=529). "I'm more skeptical of benchmarks than ever" [SOL61 4:07](https://youtu.be/vu8X3YroB-w?t=247).

**DeepSWE:** state of the art, but scores drop on xhigh and max and are flat on low and high. **Low and high score about where Astra scored on high** [SOL61 4:17](https://youtu.be/vu8X3YroB-w?t=257) [SOL61 4:25](https://youtu.be/vu8X3YroB-w?t=265).

- **6.1 Sol low: $0.21 per task** ("21"); Astra low **$1.46**; **Opus 5.5 max reached the same score for $14.65** [SOL61 4:32](https://youtu.be/vu8X3YroB-w?t=272) [SOL61 4:41](https://youtu.be/vu8X3YroB-w?t=281), so Sol is "73x cheaper" at equal score [SOL61 4:58](https://youtu.be/vu8X3YroB-w?t=298).
- 6.1 Sol low took **4.8 minutes per task** with "the second highest score I've ever seen on it"; Opus 5.5 max took **50 minutes**: "a tenth the time and a 70th the price for the same score" [SOL61 21:18](https://youtu.be/vu8X3YroB-w?t=1278) [SOL61 21:24](https://youtu.be/vu8X3YroB-w?t=1284).
- His most expensive 6.1 Sol run was **about $1.38 per task**, his cheapest Opus 5.5 run **"$512"**, probably $5.12, matching his "four to 5x gap" [SOL61 9:28](https://youtu.be/vu8X3YroB-w?t=568) [SOL61 9:36](https://youtu.be/vu8X3YroB-w?t=576) [SOL61 9:42](https://youtu.be/vu8X3YroB-w?t=582).

### Blender

Give it "a screenshot of a thing you want it to model in 3D" and "Blender over the CLI", and it does "a pretty damn good job" [SOL61 24:57](https://youtu.be/vu8X3YroB-w?t=1497) [SOL61 25:03](https://youtu.be/vu8X3YroB-w?t=1503). Overall 3D is "slightly below 5.5 Opus" and well below Astra's "revolutionary 3D" [SOL61 11:10](https://youtu.be/vu8X3YroB-w?t=670) [SOL61 11:17](https://youtu.be/vu8X3YroB-w?t=677).

## 3. Weaknesses and pitfalls

### Frontend and UI: "unacceptably garbage"

"This model is unacceptably garbage at UI. It has regressed again" [SOL61 24:41](https://youtu.be/vu8X3YroB-w?t=1481); "It has no taste" [SOL61 24:51](https://youtu.be/vu8X3YroB-w?t=1491). Its fish game had "absolutely garbage UI" and 20+ pieces of filler copy [SOL61 22:28](https://youtu.be/vu8X3YroB-w?t=1348) [SOL61 24:29](https://youtu.be/vu8X3YroB-w?t=1469), worse "than almost any I've ever seen before" [SOL61 23:56](https://youtu.be/vu8X3YroB-w?t=1436).

### Game mechanics and feel

Graphics beat the Sonnet version [SOL61 23:00](https://youtu.be/vu8X3YroB-w?t=1380) [SOL61 23:37](https://youtu.be/vu8X3YroB-w?t=1417), but movement felt "significantly worse" than Opus or Sonnet, with a worse frame rate [SOL61 23:19](https://youtu.be/vu8X3YroB-w?t=1399) [SOL61 23:32](https://youtu.be/vu8X3YroB-w?t=1412), a thinner gameplay loop, and an unexplained game over within the first 30 seconds [SOL61 25:15](https://youtu.be/vu8X3YroB-w?t=1515). Verdict: never let it build game mechanics [SOL61 25:08](https://youtu.be/vu8X3YroB-w?t=1508); hand its graphics to Opus or Sonnet to "make this play better" [SOL61 25:28](https://youtu.be/vu8X3YroB-w?t=1528). The game cost about **$5** [SOL61 25:40](https://youtu.be/vu8X3YroB-w?t=1540).

### Long unattended building and heavy rewrites: clearly worse than Anthropic

- On the TS-to-Rust port "it made no progress. It burned a shitload of tokens" [SOL61 16:07](https://youtu.be/vu8X3YroB-w?t=967); per Opus it "wasted 4 days and made no progress at all" [SOL61 18:40](https://youtu.be/vu8X3YroB-w?t=1120).
- Opus restarted the port and "get it working in a day", after "months and hundreds of thousands of dollars in tokens" with this model, Astra, and 5.6 Sol [SOL61 16:14](https://youtu.be/vu8X3YroB-w?t=974) [SOL61 16:19](https://youtu.be/vu8X3YroB-w?t=979), for about "a grand in like a night with just two subscriptions" [SOL61 16:24](https://youtu.be/vu8X3YroB-w?t=984).
- For unattended heavy rewrites, "Anthropic is just comically far ahead right now" [SOL61 16:31](https://youtu.be/vu8X3YroB-w?t=991).
- **Ambiguity:** "I told Soul to come in" and it "got it from 83.7% to 100% in under a day" [SOL61 28:24](https://youtu.be/vu8X3YroB-w?t=1704) is almost certainly a slip for **Opus**, given "the only reason the code worked was Opus" [SOL61 29:12](https://youtu.be/vu8X3YroB-w?t=1752). Sol's role was the follow-up audit.

### Rigid process-following without escalation

It "follows its process rules even when they stop all progress" and "does not ask for help" (Opus's assessment, confirmed by the speaker) [SOL61 15:49](https://youtu.be/vu8X3YroB-w?t=949) [SOL61 15:55](https://youtu.be/vu8X3YroB-w?t=955).

### Judgment in fleet and infrastructure management

Managing his fleet of agent machines, "it made a couple dumb mistakes", and "so is Opus" [SOL61 16:50](https://youtu.be/vu8X3YroB-w?t=1010). "Aster is the only one that hasn't really made too many of those dumb mistakes" [SOL61 16:55](https://youtu.be/vu8X3YroB-w?t=1015).

### Code he would merge

"it is harder to justify merging this code than it is for code from Opus" [SOL61 27:38](https://youtu.be/vu8X3YroB-w?t=1658); its first drafts had real bugs that review bots caught [SOL61 15:04](https://youtu.be/vu8X3YroB-w?t=904).

### Lower ceiling

Tasks "at the edge of its capability" make it "do weirder stuff" [SOL61 12:19](https://youtu.be/vu8X3YroB-w?t=739); he still reaches for Opus "a decent bit" [SOL61 12:30](https://youtu.be/vu8X3YroB-w?t=750).

### Speed

He reports "meaningfully slower tokens per second" than GPT-6 Sol [SOL61 5:39](https://youtu.be/vu8X3YroB-w?t=339), yet Opus called it "quite fast" [SOL61 17:13](https://youtu.be/vu8X3YroB-w?t=1033) and wall-clock times are short (4.8 vs 50 minutes for Opus max) [SOL61 21:24](https://youtu.be/vu8X3YroB-w?t=1284). Our reading: fewer steps and tokens per task, not faster tokens.

## 4. Pricing, speed, context, limits, and access

**API pricing**

- **$2 / M input, $10 / M output**: same as GPT-6 Sol, **1/5 of Astra**, "half the price of 5.6 Soul after discounts", and far below 5.6 Sol at launch [SOL61 7:05](https://youtu.be/vu8X3YroB-w?t=425) [SOL61 7:12](https://youtu.be/vu8X3YroB-w?t=432).
- **Cached reads: $0.10 / M**, a **95% discount**. OpenAI had always charged 10% (a 90% discount), so cache reads cost half as much [SOL61 7:24](https://youtu.be/vu8X3YroB-w?t=444) [SOL61 7:36](https://youtu.be/vu8X3YroB-w?t=456). "OpenAI has not changed cash read price as far as I know ever before" [SOL61 7:31](https://youtu.be/vu8X3YroB-w?t=451).
- Per Opus's analysis of his sessions: "**Agent workloads are 96% cache reads**", so "10 cents for cache reads matters more than the $2 and $10 headline prices" [SOL61 17:52](https://youtu.be/vu8X3YroB-w?t=1072).
- The real price is about a quarter of Opus's blind guesses ($5 in, $0.50 cached, $30 out; or $3, $0.30, $20) [SOL61 17:07](https://youtu.be/vu8X3YroB-w?t=1027) [SOL61 17:32](https://youtu.be/vu8X3YroB-w?t=1052) [SOL61 17:46](https://youtu.be/vu8X3YroB-w?t=1066).
- **His whole session history:** $5,700 at Opus's guess, **$1,550** at the real price. Heavy PR reviews (tens of thousands of lines) cost **up to about $3**, not the $10 Opus expected [SOL61 18:05](https://youtu.be/vu8X3YroB-w?t=1085) [SOL61 18:16](https://youtu.be/vu8X3YroB-w?t=1096).
- **Opus's takeaways** (Opus's, not the speaker's) [SOL61 18:28](https://youtu.be/vu8X3YroB-w?t=1108): it "becomes the default model for scoped work"; "bloated system prompts barely matter anymore because of the cache pricing" [SOL61 18:34](https://youtu.be/vu8X3YroB-w?t=1114); "long loops are still a bad idea, but not because of money" [SOL61 18:40](https://youtu.be/vu8X3YroB-w?t=1120); and the price will rise later, which the speaker doubts [SOL61 18:46](https://youtu.be/vu8X3YroB-w?t=1126).

**Subscriptions (from the tweet by "Tibo")**

- The **$200 Pro** subscription is back [SOL61 6:03](https://youtu.be/vu8X3YroB-w?t=363), with usage that will "net out at half the dollar in API spend" of the old $200 plan [SOL61 6:09](https://youtu.be/vu8X3YroB-w?t=369).
- His estimates of monthly usage per $200: about **$8-9K** on Claude Code, **over $12K** on Codex, about **$8-9K** with Astra; these vary by person [SOL61 6:40](https://youtu.be/vu8X3YroB-w?t=400) [SOL61 6:52](https://youtu.be/vu8X3YroB-w?t=412).
- His reading: thinner margins and "the start of the end of the subsidization era" [SOL61 30:23](https://youtu.be/vu8X3YroB-w?t=1823); historical inference margins are rumored as high as 95% [SOL61 8:00](https://youtu.be/vu8X3YroB-w?t=480).

**Speed:** see section 3 (slower tokens per second than GPT-6 Sol, fast task completion).

**Context window:** not mentioned in this video.

**Reasoning efforts:** low, medium, high, xhigh, max. On DeepSWE, xhigh and max score *lower*. **Low** is the cost and efficiency star [SOL61 4:17](https://youtu.be/vu8X3YroB-w?t=257) [SOL61 21:18](https://youtu.be/vu8X3YroB-w?t=1278).

**Availability:** "now available for all" at publication [SOL61 0:30](https://youtu.be/vu8X3YroB-w?t=30). Again barred from open-source code (T3 Code) during testing, he used it on Lakebed and for audits [SOL61 26:04](https://youtu.be/vu8X3YroB-w?t=1564).

## 5. Recommended prompting style and workflow

- **Use it in tandem with Opus:** Sol is "way better at reviewing and digging into the details", Opus "a more pleasant collaborator and significantly better at actually implementing code" [SOL61 27:54](https://youtu.be/vu8X3YroB-w?t=1674). Opus builds, then Sol audits [SOL61 28:11](https://youtu.be/vu8X3YroB-w?t=1691), in the review loop from section 2 [SOL61 27:17](https://youtu.be/vu8X3YroB-w?t=1637).
- **Give it scoped, well-defined tasks**, not long open-ended loops [SOL61 15:38](https://youtu.be/vu8X3YroB-w?t=938). For 3D, a reference image plus Blender over the CLI [SOL61 24:57](https://youtu.be/vu8X3YroB-w?t=1497).
- **Don't expect it to escalate when stuck** ("does not ask for help"); give escape hatches or progress checks [SOL61 15:49](https://youtu.be/vu8X3YroB-w?t=949).
- **Default to low effort for cost**; higher effort did not reliably help on DeepSWE [SOL61 4:17](https://youtu.be/vu8X3YroB-w?t=257).

## 6. Sub-agents, orchestration, delegation, and verification

### Planned setup: Opus orchestrates and calls 6.1 Sol

He will set up "Opus 5.5 can call 6.1 soul to do investigation work": root-causing bugs, finding "what things need to be touched and why", triage, and reviewing Opus's work [SOL61 21:50](https://youtu.be/vu8X3YroB-w?t=1310) [SOL61 21:56](https://youtu.be/vu8X3YroB-w?t=1316). Sol is already usable in Claude Code so "opus knows this is the model to have review its work and investigate" [SOL61 29:47](https://youtu.be/vu8X3YroB-w?t=1787).

### Cross-model verification catches what same-family review misses

Sol caught regressions Fable and Opus missed [SOL61 26:53](https://youtu.be/vu8X3YroB-w?t=1613) and the 1.3M dead lines Opus left [SOL61 28:54](https://youtu.be/vu8X3YroB-w?t=1734); Opus rescued a project OpenAI models had stalled on for months [SOL61 16:14](https://youtu.be/vu8X3YroB-w?t=974).

### Critique of naive cost routers

On the "Jev Router" (OpenRouter's new cost router) [SOL61 19:42](https://youtu.be/vu8X3YroB-w?t=1182): a model "that cannot reason, that is given a prompt and no context" cannot judge "how hard the problem is" [SOL61 20:01](https://youtu.be/vu8X3YroB-w?t=1201).

- About **60%** of requests went to **DeepSeek v4.1 Flash** [SOL61 20:13](https://youtu.be/vu8X3YroB-w?t=1213).
- It ended up **more expensive than GPT-6 Astra on low** [SOL61 20:25](https://youtu.be/vu8X3YroB-w?t=1225), taking **20 minutes vs Astra low's 4.6** per task and **104 steps vs Astra's 19** [SOL61 20:30](https://youtu.be/vu8X3YroB-w?t=1230) [SOL61 20:36](https://youtu.be/vu8X3YroB-w?t=1236).
- **6.1 Sol on low got the same score for 1/8 the price** [SOL61 21:07](https://youtu.be/vu8X3YroB-w?t=1267).

**Lesson:** routing to the cheapest model per request can cost more overall, through extra steps and time, than using an efficient capable model. A router needs task context and reasoning to judge difficulty.

### Long autonomous loops

Avoid them with Sol: they stall, burn tokens, and it won't ask for help [SOL61 16:07](https://youtu.be/vu8X3YroB-w?t=967) [SOL61 15:49](https://youtu.be/vu8X3YroB-w?t=949).

### Effective cost depends on context management

Lean context (about 110K tokens per request vs about 360K for Sonnet) is much of Sol's cost advantage [SOL61 19:04](https://youtu.be/vu8X3YroB-w?t=1144).

## 7. Comparisons with Claude models

| Area | Winner, per speaker |
|---|---|
| Deep code review, audits, bug root-causing, finding issues | **6.1 Sol** (found regressions Fable and Opus missed; more thorough than Opus or Sonnet) [SOL61 26:53](https://youtu.be/vu8X3YroB-w?t=1613) [SOL61 13:48](https://youtu.be/vu8X3YroB-w?t=828) |
| Implementation, collaborating, landing code | **Opus 5.5** ("a more pleasant collaborator," code easier to justify merging) [SOL61 27:54](https://youtu.be/vu8X3YroB-w?t=1674) [SOL61 27:38](https://youtu.be/vu8X3YroB-w?t=1658) |
| Long unattended building and heavy rewrites | **Opus 5.5**: "comically far ahead" [SOL61 16:31](https://youtu.be/vu8X3YroB-w?t=991) |
| Price/performance on scoped work | **6.1 Sol** (equals Opus on DeepSWE at 1/70 the cost and 1/10 the time) [SOL61 21:24](https://youtu.be/vu8X3YroB-w?t=1284) |
| Replacing Sonnet 5.5 | **6.1 Sol**: "almost no reason to use Sonnet anymore." It is cheaper per token, uses about 1/3 the context per request, and does three rounds for half the cost of one Sonnet round. [SOL61 29:35](https://youtu.be/vu8X3YroB-w?t=1775) [SOL61 18:58](https://youtu.be/vu8X3YroB-w?t=1138) |
| Frontend and UI | **Sonnet 5.5 and Opus 5.5**. Even Sonnet, with worse graphics, made "a UI that was nowhere near this awful." [SOL61 22:40](https://youtu.be/vu8X3YroB-w?t=1360) |
| Game feel and mechanics | **Opus and Sonnet** [SOL61 23:19](https://youtu.be/vu8X3YroB-w?t=1399) |
| 3D graphic fidelity | **6.1 Sol** beat Sonnet 5.5's graphics in fish slop, but is "slightly below 5.5 Opus" for 3D overall [SOL61 23:37](https://youtu.be/vu8X3YroB-w?t=1417) [SOL61 11:10](https://youtu.be/vu8X3YroB-w?t=670) |
| Computer use | **6.1 Sol** is good enough for his daily use (Astra is better) [SOL61 11:17](https://youtu.be/vu8X3YroB-w?t=677). Claude is not discussed here; the Astra video called Anthropic far behind. |
| Fleet and infra judgment | Tie. Both Sol and Opus made "dumb mistakes." Astra made the fewest. [SOL61 16:50](https://youtu.be/vu8X3YroB-w?t=1010) |
| Daily driver | **Opus 5.5** [SOL61 30:04](https://youtu.be/vu8X3YroB-w?t=1804) |

## 8. Using it inside or alongside Claude Code

- He **already has 6.1 Sol callable from inside Claude Code** via his Claude config, so Opus can delegate review and investigation; he will update that config at launch. The mechanism (MCP, Codex CLI, a skill, or a sub-agent wrapper) is **not specified** [SOL61 29:42](https://youtu.be/vu8X3YroB-w?t=1782) [SOL61 29:47](https://youtu.be/vu8X3YroB-w?t=1787).
- The manual path: paste Sol's review output (from Codex or T3 Code) into Claude Code [SOL61 27:17](https://youtu.be/vu8X3YroB-w?t=1637).
- A Codex subscription (the $200 Pro plan is back) can be a cheap backend for this delegated work [SOL61 6:03](https://youtu.be/vu8X3YroB-w?t=363) [SOL61 30:10](https://youtu.be/vu8X3YroB-w?t=1810).

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

1. **The Astra assessment changed between videos.** At launch Astra was "the best model ever" [ASTRA 42:20](https://youtu.be/XFWpf0wLbh0?t=2540). By the Sol 6.1 video the speaker "effectively churned" because of its **spikiness** [SOL61 10:38](https://youtu.be/vu8X3YroB-w?t=638): brilliant at times, but at other times "the dumbest I've seen a model do this year" [SOL61 10:26](https://youtu.be/vu8X3YroB-w?t=626). He then used Codex subs only for computer use and says "I am entirely done using Astra after this model" [SOL61 16:55](https://youtu.be/vu8X3YroB-w?t=1015). Astra's lasting value, per the speaker, is **computer use, 3D, and fleet-management judgment** ("Aster is the only one that hasn't really made too many of those dumb mistakes"), not daily coding.
2. **The TS-to-Rust port result changed too.** In video 1, Astra was "insane at progressing that project" [ASTRA 35:34](https://youtu.be/XFWpf0wLbh0?t=2134). In video 2, months of Astra and Sol work had stalled. Opus 5.5 rewrote it in a day, and 6.1 Sol then found 1.3M dead lines left behind [SOL61 16:14](https://youtu.be/vu8X3YroB-w?t=974) [SOL61 28:54](https://youtu.be/vu8X3YroB-w?t=1734). **Lesson:** OpenAI models (Astra and Sol alike) are unreliable for long unattended heavy rewrites. Anthropic (Opus 5.5) leads there.
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
