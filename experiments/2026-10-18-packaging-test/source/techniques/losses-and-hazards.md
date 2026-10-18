---
name: losses-and-hazards
description: Use when a block's functions could harm someone or something whatever the design: a person acting on wrong output, data lost or exposed, money spent, trust broken. Lists losses and the hazards that lead to them (STPA step 1), before any design exists. Not for risks of a chosen design or technology (use architectural-risk-pass).
real: true
---

List the losses first: what the builder and the users must not lose (safety, data,
money, privacy, trust). Then the hazards: system states that lead to a loss in the
worst case, stated at the level of functions, not parts. Each hazard names the losses
it leads to and the functions it threatens. Requirements answer hazards in the
requirements step. Output: `RSK-` files in the block's `risks/` folder with
`threatens:`.
