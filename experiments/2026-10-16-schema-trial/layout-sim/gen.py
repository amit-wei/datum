"""Generate synthetic engineering models in layout A (md per artifact) and B (yaml per block per type).
Usage: python3 gen.py OUTDIR CONFIG   (configs below)"""
import os, sys, random, textwrap, json, shutil

WORDS = ("the system shall refuse admit declare position agent resource boundary definition part "
         "record owner act state lookup instance schedule conferral contention detection platform "
         "identity content model condition collision consumed admission request reply message queue "
         "timeout retry limit budget token store version channel event handler schema field value "
         "when each one not that which before after only any is are a an of on in to by for").split()
PREF = {"REQ": "requirements", "FUN": "functions", "PRT": "parts", "IFC": "interfaces", "PRF": "proofs",
        "DEC": "decisions", "RSK": "risks", "SCN": "scenarios", "DU": "deployment-units"}
BASE = dict(REQ=678, DEC=235, IFC=181, RSK=156, PRF=120, FUN=80, PRT=40, SCN=20, DU=5)  # ~1515

CONFIGS = {
    # name: (total, branching per level, seed, fat)
    "small": (100, [2], 1, False),
    "medium": (1515, [11, 2], 2, False),
    "large": (10000, [12, 4, 3], 3, False),
    "wide": (1515, [60], 4, False),
    "deep": (1515, [2, 2, 2, 2, 2], 5, False),
    "fat": (1515, [11, 2], 6, True),
}

def prose(r, lo, hi, ids):
    n = r.randint(lo, hi); out = []
    while len(" ".join(out)) < n:
        if r.random() < 0.06 and ids:
            out.append(r.choice(ids) + ".")
        else:
            out.append(r.choice(WORDS))
    s = " ".join(out)
    return s[0].upper() + s[1:] + "."

def wrap(s, width, indent=""):
    return "\n".join(textwrap.wrap(s, width, initial_indent=indent, subsequent_indent=indent))

def build(cfg):
    total, branching, seed, fat = CONFIGS[cfg]
    r = random.Random(seed)
    # block tree
    blocks = [dict(path="product", code="PL", parent=None, level=0)]
    frontier = [blocks[0]]; codes = {"PL"}
    for lvl, b in enumerate(branching, 1):
        nxt = []
        for p in frontier:
            for i in range(b):
                while True:
                    code = "".join(r.choice("ABCDEFGHJKLMNPRSTUVWXYZ") for _ in range(2 if len(codes) < 300 else 3))
                    if code not in codes: break
                codes.add(code)
                name = f"{code.lower()}-block"
                blk = dict(path=f"{p['path']}/{name}", code=code, parent=p, level=lvl)
                blocks.append(blk); nxt.append(blk)
        frontier = nxt
    scale = total / sum(BASE.values())
    counts = {t: max(1, round(c * scale)) for t, c in BASE.items()}
    w = {id(b): r.uniform(0.3, 1.7) for b in blocks}
    arts = []  # dicts with type,id,block,fields,prose
    byblock = {id(b): {t: [] for t in PREF} for b in blocks}
    seq = {}
    def new_id(t, b):
        if t in ("DEC", "DU"):
            seq[t] = seq.get(t, 0) + 1; return f"{t}-{seq[t]:03d}"
        k = (t, b["code"]); seq[k] = seq.get(k, 0) + 1
        return f"{t}-{b['code']}-{seq[k]:03d}"
    def pick_block(t):
        if t == "DU": return blocks[0]
        if t == "DEC":
            if total <= 2000 or r.random() < 0.3: return blocks[0]
            cand = [b for b in blocks if b["level"] == 1]; return r.choice(cand)
        return r.choices(blocks, weights=[w[id(b)] for b in blocks])[0]
    order = ["PRT", "FUN", "REQ", "IFC", "PRF", "RSK", "SCN", "DU", "DEC"]
    fatb = blocks[1] if fat else None
    for t in order:
        n = counts[t]
        if fat and t == "REQ":
            for _ in range(200):
                a = dict(type=t, id=new_id(t, fatb), block=fatb); arts.append(a); byblock[id(fatb)][t].append(a)
            n -= 200
        for _ in range(n):
            b = pick_block(t)
            a = dict(type=t, id=new_id(t, b), block=b); arts.append(a); byblock[id(b)][t].append(a)
    allids = [a["id"] for a in arts]
    decs = [a["id"] for a in arts if a["type"] == "DEC"]
    def pool(b, t, up=True):
        x = byblock[id(b)][t]
        if not x and up and b["parent"]: return pool(b["parent"], t)
        return x
    for a in arts:
        b = a["block"]; t = a["type"]; f = {"status": r.choice(["draft"] * 6 + ["agreed"] * 3 + ["verified"])}
        refs = r.sample(decs, min(3, len(decs))) + r.sample(allids, 3)
        if t == "REQ":
            if b["parent"]:
                pr = pool(b["parent"], "REQ"); f["parent"] = r.choice(pr)["id"] if pr else None
            fu = pool(b, "FUN"); f["derives_from"] = r.choice(fu)["id"] if fu and r.random() < 0.92 else None
            f["kind"] = r.choice(["functional"] * 4 + ["performance", "constraint"])
            a["prose"] = [("statement", prose(r, 90, 230, [])), ("rationale", prose(r, 150, 430, refs))]
        elif t == "FUN":
            pt = pool(b, "PRT"); f["allocated_to"] = r.choice(pt)["id"] if pt and r.random() < 0.9 else None
            a["prose"] = [("statement", prose(r, 80, 200, []))]
        elif t == "PRT":
            a["prose"] = [("description", prose(r, 80, 220, []))]
        elif t == "IFC":
            pt = pool(b, "PRT") or [x for x in arts if x["type"] == "PRT"]
            f["between"] = [x["id"] for x in r.sample(pt, min(2, len(pt)))]
            a["prose"] = [("statement", prose(r, 150, 400, refs[:2]))]
        elif t == "PRF":
            f["method"] = r.choice(["test"] * 4 + ["inspection", "analysis"])
            a["prose"] = [("title", prose(r, 20, 50, [])), ("criterion", prose(r, 150, 350, []))]
        elif t == "RSK":
            cand = pool(b, "REQ") + pool(b, "PRT")
            f["affects"] = [x["id"] for x in r.sample(cand, min(2, len(cand)))]
            f["likelihood"] = r.choice(["low", "medium", "high"])
            a["prose"] = [("description", prose(r, 200, 480, refs[:2])), ("mitigation", prose(r, 100, 300, []))]
        elif t == "SCN":
            fu = pool(b, "FUN") or [x for x in arts if x["type"] == "FUN"]
            f["exercises"] = [x["id"] for x in r.sample(fu, min(3, len(fu)))]
            a["prose"] = [("steps", prose(r, 300, 800, refs))]
        elif t == "DU":
            pt = [x for x in arts if x["type"] == "PRT"]
            f["contains"] = [x["id"] for x in r.sample(pt, min(4, len(pt)))]
            a["prose"] = [("description", prose(r, 100, 300, []))]
        elif t == "DEC":
            f["date"] = f"2026-0{r.randint(1,9)}-{r.randint(10,28)}"; f["superseded_by"] = None
            f["status"] = "agreed"
            a["prose"] = [("decision", prose(r, 400, 1200, refs[:3])), ("reason", prose(r, 500, 2500, refs)),
                          ("reverses_if", prose(r, 80, 200, []))]
        a["fields"] = f
    # proofs cover reqs of their block: assign coverage so ~85% reqs covered
    for b in blocks:
        reqs = byblock[id(b)]["REQ"]; prfs = byblock[id(b)]["PRF"]
        if not prfs:
            continue
        for p in prfs: p["fields"]["covers"] = []
        for q in reqs:
            if r.random() < 0.85: r.choice(prfs)["fields"]["covers"].append(q["id"])
        for p in prfs:
            if not p["fields"]["covers"] and reqs: p["fields"]["covers"] = [r.choice(reqs)["id"]]
            # reorder: covers right after method
    return blocks, arts, byblock

def fmt_val(v):
    if v is None: return "null"
    if isinstance(v, list): return "[" + ", ".join(v) + "]"
    return str(v)

def write_A(root, blocks, arts):
    for a in arts:
        d = os.path.join(root, a["block"]["path"]) + ("/decisions" if a["type"] == "DEC" else "")
        os.makedirs(d, exist_ok=True)
        fm = [f"id: {a['id']}", f"type: {PREF[a['type']][:-1] if a['type']!='DU' else 'deployment-unit'}"]
        fm += [f"{k}: {fmt_val(v) if v is not None else ''}".rstrip() for k, v in a["fields"].items()]
        body = []
        for i, (k, txt) in enumerate(a["prose"]):
            if i == 0: body.append(wrap(txt, 88))
            else: body.append(f"## {k.replace('_',' ').capitalize()}\n\n" + wrap(txt, 88))
        open(os.path.join(d, a["id"] + ".md"), "w").write("---\n" + "\n".join(fm) + "\n---\n" + "\n\n".join(body) + "\n")

def write_B(root, blocks, byblock):
    for b in blocks:
        for t, lst in byblock[id(b)].items():
            if not lst: continue
            d = os.path.join(root, b["path"]); os.makedirs(d, exist_ok=True)
            ents = []
            for a in lst:
                L = [f"- id: {a['id']}"] + [f"  {k}: {fmt_val(v)}" for k, v in a["fields"].items()]
                for k, txt in a["prose"]:
                    L.append(f"  {k}: |"); L.append(wrap(txt, 84, "    "))
                ents.append("\n".join(L))
            open(os.path.join(d, PREF[t] + ".yaml"), "w").write("\n\n".join(ents) + "\n")

def write_tests(root, blocks, arts):
    r = random.Random(99)
    byb = {}
    for a in arts:
        if a["type"] == "PRF" and a["fields"]["method"] == "test":
            byb.setdefault(a["block"]["code"], []).append(a)
    os.makedirs(os.path.join(root, "tests"), exist_ok=True)
    for code, prfs in byb.items():
        L = ["import pytest", ""]
        for p in prfs:
            for k in range(r.randint(1, 3)):
                L += [f'@pytest.mark.proof("{p["id"]}")', f"def test_{p['id'].lower().replace('-','_')}_{k}():",
                      "    assert admit(make_definition()) is not None", ""]
        open(os.path.join(root, "tests", f"test_{code.lower()}.py"), "w").write("\n".join(L))

if __name__ == "__main__":
    out, cfg = sys.argv[1], sys.argv[2]
    blocks, arts, byblock = build(cfg)
    for lay in "AB":
        root = os.path.join(out, cfg, lay); shutil.rmtree(root, ignore_errors=True); os.makedirs(root)
        (write_A(root, blocks, arts) if lay == "A" else write_B(root, blocks, byblock))
        write_tests(root, blocks, arts)
    meta = dict(blocks=[dict(path=b["path"], code=b["code"], level=b["level"]) for b in blocks],
                counts={t: sum(1 for a in arts if a["type"] == t) for t in PREF}, total=len(arts))
    json.dump(meta, open(os.path.join(out, cfg, "meta.json"), "w"), indent=1)
    print(cfg, meta["total"], len(blocks), "blocks", meta["counts"])
