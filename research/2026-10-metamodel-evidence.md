# Evidence for and against a meta-model as the spine (2026-10-14)

Condensed from a Sonnet research agent's report. VERIFIED means the agent saw the
source (often only an abstract or a search snippet). INFERRED means it is the agent's
reasoning. Only the Fowler article was read in full. The 2026 arXiv items come from
search snippets.

## Traceability ROI

- **Mäder & Egyed** (EMSE 2015, 71 subjects): traceability gave about 24% faster
  maintenance and about 50% more correct solutions (V,
  https://dl.gi.de/items/690677a5-bbad-45af-8843-2380ea5ee92f/full).
  - Caveat: the subjects were students and the links were curated. It shows that good
    links help, not that keeping them current pays.
- **Links decay** when refactoring breaks the mapping. Links with no defined consumer
  cost maintenance and add little (V, SoK 2026, https://arxiv.org/pdf/2603.16208).
  Maintaining links by hand takes effort, and the links end up incomplete (V,
  https://arxiv.org/pdf/2306.10972).
- No clean cost-benefit study was found.

## MDE and MBSE

- **Hutchinson, Whittle & Rouncefield** (ICSE 2011; IEEE Software 2014: 450
  practitioners, 22 interviews). Organisational and social factors decide success more
  than technical ones. MDE is used for key parts of a system, rarely for whole systems (V).
- **MBSE barriers:** tools, knowledge, culture, cost. The advice is to focus on purpose
  and start small (V, secondary).

## Lightweight models in practice

- **ADRs:**
  - They helped documentation culture, and where they were stored mattered (V,
    Chalmers).
  - About 50% of repos with ADRs hold only 1 to 5 of them (V).
  - ICSA 2026 (921 repos): about 63% of ADRs are created already marked accepted, so
    the deliberation is skipped. Correlations with code quality are small (V).
- No studies were found on arc42, C4, Doorstop, StrictDoc or OFT, or on solo developers.

## LLM-specific

- **Böckeler on martinfowler.com** (V, read in full):
  - "very skeptical that lots of up-front spec design is a good idea"
  - Spec Kit output was verbose. Kiro turned a bug fix into 16 acceptance criteria.
  - Agents ignored the spec and recreated existing classes.
  - "rather review code than all these markdown files"
  - "the downsides of both MDD and LLMs"
- **ETH AGENTS.md study:** context files gave no improvement or a small reduction in
  success, and raised cost by more than 20%. Keep requirements minimal (V,
  https://arxiv.org/pdf/2602.11988).
- **Google:** asking agents to state pre-conditions, post-conditions and undefined
  behaviour before generating tests gave +9.8 points bug detection and +2.5 points
  branch coverage (V, https://arxiv.org/pdf/2608.17177).
- **No study shows that specs improve end-to-end code outcomes** (the SANER 2026
  registered report has no results yet).
- **Test gaming** (V): ImpossibleBench, SpecBench, EvilGenie, METR. These benchmarks are
  built to elicit hacking, so real-world rates may be lower.

## Verdict

**Supported with conditions. "Built first" is the weak part.**

Design constraints the evidence implies:

1. Small model. Start with 3 to 4 types and add types only when a skill needs them.
2. Grow the model alongside the first skill and the first real project. Do not finish
   it first.
3. Every artifact type and link has a named consumer (a check or a skill), or it is
   dropped.
4. Automate link creation and checking. Derive links from code and tests where possible.
5. Budget the requirement count and the context cost.
6. Terse artifacts that are cheap to review.
7. Tests independent of the implementing agent. Flag edits to test files.
8. A release valve: the validator warns in early states, and a draft is cheap.
9. Justify traceability by maintenance and change-impact queries, not by completeness.
