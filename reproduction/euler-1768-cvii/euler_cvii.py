"""Original stdlib teaching model: three-term categorical syllogisms.

Bits: P=1, Q=2, M=4. A model is a nonzero 8-bit occupied-cell mask;
cell t denotes one individual with exactly the memberships in t.
Forms use major, minor, conclusion moods; the conclusion is always P–Q (P minor, Q major).
"""
from itertools import product
import json

MOODS = 'AEIO'
TERMS = {'P': 1, 'Q': 2, 'M': 4}
FIGURES = {1: (('M', 'Q'), ('P', 'M')),
           2: (('Q', 'M'), ('P', 'M')),
           3: (('M', 'Q'), ('M', 'P')),
           4: (('Q', 'M'), ('M', 'P'))}
RULES = ('two_negative', 'two_particular', 'negative_conclusion',
         'particular_conclusion', 'affirmative_conclusion')


def _integer(value, low, high, label):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f'{label} must be an integer in [{low}, {high}]')


def cells(support):
    """Return occupied membership types, sorted; require nonempty universe."""
    _integer(support, 1, 255, 'support')
    return tuple(t for t in range(8) if support & (1 << t))


def _proposition(mood, subject, predicate):
    if not isinstance(mood, str) or mood not in tuple(MOODS):
        raise ValueError('mood must be one of A, E, I, O')
    if not isinstance(subject, str) or subject not in TERMS:
        raise ValueError('unknown subject')
    if not isinstance(predicate, str) or predicate not in TERMS:
        raise ValueError('unknown predicate')


def holds(support, mood, subject, predicate):
    """AEIO truth, with modern vacuous A/E and existential I/O."""
    _proposition(mood, subject, predicate)
    occupied = cells(support)
    s, p = TERMS[subject], TERMS[predicate]
    intersection = any(t & s and t & p for t in occupied)
    difference = any(t & s and not t & p for t in occupied)
    return {'A': not difference, 'E': not intersection,
            'I': intersection, 'O': difference}[mood]


def validate_form(form):
    if not isinstance(form, str) or len(form) != 4:
        raise ValueError('form must be three AEIO letters followed by figure 1–4')
    if any(c not in MOODS for c in form[:3]) or form[3] not in '1234':
        raise ValueError('invalid categorical form')
    return form


def all_forms():
    return tuple(''.join(m) + str(f) for f in range(1, 5)
                 for m in product(MOODS, repeat=3))


def _regime(all_terms_nonempty):
    if type(all_terms_nonempty) is not bool:
        raise ValueError('all_terms_nonempty must be bool')


def supports(all_terms_nonempty=False):
    """Canonical supports ordered by minimum individual count, then mask."""
    _regime(all_terms_nonempty)
    result = [s for s in range(1, 256)
              if not all_terms_nonempty or all(
                  any(t & bit for t in cells(s)) for bit in TERMS.values())]
    return tuple(sorted(result, key=lambda s: (s.bit_count(), s)))


def argument_truth(support, form):
    validate_form(form)
    major, minor = FIGURES[int(form[3])]
    return (holds(support, form[0], *major),
            holds(support, form[1], *minor),
            holds(support, form[2], 'P', 'Q'))


def minimum_countermodel(form, all_terms_nonempty=False):
    """Return smallest support satisfying premises and falsifying conclusion.

    None means no countermodel among the stated complete three-term supports.
    Cardinality is support.bit_count(); ties use the smallest integer mask.
    """
    validate_form(form)
    for support in supports(all_terms_nonempty):
        if argument_truth(support, form) == (True, True, False):
            return support
    return None


def violations(form):
    """Syntactic NECESSARY restrictions; passing does not imply validity.

    In the ordinary independent-three-term setting, each violation excludes
    validity. The conclusion restrictions are claims ABOUT VALID arguments,
    not claims that any premises force a conclusion of the required mood.
    """
    validate_form(form)
    a, b, c = form[:3]
    neg = sum(m in 'EO' for m in (a, b))
    particular = sum(m in 'IO' for m in (a, b))
    return tuple(rule for rule, violated in zip(RULES, (
        neg == 2, particular == 2,
        neg >= 1 and c not in 'EO',
        particular >= 1 and c not in 'IO',
        neg == 0 and c not in 'AI')) if violated)


def countermodel_record(support):
    if support is None:
        return None
    ts = cells(support)
    return {'support': support, 'cardinality': len(ts), 'types': list(ts),
            'extensions': {name: [i for i, t in enumerate(ts) if t & bit]
                           for name, bit in TERMS.items()}}


def native_holds(n, mood, subject, predicate):
    """AEIO over explicit n-point bitset extensions, n >= 1 (no name magic)."""
    _integer(n, 1, 16, 'n')
    if not isinstance(mood, str) or mood not in tuple(MOODS):
        raise ValueError('invalid mood')
    _integer(subject, 0, (1 << n) - 1, 'subject extension')
    _integer(predicate, 0, (1 << n) - 1, 'predicate extension')
    intersection = bool(subject & predicate)
    difference = bool(subject & ~predicate)
    return {'A': not difference, 'E': not intersection,
            'I': intersection, 'O': difference}[mood]


def singleton_counts(n):
    """Exhaust all P,Q subsets and all denoting names (one shared individual).

    Count premises A(N,P), A(N,Q) and violations of I(P,Q); likewise I(N,P),
    I(N,Q). A and I coincide when N is exactly a singleton, as do E and O.
    This native calculation is finite evidence, not proof for arbitrary n.
    """
    _integer(n, 1, 4, 'n')
    counts = {'n': n, 'assignments': 0, 'premise_pairs_true': 0,
              'counterexamples': 0, 'A_I_disagreements': 0,
              'E_O_disagreements': 0}
    for p, q, named in product(range(1 << n), range(1 << n), range(n)):
        name = 1 << named
        counts['assignments'] += 1
        counts['A_I_disagreements'] += native_holds(n, 'A', name, p) != native_holds(n, 'I', name, p)
        counts['E_O_disagreements'] += native_holds(n, 'E', name, p) != native_holds(n, 'O', name, p)
        if native_holds(n, 'A', name, p) and native_holds(n, 'A', name, q):
            counts['premise_pairs_true'] += 1
            counts['counterexamples'] += not native_holds(n, 'I', p, q)
    return counts


def report():
    result = {'model': {'bits': TERMS, 'nonempty_universe': True,
                        'conclusion': 'P–Q', 'forms': 256}, 'regimes': {}}
    for nonempty in (False, True):
        valid, surviving_invalid = [], {}
        rule_counts = {r: {'violating_forms': 0, 'valid_violating_forms': 0} for r in RULES}
        for form in all_forms():
            bad = violations(form)
            cm = minimum_countermodel(form, nonempty)
            if cm is None:
                valid.append(form)
            elif not bad:
                surviving_invalid[form] = countermodel_record(cm)
            for rule in bad:
                rule_counts[rule]['violating_forms'] += 1
                rule_counts[rule]['valid_violating_forms'] += cm is None
        result['regimes']['all_terms_nonempty' if nonempty else 'modern'] = {
            'supports': len(supports(nonempty)), 'valid_count': len(valid),
            'valid_forms': valid, 'per_rule': rule_counts,
            'filter_survivors': sum(not violations(f) for f in all_forms()),
            'surviving_invalid_count': len(surviving_invalid),
            'surviving_invalid_countermodels': surviving_invalid}
    result['singular_names'] = {
        'shared_singleton_exhaustion': [singleton_counts(n) for n in range(1, 5)],
        'independent_witnesses_countermodel': {
            'n': 2, 'P': [0], 'Q': [1], 'M': [0, 1], 'form': 'III3'},
        'non_denoting_name_countermodel': {
            'n': 1, 'N': [], 'P': [], 'Q': [],
            'premises': ['A(N,P)', 'A(N,Q)'], 'conclusion_false': 'I(P,Q)'},
        'required_name_constraint': '|N| = 1; both premises use the SAME N'}
    return result


if __name__ == '__main__':
    print(json.dumps(report(), ensure_ascii=False, indent=2, sort_keys=True))
