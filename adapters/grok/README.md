# Grok Build adapter

`sh adapters/install.sh grok [--dry-run]` (paths from
`research/harnesses.md` §7):

- Copies the seven shared skills to `~/.grok/skills/<name>/SKILL.md`
  (§7(2)).
- Appends the agent-orchestration block to `~/.grok/AGENTS.md`, or creates
  it. **UNVERIFIED filename:** the research says global rules live in
  `~/.grok/` and lists per-directory names `Agents.md`, `Claude.md`,
  `AGENT.md`, `AGENTS.md` (§7(1)), but does not name the global file. The
  installer warns; confirm with `grok inspect`.

**Have the Claude Code plugin?** Grok reads Claude plugins, their skills
and their `hooks/hooks.json` (§7(2), §7(5), B.3), so it may already load
the kit with no install. Check `grok inspect` first; installing anyway
gives duplicate skill names.

**Loading the routing table.** By instruction, through the block (rules
files are capped at 10,000 characters, §7(1); the block is far below).

**Optional upgrade: session hook.** Grok hooks use Claude's schema, as
`[[hooks.<Event>]]` tables in `~/.grok/config.toml` (§7(5)). Sketch; merge
by hand. The event name `SessionStart` is UNVERIFIED (the research shows
only `PreToolUse` and says "session start"):

```toml
[[hooks.SessionStart]]
  [[hooks.SessionStart.hooks]]
  type = "command"
  command = "CLAUDE_PLUGIN_ROOT=<kit> sh <kit>/hooks/session-start.sh"
```

**Invoking skills.** `/ao-setup`, `/ao-lesson`, `/ao-bridge-review`, ...; `/skills` lists them (§7(2)).

**Subagents.** Profiles in `~/.grok/agents/`, model pins in
`[subagents.models]` (§7(3)). Not installed; `ao-setup` offers them in step 8.

**Limitations.** Grok's `agent` symlink shadows Cursor's CLI (§0.2).
Headless permission behaviour without `--permission-mode` is UNVERIFIED.
