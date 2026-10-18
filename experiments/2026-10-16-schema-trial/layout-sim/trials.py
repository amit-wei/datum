import os, sys, json, subprocess, shutil, glob, yaml, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # paths below are relative to layout-sim/
SRC = os.path.abspath("models/fat"); TW = os.path.abspath("trials")
LINKS = ("covers","parent","affects","derives_from","between","exercises","contains","allocated_to")
DESC = {
 "A": "The engineering model is stored as one Markdown file per artifact, named <ID>.md, in the folder of its block (folders = system hierarchy under product/). Fields are YAML frontmatter (id, type, status, links); prose sections are Markdown below it. Decisions are in product/decisions/. Tests in tests/ tag proofs with @pytest.mark.proof(\"PRF-...\").",
 "B": "The engineering model is stored as one YAML file per block per artifact type (requirements.yaml, interfaces.yaml, proofs.yaml, ...), in the folder of its block (folders = system hierarchy under product/). Each file is a YAML list, one entry per artifact with an id; prose is in | block scalars. Decisions are in product/decisions.yaml. Tests in tests/ tag proofs with @pytest.mark.proof(\"PRF-...\").",
}
ST = "Each definition that names an undeclared position is refused before admission."
RA = "DEC-012 declares a position one time, and a definition that names a missing position holds nothing a boundary can refuse against."
TASKS = {
 "E1-status": "Set the status of requirement REQ-VC-104 to agreed. Change nothing else.",
 "E2-add": f"Add a new requirement REQ-VC-301 to block product/vc-block with status draft, parent REQ-PL-004, derives_from FUN-VC-001, kind functional, statement: \"{ST}\" and rationale: \"{RA}\". Follow the existing format exactly. Change nothing else.",
 "E3-move": "Move requirement REQ-VC-050 from block product/vc-block to block product/ml-block. Keep its ID, fields and text unchanged. Change nothing else.",
 "E4-query": "List every artifact whose link fields (covers, parent, derives_from, affects, between, exercises, contains, allocated_to) reference FUN-SG-001. Ignore mentions in prose text. Do not modify files. End your reply with the IDs only, one per line, after a line 'ANSWER:'.",
}
def load(root, lay):
    M = {}
    if lay == "B":
        for f in glob.glob(f"{root}/product/**/*.yaml", recursive=True):
            for e in yaml.load(open(f), Loader=yaml.CSafeLoader) or []:
                e = dict(e); i = e.pop("id"); M[i] = (os.path.dirname(os.path.relpath(f, root)), {k: (" ".join(v.split()) if isinstance(v, str) else v) for k, v in e.items()})
    else:
        for f in glob.glob(f"{root}/product/**/*.md", recursive=True):
            t = open(f).read(); _, fm, body = t.split("---\n", 2); d = yaml.load(fm, Loader=yaml.CSafeLoader); i = d.pop("id")
            d["_body"] = " ".join(body.split()); d = {k: ("" if v is None else v) for k, v in d.items()}
            M[i] = (os.path.dirname(os.path.relpath(f, root)), d)
    return M
def grade(task, lay, root, base, text):
    try: M = load(root, lay)
    except Exception as e: return f"PARSE ERROR: {type(e).__name__}"
    if task == "E4-query":
        ans = set(re.findall(r"\b[A-Z]{2,3}-[A-Z]{2,3}-\d{3}\b|\bDU-\d{3}\b", text.split("ANSWER:")[-1]))
        gt = {i for i, (_, d) in M.items() if any("FUN-SG-001" in (v if isinstance(v, list) else [v]) for k, v in d.items() if k in LINKS)}
        return f"TP={len(ans&gt)} FP={len(ans-gt)} FN={len(gt-ans)}" + (" unchanged" if M == base else " MODEL CHANGED")
    diff = {i for i in set(M) | set(base) if M.get(i) != base.get(i)}
    exp = {"E1-status": {"REQ-VC-104"}, "E2-add": {"REQ-VC-301"}, "E3-move": {"REQ-VC-050"}}[task]
    if diff != exp: return f"WRONG SET CHANGED: {sorted(diff)[:5]}"
    i = next(iter(exp)); blk, d = M[i]
    if task == "E1-status": ok = d["status"] == "agreed" and {k: v for k, v in d.items() if k != "status"} == {k: v for k, v in base[i][1].items() if k != "status"}
    elif task == "E3-move": ok = blk == "product/ml-block" and d == base[i][1]
    else:
        ok = d.get("status") == "draft" and d.get("parent") == "REQ-PL-004" and d.get("derives_from") == "FUN-VC-001" and blk == "product/vc-block"
        s = d.get("statement", d.get("_body", "")); ok = ok and ST in s and RA in (d.get("rationale", "") + s)
    return "OK" if ok else f"FIELDS WRONG: {d}"
def run(task, lay, model, rep):
    d = f"{TW}/{task}-{lay}-{model}-{rep}"; shutil.rmtree(d, ignore_errors=True); shutil.copytree(f"{SRC}/{lay}", d)
    subprocess.run(["git", "init", "-q"], cwd=d); subprocess.run("git add -A && git -c user.email=s@x -c user.name=s commit -qm base", shell=True, cwd=d)
    base = load(d, lay)
    tools = "Read Glob Grep Bash(grep:*) Bash(awk:*) Bash(ls:*) Bash(wc:*)" + ("" if task == "E4-query" else " Edit Write Bash(git mv:*) Bash(mv:*)")
    p = subprocess.run(["claude", "-p", DESC[lay] + "\n\nTask: " + TASKS[task], "--model", model, "--output-format", "json",
                        "--allowedTools", tools, "--max-budget-usd", "1", "--no-session-persistence", "--strict-mcp-config"],
                       cwd=d, capture_output=True, text=True, timeout=900)
    try: j = json.loads(p.stdout)
    except Exception: j = {"result": p.stdout[-500:] + p.stderr[-500:]}
    u = j.get("usage", {})
    g = grade(task, lay, d, base, j.get("result", "") or "")
    rec = dict(task=task, lay=lay, model=model, rep=rep, grade=g, turns=j.get("num_turns"), cost=j.get("total_cost_usd"),
               in_tok=(u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)),
               out_tok=u.get("output_tokens"), secs=round((j.get("duration_ms") or 0) / 1000))
    print(json.dumps(rec), flush=True); open("trials.jsonl", "a").write(json.dumps(rec) + "\n")
if __name__ == "__main__":
    model, reps = sys.argv[1], int(sys.argv[2]); tasks = sys.argv[3].split(",") if len(sys.argv) > 3 else list(TASKS)
    for rep in range(reps):
        for t in tasks:
            for lay in "AB": run(t, lay, model, rep)
