# Gemini CLI adapter

Legacy for consumers: since 2026-06-18 Gemini CLI serves only Gemini API
keys, Vertex AI and Code Assist (§0.1, §4). Google AI Pro/Ultra users want
`adapters/antigravity/`.

`sh adapters/install.sh gemini [--dry-run]` (paths from
`research/harnesses.md` §4):

- Copies the eight shared skills to `~/.agents/skills/<name>/SKILL.md`;
  in the user tier `.agents/` beats `.gemini/` (§4(2)). Codex, Cursor and
  Pi read the same dir.
- Appends the agent-orchestration block to `~/.gemini/GEMINI.md`, or
  creates it (§4(1)). Antigravity shares this file.

**Loading the routing table.** By instruction, through the block. Once
`ao-setup` has created `routing.md`, `GEMINI.md` can import it directly
(`@file.md` imports, §4(1)): add `@~/.agent-orchestration/routing.md`
(and `glossary.md`, `lessons.md`), then check with `/memory show`.

**Optional upgrade: SessionStart hook.** `SessionStart` under the `hooks`
key of `~/.gemini/settings.json`, `type: "command"` only (§4(5)). Sketch;
merge by hand. The nesting is copied from Claude's schema and is
UNVERIFIED, as is whether stdout reaches context:

```json
{ "hooks": { "SessionStart": [ { "hooks": [ { "type": "command",
  "command": "CLAUDE_PLUGIN_ROOT=<kit> sh <kit>/hooks/session-start.sh" } ] } ] } }
```

**Invoking skills.** `/skills list` shows them (§4(2)); no per-skill
syntax is documented (UNVERIFIED), so ask by name: "use the ao-setup skill".
For a slash command, add `~/.gemini/commands/ao/setup.toml` with
`description` and `prompt = "Use the ao-setup skill. {{args}}"`; it becomes
`/ao:setup` (§4(4)).

**Subagents.** Markdown in `~/.gemini/agents/` (`name`, `description`,
`model`; §4(3)). Not installed; the ao-setup skill offers them in step 8.

**Limitations.** No documented structured question tool; no effort flag (§4(7)).
