# Architecture

A portable kit for orchestrating coding agents across models and harnesses. It
recreates the system from Theo's orchestration video (a scored model roster, a
glossary, task-type routing rules, and bridge skills that let one agent call
another from the shell) and makes it transferable to other people and other
tools.

## Design goals

1. **One source of truth.** Model knowledge, orchestration strategy, and the
   setup interview live in `core/` as plain markdown. Nothing harness-specific
   lives there.
2. **Per-user, not per-repo.** Each user runs a setup interview that writes a
   config describing *their* environment and preferences. The routing table is
   generated from that config plus the model profiles. No routing table exists
   until the interview has run.
3. **Thin adapters.** Each harness (Claude Code, Codex, Cursor, OpenCode, Pi,
   Gemini CLI, …) gets an adapter under `adapters/` that renders the core into
   that harness's native format. Adapters contain glue, not knowledge.
4. **Maintainable by one person.** A new model means adding one profile
   file. The generator (`core/interview/generate.py`) rebuilds each user's
   table from their `config.yaml` plus the profiles and records what it read
   in a stamp. The session-start hook compares the stamp to the kit and
   flags a stale table, and refresh regenerates it without re-running the
   interview. A new harness means adding one adapter.
5. **Editable by hand.** Everything the interview generates is readable
   markdown or YAML that the user can tweak, and the improvement loop ("how do
   we prevent this next time?") appends to it over time.

## Layout

```
.claude-plugin/      plugin.json + marketplace.json: the repo root IS the
                     Claude Code plugin, so core/ ships with it
skills/              Claude Code skills: setup, refresh, orchestrate, lesson,
                     bridge-*
agents/              Claude Code subagent definitions with pinned models
hooks/               SessionStart hook that injects the user's routing table
                     and flags it when routing.stamp is stale
core/
  models/            one profile per model, YAML frontmatter + markdown body
    _schema.md       the profile schema and scoring rubric (read first)
  tasks.md           canonical task taxonomy used by profiles and routing
  strategies/        tool-agnostic orchestration guidance
  bridges/           how to invoke each harness/model from a shell, one-shot
  interview/         the setup interview, config schema, routing generator
                     spec (routing-generator.md) and the script that
                     implements it (generate.py)
adapters/
  _shared/           harness-neutral ao-* skills (ao-setup, ao-refresh, ...)
                     and the AGENTS.md fragment
  codex/             AGENTS.md fragment + skills for Codex CLI
  ...                further harnesses
research/            digests of the source videos and web research (evidence)
docs/                this file and other design notes
```

The Claude Code adapter is the repo root rather than a subdirectory because
a plugin only ships its own directory: putting the plugin at the root is the
only way the skills can read `core/` after installation without copying it.

## Data flow

```
                    setup interview (writes or updates config.yaml)
                               │
                               ▼
core/models/*.md  +  ~/.agent-orchestration/config.yaml
        │                      │
        └──────────┬───────────┘
                   ▼
  core/interview/generate.py       (spec: core/interview/routing-generator.md)
  run by refresh (no interview) or at the end of setup
                   │
                   ▼
  ~/.agent-orchestration/routing.md     ← the user's routing table and
                                           standing rules
  ~/.agent-orchestration/glossary.md    ← what the user's words mean
  ~/.agent-orchestration/routing.stamp  ← kit version, commit, tasks hash,
                   │                       and every profile's as_of
                   ▼
  adapters load these each session (Claude Code: plugin hook or CLAUDE.md
  import; Codex: AGENTS.md import; others: their equivalent). The hook
  (elsewhere, the AGENTS.md fragment) compares routing.stamp to the kit's
  profiles and names any changed or new ones, with "Run
  /agent-orchestration:refresh to regenerate."
```

Two paths lead to the generator. **Setup** is the interview: it writes
`config.yaml` from the user's answers, then runs the script. **Refresh**
is the non-interactive path: it keeps the user's answers, asks once about
any profiles the config does not list yet, adds only the `models` lines
the user accepts, then runs the script. Both preview with `--diff` before
`--write` when a table already exists. Neither touches `lessons.md`.
If the script cannot run (no YAML parser), the agent follows
`routing-generator.md` by hand, and no stamp is written.

The config directory is deliberately harness-neutral (`~/.agent-orchestration/`)
so a user on two harnesses shares one routing table.

## Scoring model

Profiles score each model on a small set of axes (1–10). The two that Theo
used, `intelligence` and `taste`, are kept with his definitions, and a few
more are added because the later videos showed they decide routing:

| Axis | Meaning |
|---|---|
| `intelligence` | How hard a problem the model can handle unsupervised. |
| `taste` | Quality of UI/UX, code style, API design, and copy. |
| `floor` | Consistency. How rarely it does something dumb over a long run. High floor beats high ceiling for wide tasks. |
| `thoroughness` | How exhaustively it digs when reviewing or auditing. Noisy reviewers score high here and may score low on precision. |
| `cost_efficiency` | Cost per *completed task*, counting steps, retries, and cache economics, not list price per token. |
| `speed` | Wall-clock to completion on typical tasks. |
| `computer_use` | Driving a browser or desktop to verify or operate software. |
| `orchestration` | Running subagents, swarms, and long multi-phase plans as the lead. |

Scores are **defaults, not limits**. Standing rule in every generated routing
table: if a cheaper model's output misses the bar, rerun with a smarter model
without asking. Judge the output, not the price tag.

Cost is an input to the user's config, not a fixed score: the same model is
"effectively free" on a generous subscription and expensive on API billing.
The interview captures which access each user has and the generator adjusts.

## Routing principles carried from the research

- Route by **task type and context**, never by a context-free classifier
  picking the cheapest model. The OpenRouter cost-router test in the Sol video
  took 104 steps and cost more than a capable model at 19 steps.
- **Wide tasks need high floors.** Failure compounds over run time: a 5% vs 3%
  per-10-minute failure rate is roughly 30% vs 50% success at four hours.
- **Cross-family review.** Have a different lab's model review the code the
  implementer wrote. Claude writes, OpenAI/Grok reviews, and vice versa.
- **Cheap models gather information, expensive models ship.** Use cheaper or
  subscription-subsidised models to explore and verify, then move the work
  that has to land to the model with the highest floor and taste.
- **Never `max` effort** on any current model. `high` is the default almost
  everywhere; see `core/strategies/effort-levels.md`.
- **Every delegated prompt states what you want, what "done" means, and when
  to stop and ask.** See `core/strategies/delegation-prompting.md`.
- **Autonomy is opt-in.** The default posture is "propose PRs, never merge".
  Goal mode with auto-merge behind reviewer bots is enabled only by the user
  in their config.

## What the adapters must provide

Each adapter must be able to:

1. Load the user's generated `routing.md` and `glossary.md` into context at
   session start.
2. Expose the setup interview and refresh as user-invocable commands.
3. Expose the bridge skills (call model X for review / implementation /
   computer use / investigation) in the harness's skill format.
4. Expose subagent definitions where the harness supports them, with the
   model pinned per the routing table.

Harness-specific details are documented in `research/harnesses.md` and in each
adapter's README.
