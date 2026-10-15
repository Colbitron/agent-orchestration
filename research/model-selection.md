# Model Selection: Research Notes from Two Videos

**Sources**

- MODELS: "Please stop using stupid models", Theo (t3.gg), YouTube, https://youtu.be/iBrAWpjXNxs
- FVA: "Fable Vs Astra Debate Is Over", Theo (t3.gg), YouTube, https://youtu.be/P7bxbDSnZRM

`[KEY m:ss]` links to that video at that timestamp. Quotes are from the auto-generated captions, so they keep the caption spellings ("soul", "codeex") listed under the caveats below.

**Speaker.** Both videos have the same speaker. He maintains **T3 Code** (an agent harness/app) [MODELS 13:33](https://youtu.be/iBrAWpjXNxs?t=813), co-hosts the "Nerd Snipe" podcast with Ben Davis [FVA 36:39](https://youtu.be/P7bxbDSnZRM?t=2199), and is a high-volume user: "nearly a billion tokens a day across both of these models" [FVA 1:10](https://youtu.be/P7bxbDSnZRM?t=70), "30 to $40,000 of inference a month" [FVA 1:10:01](https://youtu.be/P7bxbDSnZRM?t=4201), five Claude accounts and four Codex accounts [FVA 1:03:14](https://youtu.be/P7bxbDSnZRM?t=3794). The captions never say his name; the Sources block credits the channel.

**Transcription caveats. Read these before relying on model names.**

- The captions write OpenAI's previous model as "Soul", "5.6 Soul", "56 soul" and "GBD 56". This note writes it as **"Sol" (GPT-5.6 Sol)**. The transcripts never say "GPT-6.1 Sol". The second video mentions "**Astra 6.1**" only as a future release the speaker hopes for [FVA 40:16](https://youtu.be/P7bxbDSnZRM?t=2416). So if the routing project's "GPT-6.1 Sol" is a newer model than the "5.6 Sol" discussed here, **neither video covers it**.
- "GBD6 / GPD6 / GB6 Astra" means **GPT-6 Astra**. "Codeex / CEX / codec / codecs" means **Codex**. "cloud code" means **Claude Code**. "Babel / Bale / payable" means **Fable**. "cash read/write" means **cache read/write**. "Kimmy" means **Kimi**. "Flash 38" / "Gemini 38 Flash" / "Gemini 3.8 Hey, Flash" means **Gemini 3.8 Flash**.
- **"Opus" without a version:** the first video names "Opus 5" once [MODELS 4:53](https://youtu.be/iBrAWpjXNxs?t=293), and the second gives an Artificial Analysis figure for "Opus 5" [FVA 1:00:47](https://youtu.be/P7bxbDSnZRM?t=3647). **Opus 5.5, Sonnet 5.5 and Haiku 4.5 are not mentioned by version in either video.** "Sonnet" appears once, unversioned and dismissively [FVA 1:04:52](https://youtu.be/P7bxbDSnZRM?t=3892). Haiku never appears.

---

# Video 1: "Using the Right Models" (response to "you won't notice a difference going back to Opus/Sol")

## 1. Subject and thesis

**Trigger.** A post by David Kramer ("Zeg", founder of Sentry) said Fable/Astra users "should try switching back to the other high reasoning models like Opus and Soul" and would see no difference [MODELS 0:32](https://youtu.be/iBrAWpjXNxs?t=32). The speaker calls it "your worst take of all time" [MODELS 0:47](https://youtu.be/iBrAWpjXNxs?t=47) and says anyone who doesn't notice going down a gen or tier "also suck[s] at prompting" [MODELS 1:04](https://youtu.be/iBrAWpjXNxs?t=64). David K (creator of XState) said you don't need Astra, Sol or Fable for most things; the answer: "true but my time is more valuable than Fables" [MODELS 19:38](https://youtu.be/iBrAWpjXNxs?t=1178).

**Thesis.** Frontier models are valuable mainly because they **raise the floor** ("less dumb"), not the ceiling ("smarter") [MODELS 4:30](https://youtu.be/iBrAWpjXNxs?t=270). A higher floor matters most for **wide** prompts: long, multi-step, end-to-end tasks with little human input. On narrow, Jira-ticket-style prompts, older or lower-tier models clear the bar just as well [MODELS 9:17](https://youtu.be/iBrAWpjXNxs?t=557), which is why narrow prompters see no difference.

Key quotes:
- *"I like Fable because it's less dumb."* *"Less dumb and smart are almost opposites."* [MODELS 17:27](https://youtu.be/iBrAWpjXNxs?t=1047)
- *"raising the floor is way more beneficial than raising the ceiling"* [MODELS 5:50](https://youtu.be/iBrAWpjXNxs?t=350); he doesn't care about novel math *"if it doesn't know what I mean when I say revert"* [MODELS 5:57](https://youtu.be/iBrAWpjXNxs?t=357).
- People *"focus too much on the high points with models and not enough on the lows"* [MODELS 4:45](https://youtu.be/iBrAWpjXNxs?t=285)
- *"Wider prompting requires higher floors."* Width is *"the amount of things and the distance from the start to the end"*, not depth or difficulty [MODELS 8:14](https://youtu.be/iBrAWpjXNxs?t=494).
- Making a task *"wider, not harder"* raises the odds of hitting an edge where a model like Opus *"does something stupid"* [MODELS 17:10](https://youtu.be/iBrAWpjXNxs?t=1030).
- At each generation bump, he says, the time until a model is *"50% likely to have done something stupid"* *"goes down exponentially"* [MODELS 18:06](https://youtu.be/iBrAWpjXNxs?t=1086). He probably means the time *goes up*: the surrounding argument is that newer models run longer before failing, so this looks like a misstatement.

## 2. Models mentioned

| Model | What he says | Good for | Bad for / caveats |
|---|---|---|---|
| **Claude Fable (5.x)** | The high-floor model, *"less dumb"* [MODELS 17:27](https://youtu.be/iBrAWpjXNxs?t=1047). Fable and Sol arrived around May–June, and his P95 run length nearly doubled that month [MODELS 22:05](https://youtu.be/iBrAWpjXNxs?t=1325). | Wide, long-horizon, end-to-end autonomous work where one dumb step ruins the run. | Expensive; the Kramer post says "no one can afford it" [MODELS 0:40](https://youtu.be/iBrAWpjXNxs?t=40). |
| **GPT-6 Astra** | *"Astra can do things no other model in history could"* but screws up like Gemini [MODELS 3:34](https://youtu.be/iBrAWpjXNxs?t=214). *"Astra at its best can do things Fable never could"*; at its worst it makes him *"question why I'm using AI to code at all"* [MODELS 4:19](https://youtu.be/iBrAWpjXNxs?t=259). | Peak capability, e.g. a 3D environment in Blender [MODELS 5:57](https://youtu.be/iBrAWpjXNxs?t=357). | **Low, spiky floor.** Confused by "revert"; failed to "center an icon in a div" [MODELS 5:57](https://youtu.be/iBrAWpjXNxs?t=357). The *"random spikes into dumb"* make it hard to know *"what level to operate at"* [MODELS 8:46](https://youtu.be/iBrAWpjXNxs?t=526). He relabels his Astra diagram as Gemini 3.8 Flash: *"the fact that Astra can perform as poorly as Flash ever is pathetic"*; he expects a fix [MODELS 6:44](https://youtu.be/iBrAWpjXNxs?t=404). |
| **GPT-5.6 Sol ("Soul")** | Kramer's fallback "high reasoning model" [MODELS 0:40](https://youtu.be/iBrAWpjXNxs?t=40). | Moving **from Astra back to Sol** is reasonable, *"in some real cases somewhat good"* [MODELS 3:49](https://youtu.be/iBrAWpjXNxs?t=229). | He separates this from the Fable-vs-Opus case [MODELS 3:25](https://youtu.be/iBrAWpjXNxs?t=205). |
| **Opus (unversioned; "Opus 5" named once)** | Kramer's suggested downgrade from Fable. | Narrow prompts: on "here's the ticket... find the file and make this change", Opus, Fable or even Gemini won't struggle much [MODELS 7:26](https://youtu.be/iBrAWpjXNxs?t=446). He uses it during the video to analyse his own prompt/response logs because *"I got some Opus usage"* [MODELS 20:42](https://youtu.be/iBrAWpjXNxs?t=1242). | **Lower floor on wide tasks.** He was fooled by Opus 5's ceiling: it *"misbehaved far more often than I had known"* [MODELS 4:53](https://youtu.be/iBrAWpjXNxs?t=293). |
| **Gemini (generic) / Gemini 3.8 Flash** | The low-floor example: *"it'll read the same file 26 times before making a change"*, though *"it can name skateboard tricks really well"* [MODELS 5:18](https://youtu.be/iBrAWpjXNxs?t=318). A small spike is why Flash had *"those couple of good benchmarks"* [MODELS 7:00](https://youtu.be/iBrAWpjXNxs?t=420). | Nothing: *"no one should be using a Gemini thing"* [MODELS 7:09](https://youtu.be/iBrAWpjXNxs?t=429). | Very low, consistent floor. |
| **GPT-5.5 ("GBD55")** | Better with agentic stuff but *"It stopped so often"* that runs got shorter; with 5.6 *"suddenly I could let it run way longer"* [MODELS 21:03](https://youtu.be/iBrAWpjXNxs?t=1263). | — | Stops too often. |
| **Open-weight / non-Anthropic-or-OpenAI models** | The higher floor is what *"you don't get as much from open weight models and from other labs"* [MODELS 5:41](https://youtu.be/iBrAWpjXNxs?t=341). | — | Lower floors. |

He gives no per-token prices or context-window sizes for any model in this video.

## 3. Decision rules and heuristics (as literal as possible)

1. **Judge models by the floor, not the ceiling.** *"you got to think about the ceiling and the floor"* [MODELS 5:26](https://youtu.be/iBrAWpjXNxs?t=326).
2. **Narrow, well-specified task → the cheaper/older model is fine.** *"If your goal is to go from Jira ticket to code, Zeke is right"*: with files and exact behaviour listed, Claude answers *"relatively reliably"* [MODELS 9:17](https://youtu.be/iBrAWpjXNxs?t=557). In that window, Fable and Opus *"both massively clear your bar"* [MODELS 16:46](https://youtu.be/iBrAWpjXNxs?t=1006).
3. **Wide, long, end-to-end task → the frontier, high-floor model (Fable).** His example: a screenshot of a user bug plus *"Fix this. Test it. Record a video showing it works now"*, link the PR, and *"Babysit it until all the issues that come up in review are addressed"* [MODELS 9:38](https://youtu.be/iBrAWpjXNxs?t=578).
4. **Astra vs Sol is a different question from Fable vs Opus.** Falling back from Astra to Sol can be sensible because of Astra's spikiness [MODELS 3:25](https://youtu.be/iBrAWpjXNxs?t=205).
5. **When a new frontier model ships, re-baseline:** don't resend old prompts; *"start with a set that I've tried on other things that failed"* [MODELS 8:58](https://youtu.be/iBrAWpjXNxs?t=538).
6. **Two metrics to optimise:** (a) *"how long can the model run without your input?"* [MODELS 15:51](https://youtu.be/iBrAWpjXNxs?t=951) and (b) *"How likely is it that the thing works by the time a human gets involved?"* [MODELS 15:59](https://youtu.be/iBrAWpjXNxs?t=959)
7. **Fix the codebase, not just the prompt:** *"You should adjust your prompts a little, but you should adjust your codebase a lot."* If agents screw up there, *"a new dev would, too"* [MODELS 12:54](https://youtu.be/iBrAWpjXNxs?t=774). If "you know where the rough areas are", smooth them with codebase changes or by not using the model there [MODELS 14:44](https://youtu.be/iBrAWpjXNxs?t=884).
8. **Don't name files in prompts.** People who often do are "Atlassian devs" who *"have a much better time with Opus"* [MODELS 13:59](https://youtu.be/iBrAWpjXNxs?t=839). Instead, *"tell it what the problem is and tell it to find the files"* [MODELS 14:52](https://youtu.be/iBrAWpjXNxs?t=892).
9. **Push verification and delivery to the agent:** have it push the build to your phone, run it in the simulator and verify first [MODELS 15:04](https://youtu.be/iBrAWpjXNxs?t=904), or *"throw a video in the poll request so you know it worked"* [MODELS 15:18](https://youtu.be/iBrAWpjXNxs?t=918).
10. **Cheap models can cost more:** if you use dumber models because that's what you can afford, choose carefully, *"because sometimes the cheaper model ends up more expensive"* [MODELS 19:19](https://youtu.be/iBrAWpjXNxs?t=1159).
11. **Time is worth more than tokens:** a cheaper model means *"more time in before it fires and more time in when it stops"* [MODELS 19:47](https://youtu.be/iBrAWpjXNxs?t=1187).
12. **Stop watching the agent:** *"You guys need to stop paying so much attention to your agents."* [MODELS 11:41](https://youtu.be/iBrAWpjXNxs?t=701) He endorses the poll answer *"I only watch if the first output is horribly wrong"* [MODELS 11:49](https://youtu.be/iBrAWpjXNxs?t=709).
13. **When it goes wrong, ask why:** say what you expected and what it did instead, then ask *"What led you there?"* [MODELS 11:58](https://youtu.be/iBrAWpjXNxs?t=718) Models *"will usually indicate what signals they found"*, tools called and files read [MODELS 12:14](https://youtu.be/iBrAWpjXNxs?t=734).

### The compounding-failure math (his core quantitative argument)

His example [MODELS 22:41](https://youtu.be/iBrAWpjXNxs?t=1361): a model fails 5% of the time in any 10-minute window, so it has a 95% chance of success per window.
- **30 min:** 0.95^3, so roughly 15% fail [MODELS 22:48](https://youtu.be/iBrAWpjXNxs?t=1368).
- **1 hr:** "73%" (0.95^6 ≈ 0.735 success) [MODELS 23:04](https://youtu.be/iBrAWpjXNxs?t=1384).
- **2 hr:** "now you're at a 50% fail rate" (0.95^12 ≈ 0.54 success, so roughly 46% fail) [MODELS 23:11](https://youtu.be/iBrAWpjXNxs?t=1391).
- **4 hr:** "now you're at a 30% success" (0.95^24 ≈ 0.29) [MODELS 23:11](https://youtu.be/iBrAWpjXNxs?t=1391).

Improve the floor by 2 points to a 3% fail rate per 10 minutes, and at 4 hours you get *"only a 50% fail rate"* (0.97^24 ≈ 0.48 success) instead of about 70% [MODELS 23:28](https://youtu.be/iBrAWpjXNxs?t=1408). *"So that 2% change ends up being 20% at the time scale of 4 hours"* [MODELS 23:36](https://youtu.be/iBrAWpjXNxs?t=1416). Small cuts to the fail rate per time window exponentially increase how far a run can go [MODELS 23:59](https://youtu.be/iBrAWpjXNxs?t=1439). He clarifies that the floor itself improved maybe 10–15%; the *impact* is what's exponential [MODELS 22:29](https://youtu.be/iBrAWpjXNxs?t=1349).

### Empirical data from his own logs (he had Opus analyse it)
- **Median prompt run time** (logs only go back to March [MODELS 21:34](https://youtu.be/iBrAWpjXNxs?t=1294)): 53 s → 2 min 20 s ("more than doubled") [MODELS 21:43](https://youtu.be/iBrAWpjXNxs?t=1303).
- **P95:** "a bit under 7 minutes" → "over 16 minutes and 20 seconds" (April to now) [MODELS 21:51](https://youtu.be/iBrAWpjXNxs?t=1311).
- **Monthly P95:** March 9 min → 11 → 12 → **22 min in May–June** ("when we started to get Fable and Soul"), *"Nearly doubled month overmonth just from the new models"* [MODELS 22:05](https://youtu.be/iBrAWpjXNxs?t=1325).
- His estimates: runs average about 2x longer, the top 1% at least 10x [MODELS 21:17](https://youtu.be/iBrAWpjXNxs?t=1277); runs of 2 days straight, where an hour was hard before [MODELS 21:26](https://youtu.be/iBrAWpjXNxs?t=1286); six-hour unattended runs that merged 10 minutes after the PR [MODELS 16:30](https://youtu.be/iBrAWpjXNxs?t=990). A chat member: "5 to 15 minutes to 1 to four hours" [MODELS 22:29](https://youtu.be/iBrAWpjXNxs?t=1349).
- A few months earlier he didn't trust models to run *"more than 15 minutes"* [MODELS 20:57](https://youtu.be/iBrAWpjXNxs?t=1257).

## 4. Head-to-head comparisons

| Task | Winner | Why |
|---|---|---|
| Narrow Jira-ticket edit (files named, behaviour specified) | **Tie** (Opus ≈ Fable, even Gemini OK) | Every model clears the bar in a short window [MODELS 7:26](https://youtu.be/iBrAWpjXNxs?t=446). |
| Wide end-to-end task (screenshot → fix → test → video → PR → babysit review) | **Fable** (implied, along with frontier models generally) | A higher floor means fewer "dumb" events over a long run, and the odds compound [MODELS 17:18](https://youtu.be/iBrAWpjXNxs?t=1038). |
| Fable vs Astra overall quality distribution | **Fable for consistency; Astra for peaks** | Astra's ceiling is above Fable's, but its floor dips as low as Gemini Flash [MODELS 4:19](https://youtu.be/iBrAWpjXNxs?t=259), [MODELS 6:44](https://youtu.be/iBrAWpjXNxs?t=404). |
| Astra vs Sol | **Sol is acceptable / sometimes preferable** | Going back to Sol can be "in some real cases somewhat good" [MODELS 3:49](https://youtu.be/iBrAWpjXNxs?t=229), given Astra's random "spikes into dumb" [MODELS 8:46](https://youtu.be/iBrAWpjXNxs?t=526). |
| GPT-5.5 vs 5.6 for long runs | **5.6** | 5.5 "stopped so often" that runs got shorter [MODELS 21:03](https://youtu.be/iBrAWpjXNxs?t=1263). |

## 5. Subagents, orchestration, delegation, verification, review

- **Review by running the code (from a Greptile sponsor read):** a review orchestrator runs sandboxed subagents per hypothesis, from none to 10 as needed, and returns images or videos as proof [MODELS 2:32](https://youtu.be/iBrAWpjXNxs?t=152), [MODELS 2:40](https://youtu.be/iBrAWpjXNxs?t=160). *"Code breaks in ways that are not clearly visible just from reading code"* [MODELS 1:53](https://youtu.be/iBrAWpjXNxs?t=113).
- **Challenge to viewers:** on a big PR, have your local agent *"pull it down, play with it, test it"* [MODELS 1:31](https://youtu.be/iBrAWpjXNxs?t=91). **Verification is part of the prompt.** The agent self-verifies (test, simulator, video in the PR) before a human is pulled in (rules 3 and 9). Example: Maria's rewind-history PR, *"Maria wrote none of this PR"*, merged quickly because the model *"visualized what it changed"* [MODELS 15:26](https://youtu.be/iBrAWpjXNxs?t=926).
- **"Babysit" the PR until review issues are addressed** [MODELS 9:47](https://youtu.be/iBrAWpjXNxs?t=587): he delegates the review loop to the agent.
- **Overnight autonomous runs as a diagnostic (citing "Jamon"):** 5–10 hour runs hit codebase "speed bump[s]" faster; fix those, then work in-loop with 1–2 hour threads [MODELS 12:22](https://youtu.be/iBrAWpjXNxs?t=742). A bump hit *"once every two hours"* is hit *"two to three times every 5 hours"* [MODELS 12:38](https://youtu.be/iBrAWpjXNxs?t=758).
- **Specs don't replace a higher floor:** 48-hour runs in February needed hours of spec work and still had *"very, very high failure rates"* [MODELS 24:08](https://youtu.be/iBrAWpjXNxs?t=1448), [MODELS 24:30](https://youtu.be/iBrAWpjXNxs?t=1470); 4–8 hour runs now usually come out good [MODELS 25:08](https://youtu.be/iBrAWpjXNxs?t=1508).
- **Planning and vetting are where downgraders lose.** Leaders gave up the code in the middle but *"won't give up the things on the other side yet"* (prep before, vetting after) [MODELS 26:08](https://youtu.be/iBrAWpjXNxs?t=1568). *"They are testing the models against the thing they already stopped doing."* [MODELS 26:16](https://youtu.be/iBrAWpjXNxs?t=1576)
- **Trace review leads to skill refinement:** Maria spent *"3 to four days going over her traces and refining skills"*; now a single prompt lands a PR [MODELS 18:23](https://youtu.be/iBrAWpjXNxs?t=1103).

## 6. Claude Code / Codex specifics

- **No Claude Code or Codex settings, hooks, MCP or CLAUDE.md details** appear in this video beyond "skills" (Maria refining skills from traces [MODELS 18:23](https://youtu.be/iBrAWpjXNxs?t=1103)) and a "Vibe proxy" he uses for model access, which was "quite broken" at the time [MODELS 20:42](https://youtu.be/iBrAWpjXNxs?t=1242).
- He runs agents from **T3 Code on his phone** (screenshot → agent) [MODELS 9:38](https://youtu.be/iBrAWpjXNxs?t=578). He used Opus for log analysis because he "got some Opus usage" [MODELS 20:42](https://youtu.be/iBrAWpjXNxs?t=1242), implying Opus is leftover quota, not a primary model.

## 7. Cost management

- Most full-time devs can afford a $200 Claude sub plus a $200 Codex sub [MODELS 18:47](https://youtu.be/iBrAWpjXNxs?t=1127), which *"gets you 8 grand of Claude tokens and 12 grand of tokens from OpenAI"* [MODELS 18:55](https://youtu.be/iBrAWpjXNxs?t=1135). He acknowledges this is a lot for students, people outside Western countries, and so on [MODELS 19:11](https://youtu.be/iBrAWpjXNxs?t=1151).
- **Tokens vs salary:** if Julius is three times more productive by spending his salary in tokens, *"that's a no-brainer"*; even *"2x salary in tokens"* [MODELS 10:38](https://youtu.be/iBrAWpjXNxs?t=638).
- **Cheap model trap:** rule 10. He gives no rate-limit specifics in this video.

## 8. Draft routing table (Video 1 only)

| Task type | Recommended model | Fallback | Why (speaker) |
|---|---|---|---|
| Narrow, fully specified edit (files named, exact behaviour given; "Jira ticket → code") | Opus (cheaper tier) | Fable | "unlikely Opus or Fable or even a Gemini model is going to struggle" [MODELS 7:33](https://youtu.be/iBrAWpjXNxs?t=453); "both massively clear your bar in this window" [MODELS 16:54](https://youtu.be/iBrAWpjXNxs?t=1014). |
| Wide end-to-end autonomous task (vague report/screenshot → find files → fix → test → video → PR → babysit review) | Fable | Astra, only if the run can tolerate random failures | "Wider prompting requires higher floors" [MODELS 8:21](https://youtu.be/iBrAWpjXNxs?t=501); "I like Fable because it's less dumb" [MODELS 17:27](https://youtu.be/iBrAWpjXNxs?t=1047). |
| Long multi-hour unattended runs | Fable (highest-floor frontier model) | — (downgrading compounds failure) | 5% vs 3% per-10-min failure changes 4-hour success from about 30% to about 50% [MODELS 23:18](https://youtu.be/iBrAWpjXNxs?t=1398). |
| Peak-capability / novel work (e.g. 3D in Blender) | Astra | Fable | "Astra at its best can do things Fable never could" [MODELS 4:19](https://youtu.be/iBrAWpjXNxs?t=259). |
| Work where Astra is being erratic | Sol (GPT-5.6) | Fable | "I understand why people will be moving from Astra to soul"; going back can be "in some real cases somewhat good" [MODELS 3:49](https://youtu.be/iBrAWpjXNxs?t=229). |
| Analysing your own agent logs / prompt history (ad hoc data analysis) | Opus (spare quota) | — | "I got some Opus usage" [MODELS 20:42](https://youtu.be/iBrAWpjXNxs?t=1242). An observed choice, not a stated rule. |
| PR review / verification | An orchestrator that spawns sandboxed subagents to actually run the code (model unspecified) | — | "agents know a lot more about code when they can actually run it" [MODELS 2:01](https://youtu.be/iBrAWpjXNxs?t=121). |
| Anything | Not Gemini | — | "no one should be using a Gemini thing" [MODELS 7:09](https://youtu.be/iBrAWpjXNxs?t=429). |
| New-model evaluation | Re-run a personal set of previously-failed prompts | — | Rule 5 [MODELS 8:58](https://youtu.be/iBrAWpjXNxs?t=538). |

---

# Video 2: "Claude Fable 5.1 vs GPT-6 Astra"

## 1. Subject and thesis

A category-by-category comparison of **Claude Fable 5.1** and **GPT-6 Astra**, "the two actual models that matter" [FVA 0:13](https://youtu.be/P7bxbDSnZRM?t=13). He uses both daily and is *"doing thousands of dollars of inference a day"* with Astra [FVA 0:45](https://youtu.be/P7bxbDSnZRM?t=45).

**Bottom line:** rules 1–3 below (Fable to land code, Astra for everything else).
- Why: Fable *"writes code that is mergeable 20ish% more often"* [FVA 1:15:05](https://youtu.be/P7bxbDSnZRM?t=4505); *"its stupid spikes are way less stupid"* though its smart spikes are not quite as smart [FVA 1:15:11](https://youtu.be/P7bxbDSnZRM?t=4511). So Fable 5.1 is *"a better choice for day-to-day code stuff when cost is not a factor"* [FVA 1:15:17](https://youtu.be/P7bxbDSnZRM?t=4517).
- *"they don't replace each other, they compound each other"* [FVA 1:16:29](https://youtu.be/P7bxbDSnZRM?t=4589).
- **If forced to pick one, he picks Astra**, and would have it DM Julius to send prompts to Fable for him (a joke, but telling) [FVA 1:12:49](https://youtu.be/P7bxbDSnZRM?t=4369). Reasons: Astra's novel uses, computer use (he is currently "down a hand") [FVA 1:13:09](https://youtu.be/P7bxbDSnZRM?t=4389), and value: *"pretty much everyone who can have the codec sub probably should"* [FVA 1:16:35](https://youtu.be/P7bxbDSnZRM?t=4595).
- **Temperament rule:** if a model's stupid moments make you walk away, *"you should pay the extra money for Fable"*, *"a way more consistent, reliable model"* [FVA 1:12:25](https://youtu.be/P7bxbDSnZRM?t=4345).

**Consistency vs spikiness (recurring theme):** *"Fable's performance is generally more steady, where Astra is much spikier"* [FVA 24:54](https://youtu.be/P7bxbDSnZRM?t=1494). Fable's quality varies by *"never... more than like two points in either direction"* [FVA 1:11:42](https://youtu.be/P7bxbDSnZRM?t=4302); Astra is equally likely to amaze or to burn *"a thousand dollars for it to run in a loop"* and break his site [FVA 1:11:54](https://youtu.be/P7bxbDSnZRM?t=4314). *"Astra stresses me out more, a lot more."* [FVA 1:12:12](https://youtu.be/P7bxbDSnZRM?t=4332)

## 2. Models mentioned

### Claude Fable 5.1
- **Strengths:** code mergeability, the clear winner: *"Fable 5.1 writes way more mergeable code. It just does."* [FVA 33:33](https://youtu.be/P7bxbDSnZRM?t=2013), *"right on the edge of 10 out of 10 for mergeability"* [FVA 36:14](https://youtu.be/P7bxbDSnZRM?t=2174). Front-end/design (better, though still only about 5/10) [FVA 22:14](https://youtu.be/P7bxbDSnZRM?t=1334). Interaction and game feel: *"[Fable] can apply things more gently"* [FVA 9:46](https://youtu.be/P7bxbDSnZRM?t=586). Understanding intent. Using skills, a "huge lead": with a reasonable description, *"Fable correctly pulls it in and applies it"* [FVA 56:22](https://youtu.be/P7bxbDSnZRM?t=3382). Staying in scope. Full-stack intuition: it *"understands the consequences of edges by default slightly better"* [FVA 23:09](https://youtu.be/P7bxbDSnZRM?t=1389). Consistency.
- **Weaknesses:**
  - Computer use is decent *"when given the right tools"* but *"not even comparable"*; it has the *"weird misses"* OpenAI models have for code [FVA 11:07](https://youtu.be/P7bxbDSnZRM?t=667).
  - Science trails Astra [FVA 4:48](https://youtu.be/P7bxbDSnZRM?t=288); 3D rendering about 5/10 vs Astra's 9/10 [FVA 22:14](https://youtu.be/P7bxbDSnZRM?t=1334).
  - Writing skills: Fable falls into the slop loop *"even more"* than Astra [FVA 55:06](https://youtu.be/P7bxbDSnZRM?t=3306).
  - Can still scope-creep *"if it gets the wrong review comments at the wrong time"* [FVA 40:22](https://youtu.be/P7bxbDSnZRM?t=2422).
  - Relies on reading code, so it can miss deep bugs that need exhaustive testing [FVA 24:37](https://youtu.be/P7bxbDSnZRM?t=1477).
  - *"Fable isn't as good at strictly following instructions"*, but its misses feel less egregious [FVA 57:09](https://youtu.be/P7bxbDSnZRM?t=3429).
  - Least token-efficient model on the Artificial Analysis chart [FVA 1:02:04](https://youtu.be/P7bxbDSnZRM?t=3724). Its "security refusals" upset people, though *"Astra refuses more often"* [FVA 1:15:35](https://youtu.be/P7bxbDSnZRM?t=4535).
- **Cost:**
  - Cache read dropped from $1 to **$0.25 per million tokens** [FVA 57:50](https://youtu.be/P7bxbDSnZRM?t=3470).
  - Artificial Analysis cost per task: **$7.60** (vs Opus 5 ≈ $6, Astra $3.26) [FVA 1:00:47](https://youtu.be/P7bxbDSnZRM?t=3647).
  - Token efficiency: ~80K tokens for what Astra did in 27K [FVA 1:02:11](https://youtu.be/P7bxbDSnZRM?t=3731).
  - On Claude plans, Fable is capped at **half of the weekly limit** [FVA 1:04:20](https://youtu.be/P7bxbDSnZRM?t=3860).
  - **Terminal Bench Science 0.1:** Fable 5.1 on "XH high" scored 50%, cheaper than Fable 5 on high ($34, 25%) [FVA 4:28](https://youtu.be/P7bxbDSnZRM?t=268).
- **Speed:** *"so quick to work and actually apply changes"* [FVA 23:59](https://youtu.be/P7bxbDSnZRM?t=1439); about 5 minutes in the revert example [FVA 47:55](https://youtu.be/P7bxbDSnZRM?t=2875). **Context window:** not stated.

### GPT-6 Astra
- **Strengths:**
  - **3D rendering**, by a huge margin: "9/10" vs Fable "5" [FVA 22:14](https://youtu.be/P7bxbDSnZRM?t=1334); *"multiple generational difference"* [FVA 7:33](https://youtu.be/P7bxbDSnZRM?t=453); Blender scenes [FVA 7:54](https://youtu.be/P7bxbDSnZRM?t=474).
  - **Computer use**: *"so far ahead, it's kind of hilarious"*; *"Astra can often do tasks faster than I would have"* [FVA 11:01](https://youtu.be/P7bxbDSnZRM?t=661); he bought a Mac Mini to run it 24/7 [FVA 10:29](https://youtu.be/P7bxbDSnZRM?t=629).
  - **Science**: Terminal Bench Science 0.1, Astra **low** = 54.3% at **$11**, beating max Fable 5.1 *"at under a third the price"* [FVA 4:48](https://youtu.be/P7bxbDSnZRM?t=288).
  - **Giant rewrites / relentlessness** [FVA 25:10](https://youtu.be/P7bxbDSnZRM?t=1510); **orchestration "swarms"** [FVA 50:20](https://youtu.be/P7bxbDSnZRM?t=3020); **steering**, i.e. mid-task context injection [FVA 52:22](https://youtu.be/P7bxbDSnZRM?t=3142); **asking questions while it works** without blocking [FVA 53:13](https://youtu.be/P7bxbDSnZRM?t=3193); **self-prompting and writing skills** (slight lead) [FVA 56:42](https://youtu.be/P7bxbDSnZRM?t=3402); **copy/prose readability** (slight lead) [FVA 12:47](https://youtu.be/P7bxbDSnZRM?t=767); **token efficiency and cost** [FVA 1:01:58](https://youtu.be/P7bxbDSnZRM?t=3718).
  - Exhaustive debugging: *"Astra is the smartest model that acts like it's dumb"*; it *"quadruple confirms everything"*, especially on X high [FVA 24:30](https://youtu.be/P7bxbDSnZRM?t=1470). Bugs beyond what Fable gets from reading code, *"Astra will find it. It'll just take four times longer"* and burn more tokens [FVA 24:37](https://youtu.be/P7bxbDSnZRM?t=1477).
  - Video/AV prep via computer use (Ben Davis's Final Cut setup demo) [FVA 14:48](https://youtu.be/P7bxbDSnZRM?t=888).
- **Weaknesses:**
  - **UI and design.** *"straight up do not trust Astra with UI anything"* [FVA 14:02](https://youtu.be/P7bxbDSnZRM?t=842). It stuffs all-caps subtitles everywhere: 21 unnecessary ones on a 2D page [FVA 13:18](https://youtu.be/P7bxbDSnZRM?t=798), and "little" 15 times on one landing page [FVA 19:50](https://youtu.be/P7bxbDSnZRM?t=1190).
  - **Destroys existing UI during rewrites.** It ignored "Reuse as much UI code as possible" on the ping.gg rewrite [FVA 30:35](https://youtu.be/P7bxbDSnZRM?t=1835), while *"on ultra with one mil token context windows"*, so this was not compaction [FVA 31:32](https://youtu.be/P7bxbDSnZRM?t=1892).
  - **Scope creep by default:** *"a thousand line of code PR that should have been 50"* [FVA 40:46](https://youtu.be/P7bxbDSnZRM?t=2446).
  - **Intent and basic agent work** (the "revert" fiasco, below). **Skill use:** it ignores loaded skills on later turns; he partly blames a Codex system-prompt rule [FVA 55:43](https://youtu.be/P7bxbDSnZRM?t=3343). **Forgetful about boundaries:** it generally acts better than Fable here, but its failures are "more egregious"; he ties this to "the hugging face hack" [FVA 57:20](https://youtu.be/P7bxbDSnZRM?t=3440).
  - **Spiky floor.** It has given him *"the most bad model experiences I have had of any model this year"* [FVA 49:33](https://youtu.be/P7bxbDSnZRM?t=2973).
  - Game "feel" and interaction are worse: Astra's games *"look better on Twitter"*, Fable's *"actually feel nice to play"* [FVA 41:29](https://youtu.be/P7bxbDSnZRM?t=2489). Its 3D is like a *"sledgehammer"* [FVA 9:40](https://youtu.be/P7bxbDSnZRM?t=580).
  - Mergeability averages 6 follow-ups per PR vs Fable's 2 [FVA 33:40](https://youtu.be/P7bxbDSnZRM?t=2020). Refuses more often than Fable [FVA 1:15:35](https://youtu.be/P7bxbDSnZRM?t=4535). Stalled at 82.6% on the TS→Rust port [FVA 26:13](https://youtu.be/P7bxbDSnZRM?t=1573).
- **Cost:**
  - "Token costs ... are the same" as Fable list price, except for cache pricing [FVA 57:38](https://youtu.be/P7bxbDSnZRM?t=3458). He also says *"the input token cost is four times higher on Astra"* [FVA 1:00:56](https://youtu.be/P7bxbDSnZRM?t=3656). This contradicts "the same" and may refer to cache-read cost ($1 vs $0.25), so it is ambiguous.
  - OpenAI pricing as stated: input $10/M, cache read $1/M, **cache write $12.50/M** ("25% more expensive than a normal read"; OpenAI didn't used to charge for cache writes) [FVA 59:00](https://youtu.be/P7bxbDSnZRM?t=3540).
  - Artificial Analysis cost per task: **$3.26** (vs Sol $1.99) [FVA 1:01:14](https://youtu.be/P7bxbDSnZRM?t=3674).
  - Most token-efficient model benchmarked: **27K tokens vs Fable 5.1's ~80K** [FVA 1:02:04](https://youtu.be/P7bxbDSnZRM?t=3724).
  - **Flex** tier halves the price at the cost of no throughput guarantees [FVA 1:02:17](https://youtu.be/P7bxbDSnZRM?t=3737). Not available in Codex; he wishes it were [FVA 1:02:41](https://youtu.be/P7bxbDSnZRM?t=3761).
- **Speed:** fast at computer use [FVA 10:10](https://youtu.be/P7bxbDSnZRM?t=610). Slow, about 4x, on exhaustive debugging [FVA 24:37](https://youtu.be/P7bxbDSnZRM?t=1477). The ping rewrite took 1 hr 20 min [FVA 28:22](https://youtu.be/P7bxbDSnZRM?t=1702). "Fast" mode exists but should be avoided (see section 7). **Context:** he ran it "on ultra with one mil token context windows" [FVA 31:32](https://youtu.be/P7bxbDSnZRM?t=1892).

### GPT-5.6 Sol ("Soul") — previous OpenAI generation
- Mergeability *"in the two to three out of 10 range"* by default [FVA 35:10](https://youtu.be/P7bxbDSnZRM?t=2110). With the right review bots and tooling *"it could make working code incredibly well"* [FVA 35:18](https://youtu.be/P7bxbDSnZRM?t=2118).
- On working code, Sol and Fable 5 were *"neck andneck"* [FVA 35:28](https://youtu.be/P7bxbDSnZRM?t=2128), but Fable 5 was *"three to four times more mergeable"*, meaning 3–4x fewer post-PR fixes [FVA 35:42](https://youtu.be/P7bxbDSnZRM?t=2142).
- **Decision rule:** *"I would really only trust soul for exploratory work or things that could be verified programmatically"* [FVA 37:31](https://youtu.be/P7bxbDSnZRM?t=2251).
- Computer use was good enough for day-to-day use [FVA 10:17](https://youtu.be/P7bxbDSnZRM?t=617) and *"would do tedious things I didn't feel like doing"* [FVA 10:54](https://youtu.be/P7bxbDSnZRM?t=654).
- *"Soul would just get lost if you tried to steer it."* [FVA 54:11](https://youtu.be/P7bxbDSnZRM?t=3251)
- Full stack: it *"could act like it was doing that, but often just missed things"* [FVA 22:57](https://youtu.be/P7bxbDSnZRM?t=1377).
- TS→Rust: about 30% test pass rate vs Astra's 80%+ [FVA 25:52](https://youtu.be/P7bxbDSnZRM?t=1552).
- Artificial Analysis $1.99/task, cheaper than Astra [FVA 1:01:14](https://youtu.be/P7bxbDSnZRM?t=3674).

### Claude Fable 5 (previous Anthropic generation)
- About 3–4x more mergeable than Sol [FVA 35:42](https://youtu.be/P7bxbDSnZRM?t=2142). Astra is "roughly at, if not slightly ahead of where Fable 5 was" [FVA 35:55](https://youtu.be/P7bxbDSnZRM?t=2155).
- Outputs were sloppy to read: he *"hated Fable 5 for just reading its outputs"* [FVA 38:50](https://youtu.be/P7bxbDSnZRM?t=2330).
- Terminal Bench Science: high, $34, 25% [FVA 4:28](https://youtu.be/P7bxbDSnZRM?t=268).
- Design: *"if we switched just to Fable 5 or a similar design, gross"* [FVA 21:24](https://youtu.be/P7bxbDSnZRM?t=1284).
- *"Fable was the first model that could do that"*, i.e. understand full-stack codebases end to end [FVA 22:57](https://youtu.be/P7bxbDSnZRM?t=1377).

### Opus (unversioned) and Sonnet
- Once Fable quota runs out, *"the account is useless to me because **Opus sucks and Sonnet's hilariously bad**"* [FVA 1:04:52](https://youtu.be/P7bxbDSnZRM?t=3892). He calls the leftover non-Fable quota "the **opus pot**. It's a whole steaming smelly pot of opus" [FVA 1:04:26](https://youtu.be/P7bxbDSnZRM?t=3866), and loses that 50% every week [FVA 1:04:59](https://youtu.be/P7bxbDSnZRM?t=3899).
- Opus 5: Artificial Analysis about $6/task [FVA 1:00:47](https://youtu.be/P7bxbDSnZRM?t=3647).

### Others
- **Kimi K2 (original, non-thinking):** *"still writes the best of any model I've used"*, but is *"stupid as hell"* and rude; *"not a model you should actually use for much"* [FVA 12:08](https://youtu.be/P7bxbDSnZRM?t=728). Better prose than K3 and K2.5. Kimi K3 earlier impressed him on 3D [FVA 7:27](https://youtu.be/P7bxbDSnZRM?t=447).
- **GLM 5.3 Flash:** *"a more pleasant model to use arguably than Astra"*; it goes *"off the rails less than Astra for similar work"* [FVA 1:14:10](https://youtu.be/P7bxbDSnZRM?t=4450). He suggests it or the "open source plan" if cost is the main concern [FVA 1:14:04](https://youtu.be/P7bxbDSnZRM?t=4444).
- **Gemini 3.8 Flash, Muse Spark 1.3:** joke mentions [FVA 0:00](https://youtu.be/P7bxbDSnZRM?t=0). Flash 3.8 is "meme tier" [FVA 49:27](https://youtu.be/P7bxbDSnZRM?t=2967).
- **GPT-3:** historical comparison. AI video editing today is like *"shipping an app using GPT3"* [FVA 17:12](https://youtu.be/P7bxbDSnZRM?t=1032).

## 3. Decision rules and "use X for Y" statements

1. *"Fable is what I reach for when I'm trying to land code and Astra is what I reach for when I'm trying to use my computer."* [FVA 1:14:34](https://youtu.be/P7bxbDSnZRM?t=4474)
2. *"I will be defaulting to Fable for code and I'll be defaulting to Astra for every other thing that I do."* [FVA 1:15:24](https://youtu.be/P7bxbDSnZRM?t=4524)
3. *"Fable 5.1 is a better choice for day-to-day code stuff when cost is not a factor."* [FVA 1:15:17](https://youtu.be/P7bxbDSnZRM?t=4517)
4. **Science:** *"if your job is science, you should probably go get a codec subscription"* [FVA 5:01](https://youtu.be/P7bxbDSnZRM?t=301).
5. **3D prototypes and demos:** *"make the first prototype with Astra"*, then *"have Fable come in and clean it up"* and do the detail work [FVA 9:27](https://youtu.be/P7bxbDSnZRM?t=567).
6. **Game dev:** combine both. Astra handles 3D visuals; Fable handles interaction, animation curves, camera and movement feel [FVA 41:18](https://youtu.be/P7bxbDSnZRM?t=2478). *"if you use both of them carefully enough you can combine them"* [FVA 41:49](https://youtu.be/P7bxbDSnZRM?t=2509).
7. **Computer use:** Astra (with Codex on macOS). Fable only "when given the right tools" [FVA 11:07](https://youtu.be/P7bxbDSnZRM?t=667).
8. **UI / design / front end:** Fable. *"straight up do not trust Astra with UI anything"* [FVA 14:02](https://youtu.be/P7bxbDSnZRM?t=842). *"Astra needs a lot of help if you want a good design"* [FVA 22:26](https://youtu.be/P7bxbDSnZRM?t=1346). Turning on Anthropic's Claude Code design skill makes Astra "slightly better" [FVA 20:40](https://youtu.be/P7bxbDSnZRM?t=1240).
9. **Copywriting:** neither is good. Astra is slightly better at prose, but *"the way it spams it pisses me off too much"* to use it for copy [FVA 14:07](https://youtu.be/P7bxbDSnZRM?t=847). He still rewrites most copy himself [FVA 12:33](https://youtu.be/P7bxbDSnZRM?t=753). Astra usefully critiques Fable's copy (*"much better at recognizing the copy from Fable"*), but its proposals are weak [FVA 12:27](https://youtu.be/P7bxbDSnZRM?t=747).
10. **Default to Fable for:** *"a quick bug fix or UI changes that matter or feature improvements"* [FVA 39:30](https://youtu.be/P7bxbDSnZRM?t=2370).
11. **Rescue pattern (Astra death loop → Fable):** his *"favorite thing to use Fable 5.1 for"* [FVA 39:37](https://youtu.be/P7bxbDSnZRM?t=2377): stop the looping Astra run, hand Fable the PR and say *"Hey, make this actually land. Clean it up. Throw away whatever doesn't belong."*, adding that it may make a new branch [FVA 39:49](https://youtu.be/P7bxbDSnZRM?t=2389).
12. **Bulk rewrites with UI:** don't trust Astra to carry UI over: *"you cannot trust that UI is going to be carried over"* [FVA 32:29](https://youtu.be/P7bxbDSnZRM?t=1949). Workaround (which he doesn't want to need): append *"I expect the UI to be pixel perfect identical."*, then say any UI change means it failed the goal and must keep going until the UI looks identical [FVA 32:54](https://youtu.be/P7bxbDSnZRM?t=1974).
13. **Giant rewrites / ports with no UI (e.g. TS→Rust):** Astra, using a goal plus about 40 subagents [FVA 26:31](https://youtu.be/P7bxbDSnZRM?t=1591).
14. **Deep or hard-to-find bugs beyond what reading the code reveals:** Astra (X high), at about 4x the time and tokens [FVA 24:37](https://youtu.be/P7bxbDSnZRM?t=1477).
15. **Full-stack understanding:** "almost feels like a tie" [FVA 24:48](https://youtu.be/P7bxbDSnZRM?t=1488). Fable is faster and more intuitive; Astra is exhaustive.
16. **Scope-sensitive changes:** Fable. *"Fable takes less effort to prevent these things with than Astra does."* [FVA 40:59](https://youtu.be/P7bxbDSnZRM?t=2459) If you use Astra, tell it explicitly to "make the smallest possible changes" [FVA 40:32](https://youtu.be/P7bxbDSnZRM?t=2432) and stay in the loop [FVA 40:46](https://youtu.be/P7bxbDSnZRM?t=2446).
17. **Large orchestration and swarms:** Astra [FVA 50:20](https://youtu.be/P7bxbDSnZRM?t=3020).
18. **Mid-task steering / injecting new instructions:** Astra is best, Fable is solid, Sol gets lost [FVA 54:11](https://youtu.be/P7bxbDSnZRM?t=3251).
19. **Writing prompts for itself or other agents, and writing skills:** Astra is slightly better, but *"none of them are good at it"* [FVA 55:25](https://youtu.be/P7bxbDSnZRM?t=3325). *"Please write your skills by hand or at least audit them"* [FVA 55:12](https://youtu.be/P7bxbDSnZRM?t=3312). Warning: let agent-written skills shape the next skill and *"you end up in slop hell very fast"* [FVA 55:01](https://youtu.be/P7bxbDSnZRM?t=3301).
20. **Using skills:** Fable has a huge lead [FVA 56:42](https://youtu.be/P7bxbDSnZRM?t=3402).
21. **Honoring boundaries and refusals:** "Fable is ahead". Astra "looks and generally acts better about this", but it forgets, and its failures are more egregious [FVA 57:20](https://youtu.be/P7bxbDSnZRM?t=3440).
22. **Sol (previous gen) only for** *"exploratory work or things that could be verified programmatically"* [FVA 37:36](https://youtu.be/P7bxbDSnZRM?t=2256).
23. **Low frustration tolerance:** pay for Fable [FVA 1:12:31](https://youtu.be/P7bxbDSnZRM?t=4351).
24. **Cost is the main concern:** Codex $200 plan [FVA 1:09:49](https://youtu.be/P7bxbDSnZRM?t=4189); or the open-source plan / GLM 5.3 Flash [FVA 1:14:04](https://youtu.be/P7bxbDSnZRM?t=4444); or wait a few months, as *"this level of intelligence will be accessible at a much cheaper price"* [FVA 1:09:43](https://youtu.be/P7bxbDSnZRM?t=4183). For the $20 and $100 plans: wait for this level of intelligence to get cheaper [FVA 1:09:55](https://youtu.be/P7bxbDSnZRM?t=4195).
25. **Don't use Astra "fast" mode:** *"If you're using fast with Astro, you're probably using Astro wrong"* [FVA 1:06:22](https://youtu.be/P7bxbDSnZRM?t=3982). Be "very careful of the [ultra] button" too [FVA 1:06:16](https://youtu.be/P7bxbDSnZRM?t=3976).
26. **Never use AI for real audio/video editing yet** [FVA 17:12](https://youtu.be/P7bxbDSnZRM?t=1032), except computer-use *setup* (Astra preparing the Final Cut workspace) [FVA 15:37](https://youtu.be/P7bxbDSnZRM?t=937).
27. If Sol-to-Fable-5 was the gap that bothered you (Sol not mergeable, Fable 5 often clearing your bar), then *"you'll be totally fine with Astra"* [FVA 37:50](https://youtu.be/P7bxbDSnZRM?t=2270).

## 4. Head-to-head results

| Category | Winner | Detail |
|---|---|---|
| Science (Terminal Bench Science 0.1) | **Astra** | Astra low 54.3% / $11 vs Fable 5.1 XH-high 50% (Fable 5 high: 25% / $34) [FVA 4:28](https://youtu.be/P7bxbDSnZRM?t=268). He speculates OpenAI is better at post-training on new RL tooling/data [FVA 5:12](https://youtu.be/P7bxbDSnZRM?t=312). |
| 3D rendering | **Astra (huge)** | "biggest gap of anything here" [FVA 8:46](https://youtu.be/P7bxbDSnZRM?t=526). Fish Slop 3D: Astra is "nextG" visually [FVA 6:48](https://youtu.be/P7bxbDSnZRM?t=408) but movement is worse, the core loop less refined, and performance bad until told to fix it [FVA 7:03](https://youtu.be/P7bxbDSnZRM?t=423). Blender scenes from others (Amazon Spheres replica, demo home) [FVA 7:54](https://youtu.be/P7bxbDSnZRM?t=474). Astra 9/10, Fable 5/10 [FVA 22:14](https://youtu.be/P7bxbDSnZRM?t=1334). |
| Interaction / animation / game feel | **Fable** | "Fable is so much better at interaction in general" [FVA 9:08](https://youtu.be/P7bxbDSnZRM?t=548). |
| Game dev overall | **Fable (narrowly)** / combine | Fable catches up to Astra's 3D *"just due to the smoothness of its outputs"* [FVA 41:36](https://youtu.be/P7bxbDSnZRM?t=2496). |
| Computer use | **Astra (huge)** | Much faster than Sol [FVA 10:10](https://youtu.be/P7bxbDSnZRM?t=610); partly due to Codex macOS harness improvements [FVA 10:48](https://youtu.be/P7bxbDSnZRM?t=648). |
| Copywriting / prose | **Astra slightly**, but unusable | Subtitle spam (21 on one page) [FVA 13:18](https://youtu.be/P7bxbDSnZRM?t=798). Both are big jumps over their predecessors ("unslop baked in") [FVA 11:55](https://youtu.be/P7bxbDSnZRM?t=715). Kimi K2 is still best [FVA 12:08](https://youtu.be/P7bxbDSnZRM?t=728). |
| Audio / video | **Astra by default** | Neither is usable for editing; Astra wins on computer-use setup [FVA 17:43](https://youtu.be/P7bxbDSnZRM?t=1063). |
| Non-code overall | **Astra** | Biggest wins in 3D and computer use; science meaningful too [FVA 17:50](https://youtu.be/P7bxbDSnZRM?t=1070). |
| Front end / design | **Fable ("easy, significantly better")** | Neither is above 5/10 [FVA 22:14](https://youtu.be/P7bxbDSnZRM?t=1334). Fable one-shots "genuinely compelling" designs [FVA 21:29](https://youtu.be/P7bxbDSnZRM?t=1289); Astra spams subtitles and has cut-offs [FVA 20:21](https://youtu.be/P7bxbDSnZRM?t=1221). "good designs still require you sit there with a hammer" [FVA 21:53](https://youtu.be/P7bxbDSnZRM?t=1313). |
| Full stack | **Tie-ish** | Fable has intuition and speed; Astra tests every edge and finds deeper bugs [FVA 23:09](https://youtu.be/P7bxbDSnZRM?t=1389). "Astra really has that groundhog day feeling" [FVA 24:11](https://youtu.be/P7bxbDSnZRM?t=1451). |
| Giant rewrites | **Astra**, with a UI caveat | TS→Rust (TSGO port): Sol ~30% → Astra 80%+ in ~3 days, stalled at 82.6%, 40 subagents, not in the loop [FVA 25:52](https://youtu.be/P7bxbDSnZRM?t=1552). Also T3 Code mobile rewrite in Swift and a GPUI rebuild [FVA 27:26](https://youtu.be/P7bxbDSnZRM?t=1646). But the ping.gg rewrite threw away all UI despite instructions [FVA 31:20](https://youtu.be/P7bxbDSnZRM?t=1880). "For this reason alone, I would make a bigger gap in the rewriting capabilities" [FVA 32:19](https://youtu.be/P7bxbDSnZRM?t=1939). |
| Code mergeability | **Fable 5.1 (clear)** | 2 follow-ups from PR filed to merge vs Astra 6 [FVA 33:40](https://youtu.be/P7bxbDSnZRM?t=2020). Vibe scale: Sol 2–3/10; Fable 5 ~3–4x better than Sol; Astra ≈ Fable 5 or slightly ahead; Fable 5.1 near 10/10 [FVA 35:10](https://youtu.be/P7bxbDSnZRM?t=2110). "mergeable 20ish% more often" [FVA 1:15:05](https://youtu.be/P7bxbDSnZRM?t=4505). Ben Davis ("OpenAI's number one defender") admits Fable is better for real-world code and has 3 Claude Code accounts [FVA 36:39](https://youtu.be/P7bxbDSnZRM?t=2199), [FVA 37:04](https://youtu.be/P7bxbDSnZRM?t=2224). |
| Scope-creep management | **Fable** | Astra creeps by default, partly because review-agent reminders bloat its context [FVA 40:32](https://youtu.be/P7bxbDSnZRM?t=2432). |
| Understanding intent / basic agentic competence | **Fable (decisive)** | 150 PRs "fully yolo merged", 2 regressions, both from Astra [FVA 42:44](https://youtu.be/P7bxbDSnZRM?t=2564). The "revert" story below. |
| Orchestration | **Astra** | "Swarms" (section 5) [FVA 50:20](https://youtu.be/P7bxbDSnZRM?t=3020). |
| Steering | **Astra** | Fable "far ahead before"; Astra now has "actual new capability unlocks" [FVA 54:11](https://youtu.be/P7bxbDSnZRM?t=3251). |
| Self-prompting / skill writing | **Astra (slight)** | "none of them are good at it" [FVA 55:25](https://youtu.be/P7bxbDSnZRM?t=3325). |
| Skill using | **Fable (huge)** | Astra ignores a loaded skill on later turns [FVA 56:04](https://youtu.be/P7bxbDSnZRM?t=3364). |
| Honoring refusals / boundaries | **Fable** | Astra "looks and generally acts better about this" but is forgetful, with more egregious failures [FVA 57:20](https://youtu.be/P7bxbDSnZRM?t=3440). |
| Token cost per task / efficiency | **Astra** | $3.26 vs $7.60 per task [FVA 1:00:47](https://youtu.be/P7bxbDSnZRM?t=3647); 27K vs ~80K tokens [FVA 1:02:11](https://youtu.be/P7bxbDSnZRM?t=3731). |
| Subscription value | **Codex/Astra (~4x)** | See section 7 [FVA 1:08:10](https://youtu.be/P7bxbDSnZRM?t=4090). |
| Refusal rate | Astra refuses **more** | "Astra refuses more often" than Fable, despite the outcry over Fable's security refusals [FVA 1:15:35](https://youtu.be/P7bxbDSnZRM?t=4535). |

### The "revert" incident (intent, in detail)
The prompt said "revert" twice [FVA 44:15](https://youtu.be/P7bxbDSnZRM?t=2655): undo the PR that had replaced the marketing site's autoscroll marquee [FVA 43:13](https://youtu.be/P7bxbDSnZRM?t=2593). Astra never reverted. It served the wrong app, committed and pushed a Tailscale host change specific to his machine, and merged the PR after being told it hadn't made the changes, needing 5 corrections [FVA 46:54](https://youtu.be/P7bxbDSnZRM?t=2814), [FVA 47:29](https://youtu.be/P7bxbDSnZRM?t=2849), [FVA 48:50](https://youtu.be/P7bxbDSnZRM?t=2930). Verdict: it *"failed to do basic work as an agent"*, rather than misreading intent [FVA 49:53](https://youtu.be/P7bxbDSnZRM?t=2993). Fable 5.1, given the same prompt, found the exact PR and restored the marquee in about 5 minutes with one interruption [FVA 47:55](https://youtu.be/P7bxbDSnZRM?t=2875), [FVA 48:38](https://youtu.be/P7bxbDSnZRM?t=2918).

Caveat: the Tailscale request was a mid-task steer for Astra but part of the initial prompt for Fable [FVA 48:44](https://youtu.be/P7bxbDSnZRM?t=2924).

## 5. Subagents, orchestration, planning, verification, review

- **Astra "swarms" vs Fable's planned subagents (the key orchestration distinction):** Fable plans its subagents up front, in stages [FVA 50:26](https://youtu.be/P7bxbDSnZRM?t=3026). Astra runs a swarm whose members message each other and report back so it can re-fan the work, 40 in parallel on the TS→Rust port [FVA 50:44](https://youtu.be/P7bxbDSnZRM?t=3044), [FVA 51:50](https://youtu.be/P7bxbDSnZRM?t=3110). He thinks Codex's simpler subagent support is deliberate, leaving coordination to the model, unlike Claude Code's workflows [FVA 52:04](https://youtu.be/P7bxbDSnZRM?t=3124).
- **Steering enables orchestration:** the failure to test for is a mid-task addition ("I forgot number four") that the model does while dropping the unfinished tasks. Fable 5.1 rarely does this; Astra handles it best [FVA 52:30](https://youtu.be/P7bxbDSnZRM?t=3150), [FVA 52:48](https://youtu.be/P7bxbDSnZRM?t=3168).
- **Non-blocking questions:** Astra can ask mid-task without blocking; the answer steers a running task or restarts a finished one. It needs harness support, and T3 Code does it better than Codex [FVA 53:08](https://youtu.be/P7bxbDSnZRM?t=3188), [FVA 53:13](https://youtu.be/P7bxbDSnZRM?t=3193).
- **Self-prompting:** see rule 19; Astra still writes worse prompts than he does [FVA 54:35](https://youtu.be/P7bxbDSnZRM?t=3275).
- **Cross-model plan review:** for the ping.gg rewrite he had the model write a plan, *"and then I had it and Astra review each other's plans separately"* [FVA 28:11](https://youtu.be/P7bxbDSnZRM?t=1691). "It" is ambiguous, probably Fable. The plan was then committed to a branch in a worktree, then built [FVA 28:17](https://youtu.be/P7bxbDSnZRM?t=1697).
- **Verification loops and review bots:** mergeability is measured as how many follow-ups his AI review bots catch between PR filed and merge [FVA 33:46](https://youtu.be/P7bxbDSnZRM?t=2026). Review-agent feedback can *cause* scope creep: Astra's *"context get bloated a bit by its reminders from all these review agents"* [FVA 40:40](https://youtu.be/P7bxbDSnZRM?t=2440). Fable can bloat too with the wrong review comments at the wrong time [FVA 40:22](https://youtu.be/P7bxbDSnZRM?t=2422).
- **Enforce conventions at review time (from a Macroscope sponsor read):** an agent MD file only ensures *"that your agent knows about them, not that it's actually going to follow"* [FVA 2:03](https://youtu.be/P7bxbDSnZRM?t=123); path-scoped review agents defined in repo markdown approve only when their condition holds [FVA 2:21](https://youtu.be/P7bxbDSnZRM?t=141).
- **Model-to-model handoff:** rules 5, 9 and 11 (Astra prototype → Fable polish; Astra critiques Fable's copy; Astra death loop → Fable lands it).

## 6. Claude Code / Codex specifics

- **Claude Code workflows:** praised as "so good" and the subject of a separate video [FVA 52:04](https://youtu.be/P7bxbDSnZRM?t=3124). **Claude Code "design skill" from Anthropic:** makes Astra's front-end output "slightly better", though *"a little too quick to experiment with fonts"* [FVA 20:40](https://youtu.be/P7bxbDSnZRM?t=1240).
- **CLAUDE.md / AGENTS.md:** the prose comparison was run with "no Agent MD or Claude MD" [FVA 11:33](https://youtu.be/P7bxbDSnZRM?t=693). He wants agents to understand *"a claude MD or a skill file well enough to write good verbiage"* and says they don't yet [FVA 54:49](https://youtu.be/P7bxbDSnZRM?t=3289).
- **Skills:** write them by hand or audit them (rule 19); Fable reliably pulls in a skill with a reasonable description [FVA 56:22](https://youtu.be/P7bxbDSnZRM?t=3382).
  - Codex has *"a system prompt section around how skill should be applied"*: a skill used in one turn should not apply to later turns unless requested [FVA 55:43](https://youtu.be/P7bxbDSnZRM?t=3343). He thinks this is why Astra dropped his "babysitting" skill for 5 follow-ups while it was still in context [FVA 56:04](https://youtu.be/P7bxbDSnZRM?t=3364). *"I honestly think a lot of it is codeex."* [FVA 56:27](https://youtu.be/P7bxbDSnZRM?t=3387)
- **Codex modes and buttons:** "work mode" vs "codeex mode" (in work mode he couldn't open a terminal) [FVA 28:28](https://youtu.be/P7bxbDSnZRM?t=1708); "ultra" [FVA 31:32](https://youtu.be/P7bxbDSnZRM?t=1892), "X high" reasoning [FVA 24:30](https://youtu.be/P7bxbDSnZRM?t=1470) and "Astra on low" for science [FVA 4:48](https://youtu.be/P7bxbDSnZRM?t=288); "fast" (avoid it) [FVA 1:06:16](https://youtu.be/P7bxbDSnZRM?t=3976); "full access" permissions [FVA 25:47](https://youtu.be/P7bxbDSnZRM?t=1547).
  - "goal": Astra "paused the goal again" and he re-prompted *"You have my permission to do whatever you need to do."* plus *"I have you on full access for a reason. Keep going."* [FVA 25:40](https://youtu.be/P7bxbDSnZRM?t=1540)
  - Unbounded subagents: *"two ult running with unbounded sub agents. It's 40 sub agents each can run."* [FVA 1:05:36](https://youtu.be/P7bxbDSnZRM?t=3936)
- **Codex computer use on macOS:** much of the gain comes from harness changes: faster spin-up, easier context, faster movement, better background operation [FVA 10:48](https://youtu.be/P7bxbDSnZRM?t=648).
- **CLI proxy:** set up *"because one cla account just isn't enough at all for most work"*; he rotates across accounts [FVA 1:07:12](https://youtu.be/P7bxbDSnZRM?t=4032).
- **Worktrees:** he had the model make a branch, commit the plan, and work in a worktree [FVA 28:17](https://youtu.be/P7bxbDSnZRM?t=1697). **T3 Code** implements Astra's non-blocking questions better than Codex does [FVA 53:08](https://youtu.be/P7bxbDSnZRM?t=3188).

## 7. Cost management and rate limits

- **Cache economics (his key cost point):**
  - Fable 5.1 cache reads fell from $1 to $0.25/M [FVA 57:50](https://youtu.be/P7bxbDSnZRM?t=3470), but cache reads were only about 3% of his cost, and are now about 1% [FVA 58:03](https://youtu.be/P7bxbDSnZRM?t=3483). *"Four times cheaper for 3% of your cost is a less than 1% deal."* [FVA 1:00:21](https://youtu.be/P7bxbDSnZRM?t=3621)
  - **Cache writes are over 60% of his Fable costs** [FVA 58:10](https://youtu.be/P7bxbDSnZRM?t=3490). He pays Anthropic *"more money to manage RAM for me than I am paying them to run compute"* [FVA 58:30](https://youtu.be/P7bxbDSnZRM?t=3510).
  - OpenAI now charges for cache writes at $12.50/M (input $10/M, cache read $1/M) [FVA 59:09](https://youtu.be/P7bxbDSnZRM?t=3549).
  - If either lab makes *"cash rights cheap or free, they win cost by default"* [FVA 59:29](https://youtu.be/P7bxbDSnZRM?t=3569).
- **Token efficiency beats list price:** *"the actual token cost barely even matters in a world driven by token efficiency"* [FVA 59:34](https://youtu.be/P7bxbDSnZRM?t=3574). Artificial Analysis cost per task: Astra $3.26, Opus 5 ≈ $6, Fable 5.1 $7.60 [FVA 1:00:47](https://youtu.be/P7bxbDSnZRM?t=3647), Sol $1.99 [FVA 1:01:14](https://youtu.be/P7bxbDSnZRM?t=3674). Astra is *"still a fourth the price in most real world work"* [FVA 1:01:02](https://youtu.be/P7bxbDSnZRM?t=3662). On Artificial Analysis's new index, Fable 5.1 came out cheaper than Fable 5 because of the cache-read change [FVA 1:01:26](https://youtu.be/P7bxbDSnZRM?t=3686).
- **OpenAI Flex:** half price with no throughput guarantee. Good for jobs that can wait; not available in Codex [FVA 1:02:17](https://youtu.be/P7bxbDSnZRM?t=3737).
- **Subscriptions:**

  | | Claude $200 plan | Codex $200 plan |
  |---|---|---|
  | Inference value | ~$8K/month [FVA 1:03:52](https://youtu.be/P7bxbDSnZRM?t=3832) | ~$12K/month [FVA 1:03:57](https://youtu.be/P7bxbDSnZRM?t=3837) |
  | Usable on the frontier model | Only 50% for Fable (the "Opus pot" is wasted [FVA 1:04:26](https://youtu.be/P7bxbDSnZRM?t=3866)), so ~$4K, about **a third** of Codex [FVA 1:05:05](https://youtu.be/P7bxbDSnZRM?t=3905) | 100% [FVA 1:05:17](https://youtu.be/P7bxbDSnZRM?t=3917) |
  | Other cuts | Promo boost dropping from 50% to 25% means "losing around 17% off the top" [FVA 1:04:08](https://youtu.be/P7bxbDSnZRM?t=3848) | Tibo claims hosting improvements give "up to a 3 to 4x difference"; the speaker is skeptical but saw "a meaningful difference" [FVA 1:05:30](https://youtu.be/P7bxbDSnZRM?t=3930) |
  | 5-hour limit | Yes, on all plans. Each 5-hour window ≈ 40% of the Fable limit (20% of weekly), so five windows clear the weekly limit, but **only 2.5 with Fable** [FVA 1:06:58](https://youtu.be/P7bxbDSnZRM?t=4018) | **No 5-hour limits** on the $100/$200 Pro tiers; weekly only [FVA 1:06:46](https://youtu.be/P7bxbDSnZRM?t=4006) |
  | Free resets | Rare, "you can't really count on it" [FVA 1:08:56](https://youtu.be/P7bxbDSnZRM?t=4136) | Frequent: "eight free resets in the last 30 days", so the weekly limit is "more like a 3-day limit" [FVA 1:09:02](https://youtu.be/P7bxbDSnZRM?t=4142); also banked resets [FVA 1:08:32](https://youtu.be/P7bxbDSnZRM?t=4112) |
  | Felt value | — | *"four times more done with Codeex on Astra"* than with Fable and Claude Code [FVA 1:08:17](https://youtu.be/P7bxbDSnZRM?t=4097) |
  | Enough for one dev? | A few hours a day, two to three days a week, few subagents: *"you can probably get by on a single $200 plan with Claude"* [FVA 1:07:20](https://youtu.be/P7bxbDSnZRM?t=4040) | *"Most devs, when used responsibly, could absolutely get away with the $200 plan with Codex"* [FVA 1:07:38](https://youtu.be/P7bxbDSnZRM?t=4058); it falls short only with *"higher reasoning limits than necessary"* and inattention [FVA 1:07:32](https://youtu.be/P7bxbDSnZRM?t=4052) |

- **Avoid waste:** rule 25; don't use higher reasoning than necessary [FVA 1:07:32](https://youtu.be/P7bxbDSnZRM?t=4052). **Reality check:** *"Astra is cheaper than Fable, but neither are cheap"* and *"They will both burn limits fast"* [FVA 1:10:14](https://youtu.be/P7bxbDSnZRM?t=4214). For $20/$100 plans and cost-first users, see rule 24.
- **His bias:** OpenAI early access didn't count against his usage [FVA 26:49](https://youtu.be/P7bxbDSnZRM?t=1609). He ran 130 billion tokens in early access [FVA 27:08](https://youtu.be/P7bxbDSnZRM?t=1628), so he lacks a feel for how quickly Astra burns a paid account. He never had free unlimited Fable [FVA 27:15](https://youtu.be/P7bxbDSnZRM?t=1635).
- **Recommendation:** anyone who uses computers professionally and earns over $100K/year *"or your boss should be paying for the $200 a month plan"* (Codex) [FVA 1:13:23](https://youtu.be/P7bxbDSnZRM?t=4403).

## 8. Draft routing table (Video 2 only)

| Task type | Recommended model | Fallback | Why (speaker) |
|---|---|---|---|
| Day-to-day code to be merged (bug fixes, feature additions, perf improvements) | Fable 5.1 | Astra | "Fable is what I reach for when I'm trying to land code" [FVA 1:14:34](https://youtu.be/P7bxbDSnZRM?t=4474); 2 vs 6 follow-ups per PR [FVA 33:40](https://youtu.be/P7bxbDSnZRM?t=2020); "mergeable 20ish% more often" [FVA 1:15:05](https://youtu.be/P7bxbDSnZRM?t=4505). |
| Quick bug fix | Fable 5.1 | Astra | "defaulting to Fable for things like a quick bug fix" [FVA 39:30](https://youtu.be/P7bxbDSnZRM?t=2370). |
| UI changes that matter / front-end design | Fable 5.1 (+ Claude Code design skill) | Astra + design skill, with heavy iteration | "Fable takes the cake here easy" [FVA 21:53](https://youtu.be/P7bxbDSnZRM?t=1313); "do not trust Astra with UI anything" [FVA 14:02](https://youtu.be/P7bxbDSnZRM?t=842). |
| Landing pages / one-shot designs | Fable 5.1 | — | Fable 5.1's one-shot "screams like custommade" [FVA 21:34](https://youtu.be/P7bxbDSnZRM?t=1294). |
| Rescuing a stuck/looping Astra task | Fable 5.1 ("make this actually land") | — | His "favorite thing to use Fable 5.1 for" [FVA 39:37](https://youtu.be/P7bxbDSnZRM?t=2377). |
| Scope-sensitive minimal diffs | Fable 5.1 | Astra with an explicit "smallest possible changes" instruction plus a human in the loop | Astra scope-creeps "by default" [FVA 40:27](https://youtu.be/P7bxbDSnZRM?t=2427). |
| Reverts / intent-sensitive small fixes | Fable 5.1 | — | The "revert" incident [FVA 44:21](https://youtu.be/P7bxbDSnZRM?t=2661). |
| Tasks relying on skills (e.g. a "babysit PR" skill) | Fable 5.1 | — | "Skill using. Fable has a huge lead." [FVA 56:42](https://youtu.be/P7bxbDSnZRM?t=3402) |
| Tasks with strict boundaries / refusals to honor | Fable 5.1 | — | "Fable is ahead"; Astra generally acts better but forgets, and its failures are more egregious [FVA 57:20](https://youtu.be/P7bxbDSnZRM?t=3440). |
| Giant rewrites / language ports with no UI (TS→Rust) | Astra (goal + ~40 subagents, ultra) | Fable to land and clean up | Sol ~30% → Astra 80%+ [FVA 25:52](https://youtu.be/P7bxbDSnZRM?t=1552); "relentlessness" [FVA 25:10](https://youtu.be/P7bxbDSnZRM?t=1510). |
| Rewrites/ports involving existing UI | Fable 5.1 (or Astra with explicit pixel-perfect constraint, then Fable cleanup) | — | Astra "would just blanket over destroy the existing UI" [FVA 31:54](https://youtu.be/P7bxbDSnZRM?t=1914). |
| Deep / elusive bugs not visible from reading code | Astra (X high) | Fable first, for speed | "Astra will find it. It'll just take four times longer." [FVA 24:42](https://youtu.be/P7bxbDSnZRM?t=1482) |
| Full-stack feature work | Fable 5.1 (faster) | Astra (more exhaustive) | "almost feels like a tie" [FVA 24:48](https://youtu.be/P7bxbDSnZRM?t=1488). |
| Large-scale orchestration / swarms / many parallel agents with inter-agent messaging | Astra | Fable (planned, staged subagents) | "I've never seen anything else like it" [FVA 50:57](https://youtu.be/P7bxbDSnZRM?t=3057). |
| Tasks needing frequent mid-run steering | Astra | Fable 5.1 | "Astra eats this" [FVA 52:54](https://youtu.be/P7bxbDSnZRM?t=3174). |
| Writing prompts for subagents / writing skills | Astra (then human audit) | Fable | "Astra is better at it slightly" [FVA 55:25](https://youtu.be/P7bxbDSnZRM?t=3325); "write your skills by hand or at least audit them" [FVA 55:12](https://youtu.be/P7bxbDSnZRM?t=3312). |
| Computer use / desktop automation / app setup | Astra (Codex on macOS) | Fable with the right tools | "computer use is so far ahead, it's kind of hilarious" [FVA 11:07](https://youtu.be/P7bxbDSnZRM?t=667). |
| Science / research-tool tasks | Astra (even on low) | Fable 5.1 XH-high | 54.3% at $11 vs 50% for Fable [FVA 4:48](https://youtu.be/P7bxbDSnZRM?t=288). |
| 3D rendering / Blender / visual prototypes | Astra | Fable | Astra 9/10 vs Fable 5/10 [FVA 22:14](https://youtu.be/P7bxbDSnZRM?t=1334). |
| 3D/game interaction, animation curves, camera, movement feel | Fable 5.1 | — | Astra's games "look better on Twitter"; Fable's "actually feel nice to play" [FVA 41:29](https://youtu.be/P7bxbDSnZRM?t=2489). |
| Game dev end to end | Astra prototype → Fable polish | — | Explicit two-stage pipeline [FVA 9:27](https://youtu.be/P7bxbDSnZRM?t=567). |
| Copywriting / user-facing prose | Human (neither is good) | Fable draft + Astra critique; never let Astra write UI copy | Astra subtitle spam [FVA 13:18](https://youtu.be/P7bxbDSnZRM?t=798); "nothing has topped Kimmy K2" (not recommended for use) [FVA 12:08](https://youtu.be/P7bxbDSnZRM?t=728). |
| Audio/video editing | Don't use AI | Astra for workspace setup via computer use | "you are doing the equivalent of shipping an app using GPT3" [FVA 17:12](https://youtu.be/P7bxbDSnZRM?t=1032). |
| Exploratory or programmatically verifiable throwaway code | Sol (GPT-5.6), the cheap option | Astra | "I would really only trust soul for exploratory work" [FVA 37:31](https://youtu.be/P7bxbDSnZRM?t=2251). |
| Batch / non-urgent jobs via API | Astra on OpenAI Flex | — | Half price, no throughput guarantee [FVA 1:02:17](https://youtu.be/P7bxbDSnZRM?t=3737). |
| Cost-constrained general use | Astra on the Codex $200 plan | GLM 5.3 Flash / open-source plan | About 4x value [FVA 1:08:10](https://youtu.be/P7bxbDSnZRM?t=4090); GLM 5.3 Flash goes "off the rails less than Astra" [FVA 1:14:17](https://youtu.be/P7bxbDSnZRM?t=4457). |
| Work for low-frustration-tolerance users | Fable 5.1 | — | "you should pay the extra money for Fable" [FVA 1:12:31](https://youtu.be/P7bxbDSnZRM?t=4351). |
| After Fable quota is exhausted | Don't fall back to Opus/Sonnet; switch accounts (CLI proxy) or to Astra | — | "Opus sucks and Sonnet's hilariously bad" [FVA 1:04:52](https://youtu.be/P7bxbDSnZRM?t=3892). |

---

# Cross-video notes (agreements and tensions)

**Agreements**
- Fable is the consistent, high-floor model. Astra is spiky, with higher peaks and much lower troughs ([MODELS 4:19](https://youtu.be/iBrAWpjXNxs?t=259), [FVA 24:54](https://youtu.be/P7bxbDSnZRM?t=1494)).
- Astra's notable failures are basic agentic and intent failures, not intelligence failures. The **same "revert" example** appears in both videos ([MODELS 5:57](https://youtu.be/iBrAWpjXNxs?t=357), [FVA 44:21](https://youtu.be/P7bxbDSnZRM?t=2661)).
- Self-verification and review loops (sandboxed review agents, videos in PRs, babysitting PRs) are central ([MODELS 15:18](https://youtu.be/iBrAWpjXNxs?t=918), [FVA 33:46](https://youtu.be/P7bxbDSnZRM?t=2026)).
- Tokens are expensive, but human time is more expensive ([MODELS 10:30](https://youtu.be/iBrAWpjXNxs?t=630), [MODELS 19:47](https://youtu.be/iBrAWpjXNxs?t=1187)).

**Tensions / disagreements**
1. **Long autonomous runs.** Video 1 argues that wide, long runs need the highest floor, and that Astra's floor is unpredictable ("you don't really know how to gauge what level to operate at") [MODELS 8:46](https://youtu.be/iBrAWpjXNxs?t=526). Video 2 uses **Astra** for its longest unattended jobs: a multi-day TS→Rust port with 40 subagents, "not in the loop" [FVA 26:31](https://youtu.be/P7bxbDSnZRM?t=1591). One reconciliation: Video 1's "wide" means end-to-end tasks that must ship clean code, while Video 2's Astra runs are measured against a test suite (programmatically verifiable). The videos don't state this, so it is an inference.
2. **Opus.** Video 1 treats Opus as adequate for narrow, well-specified tasks and uses it for log analysis. Video 2 says "Opus sucks and Sonnet's hilariously bad" and calls non-Fable quota useless [FVA 1:04:52](https://youtu.be/P7bxbDSnZRM?t=3892).
3. **Sol.** Video 1 calls moving from Astra back to Sol understandable and "in some real cases somewhat good" [MODELS 3:49](https://youtu.be/iBrAWpjXNxs?t=229). Video 2 rates Sol's mergeability 2–3/10 and trusts it only for exploratory or programmatically verifiable work [FVA 37:31](https://youtu.be/P7bxbDSnZRM?t=2251).
4. **Spend philosophy.** Video 1 says don't downgrade to save money, because your time costs more. Video 2 strongly pushes the cheaper Codex/Astra plan for value, and would choose Astra if forced to pick one. Both still say Fable is better for code when cost isn't a factor ([MODELS 19:47](https://youtu.be/iBrAWpjXNxs?t=1187), [FVA 1:08:10](https://youtu.be/P7bxbDSnZRM?t=4090), [FVA 1:12:49](https://youtu.be/P7bxbDSnZRM?t=4369), [FVA 1:15:17](https://youtu.be/P7bxbDSnZRM?t=4517)).
5. **Gemini Flash / cheap models.** Video 1 says "no one should be using a Gemini thing" and that cheaper models can cost more. Video 2 suggests GLM 5.3 Flash as a more pleasant alternative to Astra for cost-sensitive users ([MODELS 7:09](https://youtu.be/iBrAWpjXNxs?t=429), [MODELS 19:19](https://youtu.be/iBrAWpjXNxs?t=1159), [FVA 1:14:10](https://youtu.be/P7bxbDSnZRM?t=4450)).

**Gaps relevant to the routing table:** neither video covers Opus 5.5, Sonnet 5.5, Haiku 4.5 or "GPT-6.1 Sol" by name. Neither gives context-window sizes beyond Astra's "1M" mention. Neither gives guidance on cheap, fast models for subagent grunt work such as search or summarisation.
