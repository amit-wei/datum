# Writing skill descriptions and skill text (2026-10-18)

Condensed from a Sonnet research agent's report. VERIFIED means the agent read the
primary source's full relevant text; VERIFIED-secondary means it read the source only
through a summarizing fetch. INFERRED means it is reasoning. A second agent then read
the paper and the Claude Code skills docs as raw text and checked each claim against
quotes; its corrections are folded in. Cost: about 95k tokens, 17 tool calls and 2
minutes for the first run; about 70k tokens and 7 tool calls for the re-read.

The question: how to write the `name`, `description` and body of a skill so that the
right skill is chosen and followed, with close-neighbour techniques in one library.

Sources read in full: Anthropic's skill-authoring best practices
(platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices); the Agent
Skills specification and its page on optimizing descriptions (agentskills.io);
`skill-creator/SKILL.md` and the openings of nine other skills in anthropics/skills;
issues anthropics/claude-code#64606 and #20986; arXiv 2605.24050 v2 (raw text, in
full); the Claude Code skills docs (code.claude.com/docs/en/skills, raw text, the
relevant sections). Read only through a summary: Anthropic's "Equipping agents with
Agent Skills" post, which adds little.

## Name and description

| Finding | Label |
|---|---|
| Name: at most 64 characters, lowercase letters, digits and hyphens, matching the directory | VERIFIED |
| Description: at most 1,024 characters (spec). Claude Code cuts description plus `when_to_use` at 1,536 in the listing; "put the key use case first" | VERIFIED |
| The listing budget is 1% of the context window (about 8,000 characters at 200k). On overflow, descriptions are dropped, least-used first; names stay. #64606: 25 skills at about 490 characters each overflowed it, and Claude then ignored the skills | VERIFIED |
| The user can raise the budget (`skillListingBudgetFraction`) and the per-entry cap (`skillListingMaxDescChars`); `skillOverrides` can list a skill by name only | VERIFIED |
| A description says what the skill does and when to use it, in the third person | VERIFIED |
| Imperative phrasing ("Use this skill when…"), the user's intent rather than the mechanism, and contexts where the domain is not named ("pushy"); Claude tends to under-trigger | VERIFIED |
| Anthropic's own descriptions use "Use this skill whenever…", concrete triggers, and exclusions ("Do NOT use for…"); docx, xlsx and pptx run 600–900 characters | VERIFIED |
| Near-miss negatives are the most valuable test queries; a false trigger is fixed by stating what the skill does not do and where its boundary with neighbours is | VERIFIED |
| Optimize against about 20 queries (8–10 positive, 8–10 near-miss), 3 runs each, a 60/40 train/validation split; pick the iteration with the best validation score | VERIFIED |
| Claude consults a skill only for a task it cannot easily do alone, so a simple request may not trigger a well-matched skill | VERIFIED |
| #20986: Claude skipped a skill whose description matched exactly and did the task itself; closed as a duplicate of #15136 with no fix | VERIFIED |

**Shadowing (arXiv 2605.24050, SkillsBench, Haiku 4.5 and Sonnet 4.6).** VERIFIED
unless marked.

- Libraries of 52, 102 and 202 skills lowered the pass rate by 0.08, 0.14 and 0.21
  (absolute points, against a library of only the helpful skills). Shadowing, the wrong
  skill or none, accounts for "up to 68%" of the drop; the cost of a longer listing is
  "indistinguishable from zero". At 52 and 102 the shadowing share is barely or not
  significant.
- Distractor invocations, pooled: 4%, 7%, 9%. The two models fail differently: Haiku
  abandons skills (no skill used in 66% of runs at 202), Sonnet picks wrong ones (14%
  at 202).
- The named mechanism: a distractor "whose description superficially matches the query
  better than the provided helpful skill" was invoked in all 26 runs of one task. The
  distractors come from other tasks' bundles and "are not adversarially constructed".
  The paper never studies close neighbours; it says only that "once semantically
  similar skills compete for selection, accuracy degrades regardless of the underlying
  model".
- "Description disambiguation" is named as a next step, not tested.
- Close-neighbour techniques that share nouns ("requirements", "writing") are a harder
  case than the paper's. INFERRED.

## The body

- Under 500 lines (spec: under 5,000 tokens); detail in files one level deep; a table of
  contents in a reference file over 100–300 lines. VERIFIED.
- Concise, only what Claude does not already know; one term per concept; checklists and
  validate-fix loops for multi-step work. VERIFIED.
- skill-creator prefers explaining why over capitalised MUST and NEVER; the best
  practices suggest stronger wording when a rule is missed. The two conflict. VERIFIED.
- A loaded body is not re-read in later turns, and only its first 5,000 tokens survive
  compaction: key instructions at the top; rules that must always hold belong in a
  hook. VERIFIED.

## References between skills and files

- Link a file by relative path, saying what it holds and when to read it; keep
  references one level deep, since nested ones risk partial reads. A reference file
  costs nothing until read. VERIFIED.
- No source says how one skill should name another so that it is loaded; a search of
  the Claude Code docs found nothing. Naming the exact `name` (namespaced `plugin:skill`
  across a plugin) is probably matchable. INFERRED; a gap.
- A file path is a guaranteed route; a skill name depends on Claude choosing to call the
  Skill tool. INFERRED.
- `disable-model-invocation: true` "removes the skill from Claude's context entirely";
  the docs' table says Claude can invoke it "Not on its own". Whether a step skill that
  names it can still load it is not stated. VERIFIED for the quotes; the rest is open.
  This corrects `research/2026-10-17-skill-tiering.md`, which reported as VERIFIED that
  a step skill could not call such a skill: the docs do not say so.

## For datum (INFERRED)

- Descriptions of 250–450 characters, opening with "Use when…", naming the situation
  that triggers the skill rather than only a user request, since a step skill is often
  the caller; 3–5 trigger phrases in plain words; a boundary line on every close
  neighbour ("Not for X; use Y").
- The packaging test holds the description text constant across variants: in the
  reference-file variant it becomes the step's "read X when Y" pointer line.
- Part A of the test uses the optimizing-descriptions method: about 20 queries, half
  near-misses, 3 runs each.
- `disable-model-invocation: true` on techniques would take them out of the listing and
  out of the shadowing pool. Whether a step skill can still call them is untested; a
  cheap third variant for the packaging test.

## Gaps

- How to name a sibling skill in a body so that it is invoked.
- Whether packaging (skill or reference file) changes selection. The paper varies only
  library size.
- Whether boundary lines reduce shadowing; recommended, not measured.
- The best description length: 1,024 and 1,536 are limits; 400–500 is a community
  guideline.
