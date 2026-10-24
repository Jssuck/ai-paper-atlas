#!/usr/bin/env python3
"""Compare saved oracle and production outputs without importing production."""
import json
from pathlib import Path
import sys

here = Path(__file__).resolve().parent
mode = sys.argv[1]
production_name = {'normal': 'normal', 'O': 'optimized', 'OO': 'double_optimized'}[mode]
p = json.loads((here.parent / 'results' / (production_name + '.json')).read_text())
o = json.loads((here / ('oracle-' + mode + '.json')).read_text())
for key, value in o.items():
    if p[key] != value:
        raise RuntimeError('Mismatch: ' + key)
cases = [
 ('missing_coverage_nonempty', 2, {0}, {0, 1}, {0}),
 ('missing_observations', 1, set(), {0}, {0}),
 ('empty_sample_no_existence', 1, set(), {0}, set()),
 ('classification_not_needed_for_minimal_transfer', 2, {0, 1}, {0}, {0, 1}),
 ('incomplete_but_accidentally_true', 2, {0, 1}, {0, 1}, {0}),
 ('complete_toy_enumeration', 3, {0, 1, 2}, {0, 1, 2}, {0, 1, 2}),
]
expected = []
for name, n, a, b, c in cases:
    expected.append(dict(name=name, n=n, A=sorted(a), B=sorted(b), C=sorted(c),
                         observations=all(x in a for x in c), classification=all(x in b for x in c),
                         coverage=all(x in c for x in b), universal=all(x in a for x in b),
                         particular=any(x in a for x in b), missed_failures=sorted(x for x in b if x not in a)))
if p['examples'] != expected:
    raise RuntimeError('Named counterexample mismatch')
print(json.dumps({'mode': mode, 'status': 'PASS', 'compared_keys': sorted(o), 'worlds': o['worlds'], 'rule_checks': o['worlds'] * len(o['rules']), 'coverage_pairs': o['coverage_iff_forall_A']['pairs'], 'named_examples_checked': len(expected)}, indent=2, sort_keys=True))
