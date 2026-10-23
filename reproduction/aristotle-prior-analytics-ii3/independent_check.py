"""Independent review oracle: quantified predicates, independent support enumeration.
Run with ordinary Python (assert checks must remain enabled).
"""
import sys,json,itertools,collections,hashlib
from pathlib import Path
r=Path(__file__).resolve().parent
sys.path.insert(0,str(r.resolve()))
import model
moods={'Cesare':(('E','M','P'),('A','M','S'),('E','P','S')),'Camestres':(('A','M','P'),('E','M','S'),('E','P','S')),'Festino':(('E','M','P'),('I','M','S'),('O','P','S')),'Baroco':(('A','M','P'),('O','M','S'),('O','P','S'))}
def truth(d,k,p,s):
 v=[x in d[p] for x in d[s]]
 return {'A':all(v),'E':not any(v),'I':any(v),'O':not all(v)}[k]
def state(d,k,p,s):
 if k in 'IO': return 'true' if truth(d,k,p,s) else 'false'
 v=[x in d[p] for x in d[s]]
 if not v:return 'vacuous_true'
 if truth(d,k,p,s):return 'true'
 if all(v) or not any(v):return 'wholly_false'
 return 'partly_false'
def key(d,qs):return '|'.join([state(d,*q) for q in qs[:2]]+['T' if truth(d,*qs[2]) else 'F'])
def typ(d): return {4*(x in d['M'])+2*(x in d['P'])+(x in d['S']) for x in d['universe']}
report=json.loads((r/'witnesses.json').read_text())
for policy in ['unrestricted','all_terms_nonempty']:
 counts={k:collections.Counter() for k in moods};mins={k:{} for k in moods};n=0
 for mask in range(1,256):
  u=set(i for i in range(8) if mask>>i&1)
  d={'universe':u,'M':{i for i in u if i>=4},'P':{i for i in u if i in [2,3,6,7]},'S':{i for i in u if i%2}}
  if policy=='all_terms_nonempty' and not all(d[t] for t in ['M','P','S']):continue
  n+=1
  for mood,qs in moods.items():
   k=key(d,qs);counts[mood][k]+=1;mins[mood][k]=min(mins[mood].get(k,99),len(u))
   assert not (all(truth(d,*q) for q in qs[:2]) and not truth(d,*qs[2]))
 assert n==report[policy]['models']
 for mood,rows in report[policy]['rows'].items():
  assert dict(counts[mood])=={k:v['count'] for k,v in rows.items()}
  for k,v in rows.items():
   d={t:set(z) for t,z in v['smallest_type_witness'].items()}
   assert key(d,moods[mood])==k and len(d['universe'])==mins[mood][k]
 print(policy,n,'counts and all witnesses independently verified')
# Labelled domains deliberately retain repeated membership types.
n=0;checks=0
for size in range(1,5):
 u=set(range(size));subs=[{x for x in u if mask>>x&1} for mask in range(1<<size)]
 for M,P,S in itertools.product(subs,repeat=3):
  d=dict(universe=u,M=M,P=P,S=S); m=model.Model(**{k:frozenset(v) for k,v in d.items()});compressed=model.type_model(typ(d));n+=1
  for kind,p,s in itertools.product('AEIO','MPS','MPS'):
   assert truth(d,kind,p,s)==model.proposition(m,kind,p,s)==model.proposition(compressed,kind,p,s)
   assert state(d,kind,p,s)==model.classify(m,kind,p,s)==model.classify(compressed,kind,p,s)
   checks+=1
print('labelled domains sizes1..4:',n,'models;',checks,'proposition/status/compression comparisons PASS')
print('saved witnesses sha256',hashlib.sha256((r/'witnesses.json').read_bytes()).hexdigest())
