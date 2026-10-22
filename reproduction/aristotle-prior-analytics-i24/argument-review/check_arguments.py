"""Independent finite checks of I.24 constructions; no author module imported."""
from itertools import product, combinations
from fractions import Fraction
import json, sys
from pathlib import Path

NAMES = ('S','P','M')
TYPES = tuple(product((False, True), repeat=3))
FORMS = 'AEIO'
FIGURES = {1:(('M','P'),('S','M')),2:(('P','M'),('S','M')),3:(('M','P'),('M','S'))}

def true(model, q, x, y):
    xs,ys = NAMES.index(x),NAMES.index(y)
    inside = [row[ys] for row in model if row[xs]]
    if q == 'A': return all(inside)
    if q == 'E': return not any(inside)
    if q == 'I': return any(inside)
    if q == 'O': return any(not z for z in inside)
    raise ValueError(q)

def check(condition,label):
    if not condition: raise RuntimeError(label)

def model_of(S,P,M):
    return frozenset((x in S,x in P,x in M) for x in S|P|M)

def premises(model,fig,p,q):
    a,b = FIGURES[fig]
    return true(model,p,*a) and true(model,q,*b)

def nonempty(model):
    return all(any(t[k] for t in model) for k in range(3))

def witnesses(fig,p,q,overlap):
    # Each premise gets an independent object; endpoints either equal or disjoint.
    out=set()
    for form,(x,y) in zip((p,q),FIGURES[fig]):
        choices=[]
        for t in TYPES:
            relation = (t[0] == t[1]) if overlap else not(t[0] and t[1])
            if relation and true({t},form,x,y): choices.append(t)
        check(bool(choices),'witness exists')
        out.add(choices[0])
    # Preserve equality/disjointness and supply all three nonempty terms.
    out.update({(True,True,False),(False,False,True)} if overlap else {(True,False,False),(False,True,False),(False,False,True)})
    return frozenset(out)

counts={'models':0,'mood_model_checks':0,'two_negative_constructions':0,'two_particular_constructions':0,'single_universal_local_extensions':0,'premise_preserving_extensions':0,'explicit_checks':0}
# Local extension table proves an M choice exists for each quantified edge.
extension_table=[]
for edge in sorted(set(e for pair in FIGURES.values() for e in pair)):
    for form in 'AE':
        for target,pval in [('A',False),('E',True)]:
            choices=[(True,pval,m) for m in (False,True) if true({(True,pval,m)},form,*edge)]
            check(bool(choices),'local extension choice')
            extension_table.append({'universal':form+''.join(edge),'target':target,'M':choices[0][2]})
            counts['single_universal_local_extensions']+=1
# General two-negative constructions, checking all finite syntactic cases.
disjoint=model_of({'s'},{'p'},{'m'})
equal=model_of({'s'},{'s'},{'m'})
for fig,p,q,target in product(FIGURES,'EO','EO',FORMS):
    model=disjoint if target in 'AI' else equal
    check(premises(model,fig,p,q) and not true(model,target,'S','P') and nonempty(model),'two negatives')
    counts['two_negative_constructions']+=1
# Direct independent witnesses for all two-particular cases.
for fig,p,q,target in product(FIGURES,'IO','IO',FORMS):
    model=witnesses(fig,p,q,target in 'EO')
    check(premises(model,fig,p,q) and not true(model,target,'S','P') and nonempty(model),'two particulars')
    counts['two_particular_constructions']+=1
models=[frozenset(c) for n in range(1,9) for c in combinations(TYPES,n)]
valid={False:[], True:[]}
for required in (False,True):
    allowed=[m for m in models if not required or nonempty(m)]
    counts['models']+=len(allowed)
    for fig,p,q,r in product(FIGURES,FORMS,FORMS,FORMS):
        good=True
        for model in allowed:
            counts['mood_model_checks']+=1
            if premises(model,fig,p,q) and not true(model,r,'S','P'):good=False
        if good:
            valid[required].append(f'{p}{q}{r}-{fig}')
            check(any(x in 'AI' for x in (p,q)),'affirmative necessary')
            check(any(x in 'AE' for x in (p,q)),'universal necessary')
            check(r not in 'AE' or all(x in 'AE' for x in (p,q)),'universal conclusion')
# Test proof's extension operation on every starting support and all mixed pairs.
for model,fig,p,q in product(models,FIGURES,FORMS,FORMS):
    if sum(x in 'AE' for x in (p,q))!=1 or not premises(model,fig,p,q):continue
    uform,edge = next((f,e) for f,e in zip((p,q),FIGURES[fig]) if f in 'AE')
    for target,pval in [('A',False),('E',True)]:
        extra=next((True,pval,m) for m in (False,True) if true({(True,pval,m)},uform,*edge))
        extended=model|{extra}
        check(premises(extended,fig,p,q) and not true(extended,target,'S','P'),'extension preserves premises')
        check(not nonempty(model) or nonempty(extended),'existence preserved')
        counts['premise_preserving_extensions']+=1
music=model_of({'a'},{'b'},{'a','b'})
check(true(music,'A','S','M') and true(music,'I','M','P') and not true(music,'A','S','P') and not true(music,'I','S','P'),'music');counts['explicit_checks']+=1
universal_partial=model_of({'a','b'},{'a'},{'a'})
check(premises(universal_partial,3,'A','A') and true(universal_partial,'I','S','P') and not true(universal_partial,'A','S','P'),'Darapti weak');counts['explicit_checks']+=1
empty_middle=model_of({'a'},{'b'},set())
check(premises(empty_middle,3,'A','A') and not true(empty_middle,'I','S','P'),'Darapti existence');counts['explicit_checks']+=1
check(Fraction(180)-Fraction(75,2)==Fraction(285,2),'exact subtraction');counts['explicit_checks']+=1
check(Fraction(180)-30 != Fraction(180)-40,'missing equality');counts['explicit_checks']+=1
report={'status':'passed','counts':counts,'valid_empty_allowed':valid[False],'valid_all_terms_nonempty':valid[True],'extension_table':extension_table,'scope':'Finite independent checks supplement general constructions; not proof of arbitrary logic, modal semantics or epistemic noncircularity.'}
print(json.dumps(report,ensure_ascii=False,indent=2))
