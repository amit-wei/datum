---
name: writing-proofs
description: Use when a requirement has no proof yet, or its proof no longer fits after the requirement changed - to plan how it will be shown to hold, by what method and against what pass condition. Produces PRF- files. Not for the requirement itself (use writing-requirements) or the test code that carries a proof out (the cases step).
---

# Writing proofs

A proof is the plan for showing that one requirement holds: the method, and the
condition under which it passes. It is not the code that carries it out. The cases are
written later by a case author who did not write the requirements, from the proofs
alone, so a proof must be enough to write them without asking. One case may carry out
the proofs of several requirements, as one test plan covers many rows of a verification
matrix; sharing a setup is the cases' work, not the proofs'. The reviewer of the requirements step
checks the proofs against this file.

## Choosing the method

The four names are the usual ones in systems engineering; where the line between them
falls is datum's own:

| `method` | What is done |
|---|---|
| `test` | The part is run under set conditions and a program checks the result |
| `inspection` | An artifact (code, config, a document, a dependency list, a data file) is examined against the criterion |
| `analysis` | A calculation or reasoning from a model shows it holds |
| `demonstration` | A person watches it work and records what they saw |

No method is the default. In `rationale`, say what could make this requirement stop
holding, and why the chosen method notices it, with enough confidence for what the
requirement guards, at the least cost over the part's life: tests rerun on every change
and are code to keep; a person redoes a demonstration or a manual inspection at every
release. Write the reason for this requirement alone. Two proofs may give the same
reason where it is true of both; a reason that would fit any requirement is not one.

## The criterion

- **The number lives in the requirement.** `pass` and `conditions` name its measure
  and never copy the number: "plan_time meets every bound of REQ-4W8N", not "under
  2 s"; "one plant more than REQ-X allows", not "the 61st plant". A copy goes stale
  when the value changes.
- **`pass`** says what is observed and when it passes.
- **`conditions`** say the setup the result depends on: the data, its size, the state
  before, what is made to fail.
  - For an `unwanted` requirement, provoke the unwanted condition.
  - For a requirement that answers a hazard, put the part in the hazard's state, or as
    close as is safe, under the worst conditions it could meet, and show the loss does
    not follow.
  - For `analysis`, state the assumptions, the bounds the model holds within, and the
    worst case it covers.
  - Use copies and throwaway data: a proof never risks the builder's or a user's real
    data or machine.
- **A statistical criterion** (a percentile, a proportion, a rate, a judged quality)
  also gives `sample_min` (how many trials), and where a claim about the true value is
  needed, `confidence` and which `bound` it is on. A single run does not show a p95.
- **A `TBD` value or rule** does not stop the proof: the criterion refers to the
  requirement, and holds whatever it becomes.

## Rules for each proof

- **One proof covers one requirement.** A requirement gets a second proof only when no
  single method can show all of it.
- **Every requirement is covered** by at least one proof.
- **Runnable in the current increment.** If the setup it needs (a data set, a judge, a
  device) will not exist when the increment is verified, say what it waits for and open
  an issue; until then it is not evidence.
- **Checkable without asking.** Read it as the case author: could you write the case
  from it, and would two case authors agree on pass or fail? If not, sharpen it. If the
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
few words), `method`, `rationale` (why this method, as above),
`covers` (the one requirement of this part it shows), and `criterion` with `pass` and, as needed,
`conditions`, `sample_min`, `confidence` and `bound` (`lower` or `upper`).

Three examples, one per method, for illustration only.

A test, statistical:

```yaml
id: PRF-2H7B
status: draft
title: Plan time on a full season of sessions
method: test
rationale: |
  Plan time drifts as the part and the logged history grow; only a repeated run
  catches that. An analysis of the code would not predict it well enough.
covers: REQ-4W8N
criterion:
  pass: plan_time meets every bound of REQ-4W8N over the sample.
  sample_min: 200
  conditions: |
    A climber with one season (150 sessions) logged, on the slowest phone the
    part supports.
```

An analysis, where a test would take years:

```yaml
id: PRF-6RKC
status: draft
title: Ten years of daily logging fit on the phone
method: analysis
rationale: |
  A test would have to generate ten years of sessions and would still show one
  history. The size of a logged session is fixed by the data format, so a calculation
  is enough; it is redone when the format changes.
covers: REQ-5TNA
criterion:
  pass: The calculated storage after ten years meets every bound of REQ-5TNA.
  conditions: |
    Assumes the data format of the current release and two sessions a day, every day
    (worst case; a typical climber logs about four a week). Holds only while no photos
    or videos are stored with a session.
```

An inspection, of something fixed once:

```yaml
id: PRF-9WDA
status: draft
title: Session data opens without the part
method: inspection
rationale: |
  Whether the data is plain text is set once by the file format and changes only with
  it; a test rerun on every change would check what no ordinary change can break.
covers: REQ-8B4H
criterion:
  pass: |
    Every file the part writes for a climber opens in a plain text editor and
    shows each session's date, exercises and loads in words and numbers.
  conditions: The data folder of a climber with a week of sessions logged, at the release commit.
```
