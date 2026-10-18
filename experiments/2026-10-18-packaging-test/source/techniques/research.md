---
name: research
description: Use when an answer depends on facts outside the model and the conversation: what already exists, an established convention or definition, a standard, or anything that changes over time such as prices, limits and versions. Run in a subagent that reads primary sources. Not for what only the builder knows (use grilling) or what must be measured (use running-a-spike).
real: true
---

Run it in a subagent so only the conclusion enters the session. Write the question
first. Read primary sources in full, not summaries; label every claim VERIFIED (a
primary source was seen) or INFERRED. Never answer a question about something that
changes (prices, quotas, versions, current practice) from memory. Output: a research
record (`RES-`) in the block's `analysis/` folder, dated, with its sources, cited by
the artifact that uses it.
