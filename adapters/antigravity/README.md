# Antigravity CLI (`agy`) adapter

`sh adapters/install.sh agy [--dry-run]` (alias `antigravity`) does two
things (paths from `research/harnesses.md` §4b):

- Copies the eight shared skills to
  `~/.gemini/antigravity-cli/skills/<name>/SKILL.md`, the documented global
  skills dir. The workspace path is `.agents/skills/`, but a global
  `~/.agents/skills` is not documented for `agy`.
- Appends the agent-orchestration block to `~/.gemini/GEMINI.md`, or
  creates it. Antigravity shares this file with Gemini CLI (§4, §4b), so
  installing both adapters writes the block once.

**Loading the routing table.** By instruction, through the block in
`~/.gemini/GEMINI.md`. `agy` uses the same workspace context rules as
Gemini CLI (§4b). Gemini CLI supports `@file.md` imports in `GEMINI.md`
(§4(1)). Whether `agy` does is UNVERIFIED, so the block tells the agent to
read the files instead of importing them.

**Hooks.** `agy` has a `hooks/` dir (or `hooks.json` / `settings.json`)
under `~/.gemini/antigravity-cli/` (§4b), but the schema is UNVERIFIED.
No hook is shipped.

**Invoking skills.** The research gives no explicit syntax (UNVERIFIED).
Ask by name: "use the ao-setup skill". Skills also trigger from their
descriptions.

**Subagents.** An `agents/` dir exists (§4b); schema UNVERIFIED. Not
installed.

**Limitations.**
- No documented structured question tool, so `ao-setup` asks in plain text.
- `agy` is closed source and new (2026-05-19); paths may move.
- As a bridge target, `--print-timeout` defaults to 5 minutes and must be
  raised, and stdin should come from `/dev/null` (§4b, §C.1). The bridge
  file covers this.
- `--model` persists across sessions (§4b), so a bridged call can change
  the user's interactive default.
