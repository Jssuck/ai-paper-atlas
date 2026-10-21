"""Explicit modern finite modal teaching model; not historical semantics."""
from itertools import product
import json
from pathlib import Path

TERMS = ('A', 'B', 'C')
TAGS = ('D', 'N', 'P', 'C')
MOODS = {'Barbara': ('A', 'A', 'A'), 'Celarent': ('E', 'A', 'E'),
         'Darii': ('A', 'I', 'I'), 'Ferio': ('E', 'I', 'O')}

def validate(model, n=2):
    if type(n) is not int or n < 1:
        raise ValueError('domain size must be a positive integer')
    if type(model) is not tuple or not model:
        raise ValueError('model must be a nonempty tuple of worlds')
    for world in model:
        if type(world) is not tuple or len(world) != 3:
            raise ValueError('each world must be a tuple of three masks')
        if any(type(m) is not int or not 0 <= m < 2**n for m in world):
            raise ValueError('invalid predicate mask')
    return model

def categorical(world, kind, subject, predicate, n=2):
    validate((world,), n)
    if kind not in ('A', 'E', 'I', 'O') or type(kind) is not str:
        raise ValueError('invalid categorical kind')
    if type(subject) is not str or subject not in TERMS or type(predicate) is not str or predicate not in TERMS:
        raise ValueError('invalid term')
    s, p = world[TERMS.index(subject)], world[TERMS.index(predicate)]
    if kind == 'A': return (s & p) == s
    if kind == 'E': return (s & p) == 0
    if kind == 'I': return (s & p) != 0
    return (s & p) != s

def modal(model, tag, kind, subject, predicate, n=2):
    validate(model, n)
    if type(tag) is not str or tag not in TAGS:
        raise ValueError('invalid modal tag')
    values = tuple(categorical(w, kind, subject, predicate, n) for w in model)
    if tag == 'D': return values[0]
    if tag == 'N': return all(values)
    if tag == 'P': return any(values)
    return any(values) and not all(values)

def models():
    for x in product(range(4), repeat=6):
        yield (x[:3], x[3:])

def reference(model, tag, kind, subject, predicate):
    """Separate element-wise reference implementation for tests."""
    values = []
    for world in model:
        pairs = [(bool(world[TERMS.index(subject)] & (1 << i)),
                  bool(world[TERMS.index(predicate)] & (1 << i))) for i in range(2)]
        if kind == 'A': v = all(not s or p for s,p in pairs)
        elif kind == 'E': v = all(not s or not p for s,p in pairs)
        elif kind == 'I': v = any(s and p for s,p in pairs)
        else: v = any(s and not p for s,p in pairs)
        values.append(v)
    return {'D': values[0], 'N': all(values), 'P': any(values),
            'C': True in values and False in values}[tag]

def report():
    rows=[]
    all_models=list(models())
    for name,(major,minor,conclusion) in MOODS.items():
        # Major: B -> A; minor: C -> B; conclusion: C -> A.
        caches = [{tag: [modal(m,tag,k,s,p) for m in all_models] for tag in TAGS}
                  for k,s,p in [(major,'B','A'),(minor,'C','B'),(conclusion,'C','A')]]
        for left,right,out in product(TAGS,TAGS,('D','N','P')):
            sat=[i for i in range(4096) if caches[0][left][i] and caches[1][right][i]]
            bad=[i for i in sat if not caches[2][out][i]]
            nonempty=[i for i in sat if all(mask for world in all_models[i] for mask in world)]
            bad_nonempty=[i for i in nonempty if not caches[2][out][i]]
            rows.append(dict(mood=name,major=left,minor=right,conclusion=out,
                             satisfying=len(sat),countermodels=len(bad),
                             first_countermodel=all_models[bad[0]] if bad else None,
                             nonempty_satisfying=len(nonempty),nonempty_countermodels=len(bad_nonempty)))
    incompatible=((1,1,2),(1,2,2))
    weakening=((1,1,1),(1,1,1))
    mixed=((1,1,1),(1,1,2))
    return dict(scope='Modern constant-domain two-world sentence modal model; finite tests are not general proofs',
                domain_size=2,worlds=2,actual_world=0,model_count=4096,
                configurations=len(rows),empty_predicates_allowed=True,
                all_predicates_nonempty_subset='3**6 = 729 models',
                cases={'incompatible_possible_and_contingent': incompatible,
                       'necessary_premises_have_actual_conclusion':weakening,
                       'mixed_actual_but_not_necessary_conclusion':mixed},rows=rows)

if __name__ == '__main__':
    result=report()
    Path('results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'models':result['model_count'],'configurations':result['configurations'],
                      'valid_configurations':sum(r['countermodels']==0 for r in result['rows'])}))
