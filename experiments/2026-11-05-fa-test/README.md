# Functional-analysis test (2026-11-05)

**Question:** does the functional-analysis step, with its techniques, beat no skills at
all on the same fixtures? Issue #6; design in its 2026-10-18 and 2026-10-21 handoffs.

**Method:** one turn per query, each fixture frozen just before the behaviour. The rig
and the queries are not built yet.

| Fixture | State |
|---|---|
| A | Empty: a new project |
| B | Product functional analysis open: needs, one loss, scenarios, no functions |
| C | As B with functions, no losses or hazards, one need in no scenario |
| D1 | Product closed through design evaluation; `suggest-engine` untouched, with two requirements that cannot both hold |
| D2 | As D1 without the conflict; `suggest-engine` grilled, functions written, no hazard of its own |

```sh
python3 fixtures.py
uv run ../../scripts/validate.py fixtures/<name>   # zero errors on B, C, D1, D2
```

D1 and D2 show warnings: requirements and interfaces have no schema until their steps
are built, so their links are not checked. `parts.yaml` is skipped silently. The
product's requirements have no proofs, though its requirements step is closed.

## Behaviours

`val` rows decide; `train` rows may be used to tune the skills. The split is about 60/40,
following `experiments/2026-10-18-packaging-test`, fixed before the first run. With so few
behaviours it guards against tuning to the test; it does not estimate a pass rate, so
compare datum and the baseline behaviour by behaviour.

| # | Split | Fixture | Should happen |
|---|---|---|---|
| 1 | train | A | Grills first at the product |
| 2 | val | D1 | Grills first at a new part |
| 3 | train | D1 | Finds the obligations from links |
| 4 | val | C | Keeps a property or interface out of `FUN-` |
| 5 | train | D1 | Raises a problem as an issue, not a workaround |
| 6 | val | C | Asked "done?", finds the uncovered need |
| 7 | train | C | Turns an ambiguous request into functions, or more grilling or research |
| 8 | train | C | Near miss: a requirements question stays out of functional analysis |
| 9 | val | C | Near miss: a synthesis question stays out of functional analysis |
| 10 | train | C | After functions, goes on to losses and hazards |
| 11 | val | D2 | A child that only inherits hazards writes no `HAZ-` |
| 12 | train | B | Unprompted, writes only functions that do a scenario step, with no mechanisms or values; extras are questions, not files |
| 13 | val | B | Invited to add what a good app should have, writes no unrequested function: proposes ideas as questions or issues, or calls grilling or research |

**Result:** none yet.
