"""Finite checks are implementation evidence, not general theorem proofs."""
import json
from collections import Counter
from model import examples, models


def run():
    counts = Counter()
    for n in (1, 2):
        for m in models(n):
            counts['configurations'] += 1
            for q, quality in (('all', 'E'), ('some', 'O')):
                if m.modal('A', 'B', 'K') and m.modal('B', 'C', 'N+', q):
                    counts['direct_' + q] += 1
                    if not m.modal('A', 'C', 'K', q):
                        raise RuntimeError('direct theorem failed')
                if m.stable_positive('A', 'B') and m.modal('B', 'C', 'K', q):
                    counts['stable_positive_' + q] += 1
                    if not m.modal('A', 'C', 'M+', q):
                        raise RuntimeError('stable positive theorem failed')
                    if not m.modal('A', 'C', 'K', q):
                        counts['stable_not_strong_' + q] += 1
                if m.symmetric_negative('A', 'B') and m.modal('B', 'C', 'K', q):
                    counts['symmetric_negative_' + q] += 1
                    if not m.categorical('A', 'C', quality):
                        raise RuntimeError('actual negative theorem failed')
                    if not m.modal('A', 'C', 'M-', q):
                        raise RuntimeError('actual-to-possible theorem failed')
                    if not m.modal('A', 'C', 'N-', q):
                        counts['symmetric_not_necessary_' + q] += 1
            if m.modal('A', 'B', 'N+') and m.modal('B', 'C', 'K') and not m.modal('A', 'C', 'M+'):
                counts['local_positive_failure'] += 1
            if m.modal('A', 'B', 'N-') and m.modal('B', 'C', 'K') and not m.categorical('A', 'C', 'E'):
                counts['one_way_negative_failure'] += 1
    return {'scope': 'All 1/2-object, 2-world assignments and both actual indices; branches overlap.',
            'counts': dict(sorted(counts.items())),
            'examples': {name: m.as_dict() for name, m in examples().items()}}

if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))
