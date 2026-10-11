"""Independent reviewer oracle: object tuples and explicit quantification.
Run from reproduction/euler-1768-cvii: python independent-review/audit.py
No production truth function is used to derive an expected result.
"""
from itertools import product, combinations
from pathlib import Path
import hashlib
import importlib.util
import json
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('subject_under_review', ROOT / 'euler_cvii.py')
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)
# Each individual is a tuple (P, Q, M). Define templates independently.
figures = {1: ((2, 1), (0, 2)), 2: ((1, 2), (0, 2)),
           3: ((2, 1), (2, 0)), 4: ((1, 2), (2, 0))}
forms = [''.join(x) + str(f) for f in range(1, 5) for x in product('AEIO', repeat=3)]
types = list(product((False, True), repeat=3))

def truth(model, mood, s, p):
    if mood == 'A': return all(not person[s] or person[p] for person in model)
    if mood == 'E': return all(not (person[s] and person[p]) for person in model)
    if mood == 'I': return any(person[s] and person[p] for person in model)
    if mood == 'O': return any(person[s] and not person[p] for person in model)
    raise ValueError(mood)

def argument(model, f):
    a, b = figures[int(f[-1])]
    return (truth(model, f[0], *a), truth(model, f[1], *b), truth(model, f[2], 0, 1))

def encode(model):
    return sum(2 ** (int(p) + 2 * int(q) + 4 * int(m)) for p, q, m in model)

def nonempty(model):
    return all(any(person[j] for person in model) for j in range(3))

models = [m for n in range(1, 9) for m in combinations(types, n)]
models.sort(key=lambda m: (len(m), encode(m)))
assert len(models) == 255
assert len([m for m in models if nonempty(m)]) == 218
assert tuple(forms) == e.all_forms()
expected = {}
checked_truths = 0
for required in (False, True):
    allowed = [m for m in models if not required or nonempty(m)]
    assert tuple(map(encode, allowed)) == e.supports(required)
    results = {}
    for f in forms:
        candidates = []
        for m in allowed:
            t = argument(m, f)
            assert e.argument_truth(encode(m), f) == t, (f, m)
            checked_truths += 1
            if t == (True, True, False): candidates.append(m)
        cm = min(candidates, key=lambda m: (len(m), encode(m))) if candidates else None
        result = None if cm is None else encode(cm)
        assert e.minimum_countermodel(f, required) == result, (f, required)
        if cm is not None:
            record = e.countermodel_record(result)
            assert record['cardinality'] == len(cm)
            reconstructed = tuple(tuple(i in record['extensions'][x] for x in ('P','Q','M'))
                                  for i in range(record['cardinality']))
            assert argument(reconstructed, f) == (True, True, False)
            assert not required or nonempty(reconstructed)
            assert set(reconstructed) == set(cm)
        results[f] = result
    expected[required] = results

# Independently phrase syntactic exclusions, including their intended scope.
rules = ['two_negative','two_particular','negative_conclusion','particular_conclusion','affirmative_conclusion']
counts = dict.fromkeys(rules, 0)
survivors = []
for f in forms:
    a,b,c = f[:3]
    flags = [a in {'E','O'} and b in {'E','O'},
             a in {'I','O'} and b in {'I','O'},
             (a in {'E','O'} or b in {'E','O'}) and c in {'A','I'},
             (a in {'I','O'} or b in {'I','O'}) and c in {'A','E'},
             a in {'A','I'} and b in {'A','I'} and c in {'E','O'}]
    bad = tuple(name for name, flag in zip(rules, flags) if flag)
    assert e.violations(f) == bad
    if not bad: survivors.append(f)
    for name in bad:
        counts[name] += 1
        assert all(expected[r][f] is not None for r in (False, True))
assert list(counts.values()) == [64,64,96,96,32]
assert len(survivors) == 48

# Native labeled universes allow duplicate membership types: independent check
# of compression, truth, and minimum cardinality for every invalid form.
native_min = {r: {} for r in (False,True)}
native_assignments = 0
for n in range(1,4):
    for m in product(types, repeat=n):
        native_assignments += 1
        for f in forms:
            if argument(m,f) == (True,True,False):
                native_min[False].setdefault(f,n)
                if nonempty(m): native_min[True].setdefault(f,n)
for r in (False,True):
    assert set(native_min[r]) == {f for f,c in expected[r].items() if c is not None}
    for f,n in native_min[r].items(): assert n == expected[r][f].bit_count()

singletons = []
native_truths = 0
for n in range(1,5):
    subsets = list(product((False,True), repeat=n))
    out = dict(n=n, assignments=0, premise_pairs_true=0, counterexamples=0,
               A_I_disagreements=0, E_O_disagreements=0)
    for p,q in product(subsets,repeat=2):
        model = tuple(zip(p,q))
        for mood in 'AEIO':
            got = e.native_holds(n,mood,sum(2**i for i,x in enumerate(p) if x),
                                sum(2**i for i,x in enumerate(q) if x))
            assert got == truth(model,mood,0,1)
            native_truths += 1
        for named in range(n):
            out['assignments'] += 1
            with_name = tuple((i == named,p[i],q[i]) for i in range(n))
            out['A_I_disagreements'] += truth(with_name,'A',0,1) != truth(with_name,'I',0,1)
            out['E_O_disagreements'] += truth(with_name,'E',0,1) != truth(with_name,'O',0,1)
            if truth(with_name,'A',0,1) and truth(with_name,'A',0,2):
                out['premise_pairs_true'] += 1
                out['counterexamples'] += not truth(with_name,'I',1,2)
    assert out == e.singleton_counts(n)
    assert out['assignments'] == n * 4**n
    assert out['premise_pairs_true'] == n * 4**(n-1)
    singletons.append(out)
assert argument(((True,False,True),(False,True,True)), 'III3') == (True,True,False)
assert truth(((False,False,False),),'A',0,1)
assert truth(((False,False,False),),'A',0,2)
assert not truth(((False,False,False),),'I',1,2)

# Invalid-input behavior, independently selected boundary/type cases.
guards = 0
def rejects(fn,*args):
    global guards
    try: fn(*args)
    except ValueError: guards += 1
    else: raise AssertionError((fn.__name__,args))
for bad in (None,True,False,0,-1,256,999,1.0,'1',[],{}):
    rejects(e.cells,bad)
    rejects(e.holds,bad,'A','P','Q')
    if bad is not None: rejects(e.countermodel_record,bad)
for bad in (None,True,1,[],{},'', 'AAA0','AAA5','AAA11','aaa1','AA 1','XAI1'):
    for fn in (e.validate_form,e.violations,e.minimum_countermodel): rejects(fn,bad)
    rejects(e.argument_truth,1,bad)
for bad in (None,1,True,[],{},'', 'AE','a','X'):
    rejects(e.holds,1,bad,'P','Q'); rejects(e.native_holds,1,bad,0,0)
for bad in (None,1,True,[],{},'', 'S','p'):
    rejects(e.holds,1,'A',bad,'Q'); rejects(e.holds,1,'A','P',bad)
for bad in (None,0,1,2,'false',[],{}):
    rejects(e.supports,bad); rejects(e.minimum_countermodel,'AAA1',bad)
for bad in (None,True,0,-1,17,1.0,'1',[]): rejects(e.native_holds,bad,'A',0,0)
for bad in (None,True,-1,2,1.0,'1',[]):
    rejects(e.native_holds,1,'A',bad,0); rejects(e.native_holds,1,'A',0,bad)
for bad in (None,True,0,5,1.0,'1',[]): rejects(e.singleton_counts,bad)
assert e.countermodel_record(None) is None

runs = [subprocess.check_output([sys.executable,str(ROOT/'euler_cvii.py')]) for _ in range(2)]
assert runs[0] == runs[1] == (ROOT/'results.json').read_bytes()
saved = json.loads(runs[0])
summary = {}
for r,key in ((False,'modern'),(True,'all_terms_nonempty')):
    valid = [f for f,c in expected[r].items() if c is None]
    invalid = [f for f in survivors if expected[r][f] is not None]
    actual = saved['regimes'][key]
    assert actual['valid_forms'] == valid
    assert actual['valid_count'] == len(valid)
    assert actual['filter_survivors'] == len(survivors)
    assert actual['surviving_invalid_count'] == len(invalid)
    assert set(actual['surviving_invalid_countermodels']) == set(invalid)
    for f in invalid:
        assert actual['surviving_invalid_countermodels'][f] == e.countermodel_record(expected[r][f])
    for rule in rules:
        assert actual['per_rule'][rule] == {'violating_forms':counts[rule],'valid_violating_forms':0}
    summary[key] = dict(valid_count=len(valid), valid_forms=valid, invalid_count=256-len(valid),
                        filter_survivors=48, surviving_invalid_count=len(invalid),
                        maximum_minimum_countermodel_size=max(native_min[r].values()),
                        all_form_countermodels=expected[r])
assert saved['singular_names']['shared_singleton_exhaustion'] == singletons
output = dict(status='PASS', python=platform.python_version(), implementation=platform.python_implementation(),
              platform=platform.platform(), form_regime_decisions=512, argument_truth_comparisons=checked_truths,
              native_labeled_assignments=native_assignments, native_truth_comparisons=native_truths,
              invalid_input_cases=guards, per_rule_violations=counts, singleton_results=singletons,
              results_sha256=hashlib.sha256(runs[0]).hexdigest(), regimes=summary)
(ROOT/'independent-review'/'audit-results.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in output.items() if k not in ('regimes',)},ensure_ascii=False,indent=2))
print('All 512 decisions, all 473 invalid-form minimum witnesses, filters, singleton cases, guards, and byte determinism PASS.')
