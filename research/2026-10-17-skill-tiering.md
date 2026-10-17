# Skill tiering: many small skills or few large ones (2026-10-17)

Condensed from a Sonnet research agent's report. VERIFIED means the agent read the
primary source's full relevant text (paper body, doc page, issue), not an abstract.
INFERRED means it is reasoning. 12 sources were read in full; 8 more were seen only as
search titles and are not used.

The question: a router, step skills (order of work, stance, which techniques apply when)
and 15–30 technique skills that the steps invoke by name, against fewer skills with
techniques as reference files inside them.

## Selection accuracy as the number of skills grows

- **Direct evidence (VERIFIED, arXiv 2605.24050, "More Skills, Worse Agents?").**
  SkillsBench tasks, Haiku 4.5 and Sonnet 4.6, 2,545 trajectories. Against a library
  holding only the helpful skill, libraries of 52, 102 and 202 skills lowered the pass
  rate by 0.08, 0.14 and 0.21 (confidence intervals exclude zero). Most of the drop is
  *shadowing*: the wrong skill is chosen, or none is (0.03, 0.08, 0.14). The cost of a
  bigger listing after a correct pick was not distinguishable from zero. A skill whose
  name matched the task's wording out-competed the right skill in all 26 trajectories.
  Caveats: one benchmark, two models, distractor libraries built by the authors.
- **Anthropic (VERIFIED, tool-search doc):** tool-selection accuracy "degrades once you
  exceed 30-50 available tools". No data is given for the figure.
- **Older tool studies (VERIFIED, directional only):** MetaTool (2310.03128) shows
  selection falling as candidates grow from 5 to 15, most steeply from 5 to 10, on 2023
  models. RAG-MCP (2505.03275) shows decline past about 30 tools; its text is
  inconsistent about its own setup.

## Hierarchy, and naming a skill explicitly

- **No evidence that hierarchy beats a flat set (VERIFIED).** 2607.11138: flat routing
  scored 100% on clean synthetic tasks up to 128 options; hierarchical routing scored
  0.77–1.0, with all its failures at the first routing level. Flat routing failed only
  when the catalog overflowed the context (256+). 2609.26532: hierarchy did worse than
  flat when the first level saw names without descriptions.
- **Naming a skill explicitly** appears only as an upper bound by construction. No study
  measures a skill whose text names another skill.
- **Claude Code (VERIFIED, docs):** no section on one skill invoking another.
  `disable-model-invocation: true` stops Claude invoking the skill, so a step skill could
  not call it either. `user-invocable: false` hides it from the user's menu only; Claude
  still sees it. Issue anthropics/claude-code#31505 (closed) reported that a skill
  dropped from the listing returned "Unknown skill" when called by name.

## Size of instructions

- **Instruction-following degrades with instruction count and input length (VERIFIED).**
  IFScale (2507.11538): best model 68% at 500 keyword instructions. "Same Task, More
  Tokens" (2402.14848): reasoning accuracy falls from 0.92 to 0.68 at about 3,000 tokens
  of padding, on 2023-era models.
- **Docs (VERIFIED):** SKILL.md under 500 lines; reference files cost no context until
  read; keep references one level deep. An invoked skill stays in context for the
  session; after compaction only the first 5,000 tokens of each are re-attached, 25,000
  in total, newest first.
- **No study compares one large skill with many small ones** on output quality.

## Practice with many skills

- **Listing budget (VERIFIED, docs):** every skill name is always listed; descriptions
  are dropped to fit 1% of the context window, least-used first; each entry is capped
  at 1,536 characters. `skillOverrides` can list a skill by name only. Every visible
  skill costs context on every turn.
- No primary report was found on how a public library of 20+ skills performs.

## For datum (INFERRED)

- The cost is the number of skills Claude sees, not the number of files. A router, 8
  steps and 15–30 techniques (25–40 skills) sit near the 52-skill point where the
  direct study measured a drop.
- Our risk is probably higher than the study's: its distractors were unrelated, ours
  would be close neighbours (risk techniques among themselves).
- The tiering concept does not depend on packaging. A technique can be a skill of its
  own, or a reference file inside each step that uses it, copied from one source.
- Test before choosing: 3 steps and 8 techniques built both ways, about 10 prompts each,
  recording which skill loads.
