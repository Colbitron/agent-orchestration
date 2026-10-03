---
name: ao-bridge-investigate
description: Send a read-only root-cause investigation or code analysis to a model in another harness by calling its CLI one-shot, then check its evidence. Use for hard bugs, flaky failures, performance regressions, or "how does this work / how should we split this" questions when the routing table's investigate or analyze row names a model outside this harness.
---

# Bridge: investigate

Kit root: `KIT_ROOT`. Investigation and analysis are read-only: the callee
finds and proves, it does not fix.

## 1. Pick the investigator

1. Use the `investigate` or `analyze` row of
   `~/.agent-orchestration/routing.md`. If no routing table exists, stop
   and run the `ao-setup` skill.
2. Default preference (`KIT_ROOT/core/bridges/README.md`): `codex-cli`
   with Sol at high effort; Astra as the escalation. Use only bridges the
   routing table marks live.
3. Inside T3 Code, if a `delegate_task` tool from the `t3-code` MCP server
   is available, prefer it with `role: research` and
   `interactionMode: plan`. The child sees only your task text.
4. Read `KIT_ROOT/core/bridges/<id>.md` and use its read-only command
   template exactly. If the file is missing, say so and stop; never compose
   CLI flags from memory.

## 2. Write the prompt

Self-contained and literal. Include the symptom, repro steps, logs or run
links, the absolute repo path, and a bound. Investigate template
(`KIT_ROOT/core/strategies/delegation-prompting.md` §14):

```
<Symptom, repro steps, logs, run link.> Repository: <absolute path>.
Find the root cause and reproduce it before you claim it. Do not fix it and
do not edit files. Done means a root cause with evidence (repro, failing
test, or trace) and the file:line where it originates. List what you ruled
out. Mark anything you could not confirm as UNCONFIRMED.
If you cannot find it after <bound>, stop and report what you tried.
```

For an analysis question, use the `analyze` template instead: "Read
whatever you need; do not change code. Done means <plan | ranked list |
map> with file references per claim. If something is fine, say so rather
than inventing work." Never put secrets in the prompt.

## 3. Run it

- Read-only flags from the bridge file. Timeout: 20 minutes:
  `sh KIT_ROOT/core/bridges/_timeout.sh 1200 <cmd>`
  (exit 124 = timed out). Pipe the prompt in or redirect stdin from
  `/dev/null`; it must not be a terminal.
- Capture output to `/tmp/agent-orchestration/investigate-<model>.md`,
  then read that file. Run it in the background if your harness allows.

## 4. Handle the result

1. A timeout is "no result", not "no cause". Check for partial output.
2. Check the claimed evidence yourself: run the repro or failing test,
   open the cited file:line. Do not re-derive the whole analysis.
3. If the cause is unproven or the answer misses the bar, escalate once to
   the next model in the row without asking.
4. Report with the bridge id prefix: cause, evidence, origin file:line,
   what was ruled out, and what stays unconfirmed.
5. If a fix is wanted, route it per the routing table (`ao-bridge-implement`
   or this harness), not back through this skill.
