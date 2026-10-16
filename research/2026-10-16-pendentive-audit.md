# Lessons from the outside audit of Pendentive (2026-10-16)

Source: `outside_audit_findings.md` in the Pendentive repository, commit `1211f9d`
(2026-10-16). An outside agent audited the Pendentive requirements model from first
principles. VERIFIED means the findings file states it. INFERRED means it is our reading
of what it means for datum.

## The model audited (VERIFIED)

- 34 days of work. 102 functions, 678 requirements, 156 risks, 181 interfaces, 44 tests,
  235 decisions, 117 open questions. No code. The validator is clean.
- Verdict: "Change course. Do not stop." The thinking is careful, but the specification
  has outgrown what it serves.
- The audit took the February 2027 date as fixed. The builder states it is arbitrary, so
  the schedule findings weigh less than the audit says.

## Failures of the method, and what they mean for datum

| # | Finding (VERIFIED) | For datum (INFERRED) |
|---|---|---|
| L1 | Eleven systems that share no part and no store became eleven fenced processes on a two-core host. Every act crosses four systems, so the thinnest slice is the full skeleton | Separate the logical view (parts, interfaces) from the deployment view (what runs separately). One unit by default; every extra unit needs a requirement behind it |
| L2 | Decomposition to component level before code, with a component of "approximately one file", "decides the code twice". The rule "no system is complete" leaves no stopping point | Go deep only for the increment, and stop at the stopping rule (a block built as one unit), never at file level |
| L3 | No scenario says what the user does with the platform. Product functions are infrastructure capabilities | Product-level functional analysis must show the use each top function serves |
| L4 | The verification programme (judge panels, held-out sets, adaptive injection suites, bottom-up verification of 614 Test rows) is larger than the build. "A gate that cannot be run is a gate that is skipped under pressure" | A gate must be runnable at the current increment; otherwise it is a reported trend |
| L5 | 42 of 200 design decisions restate an earlier one, each with a seven-step supersession. A system was kept separate partly because folding it in "supersedes about nine decisions": "a cost of the method, not of the design" | Revising a decision must be cheap in the format |
| L6 | The USD 50 budget is verified by Analysis and no analysis exists. The audit's first step is to measure one agent turn in a prototype. "Let code answer the open questions" | The engine needs throwaway experiments (spikes) whose result, not code, enters the model |
| L7 | About 100 safety requirements answer risks scored by likelihood and detection anchors that, with no code and no operation, are guesses | Before anything runs, likelihood scores are weak evidence. Open: rank by severity alone until there is evidence |
| L8 | A 672-line validator and a 136-line auditor brief, maintained by the one builder. A fixed internal vocabulary makes rows opaque; the audit asks for a glossary | Grow tooling only with a named consumer (P9); prefer plain names |
| L9 | The convention `Constraint: <name>` put the user's name into a field of every constraint row of a public repository | No format field may invite a name. A validator check can refuse a list of known strings |
| L10 | Decisions about the provider landscape of autumn 2026 will be revisited by February; a model that costs a supersession cascade per change lags the ground | Same as L5: decisions about a fast-moving field must be cheap to revise |

## What worked (VERIFIED)

- Decisions with reasons and reversal conditions.
- The method caught real defects: the user's hard boundary had almost no flowdown; MCP
  servers attached to the model bypassed every gate; the writer of a record and the
  source of its content are two facts.
- The trust boundaries were right; the process boundaries were not.
