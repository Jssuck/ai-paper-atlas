"""Bounded proof-tree checker for I.29 teaching reconstructions; Python stdlib only.
Not a historical semantics or a complete theorem prover. No assert-based validation.
"""
from itertools import product
import re

class InvalidProof(ValueError):
    pass


def atom(value, allow_false=False):
    if not isinstance(value, (tuple, list)) or not value:
        raise InvalidProof('statement must be a tuple/list')
    op = value[0]
    arities = {'ALL': 2, 'NO': 2, 'SOME': 2, 'EX': 1}
    if allow_false:
        arities['FALSE'] = 0
    if not isinstance(op, str) or op not in arities or len(value) != 1 + arities[op]:
        raise InvalidProof('invalid statement kind or arity')
    for name in value[1:]:
        if not isinstance(name, str) or re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,31}', name) is None:
            raise InvalidProof('invalid term name')
    return tuple(value)


def holds(statement, model):
    """Evaluate strict extensional statements; empty terms are permitted."""
    s = atom(statement)
    if not isinstance(model, dict) or any(not isinstance(v, frozenset) for v in model.values()):
        raise InvalidProof('model values must be frozensets')
    if any(x not in model for x in s[1:]):
        raise InvalidProof('missing term')
    x = model[s[1]]
    if s[0] == 'EX':
        return bool(x)
    y = model[s[2]]
    return {'ALL': x <= y, 'NO': not x & y, 'SOME': bool(x & y)}[s[0]]


def node(rule, claim, *inputs, **extra):
    return dict(rule=rule, claim=claim, inputs=list(inputs), **extra)


def given(index, claim):
    return node('given', claim, index=index)


def assume(label, claim):
    return node('assume', claim, label=label)


def verify(proof, premises, expected):
    """Check every rule and lexical discharge. Return True or raise InvalidProof.

    Premises are trusted inputs, NOT facts authenticated against the world.
    max depth 64 and 10000 visited nodes make this a bounded checker.
    """
    if not isinstance(premises, (list, tuple)):
        raise InvalidProof('premises must be a sequence')
    base = tuple(atom(p) for p in premises)
    goal = atom(expected)
    visits = [0]

    def walk(p, scope, depth):
        visits[0] += 1
        if depth > 64 or visits[0] > 10000:
            raise InvalidProof('proof resource bound')
        if not isinstance(p, dict) or not isinstance(p.get('rule'), str):
            raise InvalidProof('invalid proof node')
        r = p['rule']
        extras = {'given': {'index'}, 'assume': {'label'}, 'raa': {'label', 'assumption'}}
        if set(p) != {'rule', 'claim', 'inputs'} | extras.get(r, set()):
            raise InvalidProof('unexpected or missing node field')
        c = atom(p['claim'], allow_false=True)
        if not isinstance(p['inputs'], list):
            raise InvalidProof('inputs must be a list')
        ins = p['inputs']
        if r == 'given':
            i = p['index']
            if ins or type(i) is not int or not 0 <= i < len(base) or c != base[i]:
                raise InvalidProof('invalid given')
            return c, frozenset()
        if r == 'assume':
            label = p['label']
            if ins or not isinstance(label, str) or label not in scope or c != scope[label]:
                raise InvalidProof('unbound or mismatched assumption')
            return c, frozenset([label])
        if r == 'raa':
            label = p['label']
            a = atom(p['assumption'])
            if (not isinstance(label, str) or not label or label in scope or len(ins) != 1
                    or c[0] not in ('NO', 'SOME')):
                raise InvalidProof('invalid RAA scope or goal')
            opposite = ('SOME' if c[0] == 'NO' else 'NO', *c[1:])
            if a != opposite:
                raise InvalidProof('RAA must assume exact contradictory target')
            out, deps = walk(ins[0], {**scope, label: a}, depth + 1)
            if out != ('FALSE',) or label not in deps:
                raise InvalidProof('RAA needs contradiction depending on its assumption')
            return c, deps - {label}
        outputs = [walk(q, scope, depth + 1) for q in ins]
        ss = [x[0] for x in outputs]
        deps = frozenset().union(*(x[1] for x in outputs))
        valid = False
        if r == 'all_trans' and len(ss) == 2:
            a, b = ss
            valid = a[0] == b[0] == 'ALL' and a[2] == b[1] and c == ('ALL', a[1], b[2])
        elif r == 'no_sym' and len(ss) == 1:
            a = ss[0]
            valid = a[0] == 'NO' and c == ('NO', a[2], a[1])
        elif r == 'no_sub' and len(ss) == 2:
            a, b = ss
            valid = a[0] == 'ALL' and b[0] == 'NO' and a[2] == b[1] and c == ('NO', a[1], b[2])
        elif r == 'some_map' and len(ss) == 2:
            a, b = ss
            valid = a[0] == 'SOME' and b[0] == 'ALL' and a[2] == b[1] and c == ('SOME', a[1], b[2])
        elif r == 'witness' and len(ss) == 2:
            a, b = ss
            valid = a[0] == 'EX' and b[0] == 'ALL' and a[1] == b[1] and c == ('SOME', a[1], b[2])
        elif r == 'some_sym' and len(ss) == 1:
            a = ss[0]
            valid = a[0] == 'SOME' and c == ('SOME', a[2], a[1])
        elif r == 'clash' and len(ss) == 2:
            a, b = ss
            valid = a[0] == 'SOME' and b == ('NO', *a[1:]) and c == ('FALSE',)
        if not valid:
            raise InvalidProof('rule/claim mismatch: ' + r)
        return c, deps

    result, deps = walk(proof, {}, 0)
    if result != goal or deps:
        raise InvalidProof('wrong final target or undischarged assumptions')
    return True


def examples():
    """Six certificates: both original examples direct/RAA, two only-bridges."""
    p1 = [('ALL','A','B'), ('NO','B','E')]
    ab, be = given(0,p1[0]), given(1,p1[1])
    direct1 = node('no_sub', ('NO','A','E'), ab, be)
    assumed1 = assume('h', ('SOME','A','E'))
    ea = node('some_sym', ('SOME','E','A'), assumed1)
    eb = node('some_map', ('SOME','E','B'), ea, ab)
    not_eb = node('no_sym', ('NO','E','B'), be)
    clash1 = node('clash', ('FALSE',), eb, not_eb)
    raa1 = node('raa', ('NO','A','E'), clash1, label='h', assumption=('SOME','A','E'))
    p2 = [('EX','G'), ('ALL','G','A'), ('ALL','G','E')]
    ex, ga, ge = [given(i,x) for i,x in enumerate(p2)]
    ga_some = node('witness', ('SOME','G','A'), ex, ga)
    ag = node('some_sym', ('SOME','A','G'), ga_some)
    ae = node('some_map', ('SOME','A','E'), ag, ge)
    direct2 = node('some_sym', ('SOME','E','A'), ae)
    no_ea = assume('h', ('NO','E','A'))
    no_ga = node('no_sub', ('NO','G','A'), ge, no_ea)
    clash2 = node('clash', ('FALSE',), ga_some, no_ga)
    raa2 = node('raa', ('SOME','E','A'), clash2, label='h', assumption=('NO','E','A'))
    p3 = [('ALL','E','G'), ('ALL','G','A')]
    direct3 = node('all_trans', ('ALL','E','A'), given(0,p3[0]), given(1,p3[1]))
    p4 = [('ALL','E','G'), ('NO','G','A')]
    direct4 = node('no_sub', ('NO','E','A'), given(0,p4[0]), given(1,p4[1]))
    return [('negative_direct',p1,('NO','A','E'),direct1),
            ('negative_raa',p1,('NO','A','E'),raa1),
            ('particular_direct',p2,('SOME','E','A'),direct2),
            ('particular_raa',p2,('SOME','E','A'),raa2),
            ('only_positive',p3,('ALL','E','A'),direct3),
            ('only_negative',p4,('NO','E','A'),direct4)]


def finite_report():
    exs = examples()
    for _, ps, goal, cert in exs:
        verify(cert, ps, goal)
    counts = {name: 0 for name, *_ in exs}
    checked = 0
    for n in range(1,4):
        sets = [frozenset(i for i in range(n) if mask >> i & 1) for mask in range(1 << n)]
        for vals in product(sets, repeat=4):
            model = dict(zip(('A','B','E','G'), vals))
            checked += 1
            for name, ps, goal, _ in exs:
                if all(holds(p,model) for p in ps):
                    counts[name] += 1
                    if not holds(goal,model):
                        raise RuntimeError('certificate countermodel')
    # Countermodels are pedagogical tests, not missing historical premises repaired silently.
    empty = dict(A=frozenset([0]), E=frozenset([1]), G=frozenset())
    positive = dict(A=frozenset([0]), E=frozenset([0,1]), G=frozenset([0]))
    negative = dict(A=frozenset([1]), E=frozenset([0,1]), G=frozenset([0]))
    if not (holds(('ALL','G','A'),empty) and holds(('ALL','G','E'),empty) and not holds(('SOME','E','A'),empty)):
        raise RuntimeError('empty counterexample failed')
    if not (holds(('ALL','G','A'),positive) and holds(('ALL','G','E'),positive) and not holds(('ALL','E','A'),positive)):
        raise RuntimeError('only positive counterexample failed')
    if not (holds(('NO','G','A'),negative) and holds(('ALL','G','E'),negative) and not holds(('NO','E','A'),negative)):
        raise RuntimeError('only negative counterexample failed')
    # Each possibility is at a different world; neither world has A contained in C.
    worlds = [dict(A=frozenset([0]), B=frozenset([0]), C=frozenset()),
              dict(A=frozenset([0]), B=frozenset(), C=frozenset())]
    modal = (any(holds(('ALL','A','B'),w) for w in worlds)
             and any(holds(('ALL','B','C'),w) for w in worlds)
             and not any(holds(('ALL','A','C'),w) for w in worlds))
    if not modal:
        raise RuntimeError('modal boundary failed')
    return {'models':checked,'certificates':len(exs),'premise_satisfying_models':counts,
            'counterexamples':3,'two_world_boundary':modal,
            'scope':'strict finite extensional checking; no general theorem proof or historical modal reconstruction'}

if __name__ == '__main__':
    import json
    print(json.dumps(finite_report(), indent=2, sort_keys=True))
