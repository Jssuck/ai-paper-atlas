"""Independent bounded semantic checks. Expected values do not call model helpers."""
from pathlib import Path
from itertools import product, combinations, permutations
from collections import Counter
import hashlib, importlib.util, json, sys, time
ROOT = Path(__file__).resolve().parent
MODEL = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT.parent / 'model.py'
start_hash = hashlib.sha256(MODEL.read_bytes()).hexdigest()
sys.path.insert(0, str(MODEL.parent))
import model as m
counts=Counter()

class AuditFailure(RuntimeError):
    pass

def check(condition, label):
    if not condition:
        raise AuditFailure(label)

def powerset(values):
    return [tuple(values[i] for i in range(len(values)) if mask & (1 << i)) for mask in range(1 << len(values))]

# Enumerate all three-object, two-binary-feature catalogs. Expected partitions
# are built by repeated relation-class extraction, not a dictionary signature.
features=('x','y')
objects=('a','b','c')
masks=powerset(features)
for bit_rows in product(product(('0','1'), repeat=2), repeat=3):
    table={name:dict(zip(features,row)) for name,row in zip(objects,bit_rows)}
    catalog=m.Catalog(features,(('0','1'),('0','1')),tuple(zip(objects,bit_rows)))
    counts['catalogs']+=1
    rels={}
    for selected in masks:
        remaining=set(objects); expected=[]
        rel={(a,b) for a in objects for b in objects if all(table[a][f]==table[b][f] for f in selected)}
        while remaining:
            seed=min(remaining)
            group={b for a,b in rel if a==seed}
            expected.append(frozenset(group)); remaining-=group
        actual={frozenset(g) for g in m.equivalence_classes(catalog,selected)}
        check(actual==set(expected),'partition')
        rels[frozenset(selected)]=rel
        counts['partitions']+=1
    for f,g in product(masks,repeat=2):
        if set(f)<=set(g):
            check(rels[frozenset(g)]<=rels[frozenset(f)],'refinement')
            counts['refinement_pairs']+=1
    observations=[]
    for name, selected in product(objects,masks):
        for provenance in ('current','recalled'):
            actual=m.attend(catalog,name,selected,provenance)
            check(actual.attributes==tuple((f,table[name][f]) for f in selected),'attend')
            check(actual.provenance==provenance,'provenance')
            observations.append((actual,dict(actual.attributes)))
            counts['attention_records']+=1
    for (left, lv),(right,rv),feature in product(observations,observations,features):
        expected='unknown' if feature not in lv or feature not in rv else ('equal' if lv[feature]==rv[feature] else 'different')
        check(m.compare(catalog,left,right,feature)==expected,'comparison')
        counts['comparisons']+=1
    # One possibly empty partial observation per object, all 4^3 choices.
    for selections in product(masks,repeat=3):
        obs=tuple(m.attend(catalog,n,f) for n,f in zip(objects,selections))
        for selected in masks[1:]:
            pools={f:{table[n][f] for n,fs in zip(objects,selections) if f in fs} for f in selected}
            if any(not values for values in pools.values()):
                try: m.imagine(catalog,obs,selected)
                except ValueError: pass
                else: raise AuditFailure('missing pool accepted')
                counts['missing_pool_rejections']+=1
                continue
            # Enumerate the global feature domain, then filter membership in pools.
            possible=[tuple(zip(selected,vals)) for vals in product(('0','1'),repeat=len(selected))
                      if all(value in pools[f] for f,value in zip(selected,vals))]
            expected={attrs:tuple(n for n in objects if all(table[n][f]==v for f,v in attrs)) for attrs in possible}
            actual={c.attributes:c.witnesses for c in m.imagine(catalog,obs,selected)}
            check(actual==expected,'imagination')
            counts['imagination_queries']+=1
            counts['imagined_concepts']+=len(actual)

# All <=3-rule positive Horn theories over three atoms, with every fact subset.
# Expected consequences are intersections of all satisfying valuations. No
# production oracle or production forward chaining is used for expectations.
atoms=('p','q','r'); subsets=powerset(atoms)
candidates=[(pre,out) for pre in subsets for out in atoms]
for size in range(4):
    for indices in combinations(range(len(candidates)),size):
        raw_rules=[candidates[i] for i in indices]
        rules=tuple(m.Rule(f'r{i}',pre,out) for i,(pre,out) in zip(indices,raw_rules))
        for facts in subsets:
            theory=m.Theory(atoms,facts,rules)
            models=[set(v) for v in subsets if set(facts)<=set(v) and all(not set(pre)<=set(v) or out in v for pre,out in raw_rules)]
            expected=set.intersection(*models)
            proof=m.closure(theory); actual={s.atom for s in proof}
            check(actual==expected,'Horn intersection')
            check(len(actual)==len(proof),'duplicate proof atom')
            for target in atoms:
                check(m.verify_certificate(theory,proof,target)==(target in expected),'closure certificate')
                counts['closure_certificate_queries']+=1
            if size<=1:
                entailed,n=m.semantic_oracle(theory)
                check(set(entailed)==expected and n==len(models),'oracle')
                counts['production_oracle_queries']+=1
            counts['horn_theories']+=1

# Check arbitrary claimed certificates, including cycles, misplaced facts,
# invalid rule labels, omitted prerequisites and irrelevant suffixes.
proof_theories=[m.Theory(atoms,('p',),(
    m.Rule('pq',('p',),'q'),m.Rule('qr',('q',),'r'),m.Rule('rp',('r',),'p'))),
    m.Theory(atoms,(),(m.Rule('seed',(),'p'),m.Rule('and',('p','q'),'r'),m.Rule('rq',('r',),'q'))),
    m.Theory(atoms,('p','q'),(m.Rule('and',('p','q'),'r'),))]
for t in proof_theories:
    byname={r.name:r for r in t.rules}
    labels=(None,)+tuple(byname)+('missing',)
    for size in range(4):
        for atom_sequence in product(atoms,repeat=size):
            for rule_sequence in product(labels,repeat=size):
                proof=tuple(m.Step(a,r) for a,r in zip(atom_sequence,rule_sequence))
                valid=True
                seen=[]
                for atom,label in zip(atom_sequence,rule_sequence):
                    if atom in seen: valid=False; break
                    if label is None:
                        if atom not in t.facts: valid=False; break
                    elif label not in byname or byname[label].conclusion!=atom or any(p not in seen for p in byname[label].premises):
                        valid=False; break
                    seen.append(atom)
                for target in atoms:
                    check(m.verify_certificate(t,proof,target)==(valid and target in seen),'arbitrary certificate')
                    counts['arbitrary_certificate_queries']+=1
                counts['arbitrary_certificates']+=1

# Extensional syllogism: every triple of subsets, including the empty universe.
for n in range(5):
    u=tuple(str(i) for i in range(n)); ss=powerset(u)
    for small,middle,large in product(ss,repeat=3):
        raw=m.subset_syllogism(u,small,middle,large)
        first=all(x in middle for x in small) and all(x in large for x in middle)
        conclusion=all(x in large for x in small)
        check(raw=={'premises':first,'conclusion':conclusion,'implication':not first or conclusion,'small_nonempty':len(small)>0},'subset syllogism')
        counts['inclusion_triples']+=1

# Boundary claims not entailed by the model: no observed coordinate, no catalog
# witnesses and no seeded Horn cycle.
empty=m.Catalog(('x',),(('v',),),())
check(m.equivalence_classes(empty,())==(),'empty catalog partition')
empty_t=m.Theory((),(),())
check(m.closure(empty_t)==() and m.semantic_oracle(empty_t)==((),1),'empty theory')
# Independent input-contract and resource boundaries. Boolean/string/list inputs
# must not silently coerce to tuple collections, and recalled data remain exact.
c=m.Catalog(('x',),(('0','1'),),(('a',('0',)),))
o=m.attend(c,'a',('x',))
t=m.Theory(('p',),('p',),())
bad_calls=[
 lambda: m.Catalog((),(),()),
 lambda: m.Catalog('x',(('0',),),()),
 lambda: m.Catalog(('x',),([],),()),
 lambda: m.Catalog(('x','x'),(('0',),('0',)),()),
 lambda: m.Catalog(('x',),((),),()),
 lambda: m.Catalog(('x',),(('0','0'),),()),
 lambda: m.Catalog(('x',),(('0',),),(('a',()),)),
 lambda: m.Catalog(('x',),(('0',),),(('a',('1',)),)),
 lambda: m.Catalog(('x',),(('0',),),(('a',('0',)),('a',('0',)))),
 lambda: m.Catalog(tuple(str(i) for i in range(9)),(('0',),)*9,()),
 lambda: m.Catalog(('x',),(tuple(str(i) for i in range(9)),),()),
 lambda: m.Catalog(('x',),(('0',),),tuple((str(i),('0',)) for i in range(33))),
 lambda: m.attend(c,'a','x'),
 lambda: m.attend(c,'a',('x','x')),
 lambda: m.attend(c,'missing',()),
 lambda: m.attend(c,'a',(),'other'),
 lambda: m.compare(c,m.Observation('a',(('x','1'),),'recalled'),o,'x'),
 lambda: m.compare(c,m.Observation('a',(('x','1'),),'current'),o,'x'),
 lambda: m.compare(c,o,o,'missing'),
 lambda: m.reflect(c,o,False,()),
 lambda: m.imagine(c,(o,),()),
 lambda: m.imagine(c,(o,)*33,('x',)),
 lambda: m.imagine(c,[o],('x',)),
 lambda: m.Rule('r',('p','p'),'p'),
 lambda: m.Theory(('p',),('q',),()),
 lambda: m.Theory(('p',),(),(m.Rule('r',('q',),'p'),)),
 lambda: m.Theory(('p',),(),(m.Rule('r',(),'q'),)),
 lambda: m.Theory(('p',),(),(m.Rule('r',(),'p'),m.Rule('r',(),'p'))),
 lambda: m.Theory(tuple(str(i) for i in range(13)),(),()),
 lambda: m.Theory(('p',),(),tuple(m.Rule(str(i),(),'p') for i in range(129))),
 lambda: m.verify_certificate(t,(m.Step('p'),)*13,'p'),
 lambda: m.verify_certificate(t,[],'p'),
 lambda: m.verify_certificate(t,(),'q'),
 lambda: m.subset_syllogism(('a',),('outside',),(),()),
 lambda: m.subset_syllogism(('a',),('a','a'),(),()),
]
for call in bad_calls:
    try: call()
    except ValueError: counts['input_rejections']+=1
    else: raise AuditFailure('invalid input accepted')
for dimension,expected in ((4,4096),(5,None)):
    ff=tuple('f'+str(i) for i in range(dimension))
    vv=tuple(str(i) for i in range(8))
    cc=m.Catalog(ff,(vv,)*dimension,tuple((str(i),(str(i),)*dimension) for i in range(8)))
    oo=tuple(m.attend(cc,n,ff) for n,_ in cc.objects)
    if expected is None:
        try: m.imagine(cc,oo,ff)
        except ValueError: counts['resource_boundary_checks']+=1
        else: raise AuditFailure('oversize product accepted')
    else:
        check(len(m.imagine(cc,oo,ff))==expected,'exact product budget')
        counts['resource_boundary_checks']+=1

end_hash=hashlib.sha256(MODEL.read_bytes()).hexdigest()
check(start_hash==end_hash,'model changed during independent run')
report={'status':'PASS','optimization':sys.flags.optimize,'source_sha256':start_hash,
        'review_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'counts':dict(counts),
        'scope':'Finite software checks only; not a validation of historical psychological claims.'}
print(json.dumps(report,ensure_ascii=False,indent=2))
