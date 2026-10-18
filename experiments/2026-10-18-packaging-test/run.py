"""Run packaging-test queries headless and record what each run loaded.

Usage:
  python3 run.py --variants S,R --models sonnet,haiku --repeats 3 [--queries P1,N8]
                 [--max-turns 20] [--max-budget 0.50] [--jobs 4] [--tmp DIR]

Rerunning the same command resumes: runs already recorded are skipped.

Each run copies a fixture into a fresh git repository, runs `claude -p` with one
variant loaded as the `datum` plugin, and appends one line to results/runs.jsonl: the
datum skills, references and agents loaded, in order, and the cost. Only datum names
are recorded, plus the names of other skills loaded; raw transcripts stay in the
temporary folder, because they hold the runner's own setup.

The agent sees every tool, so its choices are not shaped by missing ones, but only
reading, searching, writing inside the run's own folder, loading skills and starting
agents are approved; any other call is refused when made (dontAsk).

After each run a judge (Sonnet, no tools) compares the final answer and the files the run
changed with the query's Outcome, and the verdict and a one-line reason are recorded.
"""
import argparse
import collections
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time

from score import load_queries

HERE = os.path.dirname(os.path.abspath(__file__))
ALLOWED = "Skill Read Glob Grep Agent Write Edit"
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


def loads(transcript, work):
    """The ordered loads and writes in a stream-json transcript."""
    events, results = [], {}
    for line in transcript.splitlines():
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = msg.get("message") if isinstance(msg, dict) else None
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
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
            elif name in ("Write", "Edit"):
                path = os.path.relpath(arg.get("file_path", ""), work)
                kind = "write" if name == "Write" else "edit"  # only new files are checked
                events.append({"kind": kind, "name": path, "id": block.get("id")})
            elif name == "Agent":
                agent = arg.get("subagent_type", "")
                if agent.startswith("datum:"):
                    events.append({"kind": "agent", "name": agent[6:], "id": block.get("id")})
    for event in events:
        event["error"] = results.get(event.pop("id"), False)
    return events


def final_text(transcript):
    text = ""
    for line in transcript.splitlines():
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(msg, dict) and msg.get("type") == "result" and isinstance(msg.get("result"), str):
            text = msg["result"]
    return text


JUDGE = """You judge one run of an AI agent working on a systems-engineering model.
The builder said: {prompt}
The expected outcome, written before the run: {outcome}

The agent's final message:
<final>
{final}
</final>

The files the run changed (git diff; empty if none):
<diff>
{diff}
</diff>

Does the run meet the expected outcome? Judge only against the expected outcome, not
style. Answer with one JSON object and nothing else:
{{"pass": true or false, "reason": "<one sentence>"}}"""


def judge(query, final, work, args):
    git(work, "add", "-A")
    diff = subprocess.run(["git", "diff", "--cached", "--", ".", ":!transcript.jsonl"], cwd=work, capture_output=True,
                          text=True).stdout
    prompt = JUDGE.format(prompt=query["prompt"], outcome=query["outcome"],
                          final=final[:8000] or "(no final message)", diff=diff[:8000])
    proc = subprocess.run(["claude", "-p", "--model", args.judge, "--output-format", "json",
                           "--no-session-persistence", "--permission-mode", "dontAsk",
                           "--allowedTools", "", "--max-turns", "2"],
                          input=prompt, capture_output=True, text=True, timeout=300,
                          cwd=tempfile.gettempdir())  # away from the fixture's CLAUDE.md
    try:
        result = json.loads(proc.stdout)
        text = result.get("result", "")
        verdict = json.loads(text[text.index("{"):text.rindex("}") + 1])
        return {"pass": bool(verdict["pass"]), "reason": str(verdict.get("reason", ""))[:300],
                "cost_usd": result.get("total_cost_usd")}
    except (ValueError, KeyError, TypeError):
        return {"pass": None, "reason": "judge output unreadable", "cost_usd": None}


def run_one(query, variant, model, args):
    work = prepare(query["fixture"], args.tmp)
    cmd = ["claude", "-p", query["prompt"], "--plugin-dir", os.path.join(HERE, "variants", variant),
           "--model", model, "--output-format", "stream-json", "--verbose",
           "--no-session-persistence", "--max-turns", str(args.max_turns),
           "--max-budget-usd", str(args.max_budget),
           "--permission-mode", "dontAsk", "--allowedTools", ALLOWED]
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True, timeout=args.timeout)
        out, status = proc.stdout, proc.returncode
    except subprocess.TimeoutExpired as e:
        out, status = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""), "timeout"
    open(os.path.join(work, "transcript.jsonl"), "w").write(out)
    cost, turns, failure = None, None, "no result message"
    for line in out.splitlines():
        try:
            result = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(result, dict) or result.get("type") != "result":
            continue
        cost, turns = result.get("total_cost_usd"), result.get("num_turns")
        # Hitting the turn or budget cap still leaves valid loads; an API error does not.
        failure = None
        if result.get("is_error") and result.get("subtype") not in (
                "error_max_turns", "error_max_budget_usd"):
            failure = str(result.get("result") or result.get("subtype"))[:200]
    verdict = judge(query, final_text(out), work, args) if not failure else None
    return {"query": query["id"], "variant": variant, "model": model, "status": status,
            "failure": failure,
            "loads": loads(out, work), "outcome": verdict, "cost_usd": cost, "turns": turns,
            "seconds": round(time.time() - started, 1), "date": time.strftime("%Y-%m-%d"),
            "transcript": os.path.join(work, "transcript.jsonl")}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--variants", default="S,R")
    p.add_argument("--models", default="sonnet,haiku")
    p.add_argument("--repeats", type=int, default=3)
    p.add_argument("--queries", default="")
    p.add_argument("--max-turns", type=int, default=20)
    p.add_argument("--max-budget", type=float, default=0.50)
    p.add_argument("--timeout", type=int, default=600)
    p.add_argument("--tmp", default=None)
    p.add_argument("--max-failures", type=int, default=3)
    p.add_argument("--jobs", type=int, default=1)
    p.add_argument("--judge", default="sonnet")
    p.add_argument("--index", default=None, help="local file mapping runs to transcripts")
    p.add_argument("--out", default=os.path.join(HERE, "results", "runs.jsonl"))
    args = p.parse_args()
    queries = load_queries()
    if args.queries:
        wanted = args.queries.split(",")
        queries = [q for q in queries if q["id"] in wanted]
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    # Resumable: runs already in the output file count towards the repeats.
    done = collections.Counter()
    if os.path.exists(args.out):
        for line in open(args.out):
            run = json.loads(line)
            done[(run["query"], run["variant"], run["model"])] += 1
    todo = [(q, v, m) for q in queries for v in args.variants.split(",")
            for m in args.models.split(",") for _ in range(args.repeats - done[(q["id"], v, m)])]
    print(f"{len(todo)} runs to do, {args.jobs} at a time", flush=True)
    state = {"total": 0.0, "failures": 0, "stop": False}
    lock = threading.Lock()

    def one(job):
        query, variant, model = job
        if state["stop"]:
            return
        try:
            record = run_one(query, variant, model, args)
        except Exception as e:  # one broken run must not end the batch
            record = {"failure": f"runner error: {e!r}", "transcript": "-"}
        transcript = record.pop("transcript")
        with lock:
            if record["failure"]:
                # A failed run (a usage limit, an API error) is not recorded, so a rerun
                # of the same command repeats it.
                state["failures"] += 1
                print(f"{query['id']:4} {variant} {model:6} FAILED: {record['failure']}  {transcript}",
                      flush=True)
                if state["failures"] >= args.max_failures:
                    state["stop"] = True
                return
            state["failures"] = 0
            record.pop("failure")
            if args.index:  # a local map from runs to their transcripts, for rejudging
                with open(args.index, "a") as f:
                    f.write(json.dumps({"query": query["id"], "variant": variant, "model": model,
                                        "work": os.path.dirname(transcript)}) + "\n")
            with open(args.out, "a") as f:
                f.write(json.dumps(record) + "\n")
            state["total"] += record["cost_usd"] or 0
            names = " > ".join(e["name"] + ("!" if e["error"] else "") for e in record["loads"])
            verdict = {True: "PASS", False: "FAIL", None: "?"}[record["outcome"]["pass"]]
            print(f"{query['id']:4} {variant} {model:6} ${record['cost_usd'] or 0:.3f} {verdict} "
                  f"[{names or '-'}]  {transcript}", flush=True)

    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        list(pool.map(one, todo))
    if state["stop"]:
        sys.exit(f"stopped after {state['failures']} failed runs in a row; rerun the same command to resume")
    total = state["total"]
    print(f"total ${total:.2f}")


if __name__ == "__main__":
    main()
