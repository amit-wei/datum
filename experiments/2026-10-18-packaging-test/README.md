# Packaging test (2026-10-18)

**Question:** should a datum technique be its own skill (S) or a reference file inside
each step skill that uses it (R)? A third variant (H, hidden skills) was dropped after
the pilot. Issue #6; background in `research/2026-10-17-skill-tiering.md` and
`research/2026-10-18-skill-descriptions.md`.

**Method:** `queries.md` holds the queries, fixtures, expected loads, the split and the
decision rule, all fixed before the runs. Part A measures what loads; Part B
(mid-run behaviour) waits for a fuller router.

| File | What it is |
|---|---|
| `source/` | The one source of every skill: `steps/` (router and steps), `techniques/`, `agents/` (per-step reviewers), `shared/` (blocks copied into every step) |
| `build.py` | Builds the variants into `variants/S` and `R`, each a plugin named `datum` |
| `fixtures.py` | Writes the fixture projects F0–F7 into `fixtures/` |
| `run.py` | Runs queries headless with `claude -p`; appends what loaded to `results/runs.jsonl` |
| `score.py` | Scores the runs against `queries.md` |

```sh
python3 build.py && python3 fixtures.py
python3 run.py --queries P3,P10 --models haiku --repeats 1   # a pilot
python3 run.py                                               # everything: costs money
python3 score.py
```

Every tool is visible to the agent, but only reading, searching, loading skills and
starting agents are approved; other calls are refused when made, since only the loads
are measured. Raw transcripts stay in the temporary
folder: they hold the runner's own setup and never enter the repository.

**Findings from the pilots** (Sonnet 5.5, 5 queries each; `results/pilot*.jsonl`):

1. **H is dead.** Claude Code refuses to load a skill with `disable-model-invocation`
   through the Skill tool, even when a step names it.
2. **Without a project CLAUDE.md, Sonnet does not enter datum mid-project.** Fixtures
   F1–F7 now carry one line telling it to load the `datum` skill.
3. **A router that allows direct answers to "questions" lets product questions skip the
   steps.** Narrowed to questions about datum itself, meaning-free edits and personal
   preferences.
4. **A technique's pointer line is enough for the agent to act on.** Steps now say a
   technique is loaded before its output is produced; questions may be answered
   directly.
5. **A Haiku judge is noise:** re-judging 10 runs three times gave differing verdicts on
   4. The builder's marks agreed with Sonnet on 8 of 10 and the two disagreements were an
   ambiguous Outcome (N5, since reworded). The judge is now Sonnet.
6. **Known failure, kept: P12.** Asked "are we done with requirements?" with a product
   budget (`REQ-B4DG`) not flowed down to the parts, every run (S and R, before and after
   the stance line on "done") checked the requirements step against its own end
   condition, found other real gaps, and missed the budget: flowdown belongs to
   synthesis, and the agent did not look past the step it was asked about. A content
   finding for the real skills, not a packaging one (issue #15).

**Result:** techniques as separate skills (S). The full run (276 runs, `results/runs.jsonl`)
and a local check in the builder's setup (`results/local-check.jsonl`) both favour S by a
small margin. Analysis, the decision and 17 lessons for writing skills:
`research/2026-10-18-packaging-test.md`. A smoke test (P3 and P10 on Haiku 5.5, one run per variant,
$0.04 in total) checked the rig end to end and found the fixture bug now fixed. In
that small sample S and H loaded no technique on their own, and R loaded the expected
ones. That is two queries and no conclusion.
