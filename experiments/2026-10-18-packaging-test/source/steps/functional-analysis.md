---
name: functional-analysis
description: Use when a block's functions are not yet known or have to change: a new product idea, a new capability the existing functions do not cover, or a part that has just become a block of its own. Engine step 1 of datum; produces functions, scenarios and losses. Not for writing requirement text (use requirements) or choosing parts (use synthesis).
real: true
---

# Functional analysis (engine step 1)

{{include stance}}

## Goal

The functions of this block and the flows between them, complete for its scope, plus
the losses the block could cause. Infeasible or conflicting inputs go back up a level.

## Inputs

At product level: the builder's needs and constraints, drawn out by grilling into an
elicitation record (`ELI-`). Below: the functions, requirements and interfaces the
parent's synthesis gave this part.

## Techniques

{{include load-techniques}}

At product level the weight is on grilling and scenarios; below, on writing functions.

{{use grilling: Forced once at the start of product level, before anything is written. Afterwards, whenever a finding can be settled only by the builder.}}
{{use research: When the domain is unfamiliar, or a solution may already exist (buy, reuse, or learn from it). Run it in a subagent; keep only the conclusion.}}
{{use writing-scenarios: Forced at product level once the needs are drawn out: the end-to-end journeys that the functions must serve.}}
{{use writing-functions: For every block; at product level after the scenarios, below from the functions the parent assigned.}}
{{use losses-and-hazards: Forced at product level; below, when a function of this block can cause a loss.}}
{{use running-a-spike: When there is a doubt that a function is feasible. In a subagent, time-boxed, with a written question.}}

## End condition

- Every scenario step is done by some function.
- Every function serves a scenario (product level) or a parent function (below).
- Every elicited need is in a scenario or marked out of scope.
- Losses are listed.
- No feasibility doubt without a spike or a TBD with an issue.
- The closing review is clean: run the `review-functional-analysis` agent; fix its
  findings and run it again. The builder closes the step.
