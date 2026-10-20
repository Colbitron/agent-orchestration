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
3. **Invoke the skills**: `ao-setup`, `ao-refresh`, `ao-orchestrate`,
   `ao-lesson`, and the four bridges (`ao-bridge-review`,
   `ao-bridge-implement`, `ao-bridge-investigate`, `ao-bridge-verify`).

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
  undocumented. OpenClaw reads `~/.agents/skills/` too but gets its managed
  dir so the skills are shared by every OpenClaw agent; Hermes reads only
  its own `~/.hermes/skills/<category>/` unless configured otherwise.
- **OpenClaw and Hermes Agent are assistant runtimes** [§0.7]: a chat
  gateway, cron and subagents around an embedded agent. Their global
  instructions files are the workspace `AGENTS.md` (OpenClaw) and
  `SOUL.md` (Hermes), both injected into every session. Both seed those
  files on first run, so the installer refuses to create them and asks for
  `openclaw onboard` or a first `hermes` run instead.
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
| OpenClaw [§9] | `<repo>/AGENTS.md` with `agent exec --cwd` | `~/.openclaw/workspace/AGENTS.md` (`$OPENCLAW_WORKSPACE_DIR`; per-agent `workspace-<id>/`) | `~/.openclaw/skills/` | `agents.entries.<id>` in `openclaw.json`, `model: provider/model`; `sessions_spawn` takes `model` per call | `~/.openclaw/hooks/<name>/HOOK.md`, `agent:bootstrap` | fragment; `bootstrap-extra-files` unsuitable (workspace-only); `agent-guidance` plugin possible (16 KiB/file, reload on regenerate) |
| Hermes Agent [§10] | `AGENTS.md`, `CLAUDE.md`, `.hermes.md` | `~/.hermes/SOUL.md` (`$HERMES_HOME`) | `~/.hermes/skills/agent-orchestration/` | `delegate_task`; global `delegation.model` + `delegation.provider` | `hooks:` in `config.yaml`, `on_session_start` (observe-only) | fragment; `skills.auto_load` optional |

Gemini CLI and Antigravity share `~/.gemini/GEMINI.md`; the marker check
makes the second install a no-op for that file.

## Install recipe

```sh
sh adapters/install.sh <harness> --dry-run      # see what would change
sh adapters/install.sh <harness> [--kit-root PATH]
sh adapters/install.sh <harness> --update       # after pulling a new kit version
```

For each harness the script:

1. Resolves `KIT_ROOT` (default: this repo) and checks it holds `core/`.
2. Copies `_shared/skills/*` into the global skills dir, replacing the
   `KIT_ROOT` placeholder with the path (sed into a temp file, then `mv`).
   A plain install never overwrites an existing skill file: it is reported
   as "up to date" or "SKIPPED (differs)".
3. Writes a manifest, `<skills dir>/.agent-orchestration-manifest`. Its
   first line names the hash tool (`shasum -a 256`, else `sha256sum`, else
   `cksum`); each other line is `<hash> <path relative to the skills dir>`,
   the hash of the file as installed (placeholder substituted).
4. Appends `_shared/AGENTS.fragment.md` (placeholder substituted) to the
   global instructions file, or creates the file. If the marker
   `<!-- agent-orchestration -->` is already there, it does nothing. To
   uninstall, delete the block between that marker and
   `<!-- /agent-orchestration -->`.
5. Prints harness-specific warnings (override files that shadow the target,
   UNVERIFIED paths) and the next step: open a new session and run the
   `ao-setup` skill.

`--update` brings an earlier install up to date. A skill file whose hash
still matches the manifest (you never edited it) is overwritten and its
manifest entry updated. One whose hash differs is reported as "SKIPPED
(edited locally; use --force to overwrite)" and keeps its old entry, so the
next update still sees the edit. With no manifest (an install from before
manifests existed), every existing file that differs counts as edited and
is skipped. The block between the two markers in the instructions file is
replaced with the current fragment, never appended twice; if the markers
are not exactly one well-formed block, the file is left alone with a
warning. For Cursor, the paste file `cursor-user-rule.md` is rewritten.

`--force` implies `--update` and also overwrites edited skill files.
`--dry-run` combines with both and reports what each file would get.

The kit root is baked into the installed files. If you move the repo,
re-run with `--update` (or `--force` for files you edited).

## Adding a harness

Add a `case` arm to `install.sh` with the paths from `research/harnesses.md`
(cite the section), add `adapters/<harness>/README.md`, and add a row to
the matrix above. If a path is not confirmed in the research, set the
`*_UNVERIFIED` variable so the script warns at runtime.
