# User config schema

The setup interview writes `~/.agent-orchestration/config.yaml`. Everything
in it is editable by hand. The routing generator reads it together with
`core/models/*.md` to produce `routing.md` and `glossary.md` in the same
directory.

The directory is harness-neutral on purpose. A user who runs both Claude Code
and Codex has one config and one routing table.

```
~/.agent-orchestration/
  config.yaml      what the user told the interview (this schema)
  routing.md       generated routing table and standing rules
  glossary.md      generated glossary (defaults + user overrides)
  runs.jsonl        optional: one line per delegated task, for tuning
                   (the canonical record in core/strategies/improvement-loop.md §8)
  lessons.md       appended by the improvement loop; never regenerated
```

## config.yaml

```yaml
version: 1
user:
  name: Ada                        # used only for prose in generated files
  updated: 2026-10-02              # set by the interview each run

# Which agent tools the user actually drives. The first `primary: true` entry
# is where the orchestrator normally lives; the rest are reachable through
# bridges.
harnesses:
  - id: claude-code                # claude-code | codex | cursor | gemini-cli |
    primary: true                  #   opencode | pi | grokbuild | t3-code |
                                   #   antigravity | openclaw | hermes
    cli: claude                    # binary name if installed, else null
  - id: codex
    primary: false
    cli: codex

# How the user pays for each vendor. `type` drives the cost score the
# generator assigns to that vendor's models. `both` (subscription and API key)
# is what lists bridges that need a key, openclaw-cli and hermes-cli, for
# Claude models: with `subscription` alone the generator leaves them out.
access:
  anthropic:
    type: subscription             # none | subscription | api | both
    plan: max-5x                   # pro | max-5x | max-20x | team | null
    notes: "Fable capped at 50% of weekly quota"
  openai:
    type: none
    plan: null                     # plus | pro | business | null
  google:
    type: none
  xai:
    type: none
  open_weights:
    type: none                     # none | api | local | both
    provider: null                 # openrouter | ollama | lmstudio | llama-cpp | zhipu | ...
    models: []                     # api ids or Ollama tags the user can reach; quote tags with colons ("qwen3.8:27b")

# The machine local models run on. Only read when a model runs locally.
# kind is vram for a dedicated GPU or unified for Apple silicon and similar;
# the generator allows 75% of unified memory to the GPU, all of VRAM.
hardware:
  memory_gb: 32
  kind: unified                  # vram | unified
  gpu: "Apple M2 Max"            # free text, or null
  notes: ""

# The setup interview fills this from access + profiles using the derivation
# rules below; the generator reads the numbers and does not recompute them.
# The user may override `enabled` or `cost` per model. `cost` is 1-10 where
# 10 means "effectively free for me" (Theo scored Codex 9 on a generous sub)
# and 1 means "every token hurts". `host` says where an open-weights model
# runs: `local` (checked against `hardware`) or `api` (hosted). It defaults
# to `local` when `access.open_weights.type` is `local` and the profile has a
# `local` block, otherwise `api`.
models:
  claude-fable-5-1:  {enabled: true,  cost: 3}
  claude-opus-5-5:   {enabled: true,  cost: 7}
  claude-sonnet-5-5: {enabled: true,  cost: 7}
  claude-haiku-5-5:  {enabled: true,  cost: 9}
  claude-haiku-4-5:  {enabled: false, cost: 9}   # superseded; keep disabled
  gpt-6-astra:       {enabled: false, cost: 1}
  gpt-6-1-sol:       {enabled: false, cost: 1}
  qwen3-8-27b:       {enabled: false, cost: 1, host: api}     # open weights; see the local-only example below
  gpt-oss-20b:       {enabled: false, cost: 1, host: api}

# What the user cares about when axes conflict. The generator turns this
# into the ordering rule in routing.md.
priorities:
  order: [intelligence, taste, cost]   # first wins ties; Theo's default
  frustration_tolerance: low           # low → prefer high-floor models
  budget_sensitivity: medium           # low | medium | high
  speed_matters: false                 # true → weight `speed` on narrow tasks
  speed_requires_review: false         # true → add the "Speed rule" to Standing
                                       #   rules: speed never skips review

# Autonomy is opt-in. Default is "propose". The interview explains each
# level before asking.
autonomy:
  level: propose                   # propose | merge-with-gates | goal-mode
  reviewer_bots: []                # e.g. [coderabbit, cursor-bugbot, macroscope]
  merge_gate: null                 # optional: what must hold before a merge, e.g.
                                   #   "ci-green + independent-model-review"
  may:
    create_worktrees: true
    open_prs: true
    merge_prs: false               # true only for merge-with-gates / goal-mode
    close_prs: false
    rebase: true
    force_push: false
    deploy: false                  # prod stays human unless explicitly true
  staging_is_safe: false           # true → agent may freely exercise staging
  may_notes:                       # optional: qualifier shown after a permission in "May:"
    force_push: "only its own branches, never main"

# Optional per-model effort overrides. Profiles carry the defaults.
effort:
  claude-opus-5-5: high

# Optional: replace the computed row for a task id from core/tasks.md. Every
# field is optional; a field left out keeps the computed value.
routing_overrides:
  babysit:
    primary: claude-sonnet-5-5     # an enabled model id; null, "" or none empties it
    fallback: claude-opus-5-5      # same rules as primary
    reason: "Cheaper quota for long polling loops"   # shown in the row's Why
    effort: medium                 # one of the primary's effort.levels; never max

# Things the orchestrator should know about how this user works. Free text,
# kept short. Rendered verbatim into routing.md.
preferences:
  stack: "TypeScript, SvelteKit, Postgres"
  style: "Small PRs. No new dependencies without asking."
  review_bots_note: ""
  machines: ""                     # e.g. "remote box 'leftbook' via tailscale"

# Optional: extra bullets appended verbatim, in order, to "Standing rules".
standing_rules:
  extra:
    - "Fable: `high`; one bounded `xhigh` pass only when `high` failed."

# Optional: one "- `<id>`: <note>" line per entry under "Bridges"; an entry
# replaces the auto-detected line for the same bridge id. A harness entry may
# also carry `smoke_tested: 2026-10-02`.
bridges:
  - {id: codex-cli, note: "smoke test passed 2026-10-02"}

# Glossary overrides. Keys replace the defaults from core/tasks.md in place;
# new keys are appended; a null value removes a default.
glossary:
  taste: "UI/UX, code quality, API design, copy. For me, also: no clever abstractions."

# Logging for the improvement loop.
logging:
  enabled: true
  path: ~/.agent-orchestration/runs.jsonl
```

### What the less obvious keys do

`generate.py` is the reference for these; the lines quoted are what it writes
into `routing.md`.

**`priorities.speed_requires_review`.** Only `true` has an effect. It adds this
bullet to "Standing rules", right after the priority order: "Speed rule: on
small tasks a faster or cheaper model may do the work only if a smarter model
with better taste reviews the result before it lands. Speed never skips
review." It does not change scoring; `speed_matters` does that.

**`autonomy.merge_gate`.** A free-text gate, written as the user said it. When
it is set:

- "Standing permissions" gets "Merge gate: `<merge_gate>`. Never merge without
  it." after the autonomy level line, at every level.
- If `may.merge_prs` is true, the level is not `propose`, and `may_notes` has
  no `merge_prs` entry, "May:" lists "merge PRs (only under the merge gate)".
- If `reviewer_bots` is empty, `may.merge_prs` is true and the level is not
  `propose`, the bots line reads "Reviewer bots that gate merges: none; the
  merge gate above stands in for them." instead of "none; merges stay human."

**`routing_overrides.<task>`.** Applied after scoring, row by row; the
`feature` override is applied before `review` is resolved, so the
cross-family rule sees the final implementer. Accepted fields are `primary`,
`fallback`, `reason` and `effort`. An overridden row's Why becomes "Config
override: <reason>." (or "Config override." with no reason), and the
profile note (with any guardrail), the "no model rates better" remark and
the `orchestrate` row's "session model" label are dropped. Without
`effort`, the row's effort comes from `config.effort` or the final primary's
profile default. With `primary` emptied, the row shows `none` as primary.

These are errors (exit 2, nothing written):

- `routing_overrides.<task>: no such task id in core/tasks.md`
- `routing_overrides.<task>.<primary|fallback>: no profile for <id>`
- `routing_overrides.<task>.<primary|fallback>: <id> is not enabled in config.models`
- `routing_overrides.<task>.effort is <value>; it must be one effort level as a string`
- `routing_overrides.<task>.effort is max; the kit never uses max effort`
- `routing_overrides.<task>.effort is <level> but <id> has no effort control (effort.levels is empty)`
- `routing_overrides.<task>.effort is <level>, not one of <id>'s levels: <levels>`
- `effort is max on rows <task>[, <task>...]; the kit never uses max` (the
  row-level check, raised alongside the `is max` message above)

The two level checks (no effort control, not one of the levels) run against
the row's final primary and are skipped when the override leaves no
primary. A non-string effort and `max` are errors with or without a primary.

## Derivation rules the interview applies when writing `models`

The setup and refresh skills apply these rules and write the results into
`models`. The generator itself checks only `enabled`, `cost`, `host` and the
hardware fit. It never reads prices; it reads `access.<vendor>.type` only to
label disabled models and `access.open_weights.type` to default `host`.

1. **Availability.** A model is `enabled` only if its vendor has `access.type`
   other than `none` and at least one harness in `harnesses` appears in the
   profile's `access.harnesses` or a bridge in `access.invoke_via` has its
   CLI installed. Open-weights models (`family: open-weights`, whatever the
   `vendor`) are gated on `access.open_weights`: `local` enables profiles
   with a `local` block whose smallest usable build fits `hardware`, `api`
   enables hosted ones, `both` enables either.
2. **Cost score.** Start from the profile's `cost_efficiency`. Then:
   - `access.type: subscription` with a generous plan (Codex Pro, Claude Max
     20x): +3, capped at 10.
   - `subscription` on a basic plan (Pro, Max 5x): +1.
   - `api`: 0 adjustment, and subtract 2 if the model's `pricing_per_mtok.output`
     is 50 or above.
   - Known quota rules (Fable's 50% cap) subtract 1.
   - `host: local`: 9. Nothing per token, but the hardware is shared with
     the user's foreground work, runs are slow, and electricity is not free;
     reserve 10 for a model that costs nothing at all.
   The user may override any value.
3. **Primary vs fallback per task.** See `routing-generator.md`.
4. **Cross-family review.** If another enabled family has a model that rates
   `ok` or better for review, the review row routes there. Otherwise route
   review to a different model in the implementer's family and add a note
   recommending a second family; a `poor` reviewer is called a smoke check.
5. **Autonomy.** Rendered as a "Standing permissions" block in routing.md.
   Nothing in `may` defaults to true except worktrees, PRs, and rebases.

## Validation

The interview re-reads the file after writing it and checks:

- every enabled model has a profile in `core/models/`
- every harness id is one the kit knows (`core/bridges/` has a matching
  bridge or the harness is `primary`)
- `autonomy.may.merge_prs` is false unless `autonomy.level` is not `propose`
- `priorities.order` contains exactly the three axes once each

If any check fails, it fixes the file and tells the user what it changed.

`generate.py` also warns, without failing, about any key this schema does not
list: at the top level and inside `user`, each `harnesses` and `bridges`
entry, `access` and each `access.<vendor>`, each `models.<id>`, `priorities`,
`autonomy`, `autonomy.may`, `autonomy.may_notes`, `routing_overrides.<task>`,
`preferences`, `standing_rules`, `logging` and `hardware`. A vendor under `access` is
known if it is listed above or is the `vendor` of a profile. Extra keys
under `autonomy.may` and `preferences` are still written into `routing.md`
as given; every other unknown key is ignored. It also warns when one of
those blocks, or a `routing_overrides.<task>` entry, is present but not a
mapping (for example `priorities is a string, expected a mapping; ignored`).
Add a new key here and to
`generate.py`'s key lists together.

## Example: a local-only user

No subscriptions, no API keys, a 32 GB Apple silicon Mac running Ollama,
OpenCode as the harness. The two open-weights profiles are enabled and the
generator checks each against `hardware`: Qwen3.8-27B fits at Q4 (about 18
GB of the roughly 24 GB the GPU may use) and gpt-oss-20b fits in its native
format. On a 16 GB machine the same config keeps gpt-oss-20b with some layers on
the CPU and runs Qwen3.8-27B only as its 2-bit build through llama.cpp;
both are below their recommended memory there, so every task fit counts one
step worse and a note says so.

```yaml
version: 1
user: {name: Sam, updated: 2026-10-19}
harnesses:
  - {id: opencode, primary: true, cli: opencode}
access:
  anthropic: {type: none}
  openai: {type: none}
  google: {type: none}
  xai: {type: none}
  open_weights:
    type: local
    provider: ollama
    models: ["qwen3.8:27b", "gpt-oss:20b"]
hardware: {memory_gb: 32, kind: unified, gpu: "Apple M2 Max"}
models:
  qwen3-8-27b: {enabled: true, cost: 9, host: local}
  gpt-oss-20b: {enabled: true, cost: 9, host: local}
priorities:
  order: [intelligence, taste, cost]
  frustration_tolerance: medium
  budget_sensitivity: low
  speed_matters: false
autonomy:
  level: propose           # no second family is available, so no model can gate another's merge
  reviewer_bots: []
bridges:
  - {id: ollama, note: "OLLAMA_CONTEXT_LENGTH=65536 for agent harnesses"}
logging: {enabled: true, path: ~/.agent-orchestration/runs.jsonl}
```

Two things the table will say that a local-only user should expect: review
is single-family (the implementer or its sibling reviews), so `propose` is
the honest autonomy level; and every speed figure is a third-party
measurement on someone else's machine until the user records their own.
