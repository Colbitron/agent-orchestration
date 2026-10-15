# agent-orchestration

A portable kit for routing work across AI models and orchestrating coding
agents, inspired by Theo's (T3) orchestration setup. It replaces a hand-tuned
personal CLAUDE.md with:

- **Model profiles** (`core/models/`): one file per model, scored on floor,
  taste, thoroughness, cost, and more, with prompting notes and routing
  guidance drawn from the research in `research/`.
- **A setup interview** (`core/interview/`): asks about your harnesses,
  subscriptions, priorities, and autonomy comfort, then generates *your*
  routing table. No table exists until you have answered.
- **Strategy docs** (`core/strategies/`): how to write delegated prompts,
  pick effort levels, parallelise, verify, think about cost, and improve the
  config over time.
- **Bridges** (`core/bridges/`): how to call another model from the shell
  one-shot (Codex CLI, Claude CLI, Gemini CLI, OpenCode, …).
- **Adapters**: the repo root is a Claude Code plugin; `adapters/` holds
  the equivalents for other harnesses.

## Install (Claude Code)

```bash
claude plugin marketplace add Colbitron/agent-orchestration
claude plugin install agent-orchestration@agent-orchestration
```

Then, in any session:

```
/agent-orchestration:setup
```

Answer the interview. The plugin loads your generated routing table at the
start of every session after that.

## Install (other harnesses)

See `adapters/<harness>/README.md`. The setup interview itself is plain
markdown, so any capable agent can run it: point it at
`core/interview/setup-interview.md`.

## Updating

Claude Code:

```bash
claude plugin marketplace update agent-orchestration
claude plugin update agent-orchestration@agent-orchestration
```

Restart Claude Code, then run `/agent-orchestration:refresh` so your routing
table picks up changed model profiles. The session-start status block tells
you when a refresh is needed.

Other harnesses, from an up-to-date checkout of this repo:

```sh
sh adapters/install.sh <harness> --update
```

It overwrites only the skill files you have not edited and replaces the
marked block in your instructions file; see `adapters/README.md`.

## Daily use

- `/agent-orchestration:orchestrate` reminds the agent how to delegate using
  your table (it also triggers on its own before non-trivial delegation).
- `/agent-orchestration:bridge-*` skills call other models for review,
  bounded implementation, investigation, or computer use.
- `/agent-orchestration:lesson` records what went wrong and turns it into a
  durable config change.

## Maintaining

- New model: follow [docs/MAINTAINING.md](docs/MAINTAINING.md), then bump
  `version` in `.claude-plugin/plugin.json`, commit, and push, so
  `claude plugin update` picks it up.
- New harness: add `core/bridges/<id>.md` and `adapters/<id>/`.
- Routing felt wrong: edit `~/.agent-orchestration/config.yaml`, not the
  generated `routing.md`, then run `/agent-orchestration:refresh` (not setup).

Layout and rationale: `docs/ARCHITECTURE.md`.
