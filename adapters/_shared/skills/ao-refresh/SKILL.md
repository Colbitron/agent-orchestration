---
name: ao-refresh
description: Regenerate the routing table and glossary from config.yaml and the current model profiles without re-running the interview. Use when the session-start status says profiles changed or new profiles exist, when a model profile was added or edited, when the user asks to refresh, update or regenerate routing, or after editing config.yaml. Not for first-time setup, which is the ao-setup skill.
---

# Refresh

Rebuild `routing.md`, `glossary.md` and `routing.stamp` from the user's
existing `config.yaml` and the kit's current profiles. No interview. The
kit root is `KIT_ROOT`. Every `core/...` path below is relative to it. The
config dir is `$AGENT_ORCHESTRATION_HOME` if set, else
`~/.agent-orchestration`.

If `config.yaml` does not exist, stop and offer the `ao-setup` skill.

Every step runs the generator with one action flag:

```bash
python3 "KIT_ROOT/core/interview/generate.py" --kit-root "KIT_ROOT" --check --json
```

1. **Read the state.** Run the command above and read the summary. Exit 1
   only means stale. If `up_to_date` is true and `unconfigured_profiles`
   is empty, say the table is current and stop.
2. **New profiles.** If `unconfigured_profiles` is non-empty, read each
   one's frontmatter in `KIT_ROOT/core/models/`. Propose a
   `config.models` line with `enabled` and `cost` derived from the user's
   `access` block by "Derivation rules the interview applies when writing `models`" in
   `KIT_ROOT/core/interview/config-schema.md`. Ask once, with every
   proposal in a single question. Use your harness's question tool if it
   allows several answers at once; ask in plain text if your harness has
   no question tool. Write only the lines the user accepts into the
   `models` block of `config.yaml`. Change nothing else in that file. A
   profile left out stays unconfigured and is flagged again; adding it
   with `enabled: false` silences it.
3. **Preview.** Run it with `--diff` in place of `--check --json`. Show
   the user only the routing-table rows that change (task, old primary and
   effort, new primary and effort), not the whole diff. If the diff
   removes lines that no profile or config change explains, they are hand
   edits: list them, suggest where they belong (a config override or
   `lessons.md`), and ask before writing.
4. **Write.** Run it with `--write`.
5. **Fallback.** If the script exits 2 at any step, show its message (it
   names the missing YAML parser and how to install one). Then follow
   `KIT_ROOT/core/interview/routing-generator.md` by hand exactly as setup
   does, diffing before overwriting. Tell the user you did this and that
   no `routing.stamp` was written, so a staleness check may keep flagging
   until the script can run.
6. **Close.** Say where the files are (`routing.md`, `glossary.md`,
   `routing.stamp` in the config dir), give one line per changed row, and
   say the new table loads at the next session start.

Never touch `lessons.md`. Never write into any harness config.
