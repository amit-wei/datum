---
name: functional-analysis
description: Use when a part's functions are not yet known or have to change - a new product idea, a new capability the existing functions do not cover, or a part the parent's synthesis has just created. Engine step 1 of datum for every part; produces functions, scenarios, losses and hazards. Not for writing what must hold for a function (use requirements) or choosing parts (use synthesis).
---

# Functional analysis (engine step 1)

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
- Before a convention, definition, standard, price or version enters the model, load
  research, even when you feel confident.
- When considering whether something is done, start from what it must cover: the end
  conditions of every step it feeds, and every parent need, budget and constraint.
  Look for what has nothing attached, and check each against the model.
- A claim that something holds names its evidence: what was run or inspected, against
  what. Say what you did not check.

## Goal

The functions of this part, complete for its scope. A function says what the part does,
never how. The scope of the product is the whole product; the scope of any other part
is the current increment.

## Inputs

- **The product:** the builder's needs and constraints, drawn out by grilling into an
  elicitation record (`ELI-` in `.datum/model/product/analysis/`).
- **Any other part:** what the parent's synthesis gave it: the parent functions it
  `contributes_to`, the requirements written into its `requirements/` folder, and the
  interfaces that name it; plus what grilling draws out.
- **Every part:** anything elsewhere in the model that links to this part's ID or its
  functions. Search for them before writing; each is an obligation on this part.

If an input from the parent part is infeasible, conflicts with another, or is missing,
open an issue on the parent part and raise it with the builder; the parent's step makes
the change. A gap in this part's own artifacts follows the stance.

## Outputs

- `FUN-` files in the part's `functions/` folder, each with `serves` (the product) or
  a `parent` function (any other part).
- `SCN-` files in `analysis/`, for the product.
- `LOS-` files in `analysis/`, for the product; `HAZ-` files in `analysis/`, for every
  part that introduces a hazard.
- Records of the techniques used (`ELI-`, `RES-`, `SPK-`) in `analysis/`.

## Techniques

Load a technique before you produce what it produces, and before you answer a question
about it. Its body holds the conventions, the quality reference and the output format;
the lines below only say when it applies. On a question, answer with the technique
loaded and offer to run it; write nothing until the builder agrees. A forced technique
runs before anything else is written; the rest are due when the end condition needs them.

1. `grilling`: forced at the start of a part that has no elicitation record in its
   `analysis/` folder, before anything is written. A part with one has been grilled:
   carry on from where it stands. Afterwards, whenever a finding can be settled only by
   the builder.
2. `research`: when the domain is unfamiliar, or a solution may already exist (buy,
   reuse, or learn from it). Run it in a subagent; keep only the conclusion.
3. `writing-scenarios`: forced for the product once the needs are drawn out.
4. `writing-functions`: for every part. In the product after the scenarios;
   in a part, from the parent functions it contributes to. It holds the rules for what
   is and is not a function (a property, an interface, a guard, a mechanism are not).
5. `losses-and-hazards`: at every part once it has functions; the end condition needs it.
   Do not name, propose or rule out a loss or a hazard without it loaded: its rules
   decide what counts as one.
6. `running-a-spike`: when there is a doubt that a function is feasible. In a
   subagent, time-boxed, with a written question.

## End condition

- The builder has gone through the set of functions, with the data table and event
  list of `writing-functions`, and agrees it covers what they expect this part to do.
- Every scenario step is done by some function.
- Each lens of `writing-functions` has been read: every empty cell of the data table
  and every event with no response is filled by a function, or left empty by the
  builder's choice.
- Every gap found has an outcome: changed, left out with the builder's reason, or
  raised as an issue.
- Every function serves a scenario (product) or a parent function (a part).
- Every function lists its inputs and outputs; every output has a user, and every
  input from a function is one of its outputs.
- Every elicited need is in a scenario, or marked `out_of_scope` with a reason.
- The elicitation records answer each area that applies to the whole part (in
  `grilling`), "none" included.
- Every function has been checked, with `losses-and-hazards` loaded, for hazards it
  introduces.
- Every elicited loss is a `LOS-` file, or marked `out_of_scope` with a reason; every
  loss is reached by at least one hazard (product).
- Every obligation found in the inputs is met by a function or raised as an issue.
- No feasibility doubt is left without a spike or a `TBD` with an issue.
- The validator is clean (no errors): `uv run "${CLAUDE_PLUGIN_ROOT}/scripts/validate.py"`.
- The closing review is clean: run the `review-functional-analysis` agent with the
  part's path. Fix each blocking and should-fix finding, or reject it with a reason,
  and run the agent again. A finding you reject that the reviewer upholds goes to the
  builder.

The builder closes the step. On their word, record it in `.datum/model/<part>/steps.yaml` as
`functional-analysis: {closed_at: "<commit>"}`.
