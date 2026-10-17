# agent-orchestration

A portable kit for routing work across AI models and orchestrating coding
agents, inspired by Theo's (t3.gg) orchestration setup (see Origins below). It replaces a hand-tuned
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

No SSH key registered with GitHub? Add `export CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`
to your shell profile first. For `Colbitron/agent-orchestration` Claude Code
tries SSH before HTTPS. `claude plugin install` in the shell can fall back
to HTTPS by itself, but installs from `/plugin` inside a session and every
plugin update do not, so without the variable they fail. Over HTTPS a
private repository also needs a stored GitHub credential: `gh auth login`,
then `gh auth setup-git`.

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

The kit has no version number. Every push to `main` is a release, and your
installed copy is tied to the commit it came from.

Claude Code does not auto-update third-party marketplaces unless you turn it
on. To have new commits arrive in the background, turn it on once: in a
session, open `/plugin`, go to **Marketplaces**, select `agent-orchestration`,
and select **Enable auto-update**. Claude Code then checks after a random
delay of up to ten minutes following your first message in a session; an
update it finds loads after `/reload-plugins` or at the next start.

To update by hand instead:

```bash
claude plugin marketplace update agent-orchestration
claude plugin update agent-orchestration@agent-orchestration
```

Inside a session, `/plugin marketplace update agent-orchestration` does the
same. Restart Claude Code, then run `/agent-orchestration:refresh` so your
routing table picks up changed model profiles. The session-start status block tells
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

- New model: follow [docs/MAINTAINING.md](docs/MAINTAINING.md), then commit
  and push to `main`. That push is the release; there is no version to bump.
- New harness: add `core/bridges/<id>.md` and `adapters/<id>/`.
- Routing felt wrong: edit `~/.agent-orchestration/config.yaml`, not the
  generated `routing.md`, then run `/agent-orchestration:refresh` (not setup).

Layout and rationale: `docs/ARCHITECTURE.md`.

## Origins

The idea comes from Theo (t3.gg) and his videos on routing work across
models and running agents in parallel. What this kit takes from him:

- Route by task shape, not by a single "best" model: judge models on
  intelligence, taste, floor (how rarely they do something dumb), and how
  wide the task is, and pick per task type.
- Delegate with a stated goal, a checkable done state, and an explicit point
  at which the agent may stop and ask.
- Subagents for bounded pieces, workflows for fan-out-and-verify, worktrees
  for parallel implementations, and a session that orchestrates
  checkpoint-driven work itself.
- Review by a different model family than the one that wrote the code.
- Keep a glossary and a lessons file, and change the config when an agent
  misbehaves instead of re-prompting.

What was added here: the setup interview and the generated per-user routing
table, the scored model profiles and their schema, the bridge files and
bridge skills for calling other harnesses from the shell, the session-start
hook, the adapters for non-Claude harnesses, the refresh path, and the
improvement loop that turns a lesson into a config change.

The videos, all on Theo's channel (https://www.youtube.com/@t3dotgg). The
strategy docs and model profiles cite them by key and timestamp
(`[KEY m:ss]` links to the video at that point). Captions mishear model
names; the correction tables are in `research/`.

| Key | Video |
|---|---|
| INSP | [A proper guide to Fable 5](https://youtu.be/8GRmLR__OGQ) (orchestration setup) |
| MODELS | [Please stop using stupid models](https://youtu.be/iBrAWpjXNxs) |
| FVA | [Fable Vs Astra Debate Is Over](https://youtu.be/P7bxbDSnZRM) |
| FAB51 | [My New Favorite Model](https://youtu.be/r_dw-1109Ag) (Fable 5.1) |
| OPUS55 | [My new favorite model.](https://youtu.be/jgGyX7MPPVg) (Opus 5.5) |
| SON55 | [OpenAI should be scared of this one](https://youtu.be/8WbW_n95wc4) (Sonnet 5.5) |
| H55 | [finally a good small model](https://youtu.be/38_6C0dkKmU) (Haiku 5.5) |
| OPUSG | [Getting the most out of Opus 5.5](https://youtu.be/ejjBbaq9RmY) |
| FABG | [So I was using Fable wrong...](https://youtu.be/-XWSJM-Ue-o) |
| ASTRA | [It's Here.](https://youtu.be/XFWpf0wLbh0) (GPT-6 Astra) |
| SOL61 | [OpenAI fights back](https://youtu.be/vu8X3YroB-w) (GPT-6.1 Sol) |

Harness facts in `research/harnesses.md` and the gap-model profiles come from
vendor docs and public benchmark sites, linked inline.

## License

MIT. See `LICENSE`.
