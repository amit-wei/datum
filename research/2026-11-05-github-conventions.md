# A GitHub convention for this repository (2026-11-05)

Research for issue #22. A proposal to decide on: nothing here is agreed
yet.

Each claim is VERIFIED (a primary source was seen) or INFERRED. The audit was done
read-only with `gh`, `git` and repo searches on 2026-11-05. Documentation pages were read
through a summarising fetch, so exact wording should be checked before it is quoted. This
note builds on `research/2026-10-github.md` and does not repeat it.

## Recommendation

Change four things and leave most of GitHub unused.

1. **Move the session handoff off #6 into one short file, `docs/handoff.md`,** rewritten
   each session and committed with the work. It holds only the current state and what is
   next. Anything decided goes in `docs/design-notes.md`.
2. **One issue is one outcome that can be closed.** #6 becomes a parent with one sub-issue
   per remaining piece, as #24 already requires for build skills.
3. **Write a definition of "closed"** (below). Closing has mostly worked. What fails is
   work left inside closed issues, and issues closed before their commit reached GitHub.
4. **Write the session routine in `AGENTS.md`.** Today it is nowhere in the repository.

A fresh agent then needs three reads:

| Question | Read |
|---|---|
| What is next? | `docs/handoff.md` |
| Why? | `gh issue list`, then `gh issue view <n>` |
| What was decided? | `docs/design-notes.md` |

No new tool, automation, board or label is needed.

## What the repo does today

VERIFIED unless marked.

**Counts.** 24 issues: 13 open, 11 closed. 0 pull requests, 0 releases, 0 tags. One
milestone, v0.1.0 (6 open, 8 closed). 11 labels, of which only `parked` is used (4
issues). One sub-issue link (#21 under #5). One dependency (#6 blocked by #1, already
closed). One issue ever assigned (#13). No pinned issue, no `.github/` folder. The repo
page shows 0 linked projects. A project owned by the account could not be checked (see
the end of this note).

**What works**

- Closed issues nearly always say where the outcome went. Three closed through
  `Closes #N` in a commit (#9, #20, #21). Eight closed by hand, each with a comment
  pointing at the result.
- No issue has ever been reopened.
- `parked` is clear, and it keeps ideas for later out of the way.
- The handoffs are good. Their "Next, in order" lists are what a fresh agent needs.
- `docs/product.md`, `docs/design-notes.md` and `research/` hold the reasons well.

**What does not work**

| # | Finding | Effect |
|---|---|---|
| A1 | `AGENTS.md`, `CLAUDE.md`, `README.md` and `docs/` never mention handoffs or a session routine. The routine lives only in a private agent memory | An agent without that memory, such as a cloud session, does not know where to start |
| A2 | #6 cannot close: "the handoffs" and "the skills" share one issue, with 10 comments and 0 sub-issues | Its progress cannot be read, and it holds the plan for most remaining work |
| A3 | Only 5 of the 10 comments on #6 are handoffs. One non-handoff comment came shortly before the session 7 handoff | INFERRED: "read the latest comment" can land on the wrong one |
| A4 | Handoffs hold agreed content found nowhere else. The experiment README points to them for the test design. "Each step brings its own schemas" was not found in `docs/design-notes.md` or `AGENTS.md` | The repo's own rule says files are the record and losing GitHub loses only discussion (Q-6). That is not true today |
| A5 | Items left the handoffs' Open list without an issue: work packages, per-type states, evals and judges, reviewer preload. All four are in session 5's list and gone by session 8's. The first three have a line in the design notes. Preload has none | Work disappears from view |
| A6 | Work left inside closed issues: #16's open question on ASD-STE100 appears in no repo file. #1 closed with per-type states still open | Same as A5, and nothing shows it |
| A7 | #18 was closed on 2026-10-21 citing commit 1b4a653. GitHub still does not have that commit: GitHub's `main` is at 873c975, local `main` is one ahead, and the `fa-test-fixtures` branch is local only | The tracker says done for something that exists on one machine. A cloud session would get older code than the handoff describes |
| A8 | Remaining work has no issues of its own: the FA test, gate checks, requirements, synthesis, design evaluation, increment | INFERRED: the milestone reads 8 of 14 closed, which makes v0.1.0 look closer than it is |
| A9 | #5, #22 and #23 have neither a milestone nor `parked` | Nobody can tell "later" from "not looked at" |
| A10 | 7 of 41 commits on `main` mention an issue | `AGENTS.md` rule 6 (a change traces to an issue) cannot be checked from the history |
| A11 | `AGENTS.md` rule 2 sends decisions to `docs/decisions/`, which does not exist. Decisions are in `docs/design-notes.md`, which uses "agreed", "settled" or "decided" on 51 lines | The rule misleads an agent about where to look or write |
| A12 | v0.1.0 is due 2026-11-08, and its description calls all dates tentative | A date nobody trusts, and it sits badly with the repo's no-estimates rule |

**Corrections to the earlier research**

- `research/2026-10-github.md` says commits plus `gh release create --generate-notes`
  give a changelog. VERIFIED otherwise: generated notes list merged pull requests,
  contributors and a changelog link. INFERRED: with no pull requests they would be nearly
  empty here.
- Issue types: `issueTypes` returns null on this repo. VERIFIED, on the repo itself, that
  they are not available.
- #8 left issue forms, creating a release and Discussions for #22 to verify "if it relies
  on them". This proposal uses neither forms nor Discussions. Creating a release stays
  INFERRED until the first one, since this research was read-only.

## What others do, and what GitHub supports

**Comparable practice.** The evidence is thin. Searches found no solo, AI-assisted project
reporting on milestones or sub-issues, and no established use of issue comments as a
handoff store (INFERRED from that absence).

- **Anthropic, long-running agents (VERIFIED).** State passes through a progress file, a
  feature list and git history. Each session starts by reading the git log and progress
  notes, then picks the top unfinished item. It ends with a commit and a progress update.
  This is the closest match to this repo's sessions.
- **Simon Willison, "The Perfect Commit" (VERIFIED).** A solo maintainer. Every commit
  links to an issue, and he opens an issue just to have one to link to. Decisions are
  written in the thread. He names the weak spot: issues are not part of git's history.
- **`handoff.md` (VERIFIED, blog post by a tool vendor).** Pass the working state, not the
  conversation. It says the file stops working when notes spread over several places and
  it becomes unclear which is current. That is an argument for one place, which is the
  aim here.
- **Beads (VERIFIED from its repo page).** An issue tracker built for agents, on its own
  database. No failure above needs it, and it would be a second tracker.

**GitHub facts relied on (VERIFIED from docs unless marked).**

- A closing keyword (`Closes #N`) works in a commit message. The issue closes when that
  commit reaches the default branch. Other branches do nothing until merged.
- Close reasons are completed, not planned and duplicate (`gh issue close --help`).
- Sub-issues: 100 per parent, 8 levels. The docs do not say that closing a parent depends
  on its children, so INFERRED: the rule is ours to keep.
- `gh` has `--parent` and `--blocked-by` since v2.94.0. The installed version is 2.102.0.
- Blocked issues show a "Blocked" icon on the issues page.
- Projects add saved views, custom fields and boards. They belong to the user account,
  not the repo. The current token cannot read them: it lacks the `read:project` permission
  (VERIFIED by the error it returned).
- Search `no:milestone -label:parked` works, and returns #5, #22 and #23 today (VERIFIED
  by running it).

## The proposed convention

This is for this repository only. It does not decide what datum tells its users, and it
is not a model of the library (`docs/out-of-scope/modelling-the-library.md`). The fixed
milestone scope in the Increments section is for modelled products, so v0.1.0's plain
description is fine here (INFERRED).

| Feature | Use here | Failure it prevents |
|---|---|---|
| Issue | One outcome that can be closed. The title says the outcome | A2, A8 |
| Sub-issue | Splits an outcome too big for one issue. The parent closes when its children have | A2 |
| Blocked by | Only when one issue truly cannot start before another. Order within a session stays in the handoff | A dependency lost when the handoff is rewritten (INFERRED) |
| Milestone | One per planned release. Every open issue has a milestone or `parked`. No due dates | A9, A12 |
| Label | `parked` only. Other default labels stay, unused | A9 |
| Commit message | `Refs #N` in the body, or `Closes #N` on the commit that finishes the issue | A7, A10 |
| Handoff file | `docs/handoff.md`: branch, last commit, pushed or not, in flight, next in order by issue number, what waits on a decision | A1, A2, A3 |
| Release | A tag plus written notes, created when a milestone closes. Nothing before that | A version with no fixed point (INFERRED) |

**Leave unused**

| Feature | Why |
|---|---|
| Projects | A board repeats what the issue list shows for about a dozen open issues, and agents cannot read it with the current token |
| Assignees | One human, and agents act under the same account, so an assignee says nothing |
| Issue types | Not available on a personal account |
| Extra labels (type, priority) | No failure needs them. Priority is the order in the handoff |
| Issue forms and templates | One person writes the issues |
| Pinned issues, Discussions, wiki | Each would be another place to look |
| Automation | Nothing above needs it. `Closes #N` is already built in |

The earlier research suggested `type:*` labels, issue forms, a pull request template and
task issues generated from files. Those fit a project with a model and with intake from
other people. This repo has neither yet, so they do not earn a place (INFERRED).

### Where handoffs live

A handoff mixes three things. Only one needs a home of its own.

| Content | Home |
|---|---|
| What was done | `git log` |
| What was agreed | `docs/design-notes.md` or the experiment README, written in the same session |
| Where things stand and what is next | `docs/handoff.md` |

A file beats a comment for four reasons. It travels with the code it describes, so the two
cannot disagree (A7). It is one read, with no hunting for the right comment (A3). It works
offline and with grep. Its history is `git log -p docs/handoff.md`. The Anthropic pattern
above is the same shape.

The cost: a file on a branch is invisible from another branch, and an unpushed file is
invisible to a cloud session. INFERRED that this is acceptable, because such a session
would not have the code either. The old comments stay on #6 as a record.

This also fits #19, which hopes a session needs to store "nothing or very little" beyond
its artifacts. A short handoff would be a first test of that.

### Definition of closed

An issue is closed only when all of these hold:

1. **It is on GitHub.** The outcome has reached `main` on GitHub, not only a local
   machine. A decision counts when the file holding it has.
2. **It says where.** The closing commit or comment names the file or commit that holds
   the outcome.
3. **Nothing is left in it.** Every leftover has its own issue, named in the closing note.
4. **It was agreed.** The push is the agreement, or it is said in the session. Agents do not
   close on their own view that the work is done.

The usual way is `Closes #N` in the last commit, so the issue closes by itself when the
push reaches `main`. That gives 1 and 4 for free. An issue with no commit uses
`gh issue close <n> --comment "..."`. A dropped issue closes as `not planned`, and a
rejected idea also gets a file in `docs/out-of-scope/` (rule 3).

To stay closed: a later finding gets a new issue that refers to the old one. Reopen only
if the issue was closed by mistake.

### Draft text for `AGENTS.md`

```markdown
## Sessions

**Start:** read `docs/handoff.md`, run `gh issue list`, read the issues it names.
**End:** put anything agreed in `docs/design-notes.md`, give anything left open an
issue, then rewrite `docs/handoff.md` and commit it last. Keep it to one screen.

## Issues

- One issue is one outcome that can be closed. Too big: split it into sub-issues.
- Every open issue has a milestone or the label `parked`.
- Every commit names its issue: `Refs #N`, or `Closes #N` on the last one.
- An issue closes when its outcome is on GitHub's `main`, the closing note says where,
  leftovers have their own issues, and it was agreed.
- A later finding gets a new issue. Reopen only a mistaken close.
```

## Improvements, in order

| # | Step | Size |
|---|---|---|
| 1 | Push `main`, so #18's commit is on GitHub (A7) | 1 push |
| 2 | Add the sections above to `AGENTS.md` | 1 file edit |
| 3 | Write `docs/handoff.md` from the session 8 handoff and today's state, then add a pointer comment on #6 | 1 new file, 1 comment |
| 4 | Sort #5, #22 and #23 into a milestone or `parked` | 3 issue edits |
| 5 | Make #6 a real parent: sub-issues for the FA test, gate checks, requirements, synthesis, design evaluation, increment | 6 new issues, 1 body edit |
| 6 | Open issues for the leftovers: work packages, per-type states, evals and judges, reviewer preload, ASD-STE100, DEC to ADR in schemas. Each gets v0.1.0 or `parked` | 6 new issues |
| 7 | Settle `AGENTS.md` rule 2 (choice 2 below) | 1 file edit |
| 8 | Remove the v0.1.0 due date | 1 milestone edit |
| 9 | After the FA test finishes, move its agreed design from the #6 comments to its README, and copy the "each step brings its own schemas" convention to the design notes | 2 file edits |
| 10 | Mark Q-6 settled in the design notes, and close #22 | 1 file edit, 1 close |

At the first release, as part of normal work: close the milestone, create the tag and
release with written notes. Check then that creating a release works as the docs say.

## Open choices

1. **Where handoffs live.** Recommended: `docs/handoff.md`. The alternative is a dedicated
   issue that never closes. It is visible from any branch, even before a push, but it
   leaves handoffs outside git and can again run ahead of the code. Confidence: medium to
   high.
2. **Rule 2 and `docs/decisions/`.** Recommended: change the rule to match practice, so
   `docs/design-notes.md` is the decision record, and bring the folder back when the design
   notes stop being enough. The alternative keeps the rule and starts the folder with this
   convention as its first file, with no back-fill, which leaves decisions in two places.
   Confidence: medium.
3. **Pull requests.** Recommended: none for now. The push already acts as the
   gate. Reconsider at the first outside contributor or when CI runs. The cost is that
   release notes are written by hand. A pull request would give a page for reviewing agent
   work before it reaches `main`, which may matter more once code is being built.
   Confidence: medium.
4. **#6: keep or replace.** Recommended: keep it as the parent, since its body still fits.
   The alternative closes it and opens a clean parent. Confidence: high.
5. **Which leftovers belong in v0.1.0** (step 6). This needs a judgement call, and
   no recommendation is offered for each. Lean: reviewer preload in v0.1.0 because the
   reviewer depends on it, the others `parked`. Confidence: low.
6. **The due date.** Recommended: remove it. If it helps as a personal target, keep it and
   ignore this. Confidence: high.

## What could not be verified

- Projects owned by the account: the token lacks `read:project`. The repo page shows 0.
- Creating a release: not tried, since this research was read-only.
- Whether closed sub-issues count against the limit of 100: one community report says yes,
  the docs are silent. It does not affect a parent of this size.
- How comparable projects use milestones and sub-issues: no good source was found.

## Sources

- GitHub Docs, docs.github.com/en: `issues/tracking-your-work-with-issues/using-issues/`
  `linking-a-pull-request-to-an-issue`, `adding-sub-issues`, `creating-issue-dependencies`;
  `issues/using-labels-and-milestones-to-track-work/about-milestones`;
  `issues/planning-and-tracking-with-projects/learning-about-projects/about-projects`;
  `repositories/releasing-projects-on-github/about-releases` and
  `automatically-generated-release-notes`; `rest/issues/issues`
- GitHub changelog, 2026-06-10: github.blog/changelog/2026-06-10-manage-sub-issues-types-and-dependencies-from-github-cli/
- Anthropic: anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Simon Willison: simonwillison.net/2022/Oct/29/the-perfect-commit/
- dev.to/a2cr_mcp/when-handoffmd-stops-being-enough-for-ai-agents-5h64
- Beads: github.com/gastownhall/beads
- Community report on the sub-issue limit: github.com/orgs/community/discussions/207865
- This repository: `gh` issue, label, milestone, release and pull request queries; `git log`;
  `AGENTS.md`; `docs/design-notes.md`; `research/2026-10-github.md`
