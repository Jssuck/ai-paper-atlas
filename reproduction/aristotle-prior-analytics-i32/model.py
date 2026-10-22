"""Original, deliberately restricted teaching model for Prior Analytics I.32.
No natural-language parsing, historical semantics certification, or proof search.
"""
from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Prop:
    kind: str
    subject: str
    predicate: str

    def __post_init__(self):
        if self.kind not in ('A', 'E', 'I', 'O'):
            raise ValueError('kind must be A, E, I, or O')
        for term in (self.subject, self.predicate):
            if not isinstance(term, str) or not term or term.strip() != term:
                raise ValueError('term must be a nonblank canonical string')

    def as_dict(self):
        return {'kind': self.kind, 'subject': self.subject, 'predicate': self.predicate}


def analyze(premises, conclusion):
    """Recognize orientation only, never infer validity or hidden premises."""
    premises = tuple(premises)
    if not isinstance(conclusion, Prop) or any(not isinstance(p, Prop) for p in premises):
        raise TypeError('structured Prop objects required')
    if len(premises) != 2:
        return {'status': 'not_two_premises', 'figure': None}
    s, p = conclusion.subject, conclusion.predicate
    if s == p:
        return {'status': 'distinct_extremes_required', 'figure': None}
    terms = {t for q in premises for t in (q.subject, q.predicate)}
    middle = terms - {s, p}
    if len(terms) != 3 or len(middle) != 1:
        return {'status': 'not_three_terms', 'figure': None}
    m = next(iter(middle))
    if any(m not in (q.subject, q.predicate) for q in premises):
        return {'status': 'middle_not_repeated', 'figure': None}
    majors = [q for q in premises if {q.subject, q.predicate} == {m, p}]
    minors = [q for q in premises if {q.subject, q.predicate} == {s, m}]
    if len(majors) != 1 or len(minors) != 1:
        return {'status': 'missing_extreme_link', 'figure': None}
    major, minor = majors[0], minors[0]
    pair = (major.subject == m, minor.predicate == m)
    figure = {(True, True): 1, (False, True): 2, (True, False): 3}.get(pair)
    return {'status': 'shape_only' if figure else 'outside_first_three_figures',
            'figure': figure, 'middle': m,
            'major': major.as_dict(), 'minor': minor.as_dict(),
            'mood': major.kind + minor.kind + conclusion.kind}


def holds(proposition, interpretation):
    """Extensional AEIO with empty extensions allowed; universe supplied by caller."""
    x, y = interpretation[proposition.subject], interpretation[proposition.predicate]
    if proposition.kind == 'A':
        return x <= y
    if proposition.kind == 'E':
        return not (x & y)
    if proposition.kind == 'I':
        return bool(x & y)
    return bool(x - y)


def find_countermodel(premises, conclusion, max_size=3, nonempty=()):
    """Finite check, not a general validity decision. No countermodel != proof."""
    premises, nonempty = tuple(premises), tuple(nonempty)
    if not isinstance(conclusion, Prop) or any(not isinstance(p, Prop) for p in premises):
        raise TypeError('structured Prop objects required')
    if type(max_size) is not int or not 1 <= max_size <= 4:
        raise ValueError('max_size must be an integer from 1 to 4')
    terms = sorted({t for q in (*premises, conclusion) for t in (q.subject, q.predicate)})
    if len(terms) > 4:
        raise ValueError('teaching enumeration limited to four terms')
    if any(t not in terms for t in nonempty):
        raise ValueError('nonempty constraint must name a present term')
    checked = admissible = premise_models = 0
    for size in range(1, max_size + 1):
        sets = [frozenset(i for i in range(size) if mask & (1 << i))
                for mask in range(1 << size)]
        for extensions in product(sets, repeat=len(terms)):
            checked += 1
            model = dict(zip(terms, extensions))
            if any(not model[t] for t in nonempty):
                continue
            admissible += 1
            if not all(holds(q, model) for q in premises):
                continue
            premise_models += 1
            if not holds(conclusion, model):
                return {'status': 'countermodel_found', 'universe_size': size,
                        'model': {t: sorted(model[t]) for t in terms},
                        'checked': checked, 'admissible': admissible,
                        'premise_models': premise_models, 'max_size': max_size,
                        'nonempty': list(nonempty)}
    return {'status': 'no_countermodel_in_bound', 'max_size': max_size,
            'checked': checked, 'admissible': admissible,
            'premise_models': premise_models, 'nonempty': list(nonempty)}


def candidate_completions(known, conclusion, candidates, max_size=3, nonempty=()):
    """Audit caller-supplied hypotheses only. Never certify a candidate as factual."""
    if not isinstance(known, Prop) or not isinstance(conclusion, Prop):
        raise TypeError('structured Prop objects required')
    nonempty = tuple(nonempty)
    rows = []
    for candidate in candidates:
        if not isinstance(candidate, Prop):
            raise TypeError('structured candidate required')
        if candidate == conclusion or candidate == known:
            rows.append({'candidate': candidate.as_dict(), 'status': 'excluded_goal_or_duplicate'})
            continue
        shape = analyze((known, candidate), conclusion)
        rows.append({'candidate': candidate.as_dict(), 'status': 'hypothesis_not_fact',
                     'shape': shape,
                     'finite_check': find_countermodel((known, candidate), conclusion,
                                                       max_size, nonempty)})
    return rows


def implication_chain_rows():
    """Existence-sentence truth values, not term extensions or AEIO premises."""
    return [{'H': h, 'N': n, 'S': s,
             'premises': ((not h) or n) and ((not n) or s),
             'conclusion': (not h) or s}
            for h, n, s in product((False, True), repeat=3)]
