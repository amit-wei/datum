---
name: writing-requirements
description: Use when a part's functions or hazards have no requirements yet, when what must hold for a function is unclear or has to change - how well, how fast, what happens on bad input or failure - or when the builder states a constraint. Produces REQ- files. Not for what the part does (use writing-functions), how a requirement will be verified (use writing-proofs), or how it is met (synthesis).
---

# Writing requirements

A requirement says what must hold for a function to count as done: what result is seen,
how well where someone cares, and what the part does when things go wrong. It is
verifiable at the level it is written: someone could check it without asking what was
meant. The reviewer of the requirements step checks the requirements against this file.

## Where requirements come from

1. **Each function.** Ask three questions, and write a requirement for each answer that
   matters:
   - **Attained:** what result must be seen for the function to be done? "When the
     climber asks for a plan, the planner shall propose a session that names each
     exercise and its load."
   - **How well:** does the builder, a hazard or a budget care about speed, size,
     accuracy or cost here? Only then write a measure. Otherwise there is no "how well"
     requirement: do not invent one.
   - **Unwanted behaviour:** what must the part do on bad input, a missing input, an
     outside system failing, an interrupted run? Write the response, not only the
     detection.
   Every function needs at least one requirement `of:` it.
2. **Each hazard of the part.** Ask what must hold so that the hazard's state cannot
   lead to its loss, or so the part does not enter that state. Write it with
   `answers: [HAZ]`, and `of:` the function it constrains. If the builder would rather
   accept the hazard than answer it, that is a decision: leave the hazard open with an
   issue, for synthesis to record.
3. **The builder's constraints.** A limit the builder sets that no function explains
   ("runs without a network connection") is a requirement with `source: builder`. A
   choice of technology is not: that is a decision for synthesis, even when the builder
   already has a preference. Record the preference in the issue or elicitation record.

## What is a requirement and what is not

| It is written as | It is really | Put it in |
|---|---|---|
| "The planner shall plan the next session" | the function restated | the result that shows it was done |
| "shall use SQLite", "shall cache plans" | a mechanism | a decision in synthesis |
| "shall be fast", "shall be easy to use", "shall be robust" | a wish with no test | a measure, or ask the builder what they would check |
| "shall handle errors" | an empty verb | the condition and the response: "If the log file cannot be read, then…" |
| "shall show plans and log sessions and export data" | several requirements | one requirement each |
| "shall not do X" with nothing that could make it do X | overbuilding | nothing |

## Rules for each requirement

- **One "shall".** Two "shall"s are two requirements. The validator warns on them.
- **An EARS pattern.** Write the statement in the pattern that fits and name it:

  | `pattern` | Form |
  |---|---|
  | `ubiquitous` | The \<part\> shall \<response\>. |
  | `event` | When \<trigger\>, the \<part\> shall \<response\>. |
  | `state` | While \<state\>, the \<part\> shall \<response\>. |
  | `unwanted` | If \<unwanted condition\>, then the \<part\> shall \<response\>. |
  | `optional` | Where \<feature is included\>, the \<part\> shall \<response\>. |
  | `compound` | Two of the above together: "While…, when…, the \<part\> shall…". |

  Use `none` only when no pattern fits, and say why in the rationale.
- **Verifiable.** You can say how it would be shown to hold. If you cannot, rewrite it
  before going on.
- **What, not how.** It must stay true if the technology changes.
- **No invented values.** A number comes from the builder (grilling), from an
  established source (research), or from a measurement (a spike), settled before it is
  written. Until then the value is `TBD`, and each `TBD` gets an issue that says how it
  will be settled.
- **The number goes in the measure, once.** The statement holds `{measure}` where the
  value would be; the measure holds the metric, its unit and the bounds. A proof refers
  to the measure and never copies the number.
- **A rationale** is required when there is a measure (why this value), and when the
  requirement picks one response over an obvious other (refuse, ignore, warn, retry).
  It never restates the links.

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

Three examples, for illustration only:

```yaml
id: REQ-4W8N
status: draft
pattern: event
statement: |
  When the climber asks for the next session, the planner shall propose it within
  {measure}.
measure:
  metric: plan_time
  definition: From the request to the proposed session being shown.
  unit: s
  bounds:
    - {statistic: p95, op: "<=", value: 2}
rationale: The climber asks at the wall, between attempts; past two seconds they stop waiting.
of: FUN-7K3Q
```

```yaml
id: REQ-9C2T
status: draft
pattern: unwanted
statement: |
  If the climber has logged pain in the last session, then the planner shall propose
  no session with a higher load than that session.
rationale: Refusing to plan was the obvious alternative; the builder wants a lighter plan instead.
of: FUN-7K3Q
answers: [HAZ-6VJR]
```

```yaml
id: REQ-1F5D
status: draft
pattern: ubiquitous
statement: The product shall do each of its functions without a network connection.
rationale: Climbing gyms often have no signal.
source: builder
```
