# Storage and traceability of engineering artifacts (2026-10-14)

Condensed from a Sonnet research agent's report. VERIFIED means a primary source was
fetched. INFERRED means it comes from the agent's background knowledge.

## Requirements-as-code tools

| Tool | Status | Format | IDs | Code and test trace | Fit |
|---|---|---|---|---|---|
| StrictDoc | 0.30.2, 2026-10-09; heavy Python deps (V) | `.sdoc` textX DSL; `RELATIONS` must be the last field (V) | free-form UID; auto-uid from a mask; opaque MIDs (V) | `@relation(REQ-1, scope=...)` in source comments (V) | richest tool; LLMs find the DSL less natural |
| Doorstop | 3.2, 2026-07-10; light deps (V) | one YAML file per item; directory = document (V) | prefix + digits tied to the document, so tree-coupled (INF) | `references` field (INF) | LLM-friendly; weak ID scheme |
| sphinx-needs | 9.0.0, 2026-10-14 (V) | RST/MyST directives in Sphinx | free-form (INF) | needs.json, needtable (INF) | too heavy for solo |
| OpenFastTrace | 4.10.0, 2026-09-20; JRE (V) | any text file; Markdown specs | `type~name~revision` (V) | `[impl~x~1 -> req~y~1]`; `>> utest` declares required coverage (V) | LLM-friendly; language-agnostic |

Newer tools (req-cli, Tracey, Reqord, SpecTrace) are immature and unvetted.

## ADRs

- **MADR 4.0.0** (V)
  - Files are `NNNN-title.md` in `docs/decisions/`, with frontmatter: status, date, decision-makers.
  - Sections: context, drivers, options, outcome, pros and cons.
  - Supersession is only a status string.
- **log4brains:** ADRs are immutable; it looks stale.
- **Sequential numbers collide** on parallel branches. Use slug or random IDs.

## Architecture as code

- Structurizr DSL and LikeC4 (v1.59.4, 2026-09-21, V) are text models in the repo.
- arc42 is a 12-section template.

## Contracts

- OpenAPI, AsyncAPI and JSON Schema as the contract formats.
- Schemathesis (4.31.0, V) for property-based API tests.
- Pact matters mostly when there are several services.

## Plain traceability (INFERRED)

- Mark tests with a registered `@pytest.mark.req("REQ-x")`, or use tags in test names.
- A script of about 100 lines fails CI on an uncovered or unknown requirement ID and writes a Markdown matrix to `$GITHUB_STEP_SUMMARY`.

## GitHub

- Sub-issues: 100 per parent, 8 levels deep (V). Issue types are an organisation feature (V).
- Durable artifacts belong in git. Issues hold the work queue, linked by ID.
- A required CI check is the useful gate for a solo developer. CODEOWNERS adds little.

## IDs

- Opaque, tool-minted IDs (for example `REQ-7K3Q`), never reused, independent of location.
- Parent and allocation are held in fields.
- An ID is retired through `status` and `replaced_by`.

## Recommendation from the agent

1. **Plain files plus our own validator.** One Markdown file per artifact with YAML frontmatter: `id`, `type`, `status`, `parent`, `links`, `replaced_by`. Best fit.
2. **OpenFastTrace over Markdown specs**, if an off-the-shelf tag syntax is wanted.
3. **StrictDoc**, if a UI and ReqIF/PDF export are wanted.
