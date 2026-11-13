# Handoff

Where things stand and what is next. Rewritten each session, committed last. What was done
is in `git log`; what was agreed is in `docs/design-notes.md`.

**State (2026-11-13):** The requirements step (#27) is drafted for v0.1.0 and grounded in
sources (`research/2026-11-13-requirements.md`): `writing-requirements` (#40),
`writing-proofs` (#41), the `requirements` step (#42), the requirement and proof schemas
and validator rules (#43), and the `review-requirements` agent (#56). Positions are in
design notes, Requirements in v0.1.0. `uv run checks/skill_examples.py` validates every
skill example against its schema; run it after changing either.

**Test in progress (#60):** `experiments/2026-11-13-requirements-test/`, pre-registered
(README, `queries.md`). Every script resumes after a usage reset: rerun the same command.
Its README lists the commands in order; check `results/` for how far it got.
Stopped at the usage limit on 2026-11-13: R1 done (3+3 runs), R2 datum 2/2 and baseline
1/2. Resume with `python3 run.py --models sonnet --repeats 2 --queries R2,R3,R6,R8 --jobs 2`,
then `judge.py`, `evaluate.py`, `uv run score.py`. Notes from reading R1 run 1 by hand
(not yet findings): datum left expenses per trip `TBD` where the baseline invented 500;
datum missed input validation and keeping the trip across app restarts; datum used
"support" as an empty verb. Runs must
stay on this machine (`work/` holds the transcripts the judge reads). After results: one
rerun per failed behaviour at most, then record the result in the README and in
`research/`.

**Issues:** opened #56 (reviewer) and #60 (test run), both under #27; #57 (how requirements flow down into a
child part, v0.2.0), #58 `research` and #59 `running-a-spike` (both v0.1.0; both steps
already point to them). #55 renamed Case-author agent. Safety-profile candidates are a
comment on #5. Under the ladder rule, #40-#43 and #56 stay open until v0.1.0 ships.

**Next:** finish #60. Then every thin step gets its own test before #54 (design notes,
Versions). Then the other thin steps: #58 and #59, then synthesis #44-#46, design evaluation
#47-#48, cases #49 and #55, build #50-#52. Before writing a skill's content, agree its
method and sources with the builder, research them first, and check the draft against
the writing guide in `research/2026-10-18-stance.md`. Fewest rules: no forcing and no
rule unless leaving it out costs more. Requirement statements say "the part", never a
name. Keep the deduper out of skill text and examples. #53 (intent sheet and hidden
suite) comes late, written by a fresh agent whose output is not read in skill-design
sessions; then pre-register #54 and run it. Hazard statements say "the part" too.

**Before the next test:** read lessons 8-17 in `research/2026-11-05-fa-test.md`. Base the
rig on `experiments/2026-11-05-fa-test/run.py`: it runs the agent with sandboxed Bash (#38),
so the validator and the reviewer run. The sandbox needs `bubblewrap` and `socat`.
