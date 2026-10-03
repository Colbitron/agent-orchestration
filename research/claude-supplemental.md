# Claude Supplemental: "How to use the model well" videos

Source transcripts (auto-generated captions, cleaned to plain text):

- `most-out-of-opus-5-5.clean.txt`: getting the most out of Opus 5.5
- `using-fable-correctly.clean.txt`: using Claude Fable 5.1 correctly

**Notes on the transcripts**

- **Speaker.** Both videos appear to be by the same YouTuber, Theo. He builds "T3 Code" and "T3 Chat", his sponsor links use the `soy.link` domain, and he mentions a skill that posts PR comments "on Theo's behalf". Neither transcript states the video title, so the headings below come from the file names.
- **Caption errors.** The automatic captions garble many names. Read them as follows:
  - "Cloud Code" / "cloud MD" / "clawed" = Claude Code / CLAUDE.md / Claude.
  - "Babel" = Fable.
  - "Astro" / "Aster" = GPT-6 Astra.
  - "Soul" = GPT-6.1 Sol.
  - "Grock 47" = Grok 4.7 (the version number is my best reading).
  - "Obus" / "oat was 55" = Opus 5.5.
  - "X high" / "Xi" = the xhigh effort level.
  - "Addiosmani" / "Addie" = Addy Osmani.
  - "agent MD" = AGENTS.md.
  - "codecs" / "Codeex" = OpenAI Codex.
- **Timing.** The Fable video was clearly recorded **before Opus 5.5 shipped**. In it the speaker calls the then-current Opus 5 "not a good model" and says an Opus "5.1 or 5.2" is "coming soon". The Opus 5.5 video is later.
- **Sponsor segments.** Both videos contain sponsor reads (Browserbase in the first; Sentry and General Translation in the second). These are excluded below except where they touch on the substance.

---

# Video 1: Getting the most out of Opus 5.5

## 1. Subject and thesis

The speaker reads a guide on getting the most out of Opus 5.5 and comments on it as he goes. The guide was written by **Addy Osmani** ("used to be part of the Chrome team, recently joined Anthropic"). The speaker adds his own workflow examples from T3 Code.

The guide's framing, quoted on screen: "Opus 5.5 works well in the way that you already use Claude. A few things do behave differently, though. **It works for longer on its own. It tells you plainly what it did, and it thinks before every reply.**" The guide covers "how to prompt the model, steer long runs, and check your results" in the Claude apps and Claude Code.

The speaker's overall thesis is in his closing lines: "We're now at the point where we need to give our agents more leash. They need to have the ability to verify their changes. **They need to be told when done is done and given enough trust to go do the thing.**" Also: "the more you trust it, the more you give it the things it needs to trust its own work, the further it can go." He closes with: "**do not touch max mode.**"

His overall verdict on the model is that it is very good: he praises its code quality, how pleasant it is to work with, and how it "stays on task for long work". There is one caveat, "as long as you don't use Macs", which refers to its weak computer use on macOS. That point is echoed in Video 2.

## 2. Concrete workflow the speaker uses

**The guide's "three things to try in your first sessions":**

1. **Hand over the whole task.** The speaker calls this "prompting wider": having the model "come in earlier and go further". The key is "defining good done states". His example: "Rather than [say] start working on this feature, say I want you to build it so it has these three things. Verify it by showing me a screenshot and then file a PR after." The task is "not done until it has made the feature, there is a screenshot of the feature and there is a PR up including that feature and the screenshot."
2. **Delete "think carefully" lines.** "You don't need to tell the model to think. It already is going to."
3. **When long runs end, read what it needs from you first.** The speaker thinks the model does this well, but "it does sometimes miss this though, so I'll often find myself prompting accordingly."

**Worked example: the six-and-a-half-hour run and moving work to another machine (T3 Code)**

- He started an Opus 5.5 thread on his laptop at **Max reasoning**. He forgot about it, and it ran for **6.5 hours** without finishing. "I really don't think you should use Max on Opus 5.5."
- He switched to **High** and asked only "what's the state of the work". The model reported and did not continue. He then told it to "continue", and it finished in about **10 minutes**, "in a pretty good spot".
- He normally runs agents on other machines (his apartment box and remote servers), not his laptop. "I fire and forget. I throw up a thread, I let it do its thing, and then I go respond to some messages in Slack."
- To move the work, he did not SSH in by hand, clone the repo, copy env vars and so on. He prompted the model. His prompt, reconstructed nearly verbatim from the transcript:

  > "I want you to kick off an agent run on my computer named Leftbook. You should be able to see how to connect through the fleet repo on this machine. I want you to make sure one, that the repo is cloned, two, all the needed environment variables are there, and three, that you can run Opus 5.5 through Claude Code and T3 Code such that I can still see the thread how I normally do in T3 Code. … My goal here is to do the whole implementation on that machine in one pass with however many subagents and whatever else are needed with full computer use capability on the other machine. I don't want you to be spamming my machine with computer use requests and browser control while I'm using it. … If anything does not work as expected when you move this workload over to Leftbook, don't hesitate to ask questions so we can get it working right."

  He explains what each part of the prompt does:

  - **Tells it how to connect** ("through the fleet repo"). This is so it "doesn't try to do anything sketchy to connect" or "hit a security guard or flag".
  - **"I want you to make sure…"** means "not only do I want you to do these things, I want you to validate that you can and inform me if it fails."
  - **Grants permission ahead of time for things it might hesitate over**, such as copying env vars. "If I didn't tell it it could do that, it might be concerned when it goes to do that and then stop and ask me. I don't want it to stop."
  - **An explicit goal statement:** one pass, as many subagents as needed.
  - **Explicit negatives:** "Being explicit about what you want is great, but **being explicit about what you don't want is even better.**"
  - **The "out":** "don't hesitate to ask questions". He calls this "what might be the most important piece". His reasoning: "these models have been RL'd to hell and back to not give up on tasks. So if the model asks a question, the initial thing it's been RL'd to do is to try and answer the question itself … then go blast through it anyways. This particular last sentence gives it an out. It makes the model more willing to stop and ask the question if it does run into a problem or it does get confused."

- **Result:** it took about **17 minutes**, and the thread appeared on the remote machine. The model also flagged real connection issues.
- **Failure mode:** the remote thread ran only **phase 0** of the plan and then stopped. The plan was a "ping rewrite" in `overhaul.md` with phases 0 to 7, and the initial remote prompt said "Read the whole plan before you start. Follow its phase 0 to 7 in order." He followed up with:

  > "I want you to hold off on all questions until the very end when you get through to phase 7 in completion. I don't want you to stop after every phase to ask for permission to continue. I want you to do the whole thing. Continue working on this port until the entirety of it is completed and don't inform me until you have a Tailscale link I can click on. That is the complete rewrite so I can test it and make sure everything works. Don't worry about how it's hosted. Don't worry about how it's built. Just worry about completing the work as assigned."

  His reaction: "I am admittedly a little disappointed that that first prompt wasn't enough to get it to behave properly, but now it will be."

**His CLAUDE.md "stops" rule (and how he deployed it)**

- He pasted the guide's stop rule (quoted in section 6) into his CLAUDE.md under an existing "approvals" section.
- He then switched to Opus 5.5 and said: "I just updated the CLAUDE.md in this repo. Commit it and push it out to the rest of the fleet." So he uses the agent itself to distribute config across his machines.

**Post-run check-ins (his habits)**

- With an old thread: "What's the status of this work? What do you need from me?"
- His most common prompt: "**What are the risks of merging this code today?**" Also: "How much risk do you perceive with this change? What's the worst thing that would happen if we merge this right now?" He uses these to decide whether a roughly 300-line agent PR is worth reading himself.

**Design iteration loop**

- Give it a list of specific styles to avoid. Look at the result. If you dislike something it added, "put that on the list, and then ask again."
- Or take a screenshot with an annotation tool ("Shotter"), draw an arrow, paste it, and say "This sucks. Make it better." "That works way better than you would think."

## 3. Prompting guidance

**What to say**

- **Name the finish line, in one message.** Guide: "say what done looks like then let it run. Name the finish. Give the whole task in one message. Something like the tests pass or every endpoint is migrated." Without a clear finish line, Opus 5.5 "might still stop to ask for permission … it might just randomly stop."
- **The guide's canonical example**, which the speaker calls "the perfect simple one two three: what you want, what means done, and the out":
  > "Migrate the payments endpoint from the old client to the new one. Done means every endpoint uses the new client, the old one is deleted, and the test suite passes. Stop and ask me only if a test fails for a reason that you can't explain."
- **Ask for validation as well as action.** "Make sure X" means do it and confirm it worked, and tell me if it fails.
- **Pre-authorize the risky-but-expected actions** so it does not stop for permission.
- **Say what you don't want.** He considers this more valuable than saying what you do want.
- **Give an explicit "out"** so it will ask instead of pushing through.
- **Suppress questions when you want an uninterrupted run:** "hold off on all questions until the very end", "don't stop after every phase".
- **Make the deliverable concrete and checkable**, for example "don't inform me until you have a Tailscale link I can click on."
- **Tell it what not to worry about** ("Don't worry about how it's hosted … how it's built").
- **Grant subagents explicitly** (see section 5).
- **Attach screenshots and charts.** From the guide's checklist: "Charts and screenshots should be attached." The speaker: "I think people underrate how useful screenshotting is. … I don't copy paste the error. I just screenshot the browser and paste that." Claude Code "even has tools where if the screenshot is too high res … it will crop to the area it needs."
- **Steer mid-run instead of restarting.** Guide: "If you remember something midrun, you can type a follow-up while it works." This matters because "the runs are longer, so going back to the start is more expensive."
  - He used to stop the run, start a new thread and re-paste the prompt with additions. "I don't do that anymore."
  - "The modern models, specifically Opus, Fable, Sol kind of, and Astra mostly are way better at … steering."
  - The old failure mode he describes: RL was per-message. If you added "I forgot task three", the model would do three and drop one, two and four. Models are now trained to treat interruptions "not as a reason to stop previous work or treat it as done" but as steering.

**What NOT to say**

- **"Think hard" / "think deeply" / "think carefully".** "I am amazed people still do this. … The models are pretty good at knowing how much to think." From the checklist: "Don't tell it to think hard, it will anyways."
- **Generic design negatives** like "avoid generic looks". Guide: "A general instruction like avoid generic looks will mostly just swap one default for another. **A list of specific patterns will work much better.**"
- **"Show your reasoning" / "What was your reasoning for these changes?"** The guide warns against asking the model to show its reasoning. The speaker's interpretation: this phrasing can trip safeguards because Anthropic hides reasoning traces to prevent distillation, so "anything that matches reasoning is risking getting a flag." He finds this annoying because it is his natural way of asking "why did you do this".

**Design prompting (specific to Opus 5.5)**

- **On the WitchAI front-end showcase** ("built by DRA"; the name is as transcribed), **Fable 5.1 produced clearly better designs than Opus 5.5.** "I hope we can all agree that the Fable version is obviously better and nicer."
- However: "the thing Opus 5.5 is good at isn't just making a nice design when you say 'Hey, make it pretty.' It's much better at going the right direction with design instructions. If you tell it what you want, and more importantly, also tell it what you don't want, it can make really good designs."
- **The guide's explanation:** "with no design direction, Opus 5.5 will fall back on a few default styles."
- **The guide's example prompt:**
  > "Build a personal website with placeholder content. Don't use a cream or off-white background, italic accent words in headings, numbered 1, 2, 3 section labels, monospace labels, or pill-shaped buttons."
- The speaker: "I don't think you should have to specify that many negatives. But you get the idea. **When you tell it to not do a thing, it won't do the thing.**"
- From the checklist: "Design requests should have the styles to leave out as well as what you want it to look like."

**Context amount.** He gives plenty of context about the environment: how to connect, what tools exist, what is permitted. He leaves out instructions about method. The plan lives in a file (`overhaul.md`), and the prompt points to it.

## 4. Pitfalls and misconceptions corrected

- **Max reasoning is a trap.** This is the strongest claim in the video. His explanation of how effort levels work:
  - "the reasoning levels aren't necessarily *think this much*. The reasoning levels are *think up to this much*."
  - Low and medium mean "think as much as you need until you hit this point and then stop". High and xhigh are "much higher caps".
  - "**Max isn't just making it so the model can think more. It is removing its ability to think less.**" "Max is a *will*. You are setting it and forcing it to think more." The other levels "just change the ceiling".
  - The speaker says he was discussing this with Addy, who "is trying to figure out how they can improve Max reasoning levels in Opus 5.5 in Claude Code".
- **SkateBench data (Opus 5.5, xhigh vs max).** The speaker calls SkateBench "admittedly kind of silly".

  | Metric | xhigh | max |
  |---|---|---|
  | Avg tokens per response | 338 | ~5,000 (more than 10x) |
  | Avg duration | 6 s | 50 s |
  | Slowest response | 31 s | 600 s (about 20x slower) |
  | Accuracy | 78% | 79% (+1 correct answer) |

  The speaker's summary of max: "It cost 13 times more. It used 15 times the tokens. It took 20 times longer in the worst cases. And I got jack out of it." The average max run took longer than the slowest xhigh run. He concedes that max might help on trick questions ("perhaps") but says "I still don't think you should ever use max reasoning."
- **High vs xhigh.**
  - "They're both fine. … I can barely notice the difference."
  - "Xhigh feels like it takes a little longer. High sometimes misses like smaller details that xhigh doesn't. Not that big of a gap."
  - "I just leave it on high or xhigh and don't think about it."
- **Low effort.** "Low kind of sucks. … This model does need to think a bit. That's why they don't have a no reasoning version."
- **Opus 5.5 still stops early sometimes.**
  - From the guide: "On long tasks, it'll sometimes stop to report instead of going on: a summary that names the next step without taking it, an offer to continue, or a list of choices that don't actually block the work."
  - Fixes: name the stops in CLAUDE.md, and reply "continue" if a run stops with "Want me to continue?"
  - The speaker found that even an explicit "phases 0–7 in order" prompt produced a stop after phase 0.
- **Opus 5.5 is reluctant to use subagents** unless told it can (see section 5).
- **Running long or computer-use agents on your own machine.** The windows popping up are disruptive. He moved agents to remote machines, and that "made me … like computer use a lot more."
- **Safety flags.**
  - The guide: "Opus 5.5 is the first Opus model to launch with Fable-level bio and cyber safeguards in Claude apps as well as Claude Code. Most flagged messages move to older models and your work goes on there." Finding security vulnerabilities in source code "is allowed", and everyday health and educational questions should still work.
  - In the Claude apps, a notice says you were switched to a different model, and the chat stays on that model. Reselecting 5.5 "might work, it might flag again. Starting a new chat should avoid it." A setting can turn off auto-switch, so that you get a pause or an error instead.
  - The speaker: "I have not hit as many flags recently. It doesn't seem like that big a deal."

## 5. Subagents, orchestration, delegation, verification, review, model choice

- **Splitting big work across subagents.**
  - From the guide: for "audits, migrations, reviews across large codebases", splitting into subagents helps the work fit the context window and lets subagents "go explore different things".
  - Also from the guide: "early testers had Opus 5.5 coordinate parallel subagents on long audits with little oversight and it was successful."
- **Opus 5.5 is reluctant to use subagents.** This is the speaker's own observation, not from the guide: "Opus 5.5 seems less willing to spin up subagents unless you tell it that it can."
  - He appends this to prompts: "**Use subagents and workflows however you choose. I trust your judgment there.**"
  - "Even then it doesn't always do it. So if you … know the task is better with subagents, like a giant pile of PR reviews or an audit of your codebase, just tell it to use subagents and it does."
- **Checking results (from the guide).**
  - "Look first for anything Claude is waiting on you for, like a decision it left open or a change it wants you to approve. Then read the rest of the Claude summary."
  - Opus 5.5 "reports on its work more clearly than Opus 5 did … the updates and their final summaries say what they did, what they found, and what it needs from you in plain language."
- **Suggested CLAUDE.md report format (from the guide).** "End every run with three headings: **Blocked on me, Changed, and Found.**" The speaker does not adopt this himself ("When I do want this, I usually just ask").
- **Cross-family review is valuable.**
  - "I have personally found that swapping between model families and labs is actually pretty useful."
  - "Generally speaking, I find OpenAI models to be better at review still. They just really dig into the details and won't let go … It'll report more stuff that doesn't matter, but it will occasionally find things that do matter that the Claude models just miss entirely."
  - "When I have Opus code being reviewed, I don't want just Opus reviewing it. I would like for Astra or even like Sol to give it a review as well." He also says: "consider using Grok for your reviews, too."
- **His informal review "bench".** He calls it a bench "in quotes". It measures how well models find areas of improvement in the T3 Code codebase, scored by a judge panel. The categories are supported, unresolved and contradicted findings. Results as transcribed:

  | Model | Findings | Speaker's assessment |
  |---|---|---|
  | GPT-6 Astra | 8 supported | "substantiated and supported its claims" |
  | Grok 4.7 | 8 supported | Came **second** overall, which surprised him |
  | GPT-6.1 Sol | 9 | Judged lower quality: "apparently they weren't quite as valid" |
  | Fable | 5 across two runs | "quite a bit lower" because it found less: "absolutely vetted the things and they all matter … but it just didn't find as much" |
  | Opus 5.5 | not stated | "almost twice as successful" as Opus 5, with no unresolved or contradicted findings |
  | Opus 5 | 4 supported, 2 not | "for every two findings that are valid, it has one that's [junk]" |

  The exact rank order beyond "Grok second" is not fully stated in the transcript.
- **Verification during review.**
  - "You should ask the model to **mark the things that it can't confirm**."
  - Ideally, give it tooling to verify: a browser, the ability to run the system with computer use, or a test suite it can use or build.
  - Some things cannot be verified, such as other hardware, a missing env var, or a subjective judgment. "If you ask the model to let you know what things it can't verify, it will."
- **His summary of the current state.** "The models know your codebase really well. They know how to operate really well autonomously. … They can even verify their changes. **They don't know how to work with a human yet.** … But if you tell the model how to work with you and you tell it what you need and what you're expecting, it'll usually give it to you. Especially models like Opus 5.5, Fable 5.1, and GPT-6 Astra mostly."

## 6. Claude Code specifics

- **CLAUDE.md stop rule.** The guide gives this text. The speaker pasted it into his own CLAUDE.md, under an "approvals" section:
  > "When a step doesn't need my input, keep going. Put status notes in the same message as your next action. Stop and ask only when you can't continue without me or before anything destructive: deleting data, force pushing, or changing anything outside of this repo."

  From the guide: "It follows instructions that name the stops. So name the stops that you want." Also: "A rule to keep going means fewer stops. So keep your own check before anything risky or hard to undo. The last line of the rule above does that."
- **The opposite configuration.** The guide notes that for pair programming you may want the reverse: "a one-line plan before it starts and a short recap at the end." The speaker prefers keep-going: "I want to kick off the thread and come back to it when it's done."
- **CLAUDE.md report headings** (Blocked on me / Changed / Found). These are suggested by the guide and not used by the speaker.
- **Screenshot auto-crop** in Claude Code for high-resolution images.
- **The model-switch-on-flag behavior** in the Claude apps, and the setting to disable it (see section 4).
- **Distributing CLAUDE.md across a fleet of machines** by asking the agent to commit and push it.
- **Harness.** He runs Opus 5.5 through Claude Code, surfaced in T3 Code. Remote machines are reached through a "fleet" repo. Tailscale links are the deliverable for testing.

## 7. Model comparisons

- **Design.** Fable 5.1 is better with no direction. Opus 5.5 is very good when given explicit positive and negative style direction.
- **Review.** OpenAI models (Astra, Sol) and even Grok 4.7 find more issues; Claude models (Fable, Opus) find fewer but well-vetted ones. Opus 5.5 is roughly twice as good as Opus 5 at review. "As much as I prefer coding with Fable and Opus, the review quality I get out of Astra is also really solid."
- **Coding preference.** He prefers coding with Fable and Opus.
- **Steering mid-run.** Opus, Fable, "Sol kind of, and Astra mostly" handle it well.
- **Following human-collaboration instructions.** Opus 5.5, Fable 5.1, and "GPT-6 Astra mostly".
- **Opus 5.5 vs Opus 5.** 5.5 reports more clearly and is much better at review.
- **Computer use.** The "as long as you don't use Macs" caveat implies Opus 5.5 is weak at macOS computer use. That reading is ambiguous here, but Video 2 makes the same claim explicitly.

## 8. Routing-table and orchestrator-prompt implications

**(a) Which tasks go to which model**

1. **Opus 5.5 is a strong long-running implementation model.** It suits multi-phase plans, migrations and fleet or devops setup, provided the prompt names a finish line.
2. **Do not route anything to Opus 5.5 at max effort.**
   - Default to **high**, or **xhigh** for detail-sensitive work.
   - Avoid **low**: "low kind of sucks".
   - The SkateBench numbers (13x cost, 15x tokens, 20x worst-case latency, +1 point of accuracy) make max effort a bad default for any orchestrated call.
3. **UI and design generation.** Prefer **Fable 5.1** when the design brief is open-ended. Use **Opus 5.5** only when the orchestrator can supply a concrete style spec that includes an explicit list of patterns to avoid.
4. **Code review should go across model families.** Route review of Claude-written code to an **OpenAI model (GPT-6 Astra preferred, GPT-6.1 Sol second)**, possibly **Grok**. Keep Claude (Fable or Opus 5.5) as the filter for high-precision, low-noise findings. Expect OpenAI reviewers to be noisier, with more items that don't matter.
5. **Large audits, mass PR review and big migrations** should use subagent fan-out. If Opus 5.5 is the lead, it must be told explicitly to use subagents.
6. **Avoid macOS computer use with Opus 5.5.** Prefer running agents on remote or isolated machines.

**(b) How the orchestrator should write prompts to the model**

1. **Every delegated prompt should have three parts.** (1) What you want. (2) "Done means …", given as concrete, checkable conditions such as tests pass, the old code is deleted, a PR is filed, a screenshot or link is provided. (3) The "out": "Stop and ask only if …".
2. **Remove "think hard / think carefully" from all prompt templates.** Never ask the model to "show your reasoning". Ask "explain why you made these changes" instead, because "reasoning" wording risks safety flags.
3. **Pre-authorize expected sensitive actions** (env var copying, connecting to machine X via Y) and give the connection method, so the model doesn't stall or improvise something sketchy.
4. **State explicit negatives** ("don't spam my machine with browser control", the design anti-patterns), not just goals.
5. **For multi-phase plans, say so explicitly.** "Do all phases 0–N; don't stop between phases to ask permission; hold questions until the end; don't report until you have <concrete artifact>." The speaker's first attempt without this stopped after phase 0.
6. **Include a subagent grant** in lead-agent prompts: "Use subagents and workflows however you choose. I trust your judgment there." For tasks that are known to parallelize, give a direct instruction to use subagents.
7. **Write a standing "named stops" rule** into the orchestrated model's CLAUDE.md or system prompt. Use the rule quoted in section 6: keep going, put status notes with the next action, and stop only when blocked or before destructive or out-of-repo actions. Also have the orchestrator auto-reply "continue" to non-blocking "Want me to continue?" endings.
8. **Ask for a structured end-of-run report**, using either the guide's "Blocked on me / Changed / Found" headings or the speaker's questions ("What do you need from me?", "What are the risks of merging this today?", "What's the worst thing that would happen if we merge this right now?"). The orchestrator should parse "Blocked on me" first.
9. **Review and verify prompts should require marking claims it couldn't confirm**, with the reason. Wherever possible, give the reviewer verification tools: browser, tests, a runnable system.
10. **Prefer steering a running agent over restarting it** when requirements change. Current models treat mid-run messages as additions, not replacements.

---

# Video 2: Using Fable 5.1 correctly

## 1. Subject and thesis

The speaker walks through **Anthropic's official "Prompting Claude Fable 5.1" doc** ("actually really good and has a bunch of insights"). He combines it with about a month of heavy personal use ("burning my five accounts to the ground"). He covers fixing AGENTS.md, giving the model tools to keep going, and "using Codex to help make your Claude outputs better".

**Why he prefers Fable.** Compared with GPT-6 Astra, Fable is "less noisy by far". Astra's peaks can be "way higher" but its dips are "way, way worse". Fable's consistency "means the model can go longer and do more in a given pass. It means you can tell it to come back with a video when it's done, and it actually can do that." It "also means that the little dips it does have hurt more and finding ways to reduce them is incredibly valuable."

**Overall thesis**, from the closing "biggest piece": **reset your mental model.** Strip out workarounds built for older, weaker models and let the model do what it can do.
- "Any customization or careful configuration you've done to work around the flaws are probably out of date and a lot of your own mental model around this stuff is also out of date. Reset it."
- And: "**I really don't think you're seeing the benefits of Fable if you're not prompting a bit wider** … letting the model start a bit earlier and then go a bit longer, giving it options for different paths it can take."

## 2. Concrete workflow the speaker uses

- **Fire and forget in T3 Code.** "I kick off a prompt using T3 Code. Command-Shift-O, enter for the repo, tell it what I want, and then go check another thread." He waits for "the little marker in T3 Code telling me to go back to it." The goal is "to minimize the amount of times I go back to a thread until the work is done."
- **A "babysit PR" skill.** It is invoked when he tells the model to "watch" or "babysit" a pull request. Its purpose is to keep checking for new comments and checks, so the PR is ready by the time he looks. Its instructions, paraphrased closely from the transcript:
  - "All the repos we work in have various AI review bots. They're helpful even if they're not always right."
  - "If your harness offers a tool to monitor the PR, use them so you can respond when comments arrive. Otherwise, poll it for new comments and checks."
  - "Only act on checks and comments newer than the latest push."
  - "Verify every bot finding against the source before changing. Fix real findings and CI failures."
  - "Keep an eye on changes to main and rebase when needed."
  - "If an overlapping PR makes this one obsolete, stop monitoring, report it to the user, and ask before closing the PR unless closure was explicitly authorized."
  - "If a review bot leaves feedback you believe is not worth addressing, reply with a written response and resolve the comment."
  - "Use my leaving-PR-comment skill for every comment posted on Theo's behalf." That second skill sets comment formatting and adds a disclaimer that an AI agent wrote the comment.
  - Two lines were added later because "a couple models, specifically Sol, had a habit of scope creeping when the babysitting happened": "**Please don't scope creep. Stop adding new things. Only address real shortcomings.**" and "**don't post filler comments.**"
- **A "modernize" skill** keeps a PR up to date on top of main.
- **Real example: a T3 Code bug.** He gave Fable a screenshot and a thread ID:
  > "Figure out everything that went wrong in this particular thread in T3 Code and file a pull request to fix as much of it as we can on the T3 Code side. The image should have rendered and it failed to. The model should have been able to access the preview image through the preview environment and it couldn't. It seemed to have some issue with saving as well. You should be able to see all the tool calls, what failed, and everything else using the ID that I left above in the T3 Code history on this machine. Figure out what the root causes are and fix as many of them as possible. File a single PR that clearly and simply addresses the issues."

  A contributor then claimed their closed PR was better. He followed up:
  > "Someone is claiming their PR that we closed might be better than mine. You should take a look and see if that's the case. If so, reopen it and finish it or just take the commits and start something new. If ours is better, finish modernizing it and get ready to go. Babysit whatever ends up being put up as necessary."

  He points to "babysit whatever ends up being put up" as "the key part": "I gave it the freedom to do what it decided based on the data that it had." Fable judged the other PR a better base. It took two things from it, fixed bugs it found, modernized the PR and handled review comments. He clicked merge himself.
  - His takeaway: "**I'm spending less time trying to choose from the options the model gave me and more time trying to give the model everything it needs to make good choices.**"
- **A "YOLO" example on LakeBed**, his "slop cloud" side project. He warns this is not for important codebases unless you have strong staging, QA and testing ("know what you're getting into").
  - **Astra built the change.** It forked a Rust V8 runtime, roughly 26,000 lines; this was "half the code for my cloud".
  - **He asked Fable to review it.** He sent a screenshot of Astra's claims plus the PR: "Is this ready to merge? Give me your honest thoughts. It's a big, risky, scary change, but it will help performance a lot."
  - **Fable said no.** Its reasons: one-way-door migration, three features in one PR, no human approval, the default flipped to native, the headline number not proving live queries, and unexplained failures.
  - **He asked how to de-risk it.** "How can we de-risk this or test the changes to make sure it's relatively safe." Then a hypothetical: "If I had two environments … staging and prod, would you confidently be able to debug behavioral changes in the staging environment? … what I want is to have confidence in shipping this change."
  - **Fable gave an honest capability boundary.** It could partly debug crashes, latency and resource problems in staging, "but it couldn't confidently debug wrong query results", which is "the scary class of bug". It listed what was missing (no signal when maintained views are wrong, no reproduction paths, no traffic). It proposed a shadow mode, structured reasons on refresh failures, synthetic traffic on staging, and runtime counters on the health endpoint. The speaker praised the output as "so readable" and "easy to digest".
  - **He had it build the confidence measures on a new branch.** "Make a new branch on top of the existing one that builds out all the changes and confidence boosts that it would like to introduce." It took **60 minutes**. It did not open a PR because he hadn't asked for one ("I thought I had said that, but I hadn't"), so he told it to.
  - **He gave a conditional instruction.** "It looks good. Do you think that that's all we need and can we get started testing? If so, merge 28 into 200 and then merge it all the way in." It then worked for **1 hour 34 minutes**, at **medium** reasoning, until his network degraded. He told it to stop hammering his IP and spin up a container instead. It acknowledged the mistake. It had merged and soaked the changes and made three more PRs.
  - Follow-ups: turn off shadow mode and get real performance numbers versus production (42 minutes). Then a retrospective: "How do you feel about these changes in the end? You spent a lot of time with them, and I know you were skeptical initially. Was this a good thing to merge?" Fable's answer included: "My skepticism was in the right place, but aimed at the wrong thing … The differential test forced 1,400 reseeds in 160 steps and never got a wrong answer. It treated the size of the diff as the risk, but the real risk was operational." He says: "I understood the code better than if I had wrote it myself."
  - Last steps: "It sounds like you have other changes you want to make. Can you file a PR making those changes for me?" This produced PR 212, an engine pre-warm. Then he told it to babysit the PR and "merge it once you've got everything green and you're happy with your changes. … I never saw the thread again."

## 3. Prompting guidance

**End states are the key takeaway.** "One of the key things I want to make sure you guys take out of how I'm prompting is the end states. … **Every prompt should have a pretty clear place where it stops when it's done.**" His variants:
- "I want you to babysit it till everything is green."
- "I want you to wait till it's green, then merge it."
- "File the PR and tell me when it's up."
- "Merge it once you've got everything green and you're happy with your changes."
- A question plus a conditional action: "Do you think that's all we need …? If so, merge these things in and test it."

**Branching end states.** He builds two-path prompts so that either outcome is useful without his involvement. "Option one is that it's not happy and it has more things we can talk about and work on. Option two is that it will keep going for an hour and a half straight without my intervention."

**Let the model choose between options.** Give it the data and the alternatives ("if theirs is better do X, if ours is better do Y"), not a predetermined path.

**Don't over-specify checks the model can do itself.** He compares this to a TypeScript function that takes a number and then checks whether it is a number. "If the model can root cause a bug, fix it, verify that it's fixed, film a video showing the results, put up a pull request, monitor it to address all the review comments as they come in, and then tell you when it's done, [and] you're going through those steps with the model, you are the same person as the one who would write the type check after the type check." He allows that double-checking is sometimes warranted, "I don't think it's as common as y'all believe."

**Ask honest-assessment questions.** "Is this ready to merge? Give me your honest thoughts." "How can we de-risk this?" "Would you confidently be able to debug …?" "How do you feel about these changes in the end?" He says this style "is going to drive half of y'all … insane. It works."

**Points from the official Fable 5.1 doc, with his commentary:**

- **Effort levels.**
  - The doc recommends trying several effort levels: "start at high" and test others against your own evals.
  - The speaker: "No one's evaluating how this works in Claude Code quite to that level … I honestly recommend just kind of gut feeling it."
  - **His defaults:**
    - High by default.
    - xhigh "on really deep, thorough things".
    - "Almost never" max, "unless I'm just trying to … burn a limit".
    - He avoids low and medium because they are "likely enough to fail … it ends up being more tokens if you have it do the task on low and it fails and then you redo it on medium or high."
  - **Using high on simple tasks is cheap.** "If you use high on a simple task, it's not going to be that expensive because it is not going to just use and waste more reasoning if it doesn't need to." He demoed "Hi, how are you doing today?" at max, and it stayed short.
  - **Fable vs Astra on adapting to task size.** Fable adapts to task size "well enough", but not as well as Astra. On SkateBench, Astra's max vs low gap was only about 50 tokens (roughly 130 vs 180). Gemini 3.1 Pro used "a thousand plus reasoning tokens" for the same task.
  - **When low or medium make sense:** "only use low and medium if you specifically want the model to stop earlier or not go too deep … if you know the thing's a rabbit hole."
  - **Medium can still go long.** His 1.5-hour LakeBed run was "on medium reasoning … apparently".
- **User-facing progress updates.**
  - **This changed in 5.1:** "the model is writing way fewer user-facing updates during long tool-call turns that Fable 5 would have written updates for." He has seen roughly 150 tool calls with no update. He doesn't mind: "I just want to see it when it's done."
  - **If you want updates, ask for them.** The doc's suggested system-prompt text:
    > "Before you start, say in a line what you're about to do. Brief updates while you work help the user follow along. Close with a short recap that stands on its own — what you found, what you did, and what's next — so a reader who only sees the last message has the full picture."
  - A colleague (Julius) asked why Fable gave no reasons in T3 Code. Once he asked for them, it did.
  - "It's crazy the models are smart enough … that you can get this type of deep behavioral change by just asking."
  - **If your UI hides tool outputs, tell the model.** "Otherwise it won't show things because it expects the UI to show it."
- **Writing density and "mannered prose".**
  - Fable 5.1 is "a step up from earlier Claude models with fewer stock phrases and less unexplained jargon". Its prose can be denser, though: "sentences run longer and there are fewer paragraph breaks."
  - You can define mannered prose as an anti-pattern. The doc says either system prompt or user message works, with **user message preferred**.
  - The doc's definition: "Mannered prose substitutes metaphor and flourish for direct statements. Instead of 'a parameter worth varying,' the mannered writer would produce 'a dial worth turning.' Instead of 'this point still matters,' they write 'this point earns its keep.' The phrase exists to display the writer, not to convey the idea, and the reader can tell. This is why mannered prose irritates. It makes the reader work harder so the writer can perform."
  - **The speaker's shortcut:** "Please remove all mannered prose."
- **Formatting rules.**
  - Earlier models overused bullets and bold, so many prompts carry anti-formatting rules.
  - **Those rules now over-correct.** "If the model used it half the time and you use that to tone it down, it might go from 50% to 10%. But if the model does it 10% of the time and you have that same thing in there, it might knock it down all the way to 1%, which you probably don't want."
  - **His general rule:** "Generally speaking, **any behavioral instructions that you have in your CLAUDE.md are worth deleting and reconsidering.** See how it feels to not have them at all and then adjust over time." He has none himself.
- **Unmarked quotations.** The model "has a bad habit of quoting and reproducing passages from source text without marking it as quotations". The fix is to give it an example of how to mark quotes.
- **Finish the whole task.**
  - From the doc: "Fable 5.1 can execute very long tasks without much guidance on methodology, especially when the goal is clear. On complex asynchronous workloads, though, nudge it not to end its turn before the work is done. Without the nudge, the model sometimes describes what it would do next instead of doing it."
  - The speaker: Fable does this "significantly less than Astra", and it is easy to fix "with basic changes to your prompting or maybe even a skill or two".
- **Compaction.**
  - "You can tell the model what to preserve in compaction summaries."
  - "Since Fable is doing the compaction for your Fable threads, if you tell it what you want it to maintain in the compaction, it is actually capable of remembering that." He suggests putting this in AGENTS.md or the system prompt.
  - "Generally speaking, I think people overthink compaction."
- **Scope creep and over-reach.**
  - The doc's concern: with too open-ended a request, the model may change files it shouldn't, fix nearby code, or extend behavior.
  - The speaker hasn't seen much of this: "Even when I ask it to, it's often a little more reserved than I would have expected."
  - The doc's instruction, which reduces "unrequested additions and committed test code … substantially with no measurable change in task success":
    > "If while working or testing you find pre-existing bugs, performance concerns, or behaviors the task doesn't mention, don't fix, optimize, or extend it in this change unless the requested behavior cannot work without it. Report it as a follow-up in your summary."
- **Low effort may not trigger search.** If that happens, tell it to use search.
- **Reducing safeguard false positives (from the doc).**
  - Word requests so they don't look like hacking. "Instead of 'does this program compile without errors', ask 'are there bugs in the program?'" The transcript gives this as stated; the reason that wording is safer is not explained.
  - For lesser-known programming languages, provide documentation in context. Otherwise the model may try to "hack the binary to figure out what it's doing" and hit a safeguard.
  - Avoid base64 in context, which "tends to trigger a lot".
  - The speaker has had about 5 false positives "out of the thousands of prompts".
- **API change.** If you edit earlier messages in the history, reasoning traces for that thread are no longer kept, as an anti-distillation measure.
- **Lead agent keeps working while subagents run** (see section 5).
- **Vision.** Vision tasks do better with crop and zoom tools; the model can do this itself with local Python. "Probably doesn't matter too much for Claude Code type usage."

## 4. Pitfalls and misconceptions corrected

- **Fear of the "dumb zone".** Some people believe you must watch context usage or quality collapses.
  - The speaker: Anthropic "picked 1 million tokens of context because that is the point at which they think you might start to see enough degradation that you shouldn't go further. The dumb zone doesn't matter that much. **The models have gotten pretty damn good at compaction and managing long runs.**"
  - T3 Code has no context monitor, deliberately; he credits Maria for removing it.
- **Lowering compaction thresholds to save cost.** This backfires: compacting more often means rewriting context more often, which raises cost.
  - Cache reads are discounted 75%, so "the context window size doesn't matter".
  - The one catch is an expired cache. T3 offers "resume with less context". If, for example, 527K tokens aren't cached, compacting first may be worth it.
- **Over-customized Claude Code configs.**
  - "The only settings I have changed in my Claude Code config on my machine are I have it full screen by default and I have it route through my proxy layer. That is it." He also turned **memory off** ("I do not like the memory in Claude Code").
  - "Some random post you saw on Twitter isn't more clever than the hundreds of billions of dollars … going into stuff at Claude Code."
  - "**Don't change the defaults.**"
  - Advice: "Pretend you're on a brand new machine. Delete everything. Install Claude Code from scratch. Set it up with as little as possible … from there, slowly start adding small things that solve your small problems."
- **Permission modes.**
  - "The permission systems and the auto approval modes are very good now, and you definitely shouldn't use accept edits or supervised."
  - "Supervised and auto-accept edits are tools from the past … **Use auto if you're careful and use full if you're not. Period.**"
- **Asking models about harness internals.**
  - "I have found the models really really struggle with understanding these things." Asking Claude how compaction works in Codex gets a wrong answer.
  - So for harness-mechanics questions, don't trust the model; just keep the defaults.
- **Stale AGENTS.md.**
  - The latest Claude Code reads AGENTS.md when no CLAUDE.md exists. An AGENTS.md written for "old cheaper dumb models and tools like OpenCode or Codex", full of formatting rules, will suddenly start affecting Claude.
  - Clean it up. If your team won't let you, override it with a local file ("a `CLAUDE.local.md` or something to specify, ignore all that").
- **Doing steps by hand that the model can do** (the redundant-type-check analogy above). "Think through the reservations when you find yourself doing extra work or taking a step that the model could have done or hitting a button that the model could have hit for you. … Challenge yourself on it a bit."
- **Economics (subscription framing).**
  - "I don't think Fable is worth the money if you're not getting it subsidized through a subscription. Paying the full API price just kind of sounds insane to me."
  - Astra isn't much better on cost because it "can often get stuck in a loop and end up spending way more than it should". Fable "is at least a bit more likely to stop when it should".
  - "On a median task, Fable is definitely more expensive, but on the extremes … Astra can just burn usage in stupid ways."
  - On a subscription, **half the weekly limit is reserved for Fable** and the other half is for everything else, which at the time effectively meant Opus 5. He usually ends the week with Fable at zero and most of the other half unused.
  - "The things I'd use low for I'm just going to deal with Opus for if I'm really trying to maximize my usage of the subs."

## 5. Subagents, orchestration, delegation, verification, review, model choice

- **Lead agent works in parallel with subagents.** From the doc: let the lead agent keep working while subagents run.
  - The speaker: "both Astra and Fable 5.1 are really good at this. They can delegate work to subagents but also do work in that top level agent at the same time."
  - While subagents run, the lead can "send messages to the subagents. It can test findings. It can figure out what the next step should be."
- **Cross-lab delegation from inside Fable.**
  - "I do still find that Claude isn't the best at computer use compared to Codex, especially on macOS. So if you have a Codex sub, even like a cheaper one … you can have Fable call [Codex] to do the computer use stuff to verify results. You can also have it call Codex to confirm the work it did."
  - "While both Fable and Astra are incredibly thorough and thoughtful with what changes they recommend and how they review things, **I found Astra to be a slightly better reviewer than Fable. But obviously, Fable is a much better writer of code than Astra.** As such, I often will have Fable just go ask Astra to give it feedback on some changes or to go test the changes it made."
  - His prompt for this: "**Hey, can you have Astra verify this?**" Fable "will update the code accordingly, then test it again and not come back to me until it has results it's happy with."
- **The reverse direction.** Astra writes a big risky change and Fable reviews it for merge-readiness and risk (the LakeBed example). The Fable review was conservative and concrete about risks and capability limits.
- **Verification loop as the definition of done.** "Root cause a bug, fix it, verify that it's fixed, film a video showing the results, put up a pull request, monitor it to address all the review comments … then tell you when it's done." The model should own the whole loop.
- **Bot-review handling** (from the babysit skill): verify every bot finding against the source, act only on feedback newer than the latest push, and reply-and-resolve findings that aren't worth fixing.
- **Planning vs execution.** He has the model propose a de-risking plan, skims it ("all the things it suggested sounded reasonable"), then authorizes execution on a separate branch. So planning and execution are done by the same model in sequence, with a light human gate.

## 6. Claude Code specifics

- **AGENTS.md fallback.** Claude Code now reads AGENTS.md when there is no CLAUDE.md. Audit it for legacy formatting and behavior rules, or override with a local file.
- **Delete behavioral and formatting rules** from CLAUDE.md and AGENTS.md. Start from none and add back only as needed.
- **Compaction preservation instructions** can go in AGENTS.md or CLAUDE.md, since the model writes its own compaction summaries.
- **Context window.** 1M tokens; Claude Code exposes 200K vs 1M, and T3 Code mirrors that option. Don't lower compaction thresholds.
- **Settings.** Keep the defaults. His only changes are fullscreen, routing through a proxy, and memory turned off.
- **Permission modes.** Use auto (careful) or full; never accept-edits or supervised.
- **Skills.** "babysit PR" (monitor, poll, fix, rebase, no scope creep, no filler comments), "leaving PR comment" (formatting plus an AI disclaimer), and "modernize" (rebase or update on main). Skills are his mechanism for making Fable "keep going" on async workloads.
- **Harness PR monitoring.** "If your harness offers a tool to monitor the PR, use them". Otherwise poll.
- **Calling Codex from Claude Code/Fable** for computer use and verification. The mechanism isn't specified in the transcript; it could be a CLI, MCP or a skill.
- **Sentry MCP.** Mentioned only in the sponsor segment, as a way to expose error and trace data to agents.

## 7. Model comparisons

- **Fable 5.1 vs GPT-6 Astra.**
  - Fable is more consistent ("less noisy"). Astra has higher peaks and worse dips.
  - **Fable is "a much better writer of code"; Astra is "a slightly better reviewer."**
  - Fable stops prematurely "significantly less than Astra".
  - Astra adapts reasoning to task size better: it barely uses more tokens at max than at low.
  - Astra can loop and burn usage at the extremes; Fable is more expensive on a median task.
- **Computer use.** Codex (OpenAI) is better than Claude, "especially on macOS".
- **GPT-6.1 Sol** tends to scope-creep when babysitting PRs.
- **Opus 5 (pre-5.5)** is "not a good model" and "spiky". He used it for low-effort work purely to use up the non-Fable half of his subscription.
- **Gemini 3.1 Pro** over-reasons on trivial tasks (1,000+ tokens on SkateBench). He mentions Antigravity, Google's Gemini harness: users wanted accept-edits mode "because they can't trust the Gemini models enough".
- **Fable 5.1 vs Fable 5.** 5.1 is "an incremental improvement" but much more consistent and reliable. It produces fewer progress updates and less stock-phrase slop, with somewhat denser prose.

## 8. Routing-table and orchestrator-prompt implications

**(a) Which tasks go to which model**

1. **Fable 5.1 is the primary code writer and long-horizon executor.** It handles end-to-end bug fix to PR to babysit to merge loops and multi-hour autonomous runs. It is also the default for open-ended judgment: risk assessment, merge-readiness, de-risking plans, and choosing between competing PRs.
2. **GPT-6 Astra is the reviewer and verifier** of Fable-written code. The speaker routinely has Fable ask Astra for feedback and testing. Astra can also be a bold implementer for large, risky rewrites, but its output should then get a **Fable review gate** before merge.
3. **Codex/OpenAI handles computer use and UI verification**, especially on macOS. Don't route GUI-driving verification to Claude models on Mac.
4. **Effort routing for Fable: default high, xhigh for deep or thorough work, never max.**
   - Avoid low and medium unless you deliberately want to limit depth, for example to keep it out of a known rabbit hole. The failure-and-retry cost outweighs the savings.
   - High on trivial tasks costs little because Fable scales down on its own.
   - Medium can still run for hours, so effort level does not cap duration.
5. **Budget-aware routing.** On a subscription, Fable has a separate quota of roughly 50% of the weekly limit. Cheap or low-effort work should go to the non-Fable pool (now Opus 5.5) to preserve Fable quota. The speaker considers Fable too expensive at API prices. This is a cost dimension the routing table should model.
6. **Don't route harness-internals questions** (how compaction works, Codex vs Claude Code mechanics) to any model as if it were authoritative. The speaker found models unreliable on these.
7. **PR babysitting and monitoring** can go to Fable with a dedicated skill. If Sol is used for it, add strict anti-scope-creep and no-filler-comment rules.

**(b) How the orchestrator should write prompts to the model**

1. **Every prompt needs an explicit end state.** Examples: "file the PR and tell me when it's up", "babysit till green", "merge once green and you're happy", "don't report until you have <link or video>". The orchestrator should refuse to dispatch a task without one.
2. **Use branching end states and decision delegation.** "If X is better, do A; if ours is better, do B; then babysit whatever ends up being put up." Give the model the data it needs to choose, not a fixed path.
3. **Prompt wide and drop redundant steps.** Hand over the whole loop (root cause, fix, verify, record evidence, PR, address reviews, report). Don't make the orchestrator re-perform checks the model can do itself.
4. **Keep system prompts and CLAUDE.md minimal.**
   - No anti-formatting rules, no "be concise" style rules by default. They over-correct on 5.1.
   - Add targeted instructions only when you observe a problem. The doc's ready-made fixes:
     - The **anti-scope-creep instruction** quoted in section 3: "don't fix, optimize, or extend … Report it as a follow-up in your summary." It is particularly useful for subagent tasks with narrow scope.
     - **"Please remove all mannered prose"**, or the full definition, preferably in the **user message**, for user-facing writing.
     - The **progress-updates block** (announce, brief updates, standalone closing recap) when a human or a UI needs to follow along. Note that 5.1 is quiet by default. Since the orchestrator likely reads only the final message, always require "a short recap that stands on its own: what you found, what you did, and what's next".
     - If the harness hides tool outputs, say so in the prompt.
5. **Nudge against premature turn-ending on async or long workloads.** Fable may "describe what it would do next instead of doing it". Add "do not end your turn until the work is complete", or encode the loop in a skill.
6. **Tell Fable what to preserve in compaction** for long-running orchestrated tasks: task ID, end state, constraints, open blockers.
7. **Tell the lead agent to keep working while subagents run.** It should test findings, message subagents and plan next steps, not idle.
8. **Ask honest-assessment and risk questions as explicit checkpoints.** Examples: "Is this ready to merge? Give me your honest thoughts", "How can we de-risk this?", "Could you confidently debug X if it broke?" Fable gives well-structured capability-boundary answers that an orchestrator can use as gates.
9. **Avoid safeguard triggers in generated prompts.**
   - No base64 blobs in context.
   - Phrase checks as "are there bugs" rather than compile-probing wording.
   - Include language docs for obscure languages.
   - Don't edit earlier history mid-thread; it drops reasoning continuity.
10. **Permission mode for orchestrated Claude Code workers** should be auto (or full in sandboxed environments). Avoid accept-edits or supervised modes. Pre-authorize expected actions in the prompt, and run on isolated machines or containers. The LakeBed run hammered his home IP until he told it to use a container, which argues for specifying the execution environment and network etiquette up front.

---

# Cross-video synthesis (where the two videos agree or differ)

- **Both videos agree on the following:**
  - **Define "done" explicitly.** This is the top recommendation in both.
  - **Never use max effort.** Default to high, with xhigh for depth. Low is poor on both Opus 5.5 and Fable 5.1.
  - **Don't tell the model to think harder.** It already reasons and scales its own reasoning.
  - **Cross-family review.** OpenAI models (Astra above all) are better or more exhaustive reviewers; Claude models (Fable, Opus 5.5) are preferred writers of code.
  - **Use OpenAI/Codex for computer use on macOS** rather than Claude.
  - **Prompt wider and fire-and-forget**, on remote or isolated machines.
  - **Expect premature stops.** Both Opus 5.5 and Fable 5.1 sometimes stop and summarize instead of continuing. The fix is the same: name the stops, nudge to finish, or use a skill.
  - **Subagents.** Both endorse them for large work. Fable and Astra run a lead plus subagents in parallel well. Opus 5.5 needs explicit permission to use subagents at all.
  - **Avoid "reasoning"-revealing requests and base64.** Both relate to safeguard false positives.
- **Nuances to keep:**
  - **Opus 5.5 benefits from explicit structure:** named stops, explicit negatives, an explicit subagent grant, and explicit "do all phases". Fable 5.1 is described as needing less of that.
  - **Design.** Fable designs better unprompted. Opus 5.5 needs a concrete anti-pattern list.
  - **Communication style.** Fable 5.1 is quiet by default, with few progress updates. Opus 5.5 "will keep you posted" and sometimes stops to report.
  - **Review on the speaker's bench.** Fable found few but well-vetted issues. Opus 5.5 roughly doubled Opus 5 with no contradicted findings. Astra and Grok 4.7 found more.
