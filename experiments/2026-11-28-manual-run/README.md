# Manual run to the end of the requirements step (2026-11-28)

**Question.** With a real person as the builder, over many turns, does datum go from the
first call through functional analysis to a closed requirements step without inventing
values, and do the forced lines make it call the `researcher` and `spiker` agents? It
tests what a one-turn rig cannot (lesson 20, `research/2026-11-14-requirements-test.md`):
grilling, the four whole-part areas, the review loop and the builder's batch. Issue #66;
it also touches #67-#70, #33 and the two agents.

**What it is not.** One run (N=1): it finds failure modes; it is not evidence that a fix
works. That is #74 and #54.

**State (2026-11-28):** set up, not run.

## The product

A static-fire log analyser, used on a laptop. It reads the CSV of one load-cell test of a
small solid rocket motor (time, thrust) and prints the peak thrust, the burn time, the
total impulse and the motor's impulse class letter; a thrust-curve plot is the builder's
call. One input file, one calculation, one report: no service, no stored data, no user
interface beyond the command line, so synthesis has no reason to split it into parts.

Chosen because it holds both things the run needs:

- **An established value:** the impulse class boundaries, and how burn time is defined,
  come from the rocketry bodies' standards. They should come from the `researcher`, not
  from memory.
- **A doubt settled only by measuring:** whether a long, high-rate log (for example
  10 kHz for 30 s) loads and is processed fast enough, or how much filtering the noise
  moves the impulse. That is the `spiker`'s.

It is not the deduper, the skill examples' products or the fixtures' expense splitter.

## Method

1. `python3 setup.py` makes `~/datum-run/` outside the repository (lesson 18): the plugin
   built from `main`, an empty git repository `product/`, a fresh Claude config
   `config/` (no personal skills, plugins, settings or memories), `notes.md`, and the
   datum commit.
2. Before the run, Amit writes a short intent sheet, kept outside `~/datum-run/`: what
   the tool must do, what he would answer, and what he does not know (for example the
   exact class boundaries, or whether plain Python is fast enough). It keeps the answers
   consistent and shows afterwards what datum missed.
3. In `product/`: `CLAUDE_CONFIG_DIR=~/datum-run/config claude --plugin-dir
   ~/datum-run/plugin --model sonnet`, then `/login`, then `/datum:datum` and a few
   lines about the product. Sonnet, as in the earlier tests. Fork mode stays on (the
   default), so the "wait for the findings" clause is tested as a builder would meet it.
4. The run ends when the requirements step closes (a clean closing review and the
   builder's agreement), or at a failure that blocks it.
5. `python3 collect.py` copies the transcripts, the model, the product's git log and the
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
| O1 | The `researcher` was called before the class boundaries (or any other established value) entered the model, and its `RES-` record quotes a source | transcript (Agent call before the write), `analysis/RES-*` |
| O2 | The `spiker` was called for the measurable doubt, and its `SPK-` record holds the commands and their raw output, the median and range, and the machine | transcript, `analysis/SPK-*`, `analysis/spikes/` |
| O3 | Grilling left an entry for each of the four whole-part areas (where it runs, the people, standards and legal, getting it into use) | `analysis/ELI-*` |
| O4 | No number or rule entered the model without a record, the builder's answer or a `TBD` | model files against the transcript |
| O5 | Each review's findings came back before the step reported or went on | transcript |
| O6 | A missing function found in requirements went back to functional analysis instead of being written around (scored only if one came up) | transcript, functions |
| O7 | The reviewer agents ran with their `skills:` loaded (#33) | subagent transcripts |
| O8 | The requirements step closed with a clean closing review and the builder's agreement, recorded in `steps.yaml` | `steps.yaml`, transcript |

Impressions go in their own section of the result and score nothing.

## Result

Not run yet.
