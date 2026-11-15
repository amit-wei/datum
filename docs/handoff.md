# Handoff

Where things stand and what is next. Rewritten each session, committed last. What was done
is in `git log`; what was agreed is in `docs/design-notes.md`.

**State (2026-11-15):** #62 is half done. The rig is in
`experiments/2026-11-14-requirements-retest/` (README, "Runs"). The Haiku pilot and all
20 Sonnet runs are done (`results/runs.jsonl`, $13.15); the run folders are in
`~/.cache/datum-experiments/2026-11-14-requirements-retest/`, not in git. Not done yet:
the judge, the blind evaluation and the score. Nothing new was agreed for the design
notes.

**Next, in order:**
1. **Finish #62.** From the retest folder: `python3 judge.py`, `python3 evaluate.py`,
   `uv run score.py`. Read every verdict by hand. Mark two runs invalid for the
   review behaviours because of rig faults: N3-datum-sonnet-21f0d2 (its reviewer was
   killed) and N1-datum-sonnet-8431de (its fix patch was denied by `dontAsk`). Apply the
   rerun limit of `queries.md`. Write the result in the README and close #62 only once
   Amit agrees. Two choices for Amit are still open:
   - keeping the normaliser's "Left open" list, which goes beyond `queries.md` (README)
   - how the G rows refer to the 2026-11-13 outcomes
2. **Go through the completeness research with Amit:**
   `research/2026-11-15-functional-completeness.md`. It is incomplete: the agent hit a
   usage limit, and many sources are VERIFIED-secondary. Decide whether to finish the
   research, then decide the method for #67 (functional analysis finds every needed
   function) and #68 (the requirements step finds missing functions and sends them
   back). The main finding is that rule 15 of `2026-10-18-functions.md` dropped the
   CRUD check along with the CRUD names.
3. **New issues from the runs:** #69 (repeat the review until clean, and wait for each
   review), #70 (writing-skill faults found in every run) and #71 (recheck the
   2026-11-13 verdicts). None has a milestone yet; sort them with Amit.
4. Then as before: #66 (Amit's manual run in a container), #58, #59, synthesis #44-#46,
   design evaluation #47-#48, cases #49 and #55, build #50-#52, each tested before #54.
   #53 comes late, by a fresh agent. #57 is v0.2.0. #40-#43 and #56 stay open until
   v0.1.0 ships.

**Watch:**
- Datum writes about 40% more requirements than the baseline (mean 46 against 33),
  partly from "one requirement per condition" and the lack of child parts (#57).
- The requirements skills grew in #61. Fix #69 and #70 by trimming, not adding.
- The run agents write YAML through a generator script in `$TMPDIR`, not with
  Write or Edit. Count changes from the transcripts.

**How to work:** before writing a skill's content, agree its method and sources,
research them, and check the draft against `research/2026-10-18-stance.md`. Use the
fewest rules, no forcing, and no menus of ready-made reasons. Statements say "the part".
"The builder" is the datum role. When the text means Amit, write Amit, and issues
mention no one where they can. Keep the deduper out of skill text and examples. Before
a test, read lessons 8-22 and base the rig on the latest experiment folder. Give
mechanical work to a cheaper subagent.
