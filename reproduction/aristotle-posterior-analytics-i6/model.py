"""I.6 teaching model: finite, constant-domain, whole-proposition necessity.
No claim that finite truth identifies essence, cause, or Aristotle's modal semantics.
"""
from itertools import product
import json


def validate_world(world, size):
    if type(size) is not int or size < 1:
        raise ValueError('domain size must be a positive integer')
    if not isinstance(world, (tuple, list)) or len(world) != 3:
        raise ValueError('world must contain A, B, C masks')
    if any(type(m) is not int or m < 0 or m >= (1 << size) for m in world):
        raise ValueError('mask outside the domain')


def all_of(subject, predicate):
    return (subject & ~predicate) == 0


def none_of(subject, predicate):
    return (subject & predicate) == 0


def evaluate(worlds, size=2):
    worlds = tuple(worlds)
    if not worlds:
        raise ValueError('at least one accessible world is required')
    for world in worlds:
        validate_world(world, size)
    ab = [all_of(b, a) for a, b, c in worlds]
    bc = [all_of(c, b) for a, b, c in worlds]
    ac = [all_of(c, a) for a, b, c in worlds]
    return {'actual_ab': ab[0], 'actual_bc': bc[0], 'actual_ac': ac[0],
            'necessary_ab': all(ab), 'necessary_bc': all(bc),
            'necessary_ac': all(ac), 'all_terms_nonempty': all(all(w) for w in worlds)}


def object_oracle(worlds, size=2):
    """Separate element-wise implementation, not a second mask-subset call."""
    worlds = tuple(worlds)
    if not worlds:
        raise ValueError('empty world family')
    for w in worlds:
        validate_world(w, size)
    rows = []
    for a, b, c in worlds:
        A, B, C = ({i for i in range(size) if m & (1 << i)} for m in (a,b,c))
        rows.append((all(x in A for x in B), all(x in B for x in C),
                     all(x in A for x in C), bool(A) and bool(B) and bool(C)))
    return {'actual_ab': rows[0][0], 'actual_bc': rows[0][1], 'actual_ac': rows[0][2],
            'necessary_ab': all(r[0] for r in rows), 'necessary_bc': all(r[1] for r in rows),
            'necessary_ac': all(r[2] for r in rows), 'all_terms_nonempty': all(r[3] for r in rows)}


def enumerate_models():
    counts = dict(models=0, nonempty_models=0, oracle_mismatches=0,
                  necessary_premise_models=0, necessity_preservation_failures=0,
                  actual_premise_models=0, actual_preservation_failures=0,
                  necessary_conclusion_contingent_route=0,
                  nonempty_necessary_conclusion_contingent_route=0,
                  nonnecessary_conclusion_both_necessary_premises=0)
    for flat in product(range(4), repeat=6):
        worlds = (flat[:3], flat[3:])
        r = evaluate(worlds)
        counts['models'] += 1
        counts['nonempty_models'] += int(r['all_terms_nonempty'])
        counts['oracle_mismatches'] += int(r != object_oracle(worlds))
        necessary_premises = r['necessary_ab'] and r['necessary_bc']
        actual_premises = r['actual_ab'] and r['actual_bc']
        counts['necessary_premise_models'] += int(necessary_premises)
        counts['necessity_preservation_failures'] += int(necessary_premises and not r['necessary_ac'])
        counts['actual_premise_models'] += int(actual_premises)
        counts['actual_preservation_failures'] += int(actual_premises and not r['actual_ac'])
        contingent_route = actual_premises and r['necessary_ac'] and not necessary_premises
        counts['necessary_conclusion_contingent_route'] += int(contingent_route)
        counts['nonempty_necessary_conclusion_contingent_route'] += int(contingent_route and r['all_terms_nonempty'])
        counts['nonnecessary_conclusion_both_necessary_premises'] += int(not r['necessary_ac'] and necessary_premises)
    return counts


def negative_models():
    """E(B,A), E(C,B), with all three terms nonempty, domain size 3.
    Record both truth values for all four directed C-to-A categorical claims.
    """
    counts = {'triples': 512, 'nonempty_two_negative_premise_models': 0,
              'conclusions': {k: {'true': 0, 'false': 0} for k in 'AEIO'}}
    for a,b,c in product(range(8), repeat=3):
        if not (a and b and c and none_of(b,a) and none_of(c,b)):
            continue
        counts['nonempty_two_negative_premise_models'] += 1
        vals = {'A': all_of(c,a), 'E': none_of(c,a), 'I': bool(c&a), 'O': bool(c&~a)}
        for k,v in vals.items():
            counts['conclusions'][k]['true' if v else 'false'] += 1
    return counts


def examples():
    # Masks 1={0}, 2={1}, 3={0,1}; B changes but A and C do not.
    disappearing = ((1,1,1), (1,2,1))
    contingent_conclusion = ((1,1,1), (0,1,1))
    return {'disappearing_bridge': {'worlds': disappearing, 'evaluation': evaluate(disappearing)},
            'actual_only_route': {'worlds': contingent_conclusion, 'evaluation': evaluate(contingent_conclusion)},
            'same_extension_different_explanation': {'worlds': ((1,1,1),(1,1,1)),
                'evaluation': evaluate(((1,1,1),(1,1,1))),
                'essential_or_causal_status': 'not represented; cannot be inferred'}}


def main():
    result = {'scope': '2 worlds, 2 objects; whole-proposition necessity; empty terms allowed and separately counted',
              'modal_enumeration': enumerate_models(), 'two_negative_enumeration': negative_models(),
              'examples': examples()}
    if result['modal_enumeration']['oracle_mismatches'] or result['modal_enumeration']['necessity_preservation_failures'] or result['modal_enumeration']['actual_preservation_failures']:
        raise RuntimeError('enumeration verification failed')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
