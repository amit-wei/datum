# Evaluator check (2026-11-23)

**Question.** Does a blind evaluator that judges criterion by criterion, with ties
allowed, give verdicts that do not follow the order the sets are shown in? (#72)

**Why.** In the #62 retest the evaluator chose whichever set was shown as X in all three
pairs, in both orders (`../2026-11-14-requirements-retest/README.md`, Result). The
design is decided in #72 (comment of 2026-11-23): pairwise, evidence first, a verdict
per criterion (coverage, faithfulness, clarity, checks, restraint), "tie" allowed, no
overall verdict.

## Method

`check.py` makes 21 Sonnet calls through the retest's `common.ask`, on normalised sets
already recorded by the two earlier rigs (no run or normaliser call):

| Case | Sets | Calls | Expected of a fair evaluator |
|---|---|---|---|
| self | one #62 set shown as both X and Y: datum 3d98ff, baseline 4e6289, datum 9c3a2b | 3 | tie on every criterion |
| retest | the three #62 pairs, both orders | 6 | no criterion where both orders name X, or both name Y |
| known | the six 2026-11-13 pairs, both orders | 12 | the baseline wins coverage in both orders, as the old evaluator found |

The prompt keeps the retest's framing (a value left open with a question is not a
defect). The 2026-11-13 sets were normalised without a "Left open" list; that is the same
input the old evaluator saw.

**Pass, pre-registered.** The evaluator is fit for #54 when all three hold:

1. Self: at least 13 of the 15 criterion verdicts are tie, and none of the non-ties
   repeat one letter across all three self-pairs.
2. Retest: in no pair does a criterion get the same letter in both orders on 3 or more
   of the 5 criteria (a criterion where both orders agree on a *set* is fine).
3. Known: the baseline wins coverage, order-consistently, in at least 4 of the 6 pairs.

If 1 or 2 fails, move to option 2 of #72 (grade each set alone). If only 3 fails, the
evaluator has gone quiet: read the reports before deciding.

Every report is read by hand before the result is written (lesson 13).

## Result (2026-11-23)

21 calls, $2.54 (`results/evaluations.jsonl`, log in `results/check.log`). **Passes all
three conditions; fit for #54, with the lean below.**

1. **Self: pass.** 15 of 15 criterion verdicts are tie.
2. **Retest: pass.** No pair gives the same letter in both orders on more than one
   criterion (9c3a2b, checks: X in both). Order-consistent verdicts: faithfulness to
   datum in 2 of 3 pairs, clarity to datum once, checks to the baseline once; the rest
   split, so no verdict.
3. **Known: pass, at the line.** The baseline wins coverage in both orders in 4 of 6
   pairs (41c2d5, 70e989, 2d9da4, 75cb73); in the other two one order says tie. The
   reports name the same gaps the old evaluator did: no requirement that the trip
   survives a restart, no refusal of malformed input. Faithfulness goes to datum in
   both orders in 5 of 6: the baseline settles values with no source (500 expenses,
   case-insensitive names).

**Read by hand.** The reports cite items from the sets and keep the same facts across
orders; where a verdict splits, it is mostly tie in one order and a letter in the other.
VERIFIED (reports read for 3d98ff, 70e989 and the self-pairs; the rest skimmed).

**The lean that remains.** Among non-tie verdicts, X appears 45 times and Y 18. On a
close criterion the evaluator still drifts toward the first set, but the both-orders
rule turns that into no verdict, not a false win: 5 of 45 criterion pairs came out the
same letter in both orders. INFERRED: per-criterion verdicts with ties keep the lean
from deciding, without removing it. #54 should report per criterion, and read a split as
"no difference found", not as a tie.
