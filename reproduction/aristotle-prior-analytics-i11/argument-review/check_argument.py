"""Independent I.11 argument checks; no import from the teaching implementation."""
from itertools import product
import json

COUNT = 0

def check(value, label):
    global COUNT
    COUNT += 1
    if not value:
        raise RuntimeError(label)


def plain(kind, subject, predicate):
    vals = [x in predicate for x in subject]
    return {'A': all(vals), 'E': not any(vals), 'I': any(vals), 'O': not all(vals)}[kind]


def anchored(kind, subject_worlds, predicate_worlds):
    s = subject_worlds[0]
    stable = {x for x in (0, 1) if all(x in p for p in predicate_worlds)}
    possible = {x for x in (0, 1) if any(x in p for p in predicate_worlds)}
    if kind == 'A': return all(x in stable for x in s)
    if kind == 'E': return all(x not in possible for x in s)
    if kind == 'I': return any(x in stable for x in s)
    return any(x not in possible for x in s)


def necessary(kind, s, p, semantics):
    if semantics == 'anchored': return anchored(kind, s, p)
    return all(plain(kind, a, b) for a, b in zip(s, p))


def model(a0, b0, c0, a1, b1, c1):
    return ((set(a0), set(a1)), (set(b0), set(b1)), (set(c0), set(c1)))


def main():
    kinds = {'Darapti':'AAI', 'Felapton':'EAO', 'Disamis':'IAI', 'Datisi':'AII', 'Bocardo':'OAO', 'Ferison':'EIO'}
    subsets = [set(), {0}, {1}, {0,1}]
    failures = {(sem, mode, side):0 for sem in ('anchored','sentence') for mode in kinds for side in (0,1)}
    premises = dict.fromkeys(failures,0)
    models = 0
    for data in product(subsets, repeat=6):
        a,b,c = model(*data)
        models += 1
        for kind in 'AEIO':
            for s,p in ((a,b),(b,c),(c,a)):
                check(not anchored(kind,s,p) or plain(kind,s[0],p[0]), 'necessity entails actual')
        # Symmetric stable witness is symmetric, but anchored I need not be.
        fixed_ab = bool(a[0] & a[1] & b[0] & b[1])
        fixed_ba = bool(b[0] & b[1] & a[0] & a[1])
        check(fixed_ab == fixed_ba, 'stable witness symmetry')
        # Both inverse routes always produce the reverse anchored conclusion.
        if c[0] and plain('A',c[0],a[0]) and anchored('A',c,b):
            check(anchored('I',a,b), 'Darapti inverse direct route')
        if plain('I',c[0],a[0]) and anchored('A',c,b):
            check(anchored('I',a,b), 'Disamis inverse direct route')
        if not c[0]: continue
        for sem in ('anchored','sentence'):
            for mode, (major,minor,conclusion) in kinds.items():
                for side in (0,1):
                    left = necessary(major,c,a,sem) if side == 0 else plain(major,c[0],a[0])
                    right = necessary(minor,c,b,sem) if side == 1 else plain(minor,c[0],b[0])
                    if left and right:
                        key = sem,mode,side
                        premises[key] += 1
                        out = necessary(conclusion,b,a,sem)
                        failures[key] += not out
                        check(plain(conclusion,b[0],a[0]), 'actual third figure preserved')
                        if sem == 'anchored' and side == 0:
                            check(out, 'six major-necessary valid')
    check(models == 4096, 'model count')
    for key, n in failures.items():
        check(premises[key] > 0, 'nonvacuous configuration')
        check((n == 0) == (key[0] == 'anchored' and key[2] == 0), 'classification')
    # Main text one-object countermodels; C1 fixed here, as in the prose.
    a,b,c = model({0},{0},{0},set(),{0},{0})
    check(plain('A',c[0],a[0]) and anchored('A',c,b), '9.1 premises')
    check(anchored('I',a,b) and not anchored('I',b,a), '9.1 reverse failure')
    a,b,c = model(set(),{0},{0},{0},{0},{0})
    check(plain('E',c[0],a[0]) and anchored('A',c,b), '9.2 premises')
    check(plain('O',b[0],a[0]) and not anchored('O',b,a), '9.2 conclusion')
    # Moving witnesses are distinct from a fixed common object.
    a,b,c = model({0},{0},{0},{1},{1},{1})
    check(necessary('I',a,b,'sentence'), 'moving witness each world')
    check(not (a[0]&a[1]&b[0]&b[1]), 'no stable common witness')
    # Empty middle invalidates only universal-only existence routes.
    for major in ('A','E'):
        a,b,c = model(set(),set(),set(),set(),set(),set())
        check(anchored(major,c,a) and plain('A',c[0],b[0]), 'empty C premises')
        check(not anchored('I' if major == 'A' else 'O',b,a), 'empty C existential false')
    output = {'result':'PASS','models':models,'checks':COUNT,'classification':[{'semantics':s,'mode':m,'necessary_premise':'major' if side==0 else 'minor','satisfying_premises':premises[s,m,side],'failures':failures[s,m,side]} for s,m,side in failures], 'limits':'Finite model checks support independent review, not a proof for all domains/worlds or historical interpretation.'}
    print(json.dumps(output,ensure_ascii=False,indent=2))

if __name__ == '__main__': main()
