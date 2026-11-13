---
name: requirements
description: Use when a part's functions are written and what must hold for them is not - how well, what happens on failure, what answers each hazard - or when a requirement, a constraint or a proof has to change. Engine step 2 of datum for every part; produces requirements and their proofs. Not for what the part does (use functional-analysis) or how the requirements are met (use synthesis).
---

# Requirements (engine step 2)

## Stance

- Before producing anything, understand the step's inputs and the outputs it must
  produce. The inputs are the outputs of earlier steps and of the parent part; read
  them in the model, and use the step's techniques to fill what is missing.
- Prefer the simple, lean solution that fits the existing architecture. Reuse what
  already does the job, inside the part that owns it; build something new only when the
  inputs call for it.
- Write only what a step needs and a later step or check uses, and link each artifact
  to what it serves. If something else seems useful, note it as an issue instead.
- Stay inside datum's steps. For work no step covers, ask the builder first.
- When a choice is the builder's (a preference, priority, premise, or trade between
  goals), ask before you write it.
- When a fact is missing, say so and what depends on it; do not fill it with a
  plausible value. When a choice rests on an assumption, say where it stops holding.
- Before a convention, definition, standard, price or version enters the model, load
  research, even when you feel confident.
- When considering whether something is done, start from what it must cover: the end
  conditions of every step it feeds, and every parent need, budget and constraint.
  Look for what has nothing attached, and check each against the model.
- A claim that something holds names its evidence: what was run or inspected, against
  what. Say what you did not check.

## Goal

The requirements that say when each function of this part is attained, and how well
where the builder, a hazard or a budget cares; the requirements that answer the part's
hazards; the builder's constraints; and a proof for each. There is no target number of
requirements: the scope is bounded by the part's functions.

## Inputs

- **The part's functions** (`functions/`) and **hazards** (`HAZ-` in `analysis/`).
- **The elicitation records** (`ELI-` in `analysis/`): the builder's constraints, and
  any values they gave.
- **Every part:** anything elsewhere in the model that links to this part's ID or its
  functions. Search for them before writing; each is an obligation on this part.

This version of the step covers the product only. In any other part, tell the builder
that datum does not yet say how to work from the requirements a parent hands down, and
stop.

If an input is infeasible, conflicts with another, or is missing, do not work around
it here: open an issue on the part that owns it and raise it with the builder.

## Outputs

- `REQ-` files in the part's `requirements/` folder, each with at least one reason to
  exist: `of` a function, `answers` hazards, or `source: builder`.
- `PRF-` files in the part's `proofs/` folder, each covering requirements of this part.
- Records of the techniques used (`ELI-`, `RES-`, `SPK-`) in `analysis/`, and an issue
  for every `TBD`.

## Techniques

Load a technique before you produce what it produces, and before you answer a question
about it. Its body holds the conventions, the quality reference and the output format;
the lines below only say when it applies. On a question, answer with the technique
loaded and offer to run it; write nothing until the builder agrees. A forced technique
runs before anything else is written; the rest are due when the end condition needs them.

1. `writing-requirements`: for every function, every hazard and every constraint of the
   builder. It holds the rules for what is and is not a requirement, and where a value
   may come from.
2. `writing-proofs`: for every requirement, once it is written.
3. `grilling`: when a value or a choice is the builder's: how well is good enough, which
   response to a failure they want, whether a hazard is answered or accepted, whether a
   constraint holds. Ask before you write it.
4. `research`: forced before a value that is not the builder's enters a measure (an
   established figure, a standard, a known limit). Run it in a subagent; keep only the
   conclusion and its source.
5. `running-a-spike`: when a value can only be found by measuring. In a subagent,
   time-boxed, with a written question. Until it reports, the value is `TBD` with an
   issue.

## End condition

- The builder has gone through the requirements and agrees they say what they expect,
  each value included.
- Every function of the part has at least one requirement `of` it.
- Every hazard of the part is answered by a requirement, or left open with an issue
  for synthesis to decide.
- Every constraint in the elicitation records is a requirement with `source: builder`,
  marked `out_of_scope` with a reason, or, for a choice of technology, left to
  synthesis.
- Every requirement is covered by at least one proof with a criterion.
- Every `TBD` has an issue that says how it will be settled.
- The validator is clean (no errors): `uv run "${CLAUDE_PLUGIN_ROOT}/scripts/validate.py"`.
- The closing review is clean: run the `review-requirements` agent with the part's
  path. Fix each blocking and should-fix finding, or reject it with a reason, and run
  the agent again. A finding you reject that the reviewer upholds goes to the builder.

The builder closes the step. On their word, record it in `.datum/model/<part>/steps.yaml` as
`requirements: {closed_at: "<commit>"}`.
