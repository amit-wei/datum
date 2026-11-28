# Manual run to the end of the requirements step (2026-11-28)

**Question.** With a real person as the builder, over many turns, does datum go from the
first call through functional analysis to a closed requirements step without inventing
values, and do the forced lines make it call the `researcher` and `spiker` agents? It
tests what a one-turn rig cannot (lesson 20, `research/2026-11-14-requirements-test.md`):
grilling, the four whole-part areas, the review loop and the builder's batch. Issue #66;
it also touches #67-#70, #33 and the two agents.

**What it is not.** One run (N=1): it finds failure modes; it is not evidence that a fix
works. That is #74 and #54.

**State (2026-11-28):** done. Result below; the findings have issues.

## The product

A pilot's logbook, for one glider or light-aircraft pilot on their own device. It logs
flights, keeps running totals, shows whether the pilot is current to fly and to carry
passengers, exports the logbook, and may fill a flight in from the glider's IGC track
file. One user, one device, local data, no server: synthesis has no reason to split it
into parts.

Chosen because datum should add something Claude alone would not: vague needs ("like my
paper logbook") for grilling, a dozen functions that interact (totals feed the currency
check; editing a past flight changes both), real hazards (a wrong total, or "current"
shown when the pilot is not), and both things the run needs:

- **Established values:** the fields a logbook must hold (EASA Part-FCL, FCL.050), the
  recency rule for carrying passengers (FCL.060), and how the IGC format records a
  track. They should come from the `researcher`, not from memory.
- **A doubt settled only by measuring:** whether take-off and landing times can be found
  reliably from an IGC track, given noisy ground speed and altitude, a ground run or a
  winch launch. That is the `spiker`'s, on sample files.

It is not the deduper, the skill examples' products or the fixtures' expense splitter.

## Method

1. `uv run setup.py` makes `~/datum-run/` outside the repository (lesson 18): the plugin
   built from `main`, an empty git repository `product/`, a fresh Claude config
   `config/` (no personal skills, plugins, settings or memories), `notes.md`, and the
   datum commit.
2. Before the run, Amit writes a short intent sheet, kept outside `~/datum-run/`: what
   the logbook must do, what he would answer, and what he does not know (for example
   which fields FCL.050 requires, or whether a track gives reliable take-off times). It keeps the answers
   consistent and shows afterwards what datum missed.
3. In `product/`: `CLAUDE_CONFIG_DIR=~/datum-run/config claude --plugin-dir
   ~/datum-run/plugin --model sonnet`, then `/login`, then `/datum:datum` and a few
   lines about the product. Sonnet, as in the earlier tests. Fork mode stays on (the
   default), so the "wait for the findings" clause is tested as a builder would meet it.
4. The run ends when the requirements step closes (a clean closing review and the
   builder's agreement), or at a failure that blocks it.
5. `uv run collect.py` copies the transcripts, the model, the product's git log and the
   notes into `results/`, with the home folder and user name replaced. Read it for
   anything personal before committing.
6. The outcomes below are scored from `results/`, not from impressions.

Issues: the run opens none, and that is accepted (Amit, 2026-11-28). A `TBD` counts as
handled when the run says how it would be settled.

## Guidelines for the builder

- **Be the builder, not datum's designer.** Never name agents, records, steps or
  techniques, and do not steer toward one.
- **Say "I don't know" where a builder would not know,** even when you do. That gap is
  what should trigger research or a spike.
- **Do not rescue it.** If it goes wrong, let it, and note the turn. If it stops early,
  nudge as a builder would ("is that everything?"), not "run the reviewer".
- **Agree only when you would.**
- **Deny any read outside `product/`;** your intent sheet and notes are there.
- **Notes:** the turn, what happened, and, in a column apart, your impression.

## Outcomes (pre-registered; yes or no from `results/`)

| # | Outcome | Read from |
|---|---|---|
| O1 | The `researcher` was called before a legal field list or rule (or any other established value) entered the model, and its `RES-` record quotes a source | transcript (Agent call before the write), `analysis/RES-*` |
| O2 | The `spiker` was called for the measurable doubt, and its `SPK-` record holds the commands and their raw output, the median and range, and the machine | transcript, `analysis/SPK-*`, `analysis/spikes/` |
| O3 | Grilling left an entry for each of the four whole-part areas (where it runs, the people, standards and legal, getting it into use) | `analysis/ELI-*` |
| O4 | No number or rule entered the model without a record, the builder's answer or a `TBD` | model files against the transcript |
| O5 | Each review's findings came back before the step reported or went on | transcript |
| O6 | A missing function found in requirements went back to functional analysis instead of being written around (scored only if one came up) | transcript, functions |
| O7 | The reviewer agents ran with their `skills:` loaded (#33) | subagent transcripts |
| O8 | The requirements step closed with a clean closing review and the builder's agreement, recorded in `steps.yaml` | `steps.yaml`, transcript |

Impressions go in their own section of the result and score nothing.

## Result

Run 2026-11-28 on datum `b549cae`, Sonnet, two sessions (the builder cleared the context
after functional analysis closed, on datum's advice). Both steps closed with the
builder's agreement: 36 functions, 30 scenarios, 5 losses, 8 hazards, 204 requirements
with 204 proofs, 16 elicitation records, 6 `RES-` records, no `SPK-` record.
`results/product/` holds the model. The raw transcripts stay out of git
(`.gitignore`): they hold account details that the scrub does not remove. So does the
EASA page the researcher saved (Findings 4).

### Outcomes

| # | Result | Evidence |
|---|---|---|
| O1 | **Partly.** The `researcher` ran 8 times before the values it covers entered the model: logbook rules (RES-7H7D), existing apps (RES-XA6N), web-app storage (RES-X2SP), privacy law (RES-RZXY), unsigned flights (RES-70FV), sign-in limits (RES-6SKG). Every finding in all six records carries a quote. **Miss:** the sign-in and recovery limits (10 and 5 an hour), a security-standard value, entered the requirements draft with no source; research ran only after the builder asked "where do the 10 and 5 come from?" | main transcripts; `analysis/RES-*` |
| O2 | **Not tested.** The IGC fill-in, the planned spike trigger, was cut in round 2 on datum's recommendation (left out with automatic tracking). The one measurable doubt left, how Safari keeps stored data on a real iPhone, cannot be run from a laptop and was left open. | session 1, 09:59 and 10:08 |
| O3 | **Yes.** Entries for where it runs (devices), the people (language, accessibility), standards and legal (rules, privacy), getting it into use (installing, upkeep). All four were datum's proposals; the builder answered "sure" or "yes". | `analysis/ELI-*` |
| O4 | **No.** Besides O1's limits, datum proposed numbers without saying they were its own until the builder pushed ("seems pretty arbitrary"); from then on it labelled each one a judgement call. The `researcher` also found that a phrase quoted as official wording came from a research summary. | session 2, 11:25-11:42 |
| O5 | **Yes.** Every review was waited for. Once, datum asked a reviewer again for a report it had not received instead of calling the review clean. | timeline; session 2, 13:19 |
| O6 | **Yes.** The requirements step changed 9 functions, reopened functional analysis, ran its reviewer and added 5 scenarios before closing. | session 2, 11:52-11:58 |
| O7 | **Yes.** Every reviewer subagent's transcript starts with its preloaded skills (#33). | `subagents/*.jsonl` |
| O8 | **No.** The builder agreed and `steps.yaml` closes both steps, but the requirements reviewer's last word was "clean once these three fixes are made"; it never reread the files, nor the later fixes from the functional review. | session 2, 13:19-13:20; `steps.yaml` |

### Findings beyond the outcomes

1. **Scope grew without a brake.** "An MVP for my future business", "simple" and "a web
   app?" became accounts, sync, conflicts, recovery, GDPR erasure and backups: 36
   functions and 204 requirements. Most review rounds in requirements were about account
   recovery. Datum never offered a smaller cut (local only, no accounts) once the builder
   asked for simplicity. INFERRED: nothing in functional analysis weighs scope; the
   increment step comes later.
2. **The builder's agreement thinned to a stamp.** Batches of up to 11 technical points
   got "sure", "idek dude agreed on your thing", "yes". The builder said "don't worry
   about the business, you're the product person". An end condition that rests on the
   builder's agreement is only as good as that agreement.
3. **The reviewer was reused across rounds.** The main agent continued the same reviewer
   by `SendMessage` (one requirements reviewer for about 8 rounds), so later rounds read
   with the earlier rounds in context: not a fresh reader. The conditional "clean once
   fixed" came from this.
4. **The researcher wrote into the product.** RES-7H7D's agent downloaded pages with
   `curl -o page.html` in the project root; datum noticed and kept it out of commits.
5. **Small:** datum committed the requirements to a new branch without asking; the run
   hit a usage limit mid-step; every functional-analysis review round after the first
   was a targeted one.
6. **Good:** datum said plainly what was not checked (sources not reread, nothing built,
   no pilot checked the rules), advised clearing the context at a closed step, and the
   next session picked up from the files.

### Review of the requirements (Claude, after the run)

All 204 requirements and their proofs read, grouped by function. A judgement, not a
scored outcome; the flying-rule checks are against memory of Part-FCL and Part-SFCL, not
a fresh reading.

**One by one, they are good.** Each is one EARS statement with a reason that cites an
elicitation entry, a scenario or a research finding, and a proof with a concrete pass
condition, often at the boundary (one day inside and outside a window, one failure short
of a cap). The flying rules hold the domain value Claude alone would likely miss: the
look-back windows defined to the day (REQ-8R8J), revalidation kept apart from renewal
(REQ-RP9J, REQ-WHAP), no result where a needed fact is missing (REQ-D8T8), no result
for land-and-sea holders rather than a guess (REQ-YZYS), and never "cleared to fly"
(REQ-YCQ7, REQ-XE2E). The thresholds spot-checked (FCL.740.A, SFCL.155, SFCL.160,
FCL.060) match. Strict readings are named as such.

**As a set, they are the wrong size and at the wrong level.**

| Group | Functions | Requirements |
|---|---|---|
| Accounts, identity, privacy | 13 | 74 |
| Sync, conflicts, updates | 4 | 29 |
| Logging, import, setup, history | 15 | 58 |
| Rules, totals, warnings | 3 | 35 |
| PDF | 1 | 8 |

- **Half the set is infrastructure the builder never asked for in detail.** The value
  of the product, the rules and totals, is 35 of 204.
- **They decide the design.** An online copy that confirms durable storage (REQ-2MA2), a
  one-time proof that replaces the last (REQ-GY5X), a browser list (REQ-5JDV), records
  made unreadable on connecting (REQ-M9E7), which functions need a connection
  (REQ-GNNK). Synthesis is left little to choose: a cloud-synced web app with accounts is
  already fixed.
- **A few statements are too big to check as one.** REQ-3KAM (unsigned flights, about
  800 characters, one rule with several exceptions), REQ-9MV4, REQ-E4BA, REQ-KPP1.
- **Cross-cutting concerns are repeated per function.** "While a device has not yet
  received all records" appears six times (totals, rules, PDF, data copy, warnings, the
  logbook); "if the device cannot store a change" three times.
- **Some are process or unbounded inspections:** a rule review no older than 90 days
  before a release (REQ-4M05) binds the builder, not the product; "no code reads these
  names for another purpose" (REQ-5BFN) has no end to the inspection.
- **The proofs need a large harness:** fault injection at every write step, corrupted
  sync in both directions, wrong device clocks, a simulated clock. Right for the
  hazards, but more verification than the MVP has build.

**Reading.** The parts are visible in the set: a rules engine (the high-severity
hazard, isolated, 27 requirements), the logbook and its import and export, and an
account and sync service. Split there, each part's requirements would be its own, and
the product level would hold perhaps a few dozen. This supports #78: the level rule is
what was missing, not the writing rules. INFERRED.

### Impressions (Amit)

It felt fine, but slow. The main way to use datum is probably long automated runs that
notify the builder when input is needed. The scope creep was plain. Amit's main point:
the run does not represent the systems-engineering process, because dividing into parts
is what keeps scope in check from the start; v0.1.0, with the product as the leaf, is
therefore not a real picture of datum. The open question is when things break into
parts, what a part's scope is, and how datum handles the split (#78, which also covers
Findings 1 and 2).

### Issues

#77 (researcher downloads, fixed), #78 (partition and scope), #79 (fresh reviewers, fewer
rounds), #80 (why TBDs are avoided), #81 (a spiker test, later). Not separate issues:
Findings 1 and 2 (in #78); O1's miss on datum's own default values (in #80, as
part of the cause).
