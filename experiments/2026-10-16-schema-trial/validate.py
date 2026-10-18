import yaml, glob, os, sys, re, warnings
warnings.filterwarnings('ignore')
from jsonschema import Draft202012Validator, RefResolver
base=sys.argv[1]; sd=os.path.join(base,'schemas')
common=yaml.safe_load(open(f'{sd}/_common.yaml'))
TYPES={'functions':'function','requirements':'requirement','proofs':'proof','parts':'part','interfaces':'interface','units':'unit','decisions':'decision','risks':'risk','externals':'external'}
errs=[];warns=[];arts={}
for f in sorted(glob.glob(f'{base}/model/**/*.yaml',recursive=True)):
    t=TYPES[os.path.basename(os.path.dirname(f))]; d=yaml.safe_load(open(f))
    sch=yaml.safe_load(open(f'{sd}/{t}.yaml'))
    v=Draft202012Validator(sch,resolver=RefResolver('',sch,store={'_common.yaml':common}))
    for e in v.iter_errors(d): errs.append(f'{os.path.basename(f)}: {e.message}')
    if os.path.basename(f)[:-5]!=d.get('id'): errs.append(f'{f}: file name is not the id')
    arts[d['id']]=(t,d,f)
ids=set(arts); refs=set()
def walk(x):
    if isinstance(x,dict): [walk(v) for k,v in x.items() if k!='id']
    elif isinstance(x,list): [walk(i) for i in x]
    elif isinstance(x,str) and re.fullmatch(r'[A-Z]{3}-[0-9A-Z]{4}',x): refs.add(x)
for t,d,f in arts.values():
    walk(d)
    if t=='requirement':
        n=d['statement'].count('{measure}')
        if ('measure' in d)!=(n==1) or n>1: errs.append(f"{d['id']}: {{measure}} placeholder rule")
        if d['pattern']=='none': warns.append(f"{d['id']}: fits no EARS pattern")
        for b in d.get('measure',{}).get('bounds',[]):
            if 'TBD' in (b['statistic'],b['value']): warns.append(f"{d['id']}: TBD in measure (spike trigger)")
    if t=='decision' and d.get('consequence')=='TBD': warns.append(f"{d['id']}: accepts a risk with no stated consequence")
    if t=='function' and '/model/product/functions/' in f and not d.get('serves'): errs.append(f"{d['id']}: product function serves no scenario")
for t,d,f in arts.values():
    if t=='part':
        child=os.path.join(os.path.dirname(os.path.dirname(f)), re.sub(' ','-',d['name'].lower()))
        if not os.path.isdir(child) and not d.get('units'): errs.append(f"{d['id']} ({d['name']}): no children in the model and no units")
unres=sorted(refs-ids)
print('ERRORS',len(errs)); [print(' ',e) for e in errs]
print('WARNINGS',len(warns)); [print(' ',w) for w in warns]
print('UNRESOLVED (not converted in this sample)',len(unres), ' '.join(unres))
