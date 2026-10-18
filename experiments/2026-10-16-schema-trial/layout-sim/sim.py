"""Emulate Claude Code tool calls on layouts A and B and count calls / chars into context.
Tool models (see report): Read = cat -n (7 chars prefix/line), max 2000 lines, max 25k tokens -> error + chunking;
paths printed absolute (PREFIX chars added); tokens = chars/4."""
import os, re, glob, json, sys
PREFIX = len("/home/user/work/project/")
READ_MAX_LINES, READ_MAX_TOK, ERR = 2000, 25000, 200
CALL_OVH = 60  # tokens per tool call (call json + result wrapper), INFERRED

class Agent:
    def __init__(s, root): s.root = root; s.calls = 0; s.inc = 0; s.outc = 0; s.notes = []
    def p(s, rel): return os.path.join(s.root, rel)
    def lines(s, rel): return open(s.p(rel)).read().split("\n")
    def read(s, rel, offset=0, limit=None):
        L = s.lines(rel)
        if limit is None:
            body = sum(len(l) + 7 for l in L[:READ_MAX_LINES])
            if body / 4 > READ_MAX_TOK:   # error, then chunk
                s.calls += 1; s.inc += ERR; s.notes.append("read-limit")
                chunk = 0; i = 0
                while i < len(L):
                    # choose chunk lines to stay under limit
                    n = 0; c = 0
                    while i + n < len(L) and n < READ_MAX_LINES and (c + len(L[i+n]) + 7) / 4 < READ_MAX_TOK * 0.95:
                        c += len(L[i+n]) + 7; n += 1
                    s.calls += 1; s.inc += c; i += n
                return
            if len(L) > READ_MAX_LINES: s.notes.append("2000-line truncation")
            s.calls += 1; s.inc += body
            if len(L) > READ_MAX_LINES: s.read(rel, READ_MAX_LINES, len(L))
            return
        s.calls += 1; s.inc += sum(len(l) + 7 for l in L[offset:offset + limit])
    def glob(s, pat):
        fs = sorted(os.path.relpath(f, s.root) for f in glob.glob(s.p(pat), recursive=True))
        s.calls += 1; s.inc += sum(len(f) + PREFIX + 1 for f in fs); return fs
    def grep(s, pat, globpat, mode="content", B=0):
        rx = re.compile(pat); fs = sorted(glob.glob(s.p(globpat), recursive=True)); out = 0; hits = []
        for f in fs:
            rel = os.path.relpath(f, s.root); L = open(f).read().split("\n"); hit = False
            for i, l in enumerate(L):
                if rx.search(l):
                    hit = True; hits.append((rel, i))
                    if mode == "content":
                        for j in range(max(0, i - B), i + 1): out += len(rel) + PREFIX + len(str(j)) + 2 + len(L[j]) + 1
            if hit and mode == "files": out += len(rel) + PREFIX + 1
        s.calls += 1; s.inc += out; return hits
    def bash(s, out_chars, cmd_chars=60): s.calls += 1; s.inc += out_chars; s.outc += cmd_chars
    def edit(s, old, new): s.calls += 1; s.outc += len(old) + len(new); s.inc += 80
    def write(s, content): s.calls += 1; s.outc += len(content); s.inc += 60
    def res(s):
        return dict(calls=s.calls, in_tok=round(s.inc / 4), ctx_tok=round(s.inc / 4 + CALL_OVH * s.calls),
                    out_tok=round(s.outc / 4), notes=sorted(set(s.notes)))

def entry_span(L, eid):
    i = L.index(f"- id: {eid}"); j = i + 1
    while j < len(L) and not L[j].startswith("- id: "): j += 1
    return i, j  # j exclusive (includes trailing blank)

def setup(model):
    meta = json.load(open(f"models/{model}/meta.json"))
    A, B = f"models/{model}/A", f"models/{model}/B"
    # target block: fat block if exists else median REQ count block among level>=1
    cnt = []
    for b in meta["blocks"]:
        n = len(glob.glob(f"{A}/{b['path']}/REQ-*.md")); cnt.append((n, b))
    cnt.sort(key=lambda x: x[0])
    blk = cnt[-1][1] if model == "fat" else [b for n, b in cnt if n > 0][len([1 for n, b in cnt if n > 0]) // 2]
    other = [b for n, b in cnt if b["path"] != blk["path"] and n > 0][0]
    reqs = sorted(os.path.basename(f)[:-3] for f in glob.glob(f"{A}/{blk['path']}/REQ-*.md"))
    covered = [r for r in reqs if any(r in open(f).read() for f in glob.glob(f"{A}/{blk['path']}/PRF-*.md"))]
    rq = covered[len(covered) // 2]
    # most-referenced REQ for reverse-link task
    allreq = [os.path.basename(f)[:-3] for f in glob.glob(f"{A}/**/REQ-*.md", recursive=True)]
    txt = "\n".join(open(f).read() for f in glob.glob(f"{A}/**/*.md", recursive=True))
    hot = max(allreq[:400], key=lambda r: txt.count(r))
    return meta, A, B, blk, other, rq, hot

def run(model):
    meta, A, B, blk, other, rq, hot = setup(model)
    bp, op = blk["path"], other["path"]; R = {}
    # T1 read implementation inputs
    a = Agent(A); fs = a.glob(f"{bp}/[RIP][ER][QCF]-*.md")
    for f in fs: a.read(f)
    R["T1 read block inputs (Read/file)"] = (a.res(),)
    a2 = Agent(A); a2.bash(sum(len(open(a2.p(f)).read()) for f in fs))
    b = Agent(B)
    for t in ["requirements", "interfaces", "proofs"]:
        if os.path.exists(b.p(f"{bp}/{t}.yaml")): b.read(f"{bp}/{t}.yaml")
    R["T1 read block inputs (Read/file)"] = (a.res(), b.res())
    R["T1 read block inputs (A: one cat)"] = (a2.res(), b.res())
    # T2 edit status
    a = Agent(A); a.read(f"{bp}/{rq}.md"); st = [l for l in a.lines(f"{bp}/{rq}.md") if l.startswith("status:")][0]
    a.edit(st, "status: agreed")
    b = Agent(B); fb = f"{bp}/requirements.yaml"; L = b.lines(fb)
    b.grep(f"^- id: {rq}$", fb); i, j = entry_span(L, rq); b.read(fb, i, 15)
    b.edit(L[i] + "\n" + L[i + 1], L[i] + "\n  status: agreed")
    R["T2 edit one status"] = (a.res(), b.res())
    # T3 add 5 requirements
    newreq = open(f"{A}/{bp}/{rq}.md").read()
    a = Agent(A); a.glob(f"{bp}/REQ-*.md")
    for k in range(5): a.write(newreq)
    b = Agent(B); b.grep(r"^- id: REQ-", fb); b.read(fb, len(L) - 15, 15)
    ent = "\n".join(L[i:j]); b.edit("\n".join(L[-4:]), "\n".join(L[-4:]) + ("\n" + ent) * 5)
    R["T3 add 5 requirements"] = (a.res(), b.res())
    # T4 reverse links of hot REQ
    a = Agent(A); hits = a.grep(re.escape(hot) + r"\b", "**/*.md")
    b = Agent(B); hits_b = b.grep(re.escape(hot) + r"\b", "**/*.yaml")
    for f, ln in hits_b: b.read(f, max(0, ln - 25), 26)  # find owning '- id:' above the hit
    R[f"T4 reverse links ({len(hits)} hits, grep)"] = (a.res(), b.res())
    b2 = Agent(B); b2.grep(re.escape(hot) + r"\b", "**/*.yaml", B=25)
    R[f"T4 reverse links (B: grep -B25)"] = (a.res(), b2.res())
    b3 = Agent(B); b3.bash(sum(len(f) + PREFIX + 14 for f, _ in hits_b), 140)
    R[f"T4 reverse links (B: awk one-liner)"] = (a.res(), b3.res())
    # T5 trace REQ -> proofs -> tests
    a = Agent(A); ph = a.grep(re.escape(rq) + r"\b", "**/PRF-*.md", mode="files")
    prfs = sorted({os.path.basename(f)[:-3] for f, _ in ph}) or ["PRF-NONE"]
    for f in sorted({f for f, _ in ph}): a.read(f)
    a.grep(r'proof\("(' + "|".join(prfs) + r')"\)', "tests/*.py")
    b = Agent(B); bh = b.grep(re.escape(rq) + r"\b", "**/proofs.yaml", B=4)
    for f, ln in bh:
        Lp = b.lines(f); k = ln
        while not Lp[k].startswith("- id: "): k -= 1
        _, e = entry_span(Lp, Lp[k][6:]); b.read(f, k, e - k)
    b.grep(r'proof\("(' + "|".join(prfs) + r')"\)', "tests/*.py")
    R["T5 trace REQ->proof->test"] = (a.res(), b.res())
    # T6 review level 1: allocated + covered (grep strategy)
    a = Agent(A); a.grep(r"^derives_from:", "product/*/REQ-*.md"); a.grep(r"^covers:", "product/*/PRF-*.md")
    b = Agent(B); b.grep(r"^- id: REQ-|^  derives_from:", "product/*/requirements.yaml"); b.grep(r"^  covers:", "product/*/proofs.yaml")
    R["T6 review level-1 (grep)"] = (a.res(), b.res())
    a = Agent(A); n = 0
    for f in glob.glob(f"{A}/product/*/REQ-*.md") + glob.glob(f"{A}/product/*/PRF-*.md"): n += len(open(f).read())
    a.bash(n)
    b = Agent(B)
    for f in sorted(glob.glob(f"{B}/product/*/requirements.yaml") + glob.glob(f"{B}/product/*/proofs.yaml")):
        b.read(os.path.relpath(f, B))
    R["T6 review level-1 (read all; A cat)"] = (a.res(), b.res())
    # T7 move requirement to other block
    a = Agent(A); a.bash(0, 80); a.read(f"{bp}/{rq}.md"); a.edit("parent: REQ-PL-001", "parent: REQ-PL-002")
    b = Agent(B); b.grep(f"^- id: {rq}$", fb); b.read(fb, i, j - i); b.edit(ent, "")
    ob = f"{op}/requirements.yaml"; Lo = b.lines(ob); b.read(ob, len(Lo) - 15, 15)
    b.edit("\n".join(Lo[-4:]), "\n".join(Lo[-4:]) + "\n" + ent)
    R["T7 move requirement"] = (a.res(), b.res())
    # T8 supersede a decision
    decs = sorted(glob.glob(f"{A}/product/decisions/DEC-*.md")); d0 = decs[len(decs) // 2]; did = os.path.basename(d0)[:-3]
    dtxt = open(d0).read()
    a = Agent(A); a.bash(20); a.read(os.path.relpath(d0, A))
    a.edit("status: agreed\ndate: 2026-01-01\nsuperseded_by:", "status: superseded\ndate: 2026-01-01\nsuperseded_by: DEC-999")
    a.write(dtxt)
    b = Agent(B); fd = "product/decisions.yaml"; Ld = b.lines(fd)
    b.grep(f"^- id: {did}$", fd); di, dj = entry_span(Ld, did); b.read(fd, di, dj - di)
    b.edit("\n".join(Ld[di:di + 4]), "\n".join(Ld[di:di + 4]).replace("agreed", "superseded"))
    b.bash(20); b.read(fd, len(Ld) - 15, 15); b.edit("\n".join(Ld[-4:]), "\n".join(Ld[-4:]) + "\n" + "\n".join(Ld[di:dj]))
    R["T8 supersede decision"] = (a.res(), b.res())
    return R, dict(block=bp, req=rq, hot=hot)

def filestats(model):
    out = {}
    for lay in "AB":
        fs = [f for f in glob.glob(f"models/{model}/{lay}/product/**/*", recursive=True) if os.path.isfile(f)]
        sz = [os.path.getsize(f) for f in fs]
        ln = [open(f).read().count("\n") for f in fs]
        over = sum(1 for f, s, l in zip(fs, sz, ln) if (s + 7 * l) / 4 > READ_MAX_TOK or l > READ_MAX_LINES)
        out[lay] = dict(files=len(fs), total_kb=round(sum(sz) / 1024), max_kb=round(max(sz) / 1024, 1), max_lines=max(ln), over_read_limit=over)
    return out

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    allr = {}
    for m in ["small", "medium", "large", "wide", "deep", "fat"]:
        R, info = run(m); allr[m] = dict(tasks={k: v for k, v in R.items()}, info=info, files=filestats(m))
        print(f"\n## {m} {info} files={allr[m]['files']}")
        for k, (ra, rb) in R.items():
            print(f"{k:42s} A calls={ra['calls']:3d} ctx={ra['ctx_tok']:7d} out={ra['out_tok']:5d} {ra['notes']} | "
                  f"B calls={rb['calls']:3d} ctx={rb['ctx_tok']:7d} out={rb['out_tok']:5d} {rb['notes']}")
    json.dump(allr, open("results.json", "w"), indent=1, default=str)
