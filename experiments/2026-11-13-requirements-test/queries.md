# Requirements test: queries

Fixed before the first run. Fixtures are in `README.md`.

**A run passes a judged behaviour** when the judge (Sonnet) finds it meets the Outcome,
from the run's final message and the files it changed. Outcomes describe substance, so
a baseline run is not failed for lacking datum's formats. **Mechanical** behaviours are
computed from the run record and the files, with no judge. A row whose Fixture is
another row's ID is judged on that row's runs.

**Runs:**
- Pilot, to check the rig only (refused commands, turn and budget caps; lesson 12): R1 on
  Haiku, datum and baseline, once each. Nothing in the skills changes on its result.
- Then Sonnet: R1 three times and R2 twice, datum and baseline; R3, R6 and R8 twice,
  datum only.
- The blind evaluation (`evaluate.py`) pairs each datum R1 run with a baseline R1 run,
  in both orders.

**Decision rule:**
- On the compared behaviours (R1, R2, R4), datum beats the baseline when it passes at
  least as many runs on each and more on at least one. Behaviour by behaviour; no
  percentage (lesson 15).
- A datum-only behaviour holds when it passes in every run.
- The blind evaluation is reported with its reasons beside the table, not folded into it.
- **Rerun limit:** after a fix, at most one rerun of each failed behaviour, then the
  result is recorded as it stands.

| # | Fixture | Variants | Prompt | Expected | Outcome |
|---|---|---|---|---|---|
| R1 | F1 | datum, baseline | The functions are agreed. Write the requirements and how each one will be checked. | `requirements`, `writing-requirements`, `writing-proofs` | Every one of the eleven functions (start a trip, record an expense, split evenly, split by exact amounts, report a mismatch between shares and total, delete an expense, work out who owes whom, show who owes whom, list the recorded expenses, propose the fewest settling transfers, write the settlement as a message) has at least one requirement about it, and each requirement has a planned check with a pass condition. |
| R2 | F2 | datum, baseline | The functions are agreed. Write the requirements and how each one will be checked. | `requirements`, `writing-requirements` | Raises how to split an amount that does not divide evenly, and states no rounding rule or number for it as settled: asks the builder, or leaves it open (TBD) and says the builder must settle it. A run that never mentions uneven amounts fails. |
| R3 | F3 | datum | The functions are agreed. Write the requirements and how each one will be checked. | `requirements`, `writing-requirements` | Asks the builder how they want the hazards dealt with (for example prevent, respond or accept) before settling it, or writes the requirements that answer hazards only as proposals for the builder to choose from. Does not present one way of dealing with each hazard as decided. |
| R4 | R1 | datum, baseline | | | Every planned check names its kind (test, inspection, analysis, demonstration or similar) and gives a reason for that kind that fits the requirement it checks. A check with no reason, or a generic one ("to verify the requirement"), fails the run. |
| R5 | R1 | datum | | | Mechanical: every requirement statement written has "the part" as its subject. |
| R6 | F4 | datum | Carry on with settlement. | `requirements` | Tells the builder that it cannot yet work from the requirements handed down to settlement by its parent, and stops. Writes no requirement or proof for settlement, and does not edit or delete REQ-HV7N or REQ-0R3S. |
| R7 | R1 | datum | | | Mechanical: the run invoked the validator and the `review-requirements` agent, and the validator reports no errors after the run. |
| R8 | F1 | datum | How quickly should the balances update after I add an expense? | `writing-requirements` | Gives no number as settled and writes none to the project. Uses the builder's answer that no speed matters to them, or asks the builder. |

## Rerun (pre-registered 2026-11-14, before any rerun)

After the first runs the skills changed (`research/2026-11-14-requirements-test.md`):
"no invented values or rules", with examples; hazard handling settled like any value,
by the builder or a method, with its reason; no ready-made reasons in the method table;
two more unwanted-behaviour examples; one proof per requirement. **R3 is retired:** the
design changed, so its outcome no longer says what datum should do; R3r replaces it.
These rows are evidence on changed skills, not a held-out check. Datum only, Sonnet:
R1r three times, R2r and R3r twice. The blind evaluation pairs each R1r run with a
baseline R1 run (`python3 evaluate.py --datum-query R1r`). This is the one rerun the
rule allows; the result is recorded as it stands.

| # | Fixture | Variants | Prompt | Expected | Outcome |
|---|---|---|---|---|---|
| R1r | F1 | datum | The functions are agreed. Write the requirements and how each one will be checked. | `requirements`, `writing-requirements`, `writing-proofs` | Every one of the eleven functions (start a trip, record an expense, split evenly, split by exact amounts, report a mismatch between shares and total, delete an expense, work out who owes whom, show who owes whom, list the recorded expenses, propose the fewest settling transfers, write the settlement as a message) has at least one requirement about it, and each requirement has a planned check with a pass condition. |
| R2r | F2 | datum | The functions are agreed. Write the requirements and how each one will be checked. | `requirements`, `writing-requirements` | Raises how to split an amount that does not divide evenly, and states no rounding rule for it as settled unless it names where the rule comes from (research with its source, or a measurement): otherwise asks the builder, or leaves it open (TBD) and says how it will be settled. A run that never mentions uneven amounts fails. |
| R3r | F3 | datum | The functions are agreed. Write the requirements and how each one will be checked. | `requirements`, `writing-requirements` | For each hazard, the way it is dealt with (prevented, responded to or accepted) comes with a reason grounded in the record or in a named source, or is put to the builder. A way chosen with no reason, or a reason that would fit any hazard, fails the run. |
| R4r | R1r | datum | | | Every planned check names its kind (test, inspection, analysis, demonstration or similar) and gives a reason for that kind that fits the requirement it checks. A check with no reason, or a generic one ("to verify the requirement"), fails the run. |
