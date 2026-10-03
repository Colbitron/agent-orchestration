# Routing generator

How an agent turns `config.yaml` plus `core/models/*.md` into
`~/.agent-orchestration/routing.md` and `glossary.md`. This is a procedure,
not a program; the agent running setup follows it by hand. Keep it
deterministic enough that two runs on the same inputs give the same table.

## Inputs

- `config.yaml` (see `config-schema.md`)
- every `core/models/*.md` whose `id` is enabled in `config.models`
- `core/tasks.md` for the task list and glossary defaults

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
4. If `priorities.frustration_tolerance` is `low`, add 1 to `floor` before
   weighting. If `budget_sensitivity` is `high`, add 1 to cost.

## Step 2: pick primary and fallback

- **Primary**: highest-scoring model with `fit: best`; if none, `good`; if
  none, `ok` with a guardrail note copied from the profile.
- **Fallback**: next model, preferring a different family if one is enabled.
- **Effort**: the primary profile's `effort.default`, unless `config.effort`
  overrides it.
- **Why**: one sentence built from the profile's task note and the axis that
  decided it. Cite nothing; the user can read the profile.

Special rules:

- `review`: primary must be from a family other than the family most used
  for `feature`. If only one family is enabled, pick the model with the
  highest `thoroughness` that is not the `feature` primary and add the line
  "Single-family setup: a second vendor's reviewer would catch more."
- `computer-use`: if no enabled model has `computer_use` ≥ 6, write
  "No capable computer-use model enabled; verify by running tests and
  reading logs instead" and leave the row's primary empty.
- `orchestrate`: this is the model the user is sitting in front of unless
  the primary harness can switch models. Say so in the row.
- `bulk`: if a model has user `cost` ≥ 8, it wins the row regardless of
  score as long as its fit is at least `ok`, because bulk work should burn
  the cheapest capable quota. Theo's rule.

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
(one row per enabled model, from profile scores and config cost)

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
- Never use `max` effort on any model. <effort notes from profiles>.
- Every delegated prompt states what you want, what "done" means, and when
  to stop and ask. See delegation-prompting.
- Review: <cross-family rule as resolved>.
- Prefix every subagent or workflow stage name with the model it runs on
  (e.g. `[sol] review-auth`) so the human can see who did what.
- If a bridged model returns nothing, it must say so and name what it
  inspected; do not re-run on an empty result.
- Log each delegated task to <logging.path> if logging is enabled.

## Standing permissions (autonomy: <level>)
- May: <list from autonomy.may where true>
- May never: <list where false>, deploy to production, or act outside the
  repository without asking.
- Reviewer bots that gate merges: <list or "none; merges stay human">.
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
- No row's effort is `max`.
- The file is under about 150 lines. If not, shorten the "Why" column; do
  not drop rows.

## Regeneration

Setup regenerates `routing.md` and `glossary.md` from scratch each run.
`lessons.md` is never touched by the generator. If the user hand-edits
routing.md, the next run will overwrite it, so setup diffs the old and new
file and shows the user anything that would be lost before writing.
