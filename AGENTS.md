# Working on this repository

Rules for agents (and people) changing this repository. Keep this file short.

## Layout

| Path | Holds |
|---|---|
| `skills/in-progress/` | Skills under development: public, not shipped in the plugin |
| `skills/<bucket>/` | Released skills (buckets decided when the first skill is released) |
| `agents/` | Subagents, such as reviewers |
| `docs/design-notes.md` | Design positions, each with its state |
| `docs/glossary.md` | The terms datum uses, one meaning each |
| `docs/decisions/` | Decisions about the library, one file each |
| `docs/out-of-scope/` | Rejected concepts, one file each, with the reason |
| `research/` | Dated research summaries |
| `experiments/` | Dated experiment rigs and their raw outputs, one folder each (`YYYY-MM-DD-<name>/`) with a README: question, method, result |

## Rules

1. **Commits follow Conventional Commits** (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`).
2. **A decision about the library becomes a file in `docs/decisions/`.** A replaced
   decision is marked superseded and names its successor. It is never deleted.
3. **A rejected idea becomes a file in `docs/out-of-scope/`** that says what was rejected
   and why. Check there before proposing something.
4. **Research is dated and keeps its labels.** Each claim is VERIFIED (a primary source
   was seen) or INFERRED.
5. **When a skill is added, renamed, removed or changes how it fits a workflow, update
   the router skill** so its map stays true.

## Hard boundary

No personal information in the repository: not in docs, examples, fixtures or commit
messages. The repository is public.
