# Requirements retest: queries (DRAFT, not yet fixed)

To be fixed before the first run, once the fresh product has passed the
functional-analysis end condition, its closing review included (FA-test lesson 8).
Issue #62.

**Fixtures:**
- **N1-N3:** the plant-watering planner (`fresh-src/`, see README): twelve functions,
  functional analysis closed (its closing review clean after three rounds), built by a Sonnet agent following datum's skills as they
  now stand. The builder's answers were written for this test.
  - N1: plus the requirements-round record ELI-N097, holding every value and choice the
    builder cares about.
  - N2: as N1 without ELI-N097#11, the rule for a plant that is overdue when rain is
    forecast.
  - N3: as N1 without ELI-N097#12, what the part does when the forecast service is
    unreachable or answers wrongly, and without #15, the choice for HAZ-DZXM, which
    would hint at it.
- **F1-F4:** the splitter, regression only (`fixtures.py`).

**A run passes a judged behaviour** when the judge (Sonnet) finds it meets the Outcome,
from the run's final message and the files it changed. Outcomes describe substance, so
a baseline run is not failed for lacking datum's formats. **Mechanical** behaviours are
computed from the run record and the files, with no judge. A row whose Fixture is
another row's ID is judged on that row's runs. Every verdict is read by hand
(lesson 13), and a pass needs the mechanism as well as the verdict (lesson 14).

**Issues:** the rig has no network (lesson 21), so a run that says an issue should be
opened (for a `TBD` or an accepted hazard) is not failed for not opening it.

**Missing functions:** a run that finds a function the analysis lacks, and raises it
for functional analysis instead of writing a requirement with no function behind it,
passes N-coverage for what that function would cover.

**Runs:**
- Pilot, to check the rig only: N1 on Haiku, datum and baseline, once each (lesson 22).
  Nothing in the skills changes on its result.
- Sonnet, fresh product: N1 three times, datum and baseline; N2 and N3 twice, datum
  and baseline.
- Sonnet, regression: G1 twice; G3, G4, G5 and G6 once each; datum only.
- The blind evaluation pairs each datum N1 run with a baseline N1 run, in both orders.
  The evaluator is told that a value left open with a question for the builder is not
  a defect, and a value stated as settled with no source is (lesson 20). The same
  instruction holds for both variants.

**Decision rule:**
- On the compared behaviours, datum beats the baseline when it passes at least as many
  runs on each and more on at least one. Behaviour by behaviour; no percentage.
- A datum-only behaviour holds when it passes in every run.
- The blind evaluation is reported with its reasons beside the table, not folded in.
- A regression row fails if a behaviour that held on 2026-11-13 no longer holds.
- **Rerun limit:** at most one rerun of each failed behaviour, then the result is
  recorded as it stands. Fixes after that get a new pre-registered test on a fresh
  fixture (Versions as a ladder).

## Fresh product (datum vs baseline)

| # | Fixture | Variants | Prompt | Expected | Outcome |
|---|---|---|---|---|---|
| N1 | N1 | datum, baseline | The functions are agreed. Write the requirements and how each one will be checked. | `requirements`, `writing-requirements`, `writing-proofs` | Every one of the twelve functions (add a plant, change a plant's details, remove a plant, list the plants, set the home town, get today's forecast, work out which plants to water today, show the plants to water today, log a watering, show a plant's watering history, remove a watering entry, show what is not set up yet) has at least one requirement about it, and each requirement has a planned check with a pass condition. |
| N1a | N1 | datum, baseline | | | Bad input: for each limit the builder gave in ELI-N097#1-7 (at most 60 plants; a plant name not blank, unique, up to 40 characters; pot width 5-60 whole cm; watering interval 1-60 whole days; inside or balcony; a town not blank, up to 60 characters; a watering day not in the future, at most a year back, once per plant per day), a requirement says what the part does with a value outside it or missing, and states the response, not only the detection. |
| N1b | N1 | datum, baseline | | | Kept on restart: the plant list (with changes and removals), the watering log (with removed entries) and the home town are still there after the part is closed and opened again, each stated by a requirement. |
| N1c | N1 | datum, baseline | | | Constraints: the forecast from an online service for the user's town (ELI-YZF1#11), running on a Linux laptop (#12), used by one person comfortable with a terminal but no programmer (#13), and installed and looked after by that person on one laptop (#15) are each a requirement, or explicitly left to design as a choice of technology. |
| N1d | N1 | datum, baseline | | | Every requirement gives a reason it is needed that fits that requirement; a missing reason, or one that only restates the requirement, fails the run. |
| N1e | N1 | datum, baseline | | | Every planned check names its kind and gives a reason for that kind that fits the requirement it checks. |
| N2 | N2 | datum, baseline | The functions are agreed. Write the requirements and how each one will be checked. | `requirements`, `writing-requirements` | Raises what the part does with a plant that is overdue when rain is forecast, and states no rule for it as settled unless it names where the rule comes from (research with its source, or a measurement); otherwise asks the builder, or leaves it open and says how it will be settled. A run that never mentions it fails. |
| N3 | N3 | datum, baseline | The functions are agreed. Write the requirements and how each one will be checked. | `requirements`, `writing-requirements` | Raises what the part does when the forecast service is unreachable or answers wrongly, and states no response as settled without the builder or a named source. A run that never mentions it fails. |
| N4 | N1 | datum | | | Mechanical: every requirement statement has "the part" as its subject. |
| N5 | N1 | datum | | | Mechanical: the run invoked the validator and the `review-requirements` agent, the reviewer before the final message, and the validator reports no errors after the run. |
| N6 | N1, N2 | datum | | | The final message asks the builder once, in one batch: every open value or rule, any disagreement with the reviewer left unsettled, and whether the requirements say what they expect. |

## Regression (splitter, datum only)

| # | Fixture | Prompt | Expected | Outcome |
|---|---|---|---|---|
| G1 | F1 | The functions are agreed. Write the requirements and how each one will be checked. | `requirements`, `writing-requirements`, `writing-proofs` | As R1r of 2026-11-13: every one of the eleven functions has at least one requirement, each with a planned check and a pass condition. |
| G2 | G1 | | | The two misses of 2026-11-13: (a) a requirement refuses a blank or duplicate name and an amount outside the builder's range (ELI-3RQV#3), with the response; (b) a requirement keeps the trip's expenses after the part is closed and opened again. |
| G3 | F2 | The functions are agreed. Write the requirements and how each one will be checked. | `requirements`, `writing-requirements` | As R2r of 2026-11-13 (uneven amounts raised, no rule stated as settled without a source). |
| G4 | F3 | The functions are agreed. Write the requirements and how each one will be checked. | `requirements`, `writing-requirements` | As R3r of 2026-11-13 (each hazard's way grounded in the record or a source, or put to the builder). |
| G5 | F4 | Carry on with settlement. | `requirements` | As R6 of 2026-11-13 (tells the builder it cannot yet work from handed-down requirements, and stops). |
| G6 | F1 | How quickly should the balances update after I add an expense? | `writing-requirements` | As R8 of 2026-11-13 (no number as settled; uses the builder's answer or asks). |
