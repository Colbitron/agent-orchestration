<!-- agent-orchestration -->
## Agent orchestration

This machine uses the agent-orchestration kit.
Kit root: `KIT_ROOT`. User config: `~/.agent-orchestration/`.

**At the start of every session**, before planning or delegating any work,
read these files if they exist. This harness has no session hook loading
them for you, so this instruction is the loader. Skip it only if an
`<agent-orchestration>` block is already in your context.

1. `~/.agent-orchestration/routing.md`: the user's routing table, standing
   rules, and permissions
2. `~/.agent-orchestration/glossary.md`: what the user's words mean
3. `~/.agent-orchestration/lessons.md`: lessons from past delegations;
   they refine the table

**If `routing.md` does not exist**, do not assume which models,
subscriptions, or CLIs the user has. Offer to run the setup interview: use
the `ao-setup` skill, or follow `KIT_ROOT/core/interview/setup-interview.md`
step by step.

**Before delegating anything non-trivial** (a subagent, another CLI, another
model), use the `ao-orchestrate` skill, or read
`KIT_ROOT/core/strategies/delegation-prompting.md` and the other strategy
docs in `KIT_ROOT/core/strategies/`. To call a model in another harness,
use the `ao-bridge-*` skills; exact commands live in `KIT_ROOT/core/bridges/`.

**Standing rule:** the routing table is defaults, not limits. If a cheaper
model's output misses the bar, escalate to a smarter model without asking.
Judge the output, not the price tag.

When a delegation goes wrong, use the `ao-lesson` skill to record it.
<!-- /agent-orchestration -->
