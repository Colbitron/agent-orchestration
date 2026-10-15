# Claude Supplemental: "How to use the model well" videos

**Sources**

- OPUSG: "Getting the most out of Opus 5.5", Theo (t3.gg), YouTube, https://youtu.be/ejjBbaq9RmY
- FABG: "So I was using Fable wrong...", Theo (t3.gg), YouTube, https://youtu.be/-XWSJM-Ue-o

A citation `[KEY m:ss]` links to that video at that timestamp (the start of the caption segment, so the passage can begin a few seconds later). Video 1 below is OPUSG and Video 2 is FABG. This note records the conclusions, rules, numbers and prompt patterns the kit relies on; it is not a substitute for watching the videos.

**Notes on the transcripts**

- **Speaker.** Both videos are by Theo. He builds "T3 Code" and "T3 Chat", his sponsor links use the `soy.link` domain, and he mentions a skill that posts PR comments "on Theo's behalf". The section headings below are descriptive; the videos' actual titles are in Sources.
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
- **Timing.** The Fable video was clearly recorded **before Opus 5.5 shipped**. In it the speaker calls the then-current Opus 5 "not a good model" and says an Opus "5.1 or 5.2" is "coming soon" [FABG 4:59](https://youtu.be/-XWSJM-Ue-o?t=299). The Opus 5.5 video is later.
- **Sponsor segments.** Both videos contain sponsor reads (Browserbase in the first; Sentry and General Translation in the second). These are excluded below except where they touch on the substance.

---

# Video 1: Getting the most out of Opus 5.5

## 1. Subject and thesis

- Theo comments on a guide to Opus 5.5 by **Addy Osmani** ("used to be part of the Chrome team, recently joined Anthropic") and adds examples from his T3 Code work [OPUSG 0:25](https://youtu.be/ejjBbaq9RmY?t=25). The guide's framing: "It works for longer on its own. It tells you plainly what it did, and it thinks before every reply." [OPUSG 2:35](https://youtu.be/ejjBbaq9RmY?t=155)
- **Thesis:** agents need "more leash": the ability to verify their changes, to be "told when done is done", and trust to do the work [OPUSG 28:01](https://youtu.be/ejjBbaq9RmY?t=1681). Give it what it needs "to trust its own work" and "the further it can go" [OPUSG 28:28](https://youtu.be/ejjBbaq9RmY?t=1708). Last line: "do not touch max mode" [OPUSG 28:35](https://youtu.be/ejjBbaq9RmY?t=1715).
- **Verdict:** very good code, pleasant to work with, "stays on task for long work", "as long as you don't use Macs" (weak macOS computer use; Video 2 says so explicitly) [OPUSG 0:05](https://youtu.be/ejjBbaq9RmY?t=5).

## 2. Concrete workflow the speaker uses

**Runaway max run.** At **max**, an Opus 5.5 thread ran **6.5 hours** without finishing [OPUSG 4:21](https://youtu.be/ejjBbaq9RmY?t=261). After switching to **high** and saying "continue", it finished in about **10 minutes** [OPUSG 5:00](https://youtu.be/ejjBbaq9RmY?t=300).

**Prompt pattern for handing over a setup task.** He had the model move a run to a remote machine rather than doing the SSH, clone and env-var work himself; it took about **17 minutes** [OPUSG 9:19](https://youtu.be/ejjBbaq9RmY?t=559) and surfaced real connection issues [OPUSG 8:57](https://youtu.be/ejjBbaq9RmY?t=537). The pattern:

- **Say how to connect**, so it doesn't improvise "anything sketchy" or trip a security flag [OPUSG 5:53](https://youtu.be/ejjBbaq9RmY?t=353).
- **"Make sure" plus numbered checks:** do it, validate it, and report if it fails [OPUSG 6:18](https://youtu.be/ejjBbaq9RmY?t=378).
- **Pre-authorize** steps it would otherwise stop to ask about, such as copying env vars [OPUSG 6:26](https://youtu.be/ejjBbaq9RmY?t=386).
- **State the goal:** the whole job in one pass, with as many subagents as needed [OPUSG 6:48](https://youtu.be/ejjBbaq9RmY?t=408).
- **State negatives:** "being explicit about what you don't want is even better" [OPUSG 7:06](https://youtu.be/ejjBbaq9RmY?t=426). Here: no computer use on his machine while he works on it.
- **Give an out** ("don't hesitate to ask questions"), which he ranks as the most important part. Models are trained hard not to give up, so without one they answer their own questions and push on [OPUSG 8:02](https://youtu.be/ejjBbaq9RmY?t=482), [OPUSG 8:11](https://youtu.be/ejjBbaq9RmY?t=491).

**Phase-0 lesson.** "Follow its phase 0 to 7 in order" still stopped after phase 0 [OPUSG 9:39](https://youtu.be/ejjBbaq9RmY?t=579). The fix: hold all questions until the end, forbid stopping between phases for permission, require every phase, report only with a concrete artifact ("a Tailscale link I can click on"), and say what not to worry about (hosting, build) [OPUSG 9:53](https://youtu.be/ejjBbaq9RmY?t=593), [OPUSG 10:11](https://youtu.be/ejjBbaq9RmY?t=611).

**Stop rule deployment.** He added the guide's stop rule (section 6) to his CLAUDE.md and had the agent commit and push it to his other machines [OPUSG 19:03](https://youtu.be/ejjBbaq9RmY?t=1143), [OPUSG 19:29](https://youtu.be/ejjBbaq9RmY?t=1169).

**Post-run check-ins.** Ask what it needs from you ("What do you need from me?") [OPUSG 21:48](https://youtu.be/ejjBbaq9RmY?t=1308) and what merging risks. "What are the risks of merging this code today?" is his most common prompt [OPUSG 21:54](https://youtu.be/ejjBbaq9RmY?t=1314); he also asks for the worst case if it merged now [OPUSG 22:16](https://youtu.be/ejjBbaq9RmY?t=1336). The answers decide whether a roughly 300-line agent PR deserves his own read [OPUSG 22:07](https://youtu.be/ejjBbaq9RmY?t=1327).

**Design iteration loop.** List specific styles to avoid; if you dislike something it added, "put that on the list, and then ask again". Or paste an annotated screenshot (he uses "Shotter") with "This sucks. Make it better.", which "works way better than you would think" [OPUSG 17:59](https://youtu.be/ejjBbaq9RmY?t=1079).

## 3. Prompting guidance

**What to say**

- **Hand over the whole task and name the finish line.** The first of the guide's "three things to try in your first sessions" [OPUSG 2:50](https://youtu.be/ejjBbaq9RmY?t=170). Theo calls it "prompting wider": the model should "come in earlier and go further", which depends on "defining good done states" [OPUSG 3:02](https://youtu.be/ejjBbaq9RmY?t=182). Not "start working on this feature" but three named things, verified by a screenshot, then a PR that includes it [OPUSG 3:11](https://youtu.be/ejjBbaq9RmY?t=191). Guide: "say what done looks like then let it run", whole task in one message [OPUSG 10:47](https://youtu.be/ejjBbaq9RmY?t=647); without a finish line Opus 5.5 "might still stop to ask for permission" or "might just randomly stop" [OPUSG 11:02](https://youtu.be/ejjBbaq9RmY?t=662).
- **The other two first-session tips:** delete "think carefully" lines [OPUSG 3:48](https://youtu.be/ejjBbaq9RmY?t=228), and when long runs end, read what it needs from you first. The model usually says, but "it does sometimes miss this", so he prompts for it [OPUSG 4:11](https://youtu.be/ejjBbaq9RmY?t=251).
- **The guide's canonical example**, "the perfect simple one two three": what you want, what done means, and the out [OPUSG 11:32](https://youtu.be/ejjBbaq9RmY?t=692):
  > "Migrate the payments endpoint from the old client to the new one. Done means every endpoint uses the new client, the old one is deleted, and the test suite passes. Stop and ask me only if a test fails for a reason that you can't explain." [OPUSG 11:18](https://youtu.be/ejjBbaq9RmY?t=678)
- **The section 2 patterns:** "make sure X" (do and validate); pre-authorize expected risky actions; say what you don't want, which he values above saying what you do; give an out; for uninterrupted runs, hold questions to the end and forbid per-phase stops; make the deliverable concrete and checkable; say what not to worry about. Grant subagents explicitly (section 5).
- **Attach screenshots and charts.** Checklist: "Charts and screenshots should be attached." [OPUSG 27:27](https://youtu.be/ejjBbaq9RmY?t=1647) "People underrate how useful screenshotting is": he screenshots the browser instead of pasting errors, and Claude Code crops a too-high-resolution screenshot to the area it needs [OPUSG 27:40](https://youtu.be/ejjBbaq9RmY?t=1660).
- **Steer mid-run instead of restarting.** Guide: "If you remember something midrun, you can type a follow-up while it works", because "the runs are longer, so going back to the start is more expensive" [OPUSG 14:54](https://youtu.be/ejjBbaq9RmY?t=894). He no longer stops and re-pastes into a new thread; "Opus, Fable, Sol kind of, and Astra mostly" steer well [OPUSG 15:20](https://youtu.be/ejjBbaq9RmY?t=920). Old RL was per message, so adding a forgotten task three got three done and one, two and four dropped; models now treat interruptions as steering, not as a reason to stop or to treat earlier work as done [OPUSG 15:36](https://youtu.be/ejjBbaq9RmY?t=936).

**What NOT to say**

- **"Think hard" / "think deeply" / "think carefully".** "The models are pretty good at knowing how much to think." [OPUSG 11:50](https://youtu.be/ejjBbaq9RmY?t=710) Checklist: "Don't tell it to think hard, it will anyways." [OPUSG 27:19](https://youtu.be/ejjBbaq9RmY?t=1639)
- **Generic design negatives.** Guide: "A general instruction like avoid generic looks will mostly just swap one default for another. **A list of specific patterns will work much better.**" [OPUSG 17:27](https://youtu.be/ejjBbaq9RmY?t=1047)
- **"Show your reasoning" / "What was your reasoning for these changes?"** The guide warns against it [OPUSG 26:47](https://youtu.be/ejjBbaq9RmY?t=1607). Theo's reading: Anthropic hides reasoning traces to prevent distillation, so "anything that matches reasoning is risking getting a flag" [OPUSG 27:13](https://youtu.be/ejjBbaq9RmY?t=1633). Annoying, since it is his natural way to ask why it did something.

**Design prompting (specific to Opus 5.5)**

- On the WitchAI front-end showcase ("built by DRA"; the name is as transcribed), **Fable 5.1 produced clearly better designs than Opus 5.5**: "the Fable version is obviously better and nicer" [OPUSG 16:43](https://youtu.be/ejjBbaq9RmY?t=1003).
- Opus 5.5 is "much better at going the right direction with design instructions": say what you want and, more importantly, what you don't [OPUSG 16:57](https://youtu.be/ejjBbaq9RmY?t=1017). Guide: "with no design direction, Opus 5.5 will fall back on a few default styles." [OPUSG 17:23](https://youtu.be/ejjBbaq9RmY?t=1043) Its example:
  > "Build a personal website with placeholder content. Don't use a cream or off-white background, italic accent words in headings, numbered 1, 2, 3 section labels, monospace labels, or pill-shaped buttons." [OPUSG 17:35](https://youtu.be/ejjBbaq9RmY?t=1055)
- Theo: you shouldn't need that many negatives, but "**When you tell it to not do a thing, it won't do the thing.**" [OPUSG 17:51](https://youtu.be/ejjBbaq9RmY?t=1071) Checklist: "Design requests should have the styles to leave out as well as what you want it to look like." [OPUSG 27:22](https://youtu.be/ejjBbaq9RmY?t=1642)

**Context amount.** Plenty about the environment (how to connect, what tools exist, what is permitted), little about method; the plan lives in a file (`overhaul.md`) the prompt points to [OPUSG 9:39](https://youtu.be/ejjBbaq9RmY?t=579).

## 4. Pitfalls and misconceptions corrected

- **Max reasoning is a trap**, the strongest claim in the video. Effort levels mean "think up to this much", not "think this much": low and medium cap early, high and xhigh are "much higher caps" [OPUSG 12:06](https://youtu.be/ejjBbaq9RmY?t=726). Max does not just let the model think more: "**It is removing its ability to think less.**" [OPUSG 12:30](https://youtu.be/ejjBbaq9RmY?t=750) The other levels "just change the ceiling"; "Max is a will" [OPUSG 14:06](https://youtu.be/ejjBbaq9RmY?t=846). Addy is working on improving max in Claude Code [OPUSG 12:41](https://youtu.be/ejjBbaq9RmY?t=761).
- **SkateBench data (Opus 5.5, xhigh vs max)**, a benchmark he calls "admittedly kind of silly" [OPUSG 12:57](https://youtu.be/ejjBbaq9RmY?t=777):

  | Metric | xhigh | max |
  |---|---|---|
  | Avg tokens per response | 338 | ~5,000 (more than 10x) |
  | Avg duration | 6 s | 50 s |
  | Slowest response | 31 s | 600 s (about 20x slower) |
  | Accuracy | 78% | 79% (+1 correct answer) |

  For one extra correct answer, max cost 13x as much, burned 15x the tokens and was 20x slower at worst: "And I got jack out of it." [OPUSG 13:40](https://youtu.be/ejjBbaq9RmY?t=820) The average max run took longer than the slowest xhigh run [OPUSG 13:24](https://youtu.be/ejjBbaq9RmY?t=804). Max might help on trick questions ("Perhaps"), but "I still don't think you should ever use max reasoning." [OPUSG 13:52](https://youtu.be/ejjBbaq9RmY?t=832)
- **High vs xhigh.** "They're both fine… I can barely notice the difference." xhigh takes a little longer; high "sometimes misses like smaller details"; "Not that big of a gap." He leaves it on high or xhigh [OPUSG 14:32](https://youtu.be/ejjBbaq9RmY?t=872).
- **Low effort.** "Low kind of sucks": the model needs some thinking, which is why there is no no-reasoning version [OPUSG 14:22](https://youtu.be/ejjBbaq9RmY?t=862)
- **Opus 5.5 still stops early sometimes.** Guide: "On long tasks, it'll sometimes stop to report instead of going on: a summary that names the next step without taking it, an offer to continue, or a list of choices that don't actually block the work." [OPUSG 18:31](https://youtu.be/ejjBbaq9RmY?t=1111) Fixes: name the stops in CLAUDE.md (section 6), and reply "continue" to "Want me to continue?" [OPUSG 19:46](https://youtu.be/ejjBbaq9RmY?t=1186). Even "phase 0 to 7 in order" stopped after phase 0 (section 2).
- **Opus 5.5 is reluctant to use subagents** unless told it can (section 5).
- **Long or computer-use agents on your own machine** pop up windows (he names Codex). Running them on other boxes made him like computer use "a lot more" [OPUSG 7:22](https://youtu.be/ejjBbaq9RmY?t=442).
- **Safety flags.** Guide: "Opus 5.5 is the first Opus model to launch with Fable-level bio and cyber safeguards in Claude apps as well as Claude Code. Most flagged messages move to older models and your work goes on there." [OPUSG 25:55](https://youtu.be/ejjBbaq9RmY?t=1555) Finding security vulnerabilities in source code "is allowed"; everyday health and educational questions should still work. In the apps a notice says you were switched and the chat stays on that model; reselecting 5.5 "might work, it might flag again", and a new chat should avoid it; a setting turns off auto-switch so you get a pause or an error [OPUSG 26:23](https://youtu.be/ejjBbaq9RmY?t=1583). Theo: "It doesn't seem like that big a deal." [OPUSG 26:41](https://youtu.be/ejjBbaq9RmY?t=1601)

## 5. Subagents, orchestration, delegation, verification, review, model choice

- **Split big work across subagents (guide)** for "audits, migrations, reviews across large codebases", to fit the context window and explore in parallel [OPUSG 20:24](https://youtu.be/ejjBbaq9RmY?t=1224). "Early testers had Opus 5.5 coordinate parallel subagents on long audits with little oversight and it was successful." [OPUSG 20:37](https://youtu.be/ejjBbaq9RmY?t=1237)
- **Opus 5.5 is reluctant to use subagents** (Theo, not the guide): it "seems less willing to spin up subagents unless you tell it that it can" [OPUSG 20:42](https://youtu.be/ejjBbaq9RmY?t=1242). He appends "**Use subagents and workflows however you choose. I trust your judgment there.**" "Even then it doesn't always do it", so for known-parallel work (a giant pile of PR reviews, a codebase audit) tell it to use them [OPUSG 20:51](https://youtu.be/ejjBbaq9RmY?t=1251).
- **Checking results (guide).** "Look first for anything Claude is waiting on you for, like a decision it left open or a change it wants you to approve. Then read the rest of the Claude summary." [OPUSG 21:11](https://youtu.be/ejjBbaq9RmY?t=1271) Opus 5.5 reports more clearly than Opus 5: "what they did, what they found, and what it needs from you in plain language" [OPUSG 21:27](https://youtu.be/ejjBbaq9RmY?t=1287).
- **Suggested CLAUDE.md report format (guide).** "End every run with three headings: **Blocked on me, Changed, and Found.**" Theo doesn't use it: "When I do want this, I usually just ask." [OPUSG 21:33](https://youtu.be/ejjBbaq9RmY?t=1293)
- **Cross-family review is valuable.** "Swapping between model families and labs is actually pretty useful." OpenAI models are "better at review still": they "won't let go", report "more stuff that doesn't matter", and occasionally find things "the Claude models just miss entirely" [OPUSG 22:44](https://youtu.be/ejjBbaq9RmY?t=1364). He wants Astra or Sol, not only Opus, reviewing Opus code [OPUSG 23:01](https://youtu.be/ejjBbaq9RmY?t=1381), and says "consider using Grok for your reviews, too" [OPUSG 24:36](https://youtu.be/ejjBbaq9RmY?t=1476).
- **His informal review "bench"** ("in quotes"): finding areas of improvement in the T3 Code codebase, scored by a judge panel into supported, unresolved and contradicted findings [OPUSG 23:16](https://youtu.be/ejjBbaq9RmY?t=1396). As transcribed:

  | Model | Findings | Speaker's assessment |
  |---|---|---|
  | GPT-6 Astra | 8 supported | "substantiated and supported its claims" |
  | Grok 4.7 | 8 supported | Came **second** overall, which surprised him |
  | GPT-6.1 Sol | 9 | Judged lower quality: "apparently they weren't quite as valid" |
  | Fable | 5 across two runs | "quite a bit lower": vetted, "they all matter", but it "didn't find as much" |
  | Opus 5.5 | not stated | "almost twice as successful" as Opus 5, no unresolved or contradicted findings |
  | Opus 5 | 4 supported, 2 not | one junk finding for every two valid ones |

  Rows from [OPUSG 23:26](https://youtu.be/ejjBbaq9RmY?t=1406) to [OPUSG 24:21](https://youtu.be/ejjBbaq9RmY?t=1461). The exact rank order beyond "Grok second" is not fully stated in the transcript.
- **Verification during review.** "Ask the model to **mark the things that it can't confirm**." Ideally give it a browser, computer use on the running system, or a test suite it can use or build. Some things can't be verified (other hardware, an env var, a subjective call), but ask it to list what it couldn't verify and "it will" [OPUSG 24:41](https://youtu.be/ejjBbaq9RmY?t=1481), [OPUSG 25:11](https://youtu.be/ejjBbaq9RmY?t=1511).
- **State of play.** The models know your codebase, work autonomously and verify their changes, but "**They don't know how to work with a human yet.**" Tell them how to work with you and they usually deliver, "especially models like Opus 5.5, Fable 5.1, and GPT-6 Astra mostly" [OPUSG 25:24](https://youtu.be/ejjBbaq9RmY?t=1524).

## 6. Claude Code specifics

- **CLAUDE.md stop rule**, the guide's text, which Theo pasted into his CLAUDE.md under "approvals":
  > "When a step doesn't need my input, keep going. Put status notes in the same message as your next action. Stop and ask only when you can't continue without me or before anything destructive: deleting data, force pushing, or changing anything outside of this repo." [OPUSG 18:47](https://youtu.be/ejjBbaq9RmY?t=1127)

  Guide: "It follows instructions that name the stops. So name the stops that you want." [OPUSG 18:43](https://youtu.be/ejjBbaq9RmY?t=1123) "A rule to keep going means fewer stops. So keep your own check before anything risky or hard to undo. The last line of the rule above does that." [OPUSG 19:52](https://youtu.be/ejjBbaq9RmY?t=1192)
- **The opposite configuration**, for pair programming: "a one-line plan before it starts and a short recap at the end". Theo prefers keep-going [OPUSG 19:59](https://youtu.be/ejjBbaq9RmY?t=1199).
- **Covered above:** report headings (section 5, guide only); screenshot auto-crop (section 3); the model switch on a flag and the setting to disable it (section 4); pushing CLAUDE.md to a fleet via the agent (section 2).
- **Harness.** Opus 5.5 through Claude Code, surfaced in T3 Code; remote machines reached through a "fleet" repo; a Tailscale link as the test deliverable [OPUSG 6:10](https://youtu.be/ejjBbaq9RmY?t=370), [OPUSG 10:11](https://youtu.be/ejjBbaq9RmY?t=611).

## 7. Model comparisons

- **Design.** Fable 5.1 is better with no direction; Opus 5.5 is very good given explicit positive and negative style direction [OPUSG 16:57](https://youtu.be/ejjBbaq9RmY?t=1017).
- **Review.** OpenAI models (Astra, Sol) and even Grok 4.7 find more issues; Claude models (Fable, Opus) find fewer but well-vetted ones; Opus 5.5 is roughly twice as good as Opus 5 [OPUSG 23:39](https://youtu.be/ejjBbaq9RmY?t=1419), [OPUSG 24:09](https://youtu.be/ejjBbaq9RmY?t=1449). He prefers "coding with Fable and Opus", but Astra's review quality "is also really solid" [OPUSG 24:27](https://youtu.be/ejjBbaq9RmY?t=1467).
- **Coding preference.** Fable and Opus (same passage).
- **Steering mid-run.** Opus, Fable, "Sol kind of, and Astra mostly" [OPUSG 15:20](https://youtu.be/ejjBbaq9RmY?t=920).
- **Following human-collaboration instructions.** Opus 5.5, Fable 5.1, and "GPT-6 Astra mostly" [OPUSG 25:35](https://youtu.be/ejjBbaq9RmY?t=1535).
- **Opus 5.5 vs Opus 5.** 5.5 reports more clearly and is much better at review [OPUSG 21:20](https://youtu.be/ejjBbaq9RmY?t=1280), [OPUSG 24:09](https://youtu.be/ejjBbaq9RmY?t=1449).
- **Computer use.** "As long as you don't use Macs" implies weak macOS computer use [OPUSG 0:05](https://youtu.be/ejjBbaq9RmY?t=5); ambiguous here, explicit in Video 2.

## 8. Routing-table and orchestrator-prompt implications

**(a) Which tasks go to which model**

1. **Opus 5.5 is a strong long-running implementation model.** It suits multi-phase plans, migrations and fleet or devops setup, provided the prompt names a finish line (sections 2 and 3).
2. **Do not route anything to Opus 5.5 at max effort.**
   - Default to **high**, or **xhigh** for detail-sensitive work.
   - Avoid **low**: "low kind of sucks".
   - The SkateBench numbers (13x cost, 15x tokens, 20x worst-case latency, +1 point of accuracy) make max effort a bad default for any orchestrated call (section 4).
3. **UI and design generation.** Prefer **Fable 5.1** when the design brief is open-ended. Use **Opus 5.5** only when the orchestrator can supply a concrete style spec that includes an explicit list of patterns to avoid (section 3).
4. **Code review should go across model families.** Route review of Claude-written code to an **OpenAI model (GPT-6 Astra preferred, GPT-6.1 Sol second)**, possibly **Grok**. Keep Claude (Fable or Opus 5.5) as the filter for high-precision, low-noise findings. Expect OpenAI reviewers to be noisier, with more items that don't matter (section 5).
5. **Large audits, mass PR review and big migrations** should use subagent fan-out. If Opus 5.5 is the lead, it must be told explicitly to use subagents (section 5).
6. **Avoid macOS computer use with Opus 5.5.** Prefer running agents on remote or isolated machines (sections 1 and 4).

**(b) How the orchestrator should write prompts to the model**

1. **Every delegated prompt should have three parts.** (1) What you want. (2) "Done means …", given as concrete, checkable conditions such as tests pass, the old code is deleted, a PR is filed, a screenshot or link is provided. (3) The "out": "Stop and ask only if …" [OPUSG 11:32](https://youtu.be/ejjBbaq9RmY?t=692).
2. **Remove "think hard / think carefully" from all prompt templates.** Never ask the model to "show your reasoning". Ask "explain why you made these changes" instead, because "reasoning" wording risks safety flags (section 3).
3. **Pre-authorize expected sensitive actions** (env var copying, connecting to machine X via Y) and give the connection method, so the model doesn't stall or improvise something sketchy (section 2).
4. **State explicit negatives** ("don't spam my machine with browser control", the design anti-patterns), not just goals (sections 2 and 3).
5. **For multi-phase plans, say so explicitly.** "Do all phases 0–N; don't stop between phases to ask permission; hold questions until the end; don't report until you have <concrete artifact>." The speaker's first attempt without this stopped after phase 0 (section 2).
6. **Include a subagent grant** in lead-agent prompts: "Use subagents and workflows however you choose. I trust your judgment there." For tasks that are known to parallelize, give a direct instruction to use subagents (section 5).
7. **Write a standing "named stops" rule** into the orchestrated model's CLAUDE.md or system prompt. Use the rule quoted in section 6: keep going, put status notes with the next action, and stop only when blocked or before destructive or out-of-repo actions. Also have the orchestrator auto-reply "continue" to non-blocking "Want me to continue?" endings.
8. **Ask for a structured end-of-run report**, using either the guide's "Blocked on me / Changed / Found" headings or the speaker's questions ("What do you need from me?", "What are the risks of merging this today?", "What's the worst thing that would happen if we merge this right now?"). The orchestrator should parse "Blocked on me" first (sections 2 and 5).
9. **Review and verify prompts should require marking claims it couldn't confirm**, with the reason. Wherever possible, give the reviewer verification tools: browser, tests, a runnable system (section 5).
10. **Prefer steering a running agent over restarting it** when requirements change. Current models treat mid-run messages as additions, not replacements (section 3).

---

# Video 2: Using Fable 5.1 correctly

## 1. Subject and thesis

- Theo walks through **Anthropic's official "Prompting Claude Fable 5.1" doc** ("actually really good and has a bunch of insights"), combined with about a month of heavy use ("burning my five accounts to the ground") [FABG 1:05](https://youtu.be/-XWSJM-Ue-o?t=65). Topics include fixing AGENTS.md, giving the model tools to keep going, and using Codex to improve Claude's output [FABG 1:33](https://youtu.be/-XWSJM-Ue-o?t=93).
- **Why he prefers Fable over GPT-6 Astra.** Fable is "less noisy by far"; Astra's peaks can be "way higher" but its dips "way, way worse" [FABG 0:22](https://youtu.be/-XWSJM-Ue-o?t=22). Consistency lets the model "go longer and do more in a given pass" and "come back with a video when it's done"; the remaining dips "hurt more", so reducing them is valuable [FABG 0:40](https://youtu.be/-XWSJM-Ue-o?t=40).
- **Thesis: reset your mental model.** Strip out workarounds built for weaker models [FABG 26:15](https://youtu.be/-XWSJM-Ue-o?t=1575). Customization done to work around flaws is "probably out of date", and so is your mental model: "Reset it." [FABG 40:36](https://youtu.be/-XWSJM-Ue-o?t=2436) You're not "seeing the benefits of Fable if you're not prompting a bit wider": start earlier, go longer, offer different paths [FABG 28:03](https://youtu.be/-XWSJM-Ue-o?t=1683).

## 2. Concrete workflow the speaker uses

- **Fire and forget in T3 Code.** Command-Shift-O, pick the repo, say what he wants, go check another thread [FABG 9:12](https://youtu.be/-XWSJM-Ue-o?t=552). The goal is "to minimize the amount of times I go back to a thread" until the work is done; he returns on "the little marker in T3 Code" [FABG 27:38](https://youtu.be/-XWSJM-Ue-o?t=1658).
- **The "babysit PR" skill.** Purpose: when told to watch or babysit a PR, keep checking for new comments and checks so the PR is ready when he looks [FABG 14:39](https://youtu.be/-XWSJM-Ue-o?t=879). Its core rules, in our words [FABG 14:52](https://youtu.be/-XWSJM-Ue-o?t=892):
  - Treat review-bot findings as leads: check each against the code, then fix the real ones and any CI failures.
  - Respond only to feedback that arrived after the latest push, and keep the branch current with main.
  - Answer and resolve findings not worth fixing; ask before closing a PR another one has made obsolete, unless closing was authorized.
  - Post comments through a separate skill that adds a note saying an AI agent wrote them [FABG 15:26](https://youtu.be/-XWSJM-Ue-o?t=926).
  - Scope lines added because Sol drifted while babysitting: "Please don't scope creep", only address real shortcomings, and "don't post filler comments" [FABG 15:42](https://youtu.be/-XWSJM-Ue-o?t=942).
- **A "modernize" skill** keeps a PR up to date on top of main [FABG 18:05](https://youtu.be/-XWSJM-Ue-o?t=1085).
- **Bug to PR, then a decision handed to the model.** With a screenshot and a thread ID he asked Fable to "figure out everything that went wrong" in a T3 Code thread, find the root causes from the tool-call history, and "File a single PR that clearly and simply addresses the issues." [FABG 16:22](https://youtu.be/-XWSJM-Ue-o?t=982) When a contributor claimed their closed PR was better, he gave a branching follow-up (if theirs is better, reopen or take its commits; if ours, finish modernizing) ending "Babysit whatever ends up being put up as necessary." [FABG 17:06](https://youtu.be/-XWSJM-Ue-o?t=1026) That is "the key part": "I gave it the freedom to do what it decided based on the data" [FABG 17:24](https://youtu.be/-XWSJM-Ue-o?t=1044). Fable picked the other PR as the base, took two things from it, fixed bugs it found, modernized and handled reviews; he clicked merge himself [FABG 17:59](https://youtu.be/-XWSJM-Ue-o?t=1079). Takeaway: "**less time trying to choose from the options the model gave me**", more time giving it what it needs to choose [FABG 17:35](https://youtu.be/-XWSJM-Ue-o?t=1055).
- **A "YOLO" run on LakeBed**, his side-project cloud; only for codebases with strong staging, QA and testing [FABG 18:36](https://youtu.be/-XWSJM-Ue-o?t=1116). Astra had written the change, a fork of a Rust V8 runtime of roughly 26,000 lines [FABG 19:15](https://youtu.be/-XWSJM-Ue-o?t=1155). What it shows:
  - **Ask for an honest merge verdict.** Fable said not ready and listed concrete risks: one-way-door migration, three features in one PR, no human approval, the default flipped to native, a headline number that didn't prove live queries, unexplained failures [FABG 19:47](https://youtu.be/-XWSJM-Ue-o?t=1187).
  - **Ask where its debugging ability ends.** It could partly debug crashes, latency and resource problems in staging but "couldn't confidently debug wrong query results" [FABG 20:57](https://youtu.be/-XWSJM-Ue-o?t=1257). It named what staging lacked (signals when maintained views are wrong, reproduction paths, traffic) and what would close the gap (shadow mode, structured reasons on refresh failures, synthetic traffic, runtime counters on the health endpoint) [FABG 21:20](https://youtu.be/-XWSJM-Ue-o?t=1280).
  - **Durations.** Building those measures took **60 minutes** and opened no PR because none was requested [FABG 22:01](https://youtu.be/-XWSJM-Ue-o?t=1321). A conditional merge instruction ("If so, merge 28 into 200…") ran **1 hour 34 minutes** at **medium** reasoning [FABG 22:25](https://youtu.be/-XWSJM-Ue-o?t=1345), [FABG 22:39](https://youtu.be/-XWSJM-Ue-o?t=1359). Turning off shadow mode and measuring against production took **42 minutes** [FABG 23:31](https://youtu.be/-XWSJM-Ue-o?t=1411).
  - **Say where heavy work runs.** It hammered his home IP until told to spin up a container instead [FABG 22:45](https://youtu.be/-XWSJM-Ue-o?t=1365).
  - **Retrospective rule:** diff size is not the risk. After a differential test forced 1,400 reseeds in 160 steps with no wrong answer, Fable concluded "the real risk was operational" [FABG 24:11](https://youtu.be/-XWSJM-Ue-o?t=1451). A follow-up PR (PR 212, an engine pre-warm) ended on a merge-when-green end state and needed no further input from him [FABG 24:46](https://youtu.be/-XWSJM-Ue-o?t=1486).

## 3. Prompting guidance

**End states are the key takeaway.** "**Every prompt should have a pretty clear place where it stops when it's done.**" [FABG 27:05](https://youtu.be/-XWSJM-Ue-o?t=1625) His variants [FABG 26:41](https://youtu.be/-XWSJM-Ue-o?t=1601):

- "I want you to babysit it till everything is green."
- "I want you to wait till it's green, then merge it."
- "File the PR and tell me when it's up."
- "Merge it once you've got everything green and you're happy with your changes."
- A question plus a conditional action: "If so, merge these things in and test it." [FABG 27:18](https://youtu.be/-XWSJM-Ue-o?t=1638)

**Branching end states.** Two paths so either outcome is useful without him: it isn't happy and comes back to discuss, or it "will keep going for an hour and a half straight without my intervention" [FABG 27:44](https://youtu.be/-XWSJM-Ue-o?t=1664). **Let the model choose:** give it the data and the alternatives, not a fixed path (section 2).

**Don't over-specify checks the model can do itself.** If the model can root-cause, fix, verify, film a video, open a PR, address reviews and report, and you walk those steps with it, you are the one "who would write the type check after the type check" [FABG 29:07](https://youtu.be/-XWSJM-Ue-o?t=1747). Double-checking is sometimes warranted, but "I don't think it's as common as y'all believe." [FABG 29:44](https://youtu.be/-XWSJM-Ue-o?t=1784)

**Ask honest-assessment questions:** "Is this ready to merge? Give me your honest thoughts." "How can we de-risk this?" "Would you confidently be able to debug …?" "How do you feel about these changes in the end?" [FABG 19:40](https://youtu.be/-XWSJM-Ue-o?t=1180), [FABG 20:13](https://youtu.be/-XWSJM-Ue-o?t=1213), [FABG 20:44](https://youtu.be/-XWSJM-Ue-o?t=1244), [FABG 23:48](https://youtu.be/-XWSJM-Ue-o?t=1428). The style "is going to drive half of y'all … insane. It works." [FABG 23:42](https://youtu.be/-XWSJM-Ue-o?t=1422)

**Points from the official Fable 5.1 doc, with his commentary:**

- **Effort levels.**
  - Doc: "start at high", then test others against your own evals [FABG 5:28](https://youtu.be/-XWSJM-Ue-o?t=328). Theo: "I honestly recommend just kind of gut feeling it." [FABG 5:47](https://youtu.be/-XWSJM-Ue-o?t=347)
  - **His defaults:** high; xhigh "on really deep, thorough things"; "almost never" max, "unless I'm just trying to like burn a limit" [FABG 5:59](https://youtu.be/-XWSJM-Ue-o?t=359). He avoids low and medium: they fail often enough that redoing on medium or high costs more tokens [FABG 6:18](https://youtu.be/-XWSJM-Ue-o?t=378).
  - **High on simple tasks is cheap**; it won't "waste more reasoning if it doesn't need to" ("Hi, how are you doing today?" at max stayed short) [FABG 6:30](https://youtu.be/-XWSJM-Ue-o?t=390).
  - **Adapting to task size:** Fable does it "well enough", Astra better. On SkateBench, Astra's max vs low gap was only about 50 tokens (roughly 130 vs 180); Gemini 3.1 Pro used "a thousand plus reasoning tokens" for the same task [FABG 7:11](https://youtu.be/-XWSJM-Ue-o?t=431).
  - **Low or medium** only to stop earlier or not go too deep, for example on a known rabbit hole [FABG 7:40](https://youtu.be/-XWSJM-Ue-o?t=460). **Medium can still go long:** the 1.5-hour LakeBed run was on medium [FABG 22:39](https://youtu.be/-XWSJM-Ue-o?t=1359).
- **User-facing progress updates.**
  - **Changed in 5.1:** "way fewer user-facing updates during long tool-call turns" than Fable 5 [FABG 8:47](https://youtu.be/-XWSJM-Ue-o?t=527). He has seen about 150 tool calls with no update and doesn't mind: "I just want to see it when it's done." [FABG 8:55](https://youtu.be/-XWSJM-Ue-o?t=535)
  - **If you want updates or reasons, ask for them.** Asking is enough for "deep behavioral change" [FABG 9:30](https://youtu.be/-XWSJM-Ue-o?t=570). The doc's suggested system-prompt text:
    > "Before you start, say in a line what you're about to do. Brief updates while you work help the user follow along. Close with a short recap that stands on its own — what you found, what you did, and what's next — so a reader who only sees the last message has the full picture." [FABG 9:37](https://youtu.be/-XWSJM-Ue-o?t=577)
  - **If your UI hides tool outputs, tell the model**, "because otherwise it won't show things because it expects the UI to show it" [FABG 10:03](https://youtu.be/-XWSJM-Ue-o?t=603).
- **Writing density and "mannered prose".**
  - Fable 5.1 is "a step up from earlier Claude models with fewer stock phrases and less unexplained jargon", but denser: "sentences run longer and there are fewer paragraph breaks" [FABG 10:57](https://youtu.be/-XWSJM-Ue-o?t=657).
  - Define mannered prose as an anti-pattern in the system prompt or a user message, **user message preferred** [FABG 11:15](https://youtu.be/-XWSJM-Ue-o?t=675). The doc's definition:
    > "Mannered prose substitutes metaphor and flourish for direct statements. Instead of 'a parameter worth varying,' the mannered writer would produce 'a dial worth turning.' Instead of 'this point still matters,' they write 'this point earns its keep.' The phrase exists to display the writer, not to convey the idea, and the reader can tell. This is why mannered prose irritates. It makes the reader work harder so the writer can perform." [FABG 11:22](https://youtu.be/-XWSJM-Ue-o?t=682)
  - **His shortcut:** "Please remove all mannered prose." [FABG 11:53](https://youtu.be/-XWSJM-Ue-o?t=713)
- **Formatting rules now over-correct.** Rules written against old bullet-and-bold habits might take a 50% habit to 10%, but a 10% habit "all the way to one" (1%), "which you probably don't want" [FABG 12:11](https://youtu.be/-XWSJM-Ue-o?t=731). **His rule:** "any behavioral instructions that you have in your CLAUDE.md are worth deleting and reconsidering"; start with none and adjust [FABG 12:28](https://youtu.be/-XWSJM-Ue-o?t=748). He has none [FABG 12:43](https://youtu.be/-XWSJM-Ue-o?t=763).
- **Unmarked quotations.** It reproduces passages from source text "without marking it as quotations"; give it an example of how to mark quotes [FABG 13:29](https://youtu.be/-XWSJM-Ue-o?t=809).
- **Finish the whole task.** Doc: "Fable 5.1 can execute very long tasks without much guidance on methodology, especially when the goal is clear. On complex asynchronous workloads, though, nudge it not to end its turn before the work is done. Without the nudge, the model sometimes describes what it would do next instead of doing it." [FABG 13:57](https://youtu.be/-XWSJM-Ue-o?t=837) Theo: Fable does this "significantly less than Astra"; easy to fix with prompting "or maybe even a skill or two" [FABG 14:16](https://youtu.be/-XWSJM-Ue-o?t=856).
- **Compaction.** "You can tell the model what to preserve in compaction summaries"; Fable writes its own compaction, so it can remember what you ask for. Put it in AGENTS.md or the system prompt. "I think people overthink compaction." [FABG 31:27](https://youtu.be/-XWSJM-Ue-o?t=1887), [FABG 31:43](https://youtu.be/-XWSJM-Ue-o?t=1903)
- **Scope creep and over-reach.** Doc: given too open-ended a request, the model may change files it shouldn't, fix nearby code, or extend behavior [FABG 31:56](https://youtu.be/-XWSJM-Ue-o?t=1916). Theo rarely sees it: "often a little more reserved than I would have expected" [FABG 32:14](https://youtu.be/-XWSJM-Ue-o?t=1934). The doc's instruction, which cut "unrequested additions and committed test code … substantially with no measurable change in task success" [FABG 32:26](https://youtu.be/-XWSJM-Ue-o?t=1946):
  > "If while working or testing you find pre-existing bugs, performance concerns, or behaviors the task doesn't mention, don't fix, optimize, or extend it in this change unless the requested behavior cannot work without it. Report it as a follow-up in your summary." [FABG 32:33](https://youtu.be/-XWSJM-Ue-o?t=1953)
- **Low effort may not trigger search**; tell it to use search [FABG 32:51](https://youtu.be/-XWSJM-Ue-o?t=1971).
- **Reducing safeguard false positives (doc).**
  - Word requests so they don't look like an attempt to hack [FABG 33:10](https://youtu.be/-XWSJM-Ue-o?t=1990): "Instead of 'does this program compile without errors', ask 'are there bugs in the program?'" [FABG 33:10](https://youtu.be/-XWSJM-Ue-o?t=1990) The transcript gives this as stated; the reason that wording is safer is not explained.
  - For lesser-known languages, put documentation in context, or it may try to "hack the binary to figure out what it's doing" and hit a safeguard [FABG 33:27](https://youtu.be/-XWSJM-Ue-o?t=2007).
  - Avoid base64 in context; it "tends to trigger a lot" [FABG 33:38](https://youtu.be/-XWSJM-Ue-o?t=2018).
  - Theo has had about 5 false positives "out of the thousands of prompts" [FABG 33:49](https://youtu.be/-XWSJM-Ue-o?t=2029).
- **API change.** Editing earlier messages drops that thread's reasoning traces, an anti-distillation measure [FABG 10:15](https://youtu.be/-XWSJM-Ue-o?t=615).
- **Lead agent keeps working while subagents run** (section 5).
- **Vision** does better with crop and zoom tools, which the model can build with local Python; "probably doesn't matter too much for Claude Code type usage" [FABG 34:35](https://youtu.be/-XWSJM-Ue-o?t=2075).

## 4. Pitfalls and misconceptions corrected

- **Fear of the "dumb zone"** (watch context or quality collapses) [FABG 35:11](https://youtu.be/-XWSJM-Ue-o?t=2111). Anthropic picked **1 million tokens** as the point where degradation might start to matter. "The dumb zone doesn't matter that much": **models are now good at compaction and at managing long runs** [FABG 36:04](https://youtu.be/-XWSJM-Ue-o?t=2164) T3 Code deliberately has no context monitor [FABG 36:16](https://youtu.be/-XWSJM-Ue-o?t=2176).
- **Lowering compaction thresholds to save cost backfires**: compacting more often rewrites context more often [FABG 37:27](https://youtu.be/-XWSJM-Ue-o?t=2247). Cache reads are discounted 75%, so "the context window size doesn't matter" [FABG 37:39](https://youtu.be/-XWSJM-Ue-o?t=2259). The catch is an expired cache: T3 offers "resume with less context", and if, say, 527K tokens aren't cached, compacting first may be worth it [FABG 37:51](https://youtu.be/-XWSJM-Ue-o?t=2271).
- **Over-customized Claude Code configs.** His only changes: full screen by default and routing through his proxy layer, "That is it." [FABG 38:40](https://youtu.be/-XWSJM-Ue-o?t=2320) Plus **memory off** ("I do not like the memory in Claude Code") [FABG 39:07](https://youtu.be/-XWSJM-Ue-o?t=2347). "**Don't change the defaults.**" [FABG 38:35](https://youtu.be/-XWSJM-Ue-o?t=2315) Start as if on a new machine: delete everything, install Claude Code fresh with as little as possible, then add small things for small problems [FABG 40:50](https://youtu.be/-XWSJM-Ue-o?t=2450).
- **Permission modes.** The auto-approval modes "are very good now, and you definitely shouldn't use accept edits or supervised" [FABG 39:58](https://youtu.be/-XWSJM-Ue-o?t=2398); those are "tools from the past". "**Use auto if you're careful and use full if you're not. Period.**" [FABG 40:24](https://youtu.be/-XWSJM-Ue-o?t=2424)
- **Asking models about harness internals.** "The models really really struggle with understanding these things"; asking Claude how compaction works in Codex gets a wrong answer. Don't trust the model on harness mechanics; keep the defaults [FABG 38:17](https://youtu.be/-XWSJM-Ue-o?t=2297).
- **Stale AGENTS.md.** The latest Claude Code reads AGENTS.md when there is no CLAUDE.md, so one written for "old cheaper dumb models and tools like OpenCode or Codex", full of formatting rules, starts affecting Claude [FABG 12:49](https://youtu.be/-XWSJM-Ue-o?t=769). Clean it up, or override with a local file ("a `CLAUDE.local.md` or something to specify, ignore all that") [FABG 13:23](https://youtu.be/-XWSJM-Ue-o?t=803).
- **Doing steps by hand that the model can do** (section 3). When you take a step the model could have taken, "Challenge yourself on it a bit." [FABG 36:46](https://youtu.be/-XWSJM-Ue-o?t=2206)
- **Economics (subscription framing).**
  - Fable is not "worth the money" unless a subscription subsidizes it; paying full API price "sounds insane to me" [FABG 4:15](https://youtu.be/-XWSJM-Ue-o?t=255)
  - Astra "can often get stuck in a loop" and overspend; Fable "is at least a bit more likely to stop when it should". On a median task Fable costs more, but at the extremes "Astra can just burn usage in stupid ways" [FABG 4:21](https://youtu.be/-XWSJM-Ue-o?t=261), [FABG 4:34](https://youtu.be/-XWSJM-Ue-o?t=274).
  - On a subscription **half the weekly limit is reserved for Fable** (50%); the other half is for everything else, then effectively Opus 5 [FABG 4:52](https://youtu.be/-XWSJM-Ue-o?t=292). He usually ends the week with Fable at zero and most of the other half unused [FABG 5:17](https://youtu.be/-XWSJM-Ue-o?t=317).
  - To get the most from the subscriptions, he sends work he would run on low to Opus instead [FABG 7:58](https://youtu.be/-XWSJM-Ue-o?t=478)

## 5. Subagents, orchestration, delegation, verification, review, model choice

- **Lead agent works in parallel with subagents.** Doc: let the lead keep working while subagents run. Theo: "both Astra and Fable 5.1 are really good at this"; meanwhile the lead can message subagents, test findings and plan the next step [FABG 34:18](https://youtu.be/-XWSJM-Ue-o?t=2058).
- **Cross-lab delegation from inside Fable.** "Claude isn't the best at computer use compared to Codex, especially on macOS", so with even a cheaper Codex subscription have Fable call Codex for computer-use verification or to confirm its work [FABG 25:15](https://youtu.be/-XWSJM-Ue-o?t=1515). Both are thorough reviewers, but **Astra is "a slightly better reviewer"** and **Fable "a much better writer of code"**, so Fable often asks Astra for feedback or testing [FABG 25:40](https://youtu.be/-XWSJM-Ue-o?t=1540). His prompt: "**Hey, can you have Astra verify this?**" Fable then fixes, retests, and doesn't come back until it is happy with the results [FABG 25:57](https://youtu.be/-XWSJM-Ue-o?t=1557).
- **The reverse direction.** Astra writes a big risky change and Fable reviews it for merge-readiness and risk, conservatively and concretely, including its own limits (LakeBed, section 2).
- **Verification loop as the definition of done:** root-cause, fix, verify, film a video, PR, address reviews, report; the model owns the whole loop [FABG 29:07](https://youtu.be/-XWSJM-Ue-o?t=1747).
- **Bot-review handling** (babysit skill, section 2): verify every bot finding against the source, act only on feedback newer than the latest push, reply-and-resolve findings not worth fixing [FABG 15:02](https://youtu.be/-XWSJM-Ue-o?t=902).
- **Planning vs execution.** The model proposed a de-risking plan, he skimmed it ("all the things it suggested sounded reasonable") and authorized execution on a separate branch: one model in sequence, with a light human gate [FABG 21:56](https://youtu.be/-XWSJM-Ue-o?t=1316).

## 6. Claude Code specifics

- **AGENTS.md fallback** when there is no CLAUDE.md: audit it for legacy rules or override with a local file (section 4).
- **Delete behavioral and formatting rules** from CLAUDE.md and AGENTS.md; add back only as needed (section 3).
- **Compaction preservation instructions** can go in AGENTS.md or CLAUDE.md (section 3).
- **Context window.** 1M tokens; Claude Code exposes 200K vs 1M and T3 Code mirrors that option [FABG 39:32](https://youtu.be/-XWSJM-Ue-o?t=2372). Don't lower compaction thresholds (section 4).
- **Settings and permissions.** Keep the defaults (his changes: fullscreen, proxy, memory off); auto or full, never accept-edits or supervised (section 4).
- **Skills.** "babysit PR" (monitor, poll, fix, rebase, no scope creep, no filler comments), "leaving PR comment" (formatting plus an AI disclaimer), and "modernize" (update on main): his mechanism for making Fable "keep going" on async workloads (section 2).
- **Harness PR monitoring.** "If your harness offers a tool to monitor the PR, use them"; otherwise poll [FABG 14:57](https://youtu.be/-XWSJM-Ue-o?t=897).
- **Calling Codex from Claude Code/Fable** for computer use and verification. The mechanism isn't specified in the transcript; it could be a CLI, MCP or a skill (section 5).
- **Sentry MCP.** Mentioned only in the sponsor segment, as a way to expose error and trace data to agents [FABG 2:22](https://youtu.be/-XWSJM-Ue-o?t=142).

## 7. Model comparisons

- **Fable 5.1 vs GPT-6 Astra.** Fable is more consistent ("less noisy"), Astra has higher peaks and worse dips [FABG 0:22](https://youtu.be/-XWSJM-Ue-o?t=22). **Fable is "a much better writer of code"; Astra is "a slightly better reviewer."** [FABG 25:40](https://youtu.be/-XWSJM-Ue-o?t=1540) Fable stops prematurely "significantly less than Astra" [FABG 14:16](https://youtu.be/-XWSJM-Ue-o?t=856). Astra adapts reasoning to task size better, barely using more tokens at max than at low [FABG 7:11](https://youtu.be/-XWSJM-Ue-o?t=431). Astra can loop and burn usage at the extremes; Fable costs more on a median task [FABG 4:34](https://youtu.be/-XWSJM-Ue-o?t=274).
- **Computer use.** Codex (OpenAI) is better than Claude, "especially on macOS" [FABG 25:15](https://youtu.be/-XWSJM-Ue-o?t=1515).
- **GPT-6.1 Sol** tends to scope-creep when babysitting PRs [FABG 15:37](https://youtu.be/-XWSJM-Ue-o?t=937).
- **Opus 5 (pre-5.5)** is "not a good model" and "spiky" [FABG 4:59](https://youtu.be/-XWSJM-Ue-o?t=299), [FABG 5:11](https://youtu.be/-XWSJM-Ue-o?t=311); he used it for low-effort work purely to use up the non-Fable half of his subscription [FABG 7:58](https://youtu.be/-XWSJM-Ue-o?t=478).
- **Gemini 3.1 Pro** over-reasons on trivial tasks (1,000+ tokens on SkateBench) [FABG 7:24](https://youtu.be/-XWSJM-Ue-o?t=444). Of Antigravity, Google's Gemini harness, users wanted accept-edits mode "because they can't trust the Gemini models enough" [FABG 40:12](https://youtu.be/-XWSJM-Ue-o?t=2412).
- **Fable 5.1 vs Fable 5.** "An incremental improvement" [FABG 41:09](https://youtu.be/-XWSJM-Ue-o?t=2469), but much more consistent and reliable [FABG 26:15](https://youtu.be/-XWSJM-Ue-o?t=1575); fewer progress updates and less stock-phrase slop, with somewhat denser prose [FABG 8:47](https://youtu.be/-XWSJM-Ue-o?t=527), [FABG 10:57](https://youtu.be/-XWSJM-Ue-o?t=657).

## 8. Routing-table and orchestrator-prompt implications

**(a) Which tasks go to which model**

1. **Fable 5.1 is the primary code writer and long-horizon executor.** It handles end-to-end bug fix to PR to babysit to merge loops and multi-hour autonomous runs. It is also the default for open-ended judgment: risk assessment, merge-readiness, de-risking plans, and choosing between competing PRs (section 2).
2. **GPT-6 Astra is the reviewer and verifier** of Fable-written code. The speaker routinely has Fable ask Astra for feedback and testing. Astra can also be a bold implementer for large, risky rewrites, but its output should then get a **Fable review gate** before merge (sections 2 and 5).
3. **Codex/OpenAI handles computer use and UI verification**, especially on macOS. Don't route GUI-driving verification to Claude models on Mac (section 5).
4. **Effort routing for Fable: default high, xhigh for deep or thorough work, never max** (section 3).
   - Avoid low and medium unless you deliberately want to limit depth, for example to keep it out of a known rabbit hole. The failure-and-retry cost outweighs the savings.
   - High on trivial tasks costs little because Fable scales down on its own.
   - Medium can still run for hours, so effort level does not cap duration.
5. **Budget-aware routing.** On a subscription, Fable has a separate quota of roughly 50% of the weekly limit. Cheap or low-effort work should go to the non-Fable pool (now Opus 5.5) to preserve Fable quota. The speaker considers Fable too expensive at API prices. This is a cost dimension the routing table should model (section 4).
6. **Don't route harness-internals questions** (how compaction works, Codex vs Claude Code mechanics) to any model as if it were authoritative. The speaker found models unreliable on these (section 4).
7. **PR babysitting and monitoring** can go to Fable with a dedicated skill. If Sol is used for it, add strict anti-scope-creep and no-filler-comment rules (section 2).

**(b) How the orchestrator should write prompts to the model**

1. **Every prompt needs an explicit end state.** Examples: "file the PR and tell me when it's up", "babysit till green", "merge once green and you're happy", "don't report until you have <link or video>". The orchestrator should refuse to dispatch a task without one (section 3).
2. **Use branching end states and decision delegation.** "If X is better, do A; if ours is better, do B; then babysit whatever ends up being put up." Give the model the data it needs to choose, not a fixed path (sections 2 and 3).
3. **Prompt wide and drop redundant steps.** Hand over the whole loop (root cause, fix, verify, record evidence, PR, address reviews, report). Don't make the orchestrator re-perform checks the model can do itself (section 3).
4. **Keep system prompts and CLAUDE.md minimal.**
   - No anti-formatting rules, no "be concise" style rules by default. They over-correct on 5.1.
   - Add targeted instructions only when you observe a problem. The doc's ready-made fixes:
     - The **anti-scope-creep instruction** quoted in section 3: "don't fix, optimize, or extend … Report it as a follow-up in your summary." It is particularly useful for subagent tasks with narrow scope.
     - **"Please remove all mannered prose"**, or the full definition, preferably in the **user message**, for user-facing writing.
     - The **progress-updates block** (announce, brief updates, standalone closing recap) when a human or a UI needs to follow along. Note that 5.1 is quiet by default. Since the orchestrator likely reads only the final message, always require "a short recap that stands on its own: what you found, what you did, and what's next".
     - If the harness hides tool outputs, say so in the prompt.
5. **Nudge against premature turn-ending on async or long workloads.** Fable may "describe what it would do next instead of doing it". Add "do not end your turn until the work is complete", or encode the loop in a skill (section 3).
6. **Tell Fable what to preserve in compaction** for long-running orchestrated tasks: task ID, end state, constraints, open blockers (section 3).
7. **Tell the lead agent to keep working while subagents run.** It should test findings, message subagents and plan next steps, not idle (section 5).
8. **Ask honest-assessment and risk questions as explicit checkpoints.** Examples: "Is this ready to merge? Give me your honest thoughts", "How can we de-risk this?", "Could you confidently debug X if it broke?" Fable gives well-structured capability-boundary answers that an orchestrator can use as gates (sections 2 and 3).
9. **Avoid safeguard triggers in generated prompts** (section 3).
   - No base64 blobs in context.
   - Phrase checks as "are there bugs" rather than compile-probing wording.
   - Include language docs for obscure languages.
   - Don't edit earlier history mid-thread; it drops reasoning continuity.
10. **Permission mode for orchestrated Claude Code workers** should be auto (or full in sandboxed environments). Avoid accept-edits or supervised modes. Pre-authorize expected actions in the prompt, and run on isolated machines or containers. The LakeBed run hammered his home IP until he told it to use a container, which argues for specifying the execution environment and network etiquette up front [FABG 22:45](https://youtu.be/-XWSJM-Ue-o?t=1365).

---

# Cross-video synthesis (where the two videos agree or differ)

- **Both videos agree on the following:**
  - **Define "done" explicitly.** This is the top recommendation in both [OPUSG 10:47](https://youtu.be/ejjBbaq9RmY?t=647), [FABG 27:05](https://youtu.be/-XWSJM-Ue-o?t=1625).
  - **Never use max effort.** Default to high, with xhigh for depth. Low is poor on both Opus 5.5 and Fable 5.1 [OPUSG 14:01](https://youtu.be/ejjBbaq9RmY?t=841), [FABG 5:53](https://youtu.be/-XWSJM-Ue-o?t=353).
  - **Don't tell the model to think harder.** It already reasons and scales its own reasoning [OPUSG 11:41](https://youtu.be/ejjBbaq9RmY?t=701), [FABG 6:30](https://youtu.be/-XWSJM-Ue-o?t=390).
  - **Cross-family review.** OpenAI models (Astra above all) are better or more exhaustive reviewers; Claude models (Fable, Opus 5.5) are preferred writers of code [OPUSG 22:44](https://youtu.be/ejjBbaq9RmY?t=1364), [FABG 25:40](https://youtu.be/-XWSJM-Ue-o?t=1540).
  - **Use OpenAI/Codex for computer use on macOS** rather than Claude [OPUSG 0:05](https://youtu.be/ejjBbaq9RmY?t=5), [FABG 25:15](https://youtu.be/-XWSJM-Ue-o?t=1515).
  - **Prompt wider and fire-and-forget**, on remote or isolated machines [OPUSG 3:02](https://youtu.be/ejjBbaq9RmY?t=182), [OPUSG 7:35](https://youtu.be/ejjBbaq9RmY?t=455), [FABG 28:03](https://youtu.be/-XWSJM-Ue-o?t=1683).
  - **Expect premature stops.** Both Opus 5.5 and Fable 5.1 sometimes stop and summarize instead of continuing. The fix is the same: name the stops, nudge to finish, or use a skill [OPUSG 18:31](https://youtu.be/ejjBbaq9RmY?t=1111), [FABG 13:57](https://youtu.be/-XWSJM-Ue-o?t=837).
  - **Subagents.** Both endorse them for large work. Fable and Astra run a lead plus subagents in parallel well. Opus 5.5 needs explicit permission to use subagents at all [OPUSG 20:42](https://youtu.be/ejjBbaq9RmY?t=1242), [FABG 34:18](https://youtu.be/-XWSJM-Ue-o?t=2058).
  - **Avoid "reasoning"-revealing requests and base64.** Both relate to safeguard false positives [OPUSG 27:13](https://youtu.be/ejjBbaq9RmY?t=1633), [FABG 33:38](https://youtu.be/-XWSJM-Ue-o?t=2018).
- **Nuances to keep:**
  - **Opus 5.5 benefits from explicit structure:** named stops, explicit negatives, an explicit subagent grant, and explicit "do all phases". Fable 5.1 is described as needing less of that.
  - **Design.** Fable designs better unprompted. Opus 5.5 needs a concrete anti-pattern list [OPUSG 16:57](https://youtu.be/ejjBbaq9RmY?t=1017).
  - **Communication style.** Fable 5.1 is quiet by default, with few progress updates [FABG 8:47](https://youtu.be/-XWSJM-Ue-o?t=527). Opus 5.5 "will keep you posted" and sometimes stops to report [OPUSG 18:28](https://youtu.be/ejjBbaq9RmY?t=1108).
  - **Review on the speaker's bench.** Fable found few but well-vetted issues. Opus 5.5 roughly doubled Opus 5 with no contradicted findings. Astra and Grok 4.7 found more [OPUSG 23:39](https://youtu.be/ejjBbaq9RmY?t=1419).
