# What a research technique must guard against (2026-11-23)

Question: what should the `research` technique (#58) tell a subagent so that the
conclusion it hands back can be trusted enough to enter a requirement? Three parts,
agreed with Amit: (a) how agent research fails; (b) quick ways to judge a source; (c)
tools that find papers and give their full text. Amit's concern: subagents read an
arXiv abstract and stop there.

Method: web searches, then the primary sources read by `web-fetch` subagents, with gaps
filled by `curl` on the raw page or an API. Pendentive had no research agent to compare
(its history holds only `model-auditor`); datum's own earlier draft is
`experiments/2026-10-18-packaging-test/source/techniques/research.md`.

Labels: **VERIFIED** = read in a primary source (named). **VERIFIED-secondary** = only a
search summary or third-party page was seen. **INFERRED** = my reasoning. Quotes are
short.

## Summary

1. **Made-up sources are common, and real ones are often cited for what they do not
   say.** The second failure matters more for datum: a real source with a wrong value.
   (§1.1, §1.2)
2. **An abstract is the part of a paper most likely to overstate it.** In the medical
   studies, spin is densest in abstract conclusions. The body has spin too, but in the
   Discussion: the Results section is the least affected. (§1.3)
3. **The fetch tool itself hides the full text.** Claude Code's WebFetch returns another
   model's answer about the page, not the page, and stops reading at a length limit.
   This session hit both. A rule that only says "read the full text" is not enough if
   the tool never shows it. (§1.4)
4. **Source quality has to be asked for.** Anthropic's research agents preferred content
   farms until source-quality guidance was added to their prompts. (§1.5)
5. **The brief needs four things:** objective, output format, tools and sources, and
   bounds. Vague briefs gave duplicated or missing work. (§1.5)
6. **For judging a source quickly, SIFT fits:** stop, investigate the source, find
   better coverage, trace the claim to its original. "Trace" is the move that answers
   the abstract problem. (§2)
7. **Full text is reachable without new tools for most papers:** arXiv HTML pages,
   OpenAlex's open-access URL, and Semantic Scholar's body-text snippets. An MCP server
   is optional, and keyless APIs throttle. (§3)

## 1. How agent research fails

### 1.1 Made-up and wrong citations

- Walters & Wilder (Sci Rep 13:14045, 2023), 84 short literature reviews on 42 topics:
  "55% of the GPT-3.5 citations but just 18% of the GPT-4 citations are fabricated";
  of the real ones, "43% … but just 24% of the real GPT-4 citations include substantive
  citation errors". Book chapters were worst: "Even with GPT-4, however, 70% of the
  cited book chapters are fabricated." The texts were generated in April 2023, with no
  web access. VERIFIED (PMC10484980, Abstract and Results).
- With search, the failure moves from making up a source to misreading a real one
  (DeepTRACE, §1.2). INFERRED from the two studies together.

### 1.2 Claims a real source does not support

- DeepTRACE (arXiv 2509.04499) audits deep-research systems. Its abstract says they
  "include large fractions of statements unsupported by their own listed sources" with
  "citation accuracy ranging from 40–80% across systems". In the introduction,
  unsupported-statement rates "remain high for several DR engines (YouChat(DR) 74.6%;
  PPLX(DR) 97.5%)". Also: "Listing more sources does not guarantee better grounding."
  VERIFIED (arxiv.org/html/2509.04499, Abstract and §1; the per-system table was not
  read verbatim).
- Other benchmarks say the same (ReportBench 2508.15804; a URL study 2604.03173 found
  3–13% of citation URLs invented, worst in deep-research agents). VERIFIED-secondary
  (search summaries only).
- Consequence for datum: a finding is checkable only if it carries the passage it rests
  on. The quote rule agreed on 2026-11-23 targets exactly this. INFERRED.

### 1.3 Abstracts overstate

All three studies are of medical trials. Whether the rates carry over to computer science
papers is not known (INFERRED: the incentive is the same).

- Boutron et al. (JAMA 2010), 72 trials with non-significant primary outcomes: spin in
  abstract Conclusions in 58.3%; in the main text, Results 29.2%, Discussion 43.1%,
  Conclusions 50.0%. VERIFIED (abstract via Europe PMC, PMID 20501928).
- Jellison et al. (BMJ EBM 2019), 116 psychiatry and psychology trials: spin in 56%;
  "2 (2%) titles, 24 (21%) abstract results sections and 57 (49.1%) abstract conclusion
  sections". VERIFIED (abstract via Europe PMC, PMID 31383725).
- Oncology trials (Crit Rev Oncol Hematol 2019): spin in "46 of 124 (37.1%)" abstracts;
  "The conclusion sections of abstracts were most prone to contain spin." VERIFIED
  (abstract via Europe PMC, PMID 31733444).
- Consequence: reading the full text helps only if the agent reads the Results (the
  tables, the numbers, the setup) rather than the Discussion. A value taken from a paper
  comes from where it was measured, with its conditions. INFERRED.
- A note on method: these numbers come from abstracts. They are the abstracts' own
  headline figures, which is what this pass needed. The papers' bodies were not read.
- No study was found that compares an LLM reading the abstract only against the same LLM
  reading the full text, for extracting a fact. One preprint found full-text *screening*
  harder for LLMs than abstract screening (arXiv 2502.15702). VERIFIED-secondary.

### 1.4 The fetch tool hides the page

- Claude Code docs: "For most pages, Claude doesn't see the full text. It asks a
  question about the page, and a separate model call reads the page and returns an
  answer." For the raw page: "ask it to run `curl` on the URL through the Bash tool."
  The `web-fetch` subagent "reads pages of up to about 48,000 characters in full, and
  WebFetch reads the first 100,000". VERIFIED (code.claude.com/docs/en/tools-reference,
  read raw with curl).
- Seen in this session: two reading subagents reported that they had read a page only
  up to its first ~40,000 characters verbatim and had the rest as a summary (the
  DeepTRACE paper, the tools reference). PubMed refused every fetch ("Cookies must be
  enabled"), and the Semantic Scholar API answered with 429 on the first keyless call.
  One subagent said so honestly; nothing makes the next one do so. VERIFIED
  (observed).
- The Read tool reads a PDF whole, or in page ranges of up to 20 for longer ones.
  VERIFIED (tools reference). This machine has no `pdftotext` or `pandoc`. VERIFIED
  (observed); other builders' machines will differ.
- Consequence: the technique must make the subagent say, per source, how much of it was
  read, and that a quote came from the page and not from a summary of it. INFERRED.

### 1.5 Source quality, briefs and stopping (Anthropic)

From "How we built our multi-agent research system" (Anthropic engineering, June 2025).
VERIFIED (read by a subagent; quotes as it returned them).

- Agents "consistently chose SEO-optimized content farms over authoritative but less
  highly-ranked sources". "Adding source quality heuristics to our prompts helped resolve
  this issue." Their judge checked "did it use primary sources over lower-quality
  secondary sources?"
- "Each subagent needs an objective, an output format, guidance on the tools and sources
  to use, and clear task boundaries." Without these, "agents duplicate work, leave gaps,
  or fail to find necessary information."
- Search: "start with short, broad queries, evaluate what's available, then
  progressively narrow focus."
- Effort: "Simple fact-finding requires just 1 agent with 3-10 tool calls." Failure
  modes include "scouring the web endlessly for nonexistent sources" and "agents
  continuing when they already had sufficient results".
- Citations are added by a separate step (a citation agent), not by the researcher.
- The post says nothing about full documents against snippets.

## 2. Judging a source quickly

- SIFT (Caulfield, 2019): **Stop** ("Ask yourself whether you know the website or source
  of the information"); **Investigate the source**; **Find better coverage** ("ignore the
  source that reached you, and look for trusted reporting or analysis on the claim");
  **Trace** claims, quotes and media to the original context, e.g. a claim "based on a
  research finding" whose research may not say it. VERIFIED (hapgood.us, 2019-06-19).
- It is built on Stanford's lateral-reading studies of fact-checkers. VERIFIED-secondary.
- One critique: searching to check a claim can raise belief in it when the results are
  dominated by poor sources (attributed to a 2024 Nature paper). VERIFIED-secondary; not
  read.
- For an agent, the useful parts: an order of preference among sources (the standard or
  official documentation, then the paper's own Results, then everything else); Trace
  (follow a secondary claim to the source it cites, and read that); and Find better
  coverage when the first hit is a blog or a summary. INFERRED.

## 3. Getting the full text

- **arXiv HTML:** an HTML version at `arxiv.org/html/<id>`, on every new TeX submission
  since 2023, backfilled for older ones; "a small percentage of papers will not have an
  HTML version". Error-free conversion is "currently 75%" (Ginev et al., arXiv
  2605.16562). VERIFIED (info.arxiv.org accessible_HTML; the 2605.16562 abstract). The
  arXiv API also answered a keyless query. VERIFIED (observed).
- **OpenAlex:** a work's `open_access.oa_url` is "the best full-text link OpenAlex
  found"; locations carry `pdf_url`. OA means readable "without paying money or logging
  in". VERIFIED (help.openalex.org). Unpaywall shares OpenAlex's open-access pipeline
  and needs an email. VERIFIED-secondary.
- **Semantic Scholar snippet search:** `/graph/v1/snippet/search` returns "excerpts of
  approximately 500 words, drawn from a paper's title, abstract, and body text", with
  the section. VERIFIED (its OpenAPI file). Keyless calls share one pool and were
  throttled at once here (429). VERIFIED (observed). Useful for finding the passage to
  quote, not for reading a paper.
- **Europe PMC REST API:** answered keyless where PubMed refused; gives abstracts, and
  full text for open-access PMC papers. VERIFIED for abstracts (observed); full text
  not tried.
- **paper-search-mcp** (openags): one MCP server over ~20 sources (arXiv, Semantic
  Scholar, OpenAlex, PMC, Europe PMC, Unpaywall, …), with a `download_with_fallback`.
  Read support is marked per source, many "⚠ info-only" or "best-effort". Sci-Hub is
  present but "disabled by default". VERIFIED (GitHub README, read to ~70%).
- Consequence: no MCP server is needed for v0. The technique can name the open routes
  (arXiv HTML, the OA URL, Europe PMC) and say "fetch the page raw when the tool
  summarises". Shipping or requiring an MCP server is a separate decision; Sci-Hub must
  never be used. INFERRED.

## What this suggests for the technique (to agree, not agreed)

INFERRED throughout; for the next round of questions.

1. Each finding carries a quote from the passage it rests on, and says where in the
   source it is (section, table, page) and how much of the source was read.
2. A value from a paper is VERIFIED only if it was read in the body, where it was
   measured (Results, a table), not in the abstract or the discussion. An abstract-only
   finding is VERIFIED-secondary or INFERRED.
3. A summary from a fetch tool is not a reading. The quote must come from the page's
   text; when the tool summarises or cuts the page, fetch the raw page or the PDF.
4. Prefer the primary source: the standard, the official documentation, the paper.
   Trace a secondary claim to its source before using it.
5. A fetch that failed or was refused is reported, not filled from memory (the agreed
   "no web access" rule, widened to a single source).
6. The brief holds the four parts Anthropic names, and a budget: a lookup is a few
   calls, not a survey.

## Not reached

- A study of abstract-only against full-text fact extraction by an LLM.
- The full Anthropic post read raw; the DeepTRACE tables; Unpaywall's own docs.
- How far the medical spin rates transfer to software and AI papers.
