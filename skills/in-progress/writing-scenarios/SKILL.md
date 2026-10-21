---
name: writing-scenarios
description: Use when the product's needs are drawn out and the end-to-end journeys a user or outside system goes through are not yet written, or when a need is in no journey. Produces SCN- files that the product's functions will serve. Not for checking a design against a journey (use walking-scenarios) or for the functions themselves (use writing-functions).
---

# Writing scenarios

A scenario is one end-to-end journey, from a trigger to an outcome someone cares about,
told as numbered steps. It shows what the product is used for, so that every function
can point at a use. Write scenarios for the product, before its functions.

## What to write

1. **The main journeys first:** one per thing the builder wants to get done with the
   product. Start from the needs in the elicitation records; every need lands in a
   scenario or is marked out of scope with a reason.
2. **Then the variations and failures that matter:** a different path to the same
   outcome, an input that is wrong, an outside system that is down, the user stopping
   halfway. Failure journeys are where error handling comes from; without them those
   functions go missing.
3. **Stop** when every need is covered and the builder recognises the set as how the
   product will be used. More scenarios than that is overbuilding.

Draft the set, then show it to the builder and ask whether it matches how they will use
the product. A scenario is `draft` until they agree.

## Rules for each scenario

- **One trigger, one outcome.** The trigger is what starts it ("the user finishes a
  run"); the outcome is what is true at the end ("the session is in the log").
- **Steps say what happens, never how.** "The product shows the plan", not "the API
  returns JSON to the React view".
- **Each step names who does it:** the user, an outside system, or the product. A step
  the product takes part in will be done by a function; the others need none.
- **At the level of someone using it.** One scenario is something one actor finishes in
  one sitting. "Run my training for a year" is too big; "enter a heart rate" is a step.
- **Preconditions only when they matter:** what must already be true for the journey
  to start ("at least one session is logged").

## The file

One file per scenario in `datum/model/product/analysis/`, named by its ID. Make the ID with:

```
echo "SCN-$(LC_ALL=C tr -dc '0-9A-HJKMNP-TV-Z' </dev/urandom | head -c 4)"
```

Fields: `id`, `status`, `name`, `kind` (`main`, `variation` or `failure`), `trigger`,
`preconditions` (optional), `steps` (numbered, each with `by` and `what`), `outcome`,
`needs` (the elicitation entries it covers, as `ELI-XXXX#n`). Functions point at the
steps they do as `SCN-XXXX#n`.

Two examples, for illustration only:

```yaml
id: SCN-4M2A
status: draft
name: Log a run and get the next session
kind: main
trigger: The user finishes a run.
steps:
  - {n: 1, by: user, what: Enters the run's distance, time and how hard it felt.}
  - {n: 2, by: product, what: Adds the run to the user's log.}
  - {n: 3, by: product, what: Proposes the next session.}
  - {n: 4, by: user, what: Accepts the session or changes it.}
outcome: The run is in the log and the next session is planned.
needs: [ELI-3RWN#1, ELI-3RWN#2]
```

```yaml
id: SCN-9TQX
status: draft
name: Come back after a week off
kind: variation
trigger: The user logs a run after seven or more days without one.
preconditions: At least one earlier session is logged.
steps:
  - {n: 1, by: user, what: Enters the run.}
  - {n: 2, by: product, what: Proposes a session that eases back in rather than continuing the old plan.}
outcome: The next session is one the user can safely do.
needs: [ELI-3RWN#2]
```

