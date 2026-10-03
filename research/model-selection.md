# Model Selection: Research Notes from Two Videos

Source transcripts (auto-generated captions, converted to plain text):

- `scratchpad/txt/using-the-right-models.clean.txt` (~34 KB)
- `scratchpad/txt/claude-fable-5-1-vs-gpt-6-astra.clean.txt` (~79 KB)

**Speaker.** Both videos have the same speaker. He is the creator/maintainer of **T3 Code** (an agent harness/app), runs the "Nerd Snipe" podcast with Ben Davis, and is a high-volume user: "nearly a billion tokens a day across both of these models", "30 to $40,000 of inference a month", five Claude accounts and four Codex accounts. The transcripts never say his name.

**Transcription caveats. Read these before relying on model names.**

- The captions write OpenAI's previous model as "Soul", "5.6 Soul", "56 soul" and "GBD 56". This note writes it as **"Sol" (GPT-5.6 Sol)**. The transcripts never say "GPT-6.1 Sol". The second video mentions "**Astra 6.1**" only as a future release the speaker hopes for. So if the routing project's "GPT-6.1 Sol" is a newer model than the "5.6 Sol" discussed here, **neither video covers it**.
- "GBD6 / GPD6 / GB6 Astra" means **GPT-6 Astra**. "Codeex / CEX / codec / codecs" means **Codex**. "cloud code" means **Claude Code**. "Babel / Bale / payable" means **Fable**. "cash read/write" means **cache read/write**. "Kimmy" means **Kimi**. "Flash 38" / "Gemini 38 Flash" / "Gemini 3.8 Hey, Flash" means **Gemini 3.8 Flash**.
- **"Opus" without a version:** the first video names "Opus 5" once, and the second gives an Artificial Analysis figure for "Opus 5". **Opus 5.5, Sonnet 5.5 and Haiku 4.5 are not mentioned by version in either video.** "Sonnet" appears once, unversioned and dismissively. Haiku never appears.

---

# Video 1: "Using the Right Models" (response to "you won't notice a difference going back to Opus/Sol")

## 1. Subject and thesis

**Trigger.** The video responds to a post by David Kramer ("Zeg", founder of Sentry): *"Everyone using Fable or Astra, which is most of us on subs because no one can afford it, should try switching back to the other high reasoning models like Opus and Soul. You'll likely realize your tasks don't perform any differently."* The speaker calls this "your worst take of all time" and says: *"if you actually think or have experienced going back a model gen or down a model tier and not notice a difference in the way you do work, you also suck at prompting."* He also names David K (creator of XState), who said "you don't need Astra, Sol or Fable for most things". The speaker answers that this is *"true but my time is more valuable than Fable's."*

**Thesis.** Frontier models are valuable mainly because they **raise the floor** (they are "less dumb"), not because they raise the ceiling (they are "smarter"). A higher floor matters most for **wide** prompts: long, multi-step, end-to-end tasks with little human input. On narrow, well-specified, Jira-ticket-style prompts, older or lower-tier models clear the bar just as well. That is why people who prompt narrowly don't see a difference.

Key quotes:
- *"I don't like Fable because it's way smarter. I like Fable because it's less dumb. And those are different things. Less dumb and smart are almost opposites."*
- *"I personally find that raising the floor is way more beneficial than raising the ceiling. I don't care if the model solves novel math problems if it doesn't know what I mean when I say revert."*
- *"Generally speaking, y'all focus too much on the high points with models and not enough on the lows."*
- *"Wider prompting requires higher floors."* "Width" here means *"not the depth, not the difficulty of the thing, but the amount of things and the distance from the start to the end."*
- *"If I make the task wider, not harder, wider, which means longer... The likelihood we hit one of those edges in something like Opus where it does something stupid goes up as time goes up."*
- *"At every generation bump, the amount of time until the model is 50% likely to have done something stupid goes down exponentially."* He probably means the time *goes up*. The surrounding argument is that newer models run longer before failing, so this looks like a misstatement.

## 2. Models mentioned

| Model | What he says | Good for | Bad for / caveats |
|---|---|---|---|
| **Claude Fable (5.x)** | The high-floor model. *"less dumb."* Fable and Sol arrived around May–June, and his P95 run length nearly doubled that month. | Wide, long-horizon, end-to-end autonomous work where a single dumb step ruins the run. | Expensive. He implies this is why people try to downgrade. |
| **GPT-6 Astra** | *"Astra can do things no other model in history could... but it can also screw up in ways I haven't seen since I last was using a Gemini model seriously."* *"Astra at its best can do things Fable never could. Astra at its worst makes me question why I'm using AI to code at all."* | Peak capability, e.g. "building a 3D environment in Blender". | **Low, spiky floor.** It got confused by the word "revert" and failed to "center an icon in a div". *"what makes Astra so annoying is the random spikes into dumb are so random and so spiky that you don't really know how to gauge what level to operate at."* He jokingly relabels his Astra quality diagram as Gemini Flash: *"the fact that Astra can perform as poorly as Flash ever is pathetic... I know for a fact they're going to fix it."* |
| **GPT-5.6 Sol ("Soul")** | Kramer lists it as a fallback "high reasoning model". | The speaker concedes that moving **from Astra back to Sol** is reasonable: *"I see why going back to soul would feel not even not bad, but in some real cases somewhat good. And I understand why people will be moving from Astra to soul."* | He separates this case from the Fable-vs-Opus case. |
| **Opus (unversioned; "Opus 5" named once)** | Kramer's suggested downgrade from Fable. | Narrow prompts. *"if your prompts are things like here's the ticket. I want you to find the file and make this change and tell me when it's done so that I can test it. Then it is unlikely Opus or Fable or even a Gemini model is going to struggle too too much."* He also uses it himself during the video: *"My Vibe proxy is quite broken. You know what? I got some Opus usage. Let's let Opus do something for once."* The task was analysing his own prompt/response history logs. | **Lower floor on wide tasks.** He says he was fooled by Opus 5's ceiling: *"I focused too much on what the best looked like for a model, things like Opus 5, and I thought it was really good when it wasn't, and it misbehaved far more often than I had known."* |
| **Gemini (generic) / Gemini 3.8 Flash** | The low-floor example. *"it'll read the same file 26 times before making a change... But sometimes it can name skateboard tricks really well."* A small spike in his diagram is *"why Flash had those couple of good benchmarks that made it look really good when it wasn't."* | Nothing endorsed. *"no one should be using a Gemini thing."* | Very low, consistent floor. |
| **GPT-5.5 ("GBD55")** | *"generally better with agentic stuff. It stopped so often that I found its runs were actually kind of shorter overall."* Session lengths went **down** with 5.5, then with 5.6 *"suddenly I could let it run way longer."* | — | Stops too often. |
| **Open-weight / non-Anthropic-or-OpenAI models** | The higher floor is *"the thing that you don't get as much from open weight models and from other labs other than anthropic and open AI generally."* | — | Lower floors. |

He gives no per-token prices or context-window sizes for any model in this video.

## 3. Decision rules and heuristics (as literal as possible)

1. **Judge models by the floor, not the ceiling.** *"you got to think about the ceiling and the floor. And we all have a bad habit of thinking too much about the ceiling."*
2. **Narrow, well-specified task → the cheaper/older model is fine.** *"If your goal is to go from Jira ticket to code, Zeke is right. If I have a well-formatted Jira ticket that lists what files the code is in and what exact behavior exists that shouldn't, I can throw that at Claude and get an answer relatively reliably."* Also: *"if your prompts look like this and the necessary bar for you is here, then yes, absolutely the difference between Fable and Opus isn't very big because both massively clear your bar in this window."*
3. **Wide, long, end-to-end task → the frontier, high-floor model (Fable).** His example prompt: a screenshot of a user bug plus *"Fix this. Test it. Record a video showing it works now and link me the PR when you're done. Babysit it until all the issues that come up in review are addressed."*
4. **Astra vs Sol is a different question from Fable vs Opus.** Falling back from Astra to Sol can be sensible because of Astra's spikiness.
5. **When a new frontier model ships, re-baseline:** *"I immediately try to reset instead of just sending the same prompts I sent before, I always start with a set that I've tried on other things that failed to see if it can succeed."*
6. **Two metrics to optimise:** (a) *"how long can the model run without your input?"* and (b) *"How likely is it that the thing works by the time a human gets involved?"*
7. **Fix the codebase, not just the prompt:** *"You should adjust your prompts a little, but you should adjust your codebase a lot. If agents are screwing up in your codebase, then a new dev would, too."* If "you know where the rough areas are", you can "smooth those out with changes to your codebase or just not using the model for those things".
8. **Don't name files in prompts.** He calls people who often do "Atlassian devs" and says they *"have a much better time with Opus and are confused about why people like... Astra so much."* Instead: *"tell it what the problem is and tell it to find the files and change them itself."*
9. **Push verification and delivery to the agent:** *"instead of telling it to let you know when it's done so you can build it on your phone, tell it to push the build to your phone... tell it to run it in the simulator first, verify it, and then push it to my phone... Or just tell it to throw a video in the pull request so you know it worked."*
10. **Cheap models can cost more:** *"If you are using the dumber models because that's what you can afford, you should be very careful which ones you use because sometimes the cheaper model ends up more expensive."*
11. **Time is worth more than tokens:** *"if I downgrade to a cheaper model I have to put more time in before it fires and more time in when it stops."*
12. **Stop watching the agent:** *"You guys need to stop paying so much attention to your agents."* He endorses a poll answer: *"I only watch if the first output is horribly wrong."*
13. **When it goes wrong, ask why:** *"I expected you to do this, but you did this other thing instead. What led you there?"* Models *"will usually indicate what signals they found and what tools they called and what files they read that led them in the wrong direction."*

### The compounding-failure math (his core quantitative argument)

His example: a model fails 5% of the time in any 10-minute window, so it has a 95% chance of success per window.
- **30 min:** 0.95^3, so roughly 15% fail.
- **1 hr:** "73%" (0.95^6 ≈ 0.735 success).
- **2 hr:** "now you're at a 50% fail rate" (0.95^12 ≈ 0.54 success, so roughly 46% fail).
- **4 hr:** "now you're at a 30% success" (0.95^24 ≈ 0.29).

Improve the floor by 2 points to a 3% fail rate per 10 minutes, and at 4 hours you get *"only a 50% fail rate"* (0.97^24 ≈ 0.48 success) instead of about 70%. *"So that 2% change ends up being 20% at the time scale of 4 hours."* Conclusion: *"When you make these small cuts to fail rates in given time windows, you exponentially increase the distance that it can run for."* He clarifies that the floor itself improved maybe 10–15%; the *impact* is what's exponential.

### Empirical data from his own logs (he had Opus analyse it)
- **Median prompt run time:** 53 s → 2 min 20 s ("more than doubled").
- **P95:** "a bit under 7 minutes" → "over 16 minutes and 20 seconds" (April to now).
- **Monthly P95:** March 9 min → 11 → 12 → **22 min in May–June** ("when we started to get Fable and Soul"), *"Nearly doubled month over month just from the new models."*
- Anecdotes: *"my agent runs averaged probably 2x longer, but the top 1% longest ones are at least 10 times longer. I've had things run for 2 days straight with no issues and I could barely get a thing to run for an hour before."* *"I have had runs go for six hours with no intervention that merged 10 minutes after I filed the PR."* A chat member: "mine went from 5 to 15 minutes to 1 to four hours."
- *"I didn't trust models to run for more than 15 minutes just a few months ago."*

## 4. Head-to-head comparisons

| Task | Winner | Why |
|---|---|---|
| Narrow Jira-ticket edit (files named, behaviour specified) | **Tie** (Opus ≈ Fable, even Gemini OK) | Every model clears the bar in a short window. |
| Wide end-to-end task (screenshot → fix → test → video → PR → babysit review) | **Fable** (implied, along with frontier models generally) | A higher floor means fewer "dumb" events over a long run, and the odds compound. |
| Fable vs Astra overall quality distribution | **Fable for consistency; Astra for peaks** | Astra's ceiling is above Fable's, but its floor dips as low as Gemini Flash. |
| Astra vs Sol | **Sol is acceptable / sometimes preferable** | Astra's random "spikes into dumb". |
| GPT-5.5 vs 5.6 for long runs | **5.6** | 5.5 "stopped so often" that runs got shorter. |

## 5. Subagents, orchestration, delegation, verification, review

- **Sponsor segment (Greptile "T-Rex"), useful as a pattern:** a *"reviewer orchestrator can spin up and run sandboxes with sub agents for whatever theories it has about what might be wrong. Some reviews might need no sandboxes, some reviews might need 10. The orchestrator will figure out what is needed to verify your changes."* It returns images and videos as proof. Principle: *"agents know a lot more about code when they can actually run it than they can possibly guess by just staring at it."* And: *"Code breaks in ways that are not clearly visible just from reading code. This is a mistake that a lot of the AI code review bots make."*
- **Challenge to viewers:** when reviewing a big PR, *"ask your agent on your machine to pull it down, play with it, test it, and make sure everything works."*
- **Verification is part of the prompt.** Have the agent self-verify (test it, run it in the simulator, record a video, attach it to the PR) before a human is pulled in. Example: Maria's PR fixing provider-history issues with rewind. *"Maria wrote none of this PR"* and it merged quickly because *"it visualized what it changed because the model did all that."*
- **"Babysit" the PR until review issues are addressed.** He delegates the review loop to the agent.
- **Overnight autonomous runs as a diagnostic (citing "Jamon"):** long 5–10 hour runs hit codebase "speed bumps" faster. Fix those, then work in-loop with 1–2 hour threads. *"If you have a speed bump in your codebase that agents hit on average once every two hours, then they'll hit on average two to three times every 5 hours."*
- **Specs and Ralph loops:** "AD guy" could run 48 hours in February, but only after *"several hours building up specs."* *"as crazy cool as Ralph loops were, the models weren't good enough at compaction or keeping track of what they've done in the past or leaving reminders of what they've tried."* *"No matter how much work you put in, the result of specking out a run and letting it go for 8 hours isn't T3 code. The result of that is cursor 2 and cursor 3 where everything broke."* Now that 4–8 hour runs are "way more likely to come out good", Cursor is stabilising.
- **Planning and vetting are where downgraders lose.** Leaders who *"struggled to give up the code in the middle... won't give up the things on the other side yet"* (the prep before and the vetting after). *"They are testing the models against the thing they already stopped doing."*
- **Trace review leads to skill refinement:** *"[Maria] spent 3 to four days going over her traces and refining skills and whatnot after seeing what the model does and doesn't do right... now she can just fire a single prompt and get a PR landed instantly."*

## 6. Claude Code / Codex specifics

- **No Claude Code or Codex settings, hooks, MCP or CLAUDE.md details** appear in this video beyond "skills" (Maria refining skills from traces) and a "Vibe proxy" he uses for model access, which was "quite broken" at the time.
- He runs agents from **T3 Code on his phone** (screenshot → agent).
- He used Opus for a log-analysis task because he "got some Opus usage". This implies he keeps Opus as leftover quota, not as a primary model.

## 7. Cost management

- *"Most full-time devs can afford a $200 sub to Claude and a $200 sub to Codex... that gets you 8 grand of Claude tokens and 12 grand of tokens from OpenAI. You got a lot of wiggle room for not a lot of money."* He acknowledges this is a lot for students, people outside Western countries, and so on.
- **Tokens vs salary:** *"despite the tokens being expensive, so are my engineers... If Julius can be three times more productive by spending his salary in tokens, that's a no-brainer. Hell, he could do 2x salary in tokens."*
- **Cheap model trap:** *"sometimes the cheaper model ends up more expensive"*, because of extra human time before and after the run.
- He gives no rate-limit specifics in this video.

## 8. Draft routing table (Video 1 only)

| Task type | Recommended model | Fallback | Why (speaker) |
|---|---|---|---|
| Narrow, fully specified edit (files named, exact behaviour given; "Jira ticket → code") | Opus (cheaper tier) | Fable | "it is unlikely Opus or Fable or even a Gemini model is going to struggle"; "both massively clear your bar in this window." |
| Wide end-to-end autonomous task (vague report/screenshot → find files → fix → test → video → PR → babysit review) | Fable | Astra, only if the run can tolerate random failures | "Wider prompting requires higher floors"; "I like Fable because it's less dumb." |
| Long multi-hour unattended runs | Fable (highest-floor frontier model) | — (downgrading compounds failure) | 5% vs 3% per-10-min failure changes 4-hour success from about 30% to about 50%. |
| Peak-capability / novel work (e.g. 3D in Blender) | Astra | Fable | "Astra at its best can do things Fable never could." |
| Work where Astra is being erratic | Sol (GPT-5.6) | Fable | "I understand why people will be moving from Astra to soul"; going back can be "in some real cases somewhat good." |
| Analysing your own agent logs / prompt history (ad hoc data analysis) | Opus (spare quota) | — | "I got some Opus usage. Let's let Opus do something for once." This is an observed choice, not a stated rule. |
| PR review / verification | An orchestrator that spawns sandboxed subagents to actually run the code (model unspecified) | — | "agents know a lot more about code when they can actually run it." |
| Anything | Not Gemini | — | "no one should be using a Gemini thing." |
| New-model evaluation | Re-run a personal set of previously-failed prompts | — | "I always start with a set that I've tried on other things that failed." |

---

# Video 2: "Claude Fable 5.1 vs GPT-6 Astra"

## 1. Subject and thesis

This is a category-by-category comparison of **Claude Fable 5.1** and **GPT-6 Astra**, "the two actual models that matter". It opens by joking about Gemini 3.8 Flash and Muse Spark 1.3. The speaker uses both daily. He was "blown away" by Fable 5.1 and calls Astra "the future": *"I'm doing thousands of dollars of inference a day with it."*

**Bottom line:**
- *"Fable is what I reach for when I'm trying to land code and Astra is what I reach for when I'm trying to use my computer."*
- *"I will be defaulting to Fable for code and I'll be defaulting to Astra for every other thing that I do."*
- *"Fable writes code that is mergeable 20ish% more often, and its stupid spikes are much less stupid. Its smart spikes are not quite as smart, but its stupid spikes are way less stupid. And for that reason alone, I think Fable 5.1 is a better choice for day-to-day code stuff when cost is not a factor."*
- *"They don't replace each other, they compound each other."*
- **If forced to pick one, he picks Astra:** *"If I had to pick one, I would pick Astra and have it write DMs to me to Julius so that he could send off the prompts using Fable for me."* (a joke, but telling). His reasons are Astra's novel uses, computer use (he is currently "down a hand") and value. *"pretty much everyone who can have the codex sub probably should because it's such an insane deal."*
- **Temperament rule:** *"If you have low tolerance for... if you leave your computer when the model does something stupid because it pissed you off so much... you should pay the extra money for Fable. You just should. It's a way more consistent, reliable model."*

**Consistency vs spikiness (recurring theme):** *"Fable's performance is generally more steady, where Astra is much spikier."* Fable's quality *"goes up and down a bit, but never... more than like two points in either direction. When I send a prompt to Astra, it's equal chances it drops my jaw because I'm so blown away... or it drops my jaw because I cannot fathom that I just spent a thousand dollars for it to run in a loop and not ship anything and then break my website."* *"Astra stresses me out more, a lot more."*

## 2. Models mentioned

### Claude Fable 5.1
- **Strengths:** code mergeability (the clear winner), front-end/design (better, though still only about 5/10), interaction and game feel, understanding intent, using skills (a "huge lead"), staying in scope, full-stack intuition, consistency.
  - *"Fable 5.1 writes way more mergeable code. It just does."*
  - *"Fable has better intuition... It understands the consequences of edges by default slightly better."*
  - *"Fable can apply things more gently."*
  - *"If the skill has a reasonable description and it's useful for the work going on, Fable correctly pulls it in and applies it."*
  - *"5.1 is like right on the edge of 10 out of 10 for mergeability."*
- **Weaknesses:**
  - Computer use is decent "when given the right tools, but it's just not even comparable". *"the weird misses that I'm used to OpenAI models having for code, it feels like Fable has those when it's doing computer use."*
  - Science benchmarks trail Astra.
  - 3D rendering about 5/10 vs Astra's 9/10.
  - Writing skills: Fable "falls into [the slop loop] even more" than Astra.
  - Can still scope-creep *"if it gets the wrong review comments at the wrong time."*
  - Relies on reading code, so it can miss deep bugs that need exhaustive testing.
  - *"Fable isn't as good at strictly following instructions, but that also means that when it doesn't follow them, it doesn't feel as egregious."*
  - Least token-efficient model on the Artificial Analysis chart.
  - Its "security refusals" upset people, though *"Astra refuses more often."*
- **Cost:**
  - Cache read dropped from $1 to **$0.25 per million tokens**.
  - Artificial Analysis cost per task: **$7.60** (vs Opus 5 ≈ $6, Astra $3.26).
  - Token efficiency: ~80K tokens for what Astra did in 27K.
  - On Claude plans, Fable is capped at **half of the weekly limit**.
  - **Terminal Bench Science 0.1:** Fable 5.1 on "XH high" scored 50%, cheaper than Fable 5 on high ($34, 25%).
- **Speed:** quick to apply changes. *"it's so quick to work and actually apply changes because it builds its understanding more effectively."* In the revert example it got it right in about 5 minutes.
- **Context window:** not stated.

### GPT-6 Astra
- **Strengths:**
  - **3D rendering**, by a huge margin ("9/10" vs Fable "5"; "multiple generational difference"; Blender scenes).
  - **Computer use** (*"so far ahead, it's kind of hilarious"*; *"Astra can often do tasks faster than I would have"*; he bought a Mac Mini to run it 24/7).
  - **Science** (Terminal Bench Science 0.1: Astra **low** = 54.3% at **$11**, beating max Fable 5.1 "at under a third the price").
  - **Giant rewrites / relentlessness.**
  - **Orchestration "swarms".**
  - **Steering**, i.e. mid-task context injection.
  - **Asking questions while it works** without blocking.
  - **Self-prompting and writing skills** (slight lead).
  - **Copy/prose readability** (slight lead).
  - **Token efficiency and cost.**
  - Exhaustive debugging. *"Astra is the smartest model that acts like it's dumb. Astra quadruple confirms everything it's trying to do, especially in X high mode. Which means if the bug is outside of what Fable can grasp just from reading code... Astra will find it. It'll just take four times longer and burn way more tokens."*
  - Video/AV prep via computer use (Ben Davis's Final Cut setup demo).
- **Weaknesses:**
  - **UI and design.** *"I... straight up do not trust Astra with UI anything at this point."* It stuffs all-caps subtitles everywhere: 21 unnecessary ones on a 2D page, and "little" 15 times on one landing page.
  - **Destroys existing UI during rewrites.** It ignored "Reuse as much UI code as possible" on the ping.gg rewrite, *"on ultra with one mil token context windows"*, so this was not compaction.
  - **Scope creep by default.** *"you end up with a thousand line of code PR that should have been 50."*
  - **Intent and basic agent work.** The "revert" fiasco.
  - **Skill use.** It ignores loaded skills on later turns. He partly blames a Codex system-prompt rule.
  - **Forgetful about boundaries.** Its failures are "more egregious"; he ties this to "the hugging face hack".
  - **Spiky floor.** *"Astra has had the most bad model experiences I have had of any model this year."*
  - Game "feel" and interaction are worse: *"Astra makes games that look better on Twitter. Fable makes games that actually feel nice to play."* Its 3D is like a *"sledgehammer."*
  - Mergeability averages 6 follow-ups per PR vs Fable's 2.
  - Refuses more often than Fable.
  - Stalled at 82.6% on the TS→Rust port.
- **Cost:**
  - "Token costs are the same" as Fable list price, except for cache pricing. He also says *"theoretically speaking, the input token cost is four times higher on Astra"*. This contradicts "the same" and may refer to cache-read cost ($1 vs $0.25), so it is ambiguous.
  - OpenAI pricing as stated: input $10/M, cache read $1/M, **cache write $12.50/M** ("25% more expensive than a normal read"; OpenAI "didn't used to charge for cache writes").
  - Artificial Analysis cost per task: **$3.26** (vs Sol $1.99).
  - Most token-efficient model benchmarked: **27K tokens vs Fable 5.1's ~80K**.
  - **Flex** tier halves the price at the cost of no throughput guarantees. Not available in Codex; he wishes it were.
- **Speed:** fast at computer use. Slow, about 4x, on exhaustive debugging. The ping rewrite took 1 hr 20 min. "Fast" mode exists but should be avoided (see section 7).
- **Context:** he ran it "on ultra with one mil token context windows".

### GPT-5.6 Sol ("Soul") — previous OpenAI generation
- Mergeability *"in the two to three out of 10 range... by default."* With the right review bots and tooling *"it could make working code incredibly well."*
- *"If we were just measuring the ability for Soul and Fable 5 to get working code, they were neck and neck."* But Fable 5 was *"three to four times more mergeable"*, meaning 3–4x fewer post-PR fixes.
- **Decision rule:** *"I would really only trust soul for exploratory work or things that could be verified programmatically where the code didn't matter that much in terms of its quality and maintainability."*
- Computer use was good enough for day-to-day use and *"would do tedious things I didn't feel like doing."*
- *"Soul would just get lost if you tried to steer it."*
- Full stack: it *"could act like it was doing that, but often just missed things."*
- TS→Rust: about 30% test pass rate vs Astra's 80%+.
- Artificial Analysis $1.99/task, cheaper than Astra.

### Claude Fable 5 (previous Anthropic generation)
- About 3–4x more mergeable than Sol. Astra is "roughly at, if not slightly ahead of where Fable 5 was."
- Outputs were sloppy to read: *"I don't hate it the same way I hated Fable 5 for just reading its outputs."*
- Terminal Bench Science: high, $34, 25%.
- Design: *"if we switched just to Fable 5 or a similar design, gross."*
- *"Fable was the first model that could [understand full-stack codebases end to end]."*

### Opus (unversioned) and Sonnet
- *"once I'm out of Fable, the account is useless to me because **Opus sucks and Sonnet's hilariously bad**."* He calls the leftover non-Fable quota "the **opus pot**. It's a whole steaming smelly pot of opus." He loses that 50% every week.
- Opus 5: Artificial Analysis about $6/task.

### Others
- **Kimi K2 (original, non-thinking):** *"still writes the best of any model I've used. But it's also stupid as hell and very quick to be incredibly rude. It's not a model you should actually use for much."* Better prose than K3 and K2.5. Kimi K3 earlier impressed him on 3D.
- **GLM 5.3 Flash:** *"a more pleasant model to use arguably than Astra. I've seen GLM53 Flash go off the rails less than Astra for similar work."* He suggests it or the "open source plan" if cost is the main concern.
- **Gemini 3.8 Flash, Muse Spark 1.3:** joke mentions. Flash 3.8 is "meme tier".
- **GPT-3:** historical comparison. AI video editing today is like "shipping an app using GPT3."

## 3. Decision rules and "use X for Y" statements

1. *"Fable is what I reach for when I'm trying to land code and Astra is what I reach for when I'm trying to use my computer."*
2. *"I will be defaulting to Fable for code and I'll be defaulting to Astra for every other thing that I do."*
3. *"Fable 5.1 is a better choice for day-to-day code stuff when cost is not a factor."*
4. **Science:** *"if your job is science, you should probably go get a codex subscription."*
5. **3D prototypes and demos:** *"make the first prototype with Astra to get everything roughly looking and feeling how you want-ish and then have Fable come in and clean it up and do all of the like detail-oriented work."*
6. **Game dev:** combine both. Astra handles 3D visuals; Fable handles interaction, animation curves, camera and movement feel. *"if you use both of them carefully enough you can combine them."*
7. **Computer use:** Astra (with Codex on macOS). Fable only "when given the right tools".
8. **UI / design / front end:** Fable. *"straight up do not trust Astra with UI anything."* *"Astra needs a lot of help if you want a good design out of it."* Turning on Anthropic's Claude Code design skill makes Astra "slightly better".
9. **Copywriting:** neither is good. Astra is slightly better at prose, but *"the way it spams it pisses me off too much to frankly want to ever use it for copy."* He still rewrites most copy himself. Astra can usefully critique Fable's copy (*"Astra is much better at recognizing the copy from Fable"*), but its proposals are weak.
10. **Default to Fable for:** *"a quick bug fix or UI changes that matter or feature improvements."*
11. **Rescue pattern (Astra death loop → Fable):** *"my favorite thing to use Fable 5.1 for [is] to take something that Astra has in a death loop that it just cannot get through. Stop it. Switch over to Fable 5.1, hand it the PR and say, 'Hey, make this actually land. Clean it up. Throw away whatever doesn't belong. Make a new branch if that's easier. Make the changes we care about here land.'"*
12. **Bulk rewrites with UI:** don't trust Astra to carry UI over. *"if the thing that you're doing this bulk rewrite for has UI, you cannot trust that UI is going to be carried over."* Workaround (which he doesn't want to need): append *"I expect the UI to be pixel perfect identical. If any of the UI has changed, you have failed at your goal, so keep going until the UI looks identical."*
13. **Giant rewrites / ports with no UI (e.g. TS→Rust):** Astra, using a goal plus about 40 subagents.
14. **Deep or hard-to-find bugs beyond what reading the code reveals:** Astra (X high), at about 4x the time and tokens.
15. **Full-stack understanding:** "almost feels like a tie". Fable is faster and more intuitive; Astra is exhaustive.
16. **Scope-sensitive changes:** Fable. *"Fable takes less effort to prevent these things with than Astra does."* If you use Astra, tell it explicitly to "make the smallest possible changes" and stay in the loop.
17. **Large orchestration and swarms:** Astra.
18. **Mid-task steering / injecting new instructions:** Astra is best, Fable is solid, Sol gets lost.
19. **Writing prompts for itself or other agents, and writing skills:** Astra is slightly better, but *"none of them are good at it."* *"Please write your skills by hand or at least audit them."* Warning: *"If you let the agent write the skill, you let the skill be involved when it writes another skill, you end up in slop hell very fast."*
20. **Using skills:** Fable has a huge lead.
21. **Honoring boundaries and refusals:** "Fable is ahead". Astra forgets, and its failures are more egregious.
22. **Sol (previous gen) only for** *"exploratory work or things that could be verified programmatically where the code didn't matter that much."*
23. **Low frustration tolerance:** pay for Fable.
24. **Cost is the main concern:** Codex $200 plan; or the open-source plan / GLM 5.3 Flash; or *"wait a few months because this level of intelligence will be accessible at a much cheaper price."* For the $20 and $100 plans: *"wait for this level of intelligence to get cheaper."*
25. **Don't use Astra "fast" mode:** *"If you're using fast with Astra, you're probably using Astra wrong or you're just burning tokens for fun."* Be "very careful of the ultra button" too.
26. **Never use AI for real audio/video editing yet**, except computer-use *setup* (Astra preparing the Final Cut workspace).
27. If Sol-to-Fable-5 was the gap that bothered you (*"Soul is not good enough to merge code from, but Fable 5 often cleared your bar"*), then *"you'll be totally fine with Astra."*

## 4. Head-to-head results

| Category | Winner | Detail |
|---|---|---|
| Science (Terminal Bench Science 0.1) | **Astra** | Astra low 54.3% / $11 vs Fable 5.1 XH-high 50% (Fable 5 high: 25% / $34). He speculates OpenAI is better at post-training on new RL tooling/data. |
| 3D rendering | **Astra (huge)** | "Biggest gap of anything here." Fish Slop 3D: Astra is "next gen" visually but movement is worse, the core loop less refined, and performance bad until told to fix it. Blender scenes from others (Amazon Spheres replica, demo home). Astra 9/10, Fable 5/10. |
| Interaction / animation / game feel | **Fable** | "Fable is so much better at interaction in general." |
| Game dev overall | **Fable (narrowly)** / combine | "Fable catches up to Astra's unbelievable 3D capabilities just due to the smoothness of its outputs." |
| Computer use | **Astra (huge)** | Much faster than Sol; partly due to Codex macOS harness improvements. |
| Copywriting / prose | **Astra slightly**, but unusable | Subtitle spam (21 on one page). Both are big jumps over their predecessors ("unslop baked in"). Kimi K2 is still best. |
| Audio / video | **Astra by default** | Neither is usable for editing; Astra wins on computer-use setup. |
| Non-code overall | **Astra** | Biggest wins in 3D and computer use; science meaningful too. |
| Front end / design | **Fable ("easy, significantly better")** | Neither is above 5/10. Fable one-shots "genuinely compelling" designs; Astra spams subtitles and has cut-offs. "Good designs still require you sit there with a hammer." |
| Full stack | **Tie-ish** | Fable has intuition and speed; Astra tests every edge and finds deeper bugs. "Astra really has that groundhog day feeling." |
| Giant rewrites | **Astra**, with a UI caveat | TS→Rust (TSGO port): Sol ~30% → Astra 80%+ in ~3 days, stalled at 82.6%, 40 subagents, not in the loop. Also T3 Code mobile rewrite in Swift and a GPUI rebuild. But the ping.gg rewrite threw away all UI despite instructions. "For this reason alone, I would make a bigger gap in the rewriting capabilities." |
| Code mergeability | **Fable 5.1 (clear)** | 2 follow-ups from PR filed to merge vs Astra 6. Vibe scale: Sol 2–3/10; Fable 5 ~3–4x better than Sol; Astra ≈ Fable 5 or slightly ahead; Fable 5.1 near 10/10. "Mergeable 20ish% more often." Ben Davis ("OpenAI's number one defender") admits Fable is better for real-world code and has 3 Claude Code accounts. |
| Scope-creep management | **Fable** | Astra creeps by default, partly because review-agent reminders bloat its context. |
| Understanding intent / basic agentic competence | **Fable (decisive)** | 150 PRs "fully yolo merged", 2 regressions, both from Astra. The "revert" story below. |
| Orchestration | **Astra** | "Swarms" (section 5). |
| Steering | **Astra** | Fable "far ahead before"; Astra now has "actual new capability unlocks". |
| Self-prompting / skill writing | **Astra (slight)** | "None of them are good at it." |
| Skill using | **Fable (huge)** | Astra ignores a loaded skill on later turns. |
| Honoring refusals / boundaries | **Fable** | Astra is forgetful, with more egregious failures. |
| Token cost per task / efficiency | **Astra** | $3.26 vs $7.60 per task; 27K vs ~80K tokens. |
| Subscription value | **Codex/Astra (~4x)** | See section 7. |
| Refusal rate | Astra refuses **more** | "Remember everybody being really upset about Fable's security refusals? Astra refuses more often." |

### The "revert" incident (intent, in detail)
A performance-focused PR replaced the T3 Code marketing site's auto-scrolling testimonials marquee with a static horizontal-scroll grid. The prompt said, roughly: *"What happened to my beloved autoscroll on the marketing site?... I need you to revert whatever change broke that and bring it back... that was not a necessary change. Please revert."* "Revert" appeared twice. A follow-up "steering" message asked it to spin up a Tailscale dev server.

**Astra:**
- Deleted a user-controlled variable and some listeners instead of reverting.
- Spun up a dev server for the T3 Code app instead of the marketing site.
- Then hit a Tailscale allowed-host error and committed and pushed an "allow Tailnet host" change specific to the speaker's machine.
- Killed the dev server and sent a dead link.
- Finally **merged the PR** after being told it hadn't made the changes.
- It needed 5 corrections. *"One of the legitimate worst AI code experiences I've had this year."* *"I don't think Astra failed to understand my intent here. I just think it failed to do basic work as an agent."*

**Fable 5.1:** got the exact same prompt, with the Tailscale request folded into the first message. About 5 minutes later the autoscroll was back, the cause was identified as the exact PR, and the link worked. It briefly got confused by seeing another agent's PR merged and reverted, and needed one interruption: *"that was another agent doing things wrong. Ignore that."* *"Exactly what I had intended."*

Note that the two runs differed in one way: the Tailscale request was a mid-task steer for Astra and part of the initial prompt for Fable.

## 5. Subagents, orchestration, planning, verification, review

- **Astra "swarms" vs Fable's planned subagents (the key orchestration distinction):**
  - *"The way Fable does large numbers of sub agents is it plans up front. It decides, I want these four sub agents for this. I want this type of sub agent next. And if these four find things, they can spin up the next type of sub agent where it goes through steps one, two, three, four, five."*
  - *"Astra, however, can just spin up a bunch of sub agents that are doing whatever and then pass messages to them, let them pass messages to each other, and most importantly, it can receive updates from those sub agents and use that to fan things out to keep the whole swarm moving well in the right direction. I've never seen anything else like it."*
  - *"Astra has unlocked novel orchestration capabilities that given a model that wasn't as expensive would legitimately be the path to something like curing cancer."*
  - In the TS→Rust run he has **40 subagents in parallel**, with messages like "root/independent reviewer", "root/object members regression cause". *"It can actually keep track of all of them and work with all of them."*
  - He suggests Codex's "more rudimentary implementation of sub agents" was deliberate, so the model could scale up its own coordination. This contrasts with Claude Code: *"workflows in Claude Code are so good that I did a whole video about why I like Claude Code largely around workflows."*
- **Steering enables orchestration:** Astra *"is so good at getting random [stuff] inserted in its context while it's working and not losing track."* The classic failure he describes: working on tasks 1, 2, 3, 5; he sends "I forgot number 4"; the model does 4 and never finishes the others. *"Fable 5.1 just doesn't do this too too much."* *"Astra eats this. It loves this. It begs you for more."* Combined with orchestration, *"it can have context injected from 40 other agents and handle that fine."*
- **Non-blocking questions:** Astra can ask the user a question mid-task without blocking. If it has already finished, it spins back up to address the answer; if it is still running, the answer steers it without interruption. Requires harness support. *"T3 Code actually does this feature better than Codex, even though it is an Astra feature."* *"This is a change in how the model actually operates."*
- **Self-prompting:** Astra *"can write a decent prompt... I'm much happier with Astra's ability to prompt itself and other agents."* But it is still worse than skilled humans.
- **Cross-model plan review:** for the ping.gg rewrite he had the model write a plan, *"and then I had it and Astra review each other's plans separately"*. "It" is ambiguous, probably Fable. The plan was then committed to a branch in a worktree, then built.
- **Verification loops and review bots:** mergeability is measured as how many follow-ups his AI review bots catch between PR filed and merge. Review-agent feedback can *cause* scope creep: Astra's *"context [gets] bloated a bit by its reminders from all these review agents that will send it off course."* Fable can bloat too *"if it gets the wrong review comments at the wrong time."*
- **Sponsor (Macroscope), useful as a pattern:** path-scoped custom review agents defined as markdown files in the repo (e.g. an "effect service conventions" agent and a "UI consistency" agent), each approving only if its condition is met. They take 12 s and 21 s. A top-level agent then gives an overall approval. *"You could add all of these things into your agent MD, but that only guarantees that your agent knows about them, not that it's actually going to follow."* He rarely merges PRs that the top-level agent hasn't approved.
- **Model-to-model handoff:** Astra for a 3D prototype → Fable for polish; Astra death loop → Fable to land it; Astra critiques Fable's copy.

## 6. Claude Code / Codex specifics

- **Claude Code workflows:** praised as "so good" and the subject of a separate video.
- **Claude Code "design skill" from Anthropic:** turning it on makes Astra's front-end output "slightly better", though *"a little too quick to experiment with fonts."*
- **CLAUDE.md / AGENTS.md:** the prose comparison was run with "no Agent MD or Claude MD". He wants agents to "understand things like a claude MD or a skill file well enough to write good verbiage" and says they don't yet.
- **Skills:**
  - Write them by hand or audit them.
  - Fable reliably pulls in a skill with a reasonable description.
  - Codex has *"a system prompt section around how skill should be applied... if a skill is used in one turn, that skill should not apply for future turns unless requested."* He thinks this is why Astra dropped his "babysitting" skill for 5 follow-ups even though it was still in context. *"I honestly think a lot of it is Codex."*
- **Codex modes and buttons:**
  - "work mode" vs "codex mode" (in work mode he couldn't open a terminal).
  - "ultra" (and "X high" reasoning; "Astra on low" for science).
  - "fast" (avoid it).
  - "goal" (Astra "paused the goal again"; he re-prompted: *"You have my permission to do whatever you need to do. I have you on full access for a reason. Keep going."*).
  - "full access" permissions.
  - Unbounded subagents (*"two ultra running with unbounded sub agents. It's 40 sub agents each can run."*).
- **Codex computer use on macOS:** much of the computer-use gain comes from Codex harness changes: faster spin-up, easier context, faster movement, better background operation.
- **CLI proxy:** he set it up *"because one Claude account just isn't enough at all for most work"* and rotates across multiple accounts.
- **Worktrees:** he had the model make a branch, commit the plan, and work in a worktree.
- **T3 Code** implements Astra's non-blocking questions better than Codex does.

## 7. Cost management and rate limits

- **Cache economics (his key cost point):**
  - Fable 5.1 cache reads fell from $1 to $0.25/M, but cache reads were only about 3% of his cost, and are now about 1%. *"Four times cheaper for 3% of your cost is a less than 1% deal."*
  - **Cache writes are over 60% of his Fable costs.** *"I am paying Anthropic more money to manage RAM for me than I am paying them to run compute for me."*
  - OpenAI now charges for cache writes at $12.50/M (input $10/M, cache read $1/M).
  - *"if either of these labs make cache writes cheap or free, they win cost by default by far."*
- **Token efficiency beats list price.** *"the actual token cost barely even matters in a world driven by token efficiency."* Artificial Analysis cost per task: Astra $3.26, Opus 5 ≈ $6, Fable 5.1 $7.60, Sol $1.99. Astra is *"still a fourth the price in most real world work."* On Artificial Analysis's new index, Fable 5.1 came out cheaper than Fable 5 because of the cache-read change.
- **OpenAI Flex:** half price with no throughput guarantee. Good for jobs that can wait; not available in Codex.
- **Subscriptions:**

  | | Claude $200 plan | Codex $200 plan |
  |---|---|---|
  | Inference value | ~$8K/month | ~$12K/month |
  | Usable on the frontier model | Only 50% for Fable (the "Opus pot" is wasted), so ~$4K, about **a third** of Codex | 100% |
  | Other cuts | Promo boost dropping from 50% to 25% means "losing around 17% off the top" | Tibo claims hosting improvements give "up to a 3 to 4x difference"; the speaker is skeptical but saw "a meaningful difference" |
  | 5-hour limit | Yes, on all plans. Each 5-hour window ≈ 40% of the Fable limit (20% of weekly), so five windows clear the weekly limit, but **only 2.5 with Fable** | **No 5-hour limits** on the $100/$200 Pro tiers; weekly only |
  | Free resets | Rare, "you can't really count on it" | Frequent: "eight free resets in the last 30 days", so the weekly limit is "more like a 3-day limit"; also banked resets |
  | Felt value | — | *"like a 4xish gap... I can get four times more done with Codex on Astra than I can with Fable and Claude Code"* |
  | Enough for one dev? | *"If you're using it a few hours a day, two to three days a week... not using a lot of sub agents, you can probably get by on a single $200 plan"* | *"Most devs, when used responsibly, could absolutely get away with the $200 plan with Codex"*. It falls short only if you use *"higher reasoning limits than necessary and not paying much attention."* |

- **Avoid waste:** avoid Astra "fast"; be careful with "ultra"; don't use higher reasoning than necessary.
- **Reality check:** *"Astra is cheaper than Fable, but neither are cheap... They will both burn limits fast."* For $20/$100 plans, wait for prices to fall. If cost is your main motivation, consider open-source plans or GLM 5.3 Flash.
- **His bias:** OpenAI early access didn't count against his usage. He ran 130 billion tokens in early access, so he lacks a feel for how quickly Astra burns a paid account. He never had free unlimited Fable.
- **Recommendation:** anyone who uses computers professionally and earns over $100K/year *"or your boss should be paying for the $200 a month [Codex] plan."*

## 8. Draft routing table (Video 2 only)

| Task type | Recommended model | Fallback | Why (speaker) |
|---|---|---|---|
| Day-to-day code to be merged (bug fixes, feature additions, perf improvements) | Fable 5.1 | Astra | "Fable is what I reach for when I'm trying to land code"; 2 vs 6 follow-ups per PR; "mergeable 20ish% more often." |
| Quick bug fix | Fable 5.1 | Astra | "defaulting to Fable for things like a quick bug fix." |
| UI changes that matter / front-end design | Fable 5.1 (+ Claude Code design skill) | Astra + design skill, with heavy iteration | "Fable takes the cake here easy"; "do not trust Astra with UI anything." |
| Landing pages / one-shot designs | Fable 5.1 | — | Fable 5.1's one-shot "screams like custom made." |
| Rescuing a stuck/looping Astra task | Fable 5.1 ("make this actually land") | — | His "favorite thing to use Fable 5.1 for." |
| Scope-sensitive minimal diffs | Fable 5.1 | Astra with an explicit "smallest possible changes" instruction plus a human in the loop | Astra scope-creeps "by default". |
| Reverts / intent-sensitive small fixes | Fable 5.1 | — | The "revert" incident. |
| Tasks relying on skills (e.g. a "babysit PR" skill) | Fable 5.1 | — | "Skill using. Fable has a huge lead." |
| Tasks with strict boundaries / refusals to honor | Fable 5.1 | — | "Fable is ahead"; Astra forgets. |
| Giant rewrites / language ports with no UI (TS→Rust) | Astra (goal + ~40 subagents, ultra) | Fable to land and clean up | Sol ~30% → Astra 80%+; "relentlessness." |
| Rewrites/ports involving existing UI | Fable 5.1 (or Astra with explicit pixel-perfect constraint, then Fable cleanup) | — | Astra "would just blanket over destroy the existing UI." |
| Deep / elusive bugs not visible from reading code | Astra (X high) | Fable first, for speed | "if the bug is outside of what Fable can grasp... Astra will find it. It'll just take four times longer." |
| Full-stack feature work | Fable 5.1 (faster) | Astra (more exhaustive) | "Almost feels like a tie." |
| Large-scale orchestration / swarms / many parallel agents with inter-agent messaging | Astra | Fable (planned, staged subagents) | "I've never seen anything else like it." |
| Tasks needing frequent mid-run steering | Astra | Fable 5.1 | "Astra eats this." |
| Writing prompts for subagents / writing skills | Astra (then human audit) | Fable | "Astra is better at it slightly"; "write your skills by hand or at least audit them." |
| Computer use / desktop automation / app setup | Astra (Codex on macOS) | Fable with the right tools | "Astra computer use is so far ahead, it's kind of hilarious." |
| Science / research-tool tasks | Astra (even on low) | Fable 5.1 XH-high | 54.3% at $11 vs 50% for Fable. |
| 3D rendering / Blender / visual prototypes | Astra | Fable | Astra 9/10 vs Fable 5/10. |
| 3D/game interaction, animation curves, camera, movement feel | Fable 5.1 | — | "Astra makes games that look better on Twitter. Fable makes games that actually feel nice to play." |
| Game dev end to end | Astra prototype → Fable polish | — | Explicit two-stage pipeline. |
| Copywriting / user-facing prose | Human (neither is good) | Fable draft + Astra critique; never let Astra write UI copy | Astra subtitle spam; "nothing has topped Kimi K2" (not recommended for use). |
| Audio/video editing | Don't use AI | Astra for workspace setup via computer use | "If you let AI edit your content... you are doing the equivalent of shipping an app using GPT3." |
| Exploratory or programmatically verifiable throwaway code | Sol (GPT-5.6), the cheap option | Astra | "I would really only trust soul for exploratory work or things that could be verified programmatically." |
| Batch / non-urgent jobs via API | Astra on OpenAI Flex | — | Half price, no throughput guarantee. |
| Cost-constrained general use | Astra on the Codex $200 plan | GLM 5.3 Flash / open-source plan | About 4x value; "GLM53 Flash go[es] off the rails less than Astra." |
| Work for low-frustration-tolerance users | Fable 5.1 | — | "you should pay the extra money for Fable." |
| After Fable quota is exhausted | Don't fall back to Opus/Sonnet; switch accounts (CLI proxy) or to Astra | — | "Opus sucks and Sonnet's hilariously bad." |

---

# Cross-video notes (agreements and tensions)

**Agreements**
- Fable is the consistent, high-floor model. Astra is spiky, with higher peaks and much lower troughs.
- Astra's notable failures are basic agentic and intent failures, not intelligence failures. The **same "revert" example** appears in both videos.
- Self-verification and review loops (sandboxed review agents, videos in PRs, babysitting PRs) are central.
- Tokens are expensive, but human time is more expensive.

**Tensions / disagreements**
1. **Long autonomous runs.** Video 1 argues that wide, long runs need the highest floor, and that Astra's floor is unpredictable ("you don't really know how to gauge what level to operate at"). Video 2 uses **Astra** for its longest unattended jobs: a multi-day TS→Rust port with 40 subagents, "not in the loop". One reconciliation: Video 1's "wide" means end-to-end tasks that must ship clean code, while Video 2's Astra runs are measured against a test suite (programmatically verifiable). The videos don't state this, so it is an inference.
2. **Opus.** Video 1 treats Opus as adequate for narrow, well-specified tasks and uses it for log analysis. Video 2 says "Opus sucks and Sonnet's hilariously bad" and calls non-Fable quota useless.
3. **Sol.** Video 1 calls moving from Astra back to Sol understandable and "in some real cases somewhat good". Video 2 rates Sol's mergeability 2–3/10 and trusts it only for exploratory or programmatically verifiable work.
4. **Spend philosophy.** Video 1 says don't downgrade to save money, because your time costs more. Video 2 strongly pushes the cheaper Codex/Astra plan for value, and would choose Astra if forced to pick one. Both still say Fable is better for code when cost isn't a factor.
5. **Gemini Flash / cheap models.** Video 1 says "no one should be using a Gemini thing" and that cheaper models can cost more. Video 2 suggests GLM 5.3 Flash as a more pleasant alternative to Astra for cost-sensitive users.

**Gaps relevant to the routing table:** neither video covers Opus 5.5, Sonnet 5.5, Haiku 4.5 or "GPT-6.1 Sol" by name. Neither gives context-window sizes beyond Astra's "1M" mention. Neither gives guidance on cheap, fast models for subagent grunt work such as search or summarisation.
