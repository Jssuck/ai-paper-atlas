"""Finite extensional teaching model; does not certify essence or historical taxonomy."""
from itertools import product
import json

def validate(universe, *sets):
    u=frozenset(universe)
    if any(not frozenset(s)<=u for s in sets):
        raise ValueError('set outside universe')
    return u

def intersection(universe, features):
    fs=tuple(frozenset(f) for f in features)
    result=validate(universe,*fs)
    for f in fs:result=result & f
    return result

def describe(universe,target,features):
    universe=frozenset(universe)
    t=frozenset(target);fs=tuple(frozenset(f) for f in features)
    validate(universe,t,*fs)
    exact=intersection(universe,fs)==t
    return {'sound':all(t<=f for f in fs), 'exact':exact,
            'severally_wider':all(t<f for f in fs),
            'irredundant':exact and all(intersection(universe,fs[:i]+fs[i+1:])!=t for i in range(len(fs)))}

def greedy_reduce(universe,target,features,order=None):
    universe=frozenset(universe)
    fs=tuple(frozenset(f) for f in features);t=frozenset(target)
    if not describe(universe,t,fs)['exact']:raise ValueError('initial conjunction not exact')
    order=tuple(range(len(fs))) if order is None else tuple(order)
    if sorted(order)!=list(range(len(fs))):raise ValueError('order must be permutation')
    keep=list(range(len(fs)))
    for i in order:
        trial=[j for j in keep if j!=i]
        if intersection(universe,[fs[j] for j in trial])==t:keep=trial
    return tuple(keep)

def split_check(parent,left,right,target):
    p,l,r,t=map(frozenset,(parent,left,right,target))
    validate(p,l,r,t)
    partition=(l|r)==p and not (l&r)
    return {'covers':l|r==p,'disjoint':not l&r,'partition':partition,
            'target_left':t<=l,'target_right':t<=r,
            'nonempty_unique_branch':partition and bool(t) and ((t<=l)!=(t<=r))}

def common_features(rows):
    rows=tuple(frozenset(r) for r in rows)
    if not rows:raise ValueError('no observations; cannot infer common vocabulary')
    return frozenset.intersection(*rows)

def subsets(n):
    return [frozenset(i for i in range(n) if mask>>i&1) for mask in range(1<<n)]

def experiment(max_n=4):
    total=sound=exact=wider_exact=irred=diff=0
    for n in range(max_n+1):
        u=frozenset(range(n));ss=subsets(n)
        for t,a,b in product(ss,repeat=3):
            total+=1;d=describe(u,t,[a,b])
            oracle=frozenset(x for x in u if x in a and x in b)
            diff+=intersection(u,[a,b])!=oracle
            sound+=d['sound'];exact+=d['exact'];wider_exact+=d['exact'] and d['severally_wider'];irred+=d['irredundant']
    split_total=split_valid=0
    for n in range(5):
        p=frozenset(range(n));ss=subsets(n)
        for l,r,t in product(ss,repeat=3):
            split_total+=1;split_valid+=split_check(p,l,r,t)['nonempty_unique_branch']
    u=frozenset(range(5));t=frozenset({0})
    # Outside target complements: {1,2,3}, {4}, {1,4}, {2}, {3}; first two and last three cover.
    fs=[u-{1,2,3},u-{4},u-{1,4},u-{2},u-{3}]
    first=greedy_reduce(u,t,fs);reverse=greedy_reduce(u,t,fs,reversed(range(5)))
    return {'max_n':max_n,'triples':total,'sound':sound,'exact':exact,'exact_severally_wider':wider_exact,
            'irredundant_exact':irred,'membership_oracle_differences':diff,
            'split_cases':split_total,'nonempty_unique_branch':split_valid,
            'greedy_forward':first,'greedy_reverse':reverse,
            'limits':'Finite extension only; no essence, natural-kind or complete-division certification.'}

if __name__=='__main__':print(json.dumps(experiment(),ensure_ascii=False,indent=2))
