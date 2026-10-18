"""Score results/runs.jsonl against the queries in queries.md.

A run is correct when three checks pass:
- outcome: the judge found the run meets the query's Outcome;
- write check: every new model file was preceded, in that run, by loading a technique
  that makes it (a requirement by writing-requirements or allocating-requirements...);
- must not: it attempted nothing under "Must not".
Expected loads (every expected name loaded in order; `none`: no technique) are reported
beside it, as a diagnostic. The decision rule uses the validation split.

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
            "outcome": row["Outcome"],
        })
    return queries


def techniques():
    return {f[:-3] for f in os.listdir(os.path.join(HERE, "source", "techniques"))}


# Which techniques may make a new file, by where it is written.
MAKERS = [
    (r"/functions/FUN-", {"writing-functions"}),
    (r"/requirements/REQ-", {"writing-requirements", "allocating-requirements"}),
    (r"/proofs/PRF-", {"writing-proofs"}),
    (r"/decisions/DEC-", {"trade-study"}),
    (r"/risks/RSK-", {"losses-and-hazards", "architectural-risk-pass"}),
    (r"/interfaces/IFC-", {"defining-interfaces"}),
    (r"/analysis/SCN-", {"writing-scenarios"}),
    (r"/analysis/ELI-", {"grilling"}),
    (r"/analysis/RES-", {"research"}),
    (r"/analysis/SPK-", {"running-a-spike"}),
    (r"parts\.yaml$", {"grouping-functions", "applying-stopping-rule"}),
]


def write_check(loads):
    """Every new model file came after loading a technique that makes it."""
    loaded = set()
    for e in loads:
        if e["kind"] in ("skill", "reference") and not e["error"]:
            loaded.add(e["name"])
        if e["kind"] == "write" and e["name"].startswith("model/"):
            for pattern, makers in MAKERS:
                if re.search(pattern, e["name"]) and not loaded & makers:
                    return False
    return True


def expected_loads(query, loads, techs):
    attempted = [e["name"] for e in loads if e["kind"] not in ("write", "edit")]
    loaded = [e["name"] for e in loads if not e["error"] and e["kind"] not in ("write", "edit")]
    if query["expected"] == ["none"]:
        return not any(n in techs for n in attempted)
    it = iter(loaded)
    return all(name in it for name in query["expected"])


def must_not(query, loads):
    return not any(e["name"] in query["must_not"] for e in loads if e["kind"] not in ("write", "edit"))


def correct(query, run):
    outcome = (run.get("outcome") or {}).get("pass") is True
    return outcome and write_check(run["loads"]) and must_not(query, run["loads"])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--runs", default=os.path.join(HERE, "results", "runs.jsonl"))
    args = p.parse_args()
    queries = {q["id"]: q for q in load_queries()}
    techs = techniques()
    cells = collections.defaultdict(lambda: [0, 0, 0.0, 0])
    misses = collections.defaultdict(list)
    for line in open(args.runs):
        run = json.loads(line)
        q = queries[run["query"]]
        ok = correct(q, run)
        for split in (q["split"], "all"):
            cell = cells[(run["variant"], run["model"], split)]
            cell[0] += ok
            cell[1] += 1
            cell[2] += (run["cost_usd"] or 0) + ((run.get("outcome") or {}).get("cost_usd") or 0)
            cell[3] += expected_loads(q, run["loads"], techs)
        if not ok:
            outcome = run.get("outcome") or {}
            why = [w for w, bad in (("outcome", outcome.get("pass") is not True),
                                    ("write check", not write_check(run["loads"])),
                                    ("must not", not must_not(q, run["loads"]))) if bad]
            misses[(run["variant"], run["model"])].append(
                f"{q['id']} ({', '.join(why)}): " + (" > ".join(
                    e["name"] + ("!" if e["error"] else "") for e in run["loads"]) or "-")
                + (f" | judge: {outcome.get('reason')}" if outcome.get("pass") is not True else ""))
    print("| Variant | Model | Validation | Training | All | Expected loads (all) | Cost |")
    print("|---|---|---|---|---|---|---|")
    for variant, model in sorted({(v, m) for v, m, _ in cells}):
        row = [cells[(variant, model, s)] for s in ("val", "train", "all")]
        fmt = lambda c: f"{c[0]}/{c[1]}" if c[1] else "-"
        print(f"| {variant} | {model} | {fmt(row[0])} | {fmt(row[1])} | {fmt(row[2])} "
              f"| {row[2][3]}/{row[2][1]} | ${row[2][2]:.2f} |")
    for key, rows in sorted(misses.items()):
        print(f"\nMisses {key[0]} {key[1]}:\n- " + "\n- ".join(rows))


if __name__ == "__main__":
    main()
