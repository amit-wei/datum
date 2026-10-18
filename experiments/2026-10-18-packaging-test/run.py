"""Run packaging-test queries headless and record what each run loaded.

Usage:
  python3 run.py --variants S,R,H --models sonnet,haiku --repeats 3 [--queries P1,N8]
                 [--max-turns 8] [--max-budget 0.50] [--tmp DIR]

Each run copies a fixture into a fresh git repository, runs `claude -p` with one
variant loaded as the `datum` plugin, and appends one line to results/runs.jsonl: the
datum skills, references and agents loaded, in order, and the cost. Only datum names
are recorded, plus the names of other skills loaded; raw transcripts stay in the
temporary folder, because they hold the runner's own setup.

The agent may read and search, load skills and start agents, but not write, run shell
commands or use the web: the test measures what loads, not the work done.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import time

from score import load_queries

HERE = os.path.dirname(os.path.abspath(__file__))
ALLOWED = "Skill Read Glob Grep Agent"
DENIED = "Write Edit Bash WebSearch WebFetch NotebookEdit"
REFERENCE = re.compile(r"/skills/([a-z0-9-]+)/references/([a-z0-9-]+)\.md$")


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
                    *args], cwd=cwd, check=True, capture_output=True)


def prepare(fixture, tmp):
    """A fresh repository holding the fixture, with each closed step at its commit."""
    work = tempfile.mkdtemp(prefix=fixture + "-", dir=tmp)
    src = os.path.join(HERE, "fixtures", fixture)
    shutil.copytree(src, work, dirs_exist_ok=True)
    git(work, "init", "-q")
    git(work, "add", "-A")
    git(work, "commit", "-q", "--allow-empty", "-m", "fixture " + fixture)
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=work,
                          capture_output=True, text=True).stdout.strip()
    for root, _, files in os.walk(work):
        if "steps.yaml" in files:
            path = os.path.join(root, "steps.yaml")
            text = open(path).read().replace("closed_at: HEAD", "closed_at: " + head)
            open(path, "w").write(text)
    git(work, "add", "-A")
    git(work, "commit", "-q", "--allow-empty", "-m", "record closed steps")
    return work


def loads(transcript):
    """The ordered loads in a stream-json transcript."""
    events, results = [], {}
    for line in transcript.splitlines():
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        content = (msg.get("message") or {}).get("content") or []
        if not isinstance(content, list):
            continue
        for block in content:
            if block.get("type") == "tool_result":
                results[block.get("tool_use_id")] = bool(block.get("is_error"))
            if block.get("type") != "tool_use":
                continue
            name, arg = block.get("name"), block.get("input") or {}
            if name == "Skill":
                skill = arg.get("skill") or arg.get("command") or ""
                if skill.startswith("datum:"):
                    events.append({"kind": "skill", "name": skill[6:], "id": block.get("id")})
                else:
                    events.append({"kind": "other-skill", "name": skill, "id": block.get("id")})
            elif name == "Read":
                m = REFERENCE.search(arg.get("file_path", ""))
                if m:
                    events.append({"kind": "reference", "name": m.group(2), "step": m.group(1),
                                   "id": block.get("id")})
            elif name == "Agent":
                agent = arg.get("subagent_type", "")
                if agent.startswith("datum:"):
                    events.append({"kind": "agent", "name": agent[6:], "id": block.get("id")})
    for event in events:
        event["error"] = results.get(event.pop("id"), False)
    return events


def run_one(query, variant, model, args):
    work = prepare(query["fixture"], args.tmp)
    cmd = ["claude", "-p", query["prompt"], "--plugin-dir", os.path.join(HERE, "variants", variant),
           "--model", model, "--output-format", "stream-json", "--verbose",
           "--no-session-persistence", "--max-turns", str(args.max_turns),
           "--max-budget-usd", str(args.max_budget),
           "--allowedTools", ALLOWED, "--disallowedTools", DENIED]
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True, timeout=args.timeout)
        out, status = proc.stdout, proc.returncode
    except subprocess.TimeoutExpired as e:
        out, status = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""), "timeout"
    open(os.path.join(work, "transcript.jsonl"), "w").write(out)
    cost, turns = None, None
    for line in out.splitlines():
        if '"type":"result"' in line.replace(" ", ""):
            try:
                result = json.loads(line)
                cost, turns = result.get("total_cost_usd"), result.get("num_turns")
            except json.JSONDecodeError:
                pass
    return {"query": query["id"], "variant": variant, "model": model, "status": status,
            "loads": loads(out), "cost_usd": cost, "turns": turns,
            "seconds": round(time.time() - started, 1), "date": time.strftime("%Y-%m-%d"),
            "transcript": os.path.join(work, "transcript.jsonl")}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--variants", default="S,R,H")
    p.add_argument("--models", default="sonnet,haiku")
    p.add_argument("--repeats", type=int, default=3)
    p.add_argument("--queries", default="")
    p.add_argument("--max-turns", type=int, default=8)
    p.add_argument("--max-budget", type=float, default=0.50)
    p.add_argument("--timeout", type=int, default=600)
    p.add_argument("--tmp", default=None)
    p.add_argument("--out", default=os.path.join(HERE, "results", "runs.jsonl"))
    args = p.parse_args()
    queries = load_queries()
    if args.queries:
        wanted = args.queries.split(",")
        queries = [q for q in queries if q["id"] in wanted]
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    total = 0.0
    for query in queries:
        for variant in args.variants.split(","):
            for model in args.models.split(","):
                for _ in range(args.repeats):
                    record = run_one(query, variant, model, args)
                    transcript = record.pop("transcript")
                    with open(args.out, "a") as f:
                        f.write(json.dumps(record) + "\n")
                    total += record["cost_usd"] or 0
                    names = " > ".join(e["name"] + ("!" if e["error"] else "") for e in record["loads"])
                    print(f"{query['id']:4} {variant} {model:6} ${record['cost_usd'] or 0:.3f} "
                          f"[{names or '-'}]  {transcript}", flush=True)
    print(f"total ${total:.2f}")


if __name__ == "__main__":
    main()
