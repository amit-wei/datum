# Handoff

Where things stand and what is next. Rewritten each session, committed last. What was done
is in `git log`; what was agreed is in `docs/design-notes.md`.

**State (2026-11-23):** #69-#73 are closed. The review loop waits for each review and
ends on the builder's batch, in both steps; functional analysis now reviews before the
builder is asked (design notes, "The review runs before the builder is asked"). The
#70 writing faults are fixed in the skill text. Test outcomes are written against what
the record holds (lesson 23). The per-criterion evaluator passed its check
(`experiments/2026-11-23-evaluator-check/`). All of #67-#70 is drafted, none tested.
Every open issue now has a parent; cross-step issues go under #6 (AGENTS.md).

**Next, in order:**
1. **#58 `research` technique, then #59 `running-a-spike`.** The requirements step and
   the stance already point at both, and neither exists, so the requirements step
   cannot be finished without them. Start each by agreeing its method and sources with
   Amit, before writing any content.
2. **#75:** check whether an agent's frontmatter can make the reviewer run in the
   foreground; if so, use it and drop the "wait" clause from both steps.
3. **#66:** the manual run from calling datum to the end of the requirements step. It
   tests #67-#70 and #33 (the reviewer's `skills:` preload) with a real builder.
4. Then the rest of v0.1.0: #56's lens rebuild (if #66 shows the need), synthesis
   #44-#46, design evaluation #47-#48, cases #49 and #55, build #50-#52. #53 late, by
   a fresh agent.
5. **#74, the small rerun, as late as possible:** after the fixes, before #54. #54 only
   once all of v0.1.0 is in. #40-#43 and #56 stay open, milestoned, until v0.1.0 ships.

**Watch:**
- The skills grew again with these fixes (lenses, gap rule, #69, #70). Trim after
  v0.1.0, not now.
- One change per test is the aim, not a rule: the inference budget is limited, so a
  rerun may cover several changes. Its README then names them all and credits none alone.
- The evaluator still leans to the first set on close criteria; #54 reads a split as
  "no difference found".
- Rig: headless runs kill a background reviewer; `dontAsk` can deny the agents'
  `$TMPDIR` generator commands (#74 lists both).

**How to work:** before writing a skill's content, agree its method and sources,
research them, and check the draft against `research/2026-10-18-stance.md`. Use the
fewest rules, no forcing, and no menus of ready-made reasons. Statements say "the part".
"The builder" is the datum role. When the text means Amit, write Amit, and issues
mention no one where they can. Keep the deduper out of skill text and examples. Give
each question its own context (the problem, the evidence, why the recommendation).
Test-rig mechanics are decided and done, then reported. Before a test, read lessons
8-23 (8-17 in `research/2026-11-05-fa-test.md`, 18-22 in
`research/2026-11-14-requirements-test.md`, 23 in the retest README) and base the rig on
the latest experiment folder. Give mechanical work to a cheaper subagent.
