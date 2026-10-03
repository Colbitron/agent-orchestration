# Adapters

An adapter makes the harness-neutral kit in `core/` usable from one coding
harness. Adapters hold glue, not knowledge: files in the harness's native
locations plus one install script. There is no runtime.

Every adapter has to give the user three things (`docs/ARCHITECTURE.md`,
"What the adapters must provide"):

1. **Run the setup interview** (`core/interview/setup-interview.md`), which
   writes `~/.agent-orchestration/{config.yaml,routing.md,glossary.md}`.
2. **Load the routing table every session**: `routing.md`, `glossary.md`,
   and `lessons.md` from `~/.agent-orchestration/`.
3. **Invoke the skills**: `ao-setup`, `ao-orchestrate`, `ao-lesson`, and the four
   bridges (`ao-bridge-review`, `ao-bridge-implement`, `ao-bridge-investigate`,
   `ao-bridge-verify`).

Subagent definitions with pinned models depend on the user's routing table,
so they are not installed here. The ao-setup skill offers to write them in
step 8 for harnesses that support them.

## Shared conventions

All facts below come from `research/harnesses.md` (section numbers in
brackets).

- **Agent Skills (`SKILL.md`) is read by every harness here** [B.1]. The
  shared skills in `_shared/skills/` use only the spec fields `name` and
  `description`, so one copy works everywhere.
- **`.agents/skills/` is the cross-harness skills path** [B.1, B.3]. Codex,
  Cursor, Gemini CLI and Pi read `~/.agents/skills/` globally, so one
  install serves all four. OpenCode, Antigravity and Grok get their own
  native global dirs because their `~/.agents/skills` support is
  undocumented.
- **`AGENTS.md` is read by most harnesses** [B.2]. Gemini CLI and
  Antigravity use `~/.gemini/GEMINI.md` globally. Cursor has no global file;
  its User Rules live in settings.
- **Claude Code is different**: it uses `CLAUDE.md` and `.claude/skills/`
  and does not read `.agents/` [§1, B.3]. It is served by the plugin at the
  repo root, whose SessionStart hook (`hooks/session-start.sh`) injects the
  routing table. `install.sh claude` only prints the plugin commands.
- **No SessionStart hook is assumed elsewhere.** Several harnesses document
  a session-start event, but the research does not confirm that hook output
  reaches the model's context. So the loader is an *instruction*:
  `_shared/AGENTS.fragment.md`, appended to the global instructions file,
  tells the agent to read the three files at session start. Each harness
  README shows the hook as an optional upgrade where one exists.

## Matrix

| Harness | Project instructions | Global instructions (install target) | Global skills (install target) | Subagents | Hooks | Session load |
|---|---|---|---|---|---|---|
| Claude Code [§1] | `CLAUDE.md`, `AGENTS.md` if no CLAUDE.md | `~/.claude/CLAUDE.md` (not touched) | plugin `skills/` | `.claude/agents/*.md`, `model:` pin | `settings.json`, plugin `hooks/hooks.json` | plugin SessionStart hook |
| Codex [§2] | `AGENTS.md` (`AGENTS.override.md` wins) | `~/.codex/AGENTS.md` | `~/.agents/skills/` | `~/.codex/agents/*.toml`, `model` | `~/.codex/hooks.json`, `SessionStart` | fragment; hook optional |
| Cursor [§3] | `.cursor/rules/*.mdc`, `AGENTS.md`, `CLAUDE.md` | none: User Rules in settings (paste `~/.agent-orchestration/cursor-user-rule.md`) | `~/.agents/skills/` | `~/.cursor/agents/*.md`, `model` | `~/.cursor/hooks.json`, `sessionStart` | pasted user rule; hook optional |
| OpenCode [§5] | `AGENTS.md`, `CLAUDE.md` fallback | `~/.config/opencode/AGENTS.md` | `~/.config/opencode/skills/` | `~/.config/opencode/agents/*.md`, `model` | JS/TS plugins, `session.created` | fragment |
| Pi [§6] | `AGENTS.md`, `CLAUDE.md` | `~/.pi/agent/AGENTS.md` (`$PI_CODING_AGENT_DIR`) | `~/.agents/skills/` | none (by design) | TS extensions, `session_start` | fragment |
| Grok Build [§7] | `AGENTS.md`, `Agents.md`, `AGENT.md`, `CLAUDE.md` | `~/.grok/AGENTS.md` (filename UNVERIFIED) | `~/.grok/skills/` | `~/.grok/agents/*.md`, `[subagents.models]` | `config.toml` `[[hooks.<Event>]]`, Claude schema | fragment; hook optional |
| Antigravity `agy` [§4b] | `GEMINI.md`, `AGENTS.md` | `~/.gemini/GEMINI.md` | `~/.gemini/antigravity-cli/skills/` | `agents/` dir (schema UNVERIFIED) | `hooks/` dir (schema UNVERIFIED) | fragment |
| Gemini CLI [§4] | `GEMINI.md` (AGENTS.md opt-in) | `~/.gemini/GEMINI.md` | `~/.agents/skills/` | `~/.gemini/agents/*.md`, `model` | `~/.gemini/settings.json`, `SessionStart` | fragment; hook optional |

Gemini CLI and Antigravity share `~/.gemini/GEMINI.md`; the marker check
makes the second install a no-op for that file.

## Install recipe

```sh
sh adapters/install.sh <harness> --dry-run      # see what would change
sh adapters/install.sh <harness> [--kit-root PATH]
```

For each harness the script:

1. Resolves `KIT_ROOT` (default: this repo) and checks it holds `core/`.
2. Copies `_shared/skills/*` into the global skills dir, replacing the
   `KIT_ROOT` placeholder with the path (sed into a temp file, then `mv`).
   An existing skill file is never overwritten: it is reported as "up to
   date" or "SKIPPED (differs)". Delete it and re-run to update.
3. Appends `_shared/AGENTS.fragment.md` (placeholder substituted) to the
   global instructions file, or creates the file. If the marker
   `<!-- agent-orchestration -->` is already there, it does nothing. To
   uninstall, delete the block between that marker and
   `<!-- /agent-orchestration -->`.
4. Prints harness-specific warnings (override files that shadow the target,
   UNVERIFIED paths) and the next step: open a new session and run the
   `ao-setup` skill.

The kit root is baked into the installed files. If you move the repo,
delete the installed skills and the marked block, then re-run.

## Adding a harness

Add a `case` arm to `install.sh` with the paths from `research/harnesses.md`
(cite the section), add `adapters/<harness>/README.md`, and add a row to
the matrix above. If a path is not confirmed in the research, set the
`*_UNVERIFIED` variable so the script warns at runtime.
