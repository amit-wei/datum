"""Judge every recorded run against each judged behaviour that reads it.

Usage: python3 judge.py [--model sonnet]

Resumable: a (behaviour, run) pair already in results/verdicts.jsonl is skipped. When a
judge call fails (a usage limit, an API error), nothing is recorded for it and the
script stops; rerun it to resume. An answer that is not readable JSON is recorded as
unreadable and can be rejudged by deleting its line.
"""
import argparse
import os

from common import (HERE, RUNS, VERDICTS, OutOfUsage, append_jsonl, ask, changed_files,
                    last_json, load_queries, read_jsonl, stop)

JUDGE = """You judge one run of an AI agent working on a software project's requirements.
The person said: {prompt}
The expected outcome, written before the run: {outcome}

The agent's final message:
<final>
{final}
</final>

The files the run added or changed (git diff; empty if none):
<diff>
{diff}
</diff>

Does the run meet the expected outcome? Judge only against the expected outcome, not
style or format. Answer with one JSON object and nothing else:
{{"pass": true or false, "reason": "<one or two sentences>"}}"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="sonnet")
    args = p.parse_args()
    queries = load_queries()
    by_id = {q["id"]: q for q in queries}
    done = {(v["behaviour"], v["run"]) for v in read_jsonl(VERDICTS)}
    runs = read_jsonl(RUNS)
    todo = []
    for q in queries:
        if q["outcome"].startswith("Mechanical"):
            continue
        source = by_id[q["fixture"]] if q["fixture"] in by_id else q
        todo += [(q, source, r) for r in runs if r["query"] == source["id"]
                 and r["variant"] in q["variants"] and (q["id"], r["run"]) not in done]
    print(f"{len(todo)} verdicts to do", flush=True)
    for q, source, run in todo:
        work = os.path.join(HERE, "work", run["run"])
        final = open(os.path.join(work, "final.txt")).read()
        diff = changed_files(work, run["base"])
        prompt = JUDGE.format(prompt=source["prompt"], outcome=q["outcome"],
                              final=final[:12000] or "(no final message)", diff=diff[:60000])
        try:
            text, cost = ask(prompt, args.model)
        except OutOfUsage as e:
            stop(f"judge call failed: {e}")
        try:
            verdict = last_json(text)
            record = {"pass": bool(verdict["pass"]), "reason": str(verdict.get("reason", ""))[:500]}
        except (ValueError, KeyError, TypeError):
            record = {"pass": None, "reason": "judge output unreadable"}
        append_jsonl(VERDICTS, {"behaviour": q["id"], "run": run["run"], **record, "cost_usd": cost})
        print(f"{q['id']:3} {run['run']:40} {record['pass']}  {record['reason'][:100]}", flush=True)


if __name__ == "__main__":
    main()
