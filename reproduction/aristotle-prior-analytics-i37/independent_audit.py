"""Independent bit-vector oracle; checks stay active under -O and -OO.

No production extension/includes/some call supplies an expected value.
Finite regression evidence only, not a general mathematical proof.
"""
import itertools
import json
from model import Atom, And, Not, Model, chain_certificate


def require(value, message):
    if not value:
        raise RuntimeError(message)


def rejected(kind, call):
    try:
        call()
    except kind:
        return
    raise RuntimeError('expected rejection: ' + kind.__name__)


def main():
    atoms = (Atom('P', 'quality', 'u'), Atom('Q', 'quality', 'u'),
             Atom('P', 'quality', 't'), Atom('P', 'relation', 'u'))
    expressions = list(atoms)
    # Oracle expressions are separate functions of integer masks.
    oracles = [lambda vals, full, i=i: vals[i] for i in range(4)]
    for i in range(4):
        expressions.append(Not(atoms[i]))
        oracles.append(lambda v, f, i=i: f ^ v[i])
    for i, j in itertools.product(range(4), repeat=2):
        expressions.append(And(atoms[i], atoms[j]))
        oracles.append(lambda v, f, i=i, j=j: v[i] & v[j])
    expressions += [Not(And(atoms[0], atoms[1])),
                    And(Not(atoms[0]), Not(atoms[1])),
                    Not(Not(atoms[0])),
                    And(Not(And(atoms[0], atoms[1])), atoms[2])]
    oracles += [lambda v, f: f ^ (v[0] & v[1]),
                lambda v, f: (f ^ v[0]) & (f ^ v[1]),
                lambda v, f: v[0],
                lambda v, f: (f ^ (v[0] & v[1])) & v[2]]
    counts = dict(models=0, expression_comparisons=0, existence_comparisons=0,
                  inclusion_comparisons=0, true_chain_instances=0,
                  intersection_distribution_instances=0,
                  certificate_shapes=0, rejected_inputs=0, concrete_checks=0)
    for n in range(4):
        full = (1 << n) - 1
        for vals in itertools.product(range(1 << n), repeat=4):
            expected = [fn(vals, full) for fn in oracles]
            m = Model(range(n), {a: [x for x in range(n) if vals[i] >> x & 1]
                                  for i, a in enumerate(atoms)})
            counts['models'] += 1
            for e, bits in zip(expressions, expected):
                want = frozenset(x for x in range(n) if bits >> x & 1)
                require(m.extension(e) == want, 'extension vs independent bits')
                require(m.some(e) == (bits != 0), 'some vs independent bits')
                counts['expression_comparisons'] += 1
                counts['existence_comparisons'] += 1
            for i, j in itertools.product(range(4), repeat=2):
                require(m.includes(atoms[i], atoms[j]) == ((vals[i] & ~vals[j]) == 0),
                        'inclusion vs independent bits')
                counts['inclusion_comparisons'] += 1
            for i, j, k in itertools.product(range(4), repeat=3):
                if vals[i] & ~vals[j] == 0 and vals[j] & ~vals[k] == 0:
                    require(m.includes(atoms[i], atoms[k]), 'true-premise chain')
                    counts['true_chain_instances'] += 1
                require(m.includes(atoms[i], And(atoms[j], atoms[k])) ==
                        ((vals[i] & ~vals[j] == 0) and (vals[i] & ~vals[k] == 0)),
                        'universal intersection distribution')
                counts['intersection_distribution_instances'] += 1
    edges = list(itertools.product(range(4), repeat=2))
    for first, second, conclusion in itertools.product(edges, repeat=3):
        want = first[1] == second[0] and conclusion == (first[0], second[1])
        got = chain_certificate(tuple(atoms[i] for i in first),
                                tuple(atoms[i] for i in second),
                                tuple(atoms[i] for i in conclusion))
        require(got == want, 'exact certificate shape')
        counts['certificate_shapes'] += 1
    p, q, t, rel = atoms
    bad = [
        (ValueError, lambda: Atom('', 'x', 'u')),
        (ValueError, lambda: Atom('P', '', 'u')),
        (ValueError, lambda: Atom('P', 'x', ' ')),
        (ValueError, lambda: Atom(None, 'x', 'u')),
        (ValueError, lambda: Model({0}, {p: {1}})),
        (TypeError, lambda: Model({0}, {'P': {0}})),
        (KeyError, lambda: Model({0}, {}).extension(p)),
        (KeyError, lambda: Model({0}, {}).extension(Not(p))),
        (TypeError, lambda: Model({0}, {}).extension('P')),
        (TypeError, lambda: Model({0}, {}).extension(And('P', q))),
        (TypeError, lambda: Model({0}, {}).extension(Not(None))),
    ]
    for invalid in [None, (p,), [p, q], ('P', q), (And(p, q), q), (p, q, t)]:
        bad.append((TypeError, lambda invalid=invalid:
                    chain_certificate(invalid, (q, t), (p, t))))
    for kind, call in bad:
        rejected(kind, call)
        counts['rejected_inputs'] += 1
    # Concrete countermodels and boundary checks, each with explicit expected sets.
    m = Model({0}, {p: set(), q: set(), t: {0}, rel: {0}})
    require(m.some(t) and not m.some(p), 'aspect deletion countermodel')
    require(m.some(rel) and not m.some(p), 'category erasure countermodel')
    m = Model({0}, {p: {0}, q: set(), t: {0}, rel: {0}})
    require(m.some(Not(And(p, q))) and not m.some(Not(p)), 'negation not first')
    require(m.some(t) and m.some(p), 'non-entailment not negative entailment')
    m = Model({0}, {p: set(), q: {0}})
    require(m.some(Not(And(p, q))) and not m.some(Not(q)), 'negation not second')
    m = Model({0, 1}, {p: {0}, q: {1}})
    require(m.some(p) and m.some(q) and not m.some(And(p, q)), 'split witnesses')
    m = Model(set(), {p: set(), q: set()})
    require(m.includes(p, q) and not m.some(q), 'vacuity not existence')
    m = Model({0}, {p: {0}, q: set(), t: {0}, rel: {0}})
    require(chain_certificate((p, t), (t, q), (p, q)) and not m.includes(t, q),
            'shape alone not truth')
    m = Model({0}, {p: {0}, q: {0}, t: {0}, rel: {0}})
    require(not chain_certificate((p, t), (q, rel), (p, rel)) and m.includes(p, rel),
            'rejected certificate may have true conclusion')
    require(chain_certificate((p, t), (t, rel), (p, rel)),
            'explicit cross-label inclusion edges allowed')
    counts['concrete_checks'] = 10
    print(json.dumps({'status': 'PASS', 'counts': counts,
                      'oracle': 'independent integer masks, no production evaluator for expected values',
                      'limits': 'finite selected-expression checks, not a theorem or historical interpretation proof'},
                     indent=2))


if __name__ == '__main__':
    main()
