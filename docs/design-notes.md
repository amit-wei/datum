# Design notes

Working record of the design grilling for this library. Positions here are **not
final**; each carries its state. Research summaries are in `research/`.

Started 2026-10-14.

## Thesis

Systems engineering was skipped in software because it was slow. With AI implementers
it becomes the enabler of speed: if every requirement is justified, verified by a test,
and allocated to a coherent architecture, implementation is well-chunked work that AI
can do fast with little oversight. Human review moves upstream, from code to the model.

**Slop** is code patched together from desired features with no cohesive spine.

**The failure mode to avoid** is the opposite: Pendentive, after about a month, held about 620 system
requirements, 177 interface rows, 198 decisions, 117 open questions, and no code.

## Positions

| # | Position | State |
|---|---|---|
| P1 | Audience: the builder first; later solo devs; later small teams | agreed |
| P2 | Claude Code first; the method in portable formats (Agent Skills, AGENTS.md, plain files); hooks and subagents as a Claude-specific enforcement layer | agreed |
| P3 | Stack-agnostic. Stack, toolchain and conventions are an **output** of the workflow (a synthesis decision), not an input. The input is "what do you want to do" | agreed |
| P4 | The model may contain what the code does not have yet, if its state says so. Model and code agree for built items | agreed in concept |
| P5 | Independent verification: tests derived from requirements before implementation; the implementer cannot weaken them | agreed in concept |
| P6 | Each level runs the full SE engine, **including synthesis** (architecture), before the next level is derived | agreed |
| P7 | A layer is completed for its scope. The product layer's scope is the whole product; deeper layers are scoped to the current increment | leaning; needs practice to raise confidence |
| P8 | Requirements and architecture co-evolve within a level (Twin Peaks). No architecture in requirement text; architecture lives in decisions and the architecture description | leaning |
| P9 | The meta-model (artifact types, links, states, validator) is the spine of the library; skills are operations on it. Evidence: supported with conditions, but **not built first in full** — grow it with the first skill and real project; every type and link needs a named consumer (`research/2026-10-metamodel-evidence.md`) | leaning |
| P10 | One canonical workflow first; custom composition after it is proven on a real project | agreed |
| P11 | Autonomy deferred; gates are explicit so they can be loosened later | leaning |

## The level engine (draft, under discussion)

The same procedure at every level (the recursive SE process of MIL-STD-499B / IEEE 1220).
Corrected 2026-10-14: functional analysis comes before this level's requirements.

**Input to a level:** the requirements and constraints allocated to this block by the
level above. At product level: the needs and the builder's constraints.

1. **Functional analysis.** What this block must do to meet its inputs, and the flows
   between functions. Infeasible or conflicting inputs go back up (requirements loop).
2. **Requirements.** For each function, requirements that state it is attained and how
   well; plus the constraints flowed down. Each with a verification method and a
   pass/fail criterion (the verifiability gate).
3. **Synthesis.** Choose the parts that perform the functions. Allocate functions and
   requirements to parts, define the interfaces between parts, record each choice as a
   decision with the alternatives considered (the trade study). Choices create
   **derived requirements**, justified by their decision rather than by a parent.
4. **Design evaluation** (not "verification", which is the right side of the V). Check
   the synthesis against the requirements: every requirement allocated, key requirements
   walked through the parts as runtime scenarios. A failure changes the architecture or
   renegotiates a requirement (a recorded decision). Loop to 1–3 until it holds.

**Output:** each part with its allocated requirements, the input to its next level.

**Decomposition and stopping (draft, agreed in principle):**
- Decompose a block when it has more than one reason to change, when its requirements
  need parts with different technologies or dependency rules, or to isolate a
  high-severity risk.
- Stop when a block carries one function (plus residual functions from scrapped
  items) and is built or bought as one thing; when its requirements can be verified by
  component tests alone; when splitting adds no new interface. (Hardware practice: one
  function, one physical component, bought or made as one. Software: a module built as
  one unit, or a third-party dependency bought as one.)

## Verification (draft)

- Verification happens at the level where something is built. A requirement at level N
  is verified by (a) its children being verified, plus (b) level-N cases that cover only
  what the children cannot: interfaces, interaction, emergent behaviour.
- Validation ("the right thing") also applies at every level, scoped to that level: the
  feel of one UI element is validated low down.
- Methods: Inspection, Analysis, Demonstration, Test (standard in aerospace SE; EASA
  means-of-compliance codes are a finer taxonomy). An AI eval is a Test with a
  statistical criterion: dataset as the test article, judge as the instrument (to be
  calibrated), threshold with confidence as the criterion.
- Experience requirements are verifiable like any other: observable proxy + judge +
  threshold. Choosing the proxy is a decision.
- Proposed structure (vocabulary leaning: **method / proof / case / evidence**):
  - *method*: the category (Inspection, Analysis, Demonstration, Test). A field, not a row.
  - *proof*: one planned verification row: method, criterion, the requirements it
    covers (many-to-many lives here), status. Its level comes from where it sits in
    the tree and gives its software name (unit, integration, system, acceptance).
  - *case*: an executable piece (test function, eval run, scan script, checklist)
    that names the proof it implements (the "tag").
  - *evidence*: the result of running a proof's cases at a commit.
  - Verdicts are computed: requirement → proofs (declared on the proof) → cases
    (declared in the code) → results.

## Risk in the engine (draft)

Risk appears twice per level, as in ARP4761: a functional hazard pass after functional
analysis (generates safety requirements), and an architectural pass after synthesis
(FMEA on parts and interfaces, STRIDE for security; generates derived requirements).

## Types (draft, under discussion)

- System model: function (agreed type), requirement, part, interface, risk, means of
  compliance.
- Engineering record (about the work, not the system): decision, open question. Whether
  these are "types" in the same sense is open.
- Intake: what exists before it becomes a function or requirement (asks, constraints,
  findings). "Need" is not a type; the form of intake is open.

## Independent review (open, deliberately undesigned)

Agreed: reviews at each engine step. Also wanted: specialised reviews (a risk
assessment, a set of interfaces), reviews at different scopes (big picture vs detail).
Open: can reviewers spawn research agents; how findings are structured. To be designed
from first principles, not inherited from Pendentive.

## Approach (2026-10-14)

Do not model the library rigorously: a model of the modelling toolset, made before we
know how we want to make models, binds us implicitly. `docs/product.md` stays at intake
and functions.

## Ideas parked

- **Compliance profiles.** Tailoring profiles that map to real standards (ASPICE,
  DO-178C, IEC 62304) and produce the evidence those standards ask for.

- **Visualisation as a consumer of the model.** Diagrams are generated views, not
  artifacts: an interactive (possibly 3D) map of containers and interfaces, hover for
  detail, click to drill into components. Requires the model to hold containment,
  interfaces and allocation.
- **Measuring the thesis.** Key metric: whether compartmentalisation lowers AI
  implementation cost and time while staying accurate. No parallel control runs (solo
  builder). At most passive telemetry the workflow logs anyway.

## Open questions

| # | Question |
|---|---|
| Q-1 | What exactly is an increment, and how big is it? Depends on what kind of thing the library is |
| Q-2 | When is each verification artifact written: the criterion with the requirement; the executable test after the level's external interface is defined? |
| Q-3 | Skill granularity. Research (`research/2026-10-skill-granularity.md`) points to ~10–15 activity-scale skills, a few atomic user-only commands, rules in references and validator scripts, state on disk, gates enforced by hooks. Awaiting the builder |
| Q-4 | Pilots: small client projects (speed, tailoring) and Pendentive (depth). Under discussion |
| Q-5 | Artifact storage, IDs, link model. Leaning: one Markdown file per artifact with YAML frontmatter, opaque IDs, own validator (`research/2026-10-storage.md`). Deferred as mechanical |
| Q-6 | GitHub: agreed in principle. Repo files are authoritative (model, decisions, open questions, proofs, evidence index); issues hold intake and work; milestones and releases scope increments; evidence is committed because CI retention is 90 days. Details open |

## Landscape in one paragraph

Spec Kit, OpenSpec, BMAD, superpowers, Kiro and Agent OS cover spec → plan → tasks →
implement well. None does checked requirement → design → code → test traceability,
decisions as first-class records, interface contracts, verification planning, risk, or
tailoring to risk. None derives the stack from requirements with recorded alternatives.
The Agent Skills standard has no concept of a workflow. See `research/2026-10-landscape.md`.
