"""Score results/runs.jsonl against the queries in queries.md.

A run is correct when it loaded every expected name in order (skills, reference files
and agents; a failed load does not count) and attempted nothing under "Must not".
`none` expects no technique at all; loading the router or a step is allowed.
The decision rule uses the validation split; the training split is reported too.

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
        if header is None or not re.fullmatch(r"[PN]\d+", cells[0]):
            continue
        row = dict(zip(header, cells))
        queries.append({
            "id": row["#"], "split": row["Split"], "fixture": row["Fixture"],
            "prompt": row["Prompt"], "expected": NAME.findall(row["Expected"]),
            "must_not": NAME.findall(row.get("Must not", "")),
        })
    return queries


def techniques():
    return {f[:-3] for f in os.listdir(os.path.join(HERE, "source", "techniques"))}


def correct(query, loads, techs):
    attempted = [e["name"] for e in loads]
    loaded = [e["name"] for e in loads if not e["error"]]
    if any(n in attempted for n in query["must_not"]):
        return False
    if query["expected"] == ["none"]:
        return not any(n in techs for n in attempted)
    it = iter(loaded)
    return all(name in it for name in query["expected"])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--runs", default=os.path.join(HERE, "results", "runs.jsonl"))
    args = p.parse_args()
    queries = {q["id"]: q for q in load_queries()}
    techs = techniques()
    cells = collections.defaultdict(lambda: [0, 0, 0.0])
    misses = collections.defaultdict(list)
    for line in open(args.runs):
        run = json.loads(line)
        q = queries[run["query"]]
        ok = correct(q, run["loads"], techs)
        for split in (q["split"], "all"):
            cell = cells[(run["variant"], run["model"], split)]
            cell[0] += ok
            cell[1] += 1
            cell[2] += run["cost_usd"] or 0
        if not ok:
            misses[(run["variant"], run["model"])].append(
                f"{q['id']}: " + (" > ".join(e["name"] + ("!" if e["error"] else "")
                                            for e in run["loads"]) or "-"))
    print("| Variant | Model | Validation | Training | All | Cost |")
    print("|---|---|---|---|---|---|")
    for variant, model in sorted({(v, m) for v, m, _ in cells}):
        row = [cells[(variant, model, s)] for s in ("val", "train", "all")]
        fmt = lambda c: f"{c[0]}/{c[1]}" if c[1] else "-"
        print(f"| {variant} | {model} | {fmt(row[0])} | {fmt(row[1])} | {fmt(row[2])} | ${row[2][2]:.2f} |")
    for key, rows in sorted(misses.items()):
        print(f"\nMisses {key[0]} {key[1]}: " + "; ".join(rows))


if __name__ == "__main__":
    main()
