"""Original finite-type teaching model for Prior Analytics II.20 (not historical code)."""
import itertools
import json

KINDS = 'AEIO'
CONTRADICTORY = {'A': 'O', 'O': 'A', 'E': 'I', 'I': 'E'}
# Bit membership: S=1, M=2, P=4. Type 000 is irrelevant to these formulas.
BITS = {'S': 1, 'M': 2, 'P': 4}
FIGURES = {1: (('M', 'P'), ('S', 'M')),
           2: (('P', 'M'), ('S', 'M')),
           3: (('M', 'P'), ('M', 'S'))}

def holds(kind, subject, predicate, support):
    """Evaluate a categorical formula on occupied membership types, with empty terms allowed."""
    if kind not in KINDS or len(kind) != 1:
        raise ValueError('kind must be A, E, I, or O')
    if subject not in BITS or predicate not in BITS:
        raise ValueError('unknown term')
    support = tuple(support)
    if any(type(t) is not int or not 1 <= t <= 7 for t in support):
        raise ValueError('support types must be integers 1..7')
    inside = any(t & BITS[subject] and t & BITS[predicate] for t in support)
    outside = any(t & BITS[subject] and not t & BITS[predicate] for t in support)
    return {'A': not outside, 'E': not inside, 'I': inside, 'O': outside}[kind]

def models(nonempty=True):
    """All 128 relevant supports; optionally require each of S, M, P nonempty."""
    for mask in range(128):
        support = tuple(t for t in range(1, 8) if mask & (1 << (t - 1)))
        if not nonempty or all(any(t & bit for t in support) for bit in BITS.values()):
            yield support

def check(figure, mood, nonempty=True):
    if type(figure) is not int or figure not in FIGURES:
        raise ValueError('figure must be 1, 2, or 3')
    if not isinstance(mood, str) or len(mood) != 3 or any(k not in KINDS for k in mood):
        raise ValueError('mood must contain three A/E/I/O letters')
    major, minor = FIGURES[figure]
    witnesses = []
    count = 0
    for support in models(nonempty):
        if holds(mood[0], *major, support) and holds(mood[1], *minor, support):
            count += 1
            if not holds(mood[2], 'S', 'P', support):
                witnesses.append(support)
    return {'valid': not witnesses, 'premise_models': count,
            'countermodels': len(witnesses),
            'first_countermodel': list(witnesses[0]) if witnesses else None}

def refutes(figure, premises, thesis, nonempty=True):
    """Thesis is a separate S-P claim, not an additional premise."""
    if thesis not in CONTRADICTORY:
        raise ValueError('thesis must be A/E/I/O')
    return check(figure, premises + CONTRADICTORY[thesis], nonempty)

def report():
    valid = {str(f): [] for f in FIGURES}
    negative = particular = 0
    for f in FIGURES:
        for letters in itertools.product(KINDS, repeat=3):
            mood = ''.join(letters)
            result = check(f, mood)
            if result['premise_models'] == 0:
                raise RuntimeError('unexpected inconsistent premise pair')
            if result['valid']:
                valid[str(f)].append(mood)
            if all(k in 'EO' for k in mood[:2]):
                negative += 1
                if result['valid']:
                    raise RuntimeError('two-negative counterexample to claimed pattern')
            if all(k in 'IO' for k in mood[:2]):
                particular += 1
                if result['valid']:
                    raise RuntimeError('two-particular counterexample to claimed pattern')
    return {'scope': 'three figures, distinct S/M/P, all three terms nonempty',
            'supports_all': len(list(models(False))),
            'supports_nonempty_terms': len(list(models())),
            'candidate_syllogisms': 192, 'valid_moods': valid,
            'two_negative_candidates_checked': negative,
            'two_particular_candidates_checked': particular,
            'examples': {'AAA_1': check(1, 'AAA'), 'EAE_1': check(1, 'EAE'),
                         'AAA_2': check(2, 'AAA'),
                         'AA_1_refutes_O': refutes(1, 'AA', 'O'),
                         'AA_1_does_not_refute_A': refutes(1, 'AA', 'A'),
                         'AAI_3_nonempty': check(3, 'AAI'),
                         'AAI_3_empty_allowed': check(3, 'AAI', False)}}

if __name__ == '__main__':
    print(json.dumps(report(), ensure_ascii=False, indent=2, sort_keys=True))
