# Packaging test: technique as skill or as reference file (2026-10-18)

The test and its raw results are in `experiments/2026-10-18-packaging-test/` (queries,
fixtures and the decision rule in `queries.md`; runs in `results/`). VERIFIED means seen
in these runs; INFERRED means our reading of them.

**Question** (#6): should a datum technique be its own skill (S), or a reference file
inside each step skill that uses it (R)? A third variant, a hidden skill only steps call
(H), was dropped in the first pilot.

**Method:** the same skill text built both ways (router, 8 steps, 18 techniques; 3 steps
and 8 techniques with real bodies), 23 queries on 8 fixture projects, 12 that should
trigger a step or technique and 11 near-misses. A run is correct when a Sonnet judge
finds it meets the query's pre-written Outcome, every new model file follows loading a
technique that makes it, and nothing under Must not is attempted. Five pilots on Sonnet
tuned the rig; the full run was 276 runs (S and R, Sonnet 5.5 and Haiku 5.5, 3 repeats)
in a cloud session, about $27.

## Result

| Variant | Model | Validation (decides) | Training | Expected loads |
|---|---|---|---|---|
| S | Sonnet | 14/27 | 36/42 | 26/69 |
| R | Sonnet | 9/27 | 32/42 | 31/69 |
| S | Haiku | 11/27 | 26/42 | 26/69 |
| R | Haiku | 8/27 | 30/42 | 31/69 |

- S wins on validation on both models, as the decision rule asks. VERIFIED.
- Five of the nine validation queries were flawed by the test's design (see lessons 11,
  12 and 13): P2, N3, N6, N9, and P1 among the training ones. On the four clean
  validation queries plus N2 (P4, P8, P11, N2, N8), S still leads: Sonnet 9/15 against
  7/15, Haiku 9/15 against 6/15. VERIFIED; the margin is small.
- The cloud session did not list the builder's other skills. Locally, S lists 58
  skills and may overflow the listing budget. A local check of the five clean
  validation queries on Sonnet, one run each: see Decision.

## Decision

**Techniques are separate skills (S).** In the builder's own setup (58 skills listed in
S), the five clean validation queries on Sonnet, once each, gave S 3/5 and R 2/5
(`results/local-check.jsonl`; one unreadable verdict re-judged). VERIFIED. The full
listing did not cost S its lead, so the listing budget is not shown to bite at this
size. INFERRED. S is also the simpler packaging: one file per technique, no copies to
keep in sync.

The evidence is weak: a small margin on few clean queries. If the number of skills
grows well past this test's 27, or a later test shows shadowing between close
neighbours, revisit with this rig.

## Lessons for writing datum's skills

These matter beyond packaging; every skill datum ships should respect them.

**Getting into datum at all**

1. **Without a project-level instruction, Sonnet does not enter datum mid-project.** It
   reads the model files and answers directly. One line in the project's CLAUDE.md ("This
   project is built with datum. Load the `datum` skill before any work in this
   project.") made the router load in every later run. VERIFIED (pilots 1 and 2).
   Datum's setup must write that line. INFERRED.
2. **On an empty repository there is no such line**, and in the cloud Sonnet did not
   load datum for a new-product request in any of 6 runs (P1), while locally it had.
   The first contact needs its own trigger: the router's description, or the builder
   invoking `/datum`. VERIFIED for the runs; the cause is INFERRED.
3. **A skill with `disable-model-invocation: true` cannot be loaded by the agent at
   all**, even when another skill names it; Claude Code tells the agent to ask the user
   to run it. VERIFIED (pilot 1).

**Inside the router and the steps**

4. **Every escape hatch is taken.** "Answer a question directly" let every product
   question skip the steps. The router now names the only exceptions (a question about
   datum itself, an edit that changes no meaning, how the builder likes to work).
   VERIFIED (pilots 2 and 3).
5. **A technique's pointer line is treated as the technique.** With its description in
   the step, the agent applied it from that line and never loaded the body. A rule "load
   a technique before producing its output" raised loading. VERIFIED (pilots 2–4).
6. **Loading a technique does not make a run correct.** R loaded the expected
   techniques more often than S yet had fewer correct outcomes. VERIFIED. The skill text
   and how the step frames the work decide more than packaging. INFERRED.
7. **Agents stay inside the step they are asked about.** Asked "are we done with
   requirements?" with a product budget not flowed down to the parts, no run in the
   pilots or the full run found it: they checked the requirements step's own end
   condition, and flowdown is synthesis's. A stance line that "done" means an end
   condition holds did not fix it. VERIFIED (P12; issue #15). A question about "done"
   must check every end condition the thing feeds. INFERRED.
8. **Agents answer conventions and definitions from memory.** Asked the best way to
   define training load, every run (0/12) gave a definition without research, though
   the research technique names "an established convention or definition". They did
   hedge on prices that change (N11, mostly correct). VERIFIED. Research needs a
   forced condition, not only a description. INFERRED.
9. **"Ask, do not decide" works for values that are the builder's.** Pinning down a
   function, data retention and a RAM figure mostly led to questions before writing.
   Some runs wrote the value first and asked afterwards (P11). VERIFIED.
10. **Placeholder text is obeyed, or not, unpredictably.** A stub step that said "say
    how you would apply this, then stop" made R stop and S ignore it (N3, N6). Never
    ship placeholder instructions in a skill. VERIFIED.

**Testing skills**

11. **A fixture must match the premise of the expected answer.** P2 expected scenarios
    to be written; the fixture already had them, and the agent was right. VERIFIED.
12. **A prompt must not be ambiguous.** "This part" in a model with three parts was
    rightly answered with a question (N9). VERIFIED.
13. **Stubs on the path of a query measure the stub.** See lesson 10. VERIFIED.
14. **Removing tools changes the choice.** With no web tool visible, the agent answered
    from memory instead of loading research. Keep tools visible and refuse them when
    called. VERIFIED (pilots 1 and 2).
15. **A Haiku judge is noise.** Re-judging 10 runs three times gave differing verdicts
    on 4; a Sonnet judge agreed with the builder on 8 of 10, and the 2 disagreements
    came from an ambiguous Outcome. Outcomes must be unambiguous. The judge also
    returned unreadable output once in about 290 calls; re-judge those. VERIFIED.
16. **Pilot on training queries only.** Tuning skill text after pilots on validation
    queries contaminated three of them, which were swapped. VERIFIED (our error).
17. **Plan the way results leave a cloud session.** Without the GitHub app connected, a
    cloud session gets a bundle and cannot push; results were copied out as base64.
    Nested `claude -p` runs draw on the plan's 5-hour window first, then credit.
    VERIFIED.
