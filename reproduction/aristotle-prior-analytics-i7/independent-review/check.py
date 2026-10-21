"""Independent set-based oracle and certificate adversarial checks; standard library."""
import copy, hashlib, importlib.util, itertools, json
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('subject',BASE/'reduction.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
checks=0

def check(v,msg):
 global checks
 checks+=1
 if not v: raise RuntimeError(msg)

names=('P','S','M'); qs='AEIO'
types=list(itertools.product((False,True),repeat=3))
models=[]
for mask in range(1,256):
 objects=[v for i,v in enumerate(types) if mask&(1<<i)]
 sets={n:frozenset(i for i,v in enumerate(objects) if v[j]) for j,n in enumerate(names)}
 support=tuple(sum((4,2,1)[j] for j,v in enumerate(o) if v) for o in objects)
 models.append((sets,support))

def val(p,sets):
 q,x,y=p; a,b=sets[x],sets[y]
 if q=='A': return a.issubset(b)
 if q=='E': return a.isdisjoint(b)
 if q=='I': return bool(a.intersection(b))
 if q=='O': return bool(a.difference(b))
 raise ValueError(q)

def ps(f,q,z):
 if f==1: return [(q,'M','P'),(z,'S','M')]
 if f==2: return [(q,'P','M'),(z,'S','M')]
 return [(q,'M','P'),(z,'M','S')]

for sets,support in models:
 for p in itertools.product(qs,names,names): check(val(p,sets)==r.truth(p,support),'truth')

classification=json.loads((BASE/'classification.json').read_text())
valid=0;invalid=0;certificates=0
for row in classification:
 policy=row['policy']; contexts=[(s,t) for s,t in models if policy=='allow-empty' or all(s.values())]
 check(len(contexts)==(255 if policy=='allow-empty' else 218),'policy counts')
 premises=ps(row['figure'],row['major'],row['minor'])
 check(tuple(premises)==r.premises(row['figure'],row['major'],row['minor']),'figure orientation')
 for direction,x,y in [('forward','S','P'),('reverse','P','S')]:
  for q in qs:
   goal=(q,x,y)
   bad=[t for s,t in contexts if all(val(p,s) for p in premises) and not val(goal,s)]
   expected=not bad
   check((q in row[direction])==expected,'classification')
   cert=r.make_certificate(premises,goal,policy)
   check((cert is not None)==expected,'certificate existence')
   if expected:
    valid+=1;certificates+=1
    check(r.verify_certificate(cert) is True,'kernel')
    for line in cert['lines']:
     if line['rule'] in ('conversion','Barbara','Celarent'):
      parents=[cert['lines'][i]['p'] for i in line['refs']]
      check(all(not all(val(p,s) for p in parents) or val(line['p'],s) for s,t in contexts),'local rule independent semantics')
   else:
    invalid+=1
    support=tuple(row['countermodels'][direction+q])
    check(support in bad,'recorded countermodel')

saved=json.loads((BASE/'certificates.json').read_text())
for name,c in saved.items():
 check(r.verify_certificate(c) is True,'saved cert')
 for i,line in enumerate(c['lines']): check(all(type(j) is int and 0<=j<i for j in line['refs']),'acyclic dependencies')
check(len(saved)==16,'14 plus 2')
# Disconnect all semantic entrypoints before kernel checking.
original={n:getattr(r,n) for n in ('truth','countermodel','supports','classify')}
def poison(*a,**kw): raise RuntimeError('semantic oracle called')
for n in original: setattr(r,n,poison)
for c in saved.values(): check(r.verify_certificate(c) is True,'oracle-independent kernel')
for n,v in original.items(): setattr(r,n,v)

base=copy.deepcopy(saved['Darii_short'])
mutants=[]
def mut(label,fn):
 c=copy.deepcopy(base);fn(c);mutants.append((label,c))
mut('goal changed',lambda c:c.update(goal=['O','S','P']))
mut('future reference',lambda c:c['lines'][3].update(refs=[5]))
mut('self reference',lambda c:c['lines'][3].update(refs=[3]))
mut('negative reference',lambda c:c['lines'][3].update(refs=[-1]))
mut('bool reference',lambda c:c['lines'][3].update(refs=[True]))
mut('float reference',lambda c:c['lines'][3].update(refs=[2.0]))
mut('string reference',lambda c:c['lines'][3].update(refs=['2']))
mut('universal conversion',lambda c:c['lines'][3].update(p=['A','P','S']))
mut('wrong middle',lambda c:c['lines'][4].update(refs=[3,2]))
mut('wrong output',lambda c:c['lines'][4].update(p=['E','S','M']))
mut('unknown rule',lambda c:c['lines'][4].update(rule='Darii'))
mut('noncontradictory clash',lambda c:c.update(clash=[0,1]))
mut('same-line clash',lambda c:c.update(clash=[1,1]))
mut('missing assumption',lambda c:c['lines'][2].update(rule='premise'))
mut('invented premise',lambda c:c['lines'][0].update(p=['A','P','M']))
mut('wrong policy',lambda c:c.update(policy='universal-existence'))
mut('clash future',lambda c:c.update(clash=[1,100]))
mut('clash boolean',lambda c:c.update(clash=[True,5]))
c=copy.deepcopy(saved['Darapti']);c['policy']='allow-empty';mutants.append(('unauthorized existence',c))
rejected=[]
for label,c in mutants:
 try:r.verify_certificate(c)
 except (ValueError,TypeError,KeyError,IndexError):rejected.append(label)
 else:raise RuntimeError('accepted mutant '+label)
 check(True,'mutant rejected')
# JSON-shaped malformed inputs, rejection may be KeyError/TypeError, not promised uniform API.
malformed=[None,[],{}, {'premises':None}, {'premises':[],'goal':['A','S','P'],'policy':'allow-empty','lines':None,'clash':[]}]
for c in malformed:
 try:r.verify_certificate(c)
 except (ValueError,TypeError,KeyError,IndexError):check(True,'malformed rejected')
 else:raise RuntimeError('accepted malformed')
report={'status':'PASS','independent_assertions':checks,'set_models':255,'conclusions_checked':valid+invalid,'valid':valid,'invalid':invalid,'saved_certificates':len(saved),'fault_variants_rejected':len(rejected),'fault_names':rejected,'malformed_shapes_rejected':len(malformed),'scope':'Independent set oracle, all saved classification rows, local rule semantics, acyclic references, kernel independence, targeted faults; not exhaustive software correctness.'}
print(json.dumps(report,ensure_ascii=False,indent=2))
