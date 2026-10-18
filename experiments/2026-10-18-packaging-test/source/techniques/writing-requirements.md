---
name: writing-requirements
description: Use when what must hold for a function, a hazard, a builder constraint or a budget is not yet stated as a checkable requirement, or a requirement must be split or flowed down. Writes EARS statements with a measure and a reason to exist. Not for how a requirement will be checked (use writing-proofs) or a small wording fix.
real: true
---

One "shall" per requirement, in an EARS pattern (ubiquitous, event, state, unwanted,
optional). A requirement says what and how well, never how: no architecture in the text.
Where it is measurable, one metric with bounds, `value: TBD` if unknown (a spike or a
grilling trigger). Every requirement has a reason to exist: `of: FUN`, `parent: REQ`,
`justified_by: DEC`, `answers: RSK`, or `source: builder`. A rationale is required with
a measure. Output: `REQ-` files in the block's `requirements/` folder.
