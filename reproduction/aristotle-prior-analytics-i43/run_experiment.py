"""Finite exhaustive checks; these counts are not a general proof."""
import json
from itertools import product
from model import Atom, And, Model, Certificate, powerset, verify_components
W,L,P = map(Atom,('W','L','P'))
D = And((L,P))
counts = dict(models=0, conjunction_equivalence=0, background_reduction=0,
              counterexample_equivalence=0, definition_two_directions=0,
              component_certificates=0, local_not_whole=0, inclusion_not_definition=0)
for n in range(5):
    u = tuple(range(n)); sets = tuple(powerset(u))
    for w,l,p in product(sets,repeat=3):
        m = Model(u,{'W':w,'L':l,'P':p}); counts['models'] += 1
        local = m.inclusion(W,P); full = m.inclusion(W,D); liquid = m.inclusion(W,L)
        if full != (liquid and local): raise RuntimeError('conjunction equivalence failed')
        counts['conjunction_equivalence'] += 1
        if liquid:
            if local != full: raise RuntimeError('background reduction failed')
            counts['background_reduction'] += 1
        if (not local) != bool(m.counterexamples(W,P)): raise RuntimeError('witness failed')
        counts['counterexample_equivalence'] += 1
        if m.definition(W,D) != (full and m.inclusion(D,W)): raise RuntimeError('definition failed')
        counts['definition_two_directions'] += 1
        certs=(Certificate(W,L),Certificate(W,P))
        if verify_components(m,W,D,certs) != full: raise RuntimeError('certificates failed')
        counts['component_certificates'] += 1
        counts['local_not_whole'] += local and not full
        counts['inclusion_not_definition'] += full and not m.definition(W,D)
print(json.dumps(counts,sort_keys=True,indent=2))
print('All finite checks passed. No general theorem or unique historical semantics is established by this run.')
