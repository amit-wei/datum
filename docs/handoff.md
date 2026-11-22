# Handoff

Where things stand and what is next. Rewritten each session, committed last. What was done
is in `git log`; what was agreed is in `docs/design-notes.md`.

**State (2026-11-22):** #62 is closed; its result is in
`experiments/2026-11-14-requirements-retest/README.md` (Result, corrected for N1c and
G4). Completeness is agreed in concept (design notes, Completeness; Going back, Gaps and
who decides) and drafted into the skills: three lenses in `writing-functions` (#67), and
the gap bullet with Class I / Class II in every stance (#68). Neither draft is tested.
#69-#73 each have a detailed comment with options, a recommendation and questions for
Amit.

**Next, in order:**
1. **Sort #69-#73 with Amit** (none has a milestone) and answer the questions in each
   issue's comment. #69 (reword Order, wait for each review; the fixture's missing
   GitHub remote kept every review not clean) and #70 (seven recurring faults, fixes
   mostly by trimming) are both skill text and fit together.
2. **#71:** rejudge 5 old verdicts (about $0.45, old judge prompt), read them, note it in
   the 2026-11-13 README. **#72** (evaluator: verdict per criterion, ties allowed,
   checked on same-set pairs first) and **#73** (outcomes mark which values the record
   gives) before the next test.
3. **Test #67 and #68** with a small rerun after #69 and #70, on few runs. It needs an
   outcome for the N1 home town (seen and corrected), which no row checked.
4. Then as before: #66, #58, #59, synthesis #44-#46, design evaluation #47-#48, cases
   #49 and #55, build #50-#52, each tested before #54. #53 late, by a fresh agent. #57 is
   v0.2.0. #40-#43 and #56 stay open until v0.1.0 ships.

**Watch:**
- The lenses and the gap rule grew both steps (68 lines in, 22 out). Keep the #69 and
  #70 fixes to trimming.
- Datum writes about 40% more requirements than the baseline (#57).
- Rig: headless runs kill a reviewer started in the background (21f0d2, G4-fbe738); the
  run agents write YAML through a generator in `$TMPDIR`, which `dontAsk` can deny.

**How to work:** before writing a skill's content, agree its method and sources,
research them, and check the draft against `research/2026-10-18-stance.md`. Use the
fewest rules, no forcing, and no menus of ready-made reasons. Statements say "the part".
"The builder" is the datum role. When the text means Amit, write Amit, and issues
mention no one where they can. Keep the deduper out of skill text and examples. Before
a test, read lessons 8-22 and base the rig on the latest experiment folder. Give
mechanical work to a cheaper subagent.
