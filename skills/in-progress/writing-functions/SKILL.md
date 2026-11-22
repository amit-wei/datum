---
name: writing-functions
description: Use when the things a part must do are not yet written or have to change - at the product from its scenarios, in any other part from the parent functions it contributes to - or when it is unclear whether something is a function at all. Produces FUN- files. Not for what must hold for a function, such as speed or limits (use writing-requirements), or for splitting a part into parts (use synthesis).
---

# Writing functions

A function is something a part does, written as a verb and its object, independent of
how it is done: "log a session", not "save a row to SQLite". The reviewer of the
functional-analysis step checks the functions against this file.

## Where functions come from

- **The product:** walk every scenario step by step, the failure paths included. For
  each step the product takes part in, name what the product does there. One function
  may serve several scenarios; a step done wholly by an outsider needs no function.
- **Any other part:** for each parent function the part `contributes_to`, ask what this
  part must do so that the parent function is done. Write each answer with
  `parent: <that FUN>`.
- **Then read the set through three lenses** to find what is missing. Each lens is
  something to build from the model, with questions to answer while you build it. A
  gap found here is not yet a function: every function must still pass the **Needed**
  rule.
  1. **Scenarios.** Walk each scenario again as each person who uses or looks after the
     part: the main user, and anyone else (a maintainer, an admin, a neighbour part).
     At each step, ask: which function does it, and what does this person need here
     that no step gives?
  2. **Data.** Build a table with one row per item the builder gives or the part keeps,
     read off the functions' inputs and outputs. Columns: who gives it, and the
     function that lets the builder see it, change it and remove it. For each empty
     cell, ask: does the builder need this, or did they choose to leave it out? A
     cell is filled by a function named for its goal ("correct the home town"), never
     by the operation.
  3. **Events.** Build a list of everything the part must answer: each scenario
     trigger, each timed event ("each morning"), and each event from outside, such as
     first use with nothing stored, a move to another machine, an upgrade, or an
     outside service that fails or answers wrongly. Beside each, the function that
     responds; where there is none, ask what should happen.

  The flows are checked too: an output nobody uses, or an input no one gives (see
  below). Show the data table and the event list to the builder when they go through
  the functions; neither is written to the model.

  At the product, settle each gap with the builder: a scenario step (add it with
  `writing-scenarios`, then write the function that does it), a requirement on an
  existing function, or out of scope. In any other part, write a function only when a
  parent function cannot be done without it; otherwise raise the gap as an issue on the
  parent part.

## What is a function and what is not

| It is written as | It is really | Put it in |
|---|---|---|
| "responds within 200 ms", "runs offline", "never loses data" | a property of a function | a requirement on that function |
| "receive a query", "give the plan to the user" | something crossing a boundary | an interface (synthesis) |
| "event bus", "store in SQLite", "cache results" | a mechanism | a decision in synthesis, or below the stopping rule |
| "prevent accidental deletion", "guard the budget" | a guard against a harm | a requirement on the function it guards |
| "create / read / update / delete a note" | operations, not goals | the goals behind them: "capture a thought", "correct a note" |
| "provide", "support", "handle", "manage", "ensure" + noun | an empty verb hiding the real act | say what is actually done |
| "show usage statistics" that no scenario or parent asks for | overbuilding | nothing; if it seems useful, an issue |

A guard is a function only when it gives the user something to do, such as "restore a
deleted note"; it then serves a failure scenario. Changes the part makes to its own
state are acts like any other: "archive old sessions" is a function.

## Rules for each function

- **What, not how.** If it would stop being true when the technology changed, it is a
  mechanism.
- **Seen from outside.** Someone watching the part could see it being done. If not, it
  is a property or something inside a lower part.
- **One act.** A name with "and", or longer than about ten words, is usually two
  functions.
- **At its level.** Ask "why is this done?": the answer is the scenario or the parent
  function. Ask "how?": the answer belongs to a lower part's functions, not here.
- **Needed.** Remove it and see whether a scenario step or a parent function loses its
  doer. If nothing does, delete it, or ask the builder.
- **No values.** No numbers, units or "shall" in the definition; those are requirements.

## Inputs and outputs

Each function lists what it takes and what it gives. The requirements step works from
these lists: each input's valid range and what happens outside it, and each output's
users, to find what must be kept when the part is closed.

- **An item is a thing someone would name:** "an expense", "the trip's people". Say
  what it holds when the name does not. No type, format or storage: those are
  synthesis.
- **An input says where it comes `from`:** a function of this part, by its ID, or who or
  what outside the part gives it, by the name the scenarios or interfaces use.
- **An output says who it goes `to`:** the functions of this part that take it, by ID,
  and anyone or anything outside the part that receives it.
- **A flow is written at both ends.** An input from a function is an output of that
  function, and the other way round. The validator checks this.
- **Every output has a user.** An output nobody uses is overbuilding, or a sign of a
  missing function. An input that nothing gives is a missing function or a missing
  output.
- **Name the data the part keeps for later as an output**, going to the functions that
  read it later: "a logged session", to the function that plans from it. Whether it
  must survive the part being closed is a question for the requirements step.

A function with no inputs or no outputs leaves that list empty, such as "show the help
page", which takes nothing.

There is no single right set. Two people decompose the same parent differently; check
the set by coverage and by these rules, not against an expected answer. If two
decompositions would lead to different parts, that choice is a decision for synthesis.

## The file

One file per function in the part's `functions/` folder, named by its ID. Make the ID
with a fresh suffix and check that no file already uses it:

```
echo "FUN-$(LC_ALL=C tr -dc '0-9A-HJKMNP-TV-Z' </dev/urandom | head -c 4)"
```

Fields: `id`, `status` (`draft` until the builder agrees), `name` (the verb and object),
`definition` (one or two sentences: what is done, for whom, with what result),
`serves` (the product: the scenario steps it does, as `SCN-XXXX#n`) or `parent` (any
other part: the parent function), `inputs` and `outputs` (each item a `name`, an
optional `holds`, and `from` or `to`; either list may be `[]`), and `rationale` only
when the reason is not already the link.

Three examples, for illustration only. The first two are product functions joined by a
flow; the third is in a part below the product.

```yaml
id: FUN-5DGR
status: draft
name: Log a session
definition: |
  Records a training session the climber has done, so later plans start from it.
serves: [SCN-4M2A#1]
inputs:
  - name: session done
    holds: the date, each exercise with its load, and any pain felt
    from: climber
outputs:
  - name: logged session
    to: [FUN-7K3Q]
```

```yaml
id: FUN-7K3Q
status: draft
name: Plan the next session
definition: |
  Proposes the next training session from the user's logged sessions and goal, for the
  user to accept or change.
serves: [SCN-4M2A#3, SCN-9TQX#2]
inputs:
  - name: logged session
    from: FUN-5DGR
  - name: goal
    holds: the grade or route the climber is training for
    from: climber
outputs:
  - name: proposed session
    holds: each exercise and its load
    to: [climber]
```

```yaml
id: FUN-H2WD
status: draft
parent: FUN-7K3Q
name: Estimate current fitness
definition: |
  Turns the logged sessions of the last weeks into an estimate of what the user can
  take now, for the planner.
inputs:
  - name: logged sessions of the last weeks
    from: logbook
outputs:
  - name: fitness estimate
    to: [planner]
```

