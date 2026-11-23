"""Check a per-criterion blind evaluator for position bias before it is used (#72).

Usage: python3 check.py [--model sonnet]

Reuses the normalised sets already recorded by two earlier rigs, so no run or
normaliser call is made:
- self-pairs: one #62 set shown as both X and Y (a fair evaluator answers tie)
- the three #62 pairs (2026-11-14 retest), both orders: close sets, where the old
  evaluator followed the position
- the six 2026-11-13 pairs, both orders: the known case, where the old evaluator
  preferred the baseline in both orders

Resumable: evaluations already in results/evaluations.jsonl are skipped; a failed call
stops the script without recording anything.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(HERE)
RETEST = os.path.join(EXP, "2026-11-14-requirements-retest")
OLD = os.path.join(EXP, "2026-11-13-requirements-test")
sys.path.insert(0, RETEST)
from common import OutOfUsage, append_jsonl, ask, read_jsonl, stop  # noqa: E402

OUT = os.path.join(HERE, "results", "evaluations.jsonl")
CRITERIA = ["coverage", "faithfulness", "clarity", "checks", "restraint"]

EVALUATE = """You are reviewing two sets of requirements written independently for the same
small app, {app}. Below is everything the authors were given: what the owner said they
need, the journeys and functions already agreed, and what must never happen.

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
rule left open with a question for the person who owns the requirements is not a defect.
A value or rule stated as settled with no source in the inputs is.

Judge each criterion on its own:
- coverage: does every agreed function and every "must never happen" get what it needs?
- faithfulness: values and choices come from the inputs; nothing invented or contradicted
- clarity: each requirement can be read only one way and checked
- checks: each check is concrete, would catch a failure, and costs no more than needed
- restraint: nothing unnecessary; no conflicts between requirements

For each criterion, first list the evidence from set X and from set Y, then give the
verdict. Answer "tie" when the sets are equal on it or the difference is small; name a set
only when the difference would matter to the team. Length is not a merit. Keep the
evidence to at most 400 words in all, then end with one JSON object:
{{"coverage": "tie" or "X" or "Y", "faithfulness": ..., "clarity": ..., "checks": ..., "restraint": ...}}"""

APPS = {
    "retest": ("a plant-watering planner", os.path.join(RETEST, "fixtures", "N1", ".datum", "model", "product")),
    "old": ("a shared-expense splitter", os.path.join(OLD, "fixtures", "F1", ".datum", "model", "product")),
}


def inputs(model_dir):
    parts = []
    for folder in ("analysis", "functions"):
        for name in sorted(os.listdir(os.path.join(model_dir, folder))):
            parts.append(open(os.path.join(model_dir, folder, name)).read().strip())
    return "\n---\n".join(parts)


def recorded(folder):
    """Normalised sets and the datum|baseline pairs an earlier rig evaluated."""
    records = read_jsonl(os.path.join(folder, "results", "evaluations.jsonl"))
    normal = {r["run"]: r["text"] for r in records if r["kind"] == "normalised"}
    pairs = []
    for r in records:
        if r["kind"] == "evaluation" and r["pair"] not in pairs:
            pairs.append(r["pair"])
    return normal, pairs


def parse(text):
    import json
    start = text.rfind('{"coverage"')
    if start < 0:
        return None
    try:
        obj = json.loads(text[start:text.rindex("}") + 1])
    except ValueError:
        return None
    return {c: obj.get(c) for c in CRITERIA}


def cases():
    """(case, set, pair, order, app key, run shown as X, run shown as Y)."""
    out = []
    normal_new, pairs_new = recorded(RETEST)
    normal_old, pairs_old = recorded(OLD)
    first = [p.split("|") for p in pairs_new]
    for run in (first[0][0], first[0][1], first[1][0]):
        out.append(("self", normal_new, f"{run}|{run}", "self", "retest", run, run))
    for normal, pairs, case, app in ((normal_new, pairs_new, "retest", "retest"),
                                     (normal_old, pairs_old, "known", "old")):
        for pair in pairs:
            d, b = pair.split("|")
            out.append((case, normal, pair, "datum=X", app, d, b))
            out.append((case, normal, pair, "datum=Y", app, b, d))
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="sonnet")
    args = p.parse_args()
    done = {(r["pair"], r["order"]) for r in read_jsonl(OUT)}
    contexts = {k: inputs(d) for k, (_, d) in APPS.items()}
    for case, normal, pair, order, app, x, y in cases():
        if (pair, order) in done:
            continue
        prompt = EVALUATE.format(app=APPS[app][0], inputs=contexts[app], x=normal[x], y=normal[y])
        try:
            text, cost = ask(prompt, args.model)
        except OutOfUsage as e:
            stop(f"evaluator call failed: {e}")
        sides = parse(text)
        winners = None
        if sides is not None and order != "self":
            datum_side = "X" if order == "datum=X" else "Y"
            winners = {c: None if s not in ("X", "Y", "tie") else "tie" if s == "tie"
                       else ("datum" if s == datum_side else "baseline") for c, s in sides.items()}
        append_jsonl(OUT, {"case": case, "pair": pair, "order": order, "sides": sides,
                           "winners": winners, "report": text, "cost_usd": cost})
        print(f"{case} {pair} {order}: {sides}", flush=True)


if __name__ == "__main__":
    main()
