# Codex adapter

`sh adapters/install.sh codex [--dry-run]` (paths from
`research/harnesses.md` §2):

- Copies the eight shared skills to `~/.agents/skills/<name>/SKILL.md`
  (§2(2); the legacy `~/.codex/skills/` is no longer documented). Cursor,
  Gemini CLI and Pi read the same dir.
- Appends the agent-orchestration block to `~/.codex/AGENTS.md`, or
  creates it (§2(1)).

**Loading the routing table.** By instruction: the block tells every
session to read `routing.md`, `glossary.md` and `lessons.md` from
`~/.agent-orchestration/`. Codex reads only the first non-empty of
`~/.codex/AGENTS.override.md` and `~/.codex/AGENTS.md`, so the installer
warns if an override file would hide the block.

**Optional upgrade: SessionStart hook.** Codex has a `SessionStart` event
in `~/.codex/hooks.json` (§2(5)). A sketch reusing the Claude hook script
(merge by hand; the installer never edits this file):

```json
{ "hooks": { "SessionStart": [ { "hooks": [ { "type": "command",
  "command": "CLAUDE_PLUGIN_ROOT=<kit> sh <kit>/hooks/session-start.sh" } ] } ] } }
```

UNVERIFIED: the JSON shape (copied from Claude's) and whether hook stdout
reaches context. Non-managed hooks need trust via `/hooks`. The script's
no-table message says `/agent-orchestration:setup`; in Codex that is `$ao-setup`.

**Invoking skills.** `$ao-setup`, `$ao-lesson`, `$ao-bridge-review`, ... or `/skills` (§2(2)).

**Subagents.** TOML in `~/.codex/agents/` with `model` and
`model_reasoning_effort` (§2(3)). Not installed; `ao-setup` offers them in step 8.

**Limitations.** No structured question tool: `ao-setup` asks in plain text.
Codex may drop a skill on later turns (`core/strategies/delegation-prompting.md`
§12); re-invoke it. Computer use is ChatGPT-desktop-only, so `ao-bridge-verify`
reports it unreachable from the CLI (§0.4). UNVERIFIED: whether `CODEX_HOME`
moves the global `AGENTS.md` (the installer warns if it is set).
