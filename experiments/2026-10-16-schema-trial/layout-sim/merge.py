import os, subprocess, random, shutil, glob, yaml, re, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # paths below are relative to layout-sim/
M = "models/medium"; W = os.path.abspath("mergework")
def sh(cwd, *a, check=True):
    return subprocess.run(a, cwd=cwd, capture_output=True, text=True, check=check)
def init(lay):
    d = f"{W}/{lay}"; shutil.rmtree(d, ignore_errors=True); shutil.copytree(f"{M}/{lay}", d)
    sh(d, "git", "init", "-q", "-b", "base"); sh(d, "git", "add", "-A")
    sh(d, "git", "-c", "user.email=s@x", "-c", "user.name=s", "commit", "-qm", "base"); return d
BLK = "product/wb-block"; OTH = "product/cm-block"
def reqs(d):  # ordered as in B file
    return [l[6:] for l in open(f"{M}/B/{BLK}/requirements.yaml").read().split("\n") if l.startswith("- id: REQ-")]
# ---- operations ----
def B_lines(d, f): return open(f"{d}/{f}").read().split("\n")
def B_write(d, f, L): open(f"{d}/{f}", "w").write("\n".join(L))
def span(L, rid):
    i = L.index(f"- id: {rid}"); j = i + 1
    while j < len(L) and not L[j].startswith("- id: "): j += 1
    return i, j
def op(d, lay, kind, rid, tag):
    fb = f"{BLK}/requirements.yaml"
    if kind == "status":
        if lay == "A":
            p = f"{d}/{BLK}/{rid}.md"; t = open(p).read(); open(p, "w").write(re.sub(r"^status: .*$", f"status: {tag}", t, 1, re.M))
        else:
            L = B_lines(d, fb); i, _ = span(L, rid); L[i + 1] = f"  status: {tag}"; B_write(d, fb, L)
    elif kind == "rationale":
        if lay == "A":
            p = f"{d}/{BLK}/{rid}.md"; L = open(p).read().split("\n"); k = L.index("## Rationale") + 2; L[k] += f" {tag}"; open(p, "w").write("\n".join(L))
        else:
            L = B_lines(d, fb); i, j = span(L, rid); k = L.index("  rationale: |", i) + 1; L[k] += f" {tag}"; B_write(d, fb, L)
    elif kind == "add":
        txt = open(f"{M}/A/{BLK}/{reqs(d)[0]}.md").read().replace(reqs(d)[0], rid) + tag
        if lay == "A": open(f"{d}/{BLK}/{rid}.md", "w").write(txt)
        else:
            L = B_lines(d, fb); i, j = span(L, reqs(d)[0]); ent = [l.replace(reqs(d)[0], rid) for l in L[i:j]]
            if L[-1] == "": L = L[:-1]
            L = L + [""] + [e for e in ent if e != ""] + [f"  # {tag}", ""]; B_write(d, fb, L)
    elif kind == "move":
        if lay == "A": sh(d, "git", "mv", f"{BLK}/{rid}.md", f"{OTH}/{rid}.md")
        else:
            L = B_lines(d, fb); i, j = span(L, rid); ent = L[i:j]; B_write(d, fb, L[:i] + L[j:])
            fo = f"{OTH}/requirements.yaml"; Lo = B_lines(d, fo)
            if Lo[-1] == "": Lo = Lo[:-1]
            B_write(d, fo, Lo + [""] + [e for e in ent if e != ""] + [""])
def check(d, lay):  # validity after clean merge
    try:
        ids = []
        if lay == "B":
            for f in glob.glob(f"{d}/**/*.yaml", recursive=True): ids += [e["id"] for e in yaml.load(open(f), Loader=yaml.CSafeLoader)]
        else:
            for f in glob.glob(f"{d}/**/*.md", recursive=True):
                fm = yaml.load(open(f).read().split("---\n", 2)[1], Loader=yaml.CSafeLoader); ids.append(fm["id"])
        return "ok" if len(ids) == len(set(ids)) else "DUPLICATE-ID"
    except Exception as e: return "PARSE-ERROR"
SCEN = {
 "status of 2 random reqs": lambda R, r: [("status", r.choice(R[:len(R)//2])), ("status", r.choice(R[len(R)//2:]))],
 "status of 2 adjacent reqs": lambda R, r: (lambda k: [("status", R[k]), ("status", R[k+1])])(r.randrange(len(R)-1)),
 "status vs rationale, same req": lambda R, r: (lambda x: [("status", x), ("rationale", x)])(r.choice(R)),
 "same field, same req": lambda R, r: (lambda x: [("status", x), ("status", x)])(r.choice(R)),
 "both add, distinct ids": lambda R, r: [("add", "REQ-WB-901"), ("add", "REQ-WB-902")],
 "both add, same next id": lambda R, r: [("add", "REQ-WB-901"), ("add", "REQ-WB-901")],
 "move vs status, same req": lambda R, r: (lambda x: [("move", x), ("status", x)])(r.choice(R)),
 "move one vs add one": lambda R, r: [("move", r.choice(R)), ("add", "REQ-WB-903")],
}
res = {}
for lay in "AB":
    d = init(lay); R = reqs(d)
    for name, gen in SCEN.items():
        r = random.Random(7); out = {"conflict": 0, "clean-ok": 0, "clean-bad": 0}
        trials = 1 if name.startswith("both add") else 10
        for t in range(trials):
            (k1, r1), (k2, r2) = gen(R, r)
            sh(d, "git", "checkout", "-q", "-f", "base"); sh(d, "git", "clean", "-qfd")
            for br, (k, rid), tag in (("b1", (k1, r1), "approved"), ("b2", (k2, r2), "retired")):
                sh(d, "git", "checkout", "-q", "-B", br, "base"); op(d, lay, k, rid, tag)
                sh(d, "git", "add", "-A"); sh(d, "git", "-c", "user.email=s@x", "-c", "user.name=s", "commit", "-qm", br)
            sh(d, "git", "checkout", "-q", "b1")
            m = sh(d, "git", "-c", "user.email=s@x", "-c", "user.name=s", "merge", "-q", "--no-edit", "b2", check=False)
            if m.returncode != 0:
                out["conflict"] += 1; sh(d, "git", "merge", "--abort", check=False)
            else:
                c = check(d, lay); out["clean-ok" if c == "ok" else "clean-bad"] += 1
                if c != "ok": out.setdefault("why", []).append(c)
        res.setdefault(name, {})[lay] = out; print(lay, name, out, flush=True)
json.dump(res, open("merge_results.json", "w"), indent=1)
