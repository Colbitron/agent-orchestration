# OpenCode adapter

`sh adapters/install.sh opencode [--dry-run]` does two things (paths from
`research/harnesses.md` §5):

- Copies the eight shared skills to
  `~/.config/opencode/skills/<name>/SKILL.md` (§5(2)). The global
  `~/.agents/skills` path is only implied by the docs (UNVERIFIED), so the
  native dir is used.
- Appends the agent-orchestration block to `~/.config/opencode/AGENTS.md`,
  or creates it (§5(1)).

**Watch out.** OpenCode falls back to `~/.claude/CLAUDE.md` only when
`~/.config/opencode/AGENTS.md` is absent (§5(1)). Creating that file ends
the fallback; the installer warns when this applies. To keep both, add
`"instructions": ["~/.claude/CLAUDE.md"]` to
`~/.config/opencode/opencode.json` (§5(1) item 3).

**Loading the routing table.** By instruction, through the block above.
Alternative: list the files in `opencode.json` → `"instructions"`, which
loads them directly (§5(1)). Only do this after `ao-setup` has created
`routing.md`.

**Hooks.** None in shell/JSON form. JS/TS plugins in
`~/.config/opencode/plugins/` receive `session.created` (§5(5)), but the
research does not say how a plugin adds context, so none is shipped.

**Invoking skills.** The research gives no explicit invocation syntax
(UNVERIFIED). Ask by name: "use the ao-setup skill". Skills also load from
their descriptions. For a slash command, add
`~/.config/opencode/commands/ao-setup.md` with frontmatter `description`
and a body like `Use the ao-setup skill. $ARGUMENTS` (§5(4)).

**Subagents.** Markdown in `~/.config/opencode/agents/` with `description`,
`mode: subagent`, `model: provider/model-id` (§5(3)). Not installed; the
ao-setup skill offers them in step 8.

**Limitations.** No documented structured question tool. Claude Pro/Max
subscription login is not supported (§5), so Claude models need an API key
or the `claude-cli` bridge.
