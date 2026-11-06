# Functional-analysis test (2026-11-05)

**Question:** does the functional-analysis step, with its techniques, beat no skills at
all on the same fixtures? Issue #6; design in its 2026-10-18 and 2026-10-21 handoffs.

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

**Result (2026-11-05, about $7.80, verdicts read by hand as well as judged):**

- Train on Sonnet: datum 7/8, baseline 3/8 after correcting one judge error. Validation
  on Sonnet: datum 5/6 by the judge, baseline 3/6 by the judge and 4 or 5 by hand; B2's
  datum fail came from test faults and passed 3/3 on rerun.
- Datum's clear wins are process discipline (B1, B5, B10, B12, B13). On pure analysis
  (B3, B6, B11, B14) plain Sonnet did about as well, reading a model already well
  structured. The builder's theory: discipline here pays off in synthesis and building,
  which this test does not reach.
- The judge erred in both directions; read the runs.
- **#23 not shown.** B11r passed 1/3 and B14r 0/3: with a neutral prompt all six datum
  runs grilled again, though the part already had its elicitation record and functions,
  so they never reached hazards. The first-run passes (3/3 each) came from a prompt that
  asked for hazards, and the baseline did as well there.
- Open: the step cannot tell that grilling is done; one Bash call per rerun was still
  refused; B8, a bare question, never entered datum.
