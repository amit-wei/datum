---
name: grilling
description: Use at the start of every part's functional analysis, and whenever something only the builder can settle is open - a need, a preference, a priority, a premise, a value only they know, a trade between goals, or a reviewer finding the builder must decide. Keeps the builder's view of the part and yours the same. Not for facts that can be looked up (use research) or values that can be measured (use running-a-spike).
---

# Grilling

Grilling keeps the builder's view of the part and yours the same, so the two do not
drift apart while the work goes on. Run it in the main session, never in a subagent:
the agent that does the work is the one that has to understand the builder.

## Before you ask

1. Read the part's inputs in the model: for the product, what the builder has said so
   far; for any other part, what the parent's synthesis gave it, and the earlier
   elicitation records of this part.
2. List what the inputs leave open. Drop anything the model, the code or research can
   answer: ask the builder only what only they know.
3. At the start of a part, write your current picture of the part in a few lines: what
   it is for, who uses it, what it must do, what it must not. Show it to the builder
   first and ask them to correct it. Their corrections often settle half the list.

If nothing is open, say so with the reason, and ask the builder to confirm.

## Asking

- Ask a few questions at a time, unless the builder's own instructions set the pace.
- Each question states the issue, your proposed answer and your confidence, so the
  builder can accept, reject or reframe it. Make the proposal concrete enough to be
  wrong.
- Ask about what the builder needs and why, not about solutions. A solution they name
  is a premise: ask what it is for, then keep the need and treat the solution as one
  option.
- When the builder skips a question, ask it again briefly in the next round.
- Expect reframes. When an answer changes the question, drop your list and redo it from
  the new picture.

## When an answer is vague

"Fast", "simple", "secure", "like app X" cannot be written down yet. Help the builder
make it concrete:

- Ask for the observable thing behind it: what they would see, an example, or a number
  with its reason.
- Offer two or three concrete options or contrasting cases: "would a 2-second wait
  count as fast? would 10?"
- Say back what you understood, in your own words, and ask whether it is right.

If the builder does not know either, do not guess: turn it into research, a spike, or
a `TBD` with an issue, and say which.

## Ending

Stop when every open point is settled, marked out of scope with a reason, or a `TBD`
with an issue. Then say back the agreed picture of the part in a few lines and get the
builder's yes.

## The record

One elicitation record per grilling round, `ELI-` in the part's `analysis/` folder.
Make the ID with:

```
echo "ELI-$(LC_ALL=C tr -dc '0-9A-HJKMNP-TV-Z' </dev/urandom | head -c 4)"
```

Each entry is numbered and holds the question and the builder's answer in their own
words. An entry that states a need says so; scenarios and functions link to it as
`ELI-XXXX` with the entry number. When an answer fills a field elsewhere (a value, a
choice), write it there too, and cite the entry.

An example, for illustration only:

```yaml
id: ELI-3RWN
date: 2026-10-18
entries:
  - n: 1
    question: Who logs the sessions: the athlete, the coach, or both?
    answer: "Just me. A coach might look at it later but that's not now."
    need: true
  - n: 2
    question: When you say the plan should be safe, what would unsafe look like?
    answer: "Jumping my weekly load by a lot after a week off."
    need: true
```
