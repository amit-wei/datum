# Functional-analysis test (2026-11-05)

**Question:** does the functional-analysis step, with its techniques, beat no skills at
all on the same fixtures? Issue #6; agreed design below.

**Method:** one turn per query, each fixture frozen just before the behaviour.

| Fixture | State |
|---|---|
| A | Empty: a new project |
| B | Product functional analysis open: needs, one loss, scenarios, no functions |
| C | As B with functions, no losses or hazards, one need in no scenario |
| D1 | Product closed through cases; `suggest-engine` untouched, with two requirements that cannot both hold |
| D2 | As D1 without the conflict; `suggest-engine` grilled, functions written; meant to bring no hazard of its own, but the runs found some |
| D3 | As D2 with one more function, which brings a new hazard that looks like the inherited one |

```sh
python3 fixtures.py
uv run ../../scripts/validate.py fixtures/<name>   # zero errors on B, C, D1, D2, D3
```

D1, D2 and D3 show warnings: requirements and interfaces have no schema until their steps
are built, so their links are not checked. `parts.yaml` is skipped silently. The
product's requirements have no proofs, though its requirements step is closed.

`queries.md` holds the 14 behaviours, their prompts, pass criteria, split and decision
rule, all fixed before the first run. Behaviours 11 and 14 are the evidence for #23.

| File | What it is |
|---|---|
| `fixtures.py` | Writes the fixture projects into `fixtures/` |
| `build.py` | Builds `plugin/`, the `datum` plugin, from the repo's skills, agents, scripts and schemas |
| `run.py` | Runs queries headless with `claude -p`, datum or baseline; appends to `results/runs.jsonl` |
| `score.py` | Prints each behaviour for datum against the baseline |

```sh
python3 build.py && python3 fixtures.py
python3 run.py --split train --models haiku --repeats 1 --tmp DIR    # a pilot
python3 score.py
```

Baseline: the same fixture with no plugin and no CLAUDE.md line. Raw transcripts stay in
the temporary folder.

## Agreed design

Moved from the 2026-10-18 and 2026-10-21 handoffs on #6. The behaviours above replace the
earlier list.

- Variants: datum against a no-skill baseline, run once per step and reused. A stance-off
  variant runs once for the whole library, not per step.
- Baseline: same fixtures, no plugin, no CLAUDE.md line; judged on substance only. Format
  compliance is a datum-only mechanical check, not part of the comparison.
- A simulated builder can come later for one end-to-end run.
- Budget about 3-5 USD per step: mechanical checks wherever the outcome is checkable, the
  Sonnet judge only where judgement is needed; pilots on Haiku with one repeat; full 3
  repeats only on a step's final version; pilot on training queries, hold out validation.
- One query per behaviour; Haiku pilots on training; a light Sonnet check. The real
  validation is building something with datum.
- Rig based on `experiments/2026-10-18-packaging-test` (run.py, score.py, judge). Fixtures
  rebuilt on the climbing-log example, each validator-clean.

## Result

Finished 2026-11-06, about $10.80, over the $3-5 budget because of three reruns. Mostly
one run per behaviour, so this gives a direction, not a measurement. Validation and rerun
verdicts were read by hand as well as judged, from each run's final message. On the train
set only B8 and B14 were; the others rest on the judge and its stated reason.

**Datum against the baseline (Sonnet):**

| Result | Behaviours |
|---|---|
| Datum clearly better | B1, B5, B10, B12, B13, B14r |
| Datum ahead, not clean | B11r (1/3 against 0/1) |
| Tied | B2, B3, B4, B6, B7 |
| Disputed | B9 (the baseline changed nothing, but gave a firm answer) |
| Both failed | B8 |

Datum was behind on none once the test's faults were fixed. On the decision rule it beats
the baseline: 5/6 against 3/6 on validation by the judge, narrower by hand (4 or 5).

**What it shows:**
- Datum's value at this step is process discipline: it stops the agent acting early or
  overbuilding, and it keeps the work moving. Asked directly to spot something, plain
  Sonnet does about as well, reading a model already well structured. Asked only to carry
  on, the baseline stalled and never checked for hazards. The working theory is that
  discipline here pays off in synthesis and building, which this test does not reach.
- **Techniques work when loaded; loading is the weak point.** In the last rerun all four
  runs that loaded `losses-and-hazards` did the right thing, by hand: three found the new
  hazard, and one applied the cause rule to write nothing. The two that skipped it, both
  B11r, offered a wrong load estimate as a candidate hazard. B8 and Haiku's B1 are the
  same kind of miss.

**#23:** the rule (three of three on B11r and B14r) is not met. By hand B14r passed 3/3
and B11r 1/3.

**Changed by this test:** grilling is forced only when a part has no elicitation record;
the same state by another cause is not a new hazard; `closed_at` is quoted.

**Still open:** forced techniques do not always load; a bare question (B8) does not enter
datum; `writing-functions` still contradicts itself ("look for what is missing" against
"Needed"), though B12 passed; the rig still refuses compound shell commands, so no run
could run the validator itself (`score.py`'s check after the run found no errors).

**Lessons for the next step's test:**
- The judge erred in both directions: at least four wrong verdicts among the runs read. Read the runs.
- Most reruns traced to the test, not the skills: refused tools, an open step in a
  fixture, a fixture with gaps of its own, a prompt that named the behaviour. Walk each
  fixture through the step's end condition before spending on runs.
- A one-turn test stops at the first thing the agent must ask, so the fixture has to be
  clean up to the behaviour under test.
