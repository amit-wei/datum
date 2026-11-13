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

## Result

Not run yet.
