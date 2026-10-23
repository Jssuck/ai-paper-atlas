"""Independent reviewer oracle: object-wise quantifiers, not set-operation predicates."""
from itertools import product
from model import Model, proposition, classify, evaluate


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def q(rows, kind, s, p):
    witnesses = [row[p] for row in rows if row[s]]
    return {'A': all(witnesses), 'E': not any(witnesses),
            'I': any(witnesses), 'O': any(not x for x in witnesses)}[kind]


def category(rows, kind, s, p):
    w = [r[p] for r in rows if r[s]]
    truth = q(rows, kind, s, p)
    if kind in 'IO':
        return 'true' if truth else 'false'
    if not w:
        return 'vacuous_true'
    if truth:
        return 'true'
    return 'partly_false' if any(w) and not all(w) else 'wholly_false'


def run():
    count = checks = compressions = 0
    types = list(product((False, True), repeat=3))
    for n in range(1, 5):
        for rows in product(types, repeat=n):
            m = Model(frozenset(range(n)), *(frozenset(i for i,r in enumerate(rows) if r[j]) for j in range(3)))
            compressed = tuple(dict.fromkeys(rows))
            for s, p in product(range(3), repeat=2):
                for kind in 'AEIO':
                    expected = q(rows, kind, s, p)
                    require(proposition(m, kind, 'ABC'[s], 'ABC'[p]) == expected, 'Predicate mismatch')
                    require(classify(m, kind, 'ABC'[s], 'ABC'[p]) == category(rows, kind, s, p), 'Category mismatch')
                    require(q(compressed, kind, s, p) == expected, 'Compression truth mismatch')
                    require(category(compressed, kind, s, p) == category(rows, kind, s, p), 'Compression category mismatch')
                    checks += 1
                    compressions += 1
            expected_moods = {
                'Barbara': (q(rows,'A',1,0), q(rows,'A',2,1), q(rows,'A',2,0)),
                'Celarent': (q(rows,'E',1,0), q(rows,'A',2,1), q(rows,'E',2,0)),
                'Darii': (q(rows,'A',1,0), q(rows,'I',2,1), q(rows,'I',2,0)),
                'Ferio': (q(rows,'E',1,0), q(rows,'I',2,1), q(rows,'O',2,0))}
            for mood, expected in expected_moods.items():
                require(evaluate(m,mood)==expected, 'Mood mismatch')
                require(expected != (True,True,False), 'TTF')
            count += 1
    print('PASS labelled models (domain sizes 1..4):', count)
    print('PASS predicate + classification comparisons:', checks)
    print('PASS compression truth + classification comparisons:', compressions)
    print('PASS mood comparisons:', count*4)
    print('No TTF; independent oracle uses per-object quantifiers.')

if __name__ == '__main__':
    run()
