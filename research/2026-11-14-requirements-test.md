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
