---
name: writing-scenarios
description: Use when the needs of a product are drawn out and the end-to-end journeys a user or outside system goes through are not yet written, or when a need is not in any journey. Produces scenarios that the functions will serve. Not for checking a design against a journey (use walking-scenarios) or for the functions themselves (use writing-functions).
real: true
---

A scenario is one end-to-end journey from a trigger to an outcome the builder cares
about, told as numbered steps by an actor (a user, an outside system), with its
preconditions and the needs (`ELI-`) it covers. Steps say what happens, never how the
system does it inside. Write the main journeys first, then the variations and the
failures that matter. Output: `SCN-` files in the block's `analysis/` folder.
