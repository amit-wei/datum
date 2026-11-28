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
what bounds scope. #66 is not closed yet: ask Amit.

**Next, in order:**
1. **#78: when a product splits into parts, what bounds a part, and how datum handles
   the split.** The run's main finding. Grill Amit on it; the answer may change
   v0.1.0's scope and the order below. Read #57 and #34 with it.
2. **#79:** fresh reviewer per round with fewer rounds; agree the method first.
3. **#80:** why the requirements step avoids `TBD`; read the run's transcripts (kept
   only in `~/datum-run/`, not in git) before fixing.
4. Then the rest of v0.1.0 as #78 leaves it: synthesis #44-#46, design evaluation
   #47-#48, cases #49 and #55, build #50-#52, #53 late. #74 as late as possible; #54
   last. #81 (a spiker test) is parked.

**Watch:**
- The forced line fires for facts datum is asked about, not for values it proposes as
  its own defaults (the run's sign-in limits). #80 covers it.
- `collect.py`'s scrub replaces the user name inside an email address instead of
  removing it; the transcripts are git-ignored for that reason. Fix before the next run
  that keeps transcripts.
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
