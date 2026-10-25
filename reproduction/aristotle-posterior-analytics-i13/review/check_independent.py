"""Reviewer check using closed-form counts and an explicit response table.
Does not import the author's test suite or reuse its equation-solving oracle.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from fractions import Fraction
import subprocess
import sys
from datetime import datetime, timezone
from itertools import product

base = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
print('UTC:', datetime.now(timezone.utc).isoformat(timespec='seconds'))
print('Python:', sys.version.splitlines()[0])
print('Dependencies: Python standard library only')
spec = importlib.util.spec_from_file_location('reviewed_model', base / 'model.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def equal(actual, expected, label):
    if actual != expected:
        raise RuntimeError(f'{label}: {actual!r} != {expected!r}')

n = 3
expected_counts = {
    'universe_size': n,
    'triples': 8 ** n,
    'fact_chain_premises': 4 ** n,
    'fact_chain_countermodels': 0,
    'reversed_inclusion_premises': 5 ** n,
    'reversed_inclusion_countermodels': 5 ** n - 4 ** n,
    'reversed_inclusion_nonempty_countermodels': 5 ** n - 4 ** n - (3 ** n - 2 ** n),
    'reciprocal_premises': 3 ** n,
    'reciprocal_countermodels': 0,
    'negative_premises': 4 ** n,
    'negative_countermodels': 0,
    'negative_with_broad_middle': 4 ** n - 3 ** n,
    'negative_with_broad_middle_all_nonempty': 6,
}
equal(m.finite_report(), expected_counts, 'closed-form set counts')
print('Closed-form set counts:', json.dumps(expected_counts, sort_keys=True))

pair_count = 0
for size in range(9):
    for a, b in product(range(2 ** size), repeat=2):
        # Arithmetic radix conversion is independent of production bit predicates.
        left = {i for i in range(size) if a // (2 ** i) % 2 == 1}
        right = {i for i in range(size) if b // (2 ** i) % 2 == 1}
        equal(m.included(a, b, size), left.issubset(right), 'inclusion')
        equal(m.disjoint(a, b, size), left.isdisjoint(right), 'disjointness')
        equal(m.members(a, size), sorted(left), 'members')
        pair_count += 1
equal(pair_count, 87381, 'all accepted-size pairs')
print('All supported universe sizes 0..8:', pair_count, 'set pairs checked')

# Each row gives outcomes for U=0 and U=1. This table is calculated by hand
# from the stipulated equations, rather than by topological or SAT evaluation.
T = {
    (None, None): (((0, 0), (1, 1)), ((0, 0), (1, 1))),
    (None, 0): (((0, 0), (1, 0)), ((0, 0), (0, 0))),
    (None, 1): (((0, 1), (1, 1)), ((1, 1), (1, 1))),
    (0, None): (((0, 0), (0, 0)), ((0, 0), (0, 1))),
    (0, 0): (((0, 0), (0, 0)), ((0, 0), (0, 0))),
    (0, 1): (((0, 1), (0, 1)), ((0, 1), (0, 1))),
    (1, None): (((1, 1), (1, 1)), ((1, 0), (1, 1))),
    (1, 0): (((1, 0), (1, 0)), ((1, 0), (1, 0))),
    (1, 1): (((1, 1), (1, 1)), ((1, 1), (1, 1))),
}
responses = 0
for interventions, both_models in T.items():
    d = {var: val for var, val in zip(('X', 'Y'), interventions) if val is not None}
    for name, outputs in zip(('X_to_Y', 'Y_to_X'), both_models):
        for u, outcome in enumerate(outputs):
            equal(m.evaluate(name, u, d), outcome, f'{name},u={u},do={d}')
            responses += 1
        distribution = {xy: Fraction(outputs.count(xy), 2) for xy in product((0, 1), repeat=2)}
        equal(m.distribution(name, d), distribution, 'manual-table distribution')
print('Independent hand table:', responses, 'responses and 18 distributions checked')
equal(m.distribution('X_to_Y')[(1,1)] / (m.distribution('X_to_Y')[(1,0)] + m.distribution('X_to_Y')[(1,1)]), 1, 'observational conditional')
equal(sum(p for (x,y),p in m.distribution('X_to_Y', {'X':1}).items() if y == 1), Fraction(1), 'forward do(X=1)')
equal(sum(p for (x,y),p in m.distribution('Y_to_X', {'X':1}).items() if y == 1), Fraction(1,2), 'reverse do(X=1)')
print('Manuscript do(X=1): P(Y=1)=1 versus 1/2; observation conditional=1')

result = m.results()
equal(result['finite_sets'], expected_counts, 'results finite report')
for row in result['scm']['intervention_cases']:
    key = tuple(row['do'].get(v) for v in ('X','Y'))
    for name, outcomes in zip(('X_to_Y','Y_to_X'), T[key]):
        expected = [{'X':x, 'Y':y, 'probability':str(Fraction(outcomes.count((x,y)),2))} for x,y in product((0,1), repeat=2)]
        equal(row['models'][name], expected, 'published serialized probabilities')
for name in ('results.json', 'logs/enumeration-normal.json', 'logs/enumeration-O.json', 'logs/enumeration-OO.json'):
    equal(json.loads((base/name).read_text()), result, name)
print('Published final JSON and three enumeration JSON files match all checked fields')

original = (base/'results.json').read_bytes()
for mode in ('normal','O','OO'):
    flags = [] if mode == 'normal' else ['-'+mode]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    command = [sys.executable, *flags, '-m','unittest','-v','test_model.py']
    run = subprocess.run(command, cwd=base, capture_output=True, env=env)
    Path(__file__).with_name('rerun-tests-'+mode+'.log').write_bytes(run.stdout+run.stderr)
    equal(run.returncode, 0, 'test exit '+mode)
    if b'Ran 32 tests' not in run.stderr or not run.stderr.rstrip().endswith(b'OK'):
        raise RuntimeError('Unexpected test summary '+mode)
    enum = subprocess.run([sys.executable,*flags,'model.py'], cwd=base, capture_output=True, env=env)
    equal(enum.returncode, 0, 'enumeration exit '+mode)
    equal(enum.stdout, original, 'fresh output byte equality '+mode)
    print('Fresh run:', mode, '32 tests OK; model output SHA256', hashlib.sha256(enum.stdout).hexdigest())
print('AUDIT PASS')
