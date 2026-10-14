# Landscape: spec-driven and structured AI development (2026-10-14)

Condensed from a Sonnet research agent's report. V = seen in a primary source,
INF = inferred. Star counts and release dates are from the GitHub API on 2026-10-14.

## Frameworks

| Tool | Stars | Last release | Spec store | Trace req→code→test | Portability | Weight |
|---|---|---|---|---|---|---|
| GitHub Spec Kit | 141k | v1.2.0, 2026-10-13 | Markdown per feature | no (an analysis step only, INF) | many agents | heavy |
| Amazon Kiro | 4.4k | pushed 2026-09-15 | requirements / design / tasks .md | weak (INF) | IDE only | heavy |
| BMAD Method | 54k | v6.12.2, 2026-10-11 (v7 alpha) | briefs, specs, architecture .md | no (INF) | skills plus plugins | medium to heavy |
| obra/superpowers | 299k | v7.0.0, 2026-10-10 | transient plan and spec docs | no | 15+ harnesses | medium |
| Agent OS | 5.5k | v3.0.0, 2026-01 | standards .md | no | multi-tool | light |
| Taskmaster AI | 28k | 0.43.1, 2026-03 (stalling) | tasks.json | no | MCP | light |
| Tessl | n/a | n/a | registry packages | no | MCP | vision ahead of product |
| OpenSpec | 72k | v1.14.1, 2026-10-06 | specs/ plus change deltas | no (INF) | 30+ tools | light to medium |
| AGENTS.md | n/a | n/a | one file | n/a | very broad (Linux Foundation) | minimal |
| Agent Skills standard | 181k (anthropics/skills) | n/a | SKILL.md dirs | n/a | open standard | minimal |

### Notes on individual tools

- **Spec Kit** (V)
  - Stages: constitution → specify → plan → tasks → implement → converge.
  - Bug-fix and idea-assessment tracks ship as extensions. Installed as skills for many agents.
  - OpenSpec criticises it as "heavyweight, rigid phase gates, lots of Markdown".
- **Kiro** (V)
  - Specs are three files: requirements, design, tasks. Tasks run in dependency waves.
  - A secondary source reports a small bug fix turned into 16 acceptance criteria.
- **BMAD** (V)
  - Moved from role-play personas to skills. `bmad-build` sizes the process to the change.
  - Licence is NOASSERTION.
- **superpowers** (V)
  - Flow: brainstorm → design sign-off → plan → subagent-driven TDD.
  - Skills trigger automatically. It is in the official Claude Code marketplace.
  - It has no persistent spec store.
- **Agent OS** (V)
  - Discovers the standards already in a codebase and injects the relevant ones.
- **OpenSpec** (V)
  - `openspec/specs/` holds the current truth.
  - Each change lives in `openspec/changes/<name>/` with a proposal, delta specs (ADDED/MODIFIED, SHALL plus scenarios), a design and tasks.
  - Archiving merges the deltas into specs. This is the best answer to spec drift found.
- **Agent Skills standard** (V, agentskills.io)
  - A skill is `SKILL.md` with `name` and `description`, plus optional scripts, references and assets. Disclosure is progressive.
  - **The standard has no concept of a workflow.**

## SE plus LLM agents

Almost empty.
- `jgsystemsconsulting/jgs-se-knowledge-packs` (8 stars) and `duonghvu/automotive-syseng` (6 stars).
- Academic work:
  - TraceDev (arXiv 2607.18886): an agent keeps a traceability graph.
  - arXiv 2508.16181: LLM-MBSE tooling lacks traceability, validation and version control.

## Gaps a systems-engineering library could fill

1. Stable requirement IDs with a checked trace from requirement to design to code to test.
2. Decisions and rationale as first-class records.
3. Interface and ICD management.
4. Verification planning: a method per requirement and a coverage report.
5. A risk register and a light FMEA.
6. Requirement quality gates (INCOSE rules).
7. Skill composition: workflows as declared graphs with gates.
8. Right-sizing the process to risk (tailoring).

## Ideas worth borrowing

- OpenSpec: delta specs and archive-merge.
- Spec Kit: the constitution and independent entry points.
- Kiro: EARS-style requirements and dependency waves of tasks.
- Agent OS: discovering the standards already in a codebase.
- superpowers: auto-triggering, subagent review loops and TDD.
- BMAD: right-sizing.
- Distribution as an Agent Skills directory plus a Claude Code marketplace entry.

## Pitfalls seen across them

- Ceremony on small tasks.
- Spec-first waterfall: Beck and Fowler criticised it, and Thoughtworks put spec-driven development in "Assess".
- Markdown bloat and review fatigue: Fowler says "I'd rather review code than the markdown".
- Spec drift when nothing ties specs to tests or CI.
- Vision ahead of product (Tessl).
- Heavy installs and licence ambiguity.
- Always-loaded context bloat.
