---
name: bridge-verify
description: Verify implemented behaviour at runtime (test a flow, verify UI behaviour, inspect a running app, capture screenshots, drive a simulator) through the computer-use route in the user's routing table, falling back honestly when no computer-use route is reachable. Use when the user asks to test or verify a flow or UI, check that a change works in the running app, or capture screenshots, and before declaring any frontend or user-facing feature done. Never reports UI verification that did not actually happen.
user-invocable: true
argument-hint: "<flow or behaviour to verify> [url | app | simulator]"
---

# Bridge verify

The kit root is `${CLAUDE_PLUGIN_ROOT}`, also announced in the
`<agent-orchestration>` block at session start. Read
`core/strategies/verification-and-review.md` §11 and the `computer-use`
template in `core/strategies/delegation-prompting.md` §14 if you have not
this session.

## What is and is not possible (research as of 2026-10)

Codex computer use, the strongest route in the research, runs **only in the
ChatGPT desktop app** (Codex mode). It has no documented `codex exec` or CLI
trigger, so no shell bridge can reach it. Do not try to make one up. If
`${CLAUDE_PLUGIN_ROOT}/core/bridges/codex-cli.md` later documents a
**verified** computer-use path, follow it; otherwise treat Codex computer use
as unavailable from here.

## 1. Write the test plan first

Before choosing a route, write down: how to start the app (command, port,
simulator), the flow as numbered steps, the expected result per step,
screenshot points, and negatives (don't log in to real accounts, don't
submit payments, don't touch other apps). This is the `computer-use`
template; every route below uses it.

## 2. Pick the route, in this order

Read the routing table's `computer-use` row first; it names the model the
user prefers. Then take the first route that is actually reachable:

1. **Inside T3 Code** (tools named `mcp__t3-code__*` are present): read
   `${CLAUDE_PLUGIN_ROOT}/core/bridges/t3-code-mcp.md`. Call
   `orchestrator_capabilities`, pick a provider that matches the routing row
   and supports computer use or browser use, then `delegate_task` with
   `role: test`, a self-contained prompt built from the test plan, and the
   timeout and mode the bridge file gives (30 minutes by default). Whether a
   provider's computer-use tools work inside a T3 child thread is not
   guaranteed; trust only the artifacts it returns.
2. **Browser or computer-use tools in this harness**: Claude in Chrome
   (`mcp__claude-in-chrome__*`), the desktop app's built-in browser, desktop
   computer use, or a Playwright MCP. If the harness has a skill for that
   tool, load it first, then drive the flow yourself. Work in a new tab, and
   ask before driving the desktop the user is actively using. If other
   subagents use the browser in parallel, each creates its own tab group and
   touches only tabs it created, or the browser lanes run one at a time
   (`core/strategies/parallelism.md` §3 "Shared resources").
3. **Programmatic fallback**: start the app and check behaviour without a
   screen: `curl` the endpoints, run the project's e2e or integration tests
   (a headless Playwright/Cypress script if the project already has one),
   read server and console logs, and for iOS use `xcrun simctl` to boot,
   install, launch, and `io booted screenshot`. This proves responses and
   rendering, not interaction or visual correctness.

If the user specifically wants Codex computer use, offer the test plan as a
ready-to-paste prompt for the ChatGPT desktop app, and say that is the only
way to reach it.

## 3. Run and capture

- Save screenshots, recordings, and logs under `<artifact dir>/verify-<slug>/`
  (artifact dir: session scratchpad, else `/tmp/agent-orchestration/`).
- One pass per step: action, expected, observed, pass/fail, artifact path.
- If the app will not start or the route cannot reach it, stop and report
  what failed. Do not substitute guesses about what the UI "should" show.
- Money and irreversible actions: stop before the final click; the human
  makes it.

## 4. Report honestly

State the route used in the first line. Never write "verified the UI" unless
a screenshot, recording, or driven session exists for it.

```
[<model or "claude">] Verify <flow> via <t3-code-mcp → provider | claude-in-chrome | programmatic fallback>
1. <step>: PASS | FAIL | NOT VERIFIED  (<observed>; <artifact path>)
...
Not verified: <what this route could not check, e.g. layout, animations, touch>
Mismatches: <exact differences from expected>
```

With the programmatic fallback, the "Not verified" line must name every
visual or interaction check that did not happen, and the summary must say
"no UI verification was performed". Do not mark a frontend task done on a
fallback alone without telling the user what remains unchecked.

## 5. Log

If `logging.enabled` in `~/.agent-orchestration/config.yaml`, append one JSON
line to `logging.path`: the canonical record in
`core/strategies/improvement-loop.md` §8, with `row: "computer-use"`,
`model` as the profile id (the `core/models/` file name, never a short
name), `mechanism` set to the route used, and `harness` and any fallback
in `notes`. If a route failed for a fixable reason, run
`/agent-orchestration:lesson`.
