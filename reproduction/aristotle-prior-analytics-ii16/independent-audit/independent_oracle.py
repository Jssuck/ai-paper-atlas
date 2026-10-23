"""Independent truth-assignment oracle for a deliberately finite Horn teaching model."""
from itertools import combinations, product
import json

def subsets(xs):
    return [frozenset(x for x,b in zip(xs,bits) if b) for bits in product((False,True), repeat=len(xs))]

def models(atoms, rules, facts):
    return [v for v in subsets(atoms) if facts <= v and all(not set(ps)<=v or q in v for ps,q in rules)]

def consequence(atoms, rules, facts):
    ms=models(atoms,rules,set(facts))
    return set.intersection(*(set(m) for m in ms))

def min_supports(atoms,rules,target,candidates):
    good=[s for s in subsets(candidates) if target in consequence(atoms,rules,s)]
    return {s for s in good if not any(t<s for t in good)}

if __name__=='__main__':
    import sys
    from pathlib import Path
    p=Path(sys.argv[1]).resolve(); sys.path.insert(0,str(p))
    import reproduce as engine
    checked=0
    def check(atoms, raw, facts):
        global checked
        rs=tuple(engine.Rule(tuple(ps),q) for ps,q in raw)
        got=set(engine.closure(rs,facts)); want=consequence(atoms,raw,facts)
        if got!=want: raise RuntimeError(('closure',raw,facts,got,want))
        checked+=1
    atoms=('A','B')
    pool=[(tuple(s),q) for s in subsets(atoms) if s for q in atoms]
    for graph in subsets(tuple(range(len(pool)))):
        raw=[pool[i] for i in graph]
        for facts in subsets(atoms): check(atoms,raw,facts)
    horn_cases=checked
    atoms=('A','B','C'); pool=[((p,),q) for p in atoms for q in atoms]
    for graph in subsets(tuple(range(len(pool)))):
        raw=[pool[i] for i in graph]
        for facts in subsets(atoms): check(atoms,raw,facts)
    support_checks=0
    atoms=('A','B')
    pool=[(tuple(s),q) for s in subsets(atoms) if s for q in atoms]
    for graph in subsets(tuple(range(len(pool)))):
        raw=[pool[i] for i in graph]
        rs=tuple(engine.Rule(tuple(ps),q) for ps,q in raw)
        for candidates in subsets(atoms):
            for target in atoms:
                got=set(engine.supports(iter(rs),target,iter(candidates)))
                want=min_supports(atoms,raw,target,candidates)
                if got!=want: raise RuntimeError(('supports',raw,target,candidates,got,want))
                support_checks+=1
    try: engine.Rule((), 'A')
    except ValueError: pass
    else: raise RuntimeError('empty antecedent contract violated')
    for row in engine.examples():
        raw=[(r['premises'],r['conclusion']) for r in row['rules']]
        atoms=set(row['candidate_external_facts'])|set(row['accepted_external_seeds'])|{row['target']}|{q for _,q in raw}|{x for ps,_ in raw for x in ps}
        got=set(row['closure']); want=consequence(tuple(sorted(atoms)),raw,row['accepted_external_seeds'])
        if got!=want: raise RuntimeError(('example closure',row['id']))
        got={frozenset(s) for s in row['minimal_candidate_supports']}
        want=min_supports(tuple(sorted(atoms)),raw,row['target'],row['candidate_external_facts'])
        if got!=want: raise RuntimeError(('example supports',row['id']))
    print(json.dumps({'two_atom_all_horn_seed_cases':horn_cases,'three_atom_unary_seed_cases':checked-horn_cases,'closure_total':checked,'minimal_support_cases':support_checks,'named_examples':len(engine.examples()),'empty_premise_contract':'rejected'},sort_keys=True))
