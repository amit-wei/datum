---
name: synthesis
description: Use when a block's functions and requirements are agreed and the design is not chosen yet or has to change: which parts, which stack, where data lives, what flows between parts, whether to split a part further. Engine step 3 of datum; produces decisions, parts, interfaces and derived requirements. Not for checking a finished design against scenarios (use design-evaluation).
real: true
---

# Synthesis (engine step 3)

{{include stance}}

## Goal

The design choices that meet this level's functions and requirements, recorded as
decisions with the alternatives considered. Choices create derived requirements.

## Techniques

{{include load-techniques}}

In this order (IEEE 1220):

{{use grouping-functions: First: group this block's functions into candidate parts.}}
{{use research: On what exists, to buy or build. In a subagent.}}
{{use trade-study: For every significant choice; forced for the stack at product level.}}
{{use running-a-spike: When trade-study options cannot be ranked without measuring.}}
{{use allocating-requirements: For every requirement of this level: flow it down as child requirements in the parts' folders (budgets split between parts), or cover it by this level's own proof.}}
{{use writing-requirements: For the derived and child requirements the choices create.}}
{{use defining-interfaces: For every pair of parts, or part and external, that exchange something.}}
{{use deployment-view: Once parts exist: which parts share a unit; every extra unit needs a decision.}}
{{use architectural-risk-pass: After the parts and interfaces exist: unsafe control actions, and STRIDE on every interface that crosses a trust boundary.}}
{{use applying-stopping-rule: For every part: stop, or queue it for its own level.}}

## End condition

- Every function has at least one contributing part.
- Every requirement is flowed down or covered by this level's own proof.
- Every interface has its items; every extra unit is justified.
- Every part meets the stopping rule or is queued for the next level.
- Every architectural risk is answered, accepted or open with an issue.
- The closing review is clean: run the `review-synthesis` agent; fix its findings and
  run it again. The builder closes the step.
