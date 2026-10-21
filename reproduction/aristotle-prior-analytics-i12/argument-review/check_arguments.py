"""Independent set-semantic checks; no imports from the teaching model."""
import itertools
import json

def check(condition, label):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(label)

def proposition(kind, subject, predicate):
    if kind == 'A': return subject <= predicate
    if kind == 'E': return not (subject & predicate)
    if kind == 'I': return bool(subject & predicate)
    if kind == 'O': return bool(subject - predicate)
    raise ValueError(kind)

def tag(kind, values):
    if kind == 'D': return values[0]
    if kind == 'N': return all(values)
    if kind == 'P': return any(values)
    if kind == 'C': return any(values) and not all(values)
    raise ValueError(kind)

checks = 0
sets = [frozenset(x for x in range(2) if mask & (1 << x)) for mask in range(4)]
moods = {'Barbara': ('A','A','A'), 'Celarent': ('E','A','E'), 'Darii': ('A','I','I'), 'Ferio': ('E','I','O')}
configurations = {(name,t,u,v):[0,0] for name in moods for t in 'DNPC' for u in 'DNPC' for v in 'DNP'}
models=0
for assignment in itertools.product(sets, repeat=6):
    worlds=(assignment[:3],assignment[3:])
    models+=1
    for name,(major,minor,out) in moods.items():
        p = tuple(proposition(major,B,A) for A,B,C in worlds)
        q = tuple(proposition(minor,C,B) for A,B,C in worlds)
        r = tuple(proposition(out,C,A) for A,B,C in worlds)
        for i in range(2):
            check(not(p[i] and q[i]) or r[i],name+' local soundness')
        check(not(all(p) and all(q)) or all(r),name+' NN to N')
        check(not(all(p) and q[0]) or r[0],name+' ND to D')
        check(not(p[0] and all(q)) or r[0],name+' DN to D')
        check(not(any(a and b for a,b in zip(p,q))) or any(r),name+' common world to P')
        for t,u,v in itertools.product('DNPC','DNPC','DNP'):
            entry=configurations[(name,t,u,v)]
            if tag(t,p) and tag(u,q):
                entry[0]+=1
                entry[1]+=not tag(v,r)
        for values in (p,q,r):
            check(not all(values) or values[0],'N to D')
            check(not values[0] or any(values),'D to P')

named = {
 'actual_not_necessary': (({0},{0},{0}),({1},{0},{0})),
 'necessary_major_only': (({0},{0},{0}),({0},{0},{1})),
 'separate_worlds': (({0},{0},{1}),({1},{0},{0})),
 'two_negatives': (({0},{1},{0}),({0},{1},{0}))}
for name,ws in named.items():
    check(all(bool(term) for w in ws for term in w),name+' all terms nonempty')
    if name=='two_negatives':
        p=tuple(proposition('E',B,A) for A,B,C in ws)
        q=tuple(proposition('E',C,B) for A,B,C in ws)
        r=tuple(proposition('E',C,A) for A,B,C in ws)
        check(all(p) and all(q) and not any(r),'two negatives invalid')
    else:
        p=tuple(B<=A for A,B,C in ws)
        q=tuple(C<=B for A,B,C in ws)
        r=tuple(C<=A for A,B,C in ws)
        if name=='actual_not_necessary': check(p[0] and q[0] and r[0] and not all(r),name)
        if name=='necessary_major_only': check(all(p) and q[0] and r[0] and not all(r),name)
        if name=='separate_worlds': check(tag('C',p) and tag('C',q) and not any(r),name)
check(models==4096,'model count')
valid=sum(bad==0 for count,bad in configurations.values())
check(valid==52,'finite classification count')
check(all(count>0 for count,bad in configurations.values()),'all selected premise configurations satisfiable')
print(json.dumps({'independent':True,'models':models,'explicit_checks':checks,'configurations':len(configurations),'finite_valid':valid,'finite_invalid':len(configurations)-valid,'named_countermodels':4,'all_configurations_have_models':True,'limitations':'Two objects, two worlds and four named first-figure skeletons only; finite checks do not replace general proofs.'},ensure_ascii=False,indent=2))
