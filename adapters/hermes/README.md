# Hermes Agent adapter

`sh adapters/install.sh hermes [--dry-run]` does two things (paths from
`research/harnesses.md` §10):

- Copies the eight shared skills to
  `~/.hermes/skills/agent-orchestration/<name>/SKILL.md` (§10(2)). A
  category directory is not required: the loader walks `~/.hermes/skills`
  recursively (`os.walk(..., followlinks=True)`, src: agent/skill_utils.py),
  so a flat `skills/<name>/SKILL.md` is found and listed under `general`.
  The kit uses its own category, `agent-orchestration`, so its skills stay
  grouped. No frontmatter is required for discovery (a missing `name` falls
  back to the directory name), but `skill_manage` validation wants `name`
  and `description`, which the kit's skills have. `$HERMES_HOME` replaces
  `~/.hermes` when set.
- Appends the agent-orchestration block to `~/.hermes/SOUL.md` (§10(1)).
  That file is the only global instructions file Hermes has: it is
  inserted verbatim as the first section of the system prompt, user-owned,
  and never overwritten by Hermes, with four exceptions. An untouched
  legacy scaffold (a `# Hermes Agent Persona` heading plus an HTML comment)
  is auto-upgraded (src: hermes_cli/config.py, hermes_cli/default_soul.py).
  `hermes profile update` rewrites a distribution-owned profile's
  `SOUL.md`. `hermes claw migrate --overwrite` replaces it. Config
  migration v41 strips a "Messaging other agents" section.

**Profiles.** A named profile (`hermes -p <name>`, home
`~/.hermes/profiles/<name>/`) or a sticky one (`hermes profile use`) has
its own `SOUL.md` and `skills/`: "Each profile gets its own directory
containing its own `config.yaml`, `.env`, `SOUL.md`, memories, sessions,
skills" (docs: user-guide/profiles). The installer targets only the home it
is given. To install into a profile, set
`HERMES_HOME=~/.hermes/profiles/<name>`.

**Run `hermes` once first.** The installer stops if `SOUL.md` does not
exist, because Hermes seeds its starter identity there on first run; a
file that holds only the kit block would become the whole identity. Edge
case: a `SOUL.md` that is still the old heading-plus-comment scaffold passes the
exists check. Once the kit block is appended, Hermes no longer
auto-upgrades it, so the block becomes the whole identity. Run `hermes`
once and confirm `SOUL.md` has real content before installing
(source-derived, not run). The installer warns when the file is under 200
bytes or holds only comments and blank lines.

**Loading the routing table.** By instruction, through the block. Hermes
loads `SOUL.md` in every session, including gateway and cron runs, up to
`context_file_max_chars` (dynamic, floor 20,000, ceiling 500,000
characters, §10(1)). Above the cap Hermes keeps the first 70 % and the last
20 % (src: agent/prompt_builder.py). The kit block is appended at the end,
so it survives only inside that tail; at 1.9 KB it is safe unless
`SOUL.md` itself exceeds the cap. `--ignore-rules` skips the file, and with
it the loader.

**Subagents' context.** Children spawned by `delegate_task` get no
`SOUL.md`, no memory and no parent history (src: tools/delegate_tool.py
`skip_context_files=True, skip_memory=True`; "SOUL.md is excluded", docs:
user-guide/features/delegation). When the parent has a resolved workspace
they receive that workspace's project context file, the first match of
`.hermes.md`, the `AGENTS.md` chain, `CLAUDE.md`, `.cursorrules`. Hermes
has no import or include syntax for these files, so a repo `AGENTS.md`
reaches a child only if it contains the loader instruction itself, and the
child can follow it only if its inherited toolsets include `file` or
`terminal`.

**Hooks and other prompt routes.** Shell hooks in `config.yaml` (`hooks:`)
fire on `on_session_start`, but that event is observer-only ("Return value:
Ignored", docs: user-guide/features/hooks). `pre_llm_call` can inject text,
but into the user message: "Always the user message, never the system
prompt". Among hooks, only a Python plugin's
`register_system_prompt_section()` (4,000 characters per section, 8,000
and 32 sections in total) writes into the system prompt (§10(5)).
Config-only routes also exist: `skills.auto_load` loads a skill's full text
into the system prompt at the start of every new session on every surface
(docs: user-guide/configuration; `--ignore-rules` suppresses it, children
skip it), and `HERMES_EPHEMERAL_SYSTEM_PROMPT` or `agent.system_prompt` add
inline text. None reads `~/.agent-orchestration` by itself, and none is
shipped; `SOUL.md` is the loader.

Optional upgrade, not shipped: add `ao-orchestrate` to `skills.auto_load`
in `config.yaml` so the orchestration rules are in every session's prompt.
A shell `pre_llm_call` hook that cats `routing.md` on the first turn is
possible but UNVERIFIED.

**Invoking skills.** `/ao-setup`, `/ao-orchestrate`, `/ao-lesson`,
`/ao-bridge-review` and so on: every installed skill is a slash command, and
`hermes chat -s ao-orchestrate` preloads one (§10(2)). The system-prompt
skill index shows each skill's name plus its description cut to 60
characters (`SKILL_PROMPT_DESC_LIMIT = 60`, src: agent/skill_utils.py), so
the model sees, for example, "ao-setup: Interview the user about their
harnesses, model subscript...". The full description is only in
`SKILL.md` and in `skills_list`/`skill_view` results, so invoke by
`/<name>` when it matters.

**Picking up changes.** New skills need no gateway restart: "your next
message to the agent carries a short note naming the new skills", and the
prompt picks them up at the next compaction; `/reload-skills` refreshes the
slash commands (docs: user-guide/features/skills). `SOUL.md` changes take
effect in a new session; existing sessions keep the old prompt (docs:
user-guide/profiles).

**Subagent model.** `delegate_task` spawns children; the model is pinned
globally with `delegation.model` and `delegation.provider`, not per call
("`delegate_task` has no per-task model parameter", docs:
user-guide/features/delegation; §10(3)). Set the pin yourself:
`hermes config set delegation.model <M>` and
`hermes config set delegation.provider <P>`. It is global, so pick the
model that fits most subagent rows in the routing table.
`delegation.reasoning_effort` exists in source only (src:
tools/delegate_tool_config.py, undocumented).

**Bridge skills inside Hermes.** The `terminal` tool's default per-command
timeout is 180 s and the foreground cap is 600 s. A call with
`timeout=1200` is promoted to a tracked background process; or pass
`background=true` and poll with `process_manage` (docs:
user-guide/configuration `terminal.timeout`; src: tools/terminal_tool.py,
the foreground cap is source-only). In one-shot sessions nothing notifies,
so poll. A subagent that shows no progress for 1200 s inside one tool call
is interrupted (the stale-progress threshold, docs:
user-guide/features/delegation), so a silent 20-minute bridge is borderline
there: run bridges from the main session.

**Limitations.**
- Questions need the main session. Hermes has a `clarify` tool (up to 5
  questions per call, each up to 4 choices plus an automatic "Other" row;
  src: tools/clarify_tool.py; "Ask the user a question when the agent needs
  clarification", docs: reference/toolsets-reference), so `ao-setup` can
  use it. It is not in the subagent, api-server or ACP toolsets, so fall
  back to plain text there.
- No read-only file toolset (§10(7)): a review that must read the tree can
  still write through `terminal`. The read-only template pipes the diff
  into the callee instead; see `core/bridges/hermes-cli.md`.
- Claude Pro subscriptions cannot be used through Hermes's Anthropic OAuth,
  and Claude Max draws only on extra-usage credits (§10 Auth); use
  `ANTHROPIC_API_KEY` or the `claude-cli` bridge for Claude models.
- `.claude/skills` is not read by default; `hermes import-agent claude-code`
  copies it once into `~/.hermes/skills/claude-code-imports/`, and
  `hermes import-agent --sync` re-imports changes. `skills.external_dirs`
  can instead point at `~/.claude/skills` to read it live (docs:
  user-guide/import-from-other-agents).
