# Requirements retest (2026-11-14)

**Question:** after the fixes from #61, does the requirements step beat no skills at
all on a fresh product, and do F1-F3 of the 2026-11-13 test still pass as regression
checks? The behaviours include requirements that apply to the whole part (data kept
on restart, bad input refused). Issue #62.

**State:** fixtures only so far; the rest of the rig and the pre-registration come
next. The fresh product for the datum against baseline comparison is not here yet:
this folder so far holds the regression fixtures F1-F4.

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

## Regenerating

```sh
python3 fixtures.py                              # writes fixtures/ (not committed)
uv run ../../scripts/validate.py fixtures/F1     # and F2, F3, F4
```

Run the validator from this folder as above, or from the repository root with the
fixture's path.
