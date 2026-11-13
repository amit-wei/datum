# Handoff

Where things stand and what is next. Rewritten each session, committed last. What was done
is in `git log`; what was agreed is in `docs/design-notes.md`.

**State (2026-11-13):** Agreed: versions are a ladder of reference products (design
notes, Versions as a ladder of reference products). v0.1.0 is a thin pass: one
one-part product, a duplicate-file finder and safe deduper, taken from needs to verified
code, with each step carrying only its core techniques. Each later version gets a fresh
product; earlier ones become a regression set. This supersedes "the full default as
designed" in Rigour in v0.1.0.

**Issues:** v0.1.0 sub-issues are open, one per thing built: requirements #40-#43,
synthesis #44-#46, design evaluation #47-#48, cases #49 (new step issue; child #55),
build #50-#52, intent sheet and hidden suite #53, end-to-end test run #54 (blocked by
#53). Moved to v0.2.0: #30 increment, #31 FA gate checks, #34 work packages. #39 parked.

**Next:** #53 first: write the deduper's intent sheet and hidden acceptance suite, and
pre-register the v0.1.0 run (what it introduces, what result shows it works). Then #27's
children, with conditions under P13: forced only where order matters, everything else
named in the end condition.

**Before the next test:** read lessons 8-17 in `research/2026-11-05-fa-test.md`. Base the
rig on `experiments/2026-11-05-fa-test/run.py`: it runs the agent with sandboxed Bash (#38),
so the validator and the reviewer run. The sandbox needs `bubblewrap` and `socat`.
