---
name: datum
description: Use when starting, resuming or steering work on a product built with datum (a model/ folder of functions, requirements and parts), when the builder describes something new to build, or when it is unclear which step comes next. Reads the state on disk and names the next engine step. Not for a quick edit, a question or a personal preference; handle those directly.
real: true
---

# datum: where are we, and what comes next

{{include stance}}

{{include model-on-disk}}

## What to do

1. Act directly, loading no step, only for: a question about datum itself or its terms
   (what EARS means), a typo or other edit that changes no meaning, or how the builder
   likes to work with you. Anything about the product, including a question ("is this
   all right?", "are we done?", "would this work?"), goes through a step: the answer
   depends on the model's state and the step's techniques.
2. If there is no `model/` folder and the builder describes something to build, start
   product-level functional analysis: load the step `functional-analysis`.
3. Otherwise read every `model/**/steps.yaml`. Find the highest block (closest to
   `model/product/`) with a step that is open or stale, and its earliest such step, in
   engine order: functional-analysis, requirements, synthesis, design-evaluation, then
   increment, cases, build, verify.
4. If the request clearly belongs to a different block or step, say so and go there:
   for example, a new capability at product level reopens product functional analysis.
5. Load that step's skill with the Skill tool (`datum:<step>`) and follow it.

Steps: `functional-analysis`, `requirements`, `synthesis`, `design-evaluation`,
`increment`, `cases`, `build`, `verify`.
