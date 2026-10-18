---
name: writing-proofs
description: Use when a requirement has no proof yet, or its criterion is unclear: how it will be shown to hold, by Inspection, Analysis, Demonstration or Test, and what counts as a pass. Writes the planned verification, not the test code. Not for executable tests (use writing-cases) or the requirement text (use writing-requirements).
real: true
---

A proof names its method (Inspection, Analysis, Demonstration, Test), the requirements
it covers (`covers:`) and its criterion: the pass condition, sample size, confidence and
conditions. It refers to the requirement's measure and never copies the number. An AI
eval is a Test with a statistical criterion. A requirement no proof can cover is
rewritten. Output: `PRF-` files in the block's `proofs/` folder.
