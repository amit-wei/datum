# Handoff

Where things stand and what is next. Rewritten each session, committed last. What was done
is in `git log`; what was agreed is in `docs/design-notes.md`.

**State (2026-11-09):** #25 and #32 are closed. "Forced" now means a technique must run
before anything else is written (P13); `losses-and-hazards` is due by the end condition
instead, and no loss or hazard may be named, proposed or ruled out without it loaded.
B11r passed 3/3 after the change. A bare question (B8) and an empty repository (B1) are
left for the developer to notice and correct; no fix planned.

**Next:** #27 (Requirements step). Write its techniques' conditions under the new P13
rule: forced only where order matters; everything else named in the end condition.

**Open for decision:** whether to build each remaining step fully, or make a thin pass
through to a small built result first. The theory that functional-analysis discipline pays
off in synthesis and building is still untested.

**Before the next test:** read lessons 8-17 in `research/2026-11-05-fa-test.md`. Base the
rig on `experiments/2026-11-05-fa-test/run.py`: it runs the agent with sandboxed Bash (#38),
so the validator and the reviewer run. The sandbox needs `bubblewrap` and `socat`.
