---
name: research
description: Use when a value, rule or answer depends on what is already established outside the model and the conversation - a convention or definition, a standard or law, a known limit, an existing solution, or anything that changes over time such as prices, quotas and versions. Runs in a subagent that reads written sources and quotes them. Not for what only the builder knows (use grilling) or what must be measured (use running-a-spike).
---

# Research

Research settles a question from written sources, so that what enters the model rests on
a passage someone can check. Always run it in a subagent: the pages stay out of your
context, and an agent that only sees the question has no answer to look for.

Run it even when you feel sure of the answer. Recalled without a source, a convention or
a value is invented.

## Before you send it

1. Look in the part's `analysis/` folder, and the parent's, for a `RES-` record that
   already answers the question. If one does, cite it.
2. Write each question so one answer settles it: "what rise in weekly training load do
   studies tie to finger injuries in climbers", not "climbing injuries".
3. Put the questions a step has open into one brief, or run briefs in parallel, instead
   of one subagent per small lookup.

## The brief

Use a general-purpose subagent: it needs web search, web fetch, the shell and file
reading. The brief holds:

- **Objective:** the question, what the answer is for (the requirement, the function),
  and what is already known.
- **Output:** the report described in the rules below.
- **Sources:** where to look first when you know (a named standard, a library's own
  documentation).
- **Bounds:** what not to cover, and when to stop. The subagent stops when a primary
  source settles the question. If a few honest attempts find nothing, it reports "not
  found" with what it tried. For a question that needs a survey, say so and widen it.
- **The researcher's rules,** copied whole from the next section.

## The researcher's rules (copy into the brief)

- Use the primary source: the standard, the official documentation, the paper. When a
  claim reaches you second-hand (a blog, a summary, a forum), find the source it rests
  on and read that instead.
- Read a value from a paper where it was measured: the Results, a table, with its
  conditions. A value read only in the abstract or the discussion is labelled
  VERIFIED-secondary.
- Quote from the page's own text. A web fetch tool may return a model's summary of the
  page, or cut it at a length limit: then fetch the page raw with `curl`, or download
  the PDF and read it with the Read tool. For papers, try the arXiv HTML page
  (`arxiv.org/html/<id>`), the open-access link OpenAlex gives (`open_access.oa_url`),
  or Europe PMC. Never use Sci-Hub or other pirate copies.
- Report every fetch that failed or was refused, and what it left unanswered. Do not
  fill the gap from memory.
- Report, per finding: the claim; its label; the source (title, and a URL, DOI or
  standard number); where in it (section, table, page); how much of the source you read;
  and a short quote of the passage it rests on. Labels: VERIFIED (read in a primary
  source), VERIFIED-secondary (only a secondary source or a summary was seen), INFERRED
  (your reasoning).
- End with the answer to the question in a few lines, or "not found" and what you
  tried.

## When the report comes back

- Use a finding only if it carries its quote and where it is. Send back a finding
  without them, or treat it as INFERRED.
- When the sources disagree, or the answer is a range and a choice is left, the choice
  is the builder's: put it in the step's batch with the findings and your
  recommendation.
- A "not found" leaves the value `TBD` with an issue that says what was tried.

## The record

One record per brief, `RES-` in the `analysis/` folder of the part that asked. Make the
ID with:

```
echo "RES-$(LC_ALL=C tr -dc '0-9A-HJKMNP-TV-Z' </dev/urandom | head -c 4)"
```

It holds the date, the question, the findings as reported, numbered, and the
conclusion. A source is named so that anyone can find it again; a URL is one way. The
artifact that uses a finding cites it in its rationale as `RES-XXXX` with the finding
number.

An example, for illustration only (the sources are made up):

```yaml
id: RES-8DQM
date: 2026-11-28
question: What weekly rise in training load is tied to finger injuries in climbers?
findings:
  - n: 1
    claim: Climbers whose weekly load rose by more than 30% had about twice the rate of finger injuries.
    label: VERIFIED
    source: {title: "Load and injury in recreational climbers (example journal, 2024)", ref: "doi:10.0000/example"}
    where: Results, Table 3
    read: full text
    quote: "load increases above 30% per week were associated with an injury rate ratio of 2.1"
  - n: 2
    claim: A national climbing body advises rises of no more than 10% a week.
    label: VERIFIED-secondary
    source: {title: "Training guidance page (example climbing federation)", ref: "https://example.org/training"}
    where: section "Building up"
    read: summary only; the page refused a raw fetch
    quote: "increase volume by no more than 10% per week"
conclusion: |
  Rises above 30% a week double the injury rate in one cohort study; guidance asks for 10%.
  The limit between the two is the builder's choice.
```
