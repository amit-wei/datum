---
name: datum
description: Use when starting, resuming or steering work on a product built with datum (a datum/model/ folder of functions, requirements and parts), when the builder describes something new to build, when it is unclear which step comes next, or when it must be judged whether something is done or ready. Reads the state on disk and loads the next engine step. Not for a question about datum itself, an edit that changes no meaning, or how the builder likes to work.
---

# datum: where are we, and what comes next

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

## The model on disk

- Everything is under `datum/model/`. The product is the top part, `datum/model/product/`; every other part has
  its own folder below its parent, named in the parent's `parts.yaml`.
- A part holds `functions/`, `requirements/`, `proofs/`, `interfaces/`, `decisions/`,
  `risks/` and `analysis/` (elicitation records `ELI-`, scenarios `SCN-`, spike results
  `SPK-`, research `RES-`), one YAML file per artifact, named by its ID.
- An ID is a type prefix and 4 Crockford base32 characters (`REQ-7K3Q`). Links name IDs,
  never paths.
- `datum/model/<part>/steps.yaml` records the engine steps the builder has closed, e.g.
  `functional-analysis: {closed_at: <commit>}`.
- States a person decides: `draft`, `agreed`, `retired`. Everything else is computed.
- An increment's scope (function IDs, and deferrals with their reasons) is in the
  description of its GitHub milestone. Open questions and work are GitHub issues; they
  never mirror model state.

## What to do

1. **Act directly, loading no step, only for:** a question about datum itself or its
   terms (what EARS means), an edit that changes no meaning (a typo, a broken link
   target), or how the builder likes to work with you. Anything about the product,
   including a question ("is this all right?", "would this work?"), goes through a step,
   because the answer depends on the model's state and the step's techniques.
2. **First contact.** If the project's `CLAUDE.md` (or `AGENTS.md`) lacks the line
   "This project is built with datum. Load the `datum` skill before any work in this
   project.", offer to add it; without it, later sessions skip datum.
3. **No `datum/model/` folder** and the builder describes something to build: load the step
   `functional-analysis` for the product.
4. **Otherwise find the work.** For every part, read `steps.yaml` and compute what is
   open or stale:
   - A step is open when it is not in `steps.yaml`.
   - A step is stale when its part's files changed after its `closed_at` commit
     (`git diff --name-only <closed_at> -- datum/model/<part>/`); every later step of that
     part is then stale too, and so is every part whose files link to a changed ID.
   - Pick the highest stale or open part (closest to `datum/model/product/`), at its earliest
     such step, in the order of the map below.
5. **If the request clearly belongs elsewhere,** say so and go there: a new capability
   reopens the product's functional analysis; a value a part cannot meet goes up
   to the parent's synthesis as an issue (problems go up, changes do not).
6. **When considering whether something is done or ready,** decide it here, not inside one step:
   list every step the thing feeds, read each one's end condition from its skill, and
   check each against the model. Report what holds, what does not, and what you did
   not check.
7. **Load the step's skill** with the Skill tool (`datum:<step>`) and follow it. Tell the
   builder in one line which part and step you are in, and why.

## The map

| # | Step | Runs | Produces | Reviewer |
|---|---|---|---|---|
| 1 | `functional-analysis` | every part | functions, scenarios, losses and hazards | `review-functional-analysis` |
| 2 | `requirements` | every part | requirements and their proofs | `review-requirements` |
| 3 | `synthesis` | every part | parts, interfaces, decisions, budgets flowed down, derived requirements | `review-synthesis` |
| 4 | `design-evaluation` | every part | computed checks, scenario walk-throughs | `review-design-evaluation` |
| 5 | `cases` | every part | executable cases for the part's proofs | `review-cases` |
| – | `increment` | once per increment, after the product's cases close | the scope: functions plus deferrals | – |
| – | `build` | each leaf part in scope, once its level reaches the stopping rule | code that passes the locked cases | `review-build` |
| – | `verify` | once per increment | evidence at one commit; the release | – |

Order: every part runs the same five steps. The product runs them first, then
`increment` sets the scope, and each part in scope runs them down to the stopping rule.
A leaf part is built as soon as its own level reaches the stopping rule. `verify` runs
when every in-scope part is built.

Each step loads its own techniques; a technique's conditions may depend on the level
(scenarios are forced at product level). Steps 1–5 and `build` end in a review loop with
their reviewer agent; `increment` and `verify` close on computed checks.
The builder closes every step; you never write `steps.yaml` without their word.
