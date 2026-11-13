"""Shared helpers: the queries, the result files, and one-shot Claude calls that stop
cleanly when the usage limit is hit, so every script can be rerun to resume."""
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
RUNS = os.path.join(RESULTS, "runs.jsonl")
VERDICTS = os.path.join(RESULTS, "verdicts.jsonl")
EVALUATIONS = os.path.join(RESULTS, "evaluations.jsonl")
NAME = re.compile(r"`([a-z0-9-]+)`")
# Run folders live outside any repository: inside this one, an agent loads the repo's
# CLAUDE.md and AGENTS.md and can read this test's queries (found in the pilot).
WORK = os.environ.get("DATUM_TEST_WORK") or os.path.expanduser(
    "~/.cache/datum-experiments/2026-11-13-requirements-test")


def load_queries():
    """The behaviours in queries.md, one table row each."""
    queries, header = [], None
    for line in open(os.path.join(HERE, "queries.md")):
        if not line.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] == "#":
            header = cells
            continue
        if header is None or not re.fullmatch(r"R\d+[a-z]?", cells[0]):
            continue
        row = dict(zip(header, cells))
        queries.append({
            "id": row["#"], "fixture": row["Fixture"], "variants": row["Variants"].split(", "),
            "prompt": row["Prompt"], "expected": NAME.findall(row["Expected"]),
            "outcome": row["Outcome"],
        })
    return queries


def read_jsonl(path):
    if not os.path.exists(path):
        return []
    return [json.loads(line) for line in open(path) if line.strip()]


def append_jsonl(path, record):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")


class OutOfUsage(Exception):
    """A Claude call failed for a reason a later rerun can fix (usage limit, API error)."""


def ask(prompt, model="sonnet", timeout=600):
    """One tool-less Claude call, away from any project's CLAUDE.md. Returns (text, cost).
    Raises OutOfUsage when the call did not produce an answer."""
    proc = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json",
                           "--no-session-persistence", "--permission-mode", "dontAsk",
                           "--allowedTools", "", "--max-turns", "2"],
                          input=prompt, capture_output=True, text=True, timeout=timeout,
                          cwd=tempfile.gettempdir())
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise OutOfUsage((proc.stdout or proc.stderr or "no output").strip()[:300])
    if result.get("is_error") or not isinstance(result.get("result"), str):
        raise OutOfUsage(str(result.get("result") or result.get("subtype"))[:300])
    return result["result"], result.get("total_cost_usd")


def last_json(text):
    """The {...} object in a model's answer."""
    return json.loads(text[text.index("{"):text.rindex("}") + 1])


def stop(message):
    sys.exit(f"stopped: {message}\nRerun the same command to resume.")


def changed_files(work, base):
    """The text of every file the run added or changed since the fixture, as a diff."""
    subprocess.run(["git", "add", "-A"], cwd=work, capture_output=True)
    return subprocess.run(["git", "diff", "--cached", base, "--", ".", ":!transcript.jsonl"],
                          cwd=work, capture_output=True, text=True).stdout
