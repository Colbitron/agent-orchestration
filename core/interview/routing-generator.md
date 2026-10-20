# Routing generator

How an agent turns `config.yaml` plus `core/models/*.md` into
`~/.agent-orchestration/routing.md` and `glossary.md`. This is a procedure,
not a program; the agent running setup follows it by hand. Keep it
deterministic enough that two runs on the same inputs give the same table.

## Inputs

- `config.yaml` (see `config-schema.md`)
- every `core/models/*.md` whose `id` is enabled in `config.models`
- `core/tasks.md` for the task list and glossary defaults
- `config.hardware`, for enabled models with `host: local`: the largest
  build in the profile's `local.memory_gb_by_quant` that fits (75% of
  unified memory, all of VRAM) and is at least `local.min_memory_gb` is the
  one the table assumes; a model with no fitting build is disabled with a
  note under the models table, and one running on a machine with less
  usable memory than `local.recommended_memory_gb` has every task fit
  degraded one step. A profile with `local.cpu_offload: true` counts the
  whole of a unified-memory machine when deciding whether it fits, while
  the GPU's share still decides the penalty. A local model that is slow
  (`speed` 3 or below) or running below its recommended memory does not
  auto-win the bulk row when another cheap model without those marks is
  enabled. The review row routes to another family only when a model there
  rates `ok` or better for review; otherwise it stays single-family and the
  standing rules say so.

## Step 1: score each (task, model) pair

For each task id in `core/tasks.md` and each enabled model:

1. Read `tasks.<id>.fit` from the profile. `poor` or `unknown` is excluded
   unless no other model is available for the task.
2. Compute a task score from the profile's `scores` using the task's
   weighting:

   | Task kind | Weighted axes |
   |---|---|
   | must-land, wide (`feature`, `long-run`, `orchestrate`, `babysit`) | floor ×2, intelligence, taste |
   | must-land, narrow (`quick-fix`, `copy`, `frontend`) | taste ×2, floor, speed if `priorities.speed_matters` |
   | information (`review`, `investigate`, `analyze`, `research`) | thoroughness ×2, intelligence, cost |
   | mechanical (`bulk`) | cost ×2, floor, speed |
   | `computer-use` | computer_use ×3 |
   | `3d-games` | intelligence, taste (profile notes split visuals vs feel) |
   | `prompt-writing` | intelligence, thoroughness |

   Use the user's per-model `cost` from config wherever "cost" appears, not
   the profile's `cost_efficiency`.
3. Apply `priorities.order` as the tiebreak sequence when scores are within
   one point.
4. If `priorities.frustration_tolerance` is `low`, add 1 to the weight of
   `floor` in every row's weighting (a row that does not weight floor gets
   floor ×1). If `budget_sensitivity` is `high`, do the same for cost.
   Adding 1 to every model's score instead would change nothing.

## Step 2: pick primary and fallback

- **Primary**: highest-scoring model with `fit: best`; if none, `good`; if
  none, `ok` with a guardrail note copied from the profile.
- **Fallback**: next model, preferring a different family if one is enabled.
- **Effort**: the primary profile's `effort.default`, unless `config.effort`
  overrides it. A configured effort must be one level from that model's
  `effort.levels`, written as a string.
- **Overrides**: `config.routing_overrides.<task>` (primary, fallback, reason,
  optional effort; each field optional) replaces those parts of the computed
  row, and the row's Why becomes "Config override: <reason>." A configured
  effort is checked against the row's final primary. Apply the `feature`
  override before resolving `review`, so the review rule sees the final
  implementer. See `config-schema.md` for the exact rules and errors.
- **Why**: one sentence built from the profile's task note and the axis that
  decided it. Cite nothing; the user can read the profile.

Special rules:

- **Expensive models are reserved for wide work.** A model whose user
  `cost` is 4 or lower may win only rows whose width in `core/tasks.md` is
  `wide` or `very wide` (and `frontend`, where taste dominates). On every
  other row the next candidate wins and the expensive model becomes the
  fallback. This keeps a quota-capped model like Fable for the tasks that
  need its floor instead of burning it on quick fixes and polling.
- `review`: primary must be from a family other than the family most used
  for `feature`, and must rate `ok` or better for review; a `poor` or
  `unknown` reviewer is no gate. If no other family has such a model, pick
  the model with the highest `thoroughness` that is not the `feature`
  primary and add the line "Single-family setup: a second vendor's reviewer
  would catch more." (plus "it rates poor for review, so treat its pass as
  a smoke check, not a gate" when that is so). If only the feature primary
  qualifies, say "No other enabled model rates ok or better for review, so
  the implementer reviews its own work"; if only one model is enabled, say
  "Only one model enabled; the implementer reviews its own work. Add a
  second model for a real gate." Warn when the final review and feature
  primaries share a family while another family is enabled. The "Review:"
  standing rule follows the row: cross-family only when the review and
  feature primaries differ in family.
- `computer-use`: if no enabled model has `computer_use` ≥ 6, write
  "No capable computer-use model enabled; verify by running tests and
  reading logs instead" and leave the row's primary empty.
- `orchestrate`: this is the model the user is sitting in front of unless
  the primary harness can switch models. Say so in the row. With only one
  model available in the primary harness, just name it as the session model.
- `bulk`: if a model has user `cost` ≥ 8, it wins the row regardless of
  score as long as its fit is at least `ok`, because bulk work should burn
  the cheapest capable quota. Theo's rule. A local model that is slow
  (`speed` ≤ 3) or below its recommended memory is passed over when another
  qualifying model is enabled.

## Step 3: write routing.md

Use exactly this structure. The orchestrator reads it every session, so keep
it under about 150 lines; nuance lives in the profiles.

```markdown
# Routing table for <user.name>
Generated <date> from config.yaml. Edit config.yaml and re-run setup rather
than editing this file; lessons go in lessons.md.

## Models available to me
| Model | Family | Reach it via | Effort | My cost (10 = free) | Floor | Taste | Thorough |
|---|---|---|---|---|---|---|---|
(one row per enabled model, from profile scores and config cost; Reach it
 via leaves out a bridge, or a primary harness driven by one, whose
 `api_key_only` names the model's vendor while access.<vendor>.type is
 `subscription`, and one note under the table says so)

## Routing table
| Task | Primary | Fallback | Effort | Why |
|---|---|---|---|---|
(one row per task id, in the order of core/tasks.md)

## Standing rules
- These are defaults, not limits. If a cheaper model's output doesn't meet
  the bar, rerun or redo with a smarter model without asking. Judge the
  output, not the price tag. Escalating costs less than shipping mediocre
  work.
- Use cheaper models to gather information and try things; move the work
  that has to land to the model with the highest floor and taste.
- Priority order when axes conflict: <priorities.order>.
- Speed rule: on small tasks a faster or cheaper model may do the work only
  if a smarter model with better taste reviews the result before it lands.
  Speed never skips review. (Only if `priorities.speed_requires_review` is
  true.)
- Never use `max` effort on any model. <effort notes from profiles>.
- Every delegated prompt states what you want, what "done" means, and when
  to stop and ask. See delegation-prompting.
- Review: <cross-family rule as resolved>.
- Prefix every subagent or workflow stage name with the model it runs on
  (e.g. `[sol] review-auth`) so the human can see who did what.
- If a bridged model returns nothing, it must say so and name what it
  inspected; do not re-run on an empty result.
- Log each delegated task to <logging.path> if logging is enabled, as one
  canonical record (core/strategies/improvement-loop.md §8). `model` is
  the profile id, the core/models/ file name (<feature primary's id> for
  <its short name>), never the short name in this table.

## Standing permissions (autonomy: <level>)
- <one line describing the level>
- Merge gate: `<autonomy.merge_gate>`. Never merge without it. (Only if
  `autonomy.merge_gate` is set.)
- May: <list from autonomy.may where true; merge PRs carries "(only under
  the merge gate)" when a gate is set and may_notes has no merge_prs entry>
- May never: <list where false>, deploy to production, or act outside the
  repository without asking.
- Reviewer bots that gate merges: <list, or "none; the merge gate above
  stands in for them" when merging is allowed under a gate, or "none;
  merges stay human">.
- Staging: <safe to exercise / treat as shared>.

## How I work
<preferences.stack, style, machines, review_bots_note, verbatim>

## Bridges
(one line per enabled non-primary harness: bridge id, smoke-tested yes/no,
 and the skill or command that wraps it)
```

## Step 4: write glossary.md

Start from the glossary in `core/tasks.md`. Replace any key present in
`config.glossary`. Append user-added terms. Keep each definition to one or
two lines.

## Step 5: validate

- Every task id has a row.
- Every primary and fallback is an enabled model.
- No row's effort is `max`, and every configured effort is a level the
  model offers.
- `tasks.md` has one task table (header row starting `| id |`) with no
  duplicate ids.
- The file is under about 150 lines. If not, shorten the "Why" column; do
  not drop rows.

## Regeneration

Setup regenerates `routing.md` and `glossary.md` from scratch each run.
`lessons.md` is never touched by the generator. If the user hand-edits
routing.md, the next run will overwrite it, so setup diffs the old and new
file and shows the user anything that would be lost before writing.

## Reference implementation

`core/interview/generate.py` implements steps 1 to 5. It needs Python 3.9+
(standard library only) and a YAML parser: pyyaml if importable, otherwise
`ruby` (the macOS system ruby works). With neither, it exits 2 with
"install pyyaml (pip install pyyaml) or ruby".

```bash
python3 "$KIT_ROOT/core/interview/generate.py" [--check | --diff | --write] [--json]
```

- `--kit-root PATH`: the kit (default: two directories above the script).
- `--config PATH`: default `$AGENT_ORCHESTRATION_HOME/config.yaml`, else
  `~/.agent-orchestration/config.yaml`.
- `--out DIR`: where the files go (default: the config's directory).
- `--check`: writes nothing; exit 0 if `routing.md` and `glossary.md` match
  what would be generated (ignoring the `Generated` line) and the stamp
  matches the current profiles, `tasks.md`, the kit commit and
  `config.user.updated`; exit 1 if anything is stale or differs.
- `--diff` (the default): prints a unified diff of what `--write` would
  change in `routing.md` and `glossary.md`. Writes nothing.
- `--write`: writes `routing.md`, `glossary.md` and `routing.stamp`. It
  never touches `lessons.md`, `runs.jsonl` or `config.yaml`.
- `--json`: prints `{"up_to_date", "changed_profiles", "new_profiles",
  "unconfigured_profiles", "rows_changed", "errors"}` (plus `warnings`)
  instead of text. With `--write` it describes the state before writing.

Optional config fields (see `config-schema.md`) carry hand-written text
through regeneration: `autonomy.may_notes` (a qualifier after a permission
in the "May:" line), `standing_rules.extra` (bullets appended to Standing
rules), `bridges` (a list of `{id, note}`, one Bridges line each, replacing the
auto-detected line for that bridge id) and `harnesses[].smoke_tested`. Glossary
keys that match a default replace it in place; new keys are appended; a
`null` value removes a default. Without these fields the output is the same
as before.

Exit 2 means an error, and nothing is written. The errors are:
- no config, no YAML parser, or YAML that does not parse;
- an unreadable enabled profile, or a score that is not a number;
- an override naming an unknown task id, a model with no profile, or a
  disabled model;
- an effort that is `max`, not a string, or not one of the model's levels;
- a duplicate task id;
- a write failure. The three files are written to temp files first and
  replaced together, keeping each existing file's mode.

Warnings go to stderr and the JSON `warnings` list. The warning cases are:
- a deprecated model that is enabled;
- an enabled model that no harness or bridge reaches;
- a missing score axis, tasks block or `effort.default`;
- `propose` with `merge_prs: true` (merging is then listed under May never);
- a quoted `enabled` value;
- a config key `config-schema.md` does not list ("unknown config key
  <path>; ignored", or how it is used instead, plus a "did you mean" hint
  when a known key is close), or a config block that is not a mapping;
- malformed optional fields. Output is byte-identical for the same
inputs on the same UTC date; set `SOURCE_DATE_EPOCH` to pin the date.

`routing.stamp` is flat text, one record per line:

```
generated <ISO-8601 UTC>
generator generate.py 1
kit_root <absolute path>
kit_version <retained for old stamps; plugin.json has no version, so always unknown>
kit_commit <git short sha if the kit root is the top of a checkout, else its dir name if 7-40 hex, else unknown>
config_updated <config.user.updated>
tasks <first 12 hex of sha256 of core/tasks.md>
profile <id> <as_of> <enabled|disabled|unconfigured>
```

There is one `profile` line for every `core/models/*.md` except
`_schema.md`, sorted by id. The session-start hook compares these lines
with the kit to say when the table is stale.

This markdown file stays the spec. Agents on harnesses without Python or a
YAML parser follow the steps above by hand. Those runs write no stamp, so
the session-start status keeps flagging until the script can run. Where the
script and this file disagree, fix the script.
