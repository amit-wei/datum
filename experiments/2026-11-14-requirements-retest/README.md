# Requirements retest (2026-11-14)

**Question:** after the fixes from #61, does the requirements step beat no skills at
all on a fresh product, and do F1-F3 of the 2026-11-13 test still pass as regression
checks? The behaviours include requirements that apply to the whole part (data kept
on restart, bad input refused). Issue #62.

**State:** fixtures F1-F4 (regression) and N1-N3 (fresh product) are here; the rest of
the rig and the pre-registration come next (`queries.md` is still a draft).

## The fixtures

F1-F4 are those of `experiments/2026-11-13-requirements-test/` (the shared-expense
splitter; see that README for what each fixture holds), brought to the schemas on
`main` as of 2026-11-14. `fixture-src/` and `fixtures.py` are copies, changed only as
below; the 2026-11-13 folder is left as the record of its experiment.

| Change on main | What changed in the fixtures | Where |
|---|---|---|
| Every function lists `inputs` and `outputs` (#63, `writing-functions`, "Inputs and outputs") | Inputs and outputs on all 11 product functions and the 2 functions of F4's child part `settlement`, taken only from the function definitions, the scenarios and the elicitation records; every flow between two functions written at both ends | `fixture-src/.../functions/`, `fixtures.py` (child part) |
| Elicitation entries may carry `constraint: true`; grilling covers four whole-part areas (#64) | `constraint: true` on ELI-5KXR#4 (phone, no data, result sent as a message), ELI-7MDP#4 (plain text for any chat app), ELI-3RQV#2 (trip size) and ELI-3RQV#3 (amount range, cents, one currency); three entries added for the areas no entry answered | `fixture-src/.../analysis/`, `fixtures.py` |
| Every requirement has a `rationale` (#65) | A rationale on each of F4's four requirements | `fixtures.py` |

ELI-5KXR#4 already answers where the part runs. ELI-5KXR#7 (one currency) is not
marked as a constraint: it carries `out_of_scope` for the wish it declines, and the
same limit is marked in ELI-3RQV#3.

### Entries written for this fixture

These were not in the 2026-11-13 records. They are written in the builder's voice,
consistent with what the builder already said, and say "none" where nothing in the
records implies more. Fresh numbers in ELI-5KXR; no entry was renumbered.

```yaml
  - n: 8
    question: Who else uses it, and does anything about the people matter, such as language, eyesight or how used to apps they are?
    answer: "Only me. The others just get the message. Nothing special about me."
  - n: 9
    question: Is there a standard or law it has to follow, such as for personal data or money?
    answer: "Not that I know of. It's only expenses between friends, on my phone."
  - n: 10
    question: Does anything matter about installing it, updating it or looking after it?
    answer: "No, nothing special. I put it on my phone myself."
```

### Validator

F1-F3: no errors, no warnings. F4: 4 errors, by design, as in 2026-11-13: the two
handed-down requirements of `settlement` carry `parent:`, which the v0.1.0 schema does
not know, so each is reported for the unknown field and for having no reason to exist.

## The fresh product (N1-N3)

A small plant-watering planner on the user's laptop. The user lists their house plants
(name, pot size, how often each likes water, inside or on the balcony) and the town they
live in. Each morning it asks an outside forecast service for the day's weather and
says which plants to water today and roughly how much; rain excuses the balcony plants.
The user logs each watering, can look back at one plant's waterings and take away a
mistyped one. `fresh-src/` holds its functional analysis.

**The builder's answers were written for this test.** ELI-YZF1 (functional analysis) and
ELI-N097 (requirements round) were written by an agent in the voice of a hobbyist with a
few dozen plants, following `grilling` for the format and the four whole-part areas
(ELI-YZF1#11-15). No real grilling took place and no builder agreed the scenarios or
functions: their status is `agreed` only so the fixture reads as a closed step.
ELI-YZF1 gives no ranges, numbers or failure responses; those are only in ELI-N097.

| Function | Name |
|---|---|
| FUN-39Z5 | Add a plant to the list |
| FUN-BY64 | Change a plant's details |
| FUN-E2EJ | Remove a plant from the list |
| FUN-M0FX | List my plants |
| FUN-SB5K | Set the home town |
| FUN-G6AB | Get today's forecast (from the forecast service) |
| FUN-N3PF | Work out which plants to water today |
| FUN-ZYDM | Show the plants to water today |
| FUN-PGV7 | Show what is not set up yet |
| FUN-QE1H | Log a watering |
| FUN-0F4C | Show a plant's watering history |
| FUN-VEWS | Remove a watering entry |

Nine scenarios (SCN-QTV4, Z7NW, 21VQ, MA9W, N7ZQ, 1YKV, HY7T, H7BK first use with nothing
set up, EYDV the forecast-service failure), two losses (LOS-ZQ68 a plant dies; LOS-0ER5 the list and log
are lost) and five hazards (HAZ-TBJC a due plant left off the list; HAZ-B91A a plant or
amount that is too much; HAZ-9YFJ a plant or watering entry removed or changed by
mistake with no way back; HAZ-DZXM a forecast that does not match the home's weather;
HAZ-5MGY the only copy of the data).

### End condition of functional-analysis, walked

| Item | Evidence |
|---|---|
| Builder agrees the set covers what they expect | Not met for real: no builder; simulated for the test (see above) |
| Every scenario step done by some function | Script over the model: every `by: product` step is in some function's `serves`, the first-use SCN-H7BK#2 by FUN-PGV7; none left over |
| Every function serves a scenario | Every function has `serves`; validator reports no unknown scenario step |
| Inputs and outputs listed; every output has a user; every function input is an output of that function | All 12 functions list both; validator checks flows at both ends (clean). The outside inputs are `user` and `forecast service`. FUN-G6AB has a second, neutral output "forecast obtained" to FUN-N3PF; FUN-0F4C takes "plant to look up" from the user; the plant-acting functions take changed and removed plant |
| Every need is in a scenario or out of scope | Script: needs ELI-YZF1#1-8, 11 and 17 are in scenarios; #16 (a reminder at 8 o'clock) is `out_of_scope` with a reason |
| Whole-part areas answered, "none" included | ELI-YZF1#12 where it runs, #13 people, #14 standards and legal ("not that I know of"), #15 installing and upkeep; #11, #12, #13 and #15 are marked `constraint: true` |
| Every function checked for hazards | Each function was considered: add, change, remove plant, log and remove watering, set town, get forecast, work out and show today's list are in the `arises_from` of a hazard; list my plants, show history and show what is not set up only repeat stored data and introduce none |
| Every loss is a file and reached by a hazard | ELI-YZF1#9 and #10 are LOS-ZQ68 and LOS-0ER5; HAZ-TBJC, B91A, DZXM reach the first, HAZ-5MGY and HAZ-9YFJ the second |
| Obligations found in inputs | None beyond the elicitation record (no parent) |
| No feasibility doubt without a spike | None: a forecast service is a lookup; no doubt recorded |
| Validator clean | `uv run scripts/validate.py experiments/2026-11-14-requirements-retest/fresh-src`: 0 errors, 0 warnings |
| Closing review by `review-functional-analysis` | Clean after three rounds (Sonnet, on N1; see "After the closing review"); the builder's agreement is simulated, and `steps.yaml` holds the placeholder commit 0000000 |

### N1-N3

Each is `fresh-src/` plus `steps.yaml` closed at 0000000, the one-line CLAUDE.md, and a
requirements-round record, ELI-N097.

| Fixture | ELI-N097 holds | Drops |
|---|---|---|
| N1 | #1-7 limits (plants at most 60; name up to 40 characters, not blank, unique; pot width 5-60 cm; water every 1-60 days; inside or balcony; town up to 60 characters; watering day today or up to a year back, once per plant per day), #8 refuse and say what is wrong, #9 about 10 ml per cm of pot width, #10 rain is 2 mm or more, #11 a plant overdue when rain is forecast is still watered, #12 forecast service failure or wrong answer, #13-17 hazard choices (#17: respond, confirm before removing, no undo), #18 a never-watered plant is first due on the day it is added | nothing |
| N2 | as N1 | #11, the overdue-and-rain rule |
| N3 | as N1 | #12, what the part does when the forecast service does not answer or answers wrongly, and #15, the choice for HAZ-DZXM (a forecast that does not match) |

Nothing else in the model states the dropped answers: the scenarios, functions and FA
record say that rain excuses balcony plants and that a forecast failure scenario exists,
but not what the part does about either, or about a plant already overdue.

### After the closing review (second commit)

The `review-functional-analysis` agent found 8 should-fix items; all applied: the
forecast-obtained output; "plant to look up"; HAZ-B91A from FUN-VEWS; the new hazard
HAZ-9YFJ with its choice (ELI-N097#17); changed and removed plant as inputs of
FUN-QE1H, FUN-BY64 and FUN-E2EJ; FUN-N3PF split into FUN-N3PF and FUN-ZYDM; the
first-use scenario SCN-H7BK with ELI-YZF1#17; `constraint: true` on ELI-YZF1#13 and #15.
Also ELI-N097#18 (all of N1-N3). Added entries, verbatim:

```yaml
# ELI-YZF1
  - n: 17
    question: What should you see the first time you open it, before you have told it anything?
    answer: "Not an empty screen or an error. Just tell me what to do first: put in my town, or add a plant."
    need: true
# ELI-N097
  - n: 17
    question: How do you want to deal with a plant or a watering entry being removed or changed by mistake (HAZ-9YFJ)?
    answer: "Respond. Show me what will be removed and ask me to confirm. No undo needed."
  - n: 18
    question: When is a plant that has never been watered first due?
    answer: "On the day I add it."
    need: true
```

Changed slot values: functions are now 12; the outputs read in a later use are as before
(the split adds the in-use flow `plants due today`, not kept). Hazard choices are #13-17.

### Validator, all fixtures

F1-F3 and N1-N3: 0 errors, 0 warnings. F4: the 4 known errors above.

## Regenerating

```sh
python3 fixtures.py                              # writes fixtures/ (not committed)
uv run ../../scripts/validate.py fixtures/F1     # and F2, F3, F4, N1, N2, N3
```

Run the validator from this folder as above, or from the repository root with the
fixture's path.

### Rounds two and three

Round two found one should-fix: whether the forecast was usable reached FUN-N3PF but
not FUN-ZYDM, which tells the user (SCN-EYDV#3). Fixed with the output "forecast used"
from FUN-N3PF to FUN-ZYDM, and FUN-ZYDM's definition and output now say whether
today's forecast went into the list. Round three: clean. Notes left standing: FUN-BY64
and FUN-E2EJ take each other's output; no backup or export function (HAZ-5MGY,
accepted in ELI-N097); the simulated agreement.
