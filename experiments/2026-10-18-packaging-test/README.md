# Packaging test (2026-10-18)

**Question:** should a datum technique be its own skill (S), a reference file inside
each step skill that uses it (R), or a skill hidden from the listing that only step
skills call (H)? Issue #6; background in `research/2026-10-17-skill-tiering.md` and
`research/2026-10-18-skill-descriptions.md`.

**Method:** `queries.md` holds the queries, fixtures, expected loads, the split and the
decision rule, all fixed before the runs. Part A measures what loads; Part B
(mid-run behaviour) waits for a fuller router.

| File | What it is |
|---|---|
| `source/` | The one source of every skill: `steps/` (router and steps), `techniques/`, `agents/` (per-step reviewers), `shared/` (blocks copied into every step) |
| `build.py` | Builds the variants into `variants/S`, `R`, `H`, each a plugin named `datum` |
| `fixtures.py` | Writes the fixture projects F0–F7 into `fixtures/` |
| `run.py` | Runs queries headless with `claude -p`; appends what loaded to `results/runs.jsonl` |
| `score.py` | Scores the runs against `queries.md` |

```sh
python3 build.py && python3 fixtures.py
python3 run.py --queries P3,P10 --models haiku --repeats 1   # a pilot
python3 run.py                                               # everything: costs money
python3 score.py
```

Runs may read, search, load skills and start agents; writing, shell and web are
denied, since only the loads are measured. Raw transcripts stay in the temporary
folder: they hold the runner's own setup and never enter the repository.

**Result:** not run yet. A smoke test (P3 and P10 on Haiku 5.5, one run per variant,
$0.04 in total) checked the rig end to end and found the fixture bug now fixed. In
that small sample S and H loaded no technique on their own, and R loaded the expected
ones. That is two queries and no conclusion.
