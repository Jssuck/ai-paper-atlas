"""Independent set-based audit of the Chinese argument; imports no author model."""
from itertools import product
from pathlib import Path
import json, re, hashlib

checks=0
def check(v, label):
    global checks
    checks+=1
    if not v: raise RuntimeError(label)
def q(k,x,y):
    if k=='A': return all(a in y for a in x)
    if k=='E': return not any(a in y for a in x)
    if k=='I': return any(a in y for a in x)
    if k=='O': return any(a not in y for a in x)
    raise ValueError(k)
base=Path(__file__).resolve().parent
main=base.parents[1]/'papers/ancient/aristotle-prior-analytics-i6.zh-CN.md'
src=base.parents[1]/'papers/ancient/aristotle-prior-analytics-i6.sources.zh-CN.md'
text=main.read_text()
rows=re.findall(r'^\| ([AEIO]{2}) \| \(([^)]+)\) \| \(([^)]+)\) \|$',text,re.M)
check(len(rows)==10,'ten countermodel rows')
for pair,left,right in rows:
    for side,raw in enumerate((left,right)):
        sets=[set(map(int,re.findall(r'\d+',s))) for s in raw.split(';')]
        check(len(sets)==3,'three sets')
        m,s,p=sets
        check(all(sets),'all terms nonempty')
        check(q(pair[0],m,p) and q(pair[1],m,s),'countermodel premise '+pair)
        check([q(k,s,p) for k in 'AEIO']==([True,False,True,False] if side==0 else [False,True,False,True]),'outer relation '+pair)
# Exhaustive nonempty support models using independent membership tuples, not author bit encoding.
types=list(product((False,True),repeat=3)) # M,S,P
models=[]
for bits in product((False,True),repeat=8):
    if not any(bits): continue
    chosen=[t for t,b in zip(types,bits) if b]
    sets=[{i for i,t in enumerate(chosen) if t[j]} for j in range(3)]
    models.append(sets)
expected={('A','I'):'I',('I','A'):'I',('O','A'):'O',('E','I'):'O'}
policy_counts={}
validity={}
for policy in ('allow_empty','middle_nonempty','all_nonempty'):
    ms=[z for z in models if policy=='allow_empty' or (bool(z[0]) if policy=='middle_nonempty' else all(z))]
    policy_counts[policy]=len(ms)
    rules=dict(expected)
    if policy!='allow_empty': rules.update({('A','A'):'I',('E','A'):'O'})
    got=[]
    for a,b in product('AEIO',repeat=2):
        premises=[(m,s,p) for m,s,p in ms if q(a,m,p) and q(b,m,s)]
        check(bool(premises),'no unsatisfiable premise pair')
        for c in 'AEIO':
            holds=all(q(c,s,p) for m,s,p in premises)
            check(holds==(rules.get((a,b))==c),f'classification {policy} {a}{b}{c}')
            if holds: got.append(a+b+c)
        # Both universal conclusions fail after explicit M-external extension.
        for m,s,p in premises:
            new=8
            check(q(a,m,p) and q(b,m,s|{new}),'A extension preserves premises')
            check(not q('A',s|{new},p),'A extension falsifies conclusion')
            check(q(a,m,p|{new}) and q(b,m,s|{new}),'E extension preserves premises')
            check(not q('E',s|{new},p|{new}),'E extension falsifies conclusion')
    validity[policy]=got
check(policy_counts=={'allow_empty':255,'middle_nonempty':240,'all_nonempty':218},'support counts')
# Check six witnesses by semantic identity and both general reductio patterns.
for m,s,p in models:
    for pair,c in [('AA','I'),('EA','O'),('IA','I'),('AI','I'),('OA','O'),('EI','O')]:
        if pair in ('AA','EA') and not m: continue
        if not(q(pair[0],m,p) and q(pair[1],m,s)): continue
        witness=(m&p if pair=='IA' else m&s if pair in ('AI','EI') else m-p if pair=='OA' else m)
        check(bool(witness),'witness exists')
        check(all(x in s and ((x in p) if c=='I' else x not in p) for x in witness),'same witness')
    if q('O',m,p) and q('A',m,s): check(not q('A',s,p),'Bocardo reductio')
    if m and q('A',m,p) and q('E',m,s): check(q('O',p,s),'reverse-direction caveat')
    check(q('A',s,p)!=q('O',s,p),'A/O complement')
    check(q('E',s,p)!=q('I',s,p),'E/I complement')
# Type compression on every three-predicate model over a 3-object labeled universe.
u=range(3)
subsets=[{i for i,b in zip(u,bits) if b} for bits in product((False,True),repeat=3)]
for m,s,p in product(subsets,repeat=3):
    ts={(i in m,i in s,i in p) for i in u}
    compressed=[{t for t in ts if t[j]} for j in range(3)]
    orig=[m,s,p]
    for x,y in product(range(3),repeat=2):
        for k in 'AEIO': check(q(k,orig[x],orig[y])==q(k,compressed[x],compressed[y]),'compression')
    check([bool(z) for z in orig]==[bool(z) for z in compressed],'nonempty compression')
check(len(re.findall(r'^\d+\. \*\*',text,re.M))==20,'twenty exercise answers')
result={'status':'PASS','checks':checks,'countermodels_read_from_main':20,'support_counts':policy_counts,'valid_rules':validity,'compression_labeled_models':512,'reviewed_sha256':{main.name:hashlib.sha256(main.read_bytes()).hexdigest(),src.name:hashlib.sha256(src.read_bytes()).hexdigest()},'method':'Independent Python sets and membership tuples; no author model imports. Finite checks supplement explicit general proofs.'}
print(json.dumps(result,ensure_ascii=False,indent=2))
