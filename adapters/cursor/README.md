# Cursor adapter

`sh adapters/install.sh cursor [--dry-run]` (paths from
`research/harnesses.md` §3):

- Copies the seven shared skills to `~/.agents/skills/<name>/SKILL.md`,
  a documented Cursor user skills dir (§3(2)) that Codex, Gemini CLI and
  Pi also read.
- Writes the agent-orchestration block to
  `~/.agent-orchestration/cursor-user-rule.md`. Cursor has **no global
  instructions file**; User Rules live in settings (§3(1)). Paste the file
  into Cursor Settings > Rules > User Rules (`pbcopy <` the file).

**Loading the routing table.** By instruction, through that User Rule. Per
project, a `.cursor/rules/agent-orchestration.mdc` rule works too
(frontmatter `description`, `globs`, `alwaysApply`; §3(1)):

```
---
description: Load the user's agent-orchestration routing table
alwaysApply: true
---
<contents of ~/.agent-orchestration/cursor-user-rule.md>
```

**Hook.** Cursor has `sessionStart` in `~/.cursor/hooks.json` (§3(5)), but
no schema or context-injection behaviour is documented: none shipped (UNVERIFIED).

**Invoking skills.** `/ao-setup` or `@ao-setup`; likewise `ao-orchestrate`, `ao-lesson`
and the `ao-bridge-*` skills (§3(2)).

**Subagents.** Markdown in `~/.cursor/agents/` (`name`, `description`,
`model` with bracket params such as `[effort=high]`, `readonly`; §3(3)).
Not installed; the ao-setup skill offers them in step 8.

**Limitations.** No documented structured question tool. The CLI binary
`agent` collides with Grok Build's `agent` symlink (§0.2), so bridges call
Cursor by absolute path. Cursor also reads `~/.claude/skills/` and
`~/.codex/skills/` (§3(2)); other kits' skills may share names.
