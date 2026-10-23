"""Original finite teaching model of Prior Analytics II.13; standard library only."""
import itertools
import json

KINDS = 'UEIO'
TERMS = 'ABC'
NEG = {'U': 'O', 'O': 'U', 'E': 'I', 'I': 'E'}


def validate_model(model):
    if not isinstance(model, (tuple, list)) or not model:
        raise ValueError('A model is a nonempty sequence of distinct types')
    if any(type(t) is not int or not 0 <= t < 8 for t in model) or len(set(model)) != len(model):
        raise ValueError('Types must be distinct integers from 0 to 7')


def truth(model, proposition):
    validate_model(model)
    if not isinstance(proposition, (tuple, list)) or len(proposition) != 3:
        raise ValueError('Expected (kind, predicate, subject)')
    kind, predicate, subject = proposition
    if any(type(v) is not str or len(v) != 1 for v in proposition) or kind not in KINDS or predicate not in TERMS or subject not in TERMS:
        raise ValueError('Unknown kind or term')
    p, s = TERMS.index(predicate), TERMS.index(subject)
    members = [bool(t & (1 << p)) for t in model if t & (1 << s)]
    return {'U': all(members), 'E': not any(members), 'I': any(members), 'O': not all(members)}[kind]


def models(policy='empty_allowed'):
    if type(policy) is not str or policy not in ('empty_allowed', 'all_nonempty', 'B_nonempty'):
        raise ValueError('Unknown existence policy')
    result = []
    for n in range(1, 9):
        for m in itertools.combinations(range(8), n):
            exists = [any(t & (1 << i) for t in m) for i in range(3)]
            if policy == 'all_nonempty' and not all(exists):
                continue
            if policy == 'B_nonempty' and not exists[1]:
                continue
            result.append(m)
    return result


def entailment(premises, conclusion, policy='empty_allowed'):
    if not isinstance(premises, (tuple, list)):
        raise ValueError('Premises must be a sequence of propositions')
    ms = models(policy)
    # Validate every proposition even if an antecedent has no models.
    for p in [*premises, conclusion]:
        truth(ms[0], p)
    satisfying = [m for m in ms if all(truth(m, p) for p in premises)]
    countermodels = [m for m in satisfying if not truth(m, conclusion)]
    return {'valid': not countermodels, 'premise_models': len(satisfying),
            'countermodels': len(countermodels),
            'minimal_countermodel': list(countermodels[0]) if countermodels else None}


def candidates(policy):
    rows = []
    for q, x, r in itertools.product(KINDS, repeat=3):
        target, hypothesis = (q, 'A', 'B'), (NEG[q], 'A', 'B')
        other, result = (x, 'C', 'B'), (r, 'A', 'C')
        known = (NEG[r], 'A', 'C')
        internal = entailment([hypothesis, other], result, policy)
        external = entailment([other, known], target, policy)
        certificate = internal['valid'] and internal['premise_models'] > 0 and external['valid'] and external['premise_models'] > 0
        rows.append({'target': target, 'hypothesis': hypothesis, 'other': other,
                     'result': result, 'known': known, 'internal': internal,
                     'external': external, 'certificate': certificate})
    return rows


def named_checks():
    cases = [
        ('U_target', [('U','C','B'),('U','A','C')], ('U','A','B'), 'empty_allowed'),
        ('I_target', [('I','C','B'),('U','A','C')], ('I','A','B'), 'empty_allowed'),
        ('E_target', [('U','C','B'),('E','A','C')], ('E','A','B'), 'empty_allowed'),
        ('O_target', [('I','C','B'),('E','A','C')], ('O','A','B'), 'empty_allowed'),
        ('I_with_universal_background', [('U','C','B'),('U','A','C')], ('I','A','B'), 'empty_allowed'),
        ('I_with_B_exists', [('U','C','B'),('U','A','C')], ('I','A','B'), 'B_nonempty'),
        ('O_with_universal_background', [('U','C','B'),('E','A','C')], ('O','A','B'), 'empty_allowed'),
        ('O_with_B_exists', [('U','C','B'),('E','A','C')], ('O','A','B'), 'B_nonempty'),
        ('wrong_E_assumption_only_returns_I', [('I','C','B'),('U','A','C')], ('U','A','B'), 'empty_allowed'),
        ('not_U_does_not_give_E', [('O','A','B')], ('E','A','B'), 'all_nonempty'),
        ('not_E_does_not_give_U', [('I','A','B')], ('U','A','B'), 'all_nonempty'),
        ('wrong_E_internal_needs_B', [('E','A','B'),('U','C','B')], ('O','A','C'), 'empty_allowed'),
        ('wrong_E_internal_with_B_exists', [('E','A','B'),('U','C','B')], ('O','A','C'), 'B_nonempty'),
        ('wrong_U_internal_needs_B', [('U','A','B'),('U','C','B')], ('I','A','C'), 'empty_allowed'),
        ('wrong_U_internal_with_B_exists', [('U','A','B'),('U','C','B')], ('I','A','C'), 'B_nonempty'),
        ('O_target_does_not_refute_I', [('I','C','B'),('E','A','C')], ('E','A','B'), 'all_nonempty'),
        ('two_existentials_different_witnesses', [('I','A','B'),('I','C','B')], ('I','A','C'), 'all_nonempty'),
    ]
    return [{'name':name, 'premises':ps, 'conclusion':c, 'policy':policy, **entailment(ps,c,policy)} for name,ps,c,policy in cases]


def report():
    sections = []
    for policy in ('empty_allowed', 'all_nonempty'):
        rows = candidates(policy)
        sections.append({'policy':policy, 'models':len(models(policy)), 'candidates':len(rows),
                         'certificate_counts':{q:sum(r['certificate'] for r in rows if r['target'][0]==q) for q in KINDS},
                         'rows':rows})
    return {'scope':'Single internal third-figure step with shared subject B; predicate-first notation; no prior conversion',
            'type_bits':'bit0=A, bit1=B, bit2=C; smallest cardinality then lexicographic witness',
            'policies':sections, 'named_checks':named_checks(),
            'coexistence':{'model':[2,7], 'I_AB':truth([2,7],('I','A','B')), 'O_AB':truth([2,7],('O','A','B'))}}


if __name__ == '__main__':
    print(json.dumps(report(), ensure_ascii=False, indent=2))
