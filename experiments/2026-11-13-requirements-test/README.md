# Requirements test (2026-11-13)

**Question:** does the thin requirements step (#27), with its techniques and reviewer,
beat no skills at all, and does it follow its own rules? Issue #60.

**Method:** one turn per query, each fixture frozen just before the behaviour. Datum
against a no-skill baseline on the behaviours a baseline can show (R1, R2, R4);
datum-only checks for the rest. A blind evaluator, told nothing about datum, compares
the two R1 requirement sets. `queries.md` holds the eight behaviours, prompts,
outcomes, runs and decision rule, all fixed before the first run.

**Product:** a shared-expense splitter, neither v0.1.0's product (the deduper, #54) nor
the climbing planner of the skill examples. Its functional analysis was written by a
Sonnet agent following datum's functional-analysis skill from two elicitation records
(`fixture-src/`; the builder's answers were written for this test). Validator clean;
the agent checked the step's end condition item by item.

| Fixture | State |
|---|---|
| F1 | Functional analysis closed (11 functions, 2 losses, 5 hazards); a requirements-round record with every value the builder cares about and their choice for each hazard |
| F2 | As F1 without the builder's rule for amounts that do not divide evenly |
| F3 | As F1 without the builder's choice for each hazard |
| F4 | As F1, the product closed through cases; its synthesis hands two requirements to a child part, `settlement`, with `parent:` links the v0.1.0 schema does not know (the validator reports 4 errors, by design) |

## Running, and resuming after a usage reset

Every script can be stopped at any point and rerun with the same command: runs,
verdicts and evaluations already recorded are skipped, and a call that fails (a usage
limit, an API error) records nothing and stops the script.

```sh
python3 build.py && python3 fixtures.py        # plugin/ and fixtures/ (not committed)
python3 run.py --models haiku --queries R1     # the pilot: checks the rig only
python3 run.py --models sonnet --repeats 3 --queries R1
python3 run.py --models sonnet --repeats 2 --queries R2,R3,R6,R8
python3 judge.py                                # judged behaviours
python3 evaluate.py                             # blind evaluation of R1 pairs
uv run score.py                                 # the table
```

`run.py` writes `results/runs.jsonl` and keeps each run's repository (transcript, final
message, files written) under `~/.cache/datum-experiments/2026-11-13-requirements-test/`
(or `$DATUM_TEST_WORK`), outside any repository. Inside this one, an agent loads the
repo's CLAUDE.md and AGENTS.md and can read this test's queries: the second pilot's
baseline did exactly that. Run folders are not committed, because transcripts hold the
runner's own setup; `judge.py` and `evaluate.py` read them, so they must run on the
machine that made the runs. Runs need `bubblewrap` and `socat`
(Linux) for the sandbox, and `uv`.

| File | What it is |
|---|---|
| `fixtures.py` | Writes F1-F4 into `fixtures/` from `fixture-src/` |
| `build.py` | Builds `plugin/`, the `datum` plugin, from the repo's skills, agents, scripts and schemas |
| `run.py` | Runs queries headless with `claude -p`, datum or baseline |
| `judge.py` | A Sonnet judge per judged behaviour and run |
| `evaluate.py` | Normalises each R1 set to a plain list, then a blind Sonnet comparison in both orders |
| `score.py` | The table, datum against the baseline, plus the mechanical checks |
| `common.py` | Shared helpers |

## Pilots (rig only)

- **Pilot 1** (`results/pilot1-rig-bug.jsonl`): `run.py` emptied each fixture's
  `steps.yaml` while setting its commit, so functional analysis looked open. Fixed.
- **Pilot 2** (`results/pilot2-inside-repo.jsonl`): run folders sat inside this
  repository; the baseline read `README.md` and `queries.md` before writing, and both
  variants loaded the repo's CLAUDE.md. Run folders moved outside the repository.
- **Pilot 3** (`results/pilot3-plugin-in-repo.jsonl`): the plugin's path still led into
  the repository, and one baseline shell call failed because the sandbox settings,
  passed as a JSON string, became a temp file that vanished with two runs in parallel.
  The plugin and a settings file are now staged beside the run folders.
- **Pilot 4** (`results/pilot4-haiku.jsonl`): clean; no path into the repository, no
  refused or failed tool call, no cap hit.

## Result (2026-11-14)

Sonnet, 16 runs, about 7 USD with the judge. `results/score-sonnet.md` is the table;
every run's final message was read by hand. Findings and lessons:
`research/2026-11-14-requirements-test.md`.

| # | Datum | Baseline | Note |
|---|---|---|---|
| R1 coverage | 3/3 | 3/3 | |
| R2 no invented rounding rule | 0/2 | 0/2 | both settle a rule the builder never gave |
| R3 hazard handling left to the builder | 0/2 | - | datum chose for every hazard but one |
| R4 a fitting reason for each method | 1/3 | 0/3 | datum's reasons are often formulaic; every datum proof is `test` |
| R5 "the part" as subject | 3/3 | - | |
| R6 stops on handed-down requirements | 2/2 | - | |
| R7 validator and reviewer run | 3/3 | - | |
| R8 bare question | 2/2 | - | `writing-requirements` not loaded in either |

By the pre-registered rule datum beats the baseline (equal on R1 and R2, one more on R4),
but the margin is one run. **The blind evaluator preferred the baseline in all three
pairs, in both orders.**

## Rerun (2026-11-14)

The one rerun the rule allows, on the changed skills (pre-registered in `queries.md`).
Seven Sonnet runs, datum only; the blind evaluation pairs them with the first baseline
runs.

| # | Datum | Note |
|---|---|---|
| R1r coverage | 3/3 | |
| R2r rounding rule not invented | 2/2 | was 0/2 |
| R3r a grounded reason for each hazard's handling | 0/2 | most hazard answers carry no rationale |
| R4r a fitting reason for each method | 2/3 | was 1/3; one run still formulaic ("a test is cheap") |

**The blind evaluator again preferred the baseline in all three pairs, in both
orders,** for the same reasons: no requirement to keep the trip when the part is closed
(none in either run read), no refusal of bad input, the expense limit left `TBD`. The
reviewer ran in 3 of 7 rerun runs: the others stopped to ask the builder their open
questions first. Recorded as it stands; see `research/2026-11-14-requirements-test.md`.

## Addendum: the judge saw only the last report (2026-11-23, #71)

`run.py` kept only a run's last result message in `final.txt`, and the judge read that
file. Six datum runs ended more than once: they reported, the background reviewer's
notice woke them, and they reported again (the fault fixed in #69). The tables above
stand as the record; these verdicts were judged on part of the run's reporting and were
not rejudged:

| Run | Verdicts | The judge saw | Could change? |
|---|---|---|---|
| R1-datum-sonnet-5ad94f | R1 pass, R4 fail | the report after review, not the main one | Unlikely: judged mostly from the files |
| R2-datum-sonnet-75ab58 | R2 fail | the report after review | Possibly: the earlier report asks who gets the extra cent, but REQ-E9PQ states the rule as settled |
| R2r-datum-sonnet-e862fc | R2r pass | the report after review | Unlikely: the earlier report also leaves the cents `TBD` |
| R3r-datum-sonnet-07ee03 | R3r fail | the report after review | Unlikely: two requirements still have no rationale |
| R1-datum-sonnet-cd9cb4, R1r-datum-sonnet-2d9da4 | four | the main report | No: the earlier message is one sentence |

At most R2 moves from 0/2 to 1/2 for datum; the conclusion above does not change. The
run transcripts are in `~/.cache/datum-experiments/2026-11-13-requirements-test/`.
Findings 1 and the rerun addendum of `research/2026-11-14-requirements-test.md` carry
dated corrections.
