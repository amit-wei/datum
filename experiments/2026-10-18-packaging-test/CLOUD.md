# Running the packaging test in a cloud session

Instructions for the agent in a Claude Code cloud session. The builder starts it from
the repository folder with one of:

```sh
claude --cloud "Follow experiments/2026-10-18-packaging-test/CLOUD.md, phase: probe"
claude --cloud "Follow experiments/2026-10-18-packaging-test/CLOUD.md, phase: full"
```

Work in `experiments/2026-10-18-packaging-test/`. Do not change any file except
`results/runs.jsonl`. Do not edit the queries, skills, fixtures or scripts, even if a
run looks wrong: report it instead.

## Phase: probe

Checks that a nested headless Claude runs here, before any real spend.

1. `claude --version`. If the command is missing, stop and report that.
2. `python3 build.py && python3 fixtures.py`
3. `python3 run.py --queries N2 --variants S --models haiku --repeats 1 --tmp /tmp/runs --out /tmp/probe.jsonl`
4. Report: the output of each command, and the first 40 lines of the transcript path it
   prints, with anything that looks like a credential removed. Commit nothing.

## Phase: full

1. `python3 build.py && python3 fixtures.py`
2. Run one query at a time, so each command finishes in a few minutes:

   ```sh
   python3 run.py --queries <ID> --models sonnet,haiku --jobs 6 --tmp /tmp/runs
   ```

   for every ID in `queries.md` (P1–P12, N1–N11), in that order. Rerun the same command
   until it prints `0 runs to do`. A command that times out or stops loses nothing:
   recorded runs are skipped on the rerun.
3. If a command prints `stopped after 3 failed runs`, wait, retry once, and if it fails
   again stop and report the failure messages: it is probably a usage limit.
4. After every few queries, commit `results/runs.jsonl` to the branch
   `packaging-test-results` and push it, so nothing is lost if the session ends.
   Commit message: `chore: packaging test results (partial)`, then
   `chore: packaging test results` when every query is done.
5. At the end, run `python3 score.py` and report its table. Do not interpret it.

The cloud setup differs from the builder's own machine: other skills are listed, and
the builder's CLAUDE.md is absent. The result is read with that in mind (see README).
