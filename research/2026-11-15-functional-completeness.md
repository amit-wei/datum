# How the field makes functions and requirements complete (2026-11-15)

Question: what does established practice do to make sure that (a) the set of functions
or behaviours a piece of software must have is complete, and (b) a set of requirements
is complete, and what is supposed to happen when gaps are found at that point? Prompted
by the requirements retest (#62): in the plant-watering fixture N1 the user sets a home
town but cannot see or correct it, and neither functional analysis, its review (clean
three times), the requirements step nor its review noticed, asked the builder, or sent
the work back.

Labels: **VERIFIED** = I read it in a primary source (source and section or page
given). **VERIFIED-secondary** = only an abstract, summary, review or third-party page
was seen (named). **INFERRED** = my reasoning. Page numbers are printed page numbers
unless I say PDF page.

## Summary

1. **No source claims a method that proves a function or requirement set complete
   against what the stakeholders need.** Wiegers and Beatty: "There is no way to be
   certain that you have found them all"; "You will never document 100 percent of the
   requirements". What can be checked is completeness *relative to a model*: every
   scenario step, every event, every data item, every state-and-input pair. Each method
   below is one such model; each finds the gaps its model can show and no others.
2. **The methods fall into five families.** Goal and scenario coverage (use cases,
   story maps); event coverage (event lists, event-response tables); data coverage
   (CRUD matrix, domain models, "counterparts"); state coverage (Leveson's completeness
   criteria, SCR tables; from safety-critical and embedded work); and prompts
   (checklists of common areas, usability heuristics, stakeholder lists, procedural
   prompts in interviews). Practitioner books recommend using more than one, because
   each representation shows different gaps (Wiegers: "Represent requirements
   information in more than one way").
3. **The N1 miss is the kind a data-coverage check is built to find.** The home town is
   created and updated (FUN-SB5K) and read only by other functions (FUN-G6AB,
   FUN-PGV7). A CRUD check asks per data item, per actor, whether each operation
   exists. Datum's functions rules ban CRUD *as function names*; the sources use CRUD
   *as a check*. Those are different things, and datum dropped the check with the
   names (see section 6).
4. **When a gap is found after functional analysis, every process source says: go back
   and change the earlier work, under control.** Systems engineering calls it the
   "requirements loop" (DAU 2001, after IEEE 1220). NASA's software safety guidebook
   says missing requirements are "back-filled" into the specification before
   implementation, under configuration control. Scrum makes the backlog "emergent" and
   has scope "renegotiated with the Product Owner". None of them tell the later step to
   work around the gap. Who decides differs: the customer or stakeholder in systems
   engineering, the Product Owner in Scrum.
5. **The evidence that these methods work is real but modest.** Incomplete or hidden
   requirements are the most-cited problem in industry surveys (NaPiRE: 48% of 228
   companies). Scenario-based reading found more defects than ad-hoc or checklist
   reading in a controlled experiment, though replications were weaker. Procedural
   prompts got more complete requirements from interviews than simple questions. Domain
   models were sensitive to missing requirements in an industrial simulation. Most
   studies are small, few are replicated, and none tests a whole method end to end.
6. **The usual cost argument is weaker than commonly cited.** The claim that a late
   fix costs many times more than an early one was not found in 171 projects (Menzies
   et al. 2017). The case for catching gaps early still holds for safety work and
   wherever rework spreads widely, but it is not a law.

## What was and was not read

Read (VERIFIED):
- **DAU, Systems Engineering Fundamentals** (Defense Acquisition University Press,
  January 2001), PDF via MIT OCW:
  https://ocw.mit.edu/courses/16-885j-aircraft-systems-engineering-fall-2005/6128a102c1a9b6dbd30f2fb18c12aa64_sefguide_01_01.pdf.
  Read chapter 3 (process overview, pp.31-33), chapter 4 (attributes of good
  requirements), chapter 5 (functional analysis and allocation, pp.45-47). The text says
  the process is "adapted from IEEE 1220"; IEEE 1220 itself was not read.
- **NASA-GB-8719.13, NASA Software Safety Guidebook** (March 2004):
  https://s3vi.ndc.nasa.gov/ssri-kb/static/resources/nasa-gb-8719.13.pdf. Read §8.4.1
  (requirements checklist, pp.168-169) and Appendix E (requirements state machines,
  pp.338-340). The appendix says it draws on Leveson's work.
- **Cockburn, Writing Effective Use Cases**, pre-publication draft #3, 2000, extract:
  https://courses.cs.duke.edu/spring23/compsci308/readings/cockburn_use_cases.pdf.
  Read the two pages "Reminders" and "The Writing Process". The book itself was not
  read.
- **Volere Requirements Specification Template**, Edition 13 (2007):
  https://www.cs.uic.edu/~i440/VolereTemplate.pdf. Read §2 (stakeholders), §7c (work
  partitioning, business event list, PDF pp.23-24), §22b.
- **Beatty and Wiegers, "Revealing Invisible Requirements"**, adapted by the authors
  from *Software Requirements*, 3rd ed. (Microsoft Press, 2013):
  https://modernanalyst.com/Resources/Articles/tabid/115/ID/2929/Revealing-Invisible-Requirements.aspx.
  Read in full. And **Wiegers and Beatty, "Modeling System Events"**, same book:
  https://modernanalyst.com/Resources/Articles/tabid/115/ID/2932/Modeling-System-Events.aspx.
  Read in full. Both are the authors' own text, so VERIFIED, but they are excerpts and
  not the book.
- **Méndez Fernández et al., "On Evidence-based Risk Management in Requirements
  Engineering"** (arXiv 1707.00144), which reproduces the NaPiRE top-10 problem table:
  https://arxiv.org/pdf/1707.00144. Read pp.1-7.
- **Nielsen, "10 Usability Heuristics for User Interface Design"** (1994, updated
  2020/2024): https://www.nngroup.com/articles/ten-usability-heuristics/.
- **The Scrum Guide**, November 2020: https://scrumguides.org/scrum-guide.html.

Seen only as abstracts, summaries or reviews (VERIFIED-secondary): Lutz 1993
(Voyager/Galileo errors; review at blog.acolyer.org); Pitts and Browne 2004 and 2007
(abstracts, a later review in arXiv 2408.12538 and 2412.13691); Davis et al. 2006
(abstract); Porter, Votta and Basili 1995 (abstract); Basili et al. 1996 PBR (abstract
and summaries); Arora, Sabetzadeh and Briand 2019 (abstract); Luitel, Hassani and
Sabetzadeh 2024 (arXiv 2308.03784 abstract); Zowghi and Gervasi 2003 (abstract);
Heimdahl and Leveson 1996 (abstract); Heitmeyer et al. SCR consistency checking
(abstracts and 2010 slides via search); Lauesen and Vinter 2001 (summaries); Menzies
et al. 2017 (abstract, and a review at neverworkintheory.org); Nuseibeh 2001 (abstract);
Lauesen, *Software Requirements* (table of contents only: §9.2.3 "Consistency checks and
CRUD"); Patton's story mapping (third-party workshop guides); Kano (Wikipedia and
vendor pages); OOUX/ORCA (practitioner pages); DO-178C structural coverage resolution
(a vendor deck and a Rolls-Royce/Rapita paper via search).

Not reached: IEEE 830-1998 and ISO/IEC/IEEE 29148 (paywalled; the completeness wording
of 830 §4.3.3 was not seen); Jaffe and Leveson 1989/1991 (the UC Irvine report is a
scanned image with no text layer); Leveson's *Safeware* Appendix; Royce 1970 (403);
McMenamin and Palmer, *Essential Systems Analysis*; Yourdon, *Just Enough Structured
Analysis*; the INCOSE handbook and Needs and Requirements Manual; DO-178C itself. The
search was cut short by the fetch tool's usage limit before the NASA SE handbook could
be re-checked for this question; its relevant sections are in
`2026-10-18-functions.md` and `2026-11-13-requirements.md`.

## 1. Completeness of the functions (behaviours)

### 1.1 Goal and scenario coverage

- **Cockburn's writing process starts from an exhaustive goal list, then checks
  it.** Steps: "Brainstorm and list the primary actors. Find every human and non-human
  primary actor, over the life of the system"; "Brainstorm and exhaustively list user
  goals for the system. The initial Actor-Goal List is now available"; "Double-check for
  time-based triggers and other events at the system boundary"; for each use case
  "Brainstorm and exhaustively list the extension conditions. Include all that the
  system can detect and must handle"; and last, "Readjust the set… Check for
  readability, completeness, and meeting stakeholders' interests". He also says to work
  "breadth-first, from lower precision to higher precision". VERIFIED (Cockburn 2000
  draft, "The Writing Process", steps 2, 3, 5, 9, 12; "Reminders").
- So the use-case method finds goals by listing (not by deriving) and checks
  completeness by review against actors, time triggers and stakeholder interests. It
  gives no test that the list is done. INFERRED.
- **Story mapping checks completeness by narrating the map.** One person tells the
  user's journey left to right from the notes on the wall while the others listen for
  gaps; stakeholders walk the map too; places needing more discovery are marked. "If a
  left-right, top-down retelling of the story based on the map does not make sense,
  your product has gaps." VERIFIED-secondary (workshop guide at barkingiguana.com and
  other practitioner pages; Patton's book not read).
- **Systems engineering derives functions from operational scenarios and modes.** DAU
  lists the activities of functional analysis as "Define system states and modes",
  "Define system functions & external interfaces", "Define functional interfaces",
  "Allocate performance requirements to functions", "Analyze failure mode effects and
  criticality", "Define fault detection and recovery behavior", "Integrate functions".
  VERIFIED (DAU 2001, Figure 5-1 and ch.5, p.46). This is defence and hardware practice.
  NASA's equivalent, "any specified operational usage… can be traced in an end-to-end
  path", is in `2026-10-18-functions.md` (VERIFIED there).

### 1.2 Event coverage

- **Volere partitions the work by business events and derives requirements from each.**
  "A list showing all business events to which the work responds. Business events are
  happenings in the real world that affect the work. They also happen because it is
  time for the work to do something—for example, produce weekly reports, remind
  nonpaying customers…" The response to each is a business use case; the list's purpose
  is "to identify logical chunks of the system that can be used as the basis for
  discovering detailed requirements". VERIFIED (Volere template ed. 13, §7c).
- **Wiegers and Beatty name three kinds of event:** business ("an action by a human
  user that stimulates a dialog with the software"), signal ("a control signal, data
  reading, or interrupt") and temporal ("time-triggered, as when the computer's clock
  reaches a specified time"). An event-response table lists every event with the
  expected behaviour, and "the expected response depends not only on the event but also
  on the state of the system at the time the event takes place". VERIFIED ("Modeling
  System Events").
- Event partitioning comes from structured analysis (McMenamin and Palmer 1984;
  Yourdon 1989). VERIFIED-secondary (Wikipedia, "Event partitioning"); the books were
  not read.
- **What it adds to scenarios (INFERRED):** a temporal or signal event is easy to miss
  when scenarios start from what the user does. In N1, the 8 o'clock reminder the
  builder deferred (ELI-YZF1 "Anything else") is a temporal event; it was handled. A
  move to another town is a business event the scenario SCN-Z7NW names in its trigger,
  but the response the user needs (see and change the stored town) was not derived from
  it.

### 1.3 Data coverage

- **CRUD as a check for missing functions.** Wiegers and Beatty: "A data model can
  reveal missing functionality"; data entities need create, read, update and delete
  operations "where applicable". VERIFIED ("Revealing Invisible Requirements"). A
  CRUDL matrix of actions against entities shows gaps as missing letters in a column.
  VERIFIED-secondary (Jama Software repost of Wiegers; the page itself returned 404).
  Lauesen's book has a section "Consistency checks and CRUD" (§9.2.3).
  VERIFIED-secondary (table of contents only).
- **Counterparts.** Wiegers and Beatty look for a requirement with no counterpart,
  such as a way to save a form with no way to retrieve it. VERIFIED (same article). A
  Jama "Elements of Requirements Style" post gives undo without redo as the same
  pattern. VERIFIED-secondary.
- **Domain models.** Arora, Sabetzadeh and Briand built UML domain models with experts
  in three industrial domains and simulated omissions: the models showed "near-linear
  sensitivity to both unspecified (i.e., missing) and under-specified requirements",
  but whether analysts can exploit these cues was left for further study.
  VERIFIED-secondary (abstract, Empirical Software Engineering 24(4), 2019).
- **Object-oriented UX.** Practitioners build an object map and a "calls-to-action"
  matrix: each row is an action a user can take on one of the system's nouns.
  VERIFIED-secondary (practitioner pages on ORCA; Prater's own material not read).
- **N1 seen through this check (INFERRED).** Home town: created and changed by the user
  through FUN-SB5K, read by FUN-G6AB and FUN-PGV7; no function shows it to the user.
  Plant: add, change, remove and list all exist (FUN-39Z5, BY64, E2EJ, M0FX). Watering:
  log, show history, remove one exist. The asymmetry between plants and the town is
  visible in a short table and not in a scenario walk, because no scenario has the
  user ask "which town did I set?".

### 1.4 State coverage (safety-critical and embedded origin)

- **NASA's software safety guidebook gives Leveson-style completeness criteria for a
  requirements state machine.** "All information from the sensors should be used
  somewhere… If not, either an input from a sensor is not required or, more
  importantly, an omission has been made from the software requirements
  specification." "If there is a legal value for an output that is never produced, then
  a requirement for software behavior has been omitted." "Every state in the RSM has a
  defined behavior (transition) for every possible input." "In case there is no input
  within a specified time, every state must have a defined transition, such as a
  time-out." It also asks what happens when input is out of range. VERIFIED
  (NASA-GB-8719.13, App. E.3 and E.5, pp.339-340). The appendix says it draws on
  Leveson; the original criteria (Jaffe, Leveson, Heimdahl, Melhart, IEEE TSE 17(3),
  1991) were not read. Their abstract says they target robustness and lack of
  ambiguity in behavioural requirements of real-time process-control systems.
  VERIFIED-secondary.
- **These checks can be automated when the requirements are formal.** SCR tables are
  checked for coverage (the conditions in a row cover every case) and disjointness (no
  two cells hold at once), to find "missing cases" and nondeterminism; this was
  evaluated on avionics specifications. VERIFIED-secondary (Heitmeyer et al., NRL
  reports and 2010 slides, via search). Heimdahl and Leveson automated completeness and
  consistency analysis for RSML and validated it on TCAS II, with a reported problem of
  spurious error reports on a large specification. VERIFIED-secondary (abstract, IEEE
  TSE 22(6), 1996).
- **What carries over to ordinary software (INFERRED).** The rules "every input is used,
  every legal output value is produced, every state answers every input" need no
  formalism to apply by hand to a small product, and the first one matches datum's
  "every output has a user" rule. They are written for controllers with sensors; a
  desktop app's "states" are mostly what is set up and what is stored.

### 1.5 Prompts: checklists, heuristics, stakeholders, interview technique

- **Wiegers and Beatty's list for finding missing requirements:** decompose high-level
  requirements; "ensure that all user classes have provided input"; trace user
  requirements, event-response lists and business rules to functional requirements;
  check boundary values; represent requirements in more than one way; use decision
  tables for complex logic; "create a checklist of common functional areas"; use the
  data model (CRUD); ask "What are we assuming?"; look for implied requirements and
  missing counterparts; re-interview and bring in "new stakeholders who know the topic
  and can spot gaps"; "read between the lines" for what customers expect without
  saying; ask context-free questions. VERIFIED ("Revealing Invisible Requirements").
- **Volere: "Failure to recognize stakeholders results in missing requirements."**
  VERIFIED (Volere template, §2, Motivation).
- **Usability heuristics name behaviours users expect without saying.** Nielsen #1:
  "The design should always keep users informed about what is going on". #3: users
  "need a clearly marked 'emergency exit' to leave the unwanted action". #9: errors
  should "precisely indicate the problem, and constructively suggest a solution".
  VERIFIED (nngroup.com). These are evaluation heuristics for designs, not a
  requirements method; using them as prompts during analysis is INFERRED. Heuristic #1
  is the one the N1 home town fails.
- **Kano: basic ("must-be") qualities are not voiced.** Customers take them for
  granted, are neutral when they are present and very dissatisfied when they are
  absent, so asking what they want does not surface them. VERIFIED-secondary
  (Wikipedia and vendor summaries; Kano et al. 1984 not read).
- **Interview technique.** Pitts and Browne tested 54 practising analysts: the
  stopping rules analysts use decide how many and how complete the elicited
  requirements are (JMIS 21(1), 2004), and procedural prompts designed against
  analysts' cognitive limits produced significantly more meaningful requirements than
  simple interrogatory prompts (Information Systems Journal 17(1), 2007).
  VERIFIED-secondary (abstracts and later reviews). Davis et al.'s systematic review
  found structured interviews among the more effective techniques, and that analyst
  experience did not appear to matter, from studies that were mostly not replicated.
  VERIFIED-secondary (abstract, RE'06).

## 2. Completeness of the requirements

### 2.1 What "complete" can mean

- **Two senses.** A set can be internally complete (nothing it refers to is undefined;
  every case of its own model has a response) or externally complete (it says all that
  the stakeholders need). The literature treats only the first as checkable. Zowghi and
  Gervasi also argue that making a set more complete can make it less consistent, and
  the other way round, as requirements evolve. VERIFIED-secondary (Zowghi and Gervasi,
  IST 45, 2003, abstract; Jaffe and Leveson TR 89-01 abstract: "no consensus as to
  precisely what constitutes complete specification").
- **Practitioners say outright that external completeness is not reachable.**
  "No little green light comes on to announce 'You're done!'" VERIFIED (Beatty and
  Wiegers).
- DAU's attributes of good requirements include "It must be complete and contain all
  mission profiles, operational and maintenance concepts, utilization environments and
  constraints. All information necessary to understand the customer's need must be
  there." VERIFIED (DAU 2001, ch.4, "Attributes of Good Requirements"). This is about
  each requirement carrying its context, not the set covering all needs.
- The GtWR and 29148 set characteristics (complete, consistent, feasible…) and NASA's
  Appendix C completeness checklist are in `2026-11-13-requirements.md` (VERIFIED-
  secondary and VERIFIED there).

### 2.2 How a requirements set is checked for gaps

- **Traceability both ways** (every requirement to a need or function, every function
  to a requirement): NASA and DAU. DAU: "Each function identified should be traceable
  back to a requirement" (ch.3, p.32). VERIFIED. This catches functions with no
  requirement and requirements with no reason. It cannot catch a need that reached
  neither (INFERRED).
- **Event-response and decision tables** over states, so each event in each state has
  a response. VERIFIED (Wiegers and Beatty, both articles).
- **State-machine criteria and formal checks** (section 1.4), where the requirements
  are formal enough.
- **Inspections with a defined reading technique.** Porter, Votta and Basili's
  replicated experiment on requirements inspections: scenario-based reading had a
  higher fault detection rate than ad-hoc or checklist reading, and reviewers found
  more of the fault classes their scenario targeted; collection meetings added no net
  detection. VERIFIED-secondary (abstract, IEEE TSE 21(6), 1995). Perspective-based
  reading (each reviewer reads as a user, designer or tester) gave reviewers with few
  defects in common; later replications were less favourable. VERIFIED-secondary
  (Basili et al., EMSE 1(2), 1996, and summaries).
- **Prototypes and usability tests.** In Lauesen and Vinter's study at an instrument
  maker, about 70% of requirement defects concerned ease of understanding or use, many
  traced to unstated (tacit) demands; the chosen remedy was to study user tasks better
  and make and usability-test early prototypes, and the next project reported fewer
  usability problems per screen. VERIFIED-secondary (summaries; the paper, RE journal
  6, 2001, was unreachable).
- **Coverage of the built code, in avionics.** DO-178C's structural coverage analysis
  is run after requirements-based testing; code not covered is resolved as a gap in
  the tests, an inadequacy in the requirements, dead code or deactivated code.
  VERIFIED-secondary (vendor deck and a Rolls-Royce/Rapita paper citing §6.4.4.3; the
  standard was not read). This finds missing requirements only after code exists, and
  only for behaviour someone already coded. Safety-critical aviation only.
- **Language models.** Luitel, Hassani and Sabetzadeh masked parts of 40 real
  specifications and found BERT's predictions highlighted missing terminology better
  than baselines; a filter reduced the noise; no user study. VERIFIED-secondary
  (abstract, RE journal 29(1), 2024). This finds missing terms, not missing behaviour
  (INFERRED).

### 2.3 What is supposed to happen when a gap is found

- **Systems engineering: the requirements loop.** "Performance of the functional
  analysis and allocation results in a better understanding of the requirements and
  should prompt reconsideration of the requirements analysis… This iterative process of
  revisiting requirements analysis as a result of functional analysis and allocation is
  referred to as the requirements loop." (ch.3, p.32). "During the performance of the
  Functional Analysis and Allocation process, it is expected that revisiting the
  requirements analysis process will be necessary. This is caused by the emergence of
  functional issues that will require re-examination of the higher-level
  requirements." (ch.5, p.46). A design loop does the same from synthesis back to the
  functional architecture. VERIFIED (DAU 2001). Note the direction: in IEEE 1220 order,
  requirements analysis comes *before* functional analysis, so the "requirements loop"
  goes from functions back to stakeholder requirements. Datum's order is functions,
  then requirements; the equivalent loop runs from the requirements step back to
  functional analysis and to the builder (INFERRED).
- **NASA software safety: back-fill under configuration control.** "Often during this
  development phase, missing requirements are identified… It may become apparent that
  various capabilities were assumed but not explicitly required, so were not
  implemented. Checklists can help identify these missing requirements. Once missing
  requirements are identified, they must be incorporated by 'back-filling' (updating)
  the requirements specifications prior to implementation in order to maintain proper
  configuration control." VERIFIED (NASA-GB-8719.13, §8.4.1, pp.168-169). The upstream
  document is corrected; the gap is not patched in the later product.
- **Lutz's guidance from spacecraft errors:** communicate requirement changes promptly
  to development and test teams. VERIFIED-secondary (review of Lutz 1993).
- **Scrum: the backlog is emergent and the Product Owner decides.** "The Product
  Backlog is an emergent, ordered list of what is needed to improve the product." "The
  Product Owner is accountable for effective Product Backlog management." During a
  Sprint, "Scope may be clarified and renegotiated with the Product Owner as more is
  learned." VERIFIED (Scrum Guide 2020). A gap becomes a backlog item, ordered by the
  owner; nobody fills it silently.
- **Requirements practice: go back to the people.** Re-interview, add stakeholders,
  ask "What are we assuming?", "study the results of initial elicitation sessions to
  identify areas of incompleteness". VERIFIED (Beatty and Wiegers).
- **Twin Peaks:** requirements and architecture are developed in parallel and
  iteratively, not one after the other. VERIFIED-secondary (Nuseibeh, IEEE Computer
  34(3), 2001, abstract).
- **Where they agree (INFERRED):** a gap found later is sent to the earlier artifact
  and to whoever owns the need, and the change is recorded. Where they differ: plan-
  driven processes re-baseline the earlier document under change control; Scrum adds
  an item to a living list and lets the owner order it.

## 3. Evidence and cost

| Claim | Evidence | Label |
|---|---|---|
| Missing requirements are a leading problem | NaPiRE: "Incomplete and / or hidden requirements" cited by 109 of 228 companies (48%), first of the top 10; 43 named it a cause of project failure, second to communication flaws with the customer (45) | VERIFIED (arXiv 1707.00144, Table 1) |
| Omissions drive safety-related errors | Voyager and Galileo: safety-related errors arose mostly from gaps between documented requirements and what correct functioning needed; missing requirements were involved in nearly half of the safety-related errors from recognising requirements; omitted operations were often missing reasonableness checks on input | VERIFIED-secondary (review of Lutz, RE'93). Spacecraft, embedded |
| Defined reading beats ad hoc and checklists for inspections | Porter et al. 1995; PBR 1996 with weaker replications | VERIFIED-secondary |
| Prompts and stopping rules change completeness in interviews | Pitts and Browne 2004, 2007 (54 analysts, lab task) | VERIFIED-secondary |
| Experience does not make an analyst find more | Davis et al. 2006; a 2024 family of studies (arXiv 2408.12538) states no study found experienced subjects more effective | VERIFIED-secondary |
| Domain models can reveal omissions | Arora et al. 2019, simulation in three domains | VERIFIED-secondary |
| Tacit usability demands dominate requirement defects in one company | Lauesen and Vinter 2001 | VERIFIED-secondary |
| Late fixes cost far more | Not found in 171 projects (2006-2014): later-phase resolution effort was not consistently or substantially higher; the authors call the effect possibly "an historical relic" | VERIFIED-secondary (Menzies et al., EMSE 22, 2017) |

**Cost of the methods (INFERRED unless noted).** A CRUD table and an event list are
cheap: one row per data item or event. Event-response tables grow with events times
states. Formal state-machine checks need formal requirements and produce spurious
reports on large specifications (Heimdahl and Leveson, VERIFIED-secondary). Inspections
cost reviewer time; the 1995 experiment found the meeting itself added nothing net
(VERIFIED-secondary). Prototypes and usability tests need something built and a user.
DO-178C coverage analysis needs code and full requirements-based tests. NASA notes that
for most software safety techniques "there are few or no metrics as of yet, to
quantitatively evaluate or compare the techniques" (VERIFIED-secondary, search summary
of NASA-GB-8719.13).

## 4. Where the methods disagree

- **Derive or list.** Systems engineering derives functions from scenarios, modes and
  decomposition (DAU, NASA). Use cases and story maps list goals by brainstorming
  "exhaustively" and then review (Cockburn). Data and event methods derive behaviour
  from things in the domain, not from journeys (Volere, Wiegers). INFERRED: a scenario
  walk finds what users do; a data walk finds what the product keeps and nobody can
  reach; neither finds the other's gaps.
- **CRUD as a smell or as a check.** "CRUD mania" (five use cases Create/Read/Update/
  Delete/List) is listed as a use-case error (VERIFIED-secondary, in
  `2026-10-18-functions.md` item 15), while Wiegers and Lauesen use CRUD to find missing
  functions (VERIFIED and VERIFIED-secondary above). These do not conflict: one is about
  how a function is named, the other about whether one is missing.
- **Complete up front or emergent.** Plan-driven and safety practice wants a complete,
  baselined set and controlled back-fill (DAU, NASA). Scrum calls the backlog emergent
  and expects to learn scope during work (Scrum Guide). The existing research's
  reconciliation ("complete within the increment, minimal across it",
  `2026-10-18-functions.md` §4) fits both.
- **Formal or informal.** Leveson, Heitmeyer and Heimdahl get mechanical completeness by
  making requirements formal state machines; mainstream practice uses checklists,
  models and reviews. The formal route is from safety-critical embedded systems
  (TCAS II, avionics, Navy).
- **Who decides a gap.** The customer and the requirements baseline in systems
  engineering; the Product Owner in Scrum; the stakeholders, re-interviewed, in
  requirements practice. All three put it outside the analyst.

## 5. How this relates to the existing research

- **Agrees with and adds to `2026-10-18-functions.md`.** Its reviewer checks R5
  (negative-space prompts) and R6 (stakeholder pass) are confirmed by Cockburn's process
  (actors over the life of the system, time-based triggers) and by Wiegers' list. It
  adds three families the file did not cover: event lists with temporal and signal
  events, data coverage (CRUD, counterparts, domain models), and Leveson-style state
  criteria. Its C10 flow check ("every function has at least one in and one out")
  matches NASA-GB-8719.13 E.3's first rule (every input used); E.3's second rule ("a
  legal value for an output that is never produced" means an omitted requirement) is
  new.
- **Qualifies `2026-10-18-functions.md` item 15.** Item 15 is right about naming
  functions; the sources here show CRUD is also an established completeness check, so
  the item should not be read as "do not think in CRUD". This is the closest thing to a
  contradiction found, and it is the one the N1 miss turns on.
- **Partly contradicts `2026-11-13-requirements.md` §3,** which says "I found no
  established method that walks each function through a fixed list of questions". That
  stays true per function, but walking every event (in every state) through a fixed
  question, "what is the response?", is an established method: event-response tables
  (Wiegers and Beatty) and the state-machine criteria (NASA-GB-8719.13 App. E). They
  walk events and states rather than functions.
- **Adds to `2026-11-14-function-inputs-outputs.md`,** which found functional FMEA
  silent on out-of-range input. NASA-GB-8719.13 App. E asks for the response to
  out-of-range input and for a time-out in every state; Lutz found omitted
  reasonableness checks on input among the commonest omissions (VERIFIED-secondary).
  This supports the inputs-and-outputs walk agreed there.
- **Agrees with `2026-11-13-requirements.md` §6** that NASA's checklists and traceability
  are the base checks; adds that a defined reading perspective outperforms a checklist
  in the one controlled experiment found.
- No finding here bears on `docs/out-of-scope/` (GitHub features, modelling the library,
  a teaching obligation).

## 6. What this means for datum's two steps (INFERRED)

Kept apart from the findings. Each point is a reading of the sources for datum, not a
decision.

- **Functional analysis has one coverage model, the scenarios.** The sources say one
  model finds only its own gaps. The cheapest second model for a small product is a
  data walk: for each item the builder gives or the part keeps, can the builder see it,
  change it and remove it, and if not, is that a choice they made? This would have
  found the N1 home town. It keeps item 15 intact: CRUD as a question, not as names.
- **Events, not only journeys.** A short event list with temporal events ("each
  morning", "at 8 o'clock") and outside-system events next to the scenarios would give
  the "first use, backup, other users" prompts in `writing-functions` a firmer base.
- **The reviewer's three clean passes fit the evidence.** An unstructured or checklist
  review is the weakest reading technique in the one controlled comparison found. A
  reviewer given a perspective ("read as the builder using it on a later day; read as
  the builder who has moved town") is closer to what was shown to work.
- **The builder is the external-completeness check, and the sources treat them as
  such.** The end condition "the builder has gone through the set of functions and
  agrees it covers what they expect" is datum's version of narrating the story map. In
  the fixture this was simulated, so the test could not exercise it. The sources
  suggest the walk is more useful as a narration with prompts (Pitts and Browne) than
  as a list to approve.
- **A gap found in the requirements step should go back, by rule.** Every process
  source sends a late-found gap to the earlier artifact and to whoever owns the need,
  under change control. `writing-requirements` already says "Something the walk finds
  missing… goes back to the step that owns it", but the requirements step has no end
  condition or order step that makes it happen: no question to the builder about
  missing functions, no reopening of the functional-analysis step. The sources would
  have it raise the gap with the builder in the step's batch, and, if agreed, reopen
  functional analysis (its closed step goes stale), not write a requirement around it.
- **No method makes a set complete.** Datum should keep claiming "complete for its
  scope, against these checks", naming the checks, and not "complete".
