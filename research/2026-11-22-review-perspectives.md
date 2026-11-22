# How reading techniques for requirements review were worded (2026-11-22)

Question: how exactly were the reading techniques in the original requirements-review
experiments worded and structured? What procedure text was a reviewer handed? Follow-up
to `2026-11-15-functional-completeness.md` §2.2 and §3, which had only abstracts.

Labels: **VERIFIED** = I read it in a primary source (source and section or page
given). **VERIFIED-secondary** = only an abstract, summary or third-party page was seen
(named). **INFERRED** = my reasoning. Page numbers are printed page numbers unless I say
PDF page. Quotes are short; everything else is my paraphrase.

## Summary

1. **Every technique has the same two-part shape: build something, and answer fixed
   questions while building it.** PBR readers build a test suite, a design or a set of
   operational scenarios. The defect-based readers (Porter et al.) build a table of data
   objects, an invariant per mode, or a list of events, and answer questions about it.
   The authors call this a "proactive process-driven scenario": VERIFIED.
2. **PBR has three perspectives with three procedures.** Tester: make tests for each
   requirement (5 questions). Designer: make a design (6 questions). User: define the
   functions a user must be able to perform, their inputs and outputs, and write
   operational scenarios from nominal to rare (6 questions). VERIFIED (lab package forms
   E6T, E6D, E6U; the tester text also in the technical report).
3. **Porter et al. have three scenarios, each derived from checklist items.** Data type
   consistency, incorrect functionality, ambiguity or missing functionality. Each is a
   numbered procedure with sub-questions. VERIFIED (Appendix, pp.14-16).
4. **The comparison conditions were weak by design.** Ad hoc reviewers got a fault
   taxonomy and nothing else. Checklist reviewers got one general checklist of
   questions. The authors call checklists "nonsystematic" because the questions are
   general and give no strategy for answering them. VERIFIED.
5. **The authors' account of why it works is "specific, distinct responsibility plus a
   method for meeting it".** It is not a tested mechanism. In Porter et al. the gain
   was tied to scenario content (reviewers found more of the faults their scenario
   targeted, and no more of the others). VERIFIED for what the paper says. The wider
   explanation of why PBR works is INFERRED here and was not tested in what I read.
6. **Replications are mixed.** A Brazilian replication pair found PBR better on one
   document and, in the first replication, worse than a checklist on the other on one
   metric. Experience in the role did not matter. VERIFIED (UMD technical report T136).
7. **Not reached:** the later PBR papers (Shull, Rus, Basili 2000; Laitenberger et al.
   2001) and the journal versions. See below.

## What was and was not read

Read (VERIFIED):
- **Porter, Votta, Basili, "Comparing Detection Methods for Software Requirements
  Inspections: A Replicated Experiment"**, UMD technical report CS-TR-3327.1 (the
  preprint of the IEEE TSE 21(6), 1995 paper), 16 PDF pages, via
  https://drum.lib.umd.edu/items/96204769-6905-4196-b903-709ad81148ee/full (file
  `CS-TR-3327.1.pdf`). The text layer is spaced oddly and was read through a cleanup;
  wording below was checked against it. The journal version itself was not read, so
  page numbers are the technical report's.
- **Basili, Green, Laitenberger, Lanubile, Shull, Sørumgård, Zelkowitz, "The Empirical
  Investigation of Perspective-Based Reading"**, as the technical report ISERN-96-06
  (38 PDF pages): https://www.cs.umd.edu/~mvz/handouts/emp_pbr.pdf. This is the report
  that the lab package calls its summary paper. It is not the EMSE 1(2), 1996 journal
  text; I could not confirm the two are word for word the same. Read §1 in full, §2-3
  for results and the experience findings.
- **PBR lab package**, forms E6T, E6D, E6U (reading scenarios for tester, designer,
  user): https://www.cs.umd.edu/projects/SoftEng/ESEG/manual/pbr_package/docs/6_test.ps
  (and `6_desig.ps`, `6_user.ps`; index at
  https://www.cs.umd.edu/projects/SoftEng/ESEG/manual/pbr_package/download.html).
  PostScript text extracted by script; word spacing was lost and rebuilt by hand, so
  the exact line breaks and any figures are not checked. Each form is one page.
- **Fabbri et al., "Data Analysis of the First Two PBR Replications in Readers
  Project"**, UMD technical report T136: https://www.cs.umd.edu/users/basili/publications/technical/T136.pdf.
  Read the abstract, §1-3 summary and the results discussion of R1 and R2 in part. §5
  (conclusions) and the threats section were not read.

Seen only through search summaries or abstracts (VERIFIED-secondary):
- Shull, Rus, Basili, "How Perspective-Based Reading Can Improve Requirements
  Inspections", IEEE Computer 33(7), 2000: citation and a one-line abstract only.
  **Not read.**
- Laitenberger et al., IEEE TSE 2001 (PBR against checklist on code documents, three
  studies, 60 professionals at one company): search summary only. **Not read.**
- Fusaro, Lanubile, Visaggio, EMSE 1997 (replication of Porter et al.): a search
  summary says it found no evidence that scenarios did better. **Not read.**
- Ciolkowski et al. 1997 (ISERN replication in a university; PBR still helped): search
  summary. **Not read.**
- Maldonado et al. 2006, EMSE (PBR against checklist, individual effectiveness):
  abstract only. Regnell, Runeson, Thelin 2000, "Are the perspectives really
  different?": title only, seen in a reference list.

Not reached: the lab package for **requirements and object-oriented design** (the
"tbr package", https://www.cs.umd.edu/projects/SoftEng/ESEG/manual/tbr_package/): I saw
its page structure only, and its `readingtechniques.ps` was fetched but I did not read
it (its visible text was about design reading, not requirements). Shull's thesis. The
slides `Day1.ps` and `Day2.ps`. The PBR examples (`examples/*.ps`). The IEEE
Xplore versions of all papers. A search for NASA SEL internal reports on PBR returned
nothing usable.

## 1. Perspective-based reading (PBR)

**Design.** Each reader builds a model and then answers questions about it. "An
operational scenario requires the reader to first create a model of the product, and
then answer questions based on analyzing the model with a particular emphasis."
VERIFIED (ISERN-96-06 §1.1, p.3). The report lists wanted properties of a technique:
detailed, specific (one purpose per reader), focused (a combination of readers gives
full coverage), tailorable. VERIFIED (§1.1, p.3). The assumption is that "the union of
the perspectives provides extensive coverage of the document, yet each reader is
responsible for a narrowly focused view". VERIFIED (§1.2, p.5).

**What each perspective builds.** Tester: "design a set of tests for a potential test
plan". Developer: "generate a high level design". User: "create a user's manual".
VERIFIED (§1.2, pp.4-5). The experiment forms then changed the user's artifact: the
user reader writes operational scenarios, not a manual (see below).

**Preamble on every form.** Customers of a document should read it "in such a way as to
find out if the document satisfies their needs for it". VERIFIED (forms E6T, E6D, E6U).

**Tester (form E6T, "Test-based Reading").** Build: "generate a test or set of tests"
for each requirement or functional specification so an implementation can be shown to
satisfy it; "use your standard test approach and technique, and incorporate test
criteria". Then ask, for each test (VERIFIED, E6T; ISERN-96-06 §1.2 has the same five
questions in slightly different words and order):
1. Do you have all the information needed to identify the item being tested and the test
   criteria? Can you make a reasonable test case for each item?
2. Can you be sure the tests will give the correct values in the correct units?
3. Are there other interpretations of the requirement that the implementer might
   make? Will this affect the tests?
4. Is there another requirement for which you would make a similar test but get a
   contradictory result?
5. Does the requirement make sense from what you know about the application or from
   the general description?

**Designer (form E6D, "Design-based Reading").** Build: "Generate a design of the system
from which the system can be implemented", with "all necessary data objects, data
structures and functions". Ask "throughout the design" (VERIFIED, E6D):
1. Are all necessary objects (data, data structures, functions) defined?
2. Are all interfaces specified and consistent?
3. Can all data types be defined (is the required precision and unit specified)?
4. Is all the information available to do the design? Are all conditions involving all
   objects specified (are any requirements missing)?
5. Are there points where you are unclear what to do because the requirement is not
   clear or not consistent?
6. Does the requirement make sense from what you know about the application or the
   general description?

**User (form E6U, "Use-based Reading").** Build: "Define the set of functions that a
user of the system should be able to perform", then the input objects each function
needs and the output objects it generates. "This may be viewed as writing down all
operational scenarios". The order is "Start with the most obvious or nominal scenarios,
and proceed to the least common scenarios or special/contingency conditions." Ask for
each scenario (VERIFIED, E6U):
1. Are all the functions needed to write the operational scenarios specified in the
   requirements (are all capabilities in the general description specified)?
2. Are the initial conditions for starting the scenario clear and correct?
3. Are the interfaces between functions well defined and compatible (do the inputs of
   one function link to the outputs of the previous one)?
4. Can you get into a system state that must be avoided (for safety or security)?
5. Might part of the scenario give different answers depending on how a requirement is
   interpreted?
6. Does the requirement make sense from what you know about the application or the
   general description?

**Patterns visible in the three procedures (INFERRED from the text above).**
- The last question is the same in all three ("does it make sense against what you know
  of the application"). It is the check that does not depend on the artifact.
- Each procedure has one question about missing information, one about interpretation
  or conflict, and one about interfaces or units. The building step forces the reader
  to need the information, so a gap shows as "I cannot write this".
- Only the user procedure orders its work (nominal first, rare cases last) and asks
  about states to avoid. Only the tester procedure asks about a contradiction between
  two requirements.

**What the experiment found (secondary to the technique).** In the pilot, PBR readers
scored 24.92 against 20.58 for the usual technique, not significant. In the 1995 run,
32.14 against 24.64, significant, a 30% improvement. Years of role experience did not
predict PBR defect rate. VERIFIED (ISERN-96-06 §3). The same report lists history,
maturation and testing as threats: day one used the usual technique and day two used
PBR, so some of the gain may be practice. VERIFIED (§4). The 1996 summary in the earlier
file stands, and this adds that the gain was partly confounded.

## 2. Defect-based (scenario-based) reading: Porter, Votta, Basili

**Three conditions.** All reviewers searched the same populations of fault in an SRS
(WLMS, CRUISE; ELEVATOR for training). The tools were nested: Ad Hoc (everything),
Checklist (a subset), Scenario (a subset of the checklist). VERIFIED (§II.B.2, Fig. 2).

**Ad hoc.** Defined by the fault taxonomy, which each reviewer got. "Ad Hoc reviewers
received no further assistance." The taxonomy has omission (missing functionality,
performance, environment, interface) and commission (ambiguous information,
inconsistent information, incorrect or extra functionality, wrong section). Each has a
one-sentence definition, such as "Information describing the desired internal
operational behavior of the system has been omitted from the SRS." VERIFIED (§II.B.2
and Appendix I, p.14).

**Checklist.** One checklist for all reviewers, made by filling the taxonomy "with
detailed questions culled from several industrial checklists". It has a General group
(for example "Are the goals of the system defined?", "Are the requirements clear and
unambiguous?") and one group per fault category. Examples under Missing Functionality:
"Are undesired events considered and their required responses specified?" and "Are the
initial and special states considered?" Under Incorrect or Extra Functionality: "Are all
the outputs produced by a function used by another function or transferred across an
external interface?" VERIFIED (§II.B.2; Appendix II, pp.14-15).

**Scenarios.** Built from the checklist "by replacing individual Checklist items with
procedures designed to implement them". Each reviewer executes one scenario; reviewers
are coordinated to cover the document. VERIFIED (§I.C, §II.B.2). The authors estimate
the three scenarios address about half of the faults the checklist covers. VERIFIED
(§II.B.2). The scenarios assume an SCR-style SRS with inputs, outputs, events and
modes. VERIFIED that the SRS notation is SCR in part (§II.B.1); that the steps assume it is INFERRED.

**Scenario A, data type consistency (Appendix III.A, p.15).** Paraphrase:
1. Identify all data objects named in the overview. Are they all listed in the external
   interface section?
2. For each object in that section, write down: name, class (input port, output port,
   application variable, abbreviated term, function), data type, acceptable values,
   failure value, units or rates, initial value. Then ask: is it consistent with the
   overview? Are units given for a physical quantity? If its value is computed, can it
   produce an unacceptable value?
3. For each functional requirement, list its data object references. Do they follow
   conventions? Are they listed as inputs or outputs? Can any use or definition be
   inconsistent with the object's type, values or failure value?

**Scenario B, incorrect functionality (Appendix III.B, p.15).**
1. For each functional requirement, identify the input and output data objects. Are all
   values written to each output consistent with its intended function? "Identify at
   least one function that uses each output data object."
2. For each functional requirement, identify the specified system events. Is the
   specification of the events consistent with their intended meaning?
3. "Develop an invariant for each system mode." Can the initial conditions fail the
   initial mode's invariant? Find an event sequence that enters a mode without meeting
   its invariant. Find one that enters a mode and never leaves it (deadlock).

**Scenario C, ambiguity or missing functionality (Appendix III.C, pp.15-16).**
1. Identify the required precision and response time for each functional requirement.
   Are all required precisions given?
2. For each requirement, identify all monitored events. Is there an event sequence for
   which several output values can be computed? One for which no output value will be
   computed?
3. For each system mode, identify all monitored events. Is there an event sequence for
   which transitions into two or more modes are allowed?

All of VERIFIED (Appendix III). Scenario B's step 1(b) is the same rule as NASA's
"every output has a user" cited in `2026-11-15-functional-completeness.md` §1.4
(INFERRED link; the paper does not cite that source).

**What the authors say about checklists.** Checklists "often pose questions that help
reviewers discover faults", but "the generality of these questions and the lack of
concrete strategies for answering them makes the approach nonsystematic". They cite
Parnas and Weiss's "active design reviews": each reviewer reads for a specific
purpose, with specialised questionnaires. VERIFIED (§I.B-C). The PBR report repeats the
Porter results: scenario readers did better by about 35%, were no worse on other
defects, and checklist reading was no better than ad hoc. VERIFIED (ISERN-96-06 §1.1,
p.4, reporting Porter 1995).

**Does the content or the method matter?** Scenario reviewers were best at the faults
their own scenario targeted and no better than others at the rest. The authors read
this as showing that the content of the scenario, not just having a scenario, drove the
gain. VERIFIED (analysis section on individual performance, part C; section number not noted).
Scenario reviewers were also generally no better than other scenario reviewers at
faults their own scenario did not target. The abstract's finding that collection
meetings added little was not re-checked.

## 3. Later work on what makes a perspective or scenario effective (short)

- **Active against passive is the authors' own framing.** Porter et al. and the PBR
  report both use "active" (Parnas and Weiss) to mean a reviewer who produces something
  while reading. No source I read isolates this as a factor: no experiment compares the
  same questions with and without the building step. That is INFERRED as a gap.
- **Replications, VERIFIED (T136).** Two undergraduate replications compared PBR with
  a checklist. On the ATM document PBR did slightly better in both. On the PG document,
  in the first replication, the checklist beat PBR on effectiveness, and in the second
  PBR did better, "almost an inversion". Pooled, PBR did better on both documents. The
  authors point to differences in subject profile and motivation, timing, and the
  trainer's experience as sources of variation. They note the document had a significant
  effect. Role experience "appeared to have little impact". The perspectives found
  complementary defects, with some found by one perspective only.
- **Other replications, VERIFIED-secondary (search summaries only).** Fusaro et al.
  1997 reported no evidence that scenarios beat the other methods. Ciolkowski et al.
  1997 reported that PBR still helped in a university. Laitenberger et al. 2001
  compared PBR with a checklist on code. The reasons these papers give for the
  differences were not seen.
- **What I could not check:** whether Shull, Rus and Basili (2000) say why PBR works,
  or what Regnell et al. found about whether perspectives really differ. Any claim
  beyond the above would be from memory and is left out.

## What this means for datum (INFERRED)

Kept apart from the findings. A reading of the sources, not a decision.

- **The sources support the structure.** One reading per view, from a stated reviewer
  perspective, with a fixed set of questions, is the structure of both families. Each
  reader has one narrow purpose. Coverage comes from combining readers. The sources
  split the work by view or perspective in the same way (scenarios, data, events, modes).
- **"One fixed question" per view is thinner than the sources.** Every procedure has
  three to six questions, and many have sub-questions. This is a design choice for
  datum, not something the sources test. A single question per view may work because
  the building step carries the work. That is not shown by anything I read.
- **The wording pattern is "build X, and while building it answer these questions".**
  The tester, designer and user forms all say it in this order: an instruction to
  produce an artifact, then "in doing so, ask yourself the following questions".
  The artifact has a defined form (tests, design, scenarios; a table of data objects;
  an invariant per mode). The questions are about missing information, interfaces and
  units, interpretation and conflict, and whether it makes sense.
- **Views datum names map onto the sources.** Scenarios are the user form (E6U), which
  also asks for nominal first and rare last. Data kept by the product is Porter's
  scenario A (a table of every data object with type, values, units, initial value)
  and scenario B step 1 (each output has a user). Events including timed ones are
  Porter's scenario B step 2 and scenario C steps 2-3 (every event, every mode). None
  of the sources asks "can the user see and change what the product stores" as a named
  question; scenario B 1(b) and the PBR user question 3 come closest. The N1 miss would
  need that question written.
- **A building step for each view looks like the useful part.** The weakest condition
  in the experiment was the checklist, which has the same questions without a thing to
  build. The sources do not prove that the building is the cause (§3), so this is a
  reason to try it, not a result.
- **The human's own walk-through is not tested in these sources.** Both families use
  reviewers who read the document; neither includes the author or customer walking
  through it. The story-map and use-case sources in `2026-11-15-functional-completeness.md`
  §1.1 cover that, not these.
- **Check against the evidence limits.** The gains are 20-35% in detection rate, with
  mixed replications, small samples, mostly student subjects, and documents with a
  structured notation (SCR) for Porter et al. Say "this found more in these studies",
  not "this finds the gaps".
