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
- **Then look for what is missing.** For each of these, write a function, a note that a
  requirement on an existing function covers it, or ask the builder whether it is out of
  scope:
  - first use, with nothing stored yet
  - startup and shutdown, and an interrupted run
  - each outside system failing or answering wrongly
  - bad or unexpected input
  - backup, restore, export, upgrade
  - what someone other than the main user needs: a maintainer, an admin, a neighbour part

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
other part: the parent function), and `rationale` only when the reason is not already the link.

Two examples, for illustration only:

```yaml
id: FUN-7K3Q
status: draft
name: Plan the next session
definition: |
  Proposes the next training session from the user's logged sessions and goal, for the
  user to accept or change.
serves: [SCN-4M2A#3, SCN-9TQX#2]
```

```yaml
id: FUN-H2WD
status: draft
parent: FUN-7K3Q
name: Estimate current fitness
definition: |
  Turns the logged sessions of the last weeks into an estimate of what the user can
  take now, for the planner.
```

