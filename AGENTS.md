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
| `docs/handoff.md` | Where things stand and what is next, rewritten each session |
| `docs/out-of-scope/` | Rejected concepts, one file each, with the reason |
| `research/` | Dated research summaries |
| `experiments/` | Dated experiment rigs and their raw outputs, one folder each (`YYYY-MM-DD-<name>/`) with a README: question, method, result |

## Rules

1. **Commits follow Conventional Commits** (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`).
2. **A decision about the library goes in `docs/design-notes.md`, with its state.** A
   replaced decision is marked superseded and names its successor. It is never deleted.
3. **A rejected idea becomes a file in `docs/out-of-scope/`** that says what was rejected
   and why. Check there before proposing something.
4. **Research is dated and keeps its labels.** Each claim is VERIFIED (a primary source
   was seen) or INFERRED.
5. **When a skill is added, renamed, removed or changes how it fits a workflow, update
   the router skill** so its map stays true.
6. **A change to the library traces to an intake line in `docs/product.md` or to an open
   issue.** Otherwise, open the issue first.

## Issues

- One issue is one outcome that can be closed. Too big: split it into sub-issues. A
  sub-issue splits an outcome and is not a category: what cuts across steps has no parent.
- One issue per thing that ships (a skill, a technique, a schema) and one per test run.
  Behaviours stay in the experiment folder. A finding gets an issue if it outlives the
  session.
- An open issue with a milestone is planned for that release. `parked` means looked at,
  not now. Neither means not sorted yet: `no:milestone -label:parked` lists those. Sub-issues
  carry the milestone too. `parked` is the only label.
- Blocked-by means it cannot start. Issues never carry build order: that is in
  `docs/handoff.md`.
- Every commit names its issue: `Refs #N`, or `Closes #N` on the last one. Only a change
  that alters no meaning is exempt.
- An issue closes when its outcome is on GitHub's `main`, the closing note says where,
  leftovers have their own issues, and it was agreed. `Closes #N` does this on push.
  Agents run `gh issue close` only when told to. A parent closes by hand after its
  children.
- A later finding gets a new issue. Reopen only a mistaken close.

## Sessions

**Start:** read `docs/handoff.md`, run `gh issue list`, read the issues it names.
**End:** put anything agreed in `docs/design-notes.md`, give anything left open an issue,
then rewrite `docs/handoff.md` and commit it last. Keep it to one screen.

## Hard boundary

No personal information in the repository: not in docs, examples, fixtures or commit
messages. The repository is public.
