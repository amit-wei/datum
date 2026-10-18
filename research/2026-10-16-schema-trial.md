# Schema trial on real Pendentive rows (2026-10-16)

Draft schemas for the 9 v0 types were written as JSON Schema in YAML, 21 rows of the
Pendentive model (commit `1211f9d`) were converted into them, and a draft validator was
run. Then a blind test asked whether requirements can be understood without a rationale.
The draft schemas, the validator and the converted rows are kept as the trial's rig in
`experiments/2026-10-16-schema-trial/`; they are not the agreed schemas.
VERIFIED means seen in this trial. INFERRED means our reading.

## Conversion findings

| # | Finding | Label |
|---|---|---|
| 1 | A risk field named `on:` parsed as the boolean `true` (YAML 1.1 reads on, off, yes, no as booleans). Renamed `threatens:` | VERIFIED |
| 2 | Every Pendentive product function cites no scenario | VERIFIED |
| 3 | DEC-199 accepts the exfiltration risk without stating the consequence the user accepts; the `consequence` field makes this visible (audit finding 2) | VERIFIED |
| 4 | "The system shall give a position within TBD" has no statistic. A structured measure forces the question (p95 or max) and marks it `TBD` | VERIFIED |
| 5 | Rationales shrink when links carry the citations: REQ-AD-001 went from four sentences to one | VERIFIED |
| 6 | Every converted requirement fits an EARS pattern ("shall refuse X when Y" is the unwanted pattern). REQ-PL-016 holds three "shall" statements in one row | VERIFIED |
| 7 | Pendentive holds one interface row per item flowing (181 rows), each naming a supplying and an accepting requirement. One interface per pair with a list of items, and `of: IFC` on the two requirements, holds the same facts | VERIFIED |
| 8 | DEC-059's reason held a trade study in prose (three rejected alternatives); it converts cleanly to structured options | VERIFIED |
| 9 | A constraint converts to `source: builder`, which removes the convention that put a name in the origin field | VERIFIED |

## Blind rationale test

20 Pendentive requirements (8 functional, 4 interface, 4 safety, 2 performance, 2
quality), stratified random sample. A fresh agent with no context got each statement and
the artifacts it links to, without the rationale, and explained why each exists. Its
answers were graded against the original rationales by the session agent.

| Result | Rows | What was missing |
|---|---|---|
| Match | 11 | nothing |
| Partial or miss, carried by datum's structure | 6 | a decision cited only in prose (would be `justified_by`); how a value is measured or the evidence for it (`measure.definition`, the proof criterion, a research output); a level-scoping note (a `TBD` and an issue) |
| Partial, not carried by structure | 3 | why this block holds the requirement ("only Ingestion sees the definition before and after"); why this response and not the obvious alternative ("refuse, not ignore, because a caller that got no report believes its write was held") |

The one miss was a decision cited only in prose (VERIFIED). Two real edge
classes remain: *why here* and *why this form* (INFERRED).

Threats to validity: 20 rows from one project; graded by the agent that designed the
rule; the subject saw only Pendentive's links, not datum's richer ones.
