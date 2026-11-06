# Functional-analysis test: queries

Fixed before the first run. Fixtures are in `README.md`.

**A run passes** when the judge (Sonnet) finds it meets the Outcome, from its final
message and the files it changed. Outcomes describe substance, so a baseline run is not
failed for lacking datum's formats. Datum runs are also checked mechanically, reported
beside the verdict and not compared: the write check (each new model file follows the
technique that makes it), Must not (no listed skill loaded) and the validator (no
errors after the run). Expected loads are a diagnostic.

**Split:** `val` rows decide; `train` rows may be used to tune the skills. Pilots run
on `train` only (packaging-test lesson 16).

**Runs:** Haiku pilots on `train`, datum and baseline. Then Sonnet on all 14, datum and
baseline, once each, and behaviours 11 and 14 three times on datum.

**Decision rule:**
- Datum beats the baseline when it passes more `val` behaviours on Sonnet. With six
  behaviours this is a comparison, not a pass rate.
- #23 closes when 11 and 14 pass in all three Sonnet runs on datum. On a failure the
  technique changes and both run again.

Behaviours 11 and 14 share a prompt: the agent must tell the fixtures apart.

| # | Split | Fixture | Prompt | Expected | Must not | Outcome |
|---|---|---|---|---|---|---|
| B1 | train | A | I want to build a tool that logs my climbing sessions and suggests what to train next. Get it going. | `grilling` | | Asks the builder what they need before producing anything. Writes no functions, requirements, design or code. |
| B2 | val | D1 | Let's work on the suggestion engine. | `grilling` | `writing-functions` | Asks the builder at least one question about what the suggestion engine must do, and writes none of its functions in this run. |
| B3 | train | D1 | What does the suggestion engine have to deliver to everything around it? | | | Names all three: its part in suggesting what to train next (FUN-7SGT), the suggestion with its reason sent to the app (IFC-8DQF), and the weekly load limit (REQ-Z3NP). |
| B4 | val | C | Add a function: the suggestion must appear within one second. | | `losses-and-hazards` | Adds no function for it. Says this is a limit on the existing suggesting function, not a function, and keeps it for a requirement or asks the builder. |
| B5 | train | D1 | The suggestion engine's requirements are all in its folder. Work from those and draft its functions. | | | Points out that REQ-Z3NP (four weeks of history) and REQ-M8YD (latest session only) cannot both hold, and raises this with the builder or as an issue. Does not settle it alone: changes neither requirement and writes no function that assumes one of them away. |
| B6 | val | C | Are we done with functional analysis? | | | Says it is not done, and names the wish to see grades over a season (entry 5) as covered by no scenario. |
| B7 | train | C | It should feel more social. | | | Writes no vague function. Either asks what the builder means by social, or names concrete acts as proposals for the builder to confirm. |
| B8 | train | C | How fast does the suggestion need to be? | | `writing-functions` | Treats this as a limit on the suggesting function. Gives no number as settled and writes none to the project; asks the builder for it, or says it comes later. |
| B9 | val | C | Should the suggestions run on the phone or on a server? | | `writing-functions` | Records no choice as made and changes no project file. Compares the options, or says this is a design choice that waits until requirements are known. |
| B10 | train | C | The functions look right to me. What's next? | `losses-and-hazards` | | Moves on to what must never happen, using the builder's answer about losing their history (entry 4), and writes or proposes that loss with at least one state of the product that leads to it. Does not start on requirements or design. |
| B11 | val | D2 | The suggestion engine's functions are agreed. Is there anything about them that could hurt someone that we haven't already dealt with? | `losses-and-hazards` | | Says that suggesting too much weekly load is already dealt with (REQ-Z3NP). Does not write or propose it as a new hazard of the suggestion engine. A different hazard, if it names one, does not fail the run. |
| B12 | train | B | The scenarios are right. Write the functions. | `writing-functions` | | Every function written or proposed does a step in a scenario. None names a technology or a number. Anything beyond the scenarios appears only as a question, not as a function. |
| B13 | val | B | The scenarios are right. Add whatever else a good climbing app should have. | | | Writes no new function or scenario. Proposes ideas as questions or issues for the builder, or starts grilling or research. |
| B14 | train | D3 | The suggestion engine's functions are agreed. Is there anything about them that could hurt someone that we haven't already dealt with? | `losses-and-hazards` | | Names a state of the exercise choice that can injure the climber while staying within the weekly limit of REQ-Z3NP, such as hard exercises repeated on the same fingers. Writes or proposes it as a new hazard, not as already dealt with. |

## Rerun

Added after the first runs, which had three faults in the test, not the skills: Bash
was refused, so the router could not check for stale steps and no ID could be made; the
product's `cases` step was open, so the router's order pointed away from the child; and
the shared prompt of B11 and B14 asked for hazards outright. All fixtures with a child
now close `cases`, and the rig approves the shell commands the skills use.

The technique also changed: the same state by another cause is not a new hazard.

B2 and B11 are no longer unseen, so these rows are evidence, not a held-out check. Datum
three times, baseline once, on Sonnet. #23's rule now reads on B11r and B14r.

A second rerun of B11r and B14r follows (`results/rerun2-sonnet.jsonl`), because all six
datum runs in the first grilled a part already grilled. The step now forces grilling only
when a part has no elicitation record. No run grilled again, but all stopped at a fixture
fault: D2 and D3 had no function for the reason or the load, so the agent rightly raised
those obligations first. A third and last rerun follows on completed fixtures
(`results/rerun3-sonnet.jsonl`).

| # | Split | Fixture | Prompt | Expected | Must not | Outcome |
|---|---|---|---|---|---|---|
| B2r | rerun | D1 | Let's work on the suggestion engine. | `grilling` | `writing-functions` | Asks the builder at least one question about what the suggestion engine must do, and writes none of its functions in this run. |
| B11r | rerun | D2 | Carry on with the suggestion engine. | `losses-and-hazards` | | Goes on to check the engine's functions for what could hurt someone. Does not write or propose as a new hazard either suggesting too much weekly load, or a cause of that such as a wrong load estimate. A different state, such as load within the cap that is the wrong kind, does not fail the run. |
| B14r | rerun | D3 | Carry on with the suggestion engine. | `losses-and-hazards` | | Goes on to check the engine's functions for what could hurt someone. Names a state of the exercise choice that can injure the climber while staying within the weekly limit of REQ-Z3NP, and writes or proposes it as a new hazard. |
