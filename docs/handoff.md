# Handoff

Where things stand and what is next. Rewritten each session, committed last. What was done
is in `git log`; what was agreed is in `docs/design-notes.md`.

**State (2026-11-14):** The requirements step (#27) is drafted for v0.1.0 and tested.
Skills: `writing-requirements` (#40), `writing-proofs` (#41), `requirements` (#42),
schemas and validator rules (#43), `review-requirements` (#56). Positions: design notes,
Requirements in v0.1.0 (several revised 2026-11-14: a proof covers one requirement and
cases share; no invented values or rules; hazard handling settled like any value; no
ready-made reasons). `uv run checks/skill_examples.py` checks skill examples against
schemas.

**Test (#60), done:** `experiments/2026-11-13-requirements-test/`, findings and lessons
18-22 in `research/2026-11-14-requirements-test.md`. Datum's mechanics hold, but the
blind evaluator preferred the no-skill baseline in 6 of 6 pairs: datum misses what holds
across the whole part (data kept on restart, bad input refused). The rerun limit is
used; fixes after it get a new test (#62, on a fresh fixture).

**Issues:** #61 (requirements that apply to the whole part) is grilled; positions in
design notes 2026-11-14: the requirements step creates no topics, failure modes are part
of a function, elicitation looks for what applies to the whole part, rationale on every
requirement, review before the builder is asked. Its sub-issues #63 (writing-functions
failure modes), #64 (elicitation), #65 (requirements thinner) are next. #62 tests them on
a fresh fixture. #54 has a comment: run it with a simulated builder. #57 (flowdown,
v0.2.0), #58 `research` and #59 `running-a-spike` open. Under the ladder rule, #40-#43
and #56 stay open until v0.1.0 ships.

**Next:** #63-#65, then test them (#62), then the other thin steps (#58, #59, synthesis
#44-#46, design evaluation #47-#48, cases #49 and #55, build #50-#52), each tested
before #54. Before writing a skill's content, agree its method and sources, research
them, and check the draft against `research/2026-10-18-stance.md`. Fewest rules, no
forcing, no menus of ready-made reasons. Statements say "the part". Keep the deduper out
of skill text and examples. #53 comes late, written by a fresh agent; then pre-register
#54 and run it.

**Before the next test:** read lessons 8-22 (`research/2026-11-05-fa-test.md`,
`research/2026-11-14-requirements-test.md`). Base the rig on
`experiments/2026-11-13-requirements-test/`: run folders outside the repository,
judging and evaluation as separate resumable scripts. Pilot the rig first.
