---
name: bridge-investigate
description: Delegate root-cause analysis, deep bug hunting, log digging, codebase audits, or large-document reading to the model the routing table lists for `investigate`, `analyze`, `bulk`, or `research` (often GPT-6.1 Sol on high, or a cheap model for logs), read-only, with a self-contained question. Use when a bug is not visible from reading the code, when the user asks why something happens, to dig through logs, or to read a large document or spec, or when the routing row for that work points at a bridged model. Returns evidence (file:line, commands run, what was ruled out) that you check before relaying.
user-invocable: true
argument-hint: "<symptom or question> [repro / log path / doc path]"
---

# Bridge investigate

The kit root is `${CLAUDE_PLUGIN_ROOT}`, also announced in the
`<agent-orchestration>` block at session start. Read
`${CLAUDE_PLUGIN_ROOT}/core/bridges/README.md` and the `investigate`,
`analyze`, `bulk`, and `research` templates in
`core/strategies/delegation-prompting.md` §14 if you have not this session.

## 1. Classify and pick the row

| The work | Routing row |
|---|---|
| Root cause, a bug not visible from the code, flaky or slow paths | `investigate` |
| Audit, decomposition, "how does X work", architecture critique | `analyze` |
| Log digging, large-document reading, no judgment calls | `bulk` |
| Docs, APIs, web facts | `research` |

Take the row's primary (fallback only if the primary is unavailable or
already failed this question). If it runs natively here, spawn a subagent
pinned to it, e.g. the `analyst` agent, instead of bridging. Otherwise
resolve its bridge id from the routing table ("Reach it via" / `## Bridges`)
or the profile's `access.invoke_via`, and read
`${CLAUDE_PLUGIN_ROOT}/core/bridges/<id>.md` in full. Use its **One-shot,
read-only** template. Note whether the callee has tools: API bridges
(`openai-api`, `openrouter-api`, `ollama`) are completions only, so they
cannot open files or run commands.

**Bridge not live:** say so, name the bridge and the reason, and offer the
`analyst` subagent on Sonnet as the fallback, labelled
`[sonnet] investigate <topic> (fallback)`.

## 2. Frame the question

Most of the value is here. The callee has none of your context.

- **One question**, stated as the decision it feeds: "Why does X happen,
  and where does it originate?" not "look into X".
- **Symptom and repro.** Exact steps, the command that shows it, expected vs
  actual, environment (branch, versions, env flags without values).
- **Pointers, not fences.** Log paths, run links, suspect files as context;
  let it search beyond them. For a tool-less callee, put the log excerpt or
  document text in the prompt (chunk it if it is large) instead of a path.
- **What you already ruled out**, so it does not repeat it.
- **Evidence required:** file:line for each claim, the commands it ran and
  their results, what it ruled out, and claims it could not confirm.
- **Bound and out:** "If you cannot find it after <N attempts | the
  timeout>, stop and report what you tried."

Sol/GPT dialect, short and literal:

```
In <repo path> on branch <b>: <symptom>. Repro: <steps/command>.
Expected <x>, got <y>. Logs: <path>. Already ruled out: <list>.
Find the root cause and reproduce it before claiming it. Do not edit files.
Report: root cause, file:line where it originates, evidence (commands run
and their output), what you ruled out, and anything UNCONFIRMED with why.
If you cannot find it after 3 attempts, stop and report what you tried.
If you find nothing, say so clearly and list exactly what you inspected.
```

## 3. Run it

Write the prompt to `<artifact dir>/investigate-<model>-prompt.md` (artifact
dir: session scratchpad, else `/tmp/agent-orchestration/`), output to
`investigate-<model>.md`, read-only flags, 20-minute timeout
(`sh ${CLAUDE_PLUGIN_ROOT}/core/bridges/_timeout.sh 1200 <cmd>`, exit 124 =
timeout). Run in the background (the Bash tool caps foreground at 10 minutes)
and keep working on the question yourself meanwhile. In a workflow or
fan-out, use the `bridge-runner` agent, named `[<model>] investigate <topic>`.
A timeout is **no result**; read any partial output before deciding to rerun.

## 4. Check the evidence

Before relaying, verify the load-bearing claims cheaply: open the cited
file:line, re-run the repro or the command it says proved the cause. Do not
redo the whole investigation. Mark each claim **confirmed**, **unconfirmed**,
or **contradicted**. If the root cause is contradicted, say so and decide
between the row's fallback model and asking the user; do not silently retry
the same model with the same prompt.

## 5. Present

```
[sol] Root cause of <symptom>: <one or two sentences>  (<confirmed | unconfirmed>)
Origin: file:line
Evidence: <command → result>, <file:line → what it shows>
Ruled out: <…>
Unconfirmed: <claim> (why)
Suggested next step: <fix via quick-fix / feature row | more data needed>
```

An empty result is a result: report it once with what was inspected, and do
not re-run. The investigator does not fix; route any fix through
`/agent-orchestration:orchestrate`.

## 6. Log

If `logging.enabled` in `~/.agent-orchestration/config.yaml`, append one JSON
line to `logging.path` (fields per `core/strategies/improvement-loop.md` §8:
`task_type`, `model`, `effort`, `harness`, `mechanism: "bridge:<id>"`,
`wall_clock_minutes`, `outcome: "info-only"`, `escalated_to`, `notes`). If a
command or flag was wrong, run `/agent-orchestration:lesson`.
