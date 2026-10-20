# Pi adapter

`sh adapters/install.sh pi [--dry-run]` does two things (paths from
`research/harnesses.md` §6):

- Copies the eight shared skills to `~/.agents/skills/<name>/SKILL.md`,
  one of Pi's documented user skill dirs (§6(2)). Codex, Cursor and Gemini
  CLI read the same dir.
- Appends the agent-orchestration block to `~/.pi/agent/AGENTS.md`, or
  creates it. If `PI_CODING_AGENT_DIR` is set, that dir is used instead
  (§6(1)).

**Loading the routing table.** By instruction, through the block above.
Pi loads `AGENTS.md` from its agent dir every session. An
`AGENTS.override.md` in the same dir replaces it (§6(1)); the installer
warns if one exists. `-nc` disables context files, and with them the
loader.

**Optional upgrade: extension.** Pi has no hook config, but TypeScript
extensions in `~/.pi/agent/extensions/` receive `session_start` (§6(5)).
The research does not show how an extension injects context, so none is
shipped (UNVERIFIED).

**Invoking skills.** `/skill:ao-setup`, `/skill:ao-orchestrate`, `/skill:ao-lesson`,
`/skill:ao-bridge-review` and so on, with arguments after the name (§6(2)).
They also trigger from their descriptions. For a shorter command, add a
prompt template at `~/.pi/agent/prompts/<name>.md` (§6(4)).

**Subagents.** None: Pi omits subagents by design (§6(3)). The
`ao-orchestrate` skill tells the agent to do bounded pieces itself or bridge
them; it will not pretend to spawn one.

**Limitations.**
- No structured question tool, so `ao-setup` asks in plain text.
- Pi has no approval system (§6(7)). Bridged read-only calls depend on the
  callee's own flags; read the bridge file before running.
- Which consumer subscriptions `/login` supports is UNVERIFIED (§6).
