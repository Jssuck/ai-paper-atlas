"""Independent direct-quantifier checks for the I.9 teaching argument.
No imports of the author's model or test implementation.
"""
import itertools
import json

CHECKS = 0

def check(value):
    global CHECKS
    CHECKS += 1
    if not value:
        raise RuntimeError('independent argument check failed')

def q(kind, s, p):
    if kind == 'A': return all(x in p for x in s)
    if kind == 'E': return all(x not in p for x in s)
    if kind == 'I': return any(x in p for x in s)
    if kind == 'O': return any(x not in p for x in s)
    raise ValueError(kind)

def n(kind, s, p):
    pos = lambda x: all(x in pw for pw in p)
    neg = lambda x: all(x not in pw for pw in p)
    if kind == 'A': return all(pos(x) for x in s[0])
    if kind == 'E': return all(neg(x) for x in s[0])
    if kind == 'I': return any(pos(x) for x in s[0])
    if kind == 'O': return any(neg(x) for x in s[0])
    raise ValueError(kind)

def dd(kind, s, p):
    return all(q(kind, sw, pw) for sw, pw in zip(s,p))

def run():
    subsets = [frozenset(x for x in range(2) if mask & (1 << x)) for mask in range(4)]
    trajectories = list(itertools.product(subsets, repeat=2))
    modes = [('Barbara','A','A','A'),('Celarent','E','A','E'),('Darii','A','I','I'),('Ferio','E','I','O')]
    rows = []
    for name,major,minor,conclusion in modes:
        for position in ('major','minor'):
            counts = {'mood': name, 'necessary_position': position, 'premise_models':0, 'necessary_failures':0, 'actual_failures':0}
            for s,m,p in itertools.product(trajectories,repeat=3):
                premises = (n(major,m,p) and q(minor,s[0],m[0])) if position == 'major' else (q(major,m[0],p[0]) and n(minor,s,m))
                if not premises: continue
                counts['premise_models'] += 1
                necessary = n(conclusion,s,p)
                actual = q(conclusion,s[0],p[0])
                counts['necessary_failures'] += not necessary
                counts['actual_failures'] += not actual
                check(actual)
                if position == 'major': check(necessary)
            check(counts['premise_models'] > 0)
            check(counts['necessary_failures'] == 0 if position == 'major' else counts['necessary_failures'] > 0)
            rows.append(counts)
    # N entails its corresponding actual proposition, for every kind and pair.
    for s,p in itertools.product(trajectories,repeat=2):
        for kind in 'AEIO': check(not n(kind,s,p) or q(kind,s[0],p[0]))
    a,b=frozenset({0}),frozenset({1}); empty=frozenset(); both=a|b
    # Four one-object countermodels with nonempty actual S and M.
    s=m=(a,a)
    for name,major,minor,conclusion in modes:
        p=(a,empty) if major=='A' else (empty,a)
        check(q(major,m[0],p[0]) and n(minor,s,m) and not n(conclusion,s,p))
        # Add spectator b to P in both worlds: all three term extensions nonempty.
        p=tuple(pw|b for pw in p)
        check(q(major,m[0],p[0]) and n(minor,s,m) and not n(conclusion,s,p))
    # Both directions of non-equivalence in section 3.3.
    s=p=(a,empty); check(dd('A',s,p) and not n('A',s,p))
    s=(a,both);p=(a,a);check(n('A',s,p) and not dd('A',s,p))
    # The de-dicto-major/actual-minor failure from section 9.
    s=(a,a);m=p=(a,empty)
    check(dd('A',m,p) and q('A',s[0],m[0]) and not dd('A',s,p))
    # N_E conversion failure: current P may enter future S.
    s=(a,both);p=(b,b)
    check(n('E',s,p) and not n('E',p,s))
    # Owen printed negative minor: constant trajectories guarantee N_O.
    s=(a,a);m=(b,b);p=(a,a)
    check(q('E',m[0],p[0]) and n('O',s,m) and not q('O',s[0],p[0]))
    # The section 7 existential bridge, explicitly requiring nonempty S0.
    for s,m,p in itertools.product(trajectories,repeat=3):
        if s[0] and n('A',s,m):
            check(not n('A',s,p) or n('I',m,p))
            check(not n('E',s,p) or n('O',m,p))
    return {'status':'PASS','checks':CHECKS,'models_per_mood_position':4096,'rows':rows,
            'limits':'Finite independent checks do not replace the general subset and witness proofs; not a historical semantic completeness claim.'}

if __name__ == '__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
