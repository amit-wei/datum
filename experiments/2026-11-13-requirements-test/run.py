"""Run the requirements-test queries headless and record what each run did.

Usage:
  python3 run.py --models sonnet --repeats 3 [--queries R1,R2] [--variants datum,baseline]
                 [--max-turns 150] [--max-budget 5] [--jobs 2]

Rerunning the same command resumes: runs already recorded are skipped, and a run that
failed (a usage limit, an API error) is not recorded, so it is repeated. After three
failures in a row the batch stops; wait for the limit to reset and rerun.

Each run copies a fixture into its own git repository under work/ (kept, not committed)
and runs `claude -p`, with the datum plugin or, for the baseline, with no plugin and no
CLAUDE.md line. Variants come from the query's row unless --variants narrows them. One
line per run goes to results/runs.jsonl: the datum skills and agents loaded, the files
written, the validator's error count on datum runs, and the cost. Judging and the blind
evaluation are separate scripts (judge.py, evaluate.py), so each resumes on its own.

The agent sees every tool; reading, searching, writing inside the run's folder, loading
skills, starting agents and sandboxed shell commands are approved, and any other call is
refused when made (dontAsk).
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
import threading
import time
import uuid

from common import HERE, RUNS, append_jsonl, load_queries, read_jsonl

ALLOWED = ["Skill", "Read", "Glob", "Grep", "Agent", "Write", "Edit", "Bash"]
# Any shell command, inside Claude Code's sandbox (bubblewrap and socat on Linux): writes
# stay in the run's folder, plus uv's cache so the validator can run.
SANDBOX = json.dumps({"sandbox": {"enabled": True, "autoAllowBashIfSandboxed": True,
                                  "allowUnsandboxedCommands": False,
                                  "filesystem": {"allowWrite": ["~/.cache/uv"]}}})
PLUGIN = os.path.join(HERE, "plugin")
WORK = os.path.join(HERE, "work")


def git(cwd, *args):
    return subprocess.run(["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
                           *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def prepare(fixture, variant, run_id):
    """A fresh repository holding the fixture, with each closed step at its commit."""
    work = os.path.join(WORK, run_id)
    shutil.copytree(os.path.join(HERE, "fixtures", fixture), work)
    if variant == "baseline" and os.path.exists(os.path.join(work, "CLAUDE.md")):
        os.remove(os.path.join(work, "CLAUDE.md"))
    git(work, "init", "-q")
    git(work, "add", "-A")
    git(work, "commit", "-q", "--allow-empty", "-m", "fixture " + fixture)
    head = git(work, "rev-parse", "--short", "HEAD")
    for root, _, files in os.walk(work):
        if "steps.yaml" in files:
            path = os.path.join(root, "steps.yaml")
            open(path, "w").write(open(path).read().replace("0000000", head))
    git(work, "add", "-A")
    git(work, "commit", "-q", "--allow-empty", "-m", "record closed steps")
    return work, git(work, "rev-parse", "HEAD")


def loads(transcript, work):
    """The ordered datum loads, agents and file writes in a stream-json transcript."""
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
                kind = "skill" if skill.startswith("datum:") else "other-skill"
                events.append({"kind": kind, "name": skill.removeprefix("datum:"), "id": block.get("id")})
            elif name in ("Write", "Edit"):
                path = os.path.relpath(arg.get("file_path", ""), work)
                events.append({"kind": name.lower(), "name": path, "id": block.get("id")})
            elif name == "Agent":
                agent = arg.get("subagent_type", "")
                if agent.startswith("datum:"):
                    events.append({"kind": "agent", "name": agent[6:], "id": block.get("id")})
            elif name == "Bash" and "validate.py" in arg.get("command", ""):
                events.append({"kind": "validator", "name": "validate", "id": block.get("id")})
    for event in events:
        event["error"] = results.get(event.pop("id"), False)
    return events


def validator_errors(work):
    """The number of validator errors in the model, or None when there is no model."""
    if not os.path.isdir(os.path.join(work, ".datum", "model")):
        return None
    proc = subprocess.run(["uv", "run", "-q", os.path.join(PLUGIN, "scripts", "validate.py"), work],
                          capture_output=True, text=True, timeout=120)
    m = re.search(r"^ERRORS (\d+)", proc.stdout, re.M)
    return int(m.group(1)) if m else None


def run_one(query, variant, model, args):
    run_id = f"{query['id']}-{variant}-{model}-{uuid.uuid4().hex[:6]}"
    work, base = prepare(query["fixture"], variant, run_id)
    plugin = ["--plugin-dir", PLUGIN] if variant == "datum" else []
    cmd = ["claude", "-p", query["prompt"], *plugin, "--model", model, "--output-format", "stream-json",
           "--verbose", "--no-session-persistence", "--max-turns", str(args.max_turns),
           "--max-budget-usd", str(args.max_budget),
           "--permission-mode", "dontAsk", "--settings", SANDBOX, "--allowedTools", *ALLOWED]
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True, timeout=args.timeout)
        out, status = proc.stdout, proc.returncode
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        status = "timeout"
    open(os.path.join(work, "transcript.jsonl"), "w").write(out)
    cost, turns, failure, final = None, None, "no result message", ""
    for line in out.splitlines():
        try:
            result = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(result, dict) or result.get("type") != "result":
            continue
        cost, turns = result.get("total_cost_usd"), result.get("num_turns")
        final = result.get("result") if isinstance(result.get("result"), str) else ""
        # Hitting the turn or budget cap still leaves a valid run; an API error does not.
        failure = None
        if result.get("is_error") and result.get("subtype") not in (
                "error_max_turns", "error_max_budget_usd"):
            failure = str(result.get("result") or result.get("subtype"))[:200]
    if status == "timeout":
        failure = None  # the files written so far are still a result; judged as they stand
    if failure:
        shutil.rmtree(work, ignore_errors=True)
        return {"failure": failure}
    open(os.path.join(work, "final.txt"), "w").write(final)
    return {"run": run_id, "query": query["id"], "variant": variant, "model": model,
            "status": status, "base": base, "loads": loads(out, work),
            "validator_errors": validator_errors(work) if variant == "datum" else None,
            "cost_usd": cost, "turns": turns, "seconds": round(time.time() - started, 1),
            "date": time.strftime("%Y-%m-%d"), "failure": None}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--variants", default="")
    p.add_argument("--models", default="sonnet")
    p.add_argument("--repeats", type=int, default=1)
    p.add_argument("--queries", default="")
    p.add_argument("--max-turns", type=int, default=150)
    p.add_argument("--max-budget", type=float, default=5.0)
    p.add_argument("--timeout", type=int, default=2400)
    p.add_argument("--max-failures", type=int, default=3)
    p.add_argument("--jobs", type=int, default=1)
    args = p.parse_args()
    queries = load_queries()
    if args.queries:
        queries = [q for q in queries if q["id"] in args.queries.split(",")]
    narrow = set(args.variants.split(",")) if args.variants else None
    done = collections.Counter((r["query"], r["variant"], r["model"]) for r in read_jsonl(RUNS))
    queries = [q for q in queries if q["fixture"].startswith("F")]  # rows with their own runs
    todo = [(q, v, m) for q in queries for v in q["variants"] if not narrow or v in narrow
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
            record = {"failure": f"runner error: {e!r}"}
        with lock:
            if record["failure"]:
                state["failures"] += 1
                print(f"{query['id']:4} {variant:8} {model:6} FAILED: {record['failure']}", flush=True)
                if state["failures"] >= args.max_failures:
                    state["stop"] = True
                return
            state["failures"] = 0
            record.pop("failure")
            append_jsonl(RUNS, record)
            state["total"] += record["cost_usd"] or 0
            names = " > ".join(e["name"] + ("!" if e["error"] else "") for e in record["loads"]
                               if e["kind"] in ("skill", "agent", "validator"))
            print(f"{query['id']:4} {variant:8} {model:6} ${record['cost_usd'] or 0:.3f} "
                  f"{record['turns']} turns [{names or '-'}]  work/{record['run']}", flush=True)

    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        list(pool.map(one, todo))
    if state["stop"]:
        sys.exit(f"stopped after {state['failures']} failed runs in a row; rerun the same command to resume")
    print(f"total ${state['total']:.2f}")


if __name__ == "__main__":
    main()
