---
name: writing-requirements
description: Use when a part's functions or hazards have no requirements yet, when what must hold for a function is unclear or has to change - how well, how fast, what happens on bad input or failure - or when the builder states a constraint. Produces REQ- files. Not for what the part does (use writing-functions), how a requirement will be verified (use writing-proofs), or how it is met (synthesis).
---

# Writing requirements

A requirement says what must hold for a function to count as done: what result is seen,
how well where someone cares, and what the part does when things go wrong. Someone who
never saw the conversation writes the cases from it, so it must stand alone and be
verifiable at the level it is written. The reviewer of the requirements step checks the
requirements against this file.

## Where requirements come from

Walk the model: each requirement comes from one of the sources below. This step creates
no topics. Something the walk finds missing, such as a function with no input for what
it needs, goes back to the step that owns it.

1. **Each function.** Every function needs at least one requirement `of:` it.
   - **Functional:** what result must be seen for the function to be done? "When the
     climber asks for the next session, the part shall propose a session that names
     each exercise and its load."
   - **Performance:** how well must it be done? Ask only where the builder, a hazard or
     a budget cares about speed, size, accuracy or cost. Where nobody does, write none.
2. **Each input of a function** (unwanted behaviour, EARS). What makes the input valid
   (its ranges, what must be present), and what the part does with one that is not.
   If it comes from an outside system: what the part does when that system fails or
   answers wrongly. Write the response, not only the detection.
3. **Each output of a function** (unwanted behaviour, EARS). If a function it goes to
   can run after the part is closed or restarted, what must still be there. If a run
   can be interrupted while the output is made: what is left, whole or none.
4. **Each hazard of the part.** Decide how to deal with it, settled like any value
   (see the rules), and give the reason in the rationale. Write the requirements with
   `answers: [HAZ]` and `of:` the function they constrain, in one or both forms:
   - **Prevent:** turn the hazard around into the condition the part keeps. "The part
     proposes a load the climber cannot take" becomes "the part shall propose only loads
     within what the climber has recently completed".
   - **Respond:** "If \<the hazard's state\> occurs, then the \<part\> shall \<detect
     it and act to prevent or reduce the loss\>": the `unwanted` pattern.
   - If the hazard is not worth answering, accepting it is a decision with its
     reason: leave the hazard open with an issue, for synthesis to record.
5. **Each elicitation entry marked `constraint: true`.** A limit the builder sets that
   no function explains ("runs without a network connection") is a requirement with
   `source: builder`. A choice of technology is not: write it into the issue or the
   elicitation record as a preference, for synthesis to decide.

One requirement for each condition that has its own response: they are proved one by
one.

## What is a requirement and what is not

| It is written as | It is really | Put it in |
|---|---|---|
| "The part shall plan the next session" | the function restated | the result that shows it was done |
| "shall use SQLite", "shall cache plans" | a mechanism | a decision in synthesis |
| "shall be fast", "shall be easy to use", "shall be robust" | a wish with no test | a measure, or ask the builder what they would check |
| "shall handle errors" | an empty verb | the condition and the response: "If the log file cannot be read, then…" |
| "shall show plans and log sessions and export data" | several requirements | one requirement each |
| "shall not do X" with nothing that could make it do X | overbuilding | nothing |

## Rules for each requirement

- **Needed.** Ask what is the worst that could happen if it were left out. If nothing,
  delete it, or ask the builder.
- **One "shall".** Two "shall"s are two requirements. The validator warns on them.
- **An EARS pattern.** Write the statement in the pattern that fits and name it:

  | `pattern` | Form |
  |---|---|
  | `ubiquitous` | The \<part\> shall \<response\>. |
  | `event` | When \<trigger\>, the \<part\> shall \<response\>. |
  | `state` | While \<state\>, the \<part\> shall \<response\>. |
  | `unwanted` | If \<trigger\>, then the \<part\> shall \<response\>. |
  | `optional` | Where \<feature is included\>, the \<part\> shall \<response\>. |
  | `complex` | More than one keyword, in this order: While, When, If…then. "While \<state\>, if \<trigger\>, then the \<part\> shall…" |

  Use `none` only when no pattern fits, and say why in the rationale.
- **The subject is "the part".** Write "the part shall…", never the part's or the
  product's name: the requirement then survives a rename or a move to another part.
- **Stands alone.** In the statement, name things, never "it", "they" or "this".
  Replace "as appropriate", "where possible", "etc.", "and/or" and "such as"
  with the actual cases.
- **Verifiable.** You can say how it would be shown to hold. Words with no test
  ("fast", "easy", "sufficient", "safe", "robust", "user-friendly") become a measure or
  a question for the builder. "All", "always" and "never" can be proved only over a
  stated set: name the set.
- **Stated positively,** as what the part does. Write "shall not" only when the hazard
  or the builder names an act the part must never do.
- **What, not how.** It must stay true if the technology changes.
- **No invented values or rules.** A number, a limit or a rule is settled with a
  reason: by research or a spike, or by the builder. Examples: how an amount that does
  not divide evenly is rounded, what is kept when the part is closed, which inputs are
  refused, how a hazard is dealt with. Until it is settled it is `TBD`, and the
  question goes to the builder with the step's batch; one still open after that gets
  an issue that says how it will be settled. A plausible guess is read later as
  agreed, so write `TBD` instead.
- **A tolerance that matters.** Ask what would happen if the value were doubled. If
  nothing would, the bound is tighter than anyone needs: loosen it or ask.
- **The number goes in the measure, once.** The statement holds `{measure}` where the
  value would be; the measure holds the metric, its unit and the bounds. A proof refers
  to the measure and never copies the number.
- **A rationale on every requirement:** why it is needed and what it assumes, in the
  requirement's own terms. Say where each value or rule came from, and why this
  response over an obvious other (refuse, ignore, warn, retry). A rationale that only
  restates the statement or the links fails review.

## The file

One file per requirement in the part's `requirements/` folder, named by its ID. Make the
ID with a fresh suffix and check that no file already uses it:

```
echo "REQ-$(LC_ALL=C tr -dc '0-9A-HJKMNP-TV-Z' </dev/urandom | head -c 4)"
```

Fields: `id`, `status` (`draft` until the builder agrees), `pattern`, `statement`, at
least one reason to exist (`of` a function of this part, `answers` hazards of this part,
or `source: builder`), `measure` when there is a number (`metric` in snake_case, an
optional `definition` of exactly what is measured, `unit`, and `bounds`, each a
`statistic` from value, mean, p50, p90, p95, p99, max, min, proportion, rate, an `op`
and a `value` or `TBD`), and `rationale` as above.

Four examples, for illustration only. The second and third answer one hazard,
HAZ-6VJR: "the part proposes a load the climber's body cannot take".

A performance requirement:

```yaml
id: REQ-4W8N
status: draft
pattern: event
statement: |
  When the climber asks for the next session, the part shall propose that session
  within {measure}.
measure:
  metric: plan_time
  definition: From the request to the proposed session being shown.
  unit: s
  bounds:
    - {statistic: p95, op: "<=", value: 2}
rationale: The climber asks at the wall, between attempts; past two seconds they stop waiting.
of: FUN-7K3Q
```

Prevent, written as a prohibition because the hazard is an act, with a value not yet
settled:

```yaml
id: REQ-9C2T
status: draft
pattern: ubiquitous
statement: |
  The part shall not propose a session whose load exceeds the climber's highest
  completed load of the last four weeks by more than {measure}.
measure:
  metric: load_increase
  definition: |
    How far the proposed session's load exceeds the highest completed load of the last
    four weeks, as a percentage of that load.
  unit: "%"
  bounds:
    - {statistic: max, op: "<=", value: TBD}
rationale: |
  A sudden rise in load is the usual path to a finger injury. The safe rise depends on
  the climber; it is settled by research (issue open).
of: FUN-7K3Q
answers: [HAZ-6VJR]
```

Respond, in the `complex` pattern, choosing a warning over a block:

```yaml
id: REQ-3JQE
status: draft
pattern: complex
statement: |
  While the climber's last logged session records pain, if the climber starts a
  session with a higher load than that session, then the part shall warn the
  climber before the first exercise.
rationale: Blocking the session was the obvious alternative; the builder wants the climber to decide.
of: FUN-2PXD
answers: [HAZ-6VJR]
```

A constraint of the builder:

```yaml
id: REQ-1F5D
status: draft
pattern: ubiquitous
statement: The part shall do each of its functions without a network connection.
rationale: Climbing gyms often have no signal.
source: builder
```
