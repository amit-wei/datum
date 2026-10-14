# Skill granularity and workflow composition (2026-10-14)

Condensed from a Sonnet research agent's report. VERIFIED means a primary source was
seen. INFERRED means it is the agent's reasoning.

## Anthropic guidance (VERIFIED)

From https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices and
https://agentskills.io/specification:

- Keep the SKILL.md body under 500 lines (spec: under about 5k tokens). Put detail in
  reference files linked one level deep. Give long references a table of contents.
- Descriptions are written in the third person and say what the skill does and when to
  use it. Claude picks among "potentially 100+" skills from the description alone.
- Put deterministic or fragile steps in scripts. Use "validator, fix, repeat" and
  plan-validate-execute.
- Write evals before extensive docs, at least 3, run on Haiku, Sonnet and Opus.

From https://code.claude.com/docs/en/skills:

- Frontmatter fields: `disable-model-invocation`, `user-invocable`, `context: fork`,
  `allowed-tools`, `paths` (glob gating) and `hooks` (active while the skill is active).
- The listing allows 1,536 characters per entry, and the whole listing gets 1% of the
  context window. On overflow, the descriptions of the least-invoked skills are dropped.
- After compaction only the start of each invoked skill is kept, so put critical
  instructions first.
- **A rule that must hold every time belongs in a hook, not in skill prose.**
- There is no documented primitive for one skill to call another. Options are stacking
  `/a /b`, a `context: fork` skill, or a subagent's `skills:` preload.

Plugin structure (https://code.claude.com/docs/en/plugins-reference):

- Directories: `skills/`, `agents/`, `hooks/hooks.json`, `.mcp.json`, `bin/`,
  `workflows/*.js`, `evals/`.
- Components are namespaced as `plugin:name`.
- Dependencies are semver-resolved against git tags.
- Use `${CLAUDE_PLUGIN_DATA}` for state that must survive updates.
- A `CLAUDE.md` at the plugin root is not loaded.

## How libraries size their skills

- **superpowers** (V): 15 skills, each at the scale of an activity or discipline. The chain
  is brainstorming → worktrees → writing-plans → subagent-driven-development (with TDD)
  → code review → finishing a branch. A `using-superpowers` skill loaded at session start
  acts as the router (INF). Atomic techniques are sub-files inside skills.
- **Spec Kit** (V): one skill per lifecycle phase, with an explicit verdict at the end of
  each sequence.
- **OpenSpec** (V): a default of 4 commands (explore, propose, apply, archive) and an
  expanded profile of 10. State lives in `openspec/changes/<name>/`, and the tasks.md
  checklist tracks progress.
- **Pattern** (INF): 5 to 15 activity-scale skills per workflow. Nobody ships dozens of
  single-rule skills.

## Triggering and evals

- `claude plugin eval` (V) runs each case with and without the plugin. Graders are
  `tool_used`, `tool_order`, `regex`, `file_exists`, `llm` and `baseline`. A
  `tool_used: Skill` grader checks triggering. Typical first finding: near-zero delta
  because the skill never triggered.
- There is no official benchmark of triggering accuracy against the number of skills.
  Blog anecdotes (unverified) claim about 15 to 25 skills with full descriptions in a
  200K window, and 9 of 66 skills that never fired.

## Composition patterns

- Sequences are declared in prose: each skill ends with "next, invoke X" (V:
  superpowers, Spec Kit).
- **State on disk** (V: OpenSpec, Spec Kit): which files exist tells you where you are.
  This is portable and survives sessions.
- **Hooks for gates** (V): `PreToolUse` and `PostToolUse` call scripts.
- **Claude Code dynamic workflows** (V, https://code.claude.com/docs/en/workflows): JS
  with `agent()`, `pipeline()`, `parallel()` and `phase()`. The script decides what runs
  next. Limits: no user input mid-run, and Claude only.

## Portability

- Portable: SKILL.md folders (an open standard) and file-based state.
- Claude-specific: hooks, subagents, `context: fork`, `paths`, the plugin manifest and
  marketplace, and dynamic workflows. Declare such needs in the spec's `compatibility`
  field.

## Recommendation from the agent

- **Granularity:** about 10 to 15 activity-scale core skills, plus 3 to 6 thin atomic
  commands marked `disable-model-invocation: true`. Atomic rules go in `references/` and
  in validator scripts. Each description is unique and includes a "NOT for" clause.
- **Composition:**
  - a workflow manifest read by a driver skill
  - a small state file, or state derived from artifact status
  - skills that check the entry gate on start and update state on exit
  - gates as scripts, enforced on Claude by hooks
  - optional Claude-only `workflows/*.js` for fan-out stages such as multi-reviewer
    verification
- **Evals:** ship `evals/` with should-trigger and should-not-trigger cases plus outcome
  graders. Test with the full skill set loaded.
