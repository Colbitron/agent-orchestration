---
name: ao-bridge-verify
description: Verify UI or runtime behaviour through a model that can drive a browser, desktop, or simulator (computer use), or say plainly that no such bridge is available. Use when the user asks to test a flow, verify UI behaviour, inspect a running app, capture screenshots, or confirm implemented behaviour that benefits from computer use.
---

# Bridge: verify (computer use)

Kit root: `KIT_ROOT`. Verification is part of the task, and the verifier
should be a different model from the one that wrote the code.

## 1. Find a path that actually exists

Check in this order and use the first that works:

1. **Inside T3 Code:** if a `delegate_task` tool from the `t3-code` MCP
   server is available, use it with `role: test` and a target that has
   computer use. This is the only documented way to reach computer use
   without a human.
2. **A live computer-use bridge:** the `computer-use` row of
   `~/.agent-orchestration/routing.md` names a bridge marked live. Read
   `KIT_ROOT/core/bridges/<id>.md` and use its command exactly. If the
   file is missing, say so; never compose CLI flags from memory.
3. **Nothing reachable:** say so plainly. Codex computer use runs only in
   the ChatGPT desktop app and has no documented CLI trigger. Do not
   pretend. Offer the user two options: paste the prompt below into a
   computer-use-capable app themselves, or fall back to scripted checks
   (the project's own end-to-end tests or a headless browser it already
   uses) run by you or `ao-bridge-implement`.

If no routing table exists, stop and run the `ao-setup` skill.

## 2. Write the prompt

Computer-use template
(`KIT_ROOT/core/strategies/delegation-prompting.md` §14):

```
On <machine | simulator | browser>, open <app/URL> and <flow>.
Expected: <behaviour per step>. Capture a screenshot at <named points>.
Don't <touch other apps | log in | submit payments>. Done means pass/fail
per step, the screenshots, and exact notes on any mismatch. If you can't
reach the app, stop and say what failed.
<If other lanes use the browser:> Create your own tab group and touch only
tabs you created.
```

Run it on a machine the user is not working on. For money or irreversible
actions the human makes the final click. Never put secrets in the prompt.
If more than one parallel lane uses the browser, each creates its own tab
group and touches only tabs it created, or the browser lanes run one at a
time (`KIT_ROOT/core/strategies/parallelism.md` §3 "Shared resources").

## 3. Run it

- Timeout: 30 minutes:
  `sh KIT_ROOT/core/bridges/_timeout.sh 1800 <cmd>`
  (exit 124 = timed out). Pipe the prompt in or redirect stdin from
  `/dev/null`; it must not be a terminal.
- Capture the report to `/tmp/agent-orchestration/verify-<model>.md`, and
  ask for screenshots in `/tmp/agent-orchestration/verify-<model>/`.

## 4. Handle the result

1. A timeout or an unreachable app is "not verified", never "passed".
2. Look at the screenshots yourself before reporting a pass.
3. Report per step: pass, fail, or not verified, with the bridge id prefix
   and the screenshot paths.
4. A failed step goes back to the implementer per the routing table.
