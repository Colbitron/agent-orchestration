# Effort levels

Load this when you choose a reasoning-effort setting for yourself, a subagent,
a workflow stage, or a shell-out. The short version: **use `high`, never use
`max`, and treat `low`/`medium` as a deliberate depth limit, not a cost saver.**

Sources:
- FAB51: "My New Favorite Model", Theo (t3.gg), YouTube, https://youtu.be/r_dw-1109Ag
- OPUS55: "My new favorite model.", Theo (t3.gg), YouTube, https://youtu.be/jgGyX7MPPVg
- SON55: "OpenAI should be scared of this one", Theo (t3.gg), YouTube, https://youtu.be/8WbW_n95wc4
- H55: "finally a good small model", Theo (t3.gg), YouTube, https://youtu.be/38_6C0dkKmU
- OPUSG: "Getting the most out of Opus 5.5", Theo (t3.gg), YouTube, https://youtu.be/ejjBbaq9RmY
- FABG: "So I was using Fable wrong...", Theo (t3.gg), YouTube, https://youtu.be/-XWSJM-Ue-o
- INSP: "A proper guide to Fable 5", Theo (t3.gg), YouTube, https://youtu.be/8GRmLR__OGQ
- FVA: "Fable Vs Astra Debate Is Over", Theo (t3.gg), YouTube, https://youtu.be/P7bxbDSnZRM
- SOL61: "OpenAI fights back", Theo (t3.gg), YouTube, https://youtu.be/vu8X3YroB-w
- ASTRA: "It's Here.", Theo (t3.gg), YouTube, https://youtu.be/XFWpf0wLbh0

`[KEY m:ss]` links open that video at that timestamp; the auto-generated captions often mishear model names (Sol as "Soul", Fable as "Able", GPT-5.6 as "GBD 56").

---

## 1. What effort actually controls

Effort levels (`low`, `medium`, `high`, `xhigh`, `max` on current Claude
models, Haiku 5.5 included, and GPT models) are not "think this much". They are "think **up to** this much".

- `low` through `xhigh` are **ceilings**. The model thinks as much as it needs
  and stops at the cap. A trivial message at `high` stays short: Theo sent
  "Hi, how are you doing today?" at `max` on Fable and the answer stayed brief
  ([FABG 6:41](https://youtu.be/-XWSJM-Ue-o?t=401)).
- `max` is a **floor**. "Max isn't just making it so the model can think more.
  It is removing its ability to think less"
  ([OPUSG 12:30](https://youtu.be/ejjBbaq9RmY?t=750)). "It's effectively telling the
  model it's not done until it does a certain number of reasoning tokens"
  ([SON55 12:21](https://youtu.be/8WbW_n95wc4?t=741)).
- Effort applies **per step**, not per task. "The reasoning effort only applies
  per tool call and per change. So if you have work that takes 500 steps, Max
  isn't going to do more steps necessarily. It's going to think more per step
  and most of the steps don't require that much thought" ([INSP 8:46](https://youtu.be/8GRmLR__OGQ?t=526)).

Consequences:

1. **Effort does not cap duration.** A Fable run at `medium` went 1 h 34 min
   unattended ([FABG 22:25](https://youtu.be/-XWSJM-Ue-o?t=1345)). A `high` run can go
   for hours. Raising effort does not make a model "work longer".
2. **High on a simple task is cheap.** Because `high` is a ceiling, the model
   does not spend what it does not need ([FABG 6:30](https://youtu.be/-XWSJM-Ue-o?t=390)).
3. **Max on any task is expensive.** Every step is forced to overthink, and
   overthinking produces second-guessing, loops, and oversized diffs.

## 2. Why never `max`

Evidence, all from the same speaker across models:

| Observation | Source |
|---|---|
| SkateBench, Opus 5.5: `xhigh` 338 tokens/response, 6 s avg, 31 s worst, 78%. `max` ~5,000 tokens, 50 s avg, 600 s worst, 79%. "It cost 13 times more. It used 15 times the tokens. It took 20 times longer in the worst cases. And I got jack out of it." | [OPUSG 12:57](https://youtu.be/ejjBbaq9RmY?t=777) |
| An Opus 5.5 thread at `max` ran 6.5 hours writing a markdown plan "in loops forever". Switched to `high`, asked for status, said "continue": done in ~10 minutes. | [OPUSG 4:23](https://youtu.be/ejjBbaq9RmY?t=263); [OPUS55 17:39](https://youtu.be/jgGyX7MPPVg?t=1059) |
| Terminal Bench 4, Opus 5.5: "a slight dip on max". Medium beat Fable 5.1 max at $2.94 vs $20. | [OPUS55 6:30](https://youtu.be/jgGyX7MPPVg?t=390) |
| Frontier Code, Sonnet 5.5: `xhigh` scored higher than `max`. | [SON55 16:11](https://youtu.be/8WbW_n95wc4?t=971) |
| Going low→xhigh added ~5–8% tokens on some benches; xhigh→max added "a 1,500% increase". Max "can often actually hurt performance because... it's going to start second guessing itself." | [SON55 11:57](https://youtu.be/8WbW_n95wc4?t=717) |
| DeepSWE, Astra: `xhigh` 74.1%, `max` 73%. | [ASTRA 20:20](https://youtu.be/XFWpf0wLbh0?t=1220) |
| DeepSWE, GPT-6.1 Sol: scores drop on `xhigh` and `max`. Terminal Bench 4: `max` failed tasks `xhigh` passed. | [SOL61 4:17](https://youtu.be/vu8X3YroB-w?t=257) |
| "Every single person complaining about blasting through their usage too fast was on X high, max, or Ultra Code." | [INSP 9:30](https://youtu.be/8GRmLR__OGQ?t=570) |

Rule: **never select `max`** for any delegated or orchestrated call. If a user
explicitly asks for `max`, do it once and tell them the expected cost multiple.
Theo's only use for it is "just trying to burn a limit"
([FABG 6:06](https://youtu.be/-XWSJM-Ue-o?t=366)).

## 3. Per-model defaults

| Model | Default | Also fine | Avoid | Notes |
|---|---|---|---|---|
| Claude Fable 5.1 | `high` | `low` for routine, known-simple work; `medium` to stop a rabbit hole | `max`; `xhigh` without evidence | "Doesn't seem to benefit as much going beyond high" ([FAB51 13:53](https://youtu.be/r_dw-1109Ag?t=833)). See §6 on the low/xhigh conflict. |
| Claude Opus 5.5 | `high` | `medium` for scoped or cost-sensitive work; `xhigh` for a polish/refinement pass | `low`, `max` | Harness default appears to be `medium` ([OPUS55 31:02](https://youtu.be/jgGyX7MPPVg?t=1862)). "Low is really bad"; "low and max are dangerous... medium, high, XH high, those all have seemed really good" ([OPUS55 8:27](https://youtu.be/jgGyX7MPPVg?t=507)). |
| Claude Sonnet 5.5 | `high` | `xhigh` for harder analysis | `low`, `max`; treat `medium` as weaker than Opus `medium` | "Medium is a lot stronger with Opus than it is with Sonnet" ([SON55 16:48](https://youtu.be/8WbW_n95wc4?t=1008)). Exception: `low` is fine when Sonnet is only a wrapper that shells out to another model (§7). |
| Claude Haiku 5.5 | `high` for subagent work | `xhigh` for a harder bounded pass | `max` until re-baselined (§6); reasoning off; `low` as for other Anthropic models (§6) | Levels `low` to `max`; API default is `medium`, so set the level explicitly. Theo's AA chart shows `xhigh` and `max` as the best value in Anthropic's range ([H55 14:01-14:09](https://youtu.be/38_6C0dkKmU?t=841)); the never-`max` rule stands until the user's own re-baseline tests it. Never turn reasoning off: Anthropic models are "bad at that" ([H55 10:23-11:25](https://youtu.be/38_6C0dkKmU?t=623)). Thinking can only be disabled at `high` or below (Anthropic docs). |
| GPT-6 Astra | `high` | `low` for science-style tasks (54.3% on Terminal Bench Science at `low`) | `max`; `fast` mode; careless `ultra` | "High does seem to be one of the best options"; `xhigh` sometimes scored below `high` ([ASTRA 8:09](https://youtu.be/XFWpf0wLbh0?t=489)). "If you're using fast with Astra, you're probably using Astra wrong" ([FVA 1:06:22](https://youtu.be/P7bxbDSnZRM?t=3982)). |
| GPT-6.1 Sol | `low` | `high` | `xhigh`, `max` | Low "is the cost and efficiency star": DeepSWE at $0.21/task and 4.8 min, matching Opus 5.5 `max` at $14.65 and 50 min ([SOL61 21:18](https://youtu.be/vu8X3YroB-w?t=1278)). |
| Others (Grok, open-weight) | `high` | — | `max` | No effort-specific evidence. Start at `high` and log results. |

Profiles in `core/models/` carry the authoritative `effort:` block per model;
when a profile and this table disagree, the profile wins because it is dated.

## 4. When `low` or `medium` make sense

Use a lower effort only as a deliberate choice, for one of these reasons:

- **You want the model to stop earlier or not go deep.** "Only use low and
  medium if you specifically want the model to stop earlier or not go too
  deep... if you know the thing's a rabbit hole"
  ([FABG 7:40](https://youtu.be/-XWSJM-Ue-o?t=460)).
- **The model is a cheap token-efficient one where low is its sweet spot**
  (Sol).
- **The task is routine and verified by a test**, so a miss is caught cheaply.
  Fable 5.1 `low` is "surprisingly capable" and on Cursor Bench "a very
  compelling option for a lot of work" ([FAB51 14:43](https://youtu.be/r_dw-1109Ag?t=883); [FAB51 32:44](https://youtu.be/r_dw-1109Ag?t=1964)).
- **The agent is a wrapper** whose only job is to run a command and relay
  output (§7).

Do not use low to save money on work that must land. Low "will miss" hidden
complexity in a task you thought was simple ([FAB51 32:29](https://youtu.be/r_dw-1109Ag?t=1949)),
and "it ends up being more tokens if you have it do the task on low and it
fails and then you redo it on medium or high"
([FABG 6:24](https://youtu.be/-XWSJM-Ue-o?t=384)). If a low/medium run fails, rerun at
`high` directly; do not step through each level.

## 5. When `xhigh` makes sense

- A **refinement pass** after a draft at the default. Theo drafted a game at
  Opus `medium`, then ran "make it as visually appealing as possible" at
  `xhigh` ([OPUS55 31:02](https://youtu.be/jgGyX7MPPVg?t=1862)).
- **Deep, detail-sensitive work** where `high` "sometimes misses smaller
  details" ([OPUSG 14:40](https://youtu.be/ejjBbaq9RmY?t=880)), e.g. Opus or Sonnet on a
  hard analysis.
- **Exhaustive bug hunting with Astra**, accepting ~4x time and tokens
  ([FVA 24:37](https://youtu.be/P7bxbDSnZRM?t=1477)).

Do not leave `xhigh` on as a session default for Fable (§6). Switch back to
`high` after the pass.

## 6. Conflicts in the sources, and the kit's rule

**Fable and `xhigh`.** The orchestration video says "Do not use Fable on
higher than high reasoning efforts. The X high and max options are dangerous"
and "just keep it on low through high" ([INSP 7:44](https://youtu.be/8GRmLR__OGQ?t=464); [INSP 9:24](https://youtu.be/8GRmLR__OGQ?t=564)). The later Fable 5.1 prompting
video says he uses `xhigh` "on really deep, thorough things"
([FABG 6:06](https://youtu.be/-XWSJM-Ue-o?t=366)), and the Fable 5.1 release video
says returns diminish past `high` ([FAB51 13:53](https://youtu.be/r_dw-1109Ag?t=833)).
**Kit rule:** Fable at `high`. Use `xhigh` only for a single bounded deep pass
that the user asked for or that `high` demonstrably failed, then return to
`high`.

**Fable and `low`.** The release video calls Fable `low` "surprisingly capable"
([FAB51 32:44](https://youtu.be/r_dw-1109Ag?t=1964)); the prompting video avoids low and
medium because retries cost more ([FABG 6:11](https://youtu.be/-XWSJM-Ue-o?t=371)).
**Kit rule:** `low` only for routine, test-verified tasks or rabbit-hole
limiting; never for `feature`, `long-run`, `frontend`, or `orchestrate`.

**Opus default.** Claude Code's default for Opus 5.5 appears to be `medium`
and AA rates medium as the best value ([OPUS55 31:02](https://youtu.be/jgGyX7MPPVg?t=1862); [OPUS55 17:10](https://youtu.be/jgGyX7MPPVg?t=1030)); the Opus prompting video says "I just leave it on high or xhigh"
([OPUSG 14:18](https://youtu.be/ejjBbaq9RmY?t=858)). **Kit rule:** `high` for work that
must land or is wide; `medium` is acceptable for narrow or cost-sensitive work
when the user's config prefers it.

**Anthropic models on `low` generally.** The Sonnet video says "I don't think
you should use any anthropic model on low right now"
([SON55 16:17](https://youtu.be/8WbW_n95wc4?t=977)), which conflicts with the Fable `low`
praise. The kit rule above (Fable `low` only for routine, test-verified work;
Opus, Sonnet and Haiku 5.5 never `low` for real work) covers both.

**Haiku 5.5 and `max`.** On Theo's chart of Artificial Analysis data, Haiku
5.5 at `xhigh` and `max` are "the best value in that range within
Anthropic's line of models" ([H55 14:01-14:09](https://youtu.be/38_6C0dkKmU?t=841)), and `max` is still cheap in
absolute terms. That conflicts with §2. **Kit rule:** `high` by default and
`xhigh` when a bounded task needs more; no `max` until the user's re-baseline
(`improvement-loop.md` §6) shows it pays on their own tasks. Whatever the
level, keep reasoning on.

## 7. Bundled modes that hide effort

- **Claude Code `ultracode` / workflows** run `high` under the hood: "Ultra
  Code uses high under the hood. It just spins up a ton more of them. So, even
  Anthropic agrees high is the best bang for your buck" ([INSP 9:37](https://youtu.be/8GRmLR__OGQ?t=577)). Its cost comes
  from fan-out, not effort. Theo also says it "causes it to use workflows when
  it shouldn't" ([INSP 7:51](https://youtu.be/8GRmLR__OGQ?t=471)). Use workflows deliberately (see `parallelism.md`), not
  through a mode toggle.
- **Codex `ultra`** with unbounded subagents can mean "40 sub agents each can
  run" ([FVA 1:05:42](https://youtu.be/P7bxbDSnZRM?t=3942)). Be "very careful of the ultra
  button" ([FVA 1:06:16](https://youtu.be/P7bxbDSnZRM?t=3976)).
- **Codex / OpenAI `fast`** is about 2x speed at about 2x price
  ([ASTRA 3:39](https://youtu.be/XFWpf0wLbh0?t=219)). Not for orchestrated work.
- **Wrapper subagents.** When a cheap Claude subagent exists only to call
  another model's CLI and relay its output, run it at the lowest effort its
  model handles: Theo uses "sonnet on low" for this ([INSP 19:37](https://youtu.be/8GRmLR__OGQ?t=1177)). Its job is a shell
  command, not reasoning. This is the one sanctioned use of Sonnet `low`.

## 8. Changing effort mid-run

- **On Claude, changing effort mid-session no longer busts the cache.** The
  effort level used to live in the cached system-prompt prefix
  ([OPUS55 12:50](https://youtu.be/jgGyX7MPPVg?t=770)). So escalate or de-escalate
  within a thread instead of starting a new one.
- **Recovering a runaway run** ([OPUSG 4:59](https://youtu.be/ejjBbaq9RmY?t=299)):
  1. Stop it.
  2. Switch to `high` (or `xhigh` if it was `max` and you want a middle step).
  3. Ask only: "What's the state of the work?"
  4. Read the report, then say "continue".
- **Escalation on failure:** if output misses the bar, rerun the same task at
  `high` on the same model first if the failure looks like depth; switch to a
  smarter model if it looks like capability or judgment. Either is allowed
  without asking (see `cost-model.md`, standing permission).

## 9. Setting effort in delegated calls

- State the effort in the dispatch itself (subagent definition, workflow
  stage config, or CLI flag), never in prose. Prose like "think hard" does
  nothing useful and is banned (`delegation-prompting.md` §11).
- Log the effort used for every delegated run (`improvement-loop.md` §8) so
  routing can be tuned from data instead of vibes. "No one's evaluating how
  this works in Claude Code quite to that level... I honestly recommend just
  kind of gut feeling it" ([FABG 5:34](https://youtu.be/-XWSJM-Ue-o?t=334)); your logs
  are the only evals you will have.

**Harness notes.**
- *Claude Code:* effort is set per session and can be pinned per subagent
  definition and per workflow stage where supported. `ultracode` is a
  fan-out mode at `high`, not a higher effort.
- *Codex CLI:* effort is a config/CLI option per invocation; `fast` and
  `ultra` are separate toggles. Exact flags belong in `core/bridges/`.
- *Low effort may skip search* on Claude; if a low-effort worker needs web or
  code search, tell it to search ([FABG 32:51](https://youtu.be/-XWSJM-Ue-o?t=1971)).
