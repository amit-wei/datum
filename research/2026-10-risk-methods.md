# Risk methods for software: STPA, FMEA, threat modelling, tailoring (2026-10-14)

Condensed from a Sonnet research agent's report. **Mostly INFERRED** (the agent's
knowledge of the standards; the STPA handbook PDF was unreadable). VERIFIED items rest
on abstracts or snippets.

## STPA (Leveson)

- **Steps.**
  1. Losses, hazards and system constraints.
  2. The control structure: controllers, control actions, feedback.
  3. Unsafe control actions (UCAs) of four types: not provided, provided, wrong timing
     or order, stopped too soon or applied too long.
  4. Loss scenarios: why each UCA happens.
- **Trace chain:** loss → hazard → UCA → constraint → scenario → requirement.
- **Fit:** works top-down without a detailed design. It targets requirement, design and
  interaction flaws, not component failures, which suits software.
- **Applied to ML and LLM agents** (V, abstracts):
  - frontier AI (arXiv 2506.01782)
  - ML controllers (2502.07974)
  - safe tool use for LLM agents, with STPA turned into enforceable specs on data flows
    and tool sequences (2601.08012)
  - STPA done by ChatGPT (2304.01246)
- LLMs widen the search for hazards, but a human must validate the result.

## Software FMEA

- **Variants:**
  - functional (early, no design needed)
  - interface (per interface, with guidewords: omission, commission, value, timing,
    sequence, corruption)
  - detailed (per module; costly, worth it only for small critical code)
- **Weaknesses for software:**
  - Faults are systematic, not random wear-out.
  - It looks at single faults, so it misses interactions (the gap STPA fills).
  - Occurrence ratings mean little for design faults.
- **RPN is criticised** (V, practitioner sources):
  - Multiplying ordinal scales is unsound, and equal RPNs can hide very different risks.
  - AIAG-VDA 2019 replaced RPN with Action Priority: severity first, then occurrence,
    then detection.

## Security and privacy

- **STRIDE** per element and trust boundary on a data-flow diagram. This is an
  architecture-level pass.
- **Attack trees** for a few high-value assets (critical profile only).
- **LINDDUN** for privacy, only when personal data is present.
- **The OWASP four-question frame:**
  - What are we working on?
  - What can go wrong?
  - What are we going to do about it?
  - Did we do a good job?
- **OWASP Top 10 for Agentic Applications 2026** (V, published 2025-12-09). Confirmed
  entries include goal hijack, supply chain, memory/context poisoning, inter-agent
  communication, cascading failures, human–agent trust exploitation and rogue agents.

## Tailoring in the standards

What scales across DO-178C (DAL A–E: 71, 69, 62 and 26 objectives for A to D, none for
E), ISO 26262 (ASIL), IEC 62304 (classes A–C) and ECSS (a tailoring record):

- which analyses are mandatory
- depth
- independence of review
- strictness of traceability
- test and coverage strength

The method stays the same. The entry and exit criteria change.

## The agent's recommendation

| Engine step | Technique |
|---|---|
| Functional analysis | Losses, hazards, system constraints (STPA step 1) |
| Risk on functions | Guidewords (omission, commission, wrong value, wrong timing; for AI functions, hallucination and over-agency), STPA UCAs on the control structure, a pre-mortem |
| Requirements | Constraints and UCAs become requirements tagged with their source hazard or UCA |
| Synthesis | Risk-driven architecture (Fairbanks) |
| Risk on the architecture | STPA loss scenarios, interface FMEA with guidewords, STRIDE per trust boundary, OWASP LLM and agentic checklists, LINDDUN if personal data |
| Design evaluation | Every hazard and threat is mitigated or has its residual risk explicitly accepted; a risk-based test plan |

**How a mitigation works:**

- It eliminates the hazard by architecture, adds a safeguard or monitor, or adds a test
  or review.
- It creates a requirement linked to its source.
- Derived requirements go back to the hazard log, as in DO-178C.

**Profiles:**

1. **Prototype:** written losses and hazards, a pre-mortem, a check of secrets and
   prompt-injection exposure, no formal trace.
2. **Product (default):**
   - guidewords on key functions
   - UCA table
   - trace IDs
   - STRIDE on trust boundaries
   - for LLM features, the agentic checklist and a human gate on destructive tools
   - a risk-based test plan
3. **Critical:**
   - full STPA with a hazard log
   - interface FMEA
   - attack trees
   - LINDDUN if personal data is present
   - bidirectional trace
   - independent review
   - mandatory evidence for each mitigation

**Notes:**

- Prioritise severity first, never by RPN.
- The depth knob: scenarios per UCA, the set of guidewords, and the strictness of trace
  and review.
- LLM output on hazards is a proposal until it is validated.
