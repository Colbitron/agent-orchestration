# OpenClaw adapter

`sh adapters/install.sh openclaw [--dry-run]` does two things (paths from
`research/harnesses.md` §9):

- Copies the eight shared skills to `~/.openclaw/skills/<name>/SKILL.md`,
  the managed skills dir shared by every agent (§9(2)). Workspace `skills/`,
  project `.agents/skills/` and personal `~/.agents/skills/` rank higher, so
  a kit copy installed there for Codex, Cursor, Gemini or Pi shadows this
  one; update both or remove one.
- Appends the agent-orchestration block to the default workspace's
  `AGENTS.md`: `~/.openclaw/workspace/AGENTS.md`, or
  `$OPENCLAW_WORKSPACE_DIR/AGENTS.md` when that is set (§9(1)).

**Run `openclaw onboard` first.** OpenClaw seeds its default `AGENTS.md`
template when it first prepares the workspace, and it never overwrites an
existing `AGENTS.md` ("`openclaw setup` can recreate missing defaults
without overwriting existing files",
https://docs.openclaw.ai/concepts/agent-workspace). If the kit created the
file first, it would hold only the kit block, and OpenClaw's default
operating instructions would never be written. So the installer stops
unless `AGENTS.md` already exists.

**After installing.** The file watcher (`skills.load.watch`, on by default)
picks up the new skills. The docs disagree on whether a running session sees
them (tools/skills says on its next turn, creating-skills says start a new
session), so if `/skill ao-setup` is not found, send `/new`. No Gateway
restart is needed (https://docs.openclaw.ai/tools/creating-skills).

**Per-agent workspaces.** A sole configured agent uses the default
workspace, so the block already reaches it. In a multi-agent roster,
entries without `workspace` use `<agents.defaults.workspace>/<id>` when
that root is set, else `~/.openclaw/workspace-<id>/`. Entries can also pin
their own `workspace`. Each workspace has its own `AGENTS.md`, and
`openclaw agents list` shows the real paths. The installer touches only the
default workspace; copy the block between the markers into the other
agents' files by hand (https://docs.openclaw.ai/concepts/agent-workspace).
`OPENCLAW_WORKSPACE_DIR` overrides the default locations; the docs do not
rank it against an explicit `agents.defaults.workspace`, so trust
`openclaw agents list`. The installer ignores `OPENCLAW_PROFILE` and
`OPENCLAW_STATE_DIR`, which relocate both the workspace and the managed
skills dir. Sub-agents run in `minimal` prompt mode and still get
`AGENTS.md`, so the block reaches them.

**Loading the routing table.** By instruction, through the block. Each
bootstrap file is capped at 20,000 characters and the set at 60,000
(§9(1)); the block is far below that. In a normal Gateway session the
`read` tool is unrestricted unless `tools.fs.workspaceOnly: true`, a
`read-only`/`guarded`/`workspace` permission mode, or sandboxing is set
(https://docs.openclaw.ai/gateway/permission-modes), so it can open
`~/.agent-orchestration/*.md`. In `openclaw agent exec --cwd <D>` runs,
file tools are restricted to `<D>`, and the workspace `AGENTS.md` is not
injected at all: exec sets `skipBootstrap`, and only `<D>/AGENTS.md` is
loaded. So the kit block does not reach exec runs; that is the outbound
bridge's job (`core/bridges/openclaw-cli.md`).

**No bootstrap hook shipped.** The bundled `bootstrap-extra-files` hook
(config `hooks.internal.entries.bootstrap-extra-files.{enabled, paths}`)
only loads files inside the workspace, and only files named `AGENTS.md`,
`SOUL.md`, `IDENTITY.md`, `USER.md`, `BOOTSTRAP.md` or `MEMORY.md` ("Paths
resolve relative to the event's workspace and must remain inside it",
https://docs.openclaw.ai/automation/hooks/bundled-hooks). It cannot load
`~/.agent-orchestration/routing.md`. The `agent-guidance` plugin can
inject files from an absolute operator directory
(`plugins.entries.agent-guidance.config.{directory, agents, append}` with
`hooks.allowPromptInjection: true`). But it caps each file at 16 KiB and
reads files once at registration, so it needs
`openclaw plugins reload agent-guidance` after every regenerate
(https://docs.openclaw.ai/plugins/agent-guidance). The read-by-instruction
loader stays the shipped path.

**Invoking skills.** `/skill ao-setup` always works. The native command is
`/ao_setup`, because OpenClaw sanitizes skill command names ("Names are
sanitized to `a-z0-9_` (max 32 chars)",
https://docs.openclaw.ai/tools/slash-commands), so `/ao-setup` does not
match. `$ao-setup` in a message also references the skill. In
Discord and Telegram `commands.nativeSkills: "auto"` registers them as
native commands. Skills also
trigger from their descriptions (§9(2)).

**Subagents.** `sessions_spawn` takes `model` and `thinking` per call;
`agents.entries.<id>.model: "provider/model"` pins an agent, and
`agents.defaults.subagents.model` the default child (§9(3)). Not installed;
`ao-setup` offers them in step 8.

**Bridging out.** OpenClaw can dispatch to Claude Code, Codex, OpenCode,
Gemini CLI, Cursor and others over ACP (`acp.enabled`, the `acpx` plugin,
`/acp spawn <agent> --cwd <abs>`, §9(3)). Prefer that over shelling out when
the routing row points at a harness OpenClaw already has configured; the
bridge files in `core/bridges/` cover the shell path.

**Bridge skills inside OpenClaw.** The `exec` tool returns a handle after
`yieldMs` (default 10 s), and the agent must `process poll` for the result.
The default `tools.exec.timeoutSeconds` is 1800 s, so a 20-minute bridge
fits; anything longer needs a per-call `timeoutSeconds`. If you have set
exec to `ask` or `allowlist`, bridge commands are prompted or denied
(https://docs.openclaw.ai/tools/exec,
https://docs.openclaw.ai/tools/exec-approvals).

**Limitations.**
- `ao-setup` uses OpenClaw's `ask_user` tool where it exists (main session
  on Discord, Slack, Telegram or WebChat) and plain text elsewhere and in
  sub-agents (https://docs.openclaw.ai/tools/ask-user).
- `openclaw agent exec` (§9(7)) runs against a temporary state dir with
  your stored credentials, so bridged calls work beside a running Gateway;
  only `--state-dir` needs the Gateway stopped. The Gateway path
  (`openclaw agent --agent <id>`) has no per-call working directory.
- `CLAUDE.md` is never read; `openclaw migrate claude` imports it once.
- The research reflects the docs of about v2026.10; builds from early 2026
  (the `TOOLS.md`/`HEARTBEAT.md` era) differ, so run `openclaw update`.
  Installations older than July 2026 must upgrade to `2026.9.5` first
  (https://docs.openclaw.ai/install/updating).
- `openclaw onboard --reset --reset-scope full` trashes the workspace, so
  re-run the installer after a full reset.
