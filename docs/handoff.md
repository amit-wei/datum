# Handoff

Where things stand and what is next. Rewritten each session, committed last. What was done
is in `git log`; what was agreed is in `docs/design-notes.md`.

**State (2026-11-14, second session):** #61 and its children #63-#65 are closed. The
requirements step is reworked for what applies to the whole part, and is untested. The
#62 retest is ready to run except its scripts: `experiments/2026-11-14-requirements-retest/`
holds the fresh product (a plant-watering planner, `fresh-src/`, its functional analysis
reviewed clean in three rounds), fixtures N1-N3 and F1-F4 (`fixtures.py`), and the
pre-registration `queries.md`, fixed and agreed. The 2026-11-13 rig is unchanged.

**Agreed this session (design notes, 2026-11-14):**
- A function lists its `inputs` (with `from`) and `outputs` (with `to`); a flow is
  written at both ends (validator) and every output has a user. This supersedes failure
  modes on a function: a failure-mode list is FMEA, which datum does not use
  (`research/2026-11-14-function-inputs-outputs.md`).
- `grilling` covers four whole-part areas (where it runs, the people using it, standards
  and legal, getting it into use), each answered, "none" included; `constraint: true`
  marks an entry that sets a limit.
- Requirements walk the model: each function, input, output, hazard and constraint
  entry. A rationale on every requirement (schema). One requirement per condition with
  its own response; copied checks are a proofs fault.
- Order: write, validator, reviewer loop, then one batch to the builder; afterwards the
  reviewer reruns only on requirements whose meaning changed.
- Right-sizing above a leaf (general requirement, specific faults flowed down) is a
  proposal on #57.

**Next, in order:** #62: copy `run.py`, `judge.py`, `evaluate.py`, `score.py` and
`common.py` from `experiments/2026-11-13-requirements-test/` and point them at the new
folder, its fixtures and `queries.md` (the evaluator instruction on open values is in
it); run the Haiku pilot, then the Sonnet runs as fixed; read every verdict by hand.
Then #66: the builder's manual run in a container, from calling `datum` to the end of
the requirements step. After that: #58, #59, synthesis #44-#46, design evaluation
#47-#48, cases #49 and #55, build #50-#52, each tested before #54 (run with a simulated
builder, per its comment). #53 comes late, by a fresh agent. #57 is v0.2.0. #40-#43 and
#56 stay open until v0.1.0 ships.

**Watch in #62:** the requirements skills grew (+13, +10, +4 lines) instead of
thinning; if a run shows text ignored, trim there first.

**How to work:** before writing a skill's content, agree its method and sources,
research them, check the draft against `research/2026-10-18-stance.md`. Fewest rules, no
forcing, no menus of ready-made reasons. Statements say "the part". Keep the deduper out
of skill text and examples. Before a test, read lessons 8-22 and base the rig on
`experiments/2026-11-13-requirements-test/`.
