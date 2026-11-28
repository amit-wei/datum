# Handoff

Where things stand and what is next. Rewritten each session, committed last. What was done
is in `git log`; what was agreed is in `docs/design-notes.md`.

**State (2026-11-28):** #58 is done in substance, not closed. Research is an agent,
`agents/researcher.md`, not a technique skill: it holds the agreed rules (quote the
passage, values from a paper's body, raw fetch when the tool summarises, primary source
first, failed fetches reported, stop when a primary source settles it), writes the
`RES-` record and returns its ID and conclusion. The stance and the steps call it by
forced lines (design notes, "Research"). Datum agents pin no model (design notes,
"Agent settings"). #66 now asks for a product that needs an established value, to test
whether the forced lines trigger the researcher. Nothing about the agent is tested.

**Next, in order:**
1. **Close #58** once Amit agrees, the note pointing at `agents/researcher.md`.
2. **#59 `running-a-spike`.** Agree its method and sources with Amit first. It always
   runs in a subagent, so it is likely an agent too, like the researcher.
3. **#75:** check whether an agent's frontmatter can make the reviewer run in the
   foreground; if so, use it and drop the "wait" clause from both steps.
4. **#66:** the manual run from calling datum to the end of the requirements step. It
   tests #67-#70, #33 (the reviewer's `skills:` preload) and the researcher agent.
5. Then the rest of v0.1.0: #56's lens rebuild (if #66 shows the need), synthesis
   #44-#46, design evaluation #47-#48, cases #49 and #55, build #50-#52. #53 late, by
   a fresh agent.
6. **#74, the small rerun, as late as possible:** after the fixes, before #54. #54 only
   once all of v0.1.0 is in. #40-#43 and #56 stay open, milestoned, until v0.1.0 ships.

**Watch:**
- An available skill or agent is not enough to make the main agent research (lesson 8):
  the trigger is the forced line. If #66 shows it missed, strengthen the line, not the
  description.
- The skills grew with recent fixes. Trim after v0.1.0, not now.
- One change per test is the aim, not a rule; a rerun covering several names them all.
- The evaluator still leans to the first set on close criteria; #54 reads a split as
  "no difference found".
- Rig: headless runs kill a background reviewer; `dontAsk` can deny the agents'
  `$TMPDIR` generator commands (#74 lists both).

**How to work:** before writing a skill or agent, agree its method and sources,
research them, and check the draft against the writing guide (`research/2026-10-18-stance.md`
Q3) and the lessons in `research/2026-10-18-packaging-test.md`. Work that is always done
by a subagent is an agent, not a skill. Use the fewest rules, no forcing, and no menus
of ready-made reasons. Statements say "the part". "The builder" is the datum role. When
the text means Amit, write Amit, and issues mention no one where they can. Keep the
deduper out of skill text and examples. Give each question its own context. Test-rig
mechanics are decided and done, then reported. Before a test, read lessons 8-23 and base
the rig on the latest experiment folder. Give mechanical work to a cheaper subagent.
