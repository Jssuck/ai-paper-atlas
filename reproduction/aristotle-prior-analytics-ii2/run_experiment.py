"""Run bounded checks and output reproducible JSON, never use assert for checks."""
import json
from collections import Counter
from model import MOODS, classify, evaluate, examples, signature, type_models


def run():
    result = {}
    for policy in (False, True):
        models = list(type_models(policy))
        stats = {}
        for mood, props in MOODS.items():
            sigs, classes = Counter(), Counter()
            for m in models:
                truth = evaluate(m, mood)
                if truth == (True, True, False):
                    raise RuntimeError('Invalid soundness result')
                sigs[signature(m, mood)] += 1
                major = classify(m, *props[0])
                minor = classify(m, *props[1])
                classes[f'{major}|{minor}|{truth[2]}'] += 1
                if policy and mood in ('Barbara', 'Celarent'):
                    if major == 'wholly_false' and truth[1] and truth[2]:
                        raise RuntimeError('Major-wholly-false universal restriction failed')
            stats[mood] = {'truth_signatures': dict(sorted(sigs.items())),
                           'classification_counts': dict(sorted(classes.items()))}
        result['nonempty_BC' if policy else 'empty_terms_allowed'] = {
            'models': len(models), 'mood_evaluations': len(models) * len(MOODS),
            'moods': stats}
    result['examples'] = {}
    for name, (m, mood) in examples().items():
        if not evaluate(m, mood)[2]:
            raise RuntimeError('Example conclusion must be true')
        result['examples'][name] = {'mood': mood, 'A': sorted(m.A), 'B': sorted(m.B),
            'C': sorted(m.C), 'signature': signature(m, mood),
            'major': classify(m, *MOODS[mood][0]), 'minor': classify(m, *MOODS[mood][1])}
    return result

if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
