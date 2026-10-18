---
name: writing-functions
description: Use when the things a block must do are not yet written: at product level from its scenarios, below from the functions the parent gave a part. Produces functions and the flows between them (functional decomposition). Not for what must hold for a function (use writing-requirements) or for splitting a block into parts (use synthesis).
real: true
---

A function is a verb phrase for something the block does, independent of how: "log a
session", not "save a row to SQLite". Each serves a scenario (product level, `serves:`)
or decomposes a parent function (`parent: FUN`). Name the flows between functions:
what each receives and produces. Stop at functions this block itself performs. Output:
`FUN-` files in the block's `functions/` folder.
