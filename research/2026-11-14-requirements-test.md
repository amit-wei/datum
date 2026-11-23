# Requirements test: findings and lessons (2026-11-14)

The test of the thin requirements step (#60), pre-registered in
`experiments/2026-11-13-requirements-test/`. Sixteen Sonnet runs on a shared-expense
splitter, datum against a no-skill baseline, plus a blind evaluator. VERIFIED means seen
in the runs (final messages and files read by hand, not only the judge's verdict);
INFERRED means a reading of the cause.

## Result

| # | Datum | Baseline |
|---|---|---|
| R1 coverage of every function | 3/3 | 3/3 |
| R2 no invented rounding rule | 0/2 | 0/2 |
| R3 hazard handling left to the builder | 0/2 | - |
| R4 a fitting reason for each method | 1/3 | 0/3 |
| R5 "the part" as subject | 3/3 | - |
| R6 stops on handed-down requirements | 2/2 | - |
| R7 validator and reviewer run | 3/3 | - |
| R8 bare question answered from the record | 2/2 | - |

By the pre-registered rule datum beats the baseline, by one run on R4. The blind
evaluator preferred the baseline in all three pairs, in both orders. Datum cost about
three times as much per run (about 0.65 against 0.21 USD).

## Findings

1. **Datum invents a rule when the missing value is not a number.** In both R2 runs
   datum wrote a rounding rule (shares differ by at most a cent, leftover cents spread
   one each) as settled, with no question and no `TBD`. VERIFIED. The rule in
   `writing-requirements` speaks of "a number"; a rounding policy is a choice, not a
   number, so the rule did not fire. INFERRED. The baseline did the same.
   *Corrected 2026-11-23 (#71):* the judge and this reading saw only each run's last
   report. R2-datum-sonnet-75ab58's earlier report asks "which person gets the extra
   cent?" and says it left that unspecified, so that run did ask, though REQ-E9PQ still
   states the rule as settled. VERIFIED (transcript). The verdict was not rejudged.
2. **Datum decides how a hazard is dealt with.** In both R3 runs datum wrote prevent
   requirements for four hazards and asked about one (deleting by mistake). VERIFIED. The
   technique says the builder chooses and the agent offers the forms; the step lists
   `grilling` for "whether a hazard is answered or accepted". Neither held when the
   record was silent and writing was under way. INFERRED.
3. **Method reasons are present but formulaic.** Every datum proof in R1 has a
   rationale and every one is `test`; the judge passed one run of three, finding reasons
   such as "later code can break it unnoticed" repeated across proofs. VERIFIED. That
   phrase is the `test` row of the technique's method table, copied rather than reasoned.
   INFERRED. The baseline gives no reasons at all.
4. **The blind evaluator's reasons, consistent across all six reports.** VERIFIED (the
   reports in `results/evaluations.jsonl`):
   - *Against datum:* requirements split so finely that several carry an identical,
     copied check; a missing requirement to keep the trip when the app is closed and
     reopened; no refusal of bad input (blank or duplicate names, amounts out of range)
     in most runs; one value left `TBD` (expenses per trip), so the set cannot be
     built as it stands; the case of a payer not among the people picked left open.
   - *Against the baseline:* invented values (500 expenses, a minimum of 2 names,
     distinct names) and design constraints (no floating point, no stored balances).
   - *For datum:* tighter faithfulness to the record, concrete property-based checks.
5. **Keeping data across a restart and refusing bad input are both unwanted behaviour,**
   the third question asked of each function. Datum asked it and still missed them in
   most runs. INFERRED: the question's examples (bad input, a missing input, an outside
   system failing, an interrupted run) do not name "the part is closed or restarted",
   and nothing prompts input limits from the builder's ranges.
6. **The handed-down stop, the subject rule and the review loop work.** R6, R5 and R7
   held in every run; R6 runs also listed real gaps without acting on them. VERIFIED.
7. **R8 passed without the technique.** Both runs answered from the record, but neither
   loaded `writing-requirements` (lesson 14 of the functional-analysis test). VERIFIED.

## Lessons for testing a step

18. **Keep run folders outside the repository.** Inside it, an agent loads the repo's
    CLAUDE.md and AGENTS.md, and the baseline read the test's own queries before
    writing (pilot 2). VERIFIED.
19. **Agents write files through Bash heredocs,** not only Write and Edit, so a check
    built on tool calls (the write check, the subject check) must read the files from
    git. VERIFIED.
20. **A one-turn test penalises an honest `TBD`.** The evaluator is told the team cannot
    ask the authors, so a value left open reads as a defect, while in datum the `TBD`
    goes to the builder and comes back answered. A multi-turn run with a simulated
    builder would measure the process datum actually has. INFERRED.
21. **The rig cannot open issues** (no network in the sandbox), so "every `TBD` has an
    issue" cannot be met in a run. VERIFIED (R3, one run).
22. **Pilot on the rig, every time.** Three of four pilots found a rig fault (an emptied
    `steps.yaml`, the leak, a vanishing settings file); none would have shown as a skill
    failure. VERIFIED.

## Addendum: the rerun (2026-11-14)

On the changed skills, datum only, the one rerun allowed. VERIFIED unless marked.

- **Fixed:** no rounding rule invented (R2r 2/2, was 0/2); method reasons better (R4r
  2/3, was 1/3), with one run still formulaic ("a test is cheap").
- **Not fixed: a reason for each hazard's handling** (R3r 0/2). Most hazard-answering
  requirements carry no rationale. The hazard section asks for one, but the rationale
  rule lists only a measure and a chosen response, so the two rules disagree. INFERRED;
  the writing guide warns that contradictions are resolved arbitrarily.
- **Not fixed: keeping data across a restart.** No rerun requirement covers it, though
  the unwanted-behaviour question now names "being closed or restarted". Both runs read
  the accepted hazard (the trip is lost with the phone, no backups) as covering it.
  INFERRED. *Corrected 2026-11-23 (#71):* this holds for the two R1r runs only. Two
  other rerun runs wrote one: R2r-datum-sonnet-e862fc REQ-BF0P and
  R3r-datum-sonnet-8f7db2 REQ-2M5M. VERIFIED (run files).
- **The reviewer ran in 3 of 7 runs** (3 of 3 before). The others stopped to put their
  open values to the builder first, planning to review after. INFERRED: "settle it or
  ask" moved the stopping point ahead of the review.
- **Blind evaluation: the baseline again in all three pairs, both orders,** for the same
  reasons as before: persistence, input refusal, the open expense limit. Across both
  rounds datum lost 6 of 6 pairs.

**Reading.** Datum's mechanics hold: coverage, the subject rule, the handed-down stop,
the review loop when it runs, no invented values once the rule names rules. What a
reader of the requirements values most, a set that misses no ordinary software behaviour
(data kept, bad input refused), datum does worse than no skill at all. Its three
questions find what each function must do, not what any software product must do.
INFERRED.
