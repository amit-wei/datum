"""Blind comparison of the requirement sets written in N1, datum against the baseline.

Usage: python3 evaluate.py [--model sonnet]

Each datum N1 run (Sonnet) is paired with a baseline N1 run, in the order they were recorded.
First each run's output is rewritten as a plain list by a normaliser, so neither set
shows its file format, IDs or tooling. Then an evaluator that is told nothing about how
either set was made compares the two, in both orders (X/Y swapped), and writes a short
report with a verdict. A verdict counts for a side only when both orders agree.

Resumable: normalised sets and evaluations already in results/evaluations.jsonl are
skipped; a failed call stops the script without recording anything.
"""
import argparse
import os

from common import (WORK, EVALUATIONS, HERE, RUNS, OutOfUsage, append_jsonl, ask, changed_files,
                    last_json, read_jsonl, stop)

MODEL_DIR = os.path.join(HERE, "fixtures", "N1", ".datum", "model", "product")

NORMALISE = """Below are files an author wrote: requirements for a small app, and plans for
checking each one. Rewrite their content as a plain numbered list. For each requirement
give its statement, its reason if one is given, and how it will be checked (the kind of
check, the pass condition and any conditions). Keep the author's wording and every number.
Drop file names, IDs, field names, cross-references, status markers and formatting, and
any mention of tools, folders or processes. Add nothing, judge nothing, and leave out
anything that is not a requirement or a check (notes, summaries). Then add a second list,
"Left open": every value or rule the author did not settle but left open (marked to be
decided, or put as a question to the person who owns the requirements, in the files or in
the author's final message), each with its question as asked, or "none". Output only the
two lists.

<files>
{files}
</files>

The author's final message:
<final>
{final}
</final>"""

EVALUATE = """You are reviewing two sets of requirements written independently for the same
small app, a plant-watering planner. Below is everything the authors were given: what
the owner said they need, the journeys and functions already agreed, and what must
never happen.

<inputs>
{inputs}
</inputs>

<set X>
{x}
</set X>

<set Y>
{y}
</set Y>

A separate team will build the app and write its tests from one of these sets. A value or
rule left open with a question for the person who owns the requirements ("Left open") is
not a defect. A value or rule stated as settled with no source in the inputs is. Compare the sets on:
- coverage: does every agreed function and every "must never happen" get what it needs?
- faithfulness: values and choices come from the inputs; nothing invented or contradicted
- clarity: each requirement can be read only one way and checked
- the checks: each is concrete, would catch a failure, and costs no more than needed
- restraint: nothing unnecessary; no conflicts between requirements
Length is not a merit. Write a report of at most 250 words, then end with one JSON object:
{{"verdict": "X" or "Y" or "tie", "reason": "<one sentence>"}}"""


def inputs():
    parts = []
    for folder in ("analysis", "functions"):
        for name in sorted(os.listdir(os.path.join(MODEL_DIR, folder))):
            parts.append(open(os.path.join(MODEL_DIR, folder, name)).read().strip())
    return "\n---\n".join(parts)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="sonnet")
    args = p.parse_args()
    runs = read_jsonl(RUNS)
    datum = [r for r in runs if r["query"] == "N1" and r["variant"] == "datum"
             and r["model"] == "sonnet"]
    base = [r for r in runs if r["query"] == "N1" and r["variant"] == "baseline" and r["model"] == "sonnet"]
    records = read_jsonl(EVALUATIONS)
    normal = {r["run"]: r["text"] for r in records if r["kind"] == "normalised"}
    judged = {(r["pair"], r["order"]) for r in records if r["kind"] == "evaluation"}
    context = inputs()
    for d, b in zip(datum, base):
        for run in (d, b):
            if run["run"] in normal:
                continue
            work = os.path.join(WORK, run["run"])
            diff = changed_files(work, run["base"])
            final = open(os.path.join(work, "final.txt")).read()
            try:
                text, cost = ask(NORMALISE.format(files=diff[:80000], final=final[:12000]), args.model)
            except OutOfUsage as e:
                stop(f"normaliser call failed: {e}")
            normal[run["run"]] = text
            append_jsonl(EVALUATIONS, {"kind": "normalised", "run": run["run"], "text": text,
                                       "cost_usd": cost})
            print(f"normalised {run['run']}", flush=True)
        pair = f"{d['run']}|{b['run']}"
        for order, (x, y) in (("datum=X", (d, b)), ("datum=Y", (b, d))):
            if (pair, order) in judged:
                continue
            try:
                text, cost = ask(EVALUATE.format(inputs=context, x=normal[x["run"]],
                                                 y=normal[y["run"]]), args.model)
            except OutOfUsage as e:
                stop(f"evaluator call failed: {e}")
            try:
                verdict = last_json(text[text.rindex("{\"verdict\""):] if "{\"verdict\"" in text else text)
                side = verdict["verdict"]
            except (ValueError, KeyError, TypeError):
                side = None
            winner = None if side is None else "tie" if side == "tie" else (
                "datum" if side == order[6] else "baseline")
            append_jsonl(EVALUATIONS, {"kind": "evaluation", "pair": pair, "order": order,
                                       "verdict": side, "winner": winner, "report": text,
                                       "cost_usd": cost})
            print(f"evaluated {pair} {order}: {winner}", flush=True)


if __name__ == "__main__":
    main()
