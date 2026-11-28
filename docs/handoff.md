# Handoff

Where things stand and what is next. Rewritten each session, committed last. What was done
is in `git log`; what was agreed is in `docs/design-notes.md`.

**State (2026-11-28):** research and spikes are agents (`agents/researcher.md`,
`agents/spiker.md`; #58, #59 closed). #75 closed: no frontmatter forces the foreground,
the steps' wait clause stays. **#66, the manual run, is done** and recorded in
`experiments/2026-11-28-manual-run/README.md`: a pilot's logbook went to 36 functions
and 204 requirements at the product level. Researcher, four areas, waiting, sending gaps
back and the reviewer's preload worked; values without a source, and closing on a
conditional "clean", did not; the spiker was not reached. Amit's reading: v0.1.0, with
the product as the leaf, does not show the SE process, because splitting into parts is
what bounds scope. A read of all 204 requirements (the README's "Review of the
requirements") backs it: good one by one, but half infrastructure, design decided early,
and three parts visible in the set. #66 and #33 are closed.

**Next, in order:**
1. **#78, research.** Run the researcher on how SE practice bounds each level: when a
   system is split before its functions are detailed, how deep a level's functions and
   requirements go, and how a product-level MVP cut fits (increments). Primary sources
   (NASA SE Handbook logical decomposition, INCOSE, ISO/IEC/IEEE 15288, IEEE 1220).
2. **#78, grilling.** Agree with Amit when a part splits, what bounds a part, how deep
   the product level goes, and what that does to v0.1.0's scope (product as the leaf no
   longer holds; #57's flowdown then joins v0.1.0). Record it in the design notes and
   re-plan the milestone (due 2026-12-13).
3. **Apply #78** to the router, functional analysis, requirements, the reviewers and
   synthesis's split. Fold in #79 (fresh reviewer, fewer rounds) and #80 (why `TBD` is
   avoided; read the run's transcripts in `~/datum-run/` first) only if they touch the
   same text; otherwise they follow.
4. **Rerun on the logbook** with the same builder answers, so the result compares with
   #66 (36 functions, 204 requirements). Consider a simulated builder from Amit's #66
   answers: Amit expects datum to run mostly unattended. Fix `collect.py`'s scrub first.
5. Then the rest of v0.1.0 as #78 leaves it. #74 and #54 last; #81 parked.

**Watch:**
- The forced line fires for facts datum is asked about, not for values it proposes as
  its own defaults (the run's sign-in limits). #80 covers it.
- `collect.py`'s scrub replaces the user name inside an email address instead of
  removing it; the transcripts are git-ignored for that reason.
- The skills grew with recent fixes. Trim after v0.1.0, not now.
- The evaluator still leans to the first set on close criteria; #54 reads a split as
  "no difference found".

**How to work:** before writing a skill or agent, agree its method and sources,
research them (a general-purpose subagent told to follow `agents/researcher.md`), and
check the draft against the writing guide (`research/2026-10-18-stance.md` Q3). Work
always done by a subagent is an agent. Fewest rules, no menus of ready-made reasons.
"The builder" is the datum role; when the text means Amit, write Amit. Keep the deduper
out of skill and agent examples. Scripts run with `uv run`, never `python3`. Before a
test, read lessons 8-23 and base the rig on the latest experiment folder. Give
mechanical work to a cheaper subagent.
