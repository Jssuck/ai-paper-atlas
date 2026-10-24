"""Independent auditor: enumerate actual nonempty subsets of a four-object universe."""
import itertools
import json
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import syllogism

U = frozenset(range(4))
subsets = [frozenset(c) for n in range(1, 5) for c in itertools.combinations(U, n)]

def truth(k, x, y):
    if k == 'A': return all(e in y for e in x)
    if k == 'E': return all(e not in y for e in x)
    if k == 'I': return any(e in y for e in x)
    if k == 'O': return any(e not in y for e in x)
    raise ValueError(k)

relations = {1: lambda s,m,p: ((m,p),(s,m)),
             2: lambda s,m,p: ((p,m),(s,m)),
             3: lambda s,m,p: ((m,p),(m,s))}
valid = {str(f): [] for f in relations}
checked = 0
for f, relation in relations.items():
    for letters in itertools.product('AEIO', repeat=3):
        mood = ''.join(letters)
        models = 0
        bad = 0
        for s,m,p in itertools.product(subsets, repeat=3):
            major, minor = relation(s,m,p)
            if truth(letters[0],*major) and truth(letters[1],*minor):
                models += 1
                bad += not truth(letters[2],s,p)
        if not models: raise RuntimeError(('vacuous',f,mood))
        actual = bad == 0
        production = syllogism.check(f,mood)
        if actual != production['valid']: raise RuntimeError(('disagreement',f,mood))
        if actual: valid[str(f)].append(mood)
        else:
            support = production['first_countermodel']
            terms = [frozenset(t for t in support if t & b) for b in (1,2,4)]
            major,minor = relation(*terms)
            if not (all(terms) and truth(letters[0],*major) and truth(letters[1],*minor) and not truth(letters[2],terms[0],terms[2])):
                raise RuntimeError(('bad witness',f,mood))
        checked += 1
print(json.dumps({'method':'actual nonempty subsets of four objects; separate quantified set predicates',
                  'set_assignments_per_candidate':15**3, 'candidates':checked,
                  'candidate_model_evaluations':checked*15**3,
                  'valid_moods':valid, 'validated_returned_countermodels':174,
                  'agreement':True, 'scope':'bounded independent cross-check, not a proof of arbitrary-domain validity'},indent=2))
