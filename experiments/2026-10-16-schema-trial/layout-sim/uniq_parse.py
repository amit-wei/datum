import glob, os, time, yaml, collections, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # paths below are relative to layout-sim/
L = yaml.CSafeLoader
def parse_A(root):
    n=0
    for f in glob.glob(f"{root}/**/*.md", recursive=True):
        t=open(f).read(); fm=t.split("---\n",2)[1]; yaml.load(fm, Loader=L); n+=1
    return n
def parse_B(root):
    n=0
    for f in glob.glob(f"{root}/**/*.yaml", recursive=True):
        n+=len(yaml.load(open(f), Loader=L))
    return n
for m in ["small","medium","large","fat"]:
    for lay,fn in (("A",parse_A),("B",parse_B)):
        ts=[]
        for _ in range(3):
            t=time.perf_counter(); n=fn(f"models/{m}/{lay}"); ts.append(time.perf_counter()-t)
        print(f"parse {m} {lay}: {n} artifacts, best {min(ts)*1000:.0f} ms")
# uniqueness of field lines in B (non-id, non-prose)
for m in ["medium","fat"]:
    tot=nonu=0; st=0; stn=0
    for f in glob.glob(f"models/{m}/B/**/*.yaml", recursive=True):
        lines=open(f).read().split("\n"); c=collections.Counter(lines)
        for l in lines:
            if l.startswith("  ") and not l.startswith("    ") and not l.endswith("|"):
                tot+=1; nonu+= c[l]>1
                if l.startswith("  status:"): st+=1; stn+=c[l]>1
    print(f"{m} B: field lines non-unique within file: {nonu}/{tot} = {nonu/tot:.0%}; status lines non-unique {stn}/{st} = {stn/st:.0%}")
