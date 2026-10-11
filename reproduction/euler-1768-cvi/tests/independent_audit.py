"""Separately authored audit: constructs Boolean profiles and explicit class sets.

Run: python3 tests/independent_audit.py
This file intentionally does not use the production support decoder or evaluator
for its reference models. No external package, filesystem mutation, or network.
"""
import sys
from itertools import combinations, product
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import syllogisms as s
TERMS = ('P','Q','M')
MOODS = ('A','E','I','O')
FIG = {1: (('M','Q'),('P','M')), 2: (('Q','M'),('P','M')), 3: (('M','Q'),('M','P')), 4: (('Q','M'),('M','P'))}
def powerset(xs):
    return [frozenset(c) for n in range(len(xs)+1) for c in combinations(xs,n)]
def holds(m,a,b):
    return {'A': a <= b, 'E': not (a & b), 'I': bool(a & b), 'O': bool(a - b)}[m]
profiles = list(product((False,True), repeat=3))
models = [{t: frozenset(a for a in occ if a[i]) for i,t in enumerate(TERMS)} for occ in powerset(profiles) if occ]
regimes = powerset(TERMS)
forms = [(f, ''.join(m)) for f in FIG for m in product(MOODS, repeat=3)]
valid = {}
max_witness = 0
invalid_sizes = Counter()
for required in regimes:
    relevant = [c for c in models if all(c[t] for t in required)]
    assert len(relevant) == len(s.models_with(required))
    valid[required] = set()
    for f,m in forms:
        maj,minor=FIG[f]
        premise_models = [c for c in relevant if holds(m[0], c[maj[0]], c[maj[1]]) and holds(m[1], c[minor[0]], c[minor[1]])]
        countermodels = [c for c in premise_models if not holds(m[2], c['P'], c['Q'])]
        out=s.check_form(f,m,required)
        assert out['valid'] == (not countermodels), (f,m,required)
        assert len(premise_models) == out['premise_models']
        assert len(countermodels) == out['countermodel_count']
        if countermodels:
            # The all-empty profile is not in any class; recover occupied profile cardinality
            # from s's certificate only for the certificate itself. True minimality below
            # independently enumerates all labelled domains of sizes 1, 2, and 3.
            cert=out['countermodel']; c={t:set(cert['classes'][t]) for t in TERMS}
            assert all(c[t] for t in required)
            assert holds(m[0],c[maj[0]],c[maj[1]]) and holds(m[1],c[minor[0]],c[minor[1]])
            assert not holds(m[2],c['P'],c['Q'])
            n=len(cert['domain']); max_witness=max(max_witness,n); invalid_sizes[n]+=1
            for k in range(1,n):
                subs=powerset(list(range(k)))
                for p,q,mid in product(subs,repeat=3):
                    d={'P':p,'Q':q,'M':mid}
                    assert not (all(d[t] for t in required) and holds(m[0],d[maj[0]],d[maj[1]]) and holds(m[1],d[minor[0]],d[minor[1]]) and not holds(m[2],p,q)), (f,m,required,n,k)
        else:
            valid[required].add((f,m))
for f,m in forms:
    sufficient=[a for a in regimes if (f,m) in valid[a]]
    expected={a for a in sufficient if not any(b<a for b in sufficient)}
    actual={frozenset(a) for a in s.minimal_existence_assumptions(f,m)}
    assert actual == expected, (f,m,actual,expected)
# Change transcription data in memory only; independently computed answers must not change.
old=s.EULER_LIST
s.EULER_LIST={}
assert set(s.valid_forms()) == valid[frozenset()]
assert set(s.valid_forms(TERMS)) == valid[frozenset(TERMS)]
assert len(s.nonweakened_valid_forms(TERMS)) == 19
s.EULER_LIST=old
assert len(models) == 255
assert len([c for c in models if all(c.values())]) == 218
print('Independent 255-model set oracle: all 2048 form/regime checks, premise counts, countermodel counts and certificate truths PASS')
print('Independent minima for all 256 forms PASS')
print('Direct labelled-domain countermodel minimality PASS; maximum certificate size:', max_witness, '; histogram:', dict(invalid_sizes))
print('Valid counts by assumptions:', {''.join(t for t in TERMS if t in a) or 'none':len(valid[a]) for a in regimes})
print('Source-transcription deletion leaves validity counts 15/24/nonweakened19 unchanged: PASS')
print('Existence-dependent valid forms and inclusion-minimal assumptions:', [(f,m,s.minimal_existence_assumptions(f,m)) for f,m in forms if (f,m) in valid[frozenset(TERMS)]-valid[frozenset()]])
