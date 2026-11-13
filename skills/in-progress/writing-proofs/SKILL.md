---
name: writing-proofs
description: Use when a requirement has no proof yet, or its proof no longer fits after the requirement changed - to plan how it will be shown to hold, by what method and against what pass condition. Produces PRF- files. Not for the requirement itself (use writing-requirements) or the test code that carries a proof out (the cases step).
---

# Writing proofs

A proof is the plan for showing that requirements hold: the method, and the condition
under which they pass. It is not the test code. The cases are written later by an agent
that did not write the requirements, from the proof alone, so a proof must be enough to
write them without asking. The reviewer of the requirements step checks the proofs
against this file.

## Choosing the method

| `method` | What is done | Use when |
|---|---|---|
| `test` | The part is run under set conditions and the result is checked by a program | The default. Anything a script can provoke and observe |
| `inspection` | An artifact (code, config, a document, a dependency list) is examined against the criterion | The requirement is about what the product is or contains, not what it does |
| `analysis` | A calculation or reasoning from a model shows it holds | Running it is impossible or too costly: worst cases, rare conditions, long durations |
| `demonstration` | A person watches it work and records what they saw | Only a person can judge it, and no proxy can be measured |

Prefer `test`. Every other method needs a `rationale` saying why not a test: manual
proofs are redone at every release, so a demonstration that could be a scripted test is
a cost paid again and again.

## The criterion

- **`pass`** says what is observed and when it passes. It names the requirement's
  measure and never copies its number: "plan_time meets every bound of REQ-4W8N", not
  "under 2 s". The number lives in one place.
- **`conditions`** say the setup the result depends on: the data, its size, the state
  before, what is made to fail. A test of an `unwanted` requirement provokes the
  unwanted condition; a proof of a requirement that answers a hazard puts the part in
  the hazard's state, or as close as is safe, and shows the loss does not follow.
- **A statistical criterion** (a percentile, a proportion, a rate, a judged quality)
  also gives `sample_min` (how many trials), and where a claim about the true value is
  needed, `confidence` and which `bound` it is on. A single run does not show a p95.
- **A `TBD` value** does not stop the proof: the criterion refers to the measure, and
  holds whatever value it gets.

## Rules for each proof

- **One requirement, one proof, by default.** A proof covers several only when one run
  under the same conditions checks them all. A proof that covers half a part's
  requirements has stopped being a plan.
- **Every requirement is covered** by at least one proof.
- **Checkable without asking.** Read it as the case author: could you write the test
  from it, and would two authors agree on pass or fail? If not, sharpen it. If the
  requirement itself is the problem, rewrite the requirement first, with
  `writing-requirements` loaded.
- **About the requirement, not the code.** Name what is observed from outside the
  part, not functions, files or classes; the code does not exist yet.

## The file

One file per proof in the part's `proofs/` folder, named by its ID. Make the ID with a
fresh suffix and check that no file already uses it:

```
echo "PRF-$(LC_ALL=C tr -dc '0-9A-HJKMNP-TV-Z' </dev/urandom | head -c 4)"
```

Fields: `id`, `status` (`draft` until the builder agrees), `title` (what is shown, in a
few words), `method`, `covers` (requirements of this part), and `criterion` with `pass`
and, as needed, `conditions`, `sample_min`, `confidence` and `bound` (`lower` or
`upper`); `rationale` when the method is not `test`.

Two examples, for illustration only:

```yaml
id: PRF-2H7B
status: draft
title: Plan time on a full season of sessions
method: test
covers: [REQ-4W8N]
criterion:
  pass: plan_time meets every bound of REQ-4W8N over the sample.
  sample_min: 200
  conditions: |
    A climber with one season (150 sessions) logged, on the slowest machine the
    product supports.
```

```yaml
id: PRF-8M3E
status: draft
title: No heavier session after logged pain
method: test
covers: [REQ-9C2T]
criterion:
  pass: |
    No proposed session has a higher load than the last logged session.
  conditions: |
    The last session is logged with pain. Repeated for each kind of session the
    planner can propose, and for a last session at the lowest and the highest load.
```
