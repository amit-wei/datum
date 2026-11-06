"""Print results/runs.jsonl behaviour by behaviour, datum against the baseline.

A run passes when the judge found it meets the query's Outcome. Datum runs also show the
mechanical checks, which are not compared: the write check, Must not, the validator.
Expected loads are a diagnostic.

Usage: python3 score.py [--runs results/runs.jsonl]
"""
import argparse
import collections
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = re.compile(r"`([a-z0-9-]+)`")


def load_queries():
    queries, header = [], None
    for line in open(os.path.join(HERE, "queries.md")):
        if not line.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] == "#":
            header = cells
            continue
        if header is None or not re.fullmatch(r"B\d+r?", cells[0]):
            continue
        row = dict(zip(header, cells))
        queries.append({
            "id": row["#"], "split": row["Split"], "fixture": row["Fixture"],
            "prompt": row["Prompt"], "expected": NAME.findall(row["Expected"]),
            "must_not": NAME.findall(row["Must not"]), "outcome": row["Outcome"],
        })
    return queries


# Which techniques may make a new file.
MAKERS = [
    (r"/functions/FUN-", "writing-functions"),
    (r"/analysis/SCN-", "writing-scenarios"),
    (r"/analysis/ELI-", "grilling"),
    (r"/analysis/(LOS|HAZ)-", "losses-and-hazards"),
]


def write_check(loads):
    """Every new model file came after loading a technique that makes it."""
    loaded = set()
    for e in loads:
        if e["kind"] == "skill" and not e["error"]:
            loaded.add(e["name"])
        if e["kind"] == "write" and e["name"].startswith(".datum/model/"):
            if any(re.search(p, e["name"]) and m not in loaded for p, m in MAKERS):
                return False
    return True


def mechanics(query, run):
    """What failed among the datum-only checks, and which expected loads are missing."""
    loads = run["loads"]
    names = [e["name"] for e in loads if e["kind"] in ("skill", "agent") and not e["error"]]
    bad = []
    if not names:
        bad.append("datum not loaded")
    if not write_check(loads):
        bad.append("write check")
    if any(n in query["must_not"] for n in names):
        bad.append("must not")
    if run.get("validator_errors"):
        bad.append(f"validator {run['validator_errors']}")
    bad += [f"no {n}" for n in query["expected"] if n not in names]
    return bad


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--runs", default=os.path.join(HERE, "results", "runs.jsonl"))
    args = p.parse_args()
    queries = load_queries()
    by_id = {q["id"]: q for q in queries}
    cells = collections.defaultdict(lambda: [0, 0])
    notes, reasons, cost = collections.defaultdict(list), [], collections.Counter()
    for line in open(args.runs):
        run = json.loads(line)
        q, key = by_id[run["query"]], (run["query"], run["model"], run["variant"])
        outcome = run.get("outcome") or {}
        cells[key][0] += outcome.get("pass") is True
        cells[key][1] += 1
        cost[run["model"]] += (run["cost_usd"] or 0) + (outcome.get("cost_usd") or 0)
        if run["variant"] == "datum":
            notes[key] += mechanics(q, run)
        if outcome.get("pass") is not True:
            reasons.append(f"{run['query']} {run['variant']} {run['model']}: {outcome.get('reason')}")
    fmt = lambda c: f"{c[0]}/{c[1]}" if c[1] else "-"
    print("| # | Split | Model | Datum | Baseline | Datum checks |")
    print("|---|---|---|---|---|---|")
    for q in queries:
        for model in sorted({k[1] for k in cells if k[0] == q["id"]}):
            d, b = cells[(q["id"], model, "datum")], cells[(q["id"], model, "baseline")]
            print(f"| {q['id']} | {q['split']} | {model} | {fmt(d)} | {fmt(b)} "
                  f"| {', '.join(sorted(set(notes[(q['id'], model, 'datum')]))) or 'ok'} |")
    print("\nCost:", ", ".join(f"{m} ${c:.2f}" for m, c in cost.items()))
    if reasons:
        print("\nFails:\n- " + "\n- ".join(reasons))


if __name__ == "__main__":
    main()
