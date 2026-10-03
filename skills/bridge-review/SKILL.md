---
name: bridge-review
description: Get an independent code review from a different model family (usually GPT-6.1 Sol via Codex, or Grok, per the user's routing table) of uncommitted changes, a branch diff, a commit, or a PR, then verify its findings before presenting them. Use when the user asks for a second opinion, an independent or cross-family review, or says "have Sol/Codex/Grok look at this"; when the orchestrate skill's review row points at a bridged model; or before merging a change broad enough that another lab's perspective is useful. Read-only; the reviewer never edits files.
user-invocable: true
argument-hint: "[uncommitted | branch <name> | commit <sha> | pr <n>] [focus]"
---

# Bridge review

Cross-family review: the model that wrote the code does not review it. The
kit root is `${CLAUDE_PLUGIN_ROOT}`, also announced in the
`<agent-orchestration>` block at session start. Read
`${CLAUDE_PLUGIN_ROOT}/core/bridges/README.md` (common rules) and
`core/strategies/verification-and-review.md` §3 and §5 if you have not this
session.

## 1. Identify the review target

Pick exactly one, and write down the git command that shows it:

| Target | Show it with |
|---|---|
| Uncommitted changes | `git status --short` and `git diff HEAD` |
| Branch vs base | `git diff <base>...<branch>` (base: the PR base or `main`) |
| One commit | `git show <sha>` |
| A PR | `gh pr view <n> --json headRefName,baseRefName,title` then `gh pr diff <n>` |

If the diff is empty, stop and say so; there is nothing to review. For a PR
that is not checked out, add a worktree on its head
(`git worktree add <path> <headRef>`) so the reviewer can run the code.

## 2. Pick the bridge

1. Read the `review` row of the routing table. Take the primary model; use
   the fallback only if the primary is unavailable or already failed this
   review.
2. If that model runs natively in this harness, do not bridge: spawn a
   subagent pinned to it instead.
3. Otherwise find its bridge id in the routing table's "Reach it via"
   column or `## Bridges` section (or the profile's `access.invoke_via` in
   `core/models/<id>.md`), then read `${CLAUDE_PLUGIN_ROOT}/core/bridges/<id>.md`
   in full. Use its **One-shot, read-only** template, its flags table, and
   its prompting section. Never type a bridge command from memory.
4. If the bridge is not marked smoke-tested in `## Bridges`, run its
   **Detect** snippet first.

**Bridge not live** (no routing table, detect fails, no access): say so
plainly, naming the bridge and why. Then offer the single-family fallback:
the `analyst` subagent on Sonnet with the same prompt, named
`[sonnet] review <target> (single-family fallback)`. If the user asked for a
specific model, ask before substituting; if the orchestrate skill sent you
here, run the fallback and label it. Never present a Claude review as Sol's.

## 3. Build the prompt

Start from the `review` template in `core/strategies/delegation-prompting.md`
§14, in the callee's dialect from the bridge file. GPT and Grok want it short
and literal. It must be self-contained:

```
Review the changes in <repo path>. Run `<git command from step 1>` to see them.
Focus: correctness, regressions, edge cases, security<, plus user focus>.
Do not edit files. Run the tests or code where that confirms a finding.
For each finding give file:line, what is wrong, how you confirmed it, and
severity (high/medium/low). Mark any finding you could not confirm as
UNCONFIRMED and say why.
If you find nothing, say so clearly and list exactly what you inspected.
```

Add context the reviewer cannot discover itself (what the change is for,
known non-goals). Never paste secrets.

## 4. Run it

- Write the prompt to `<artifact dir>/review-<model>-prompt.md`; artifact dir
  is the session scratchpad, else `/tmp/agent-orchestration/`. Pass it the
  way the bridge file says (stdin or `"$(cat …)"`) so quoting cannot break.
- Output goes to `<artifact dir>/review-<model>.md`.
- Wrap the command in the 20-minute timeout from the bridges README rule 4.
  Claude Code's Bash tool caps foreground commands at 10 minutes, so run it
  in the background and keep working; you are notified when it exits.
- Inside a workflow or fan-out, give this step to the `bridge-runner` agent
  instead, named `[<model>] review <target>`.
- Exit by timeout (142 from the perl wrapper, 124 from `gtimeout`) means **no
  result**, not "nothing found". Check the output file for partial text.

## 5. Verify, then present

Read the report file. For each important claim, open the cited file:line
and, where cheap, run the test or command that would confirm it. Classify:
**confirmed**, **unconfirmed** (plausible, not checkable here), or
**contradicted** (drop it, but count it). Do not redo the reviewer's whole
analysis; check facts.

Present, prefixed with the model so the user sees who said what:

```
[sol] Review of <target> (<N> findings confirmed, <M> unconfirmed, <K> dropped)
Confirmed: <severity> file:line: problem (how confirmed)
Unconfirmed: file:line: claim (why it could not be checked)
Inspected, nothing found: <reviewer's list>
```

An empty review is a result: report it once with what was inspected, and do
not re-run. Do not fix anything unless the user asks; if they do, route the
fix through `/agent-orchestration:orchestrate`.

## 6. Log

If `logging.enabled` in `~/.agent-orchestration/config.yaml`, append one line
to `logging.path` (default `~/.agent-orchestration/runs.jsonl`), fields per
`core/strategies/improvement-loop.md` §8:

```
{"date":"<YYYY-MM-DD>","repo":"<name>","task_type":"review","model":"<id>","effort":"<e>","harness":"<callee harness>","mechanism":"bridge:<id>","delegated_by":"<you>","wall_clock_minutes":<n>,"outcome":"info-only","reviewer_findings":{"confirmed":<n>,"unconfirmed":<n>,"contradicted":<n>},"notes":""}
```

If a command or flag was wrong, run `/agent-orchestration:lesson` so the fix
lands in the bridge file.
