## The model on disk

- Everything is under `model/`. The product is the block `model/product/`; each part is
  a block in its own folder below its parent, named in the parent's `parts.yaml`.
- A block holds `functions/`, `requirements/`, `proofs/`, `interfaces/`, `decisions/`,
  `risks/` and `analysis/` (elicitation records `ELI-`, scenarios `SCN-`, spike results
  `SPK-`, research `RES-`), one YAML file per artifact, named by its ID.
- An ID is a type prefix and 4 Crockford base32 characters (`REQ-7K3Q`). Links name IDs,
  never paths.
- `model/<block>/steps.yaml` records which engine steps the builder has closed, e.g.
  `functional-analysis: {closed_at: <commit>}`. A closed step whose files changed after
  that commit is stale.
- States a person decides: `draft`, `agreed`, `retired`. Everything else is computed.
