# Setup interview

This is the script an agent follows when the user runs setup. It is written
for the agent. The agent runs it inside whatever harness the user has; the
questions are the same everywhere, only the way they are asked differs.

Outcome: `~/.agent-orchestration/config.yaml`, `routing.md`, and
`glossary.md` exist, the user has read the routing table, and the harness
loads it on the next session.

Do not generate a routing table before step 4 is complete. The whole point
of the interview is that the table reflects the user's real environment.

## 0. Before asking anything

1. Check for an existing `~/.agent-orchestration/config.yaml`. If present,
   say so, show `user.updated`, and ask whether to **update** it (keep
   answers, re-ask only what they want to change) or **start over**.
2. Detect what is installed, silently, and keep the results for step 1:

   ```bash
   for b in claude codex gemini opencode cursor-agent agent pi grok; do
     command -v "$b" >/dev/null 2>&1 && echo "$b: $(command -v $b)"
   done
   ```

3. Read `core/models/*.md` frontmatter so you know which models and vendors
   exist. Do not read the bodies yet.

Keep each question short. Offer options where the answer set is known. Let
the user answer several questions in one message if they want. If the
harness has a structured question tool (Claude Code has `AskUserQuestion`),
use it; otherwise ask in plain text and parse the reply.

## 1. Harnesses

Ask: "Which of these do you drive agents from? Which one do you live in?"

Options: Claude Code, Codex CLI or app, Cursor, Gemini CLI, OpenCode, Pi,
GrokBuild, T3 Code, other. Pre-check the ones detected in step 0 and say
which binaries were found. Record `harnesses[]` with exactly one
`primary: true`.

If T3 Code is selected, ask which underlying agents it wraps for them (it
is a front end, not a model host) and record those as harnesses too.

## 2. Access

For each vendor, ask how they pay, if at all:

- **Anthropic**: none / Claude subscription (Pro, Max 5x, Max 20x, Team) /
  API key / both.
- **OpenAI**: none / ChatGPT subscription (Plus, Pro, Business) / API key /
  both. Mention that the Codex CLI is how GPT models are reached from other
  harnesses.
- **Google**: none / Gemini CLI or AI Studio key / subscription.
- **xAI**: none / API key / subscription.
- **Open-weights**: none / hosted API (OpenRouter, Zhipu, Together, …) /
  local (Ollama, LM Studio, …). If yes, ask which models they actually run.

Do not ask for keys or secrets. Record `access` only as types and plan
names.

## 3. Priorities

Explain the three axes in one line each (intelligence, taste, cost; see
`core/tasks.md` glossary) and ask:

1. "When they conflict, which order?" Default `[intelligence, taste, cost]`.
   Offer "cost first" for budget-constrained users and explain the trade:
   cheaper models can cost more in retries and human time.
2. "How much does it bother you when an agent does something dumb mid-run?"
   low / medium / high tolerance. Low tolerance pushes the table toward
   high-floor models.
3. "How tight is budget?" low / medium / high sensitivity.
4. "Does speed matter more than quality on small tasks?" yes / no. Record
   it as `priorities.speed_matters`. If yes, ask whether a faster model's
   work must still be reviewed by a smarter one before it lands; if so, set
   `priorities.speed_requires_review: true`, which adds a "Speed rule" to
   the standing rules.

## 4. Autonomy

Explain the three levels, in this order, then ask which one:

- **propose** (default): the agent branches, implements, opens PRs, and
  reports. It never merges, closes PRs, force-pushes, or deploys.
- **merge-with-gates**: the agent may merge when CI and the user's named
  review bots are green and it has answered every bot thread. Ask which
  bots they have (CodeRabbit, Cursor Bugbot, Macroscope, Greptile, other).
  If none, explain that without bots the gate has to be an independent
  review by a model other than the implementer (see the merge gate below),
  and recommend `propose` only if they do not want that.
- **goal-mode**: merge-with-gates plus permission to keep going through a
  todo list until a stated condition holds, including closing superseded
  PRs and rebasing stacks. Say plainly that this is Theo's "yolo" mode and
  only makes sense when production deploys stay human and staging can be
  broken.

Record the bots as `autonomy.reviewer_bots`. For merge-with-gates or
goal-mode, ask what must hold before the agent merges (for example "CI green
plus the named bots", or, with no bots, "CI green plus an independent review
by a model other than the implementer") and record it in their words as
`autonomy.merge_gate`. The routing table then states the gate and says never
to merge without it.

Then ask the yes/no permissions in `autonomy.may`, pre-filled for the chosen
level, and whether staging is safe to exercise freely.

## 5. Preferences and glossary

Ask, each optional:

1. Stack and languages they mostly work in.
2. Code style rules the orchestrator should pass to every implementer
   (one or two lines).
3. Machines: do they run agents on remote boxes, and how are those reached?
4. Any words they use that mean something specific to them. Show the
   default glossary from `core/tasks.md` and ask what to change or add.

## 6. Write the config

Write `~/.agent-orchestration/config.yaml` per `config-schema.md`. Fill
`models` by applying the derivation rules. Show the user the `models` block
with the derived cost scores and ask if any look wrong. Fix what they say.

## 7. Generate

Run the generator script, which implements `routing-generator.md`:
`python3 <kit root>/core/interview/generate.py --kit-root <kit root> --write`.
It writes `routing.md`, `glossary.md` and `routing.stamp`. If a table already
exists, run it with `--diff` first and show what would be lost. If the script
exits 2 (no YAML parser available), follow `routing-generator.md` by hand and
say so; no stamp is written in that case. Then
show the user the routing table (the table only, not the standing rules)
and ask two questions:

1. "Any row you'd route differently?" Apply changes as
   `routing_overrides.<task>` entries in `config.yaml` (`primary`,
   `fallback`, `reason`, optional `effort`; see `config-schema.md`), not by
   hand-editing routing.md, which gets regenerated. Re-run the generator.
2. "Should I wire this into your harness now?" See step 8.

## 8. Wire the harness

Do only what the user says yes to. Describe each change before making it.

- **Claude Code**: if the kit is installed as a plugin, its SessionStart
  hook already loads `routing.md`. Otherwise offer to append
  `@~/.agent-orchestration/routing.md` to `~/.claude/CLAUDE.md`.
- **Codex**: offer to append the same import line (or the file contents, if
  imports are not supported by their version) to `~/.codex/AGENTS.md`.
- **Cursor**: offer to write a user rule that references the file.
- **Gemini CLI**: offer to append to `~/.gemini/GEMINI.md`.
- **OpenCode / Pi / others**: offer the harness's global instructions file
  per `research/harnesses.md`.

Check the bridges: for each non-primary harness, confirm the CLI is
installed and that a one-shot invocation works (`core/bridges/<id>.md` has
the smoke-test command). Report which bridges are live.

## 9. Close

Tell the user, in a few lines:

- where the files are
- which models are enabled and which bridges are live
- the autonomy level and what the agent will never do
- that `lessons.md` is where the improvement loop appends, and that re-running
  setup keeps their answers

Remind them that the table is a default, not a limit, and that the standing
rule lets the orchestrator escalate to a smarter model when output misses
the bar.
