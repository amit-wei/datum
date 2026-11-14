| # | Datum | Baseline | Datum checks |
|---|---|---|---|
| R1 | 3/3 | 3/3 | write check not measurable (files written through Bash) |
| R2 | 0/2 | 0/2 | write check not measurable (files written through Bash) |
| R3 | 0/2 | - | write check not measurable (files written through Bash) |
| R4 | 1/3 | 0/3 | ok |
| R5 | 3/3 | - | ok |
| R6 | 2/2 | - | validator 4 |
| R7 | 3/3 | - | ok |
| R8 | 2/2 | - | no writing-requirements |
| R1r | 3/3 | - | write check not measurable (files written through Bash) |
| R2r | 2/2 | - | write check not measurable (files written through Bash) |
| R3r | 0/2 | - | write check not measurable (files written through Bash) |
| R4r | 2/3 | - | ok |

Cost on sonnet, judge included: $11.21

Blind evaluation (both orders must agree):
- R1-datum-sonnet-5ad94f|R1-baseline-sonnet-6881e8: baseline
- R1-datum-sonnet-cd9cb4|R1-baseline-sonnet-4a4a3e: baseline
- R1-datum-sonnet-41c2d5|R1-baseline-sonnet-6f1ad0: baseline
- R1r-datum-sonnet-70e989|R1-baseline-sonnet-6881e8: baseline
- R1r-datum-sonnet-2d9da4|R1-baseline-sonnet-4a4a3e: baseline
- R1r-datum-sonnet-75cb73|R1-baseline-sonnet-6f1ad0: baseline

Fails:
- R2 R2-datum-sonnet-c4c916: The run does address uneven amounts, but it states a settled rule: REQ-7SHX fixes that leftover cents go to individual people, one cent each, with a share spread of at most 0.01. It does not ask the builder how to split an amount that doesn't divide evenly, and it does not mark the rule TBD. None of the eight questions to the builder covers it.
- R2 R2-datum-sonnet-75ab58: The final message never raises how to split an amount that does not divide evenly. REQ-E9PQ states a rule as settled (shares sum exactly and differ by at most one cent), with no question to the builder and no TBD. The questions about out-of-range and sub-cent amounts are a different issue.
- R2 R2-baseline-sonnet-e4c9b3: The run raises the uneven-split issue, but it settles a rule in C3P9. It sets shares to differ by at most 0.01, and an example gives 10.00 among 3 as 3.34, 3.33, 3.33. It leaves only which person gets the extra cent open, and it never states that the builder must settle the rounding rule. The expected outcome is to leave the whole rule open, or to ask the builder, and this run does neither.
- R2 R2-baseline-sonnet-a4c892: The run raises the spare-cent issue but states a rounding rule as settled in REQ-E5F6 (first picked get the extra cent, 10.00 among 3 gives 3.34/3.33/3.33). It marks the rule only as a proposal in the final message, and the requirement itself states it flatly with worked cases. It does not leave the rule open or ask the builder to settle it.
- R3 R3-datum-sonnet-ba7633: The agent did not ask the builder how to deal with hazards before settling them. It wrote requirements that present one way of dealing with each hazard as decided (prevent by confirmation, prevent by settlement invariant, etc.). Only the delete safeguard (HAZ-DD0C) was flagged for builder choice, which is partial, and the other hazards were not offered as proposals.
- R3 R3-datum-sonnet-aa3163: The agent did not ask how hazards should be handled for most of them. It decided on a response for HAZ-4R75 (reject mismatched amounts and leave the record unchanged), HAZ-8NA1 and HAZ-FJYD (requirements written as decided), and HAZ-WKAA (it assumed the split between accepting loss of the phone and preventing loss on closing the app, and only asked for confirmation afterward). It did leave HAZ-DD0C open with options, but that is one hazard of several.
- R4 R1-datum-sonnet-5ad94f: Most proofs name a method (test) with a reason, but several reasons are generic or weak: PRF-V3MZ ("a test keeps it from drifting"), PRF-K1FF, PRF-GYQ9 and PRF-CZJE are thin. Also, PRF-CDV8 says "A test with that oracle ... is the carrying out of this analysis" and PRF-FM37 says "a calculation by hand covers a few", which are not reasons that fit the requirement. Every requirement uses test, with no inspection, analysis or demonstration where it would fit (e.g. REQ-V08Y, REQ-9W7B, the measures).
- R4 R1-datum-sonnet-cd9cb4: Every proof names its method (test), but several rationales are generic or don't explain why test fits. Examples: PRF-M8HK says "Recording is the core act, and later code can break it unnoticed", and PRF-MZ51 and PRF-GV7B say a script can enter or set up inputs. None says why inspection, analysis or demonstration would be less suitable. Offline use is also checked only by test, with no consideration of demonstration.
- R4 R1-baseline-sonnet-6881e8: Every check names a method, but none gives a reason for that kind. The `how` fields only describe the procedure, and the final message's table just lists methods. The reasons that do appear, such as why a requirement needs inspection or a device demonstration, are either implicit or missing.
- R4 R1-baseline-sonnet-4a4a3e: Each check names a method (test, inspection, demonstration), but none gives a reason why that kind fits the requirement. The `how` fields only describe the procedure, and the final message's 'How it's checked' column does the same. The expected outcome requires a stated reason for the kind, so a check without one fails.
- R4 R1-baseline-sonnet-6f1ad0: Checks name a method (test, inspection, demonstration) but give no reason why that method suits each requirement. The `check` fields only describe procedures, and there is no rationale for choosing the kind. Some requirements also mix methods under a single `method: test` (for example G7SH, I9DL and N4MN list inspection or demonstration in the check text), and the stated method doesn't match that.
- R3r R3r-datum-sonnet-8f7db2: The run does not give a grounded treatment for each hazard. Only some requirements carry a rationale, and most rely on 'answers' links with no explanation. HAZ-DD0C is only partly answered, with no stated reason why deletion is neither prevented nor accepted. HAZ-WKAA, HAZ-FJYD and HAZ-8NA1 have no reason tied to the record or a named source for the chosen approach (prevent, respond or accept). Hazards are mapped to requirements without stating how each is dealt with.
- R3r R3r-datum-sonnet-07ee03: The requirements that answer HAZ-8NA1 (REQ-KGB2) and HAZ-FJYD (REQ-Z8AE) have no rationale, so those treatments are chosen with no reason. HAZ-DD0C is left "open" without a stated treatment or reason. The final message doesn't say how each hazard is dealt with and why.
- R4r R1r-datum-sonnet-2d9da4: All 21 proofs use the `test` method, and most rationales are generic or boilerplate ("A direct result; a test is cheap.", "a test is cheap", "A direct display result; a test is cheap.") with no reason fitted to the specific requirement. Several others only partly fit, e.g. "A mechanical property of the output; a test is cheap and rerunnable." Because those rationales are generic, the run does not meet the expected outcome.
