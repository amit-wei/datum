# Handoff

Where things stand and what is next. Rewritten each session, committed last. What was done
is in `git log`; what was agreed is in `docs/design-notes.md`.

**State (2026-11-28):** #58 and #59 are closed: research and spikes are agents,
`agents/researcher.md` and `agents/spiker.md` (design notes, "Research" and "Spikes";
evidence `research/2026-11-28-spikes.md`). The spiker keeps its code in
`analysis/spikes/<SPK-ID>/`; qualitative spikes are parked as #76. #75 is closed: no
frontmatter forces the foreground, so the steps' "wait for the findings" clause stays,
and datum does not tell builders about the fork-mode setting. **#66 is set up and Amit
is running it:** `experiments/2026-11-28-manual-run/`, a pilot's logbook (one part; the
researcher for FCL.050/FCL.060 and the IGC format, the spiker for take-off and landing
times from a track). Eight yes/no outcomes are pre-registered in its README.

**Next, in order:**
1. **Finish #66.** When Amit is back: `uv run experiments/2026-11-28-manual-run/collect.py`,
   read `results/` for anything personal, score O1-O8 from the files, write the Result
   (impressions apart), give each finding that outlives the session an issue, commit.
2. **Decide from #66** whether #56's lens rebuild is needed, and what #74 must cover.
3. Then the rest of v0.1.0: synthesis #44-#46, design evaluation #47-#48, cases #49 and
   #55, build #50-#52. #53 late, by a fresh agent.
4. **#74, the small rerun, as late as possible;** in `claude -p` runs, ask the agent to
   wait for the reviewer (#74 comment). #54 only once all of v0.1.0 is in. #40-#43 and #56
   stay open, milestoned, until v0.1.0 ships.

**Watch:**
- An available skill or agent is not enough to make the main agent use it (lesson 8):
  the trigger is the forced line. If #66 shows a miss, strengthen the line, not the
  description.
- The researcher's rules held in two runs this session (raw fetches, failed fetches
  reported, labels kept). Nothing about the spiker is tested.
- The skills grew with recent fixes. Trim after v0.1.0, not now.
- The evaluator still leans to the first set on close criteria; #54 reads a split as
  "no difference found".

**How to work:** before writing a skill or agent, agree its method and sources,
research them (the `researcher` rules work through a general-purpose subagent told to
follow `agents/researcher.md`), and check the draft against the writing guide
(`research/2026-10-18-stance.md` Q3). Work always done by a subagent is an agent. Use
the fewest rules and no menus of ready-made reasons. "The builder" is the datum role;
when the text means Amit, write Amit. Keep the deduper out of skill and agent examples.
Scripts run with `uv run`, never `python3`. Before a test, read lessons 8-23 and base
the rig on the latest experiment folder. Give mechanical work to a cheaper subagent.
