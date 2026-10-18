---
name: requirements
description: Use when a block's functions are agreed and what must hold for each, and how well, is not yet written or has to change; or when a hazard, constraint or budget needs a requirement. Engine step 2 of datum; produces requirements and their proofs. Not for discovering new functions (use functional-analysis) or flowing budgets down to parts (use synthesis).
real: true
---

# Requirements (engine step 2)

{{include stance}}

## Goal

The requirements that say each function is attained, and how well where the builder, a
hazard or a budget cares; plus constraints and allocated budgets. Each has a proof.

## Inputs

The block's functions and hazards; at product level the builder's constraints; below,
the requirements the parent's synthesis wrote into this part's folder.

## Techniques

{{include load-techniques}}

No bound on the number of requirements: the scope is bounded by the increment.

{{use writing-requirements: For every function (attained, how well, unwanted behaviour), for every hazard, and for every builder constraint.}}
{{use writing-proofs: For every requirement, as soon as its statement is agreed: no requirement is finished without a proof.}}
{{use grilling: When a value or a choice only the builder knows is missing, or it is unclear whether something is a constraint of theirs.}}
{{use research: When a value or a definition is already established elsewhere (a standard, a convention, a current price). In a subagent.}}
{{use running-a-spike: When a TBD value can be measured. In a subagent, time-boxed.}}

## End condition

- Every function has at least one requirement `of:` it.
- Every hazard is answered, accepted by a decision, or open with an issue.
- Every requirement has a reason to exist and a proof with a criterion.
- Every TBD has an issue.
- The closing review is clean, including conflicts visible from the requirements alone:
  run the `review-requirements` agent; fix its findings and run it again. The builder
  closes the step.
