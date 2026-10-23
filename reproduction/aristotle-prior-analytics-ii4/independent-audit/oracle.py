import sys,json,itertools,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
import model
modes={'Darapti':('A','A','I',True),'Felapton':('E','A','O',True),'Disamis':('I','A','I',False),'Datisi':('A','I','I',False),'Bocardo':('O','A','O',False),'Ferison':('E','I','O',False)}
def prop(k,x,y):
    if k=='A': return all(t in x for t in y)
    if k=='E': return all(t not in x for t in y)
    if k=='I': return any(t in x for t in y)
    if k=='O': return any(t not in x for t in y)
def cls(k,x,y):
    t=prop(k,x,y)
    if k in ('I','O'):return 'true' if t else 'false'
    if not y:return 'vacuous_true'
    if t:return 'true'
    if prop('E' if k=='A' else 'A',x,y):return 'wholly_false'
    return 'partly_false'
checks=0
for mask in range(1,256):
    domain=tuple(t for t in range(8) if mask>>t&1)
    a={t for t in domain if t>=4}; b={t for t in domain if t%4>=2}; c={t for t in domain if t%2==1}
    for name,(p,q,r,exists) in modes.items():
        want={'premises':[prop(p,a,c),prop(q,b,c)],'classes':[cls(p,a,c),cls(q,b,c)],'conclusion':prop(r,a,b),'eligible':bool(c) if exists else True}
        got=model.evaluate(domain,name)
        if got!=want:raise RuntimeError((domain,name,want,got))
        checks+=1
stored=json.loads((root/'witnesses.json').read_text())
if model.survey()!=stored:raise RuntimeError('stored witness mismatch')
for name,data in stored['modes'].items():
    for key,w in data['minimum_witnesses'].items():
        p,q,r,_=modes[name]
        for mask in range(1,256):
            d=tuple(t for t in range(8) if mask>>t&1)
            a={t for t in d if t>=4};b={t for t in d if t%4>=2};c={t for t in d if t%2}
            k='|'.join([cls(p,a,c),cls(q,b,c),str(prop(r,a,b)).lower()])
            if k==key and (len(d),d)<(len(w),tuple(w)):raise RuntimeError('not minimal')
print('independent_elementwise_oracle_evaluations:',checks)
print('stored_witnesses_exact_match: PASS')
print('minimum_cardinality_and_lexicographic_witnesses: PASS')
print('witnesses_sha256:',hashlib.sha256((root/'witnesses.json').read_bytes()).hexdigest())
