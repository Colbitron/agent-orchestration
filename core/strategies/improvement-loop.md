# Improvement loop

Load this when something went wrong, when the user asks "how do we stop this
happening again?", when a new model ships, or when you are about to edit the
user's config, a bridge skill, or an AGENTS.md / CLAUDE.md. The kit's config
is meant to grow by small, evidence-driven edits and to shrink whenever a rule
stops earning its place.

Sources:
- INSP: "A proper guide to Fable 5", Theo (t3.gg), YouTube, https://youtu.be/8GRmLR__OGQ (recorded in the Fable 5 / GPT-5.5 / Opus 4.8 era)
- MODELS: "Please stop using stupid models", Theo (t3.gg), YouTube, https://youtu.be/iBrAWpjXNxs
- OPUSG: "Getting the most out of Opus 5.5", Theo (t3.gg), YouTube, https://youtu.be/ejjBbaq9RmY
- FAB51: "My New Favorite Model", Theo (t3.gg), YouTube, https://youtu.be/r_dw-1109Ag
- FVA: "Fable Vs Astra Debate Is Over", Theo (t3.gg), YouTube, https://youtu.be/P7bxbDSnZRM
- FABG: "So I was using Fable wrong...", Theo (t3.gg), YouTube, https://youtu.be/-XWSJM-Ue-o
- OPUS55: "My new favorite model.", Theo (t3.gg), YouTube, https://youtu.be/jgGyX7MPPVg

`[KEY m:ss]` links to the video at that timestamp; the auto-generated captions
often mishear model names (Sol as "Soul", Fable as "Able").

---

## 1. The loop

Theo's config was not designed up front: "I spent about half an hour getting
it mostly working and then as I ran into problems I would go back to the
original thread and tell Claude, 'Hey, I had this problem. How can we prevent
this going forward?' And it would suggest changes. I would tell it to cut them
in half and then put them in here" ([INSP 20:08](https://youtu.be/8GRmLR__OGQ?t=1208)).

Run it like this:

1. **Diagnose** in the thread where it happened (§2).
2. **Ask for prevention:** "How can we prevent this going forward?"
3. **Choose the layer** to change (§3).
4. **Have the model propose the change.**
5. **Cut it in half.** Remove hedges, examples that restate the rule, and
   anything that addresses a problem you have not seen.
6. **Show the user the diff and append it** to the right file. Never
   rewrite the user's config wholesale.
7. **Log** the incident and the change (§8) so you can later tell whether the
   rule helped.

The user owns their config. Propose edits; apply them only with the user's
approval, unless their config grants standing permission for this.

## 2. Diagnose before you prescribe

Ask the model that made the mistake what led it there. Use Theo's wording
([MODELS 11:58](https://youtu.be/iBrAWpjXNxs?t=718), rule 13):

```
I expected you to do <X>, but you did <Y> instead. What led you there?
```

Models "will usually indicate what signals they found and what tools they
called and what files they read that led them in the wrong direction."

- Do not ask it to "show your reasoning" or "what was your reasoning"; that
  wording risks safeguard flags on Claude. "Explain why you did this" is fine
  ([OPUSG 26:48](https://youtu.be/ejjBbaq9RmY?t=1608)).
- Ask once and read the answer. The cause is often a misleading file, a stale
  doc, an ambiguous word, or a missing permission, not the model.
- If the failure was intent (the model read a word narrowly), the fix is
  usually a glossary entry, not a rule
  ([FAB51 39:22](https://youtu.be/r_dw-1109Ag?t=2362); [INSP 16:44](https://youtu.be/8GRmLR__OGQ?t=1004) on glossaries).

## 3. Pick the right layer

Fix at the lowest layer that removes the cause. In order of preference:

| Layer | Fix here when | Example |
|---|---|---|
| **Codebase** | A new developer would have tripped too. | Delete dead code, fix a flaky test, clarify a confusing module boundary. "You should adjust your prompts a little, but you should adjust your codebase a lot" ([MODELS 12:54](https://youtu.be/iBrAWpjXNxs?t=774), rule 7). |
| **Bridge skill** | A shell-out was wrong: command, flags, prompt shape, output handling. | Record the correct command; add "if Codex finds nothing, say so" (§4). |
| **Glossary** | The model misread a term. | Define "revert", "babysit", "done", or a project term. |
| **Routing table / model profile** | The wrong model or effort was used for the task type. | Move a task type's default; note a failure mode in the profile and bump `as_of`. |
| **Standing rules** (user config, CLAUDE.md, AGENTS.md) | The behaviour is general and recurring across tasks. | Named-stops rule; anti-scope-creep line for babysitting. |
| **One prompt** | It was a one-off. | Steer the running agent; do not persist anything. |

Prefer adding a **check** over adding a **rule**. A path-scoped review agent
that blocks merge enforces a convention; a line in AGENTS.md "only guarantees
that your agent knows about them, not that it's actually going to follow"
([FVA 2:03](https://youtu.be/P7bxbDSnZRM?t=123)).

## 4. Capture exact commands in the bridge

The most valuable lines in a bridge skill are the commands. "Not because the
model can't get them right, but because the one or two times they get it
wrong, it's really annoying. So you ask the model when that happens, what did
you get wrong? What is the right structure for this? And then once you have
that, you can go add it here" ([INSP 21:23](https://youtu.be/8GRmLR__OGQ?t=1283)).

When a shell-out fails:

1. Ask: "What did you get wrong? What is the right structure for this command?"
2. Run the corrected command once to confirm it works.
3. Add it to the bridge verbatim, in a code block, next to a one-line note of
   when to use it.
4. Add any output-handling fix the failure revealed. Theo's examples ([INSP 21:58](https://youtu.be/8GRmLR__OGQ?t=1318)):
   - Codex returned nothing and the parent reran it → "If Codex finds nothing,
     say that clearly and mention what the review target is that it inspected."
   - Claude prompted Codex as if it were Claude → a short, simple example prompt.
   - Workflow subagents calling GPT were invisible → a name prefix.
   - Tasks timed out → a note that they can.

Keep the bridge **description** complete enough to decide when to call it: the
model sees only the description until it invokes the skill ([INSP 23:17](https://youtu.be/8GRmLR__OGQ?t=1397)). When you
change a bridge's trigger, rewrite the description, not just the body. Theo
widened his computer-use bridge from "when the user asks Claude to have Codex
test a flow" to "when the user asks Claude to test a flow" so it became the
default ([INSP 23:58](https://youtu.be/8GRmLR__OGQ?t=1438)).

## 5. Keep standing rules minimal

Current models are hurt by rules written for older ones.

- "Any behavioral instructions that you have in your CLAUDE.md are worth
  deleting and reconsidering. See how it feels to not have them at all and
  then adjust over time" ([FABG 12:28](https://youtu.be/-XWSJM-Ue-o?t=748)). Theo has
  none.
- Formatting rules over-correct: a habit the model shows 10% of the time can be
  pushed to 1% ([FABG 12:17](https://youtu.be/-XWSJM-Ue-o?t=737)). Old anti-chatter rules
  ("hold all findings for the final response") now suppress output you want
  ([FAB51 34:28](https://youtu.be/r_dw-1109Ag?t=2068)).
- Anti-slop rules became unnecessary for Opus 5.5; Theo deleted his "unslop"
  instructions and did not re-add them ([OPUS55 10:03](https://youtu.be/jgGyX7MPPVg?t=603)).
- **Reset procedure:** "Pretend you're on a brand new machine. Delete
  everything. Install Claude Code from scratch. Set it up with as little as
  possible... from there, slowly start adding small things that solve your
  small problems" ([FABG 40:50](https://youtu.be/-XWSJM-Ue-o?t=2450)).
- **Don't change harness defaults.** Theo's only Claude Code changes: fullscreen,
  routing through his proxy, memory off. "Some random post you saw on Twitter
  isn't more clever than the hundreds of billions of dollars... going into stuff
  at Claude Code" ([FABG 38:40](https://youtu.be/-XWSJM-Ue-o?t=2320)).
- **What does belong in standing config** (from Theo's setup, [INSP 11:41](https://youtu.be/8GRmLR__OGQ?t=701);
  [OPUSG 19:10](https://youtu.be/ejjBbaq9RmY?t=1150)): the glossary, the model roster
  with scores and the standing-override rule, named stops for approvals, bridge
  pointers, and preferences that are genuinely his (tech stack, code style).

Every standing rule should trace to a problem that actually happened. When you
append one, add a short reason or a link to the log entry, so a later pruning
pass can tell whether the reason still holds.

## 6. Re-baseline when a model ships

Configs and mental models go stale with each release. "Any customization or
careful configuration you've done to work around the flaws are probably out of
date and a lot of your own mental model around this stuff is also out of
date. Reset it" ([FABG 40:36](https://youtu.be/-XWSJM-Ue-o?t=2436)).

Procedure:

1. **Keep a personal set of previously failed prompts.** Theo: "I always start
   with a set that I've tried on other things that failed to see if it can
   succeed" ([MODELS 8:58](https://youtu.be/iBrAWpjXNxs?t=538), rule 5). Store them with
   the date, the model that failed, and what failure looked like.
2. **Run the set on the new model** with the user's current config, then with
   standing rules stripped. Compare.
3. **Prompt wider** than before. Old narrow prompts hide the difference
   between models ("you also suck at prompting" if you notice no difference
   going back a tier, [MODELS 1:04](https://youtu.be/iBrAWpjXNxs?t=64)).
4. **Update or add the model profile** in `core/models/`, set `confidence`
   honestly, bump `as_of`, and re-run the routing generator.
5. **Delete workarounds the new model no longer needs** (§5).
6. **Re-check effort defaults** with a few runs at `high` and one lower level
   (`effort-levels.md`). Do not test `max` except to confirm it is still bad.
7. **Do not trust benchmarks alone.** Theo was fooled by Opus 5's ceiling: "I
   focused too much on what the best looked like... and it misbehaved far more
   often than I had known" ([MODELS 4:53](https://youtu.be/iBrAWpjXNxs?t=293)). Measure the
   floor: how often it does something dumb on wide tasks.

## 7. Audit what agents write

- **Skills and prompts written by agents must be audited by a human.** "Please
  write your skills by hand or at least audit them." "If you let the agent
  write the skill, you let the skill be involved when it writes another skill,
  you end up in slop hell very fast" ([FVA 55:01](https://youtu.be/P7bxbDSnZRM?t=3301)).
  Astra is slightly better at it than Fable, but "none of them are good at it".
- **Read the parts the model wrote.** Theo found a model-written cost clause
  he disagreed with while reviewing his own CLAUDE.md on camera and rewrote it
  ([INSP 18:14](https://youtu.be/8GRmLR__OGQ?t=1094); see `cost-model.md` §7).
- **Do not copy someone else's config blindly.** "Don't just blindly copy paste
  my stuff... I want you guys to learn from this" ([INSP 22:18](https://youtu.be/8GRmLR__OGQ?t=1338)). The interview exists
  so each user's config reflects their own environment.
- **Prune stale AGENTS.md.** Claude Code reads AGENTS.md when no CLAUDE.md
  exists, so an AGENTS.md written for "old cheaper dumb models" full of
  formatting rules will start steering Claude
  ([FABG 12:49](https://youtu.be/-XWSJM-Ue-o?t=769)). Clean it up; if the team will
  not allow that, override locally (e.g. a `CLAUDE.local.md` that says to
  ignore it).
- **Do not ask models how harnesses work internally.** "The models really
  really struggle with understanding these things"
  ([FABG 38:17](https://youtu.be/-XWSJM-Ue-o?t=2297)). Check harness docs instead; keep
  defaults when unsure.

## 8. What to log

Routing can only improve if you record what happened. After every delegated
run, append one line to the user's run log (`logging.path` in config; kit
default `~/.agent-orchestration/runs.jsonl`). This is the canonical record:
one JSON object with exactly these ten keys, in this order, and nothing else.

| Key | Meaning |
|---|---|
| `ts` | When the run ended: ISO 8601 date (`2026-10-15`) or date-time with offset (`2026-10-15T14:05:00-06:00`). |
| `repo` | Repository or project name, or `null`. |
| `row` | One task id from `core/tasks.md` (`feature`, `review`, ...): the routing row used. |
| `model` | One profile id: a file name in `core/models/` without `.md` (`claude-opus-5-5`, not `opus-5.5`). |
| `effort` | Effort as passed (`high`, `default`), or `null`. |
| `mechanism` | How it ran, free text: `subagent`, `workflow`, `bridge:<id>`, `subagent+worktree`, ... |
| `duration_s` | Wall-clock seconds as an integer, or `null`. A diagnostic of task and codebase (`parallelism.md` §12). |
| `outcome` | merged / closed / superseded / abandoned / info-only / pass / fail, plus a short clause; `unknown` when not recorded. |
| `follow_ups` | What still needs doing, one string (`; `-separated); `none` when there are none. |
| `notes` | Free text, or `null`. |

```
{"ts":"2026-10-15T14:05:00-06:00","repo":"hill-family-cookbook","row":"review","model":"gpt-6-1-sol","effort":"high","mechanism":"bridge:codex-cli","duration_s":412,"outcome":"info-only: 3 confirmed, 1 unconfirmed","follow_ups":"fix the two auth findings","notes":"task: review PR 141; harness: codex; delegated_by: claude-opus-5-5; reviewer_findings: confirmed 3, unconfirmed 1, contradicted 0"}
```

Richer facts go in `notes` as `key: value` pairs separated by `; `, when
known: `task` (a one-line description), `harness`, `access`
(subscription/API), `delegated_by` (orchestrator model or human, to separate
your routing decisions from the user's), `human_interventions` (Theo's metric:
"how long can the model run without your input?"), `escalated_to` (a profile
id, when the standing override was used; `model` stays the routed one),
`reviewer_findings` (confirmed / unconfirmed / contradicted counts),
`follow_ups_to_merge` (commits or fixes between PR filed and merged: Fable ~2
vs Astra ~6 in [FVA 33:46](https://youtu.be/P7bxbDSnZRM?t=2026)),
`cost_or_quota`, and a link to any improvement made. An earlier version of
this section gave each of these its own key; nothing wrote that shape, so
they stay in `notes` until the log shows one is worth a key.

`scripts/normalize_runs.py` rewrites older rows to this record (dry run by
default; `--write` backs the file up first), and `--check` validates a log
against it. A compound row such as `babysit+review` keeps its first id in
`row` and adds `also_row: review` to `notes`, only when every part is a task
id. An escalation such as `claude-fable-5-1->claude-opus-5-5` keeps the left
side in `model` and adds `escalated_to: claude-opus-5-5` to `notes`, only
when both sides are profile ids. Values it cannot map without guessing, such
as an unknown model id, are left as written and listed.

Theo's two headline metrics ([MODELS 15:51](https://youtu.be/iBrAWpjXNxs?t=951), rule 6):
"How long can the model run without your input?" and "How likely is it that
the thing works by the time a human gets involved?" Track both per model and
task type. His own log analysis (median run time 53 s → 2 min 20 s; monthly
P95 9 → 22 min as models improved) came from having an agent analyse his
prompt history ([MODELS 21:26](https://youtu.be/iBrAWpjXNxs?t=1286)).

Use the log:

- **Monthly, or on user request:** have an agent summarise the log by task
  type and model. Propose routing-table changes where a model consistently
  escalates, needs many follow-ups, or burns quota.
- **On a new model:** compare its first runs against the log's baseline for
  the same task types.
- **Trace review:** reading what models actually did, then refining skills, is
  how Maria got to "fire a single prompt and get a PR landed instantly" after
  3–4 days of review ([MODELS 18:23](https://youtu.be/iBrAWpjXNxs?t=1103)).

## 9. Distributing changes

- When the user runs agents on several machines, the config lives in
  `~/.agent-orchestration/` and is shared across harnesses
  (`docs/ARCHITECTURE.md`). Theo distributed his CLAUDE.md by telling the
  agent: "I just updated the CLAUDE.md in this repo. Commit it and push it out
  to the rest of the fleet" ([OPUSG 19:31](https://youtu.be/ejjBbaq9RmY?t=1171)).
- After any change to routing or bridges, re-run the generator so every
  adapter picks it up.

## 10. Pruning pass

Run this when the user asks, after each re-baseline, or when the standing
config grows past what fits on one screen:

1. List every standing rule and bridge note with its recorded reason.
2. For each, ask: has the logged problem recurred since the rule was added? Is
   the model that caused it still in use?
3. Propose deleting rules whose reason no longer applies. Theo expects to
   delete his bridge skills "once better models come out, or better yet,
   Anthropic gets good at computer use" ([INSP 20:32](https://youtu.be/8GRmLR__OGQ?t=1232)).
4. Try the deletion on a few real tasks before committing to it.

The direction of travel is less configuration over time, and more trust in
the model where the log shows it has earned it. Theo's trust ladder went from
tab completion to "I tell it to find them, fix them, and merge them for me"
for bug fixes and performance work, with product calls kept by the human
([FAB51 52:54](https://youtu.be/r_dw-1109Ag?t=3174)).
