"""Independent I.26 argument checks. Does not import author code.
Finite evidence complements, not substitutes for, the written general proofs.
"""
from itertools import product
from fractions import Fraction
import json

TYPES = tuple(product((False, True), repeat=3)) # S,P,M membership
CANONICAL = {1: ('AAA','EAE','AII','EIO'),
             2: ('EAE','AEE','EIO','AOO'),
             3: ('AAI','IAI','AII','EAO','OAO','EIO')}
PAIRS = {1: ((2,1),(0,2)), 2: ((1,2),(0,2)), 3: ((2,1),(2,0))}

def require(ok, label):
    if not ok: raise RuntimeError(label)

def q(kind, x, y):
    if kind == 'A': return x <= y
    if kind == 'E': return not (x & y)
    if kind == 'I': return bool(x & y)
    if kind == 'O': return bool(x - y)
    raise ValueError(kind)

def holds(mode, figure, terms):
    a,b=PAIRS[figure]
    prem=q(mode[0],terms[a[0]],terms[a[1]]) and q(mode[1],terms[b[0]],terms[b[1]])
    return not prem or q(mode[2], terms[0], terms[1])

def terms_for(mask):
    members=[TYPES[i] for i in range(8) if mask & (1<<i)]
    return tuple(frozenset(i for i,t in enumerate(members) if t[j]) for j in range(3))

models=[terms_for(mask) for mask in range(1,256)]
nonempty=[m for m in models if all(m)]
require(len(models)==255 and len(nonempty)==218,'model counts')
results={}; evaluations=0
for label, space in [('empty_allowed',models),('all_terms_nonempty',nonempty)]:
    valid=[]
    for fig in (1,2,3):
        for letters in product('AEIO',repeat=3):
            mood=''.join(letters)
            values=[holds(mood,fig,t) for t in space]
            evaluations+=len(values)
            if all(values): valid.append((fig,mood))
    results[label]=valid
canonical={(f,m) for f,ms in CANONICAL.items() for m in ms}
weak={(1,'AAI'),(1,'EAO'),(2,'EAO'),(2,'AEO')}
require(set(results['all_terms_nonempty']) == canonical|weak,'18 classification')
require(set(results['empty_allowed']) == canonical-{(3,'AAI'),(3,'EAO')},'12 classification')
counts={c:sum(m[-1]==c for f,m in results['all_terms_nonempty']) for c in 'AEIO'}
require(counts==dict(A=1,E=3,I=5,O=9),'nonempty distribution')
require({c:sum(m[-1]==c for f,m in canonical) for c in 'AEIO'}==dict(A=1,E=3,I=4,O=6),'canonical distribution')
contradictions=0; bridges=0; pairs={'A':'O','E':'I','I':'E','O':'A'}
for S,P,M in models:
    for c,d in pairs.items():
        require(q(c,S,P) != q(d,S,P),'contradiction')
        contradictions+=1
    if S:
        require(not q('A',S,P) or q('I',S,P),'A weakens to I')
        require(not q('E',S,P) or q('O',S,P),'E weakens to O')
        bridges+=2
# Explicit examples and exercises, each condition checked independently.
e=frozenset(); a=frozenset({0}); b=frozenset({1}); ab=a|b
checks=[q('A',e,a),q('E',e,a),not q('I',e,a),not q('O',e,a),
        q('I',ab,a),q('O',ab,a),not q('A',ab,a),not q('E',ab,a),
        q('A',e,a),q('A',e,b),not q('I',a,b),
        q('E',e,a),q('A',e,a),not q('O',a,a)]
require(all(checks),'explicit models')
# IID toy equation checked by summing every Bernoulli outcome, exact rational arithmetic.
probability_checks=0
for k in range(1,8):
    for p in (Fraction(0),Fraction(1,4),Fraction(1,2),Fraction(3,4),Fraction(1)):
        total=Fraction(0)
        for bits in product((0,1),repeat=k):
            if any(bits): total += p**sum(bits)*(1-p)**(k-sum(bits))
        require(total==1-(1-p)**k,'IID complement identity')
        probability_checks+=1
# Repeated copies of each type do not change AEIO: one to three representatives.
compression_checks=0
for mask in range(1,256):
    original=terms_for(mask)
    active=[TYPES[i] for i in range(8) if mask & (1<<i)]
    expanded=[t for i,t in enumerate(active) for _ in range(1+i%3)]
    terms=tuple(frozenset(i for i,t in enumerate(expanded) if t[j]) for j in range(3))
    for x in range(3):
        for y in range(3):
            for c in 'AEIO':
                require(q(c,original[x],original[y])==q(c,terms[x],terms[y]),'compression preservation')
                compression_checks+=1
print(json.dumps({'models':len(models),'nonempty_models':len(nonempty),
 'figure_model_evaluations':evaluations,'valid':results,
 'canonical_counts':{'A':1,'E':3,'I':4,'O':6},'nonempty_counts':counts,
 'contradiction_checks':contradictions,'conditional_weakening_checks':bridges,
 'explicit_example_claims':len(checks),'exact_probability_checks':probability_checks,
 'duplicate_type_comparisons':compression_checks,'status':'PASS'},indent=2))
