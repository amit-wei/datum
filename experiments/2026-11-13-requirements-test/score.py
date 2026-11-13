# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Print the results behaviour by behaviour, datum against the baseline.

Usage: uv run score.py [--model sonnet]

Judged behaviours come from results/verdicts.jsonl; mechanical ones (R5, R7) are
computed here from the run records and the files the runs wrote. Beside each datum cell:
whether datum loaded, expected loads missing, the write check (each new REQ file after
writing-requirements, each new PRF file after writing-proofs) and validator errors. Then
the blind evaluation per pair: a side wins a pair only when both orders agree.
"""
import argparse
import collections
import glob
import os
import re

import yaml

from common import EVALUATIONS, HERE, RUNS, VERDICTS, load_queries, read_jsonl

MAKERS = [(r"/requirements/REQ-", "writing-requirements"), (r"/proofs/PRF-", "writing-proofs")]


def checks(query, run):
    """What failed among the datum-only checks of one run."""
    loads = run["loads"]
    names = [e["name"] for e in loads if e["kind"] in ("skill", "agent") and not e["error"]]
    bad = [] if names else ["datum not loaded"]
    loaded = set()
    for e in loads:
        if e["kind"] == "skill" and not e["error"]:
            loaded.add(e["name"])
        if e["kind"] == "write" and any(re.search(p, e["name"]) and m not in loaded for p, m in MAKERS):
            bad.append("write check")
            break
    if run.get("validator_errors"):
        bad.append(f"validator {run['validator_errors']}")
    return bad + [f"no {n}" for n in query["expected"] if n not in names]


def subject_ok(run):
    """R5: every requirement statement the run wrote has 'the part' as its subject."""
    work = os.path.join(HERE, "work", run["run"])
    written = {e["name"] for e in run["loads"] if e["kind"] in ("write", "edit")}
    statements = []
    for path in glob.glob(os.path.join(work, ".datum/model/**/requirements/REQ-*.yaml"), recursive=True):
        if os.path.relpath(path, work) in written:
            try:
                statements.append(str((yaml.safe_load(open(path)) or {}).get("statement", "")))
            except yaml.YAMLError:
                statements.append("")
    return bool(statements) and all(re.search(r"\bthe part shall\b", s, re.I) for s in statements)


def done_checks(run):
    """R7: validator invoked, review-requirements run, no validator errors after the run."""
    kinds = {(e["kind"], e["name"]) for e in run["loads"] if not e["error"]}
    return (("validator", "validate") in kinds and ("agent", "review-requirements") in kinds
            and run.get("validator_errors") == 0)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="sonnet")
    args = p.parse_args()
    queries = load_queries()
    by_id = {q["id"]: q for q in queries}
    runs = [r for r in read_jsonl(RUNS) if r["model"] == args.model]
    verdicts = {(v["behaviour"], v["run"]): v for v in read_jsonl(VERDICTS)}
    print(f"| # | Datum | Baseline | Datum checks |\n|---|---|---|---|")
    fails = []
    for q in queries:
        source = by_id[q["fixture"]] if q["fixture"] in by_id else q
        cells, notes = {}, set()
        for variant in q["variants"]:
            mine = [r for r in runs if r["query"] == source["id"] and r["variant"] == variant]
            passed = 0
            for r in mine:
                if q["id"] == "R5":
                    ok = subject_ok(r)
                elif q["id"] == "R7":
                    ok = done_checks(r)
                else:
                    v = verdicts.get((q["id"], r["run"]))
                    ok = v and v["pass"]
                    if v and not v["pass"]:
                        fails.append(f"{q['id']} {r['run']}: {v['reason']}")
                passed += bool(ok)
                if variant == "datum" and q["fixture"].startswith("F"):
                    notes.update(checks(q, r))
            cells[variant] = f"{passed}/{len(mine)}" if mine else "-"
        print(f"| {q['id']} | {cells.get('datum', '-')} | {cells.get('baseline', '-')} "
              f"| {', '.join(sorted(notes)) or 'ok'} |")
    cost = sum((r["cost_usd"] or 0) for r in runs) + sum((v.get("cost_usd") or 0) for v in verdicts.values())
    print(f"\nCost on {args.model}, judge included: ${cost:.2f}")
    pairs = collections.defaultdict(dict)
    for e in read_jsonl(EVALUATIONS):
        if e["kind"] == "evaluation":
            pairs[e["pair"]][e["order"]] = e["winner"]
    if pairs:
        print("\nBlind evaluation (both orders must agree):")
        for pair, orders in pairs.items():
            sides = set(orders.values())
            result = sides.pop() if len(sides) == 1 and len(orders) == 2 else f"split {orders}"
            print(f"- {pair}: {result}")
    if fails:
        print("\nFails:\n- " + "\n- ".join(fails))


if __name__ == "__main__":
    main()
