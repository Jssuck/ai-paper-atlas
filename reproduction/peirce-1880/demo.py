"""Small reproducible traces; execute from this directory with python demo.py."""
from peirce_finite import *


def run():
    print('1. Empty subjects (p23):', categorical(frozenset(), frozenset({0})))
    print('\n2. Eliminate x (p39-inspired modern reconstruction):')
    formula = normalize([clause('~a', 'x'), clause('~x', 'b')])
    projected, trace = eliminate(formula, 'x')
    print('input: ', format_cnf(formula))
    for step in trace:
        print('resolve:', step)
    print('output:', format_cnf(projected))

    print('\n3. Boole example: original p39 vs six premises p41 vs summary p42')
    original = cnf_from_truth_function(('v', 'x', 'y', 'z', 'w'), boole_original)
    projected, _ = eliminate(original, 'v')
    good, mismatches = [], []
    for env in assignments(('x', 'y', 'z', 'w')):
        row = ''.join(str(int(env[k])) for k in ('x', 'y', 'z', 'w'))
        if eval_cnf(projected, env):
            good.append(row)
        if eval_cnf(projected, env) != boole_printed_summary(env):
            mismatches.append(row)
    print('allowed xyzw:', ', '.join(good))
    print('p42 additionally admits:', ', '.join(mismatches))
    print('six p41 clauses:', format_cnf(boole_six_clauses()))

    print('\n4. All four operations (p52): same operands, different quantifiers')
    r = Relation(3, frozenset(((0, 0), (0, 1), (1, 1))))
    s = Relation(3, frozenset(((0, 2), (1, 2), (2, 0))))
    for operation in ('compose', 'regressive', 'progressive', 'transadd'):
        print(operation, sorted(getattr(r, operation)(s).pairs))
    print('Witnesses for compose at (0,2):', r.witnesses(s, 0, 2))

    print('\n5. Corrected classification (p47 + p57 Note), n=2')
    for name, relation in [('zero', Relation.zero(2)), ('identity', Relation.identity(2)),
                           ('diversity', ~Relation.identity(2)), ('top', Relation.top(2))]:
        print(name, ', '.join(k for k, v in relation.classify().items() if v))
    print('\n6. Equality patterns (p48):', equality_patterns(3))
    print('B0..B7:', bell_numbers(7))

    print('\n7. Intersection counterexample: two paths, no shared witness')
    r = Relation(3, frozenset(((0, 0), (0, 1))))
    s = Relation(3, frozenset(((0, 2),)))
    t = Relation(3, frozenset(((1, 2),)))
    print('R;(S & T):', sorted(r.compose(s & t).pairs))
    print('(R;S) & (R;T):', sorted((r.compose(s) & r.compose(t)).pairs))
    print('separate witness sets:', r.witnesses(s, 0, 2), r.witnesses(t, 0, 2))

    print('\n8. Mixed operations are not automatically associative')
    a, b, c = Relation.top(2), Relation.identity(2), Relation.top(2)
    print('(A reg B);C:', sorted(a.regressive(b).compose(c).pairs))
    print('A reg (B;C):', sorted(a.regressive(b.compose(c)).pairs))
    print('\nThese are bounded finite checks, not a proof of all 1880 formulae.')


if __name__ == '__main__':
    run()
