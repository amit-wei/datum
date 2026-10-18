# Packaging test: queries and fixtures

Question: should a technique be its own skill, or a reference file inside each step that
uses it?

## Variants

| Code | Techniques packaged as | A correct load is |
|---|---|---|
| S | Separate skills, listed | A Skill call to the technique |
| R | Reference files inside each step skill | A Read of `references/<technique>.md` |

A third variant, H (skills hidden with `disable-model-invocation: true`, called only by
steps), was dropped after the Sonnet pilot: Claude Code refuses to load such a skill
through the Skill tool and tells the agent to ask the user to run it.

The description text is the same in both variants; in R it is the step's pointer line.
All 19 planned techniques, 9 steps (the router `datum` among them) and 6 per-step
reviewer agents are present; only the router, 3 steps and 8 techniques have real
bodies, the rest are stubs. Runs happen in the
builder's real setup, with their other skills listed.

Models: Sonnet 5.5 and Haiku 5.5; Opus 5.5 only if Sonnet falls short (cost). Each
query 3 times per variant per model: 23 × 3 × 2 × 2 = 276 runs. A pilot of about 5
queries per model first measures the cost per run. Train/validation split about 60/40,
fixed before the first run.

## Decision rule (fixed before the runs)

The variant with the most correct loads on the validation queries wins; on a tie, S
(no copies to keep in sync). A variant that wins on some models only is reported, not
chosen, and the builder decides.

## Example project

A fictional project: a tool that logs climbing sessions and suggests what to train
next. A fixture is a `model/` folder in a given state (written by `fixtures.py`). Every
fixture but F0 has a one-line project CLAUDE.md: "This project is built with datum.
Load the `datum` skill before any work in this project."

| Fixture | State |
|---|---|
| F0 | Empty repository |
| F1 | Product functional analysis open; an elicitation record and two scenarios exist |
| F2 | Functional analysis closed; requirements open; functions `FUN-3G1N` (log a session), `FUN-7SGT` (suggest training), `FUN-5YNC` (keep devices in sync); `REQ-7K3Q` (sync, p95 bound, with a typo) has no proof yet |
| F3 | Requirements closed, with proofs (including `REQ-B4DG`, suggestion shown within p95 1 s); synthesis open, no parts yet |
| F6 | Product synthesis open, parts and a decision exist; `REQ-B4DG` spans `app` and `suggest-engine` but has no child requirements |
| F7 | As F6 with `REQ-B4DG` flowed down and interfaces defined; synthesis closed, design evaluation open |
| F4 | Product steps 1–4 closed, cases open; part `suggest-engine` at its own functional analysis |
| F5 | As F4, with `suggest-engine`'s functional analysis and requirements closed |

Prompts are worded so they do not name the action: the agent has to reason from the
state to the right step or technique.

**How a row is scored** (`score.py`): Expected names, in backticks, must all load in
that order; anything under Must not must not even be attempted. `none` means no
technique loads; the router or a step may. Split: `val` rows decide, `train` rows may
be used to tune descriptions.

## Should trigger (12)

| # | Split | Fixture | Prompt | Expected | Why |
|---|---|---|---|---|---|
| P1 | train | F0 | I want to build a tool that tracks my climbing sessions and suggests what to train next. | `functional-analysis` then `grilling` | A new product; grilling is forced first |
| P2 | val | F1 | I think we've got what people need. What now? | `writing-scenarios` | Needs drawn out; scenarios are forced next |
| P3 | train | F2 | Let's pin down logging a session. | `writing-requirements` | `FUN-3G1N` has no requirement |
| P4 | train | F2 | REQ-7K3Q looks finished to me. | `writing-proofs` | It has no proof |
| P5 | val | F3 | Where should the session data live? | `trade-study` | A design choice with credible options |
| P6 | train | F1 | Surely someone has built this already. | `research` | Possible existing solution |
| P7 | train | F1 | People will train based on what this tells them. | `losses-and-hazards` | A function can cause harm |
| P8 | val | F4 | Let's work on the suggestion engine. | `writing-functions` | The part is at its own functional analysis |
| P9 | train | F2 | We need something on how long session data is kept. | `grilling` | A requirement whose value only the builder knows |
| P10 | train | F2 | Okay, I'm happy with the functions. | `requirements` | The next step |
| P11 | val | F3 | This should use up to 512 MB of RAM. | `grilling` | A builder constraint (a target device) or a requirement a later choice should derive? |
| P12 | train | F6 | So are we done with requirements? | `review-synthesis` then `allocating-requirements` | `REQ-B4DG`'s budget is not flowed down; flowdown is in synthesis's end condition |

## Near-misses (11): the obvious neighbour is wrong

| # | Split | Fixture | Prompt | Expected | Must not | Why |
|---|---|---|---|---|---|---|
| N1 | train | F2 | There's a typo in REQ-7K3Q. | `none` | `writing-requirements` | A direct edit |
| N2 | val | F2 | What does EARS stand for? | `none` | `writing-requirements` | An answer |
| N3 | train | F4 | The sync proof needs to run in CI. | `writing-cases` | `writing-proofs` | The proof exists; its executable form does not |
| N4 | train | F2 | Users want streaks too. | `functional-analysis` | `writing-requirements` | No function for it yet |
| N5 | val | F3 | SQLite on the device: anything to worry about? | `architectural-risk-pass` | `losses-and-hazards` | A risk of a design choice, not of a function |
| N6 | train | F7 | Does the design actually support logging a session? | `walking-scenarios` | `writing-scenarios` | Design evaluation |
| N7 | train | F3 | Which of these two scenarios is more realistic? | `none` | `trade-study`, `writing-scenarios` | An opinion or a review, not a design choice |
| N8 | val | F2 | What's the best way to define training load? | `research` | `grilling` | An established convention; the other wording is "What's the convention for training load?" |
| N9 | val | F5 | What's the next decomposition of this part? | `synthesis` then `applying-stopping-rule` | `writing-functions` | Its functions are done; at F4 `writing-functions` would be right |
| N10 | train | F1 | I like short answers. | `none` | `grilling` | Personal, outside the model |
| N11 | val | F3 | Supabase's free tier would cover us, right? | `research` | | Pricing changes; an answer from memory fails |

## Part B: mid-run fixtures (run once the router is drafted)

Each fixture comes with an expected finding, written before the runs and checked by a
reviewer agent. Prompt: "Continue."

| # | State | Expected finding |
|---|---|---|
| B1 | Requirements half done: two of three functions have requirements | Resumes at the third function; rewrites nothing |
| B2 | Leaf part whose allocated latency budgets add up to more than the parent's bound | Raises it to the parent level; does not change the parent or work around it |
| B3 | A function edited after functional analysis closed | Router reports functional analysis stale and sends work there first |
| B4 | Asked to add "export sessions" when a function for it already exists | Finds the existing function; does not add a second |
| B5 | A requirement `justified_by` a decision that has been superseded | Flags the requirement for review against the new decision |

## Open for the builder

- More near-misses with systems-engineering nuance (a constraint vs a derived
  requirement, a budget vs a requirement).
