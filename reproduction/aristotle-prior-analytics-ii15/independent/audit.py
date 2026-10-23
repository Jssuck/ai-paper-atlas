#!/usr/bin/env python3
"""Independent bounded set oracle; no production evaluator or result generator imported."""
import itertools
import json
from pathlib import Path

D = frozenset(range(3))
SETS = [frozenset(x for x in D if m & (1 << x)) for m in range(8)]

def holds(kind, predicate, subject):
    if kind == 'U':
        return subject <= predicate
    if kind == 'E':
        return not subject & predicate
    if kind == 'I':
        return bool(subject & predicate)
    if kind == 'O':
        return bool(subject - predicate)
    raise ValueError(kind)

def check(condition, label):
    if not condition:
        raise RuntimeError(label)


def run():
    models = list(itertools.product(SETS, repeat=3))
    records = []
    for figure, pair in [(2, (0, 1, 0, 2)), (3, (1, 0, 2, 0))]:
        for p, q in [('U','E'), ('E','U'), ('U','O'), ('O','U'), ('I','E'), ('E','I')]:
            for policy in ['empty_allowed','all_nonempty']:
                relevant = [m for m in models if policy == 'empty_allowed' or all(m)]
                witnesses = [m for m in relevant if holds(p,m[pair[0]],m[pair[1]]) and holds(q,m[pair[2]],m[pair[3]])]
                for orientation in ['BC','CB']:
                    pred, sub = (1,2) if orientation == 'BC' else (2,1)
                    for target in ['E','O']:
                        bad = [m for m in witnesses if not holds(target,m[pred],m[sub])]
                        records.append({'figure':figure,'premises':p+q,'policy':policy,'conclusion':target+orientation,'satisfying':len(witnesses),'valid_on_three_objects':not bad,'counterexample':[sorted(s) for s in bad[0]] if bad else None})
    # Specific identity/whole-part tests are evaluated independently, not by explosion.
    named = {}
    named['IO_coexist'] = holds('I',{0},{0,1}) and holds('O',{0},{0,1})
    named['UE_empty_coexist'] = holds('U',{0},set()) and holds('E',{0},set())
    named['E_self_empty_true'] = holds('E',set(),set())
    named['E_self_nonempty_false'] = not holds('E',{0},{0})
    named['O_self_always_false'] = all(not holds('O',s,s) for s in SETS)
    named['UO_exact_complements'] = all(holds('U',p,s) != holds('O',p,s) for p,s in itertools.product(SETS,repeat=2))
    named['EI_exact_complements'] = all(holds('E',p,s) != holds('I',p,s) for p,s in itertools.product(SETS,repeat=2))
    named['UE_disjoint_nonempty_subject'] = all(not(holds('U',p,s) and holds('E',p,s)) for p,s in itertools.product(SETS,repeat=2) if s)
    named['whole_part_E_false_nonempty_part'] = all(not holds('E',whole,part) for whole,part in itertools.product(SETS,repeat=2) if part and part <= whole)
    named['whole_part_O_false'] = all(not holds('O',whole,part) for whole,part in itertools.product(SETS,repeat=2) if part <= whole)
    named['same_subject_UE_no_nonempty_model'] = not any(holds('U',p,s) and holds('E',p,s) for p,s in itertools.product(SETS,repeat=2) if s)
    named['unrelated_terms_can_have_true_negative'] = holds('U',{0},{0}) and holds('E',{0},{1}) and holds('E',{0},{1})
    for label,value in named.items(): check(value,label)
    # Famous generic inference directions before any coincident terms are imposed.
    expected = [(2,'UE','EBC'),(2,'EU','EBC'),(2,'UO','OBC'),(2,'IE','OCB'),(3,'UE','OCB'),(3,'EU','OBC'),(3,'UO','OCB'),(3,'OU','OBC'),(3,'IE','OCB'),(3,'EI','OBC')]
    for f,p,c in expected:
        rec = next(r for r in records if r['figure']==f and r['premises']==p and r['conclusion']==c and r['policy']=='all_nonempty')
        check(rec['valid_on_three_objects'],str((f,p,c)))
    return {'domain_size':3,'labelled_models':len(models),'records':records,'named_checks':named,'named_checks_passed':len(named),'generic_direction_checks':len(expected),'scope':'Bounded independent check; not a general proof or reconstruction of all ancient semantics.'}

if __name__ == '__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2,sort_keys=True))
