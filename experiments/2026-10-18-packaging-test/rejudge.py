"""Judge recorded runs again, to check the judge: does it agree with itself, and with a
stronger model?

Usage: python3 rejudge.py --index INDEX --judges haiku,haiku,haiku,sonnet --review FILE

INDEX is the local file run.py --index wrote (runs and their folders). For every run it
prints the verdicts side by side, and writes FILE: one section per run with the prompt,
the expected Outcome, the agent's final answer and the verdicts, for the builder to mark.
FILE holds the agents' answers; keep it outside the repository.
"""
import argparse
import json
import os
from types import SimpleNamespace

from run import final_text, judge
from score import load_queries


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--index", required=True)
    p.add_argument("--judges", default="haiku,haiku,haiku,sonnet")
    p.add_argument("--review", required=True)
    args = p.parse_args()
    queries = {q["id"]: q for q in load_queries()}
    judges = args.judges.split(",")
    sections, flips = [], 0
    for line in open(args.index):
        entry = json.loads(line)
        query = queries[entry["query"]]
        final = final_text(open(os.path.join(entry["work"], "transcript.jsonl")).read())
        verdicts = [judge(query, final, entry["work"], SimpleNamespace(judge=j)) for j in judges]
        marks = [{True: "PASS", False: "FAIL", None: "?"}[v["pass"]] for v in verdicts]
        flips += len(set(marks)) > 1
        print(f"{entry['query']:4} {entry['variant']} " + " ".join(
            f"{j}:{m}" for j, m in zip(judges, marks)), flush=True)
        sections.append(
            f"## {entry['query']} ({entry['variant']}, {entry['model']})\n\n"
            f"**Prompt:** {query['prompt']}\n\n**Expected outcome:** {query['outcome']}\n\n"
            f"**Verdicts:** " + "; ".join(f"{j} {m}: {v['reason']}" for j, m, v in
                                          zip(judges, marks, verdicts)) +
            "\n\n**Your mark (agree / disagree, and why):** \n\n"
            f"<details><summary>Agent's final answer</summary>\n\n{final}\n\n</details>\n")
    open(args.review, "w").write("# Judge review\n\n" + "\n".join(sections))
    print(f"{flips} of {len(sections)} runs got differing verdicts; review in {args.review}")


if __name__ == "__main__":
    main()
