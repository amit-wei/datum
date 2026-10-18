# Schema trial and layout simulation (2026-10-16)

The rig and raw outputs behind two research notes. The findings, their VERIFIED and
INFERRED labels, and the threats to validity are in the notes, not here:

- [`research/2026-10-16-schema-trial.md`](../../research/2026-10-16-schema-trial.md)
- [`research/2026-10-16-layout-simulation.md`](../../research/2026-10-16-layout-simulation.md)

The schemas here are drafts from the trial, not datum's agreed schemas.

## Questions

1. Do draft schemas for the 9 v0 types hold real rows, and what does a validator catch?
   Can a requirement be understood without its rationale?
2. Which model file layout serves an AI agent best: one file per artifact (A) or one
   file per block per type (B)?

## Method

| Path | What it is |
|---|---|
| `schemas/` | Draft JSON Schema (in YAML) for the 9 types |
| `convert.py` | Converts 21 Pendentive rows (commit `1211f9d`) into `model/` with new IDs |
| `validate.py` | Draft validator: schema checks, then rules across rows |
| `rationale-test/` | Blind test: `input.md` (20 statements with their links, no rationale) and `key.json` (the original rationales) |
| `layout-sim/gen.py` | Generates synthetic models in layouts A and B |
| `layout-sim/sim.py` | Emulates the agent's tool calls on both layouts; writes `results.json` (summary in `table.md`) |
| `layout-sim/merge.py` | Parallel branches merged with real git; writes `merge_results.json` |
| `layout-sim/trials.py` | Real `claude -p` runs on the fat model; appends to `trials.jsonl` |
| `layout-sim/uniq_parse.py` | Parse time and how often field lines repeat in B |

Needs Python 3 with PyYAML and jsonschema. From this folder:

```sh
python3 convert.py .           # rewrites model/ (and an ignored id_map.json)
python3 validate.py .
cd layout-sim
for m in small medium large wide deep fat; do python3 gen.py models $m; done
python3 sim.py                 # also merge.py, uniq_parse.py
python3 trials.py haiku 3      # calls the Claude CLI and costs money
```

`models/`, `trials/` and `mergework/` are generated and not kept.

## Result

- The validator on `model/` gives 1 error (a product function serves no scenario) and
  3 warnings (two `TBD` measures, a risk accepted with no consequence). This matches
  conversion findings 2, 3 and 4.
- Blind test: 11 of 20 matched; 6 more are carried by datum's structure; 3 are not.
- Layout: A, confidence about 70%. Same accuracy (40/40 runs each), A cheaper for the
  commonest operations and fewer merge conflicts.
