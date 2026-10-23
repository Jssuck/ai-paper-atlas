"""Original finite teaching model for Prior Analytics II.11; Python stdlib only.

U(P,S) means every S is P. This is modern extensional semantics, not a
claim to uniquely recover Aristotle's semantics or to prove a theorem by testing.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
import json
from pathlib import Path

FORMS = 'UEIO'
NEG = dict(U='O', E='I', I='E', O='U')

@dataclass(frozen=True)
class Proposition:
    form: str
    predicate: str
    subject: str
    def __post_init__(self):
        if self.form not in tuple(FORMS) or self.predicate not in tuple('ABC') or self.subject not in tuple('ABC'):
            raise ValueError('Unsupported proposition')
    def negate(self):
        return Proposition(NEG[self.form], self.predicate, self.subject)
    def __str__(self):
        return f'{self.form}({self.predicate},{self.subject})'

def models(nonempty_terms=False):
    """All nonempty supports of 8 membership types, each represented once.

    Type t has A bit 0, B bit 1, C bit 2. Multiplicity is immaterial only
    for this restricted one-place, equality-free categorical language.
    """
    for mask in range(1, 256):
        model = {name: frozenset(t for t in range(8) if mask & (1 << t) and t & (1 << bit))
                 for bit, name in enumerate('ABC')}
        if not nonempty_terms or all(model.values()):
            yield mask, model

def truth(p, model):
    pred, sub = model[p.predicate], model[p.subject]
    if p.form == 'U': return sub <= pred
    if p.form == 'E': return not (sub & pred)
    if p.form == 'I': return bool(sub & pred)
    return bool(sub - pred)

def witness(mask, model):
    return {'support': [t for t in range(8) if mask & (1 << t)],
            'A': sorted(model['A']), 'B': sorted(model['B']), 'C': sorted(model['C'])}

def implication(premises, conclusion, space):
    """Return a smallest-support countermodel, if one exists, and antecedent count."""
    satisfying = [(mask, m) for mask, m in space if all(truth(p, m) for p in premises)]
    bad = [(mask, m) for mask, m in satisfying if not truth(conclusion, m)]
    bad.sort(key=lambda pair: (pair[0].bit_count(), pair[0]))
    return (witness(*bad[0]) if bad else None), len(satisfying)

def route(goal_form, position, extra_form, result_form):
    goal = Proposition(goal_form, 'A', 'B')
    hypothesis = goal.negate()
    if position == 'major':
        extra = Proposition(extra_form, 'B', 'C')
        result = Proposition(result_form, 'A', 'C')
        major, minor = hypothesis, extra
    elif position == 'minor':
        extra = Proposition(extra_form, 'C', 'A')
        result = Proposition(result_form, 'C', 'B')
        major, minor = extra, hypothesis
    else:
        raise ValueError('Position must be major or minor')
    return goal, hypothesis, extra, result, major, minor

def classify(nonempty_terms=False):
    space = list(models(nonempty_terms))
    rows = []
    for q, pos, x, r in product(FORMS, ('major', 'minor'), FORMS, FORMS):
        goal, h, extra, result, major, minor = route(q, pos, x, r)
        ce, count = implication([h, extra], result, space)
        closure_ce, background_count = implication([extra, result.negate()], goal, space)
        valid = ce is None and count > 0
        rows.append({'id': f'{q}-{pos}-{x}-{r}', 'goal': str(goal), 'hypothesis': str(h),
                     'extra': str(extra), 'internal_result': str(result),
                     'known_background': str(result.negate()),
                     'mood': major.form + minor.form + result.form,
                     'internal_valid': valid, 'internal_antecedent_models': count,
                     'internal_countermodel': ce, 'background_models': background_count,
                     'discharge_valid': closure_ce is None,
                     'discharge_countermodel': closure_ce,
                     'certificate': valid and closure_ce is None and background_count > 0})
    return {'model_count': len(space), 'candidate_count': len(rows),
            'certificates_by_goal': {q: sum(row['certificate'] and row['id'].startswith(q+'-') for row in rows) for q in FORMS},
            'rows': rows}

def named_checks():
    P = Proposition
    empty = list(models(False)); occupied = list(models(True))
    cases = [
        ('I-universal-background-needs-C', [P('U','B','C'), P('U','A','C')], P('I','A','B')),
        ('I-particular-B-C', [P('I','B','C'), P('U','A','C')], P('I','A','B')),
        ('E-positive-C-A', [P('U','C','A'), P('E','C','B')], P('E','A','B')),
        ('E-negative-C-A', [P('E','C','A'), P('U','C','B')], P('E','A','B')),
        ('O-positive-C-A', [P('U','C','A'), P('O','C','B')], P('O','A','B')),
        ('O-negative-C-A', [P('E','C','A'), P('I','C','B')], P('O','A','B')),
        ('O-B-side-universal', [P('U','B','C'), P('O','A','C')], P('O','A','B')),
        ('O-B-side-particular', [P('I','B','C'), P('E','A','C')], P('O','A','B')),
        ('not-E-does-not-give-U', [P('I','A','B')], P('U','A','B')),
        ('not-U-does-not-give-E', [P('O','A','B')], P('E','A','B')),
        ('I-is-not-negation-of-O', [P('I','A','B')], P('U','A','B')),
    ]
    out = []
    for label, premises, conclusion in cases:
        record = {'id': label, 'premises': list(map(str,premises)), 'conclusion': str(conclusion)}
        for policy, space in [('empty_allowed',empty),('all_terms_nonempty',occupied)]:
            ce, count = implication(premises, conclusion, space)
            record[policy] = {'valid': ce is None, 'antecedent_models': count, 'countermodel': ce}
        out.append(record)
    # Explicitly separate a true mixed I/O target from a contradictory background.
    mixed = {'A': frozenset([7]), 'B': frozenset([6,7]), 'C': frozenset([6,7])}
    out.append({'id':'mixed-case', 'model': witness((1<<7)|(1<<6),mixed),
                'I_A_B':truth(P('I','A','B'),mixed), 'O_A_B':truth(P('O','A','B'),mixed),
                'U_C_A':truth(P('U','C','A'),mixed), 'I_C_B':truth(P('I','C','B'),mixed),
                'E_C_B':truth(P('E','C','B'),mixed)})
    return out

def main():
    result = {'scope':'One internal first-figure syllogism, three categorical terms, exact contradictory background.',
              'not_claimed':'Full ancient semantics, natural-language truth, arbitrary multi-step impossibility.',
              'empty_allowed': classify(False), 'all_terms_nonempty': classify(True),
              'named_checks': named_checks()}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__': main()
