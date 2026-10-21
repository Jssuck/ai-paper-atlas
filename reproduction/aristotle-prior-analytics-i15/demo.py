"""Reproducible exhaustive finite checks and explicit boundary examples."""
import json
from collections import Counter
from itertools import product
from model import Model, models, possible, entails


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def run():
    counts = Counter()
    for n in (1, 2):
        for m in models(n):
            counts['model_actual_configurations'] += 1
            # A contingent major over actual B transfers to actual C or a C witness.
            for quantity, mood in (('all', 'A'), ('some', 'I')):
                if m.modal('A', 'B') and m.categorical('B', 'C', mood):
                    counts['direct_' + quantity] += 1
                    check(m.modal('A', 'C', quantity=quantity), 'direct transfer failed')
                # The stable bridge is explicitly additional, not inferred from a time slice.
                for negative in (False, True):
                    if m.stable('A', 'B', negative) and m.modal('B', 'C', quantity=quantity):
                        key = ('negative_' if negative else 'positive_') + quantity
                        counts['stable_' + key] += 1
                        mode = 'M-' if negative else 'M+'
                        check(m.modal('A', 'C', mode, quantity), 'stable weak bridge failed')
                        if not m.modal('A', 'C', 'K', quantity):
                            counts['not_strong_' + key] += 1
                for negative in (False, True):
                    if m.stable('A', 'B', negative) and m.reverse_strong_guard('A', 'B', 'C', negative, quantity):
                        counts['strong_guard_' + ('negative_' if negative else 'positive_') + quantity] += 1
                        check(m.modal('A', 'C', 'K', quantity), 'strong witness guard failed')
            if m.categorical('A', 'B') and m.modal('B', 'C') and not m.modal('A', 'C', 'M+'):
                counts['time_slice_positive_failures'] += 1
            if m.categorical('A', 'B', 'E') and m.modal('B', 'C') and not m.modal('A', 'C', 'M-'):
                counts['time_slice_negative_failures'] += 1
    # Truth-vector theorem: jointly possible premises and necessary implication.
    for k in range(1, 5):
        vectors = tuple(product((False, True), repeat=k))
        for p in vectors:
            for q in vectors:
                counts['truth_vector_pairs'] += 1
                if entails(p, q) and possible(p):
                    counts['possible_consequence_cases'] += 1
                    check(possible(q), 'possible consequence failed')
                for r in vectors:
                    if entails(tuple(a and b for a, b in zip(p, r)), q) and possible(tuple(a and b for a,b in zip(p,r))):
                        counts['fixed_background_joint_cases'] += 1
                        check(possible(q), 'joint-background consequence failed')
    examples = {
        'time_slice_positive': Model(1, ((0,0,1),(0,1,1))),
        'time_slice_negative': Model(1, ((1,0,1),(1,1,1))),
        'stable_positive_not_strong': Model(1, ((1,0,1),(1,1,1))),
        'stable_negative_not_strong': Model(1, ((0,0,1),(0,1,1))),
        'nonempty_time_slice_positive': Model(2, ((1,1,2),(1,2,2))),
        'nonempty_time_slice_negative': Model(2, ((2,1,2),(2,2,2))),
        'negative_minor_necessary_positive': Model(2, ((3,1,2),(2,1,2))),
        'negative_minor_necessary_negative': Model(2, ((1,1,2),(0,1,2))),
        'weak_negative_not_actual': Model(1, ((0,1,1),(1,0,1)),1),
        'pointwise_not_joint': Model(2, ((1,0,3),(2,0,3))),
        'direct_particular_witness': Model(2, ((1,1,3),(0,1,3))),
    }
    return {'semantics':'modern fixed-domain, actual-subject, pointwise; not unique Aristotle semantics',
            'counts':dict(sorted(counts.items())),
            'examples':{k:v.as_dict() for k,v in examples.items()},
            'propositional_examples':{
                'false_premise_true_conclusion':{'P':[False,True],'Q':[True,True]},
                'separately_possible_not_joint':{'P':[True,False],'R':[False,True]},
                'background_not_preserved':{'P':[False,True],'R':[True,False],'Q':[False,False]},
                'necessary_implication_not_necessary_conclusion':{'P':[True,False],'Q':[True,False]}}}

if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
