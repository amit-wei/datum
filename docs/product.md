# Product level: the library

The library's own product level, applied lightly: the spine only. Not a model; the
model format does not exist yet. Started 2026-10-14.

## Intake

Condensed from the builder, 2026-10-14.

| # | Intake |
|---|---|
| I1 | Turn an AI workflow into a systems engineering workflow for a single developer: solid, rapid, well-conventioned, no slop |
| I2 | Model and code agree. The model may run ahead of the code if it says so |
| I3 | Layers are complete for their scope: the product layer wide, deeper layers per increment |
| I4 | Stack-agnostic. Conventions are an output; the input is "what do you want to do" |
| I5 | Claude Code first, portable formats |
| I6 | Skills as building blocks; preset workflows first, custom workflows later |
| I7 | Fast enough for rapid small client projects, deep enough for Pendentive |
| I8 | Rigour tailored to risk tolerance in a structured, traceable way; later, compliance profiles for real standards |
| I9 | Attractive, explorable views of the model |
| I10 | Open source; the builder first |
| I11 | The builder's review is structured (not necessarily minimised) |
| I12 | Decomposition follows rules: how to decompose and when to stop is not each agent's call |
| I13 | Adopt into existing codebases (brownfield) — in scope, later |

## Functions (draft)

| # | Function |
|---|---|
| F1 | Capture intake with its source |
| F2 | Elicit and analyse: grill, research, turn intake into functions and requirements at a level |
| F3 | Analyse risk on functions and on architecture |
| F4 | Synthesise: decompose into building blocks by rule, trade studies, decisions, allocation, derived requirements |
| F5 | Evaluate the design against the requirements |
| F6 | Plan verification (proofs) |
| F7 | Scope increments: what is built next, and how deep |
| F8 | Implement: hand bounded, traced work to AI implementers, independent of the proofs, under the conventions decided in synthesis |
| F9 | Verify: run cases, compute verdicts, keep evidence |
| F10 | Keep model and code consistent: links, drift, stale evidence |
| F11 | Keep the engineering record: decisions, open questions, supersession |
| F12 | Tailor rigour (profiles) |
| F13 | Present the model: views, structured review |
| F14 | Review independently: AI reviewers, apart from the author, check coherence of model and code |
| F15 | Sequence the work: run preset or custom workflows, know where the work stands, gate transitions |
| F16 | Adopt an existing codebase (later) |

## Naming

- Building blocks, unbounded depth (arc42). C4 kinds (container, component) optional.
- Verification levels use ISTQB names derived from tree position: component,
  component integration, system, system integration, acceptance. Combined with the
  method or "proof": "component test", "system demonstration", "integration proof".

## Open at this level

- Decomposition and stopping rules (I12): the criteria.
- Requirements for each function: not started.
