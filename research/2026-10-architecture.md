# Architecture practice and SE applied to software (2026-10-14)

Condensed from a Sonnet research agent's report. **Mostly INFERRED** (the agent's
recall of the standards and books; clause details need checking before citing). It
fetched four primary pages: Spec Kit `spec-driven.md`, boringtechnology.club, and the Kiro specs docs (V).

## How SE-rigour domains layer software

- **Automotive SPICE.**
  - System side: SYS.2 system requirements → SYS.3 system architecture, which allocates to HW and SW.
  - Software side: SWE.1 software requirements → SWE.2 software architecture → SWE.3 detailed design and units.
  - The V pairs each with a test level: SWE.4 to SWE.6, SYS.4 to SYS.5.
  - Bidirectional traceability at every level. The architecture records its rationale and the alternatives considered.
- **DO-178C.**
  - Chain: system requirements → high-level requirements (HLR) → software architecture → low-level requirements (LLR) → code.
  - **Derived requirements** come from design choices, not from a parent. They need justification and are fed back to the system safety assessment.
- **ECSS-E-ST-40C:** SRS → architecture design document (top-level, then detailed). The PDR baselines the architecture.
- **IEC 62304:** requirements → architecture (software items, interfaces, third-party software as first-class) → units. Rigour scales by safety class.
- **ISO 15288 / 12207:** architecture definition with viewpoints, alternatives, rationale, allocation and trace.
- **Common pattern:** requirements, then an explicit architecture with its rationale, then derived requirements fed back up, then allocation, then verification at each level. The standards do not say *how* to choose the architecture.

## How architects decide

- **Fairbanks, risk-driven.** Identify and rank risks → apply a technique that reduces the top risks → evaluate → repeat. Architecture is "just enough" when the top risks are mitigated.
- **Quality-attribute scenarios and utility trees** (ATAM).
  - A scenario is: source, stimulus, artifact, environment, response, measure.
  - The leaves rated (high importance, high difficulty) are the architecturally significant requirements (ASRs).
- **ASR test:** "would the design change significantly if this changed?"
- **C4 (Simon Brown):** context, containers, components, code. Just enough up-front design for a shared vision, with decisions recorded in ADRs.
- **ADD 3.0 (SEI).**
  - Drivers → iteration goal → elements to refine → design concepts (patterns, tactics, **technologies**) → instantiate and allocate → views and decisions → analyse → repeat.
  - The stack is an output.
- **Evolutionary architecture:** fitness functions are automated checks that an architectural characteristic still holds.

## Styles for solo and small teams

- **Modular monolith** is the usual default.
- **Hexagonal boundaries** go around volatile or external I/O. They give testable ports, which suits AI agents.
- **Layered** suits simple CRUD.
- **Event-driven** only when the requirements force it.
- **Pipes and filters** for data transformation.
- **Microservices** rarely make sense for a solo developer.

## Stack selection

- **Boring technology / innovation tokens** (V): a small budget of unusual choices.
- Tech radar rings; weighted decision matrices with sensitivity analysis; an ADR for each choice.
- Spec Kit, Kiro and BMAD take the stack as human input or a constitution. None derives it from requirements with criteria and recorded alternatives. That is a gap.

## Walking skeleton and tracer bullet

- **Walking skeleton (Cockburn):** a thin end-to-end implementation linking the main components.
- **Tracer bullet (Hunt and Thomas):** production-quality code that is kept, unlike a throwaway prototype.
- It acts like an engineering development unit. It verifies the riskiest architectural assumptions, settles TBDs, and feeds derived requirements back up.

## The agent's proposed procedure

From "product requirements complete" to "architecture and stack recorded":

1. Drivers.
2. Functional analysis, technology-free.
3. ASRs as measurable scenarios, ranked.
4. Risk list, plus a depth rule: no more architecture than the top risks need.
5. Choice of style, as an ADR with at least two alternatives, with functions allocated to modules.
6. Stack choice per decision area, using criteria, a boring default, "what the builder knows" and an innovation-token budget, each as an ADR.
7. Allocation, plus derived requirements fed back up.
8. Interfaces and contracts, a verification method per requirement, and fitness functions.
9. A walking skeleton on the real stack, including CI and deploy.
10. Update the ADRs from the skeleton and baseline the architecture (an informal PDR), then implement block by block.

**Open points it raised:**
- a maximum number of requirements per layer
- whether the skeleton comes before the lower-level requirements (its recommendation: before, for anything touching a top-3 risk)
- which decisions need a human gate
