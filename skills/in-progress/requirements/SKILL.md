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
- When you find something missing or wrong in an earlier step's artifacts (a gap),
  change it there instead of writing around it. If the change only brings the model in
  line with what is agreed (Class II), make it and say so. If it adds scope or changes
  what was agreed (Class I), put it in the builder's batch with a recommendation, and
  make it once they agree.
- Before a convention, definition, standard, price or version enters the model, run
  the `researcher` agent instead of searching yourself, even when you feel confident.
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

- **The part's functions** (`functions/`), with their inputs and outputs, and
  **hazards** (`HAZ-` in `analysis/`).
- **The elicitation records** (`ELI-` in `analysis/`): the entries marked
  `constraint: true`, and any values the builder gave.
- **Every part:** anything elsewhere in the model that links to this part's ID or its
  functions. Search for them before writing; each is an obligation on this part.

Datum cannot yet work from requirements handed down by a parent part's synthesis. If
any were handed to this part, tell the builder so, and stop. A part with none runs this
step like any other.

If an input from the parent part is infeasible, conflicts with another, or is missing,
open an issue on the parent part and raise it with the builder; the parent's step makes
the change. A gap in this part's own artifacts follows the stance.

## Outputs

- `REQ-` files in the part's `requirements/` folder, each with at least one reason to
  exist: `of` a function, `answers` hazards, or `source: builder`.
- `PRF-` files in the part's `proofs/` folder, each covering one requirement of this part.
- Records of the techniques used (`ELI-`, `RES-`, `SPK-`) in `analysis/`, and an issue
  for every `TBD`.

## Techniques

Load a technique before you produce what it produces, and before you answer a question
about it. Its body holds the conventions, the quality reference and the output format;
the lines below only say when it applies. On a question, answer with the technique
loaded and offer to run it; write nothing until the builder agrees. A forced technique
runs before anything else is written; the rest are due when the end condition needs them.

1. `writing-requirements`: for every function, input, output, hazard and constraint.
   It holds the walk over these sources and what to ask of each, the ways to answer a
   hazard, the rules for what is and is not a requirement, and the file format.
2. `writing-proofs`: for every requirement, once it is written. It holds how to choose
   and justify a method, how to write a criterion a case author can check without
   asking, and the file format.
3. **Settling a value or a rule:** due before the builder agrees the requirements.
   Settle it with the `researcher` agent (cite the `RES-` record it returns) or
   the `spiker` agent (cite the `SPK-` record it returns), or leave it
   `TBD` for the builder's batch, asked with `grilling`. One still open after the batch
   gets an issue that says how it will be settled.

## Order

1. Write the requirements and proofs; a value only the builder can give stays `TBD`.
2. Run the validator, then the `review-requirements` agent with the part's path, and
   wait for its findings before going on: it runs in the background by default. Fix
   each blocking and should-fix finding, or reject it with a reason, and run the agent
   again until it is clean, or until each finding left is an upheld rejection or waits
   on the builder's answer.
3. Ask the builder once, with `grilling`: every open value or rule, every Class I gap
   in the functions, every rejection the reviewer upheld, and whether the requirements
   say what they expect.
4. Write in the answers. Run the validator again, and the reviewer again on each
   requirement whose meaning changed beyond a value filled in.

## End condition

- Every function of the part has at least one requirement `of` it, and each of its
  inputs and outputs has been asked the questions in `writing-requirements`.
- Every hazard of the part is answered by a requirement, or, where it is accepted,
  left open with an issue for synthesis to record the decision.
- Every elicitation entry marked `constraint: true` is a requirement with
  `source: builder`, marked `out_of_scope` with a reason, or, for a choice of
  technology, left to synthesis.
- Every requirement is covered by at least one proof with a criterion.
- Every `TBD` has an issue that says how it will be settled.
- Every gap found has an outcome: changed, left out with the builder's reason, or
  raised as an issue.
- The validator is clean (no errors): `uv run "${CLAUDE_PLUGIN_ROOT}/scripts/validate.py"`.
- The closing review is clean, as in Order: each finding fixed, or rejected with a
  reason the reviewer accepts or the builder settles.
- The builder has gone through the requirements, after the review, and agrees they say
  what they expect, each value included.

The builder closes the step. On their word, record it in `.datum/model/<part>/steps.yaml` as
`requirements: {closed_at: "<commit>"}`.
