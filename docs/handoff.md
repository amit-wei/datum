# Handoff

Where things stand and what is next. Rewritten each session, committed last. What was done
is in `git log`; what was agreed is in `docs/design-notes.md`.

**State (2026-11-14):** The requirements step (#27) is drafted for v0.1.0 and tested
once (#60, closed): mechanics held, but the blind evaluator preferred the no-skill
baseline in 6 of 6 pairs; datum missed data kept across a restart and refusal of bad
input. Findings and lessons 18-22: `research/2026-11-14-requirements-test.md`.

**Agreed this session (design notes, 2026-11-14):**
- A rerun limit binds one test; fixes after it get a new pre-registered test on a fresh
  fixture, and old fixtures become regression checks (Versions as a ladder).
- The requirements step creates no topics: requirements trace to functions (result and
  failure modes), hazards or threats (STPA; STRIDE in synthesis), and elicited
  constraints. Values are settled with a reason (asking, research, spike), never
  invented. Missing topics go back to their step.
- Failure modes are part of a function (heavier functional analysis accepted).
- Elicitation, right-sized for every part, asks about operating environment, human
  factors, standards and legal (NASA App C.4). Security stays STRIDE in synthesis.
- Rationale on every requirement (old narrower rule superseded).
- The review runs before the builder is asked; unsettled disagreement goes to them.

**Next, in order:** #63 (`writing-functions`: failure modes on every function, and its
reviewer), #64 (elicitation looks for what applies to the whole part), #65
(requirements, writing-requirements, review-requirements made thinner). All under #61.
Then #62: test them on a fresh fixture, F1-F3 as regression only. #62's
pre-registration must count raising a missing function as a pass, and walk each fixture
through the functional-analysis end condition first (FA-test lesson 8). After that:
#58, #59, synthesis #44-#46, design evaluation #47-#48, cases #49 and #55, build
#50-#52, each tested before #54 (run with a simulated builder, per its comment). #53
comes late, by a fresh agent. #57 is v0.2.0. #40-#43 and #56 stay open until v0.1.0
ships.

**How to work:** before writing a skill's content, agree its method and sources,
research them, check the draft against `research/2026-10-18-stance.md`. Fewest rules, no
forcing, no menus of ready-made reasons. Statements say "the part". Keep the deduper out
of skill text and examples. Before a test, read lessons 8-22 and base the rig on
`experiments/2026-11-13-requirements-test/`.
