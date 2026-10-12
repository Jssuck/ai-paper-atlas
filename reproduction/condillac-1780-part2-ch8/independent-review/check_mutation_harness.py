"""Independent sanity checks of the behavioral fault-probe classifier."""
from dataclasses import asdict
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mutation_check as h


def crash():
    raise RuntimeError('intentional independent harness diagnostic')


def main():
    cases = (
        ('kill', lambda: 1, lambda: 2, 1, 'killed'),
        ('survival', lambda: 1, lambda: 1, 1, 'survived'),
        ('invalid baseline', lambda: 2, lambda: 3, 1, 'invalid_baseline'),
        ('baseline exception', crash, lambda: 2, 1, 'baseline_error'),
        ('mutant exception', lambda: 1, crash, 1, 'mutant_error'),
        ('bool-int result', lambda: 1, lambda: True, 1, 'killed'),
        ('nested bool-int result', lambda: {'x': (1,)}, lambda: {'x': (True,)}, {'x': (1,)}, 'killed'),
        ('bool-int dictionary key', lambda: {1: 'x'}, lambda: {True: 'x'}, {1: 'x'}, 'killed'),
        ('nested bool-int dictionary key', lambda: {'x': {1: 'y'}}, lambda: {'x': {True: 'y'}}, {'x': {1: 'y'}}, 'killed'),
        ('tuple bool-int dictionary key', lambda: {(1,): 'x'}, lambda: {(True,): 'x'}, {(1,): 'x'}, 'killed'),
    )
    result = {}
    for label, baseline, mutant, expected, status in cases:
        actual = h.classify(baseline, mutant, expected)
        if actual.status != status:
            raise RuntimeError(label + ': expected ' + status + ', got ' + actual.status)
        result[label] = asdict(actual)
    probes = h.run()
    if len(probes) != 13 or any(v['status'] != 'killed' for v in probes.values()):
        raise RuntimeError('published behavioral probes did not distinguish all witnesses')
    print(json.dumps({'status': 'PASS', 'sanity': result, 'published_behavioral_probes': probes,
                      'limits': 'hand-written behavioral alternatives, not source-mutation coverage'},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
