import random, yaml, os, json, sys
random.seed(7)
AL='0123456789ABCDEFGHJKMNPQRSTVWXYZ'
M={}
def nid(old,prefix):
    if old not in M: M[old]=prefix+'-'+''.join(random.choice(AL) for _ in range(4))
    return M[old]
P=lambda o:nid(o,{'FUN':'FUN','REQ':'REQ','TST':'PRF','DEC':'DEC','RSK':'RSK','INT':'IFC','EXT':'EXT','PRT':'PRT','UNT':'UNT'}[o.split('-')[0]])
class L(str): pass
yaml.add_representer(L, lambda d,s: d.represent_scalar('tag:yaml.org,2002:str', s, style='|'))
def fold(d):
    return {k:(L(v.strip()+'\n') if isinstance(v,str) and len(v)>70 else v) for k,v in d.items()}
out=[]
def put(path,d): out.append((path,d))
R='model/product'
# parts and externals
put(f'{R}/parts/{P("PRT-AD")}.yaml',dict(id=P('PRT-AD'),status='draft',name='Agent Definition',purpose='Holds and admits what states each agent, and gives positions to the boundaries that ask.'))
put(f'{R}/parts/{P("PRT-IN")}.yaml',dict(id=P('PRT-IN'),status='draft',name='Ingestion',purpose='Receives deliveries from external sources and turns them into items.'))
put(f'{R}/parts/{P("PRT-ST")}.yaml',dict(id=P('PRT-ST'),status='draft',name='State Custody',purpose='Holds life state with provenance and serves it.',units=[P('UNT-MAIN')]))
put(f'{R}/externals/{P("EXT-HOST")}.yaml',dict(id=P('EXT-HOST'),status='draft',name='The host',definition='The machine and the operating system on which the platform runs, and what the owner of the host runs on it for the platform.'))
put(f'model/deployment/units/{P("UNT-MAIN")}.yaml',dict(id=P('UNT-MAIN'),status='draft',name='Main process',kind='process',default=True))
# functions
put(f'{R}/functions/{P("FUN-PL-01")}.yaml',dict(id=P('FUN-PL-01'),status='draft',name='Life State Custody',definition='Holds the data that describes the life of the user. Organises it and serves it. All agents read the same data.',rationale='Agents keep their own part of the data. Their answers do not agree.',serves=[]))
put(f'{R}/agent-definition/functions/{P("FUN-AD-01")}.yaml',dict(id=P('FUN-AD-01'),status='draft',parent=P('FUN-PL-10'),name='Definition Admission',definition='Accepts what states an agent when it meets the contract, and refuses it when it does not.'))
# requirements
put(f'{R}/agent-definition/requirements/{P("REQ-AD-001")}.yaml',dict(id=P('REQ-AD-001'),status='draft',pattern='unwanted',of=P('FUN-AD-01'),parent=P('REQ-PL-016'),justified_by=P('DEC-117'),
  statement='If what states an agent does not state each part that a definition must state, then the system shall refuse it.',
  rationale='The system refuses on the parts and not on what they say, because the content of an identity stays outside the model.'))
put(f'{R}/agent-definition/requirements/{P("REQ-AD-002")}.yaml',dict(id=P('REQ-AD-002'),status='draft',pattern='unwanted',of=P('FUN-AD-01'),parent=P('REQ-PL-016'),
  statement='If what states an agent names a position that is not declared, then the system shall refuse it.'))
put(f'{R}/agent-definition/requirements/{P("REQ-AD-015")}.yaml',dict(id=P('REQ-AD-015'),status='draft',pattern='ubiquitous',of=P('FUN-AD-04'),parent=P('REQ-PL-005'),
  statement='The system shall give a position within {measure}.',
  measure=dict(metric='position_lookup_latency',definition='From a boundary asking for a position to the position received.',unit='ms',bounds=[dict(statistic='TBD',op='<=',value='TBD')]),
  rationale='Every read and every write at every boundary waits for this answer, so it is on the path of all of them. The value depends on the host and on what a boundary needs, and neither is known.'))
put(f'{R}/requirements/{P("REQ-PL-042")}.yaml',dict(id=P('REQ-PL-042'),status='draft',pattern='ubiquitous',of=P('FUN-PL-16'),justified_by=P('DEC-187'),
  statement='The platform shall give a correct answer or result of work in {measure} of cases.',
  measure=dict(metric='correct_result_rate',definition='Answers and results judged correct against a reference answer or a rubric.',unit='ratio',bounds=[dict(statistic='proportion',op='>=',value='TBD')]),
  rationale='Most of it can be judged without a person. Usefulness to the user is a separate requirement.'))
put(f'{R}/requirements/{P("REQ-PL-004")}.yaml',dict(id=P('REQ-PL-004'),status='draft',pattern='unwanted',answers=P('RSK-PL-002'),
  statement='If an external source does not deliver data as its definition states, then the platform shall report it.'))
put(f'{R}/requirements/{P("REQ-PL-013")}.yaml',dict(id=P('REQ-PL-013'),status='draft',pattern='ubiquitous',source='builder',
  statement='The platform shall not perform an action that communicates with a third party, commits funds, or gives the platform access to an external service without the authorization of the user.'))
put(f'{R}/ingestion/requirements/{P("REQ-IN-006")}.yaml',dict(id=P('REQ-IN-006'),status='draft',pattern='ubiquitous',of=P('INT-PL-01'),parent=P('REQ-PL-001'),justified_by=P('DEC-061'),
  statement='The system shall give, with each item, the source that supplied the item.',
  rationale='Only the system that received the delivery knows where the item came from; State Custody cannot find it out later.'))
put(f'{R}/state-custody/requirements/{P("REQ-ST-002")}.yaml',dict(id=P('REQ-ST-002'),status='draft',pattern='unwanted',of=P('INT-PL-01'),parent=P('REQ-PL-001'),justified_by=P('DEC-061'),
  statement='If a write of an observed item does not state its source, then the system shall refuse it.',
  rationale='The refusal is the side of the contract that cannot be gone around. A derived value has no source.'))
# interface
put(f'{R}/interfaces/{P("INT-PL-01")}.yaml',dict(id=P('INT-PL-01'),status='draft',between=[P('PRT-IN'),P('PRT-ST')],items=[dict(item='the source of an item',from_=P('PRT-IN'))]))
# proof
put(f'{R}/agent-definition/proofs/{P("TST-AD-001")}.yaml',dict(id=P('TST-AD-001'),status='draft',title='Admission of agent definitions',method='test',covers=[P('REQ-AD-001'),P('REQ-AD-002')],
  criterion=dict(pass_='Each definition in a set that omits one required part, and a definition that names an undeclared position, is refused. A complete definition that names a declared position is admitted.')))
put(f'{R}/proofs/{P("TST-PL-042")}.yaml',dict(id=P('TST-PL-042'),status='draft',title='Correctness of answers on a held-out set',method='test',covers=[P('REQ-PL-042')],
  criterion=dict(pass_='The lower bound of the correct result rate over the held-out set meets the requirement.',sample_min='TBD',confidence=0.95,bound='lower')))
# risks
put(f'{R}/risks/{P("RSK-PL-002")}.yaml',dict(id=P('RSK-PL-002'),status='draft',threatens=[P('FUN-PL-01')],statement='A source stops without a message, and the system gives a confident answer from old data.'))
put(f'{R}/risks/{P("RSK-PL-014")}.yaml',dict(id=P('RSK-PL-014'),status='draft',threatens=[P('FUN-PL-01')],statement='An agent that content steers puts life state into the address or content of a request that only reads, and a party outside the platform holds it for good.'))
# decisions
put(f'{R}/decisions/{P("DEC-059")}.yaml',dict(id=P('DEC-059'),status='agreed',date='2026-09-20',
  decision='Each declared resource has one owner: only one position admits the acts on it, and the platform refuses a position, or its conferral, that admits an act another position already admits. An agent that needs such an act asks the owner. The platform does not detect contention.',
  options=[dict(option='Detect contention at admission',against='The agent must know the instance before it acts.'),
           dict(option='Detect contention at the act',against='Needs a record of what is consumed, which has no place.'),
           dict(option='Detect contention on a schedule',against='Finds the collision after both acts occurred.'),
           dict(option='One owner per declared resource',chosen=True,for_='Removes the condition instead of finding it; reuses positions and the existing request path.')],
  reason='Ownership removes the condition instead of preventing it or finding it. The refusal of a second position makes it a property of the platform, not an arrangement of the configuration.',
  reverses_if='A declared resource is found that two positions must both admit the acts on.',
  drivers=[P('REQ-PL-006')]))
put(f'{R}/decisions/{P("DEC-199")}.yaml',dict(id=P('DEC-199'),status='agreed',date='2026-10-16',
  decision='The platform bounds what an agent that content steers can do, and does not judge whether content steers it. No requirement counts on a model or a detector to resist an instruction. External Access does not refuse a call by its address.',
  reason='Most published defences inside a model, and most detectors, fail under attacks that adapt. A test can verify the bounds whatever the model does.',
  reverses_if='A mechanism is found that keeps content from steering an agent and that a test can verify.',
  accepts=[P('RSK-PL-014')],
  consequence='TBD',
  drivers=[P('REQ-PL-005')]))
fix=lambda d:{k.rstrip('_'):(fix(v) if isinstance(v,dict) else [fix(x) if isinstance(x,dict) else x for x in v] if isinstance(v,list) else v) for k,v in d.items()}
base=sys.argv[1]
for path,d in out:
    d=fix(d); f=os.path.join(base,path); os.makedirs(os.path.dirname(f),exist_ok=True)
    def deep(x):
        if isinstance(x,dict): return fold({k:deep(v) for k,v in x.items()})
        if isinstance(x,list): return [deep(i) for i in x]
        return x
    yaml.dump(deep(d),open(f,'w'),sort_keys=False,allow_unicode=True,width=88)
json.dump(M,open(os.path.join(base,'id_map.json'),'w'),indent=1)
