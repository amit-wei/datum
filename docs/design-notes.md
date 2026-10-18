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
| P12 | Architecture has two views: logical (parts, interfaces) and deployment (units that run separately, each listing the parts it hosts). One unit by default; every extra unit needs a decision that cites the requirement forcing the boundary (`research/2026-10-16-pendentive-audit.md`, L1) | agreed |
| P13 | Each engine step draws on a menu of techniques. Conditions (level among them) make a technique encouraged, forced or banned. First entries: end-to-end user scenarios, forced in functional analysis at product level; spikes (see the engine) | agreed in concept |
| P14 | No code for a block until it is analysed down to the stopping rule. Depth only for the increment's blocks (P7); nothing modelled below the stopping rule (no file-level components) | agreed |

## The level engine (draft, under discussion)

The same procedure at every level (the recursive SE process of MIL-STD-499B / IEEE 1220).
Corrected 2026-10-14: functional analysis comes before this level's requirements.

**Input to a level:** the requirements and constraints allocated to this block by the
level above. At product level: the needs and the builder's constraints, drawn out by
grilling into an elicitation record (see Skills). Greenfield has no separate intake step.

1. **Functional analysis.** What this block must do to meet its inputs, and the flows
   between functions. Infeasible or conflicting inputs go back up (requirements loop).
2. **Requirements.** For each function, requirements that state it is attained and how
   well; plus the constraints flowed down. Each with a verification method and a
   pass/fail criterion (the verifiability gate).
3. **Synthesis.** Choose the parts that perform the functions. Allocate functions and
   requirements to parts, define the interfaces between parts, record each choice as a
   decision with the alternatives considered (the trade study). Choices create
   **derived requirements**, justified by their decision rather than by a parent.
   Its outputs (agreed 2026-10-17): decisions with their trade studies; parts (purpose,
   `contributes_to`, unit); interfaces with their items; budgets flowed down as child
   requirements in each part's folder (a latency or cost budget split between parts);
   derived requirements, including interface requirements (`of: IFC`); the deployment
   view; architectural risks and the requirements that answer them. The part entry is
   the thinnest of these.
4. **Design evaluation** (not "verification", which is the right side of the V). Check
   the synthesis against the requirements: every requirement allocated, key requirements
   walked through the parts as runtime scenarios. A failure changes the architecture or
   renegotiates a requirement (a recorded decision). Loop to 1–3 until it holds.
5. **Cases** (added 2026-10-17). The test author writes the executable cases for this
   level's proofs, as on the left side of the V. The same at every level: a leaf's
   cases test it through the interfaces its parent fixed; a non-leaf's integration
   cases run against stubs until its children exist. See Build and verify.

**Output:** each part with its allocated requirements, the input to its next level.

**The level rule** (agreed 2026-10-17; the usual SE spine, not a new rule). A choice is
made, a function defined and a requirement tested at the lowest level that holds
everything it touches. A choice that affects more than one part, or a requirement of
this level, is made here; one that affects a single part waits for that part's level.

**Spikes** (agreed in concept, 2026-10-16). A spike is throwaway code that answers a
question: a measurement, a feasibility check. Its result enters the model as evidence;
its code is deleted. It is a technique of the menu (P13), not a free permission: it is
triggered by a named condition in a step, for example research in functional analysis,
or filling a TBD value of a requirement during synthesis. Each spike has a time-box and
a written question before it starts.

Starting set of triggers (agreed 2026-10-16; revised with use, like everything here):

| Step | Trigger | Output |
|---|---|---|
| 1 Functional analysis | Doubt that a function is feasible | Evidence to keep, change or send it up a level |
| 2 Requirements | A TBD value that can be measured | The value, justified by the spike |
| 3 Synthesis | Trade-study alternatives that cannot be ranked without measuring | Evidence in the decision |
| 4 Design evaluation | A scenario that cannot be walked through the parts on paper | Pass or fail of the walk-through |

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

## Risk in the engine (agreed 2026-10-17)

Risk is a technique, not a step of its own. It appears twice per level, as in ARP4761
(`research/2026-10-risk-methods.md`):

- **In functional analysis:** losses and hazards (STPA step 1). Some functions are
  dangerous whatever the design. Requirements answer them in the requirements step.
- **After synthesis:** STPA unsafe control actions and loss scenarios on the control
  structure, which exists only once there are parts; STRIDE (spoofing, tampering,
  repudiation, information disclosure, denial of service, elevation of privilege) on
  every interface that crosses a trust boundary. They generate derived requirements.
- **FMEA is not in the default profile**, only in the critical one (interface FMEA).
  Corrects the earlier draft, which named FMEA on parts and interfaces.
- Requirements that interact can create risk (Pendentive's exactly-once rules made
  retrying impossible). Such conflicts are caught in the requirements step's closing
  review when they show from the requirements alone, and in design evaluation when they
  need the parts.

## Types (v0, agreed 2026-10-16)

A type is in v0 only if an engine step makes it and a step or check uses it (P9).

| Type | Made by | Used by |
|---|---|---|
| function | 1 Functional analysis | requirements (`of`), child functions, parts (`contributes_to`) |
| requirement | 2 Requirements | proofs, child requirements, the next level |
| proof | 2 Requirements (the verifiability gate) | cases, verdicts |
| part | 3 Synthesis | the next level (each part becomes a block) |
| interface | 3 Synthesis | proofs at its level |
| unit | 3 Synthesis (deployment view, P12) | the rule that an extra unit cites a decision |
| decision | 3 Synthesis (trade study), and any recorded choice | derived requirements, units, impact analysis |
| risk | the two risk passes | the requirements that answer it |
| external | product-level functional analysis (the context: the user, the host, outside services) | interfaces (`between`); generated views such as a README or an installer |

- **Not files of the model:** a *case* lives in code and names its proof (a tag); a
  search for the proof ID finds every case, in any file or language. *Evidence* is
  generated output at a commit. "Means of compliance" is replaced by proof.
- **Not a type: technique outputs.** Scenarios, spike results and research live in the
  block's `analysis/` folder, for every engine step. Each technique defines its output's
  format in its skill reference; the validator checks only that references to them
  resolve, so each output has a stable ID. An output exists only if a model artifact
  cites it (P9). Scenarios are forced at product level (P13), and product functions cite
  the scenario they serve. A trade study is not a separate output: it lives inside its
  decision (the alternatives considered).
- **Need is not a type** (agreed 2026-10-17). Needs live in an elicitation record
  (`ELI-`), the output of grilling, an analysis output like a research report. The chain
  is function → scenario → elicitation record.
- **Not a type in v0:** open question. It is a `TBD` in the field it blocks (a spike
  trigger) plus a GitHub issue for the work. This narrows Q-6.
- **Constraint is not a type:** it is a requirement with `source: builder`. A field
  names a role, never a person (`research/2026-10-16-pendentive-audit.md`, L9).
- **Unit vs part.** A part is a logical block (arc42 building block); a unit runs on its
  own (process, container, store; arc42 deployment node). Parts share a unit unless a
  requirement forces them apart; a part goes where its technology runs; each
  lowest-level part runs in one unit; an interface that crosses units gains a
  transport, a format and failure modes.
- **File layout (agreed):** one file per artifact, in a folder per block per type, under
  one root, e.g. `model/product/agent-runtime/requirements/REQ-7K3Q.yaml`. Chosen over one YAML file per block per type
  on agent cost, merges and tool limits, with equal accuracy
  (`research/2026-10-16-layout-simulation.md`). The content is YAML throughout: prose is in
  fields (`statement`, `rationale`) that a schema can require. Policy: structure where
  possible, until a need for unstructured content is shown.
- **Deployment view:** `model/deployment/units/`, beside `model/product/`. Not
  `deployment/` at the root, where a codebase keeps its deploy configuration.

## Links (agreed 2026-10-16)

Each link is stored once, in one direction; the reverse is computed (search or a trace
command), never stored.

- **Containment comes from the folder.** A part is an entry in its parent block's parts
  file; its own artifacts live in its folder. A part has no `parent` field.
- **Functions belong to the block they describe.** A part's own functions are written by
  that part's functional analysis, one level down, each with `parent: FUN` (functional
  decomposition). A function may store `serves:`, the scenarios it serves (a gate
  requires it at product level).
- **Allocation is a design choice of synthesis** (revised 2026-10-17). The part entry
  stores `contributes_to: [FUN]`, the functions of this level it contributes to. Several
  parts may contribute to one function; the children's functions split the work below.
  Recorded at synthesis so that design evaluation can check that every function has at
  least one contributing part, and so that parts outside the increment, which get no
  functional analysis yet (P7, P14), still record their purpose as a link. Functional
  decomposition and allocation are separate facts, as in classic SE; the earlier
  position merged them.
- **Requirements are never passed down whole.** A requirement is verifiable at the level
  it is written. Flowdown writes child requirements in the part's folder with
  `parent: REQ`; that is the allocation. A parent is verified by its children plus its
  own level's proofs (see Verification). When a parent changes, its computed children are
  revisited.
- **A requirement has at least one reason to exist**, any of: `of: FUN` (the function it
  constrains), `parent: REQ`, `justified_by: DEC`, `answers: RSK`, `source: builder`.
  None is an error.
- **Proofs** store `covers: [REQ]`. Cases name their proof; a proof does not list cases.
- **Decisions** store `supersedes: DEC` (the old one's state is computed) and
  `drivers: [REQ]`, the requirements it serves, for impact analysis. Revising a decision
  is one new entry (L5).
- **Interfaces** store `between:` their two ends (part or external) and live in the folder
  of the block whose synthesis defined them. A refining interface stores `parent: IFC`.
  A requirement's `of:` may name a function or an interface. A unified interface style
  is a decision at the higher level that the children follow.
- **Units:** every part with no children in the model stores `units:`; a parent's units
  are computed from its children. A unit stores `justified_by: DEC`, except the default
  unit.
- **Risks** store only `threatens:` (function, part or interface). Requirements store
  `answers: RSK`; a decision may store `accepts: [RSK]` and must state the consequence
  accepted. A risk is computed as answered, accepted or open. All other risk fields wait
  for the design of the risk passes.
- **Open:** whether design evaluation's
  "every requirement is handled" can be computed without `allocated_to`: own proof at its
  level, or children written at synthesis, or reach through its function's children.

## Fields (agreed 2026-10-16)

Tried on real rows in `research/2026-10-16-schema-trial.md`. Schemas, like the pattern
list, techniques and skills, belong to datum; a project uses them and does not extend
them.

- **YAML hygiene.** No key or plain value may be a YAML 1.1 boolean word (on, off, yes,
  no); the validator refuses boolean keys.
- **Requirement statement** follows EARS: `statement` plus `pattern` (ubiquitous, event,
  state, unwanted, optional, compound, none). The validator warns on `none` and on more
  than one "shall". A pattern of our own is added only after the pilot shows a recurring
  misfit.
- **Measure.** One metric per requirement, with any number of bounds on it
  (`{statistic, op, value}`, e.g. p95 and p99), like a tolerance band. The statement
  holds `{measure}` exactly once when a measure exists, so the number is stored once.
  `value: TBD` is allowed and is a spike trigger. A metric's definition is inline in v0.
- **Proof criterion** holds how we will know: the pass condition, sample size,
  confidence, bound, conditions. It refers to the requirement's measure and never copies
  it. The case holds the test article (a held-out set, the judge); evidence holds the
  result.
- **No `kind` field.** Safety, interface, constraint, performance and functional are
  computed from links and fields.
- **Rationale** is required when a measure exists, or when the requirement chooses a
  response over an obvious alternative (refuse, ignore, report, block); the second is a
  review check, not a validator rule. Otherwise optional, and it never restates links.
  *Why this block holds it* goes once in the part's `purpose`.
- **Part folders** are slugs, and the part names its folder in a `folder:` field.
- **Interfaces** list the `items` that flow, each with its sender.
- **Decisions** hold the trade study as `options`; `accepts:` requires `consequence:`;
  `evidence:` cites analysis outputs.

## Validator and gates (agreed 2026-10-16)

- **The validator** checks invariants true of every artifact on every commit. Its rules
  are the same at every level and for every artifact of a type; an exception needs a
  very good reason.
- **Gate checks** run when an engine step is closed (P11). Level- or step-specific rules
  live there, e.g. product functions serve a scenario before product-level functional
  analysis closes (P13). `serves:` is an ordinary optional field at every level.

## IDs and references (agreed 2026-10-16)

- An ID is a type prefix plus 4 characters of Crockford base32, e.g. `REQ-7K3Q`, minted
  by a script that checks existing IDs. The validator catches a collision between
  branches. No block in the ID, no sequence numbers.
- The file name is the ID. An ID never changes and is never reused. A move is `git mv`.
- Links name IDs only, never paths. Analysis outputs get IDs the same way (`ELI-`,
  `SCN-`, `SPK-`, `RES-`).
- Only decisions are superseded. Other artifacts are edited in place (git is their
  history) or set to `retired`; nothing is deleted.

## States (agreed 2026-10-16)

Only states a person decides are stored: `draft → agreed → retired`; for a decision
`proposed → agreed`. Everything else is computed, never stored: *built* (a case exists),
*covered* (a proof covers it), *verified* (evidence passes at a version's commit; see
Build and verify), *answered*
(a requirement answers a risk), *superseded*. The model is ahead of code during every
build (P4); code ahead of the model is the defect. Per-type states beyond these: open.

**Step state** (agreed 2026-10-17). Closing a step is a decision of the builder, so it is
stored: one file per block, `model/<block>/steps.yaml`, with a fixed schema the
validator checks, e.g. `functional-analysis: {closed_at: <commit>}`. *Stale* is
computed: model files of the block changed after the closing commit. The router reads
these files; GitHub issues hold the queue of work and never mirror model state.

## Skills (agreed 2026-10-17)

Settles Q-3. Evidence: `research/2026-10-skill-granularity.md`,
`research/2026-10-17-skill-tiering.md`.

- **Three tiers.** A router (`datum`) that reads the state on disk and names the next
  step. Step skills, one per engine step and around it. Technique skills, each how to
  do one thing well with its conventions and output format.
- **A step skill** opens with the stance, then its goal, its techniques in order with
  the condition that makes each encouraged, forced or banned (P13), its end condition,
  and where subagents are used. The stance is the same block at the top of every step
  skill (the top survives compaction), copied by hand.
- **The stance** (draft, 2026-10-18, from `research/2026-10-18-stance.md`; tested with
  the skills, not before): understand the step's inputs and outputs first; the simple,
  lean solution that fits the existing architecture; write only what a later step uses;
  stay inside datum's steps unless the builder agrees; ask on the builder's choices; say
  what is missing or assumed; research before a convention or changing fact enters the
  model; judge "done" from what something must cover; name the evidence. The text is in
  the router (`skills/in-progress/datum/SKILL.md`).
- **Skills follow the writing guide** in `research/2026-10-18-stance.md` (agreed
  2026-10-18): plain imperatives, rules as trigger plus action, no MUST by default,
  standing rules first, short files.
- **Every skill is invocable by the builder.** Ideally only `datum` is invoked.
- **Packaging: each technique is its own skill** (agreed 2026-10-18, by test). Against
  reference files inside the steps, separate skills won on the validation queries on
  Sonnet and Haiku and in the builder's own setup, by a small margin, and need no
  copies. A skill hidden with `disable-model-invocation` cannot be called by a step.
  Evidence and caveats: `research/2026-10-18-packaging-test.md`.
- **Lessons for writing skills** are in that note (17, each labelled); read them before
  writing or changing any skill. The ones that change the design: datum's setup writes a
  line into the project's CLAUDE.md telling the agent to load `datum`; the router names
  its only exceptions; a technique is loaded before its output is produced; no
  placeholder text ships in a skill.
- **Quality references are curated:** what matters, in plain words, each item citing its
  source. Never a standard pasted in. The writing and the reviewing technique of a type
  read the same reference.
- **Grilling** is one technique at every level. Forced once at the start of product
  functional analysis. Afterwards, at any level and after any technique, triggered when
  a finding can be settled only by the builder: a preference, a priority, a premise, a
  trade between goals.
- **Every step ends in a review loop** with a subagent that did not do the work,
  against the step's end condition, the quality references and the stance. Findings go
  straight back to the agent doing the step, which fixes them, and the review runs
  again. The builder closes the step when neither the working agent nor the reviewer
  has issues left above a severity threshold. Targeted reviews of one piece (a trade
  study, a walk-through) are triggered inside a step.
- **Severity of a finding:** *blocking* (breaks the end condition, or an artifact is
  wrong) and *should fix* (weakens the work: unclear, unjustified, an alternative
  missing) keep the loop going; a *note* is shown to the builder at closing. The working
  agent may reject a finding with its reason; if the reviewer does not accept it, the
  disagreement goes to the builder (a grilling trigger). The loop ends clean or with a
  question for the builder, never after a fixed number of rounds. #4 may refine this.
- **A technique is loaded before its output is produced** (agreed 2026-10-18): before
  writing or changing an artifact, a record or a looked-up fact, the agent loads the
  technique that makes it. A question gets an answer grounded in the model and an offer
  to run the technique. A hook that enforces this on writes under `model/` is parked.
- **Reviewers are per step, not per type** (agreed 2026-10-18): one reviewer per engine
  step, against that step's end condition, the quality references and the stance. Each is
  an agent in `agents/`, not a skill: the review is always done by a subagent, and an
  agent is not in the skill listing, so it cannot shadow a technique. `increment` and
  `verify` have no reviewer agent (agreed 2026-10-18): they close on computed checks
  (scope coverage, stubs on the demonstrated path, evidence at one commit) and the
  builder's word.
- **Scripts for agents** are written when a step needs one, as with types (P9).
  Candidates: validate, stale, trace (links up and down from an ID), coverage (every
  parent has a child, every function a requirement, every requirement a proof).

### Going back (agreed 2026-10-17)

One mechanism, no explicit "reopen" command:

1. Any artifact may change at any time. A superseding decision needs the builder's
   agreement.
2. Staleness is computed: a step whose artifacts changed after its closing commit, every
   later step of that block, and every block whose inputs link to the changed artifact.
3. The router sends work to the highest stale block first, at its earliest stale step.
4. The builder re-closes each stale step after a review loop over what changed and what
   links to it. A revisit that changes nothing closes quickly.

- **Across levels, problems go up, changes do not.** A level that finds an input
  infeasible or conflicting raises it (an issue and a grilling trigger); the parent's
  step makes the change, under its own review loop.
- **Across increments:** a later increment can make built items stale; their verdicts
  are then computed as unverified (P4). Rework that blocks the current increment joins
  its milestone; otherwise it is an issue for a later increment.
- **Subagents** for independence (review; cases apart from implementation, P5), for
  read-heavy work where only the conclusion matters (research, codebase surveys), and
  for parallel independent pieces (scenario walk-throughs, leaf blocks). Never for
  grilling or for a choice the builder must agree to: a subagent proposes, the main
  session decides with the builder.
- **Proof vocabulary in techniques:** `writing-requirements` → `writing-proofs` (which
  verification covers a requirement, by what method, against what criterion) →
  `writing-cases` (the test code, in build). Functions are never verified;
  requirements are.

### Step designs (first draft; techniques are names, not yet written)

**Functional analysis.** Goal: the functions of this block and the flows between them,
complete for its scope, plus the losses it could cause. Techniques: `grilling` (forced
at product level), `research` (triggered by an unfamiliar domain or a possible existing
solution; subagent), `writing-scenarios` (forced at product level), `writing-functions`,
`losses-and-hazards` (forced at product level; below, when a function can cause a loss),
`running-a-spike` (doubt about feasibility; subagent). At product level the weight is
on grilling and scenarios; below, on writing functions. End condition: every scenario
step is done by some function; every function serves a scenario (product) or a parent
function (below); every elicited need is in a scenario or marked out of scope; losses
are listed; no feasibility doubt without a spike or a TBD issue; closing review clean.

**Requirements.** Goal: the requirements that say each function is attained, and how
well where the builder, a hazard or a budget cares; plus constraints and allocated
budgets; each with a proof. Inputs: functions, hazards, the builder's constraints
(product level) or the requirements the parent's synthesis wrote (below). Techniques:
`writing-requirements` per function (attained, how well, unwanted behaviour),
requirements answering hazards, `writing-proofs`, `grilling` (a value only the builder
knows), `research` (a value already established elsewhere; subagent), `running-a-spike`
(a measurable TBD; subagent). The closing review also looks for conflicts visible from
the requirements alone. No bound on the number of requirements: scope is bounded by the
increment. End condition: every function has at least one requirement `of: FUN`; every
hazard answered, accepted or open with an issue; every requirement has a reason and a
proof with a criterion; every TBD has an issue; validator clean; closing review clean.

**Synthesis.** Goal: the design choices that meet this level's functions and
requirements. Techniques, in classic order (IEEE 1220): grouping functions into
candidate parts, `research` on what exists (buy or build; subagent), `trade-study` per
significant choice (forced for the stack at product level), `running-a-spike` (options
that cannot be ranked on paper), allocation and derived requirements, `defining-interfaces`,
`deployment-view`, the architectural risk pass (ARP4761), `applying-stopping-rule` per
part. End condition: every function has at least one contributing part; every
requirement flowed down or covered by this level's own proof; every interface has its
items; every extra unit justified; every part meets the stopping rule or is queued for
the next level; every architectural risk answered, accepted or open with an issue;
closing review clean.

**Design evaluation.** Goal: evidence before code that the synthesis meets this level's
requirements. Techniques: computed checks first (allocation, coverage, links; a
script), `walking-scenarios` through parts and interfaces (forced per scenario at
product level; below, the parent's scenarios that touch the block; a subagent per
scenario), conflicts that need the parts, analysis of budgets verified by Analysis (a
spike). End condition: checks pass, every walk-through completes without a gap,
conflicts resolved by a decision, closing review clean. A failure loops to requirements
or synthesis.

**Increment.** See Increments below. Techniques: a menu of strategies for choosing the
scope, each with where it fits, none forced: walking skeleton (an unproven architecture
or several units), scenario slice (scenarios exist and a user should try the result),
risk first (one unknown dominates), function-based (a capability stands alone, such as
a library or a CLI tool); `grilling` on the choice. The builder decides. The closing
review flags a stub on the path of the slice the builder means to demonstrate.

**Cases, build, verify.** See Build and verify.

**Not designed yet:** work packages (the session-sized unit of work inside an increment;
deliberately not defined yet), and evals with their judges.

## Build and verify (agreed 2026-10-17)

Settles Q-2: the criterion is written with the requirement (a proof), the executable
case when the level closes (engine step 5).

**Build is a contract, not a coding method.** Datum defines what goes in, who does what,
what is protected and what comes out. The craft of coding is left to the implementer
agent. No dependency on superpowers: its test-driven development has one agent write
both the test and the code, against P5.

The contract for one leaf block:

1. **In:** the block's requirements, proofs and cases (written at step 5), its
   interfaces as the parent fixed them, and the decisions that set conventions.
2. **A hook locks the cases;** the implementer cannot edit or delete them (P5).
3. **The implementer writes code until the cases pass.** It builds nothing that no
   requirement asks for; a need it finds is raised (problems go up). A case it thinks
   is wrong is raised to the test author, never fixed by the implementer.
4. **Review loop** against the block's functions and decisions. Verification cannot
   catch overbuilding or broken conventions: overbuilt code can pass every case.
5. **Out:** code and passing cases, the IDs listed in the commit or PR.

Standard checks in build:

| Check | Catches | How |
|---|---|---|
| The contract | Weakened tests | Hook |
| Traceability: proof IDs in cases, requirement IDs in commits | Lost trace | Script |
| Boundary conformance: a block reaches other blocks only through its interfaces | Architecture eroding in code | Script (an import-rule checker) |
| Overbuild signals: code no case reaches, public surface beyond the interface items, a dependency no decision chose, configuration or abstraction no requirement asks for | Overbuilding | Coverage and script, then review |
| Functions and decisions | Code doing something other than what the block is for | Review loop |

The step-5 reviewer checks the cases against the proofs and the synthesis; the build
reviewer checks only the code.

**Conventions come from three sources:**

| Source | Examples | Lives in |
|---|---|---|
| Datum, the same in every project | Model layout, IDs, case tags, the build contract, the evidence format | Datum's skills and schemas |
| The project, an output of synthesis (P3) | Language, frameworks, how code folders map to parts, dependency rules, error handling, logging, test framework, code style | Decisions; a generated, never hand-edited section of the project's AGENTS.md lists them |
| The builder, across projects | How the agent talks, explains, asks | The builder's own CLAUDE.md, outside the repo |

- A preference that affects the product enters as a builder constraint through grilling.
  One that affects only how the agent works with the builder stays personal.
- **Code style** (comments, function size, tone of docs) is the project's, not datum's.
  Product synthesis records one code-style decision; the default is the ecosystem's
  standard formatter and linter, whose config files are the convention. What no tool can
  check is written in the decision and checked by the build review.

**What runs when:**

- **On each commit of the work branch:** the cases a change could affect (change impact
  analysis, as DO-178C requires for re-verification). Code in a block runs its cases and
  the cases of every proof that covers its interfaces; a model change runs the proofs of
  the changed requirements and what links to them; a shared change (a dependency, build
  config, a shared library) runs everything. Boundary conformance is what makes this
  trustworthy. These runs are feedback, not evidence of record.
- **At a release:** everything, on the release candidate.

**Verified = the evidence passes at the version's commit.** Nothing else. Consequences:

- `main` holds only verified versions; each increment works on its own branch.
- The release candidate is frozen on the work branch, CI and the manual proofs run on
  that commit, and it reaches `main` without a new commit (a fast-forward merge) and is
  tagged. A squash merge would orphan the evidence.
- Manual proofs (Demonstration, manual Inspection) are redone on every release
  candidate. The cost pushes toward automating a demonstration as a scripted end-to-end
  Test. Carrying manual evidence forward is the fallback if the pilot shows the cost is
  real.

**Evidence** has a common core (proof ID, commit, result, date) and a basis by method:

| Method | Basis | Written by |
|---|---|---|
| Test | CI run link | CI only |
| Demonstration | A record: what was shown, what was observed, the criterion | The builder observes; an agent prepares the context and steps, points to what to look at, and writes the record |
| Inspection | A record: the artifact at a commit, the criterion, the verdict | A reviewer agent that is not the author, or the builder as above |
| Analysis | The analysis output's ID | Its author; the closing review checks it |

Evidence is never written by the author of the thing it verifies. Where the builder
supplies evidence, an agent makes the edit.

## Increments (agreed 2026-10-17)

Settles Q-1 and #2.

- **An increment is a usable, verified addition of capability** (the convention of
  incremental development; Scrum Guide 2020: "thoroughly verified"). It includes the
  descent through the levels for its scope, build and verify, and ends with something
  that runs and passes. It is not a session of work.
- **Scope is a set of functions at any level that is already modelled, plus explicit
  deferrals.** Everything else is computed: functions → requirements (`of`) →
  contributing parts (`contributes_to`) → interfaces. No rule makes the first increment
  product-level: before it, nothing below the product level exists.
- **Deferrals** each carry a reason. Deferring a requirement that answers a hazard needs
  a decision with `accepts: [RSK]` in the model. Nothing in scope is dropped silently
  (L4).
- **Where it lives (GitHub, accepted for now).** The scope is in the milestone
  description, in a fixed structure a script reads: function IDs, and deferrals with
  their reasons. The milestone holds the work; a GitHub release (a version tag) is the
  close. The router reads the scope through the GitHub API. Accepted costs: no offline
  use, no other hosts, and probably no edit history of the scope. Reversible by moving
  the scope into a file.
- **Out-of-scope neighbours are stubbed, not banned.** An in-scope part with an interface
  to an out-of-scope sibling is tested against a stub derived from the interface as the
  parent level defined it (a test double, contract testing; an interface simulator in
  hardware). The part's own requirements on that interface are verified against the
  stub; requirements that need both real sides are listed as deferred, with the reason
  "other end out of scope". A ban would pull every connected part into scope (L1).
- **Flow.** Every block runs the same five engine steps (corrected 2026-10-18: the
  product block too, including cases). The increment step runs after the product block's
  cases close, then the engine for each block in scope down to the stopping rule, then
  build and verify.
  A block may be built as soon as its own level reaches the stopping rule, without
  waiting for its siblings (P14 holds per block; interfaces are fixed above).
- **Done:** every in-scope requirement that is not deferred is verified at one commit,
  and the builder closes the increment, which creates the release.

## Independent review (open, deliberately undesigned)

Agreed: reviews at each engine step; each step closes with a closing review by a
subagent (see Skills). How to review is a technique skill; the reviewer is an agent
that loads it. Also wanted: specialised reviews (a risk
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
| Q-1 | What exactly is an increment, and how big is it? Settled 2026-10-17: see Increments. Size is the builder's choice, by strategy, not by number |
| Q-2 | When is each verification artifact written? Settled 2026-10-17: the proof with the requirement, the case when the level closes (engine step 5). See Build and verify |
| Q-3 | Skill granularity. Settled 2026-10-17 in concept: see Skills. Packaging (technique as skill or as reference) is decided by a test in #6 |
| Q-4 | Pilots. Agreed 2026-10-16: the first real use of datum v0 is Pendentive's re-scoped v1, run from datum's intake with the existing Pendentive model as reference material, not migrated. While formats are designed, they are tested against real Pendentive rows. Small client projects later |
| Q-5 | Artifact storage, IDs, link model. Settled 2026-10-16: see Types, Links, IDs and references |
| Q-6 | GitHub: agreed in principle. Repo files are authoritative (model, decisions, proofs, evidence index; open questions are issues plus a `TBD`, see Types); issues hold intake and work; a milestone holds an increment's scope and work, a release closes it (see Increments); evidence is committed because CI retention is 90 days. Details open |

## Landscape in one paragraph

Spec Kit, OpenSpec, BMAD, superpowers, Kiro and Agent OS cover spec → plan → tasks →
implement well. None does checked requirement → design → code → test traceability,
decisions as first-class records, interface contracts, verification planning, risk, or
tailoring to risk. None derives the stack from requirements with recorded alternatives.
The Agent Skills standard has no concept of a workflow. See `research/2026-10-landscape.md`.
