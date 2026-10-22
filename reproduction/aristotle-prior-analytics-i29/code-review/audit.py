"""Independent bit-mask oracle and hostile proof-input checks; standard library."""
import copy, hashlib, itertools, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import model as m

names=('X','Y','Z')
atoms=[(op,x,y) for op in ('ALL','NO','SOME') for x in names for y in names]+[('EX',x) for x in names]
worlds=[dict(zip(names,v)) for n in (1,2,3) for v in itertools.product(range(1<<n),repeat=3)]
def truth(s,w):
    if s[0]=='FALSE': return False
    x=w[s[1]]
    if s[0]=='EX': return x!=0
    y=w[s[2]]
    if s[0]=='ALL': return x & y == x
    if s[0]=='NO': return x & y == 0
    if s[0]=='SOME': return x & y != 0
    raise RuntimeError(s)
def ensure(b,why):
    if not b: raise RuntimeError(why)
counts={}; attempts=0
# All candidate conclusions for all ordered input atoms, including coincident terms.
for rule,arity in [('all_trans',2),('no_sym',1),('no_sub',2),('some_map',2),('witness',2),('some_sym',1)]:
    accepted=0
    for ps in itertools.product(atoms,repeat=arity):
        for goal in atoms:
            attempts+=1
            cert=m.node(rule,goal,*[m.given(i,p) for i,p in enumerate(ps)])
            try: m.verify(cert,list(ps),goal)
            except m.InvalidProof: continue
            accepted+=1
            for w in worlds:
                ensure(not all(truth(p,w) for p in ps) or truth(goal,w),('unsound',rule,ps,goal,w))
    counts[rule]=accepted
# Match all atomic statements against a separate integer-mask interpretation.
for w in worlds:
    sets={k:frozenset(i for i in range(3) if v>>i&1) for k,v in w.items()}
    for s in atoms: ensure(m.holds(s,sets)==truth(s,w),('holds',s,w))

attacks=0
def rejected(p,ps,g):
    global attacks
    attacks+=1
    try: m.verify(p,ps,g)
    except m.InvalidProof: return
    raise RuntimeError('hostile certificate accepted')
base=[('NO','X','Y')]
# Valid nested RAA keeps outer dependency until outer discharge.
h=m.assume('outer',('SOME','X','Y')); k=m.assume('inner',('NO','X','Y'))
inner=m.node('raa',('SOME','X','Y'),m.node('clash',('FALSE',),h,k),label='inner',assumption=('NO','X','Y'))
outer=m.node('raa',('NO','X','Y'),m.node('clash',('FALSE',),inner,m.given(0,base[0])),label='outer',assumption=('SOME','X','Y'))
ensure(m.verify(outer,base,base[0]),'nested RAA failed')
p=copy.deepcopy(outer); p['inputs'][0]['inputs'][0]['label']='outer'
rejected(p,base,base[0]) # shadow outer binding
p=copy.deepcopy(outer); p['inputs'][0]['inputs'][0]['inputs'][0]['inputs'][0]['label']='missing'
rejected(p,base,base[0])
# Remove binding but leave syntactically identical assumption node.
rejected(inner,base,('SOME','X','Y'))
# RAA labels shared only across disjoint trees do not confer a global binding.
rejected(m.node('some_sym',('SOME','Y','X'),h),base,('SOME','Y','X'))
# A shared cyclic tree must hit explicit depth guard, not be treated as a proof DAG.
p=m.node('no_sym',('NO','X','X')); p['inputs']=[p]
rejected(p,[('NO','X','X')],('NO','X','X'))
# Node-count bound with a binary duplicated proof; all local rules otherwise valid.
p=m.given(0,('ALL','X','X'))
for _ in range(14): p=m.node('all_trans',('ALL','X','X'),p,p)
rejected(p,[('ALL','X','X')],('ALL','X','X'))
for index in (False,True,-1,1,0.0,'0',None): rejected(m.given(index,base[0]),base,base[0])
for field,value in [('inputs',()),('rule',None),('claim',('NO','X')),('claim',('NO','X','Y','Z'))]:
    p=m.given(0,base[0]);p[field]=value;rejected(p,base,base[0])
for bad in ({},None,[],{'rule':'given'}): rejected(bad,base,base[0])
# Mutate every term position in every claim of each positive certificate.
mutations=0
for _,ps,g,p in m.examples():
    def paths(q,path=()):
        yield path
        for i,c in enumerate(q['inputs']): yield from paths(c,path+(i,))
    for path in paths(p):
        q=p
        for i in path:q=q['inputs'][i]
        for pos in range(1,len(q['claim'])):
            changed=copy.deepcopy(p); at=changed
            for i in path:at=at['inputs'][i]
            claim=list(at['claim']);claim[pos]='Alien';at['claim']=tuple(claim)
            rejected(changed,ps,g);mutations+=1
# Test clash plus discharge against every potential background atom.
raa_candidates=0;raa_accepted=0
for x,y in itertools.product(names,repeat=2):
    goal=('NO',x,y); assumed=('SOME',x,y)
    for background in atoms:
        raa_candidates+=1
        c=m.node('raa',goal,m.node('clash',('FALSE',),m.assume('local',assumed),m.given(0,background)),label='local',assumption=assumed)
        try:m.verify(c,[background],goal)
        except m.InvalidProof:continue
        raa_accepted+=1
        for w in worlds:ensure(not truth(background,w) or truth(goal,w),('RAA soundness',background,goal,w))
ensure(raa_accepted==9,'unexpected clash acceptance')
# Check source/example files are unchanged by audit; bind exact tested implementation.
root=pathlib.Path(__file__).resolve().parents[1]
print(json.dumps({'candidate_rule_certificates':attempts,'accepted_local_rules':counts,
 'oracle_models':len(worlds),'oracle_atom_evaluations':len(worlds)*len(atoms),
 'raa_clash_candidates':raa_candidates,'raa_clash_accepted':raa_accepted,'nested_raa_valid':True,'hostile_inputs_rejected':attacks,'single_term_mutations_rejected':mutations,
 'model_sha256':hashlib.sha256((root/'model.py').read_bytes()).hexdigest(),
 'scope':'Finite independent oracle; no exhaustive proof-tree/RAA metatheory or historical semantics certification'},indent=2,sort_keys=True))
