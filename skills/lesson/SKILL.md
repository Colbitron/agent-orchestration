---
name: lesson
description: Record a lesson from a delegation that went wrong and turn it into a durable config change. Use when the user says an agent or model did something unexpected, or asks "how do we prevent this going forward", or after a bridged model misbehaved.
user-invocable: true
argument-hint: "[what you expected] -> [what happened]"
---

# Lesson

This is the improvement loop from `core/strategies/improvement-loop.md`.
Read that file from the kit root first if you have not this session.

## Procedure

1. **Diagnose.** Ask the model that misbehaved (or reason about its
   transcript if it is gone): "I expected X. You did Y. What signals, files,
   or tool results led you there?" Summarise the cause in two sentences.
2. **Propose.** Draft the smallest set of changes that would prevent a
   repeat. Candidates, in order of preference:
   - a line in the user's `~/.agent-orchestration/lessons.md`
   - an exact command or flag correction in the relevant bridge skill
   - a per-model note in `config.yaml` (an `effort` or `cost` override, or
     disabling a model for a task) followed by regenerating the table
   - a change to a core profile or strategy doc, if the lesson is general
     and not user-specific; say so and let the user decide whether to
     upstream it
3. **Cut it in half.** Show the proposal and remove anything the user does
   not confirm. Theo's rule: the model always suggests too much.
4. **Apply.** Append to `lessons.md` in this form:

   ```
   - <date> | <task id> | <model> | <one-line cause> → <one-line rule>
   ```

   Make any bridge or config edit the user approved. If config changed,
   regenerate `routing.md` via the generator procedure.
5. **Confirm.** Restate the rule in one line so the user can object.

Never rewrite or delete earlier lessons. If a lesson contradicts an older
one, append the new one and mark the old one superseded with a trailing
`(superseded <date>)`.
