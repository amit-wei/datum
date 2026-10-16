# Model file layout: one file per artifact vs one file per block per type (2026-10-16)

Condensed from a research agent's report. VERIFIED means measured in the simulation or
seen in a primary source. INFERRED means reasoning.

## Question

Which layout serves an AI agent best (accuracy and speed of analysis), under the
constraint of token cost and a small context? Human reading does not count; views are
generated.

- **A:** one file per artifact (Markdown with a YAML header), e.g.
  `agent-definition/REQ-AD-001.md`.
- **B:** one YAML file per block per type, a list of entries, e.g.
  `agent-definition/requirements.yaml`.

## Verdict

**A, confidence about 70%.** No difference in accuracy; A is cheaper for the commonest
operations, merges cleanly where B conflicts, and never meets the Read tool's limits.
B's one advantage (a block in about 3 reads) is matched by one `cat` in A.

## Setup (VERIFIED)

- Synthetic models in both layouts: small (101 artifacts), medium (1,515, shaped like the
  Pendentive model), large (10,000), wide (61 blocks, 2 levels), deep (63 blocks,
  6 levels), fat (one block with 217 requirements). Text lengths taken from real rows.
- Claude Code's tools emulated on the real files (Read cap 25k tokens and 256 KB per
  whole file, Glob cap 100 files). Tokens estimated as chars/4.
- Real git merges, and 40 real `claude -p` runs (Haiku ×3, Sonnet ×2) on the fat model.

## Findings

| | A | B | Label |
|---|---|---|---|
| Accuracy, 40 runs of edit, add, move, reverse-link query | 40/40 | 40/40; no YAML indentation errors, no wrong entry | VERIFIED |
| Add and move, cost | baseline | 1.3–2.5× tokens and time (Haiku move: 226k vs 92k input tokens, 34 s vs 13 s) | VERIFIED |
| Move, output written by the model | 29 tokens (`git mv` + one edit) | ~400 tokens (entry cut and pasted) | VERIFIED |
| Reverse links by grep | 1 call, ~0.7k tokens; the file name is the ID | 12–19k tokens; equal once a trace script exists | VERIFIED |
| Read a whole block | 1 `cat`, ~30% fewer tokens than B | ~3 Read calls | VERIFIED |
| Edit needs a unique match | every field line unique in its file | 82–90% of field lines repeat; anchor on the `- id:` line. A non-unique match fails loudly, it does not edit the wrong entry | VERIFIED |
| Largest file | under 4 KB | 625 KB (medium `decisions.yaml`), over the Read limit | VERIFIED |
| Parse of the whole model, large | 0.96 s | 0.78 s | VERIFIED |

The 625 KB file comes partly from the generator, which put all decisions at product
level (INFERRED); per-block decisions would be smaller.

## Parallel branches, same block (real git, VERIFIED)

| Scenario | A conflicts | B conflicts |
|---|---|---|
| edits of different requirements | 0/20 | 0/20 |
| same field of the same requirement (a real conflict) | 10/10 | 10/10 |
| both add requirements, different IDs | 0/1 | 1/1 (both append at the end) |
| move a requirement vs edit it | 0/10 (rename detection) | 10/10 |

No merge was clean but invalid in either layout. A union merge driver would remove B's
append conflicts but could hide real ones (INFERRED).

## Research

- Model accuracy falls as input grows, and one distractor already hurts (Chroma, context
  rot, VERIFIED). Accuracy drops for text in the middle of a long context (Liu et al.,
  VERIFIED). Loading only the needed artifacts favours A (INFERRED).
- Anthropic's context-engineering guide recommends lightweight identifiers such as file
  paths, loaded just in time (VERIFIED).
- The main failure of exact-match editing is old text that does not match; repeated text
  makes it worse (aider, VERIFIED).
- Doorstop, built for tools, stores one YAML file per item. StrictDoc and OpenFastTrace,
  built for human-read documents, hold many items per file (VERIFIED).

## Threats to validity

Hand-written agent plans in the simulation; chars/4 token estimate; synthetic prose; all
LLM runs on one model shape with one phrasing; 40 runs cannot detect failure rates below
about 10%; tool limits change between versions.

## Sources

- https://www.trychroma.com/research/context-rot
- https://arxiv.org/abs/2307.03172
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://code.claude.com/docs/en/tools-reference
- https://aider.chat/docs/more/edit-formats.html
- https://doorstop.readthedocs.io/en/latest/
- https://strictdoc.readthedocs.io/en/latest/strictdoc_02_faq.html
