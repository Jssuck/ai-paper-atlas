"""Own finite-model teaching reconstruction of Prior Analytics II.7.
Not an edition, historical implementation, or proof by enumeration.
Predicate-first: A(X,Y) means all Y are X. No external dependencies.
"""
from dataclasses import dataclass
from itertools import product
import json


def categorical(kind, x, y):
    if kind == 'A':
        return y <= x
    if kind == 'E':
        return not x & y
    if kind == 'I':
        return bool(x & y)
    if kind == 'O':
        return bool(y - x)
    raise ValueError('unknown categorical kind')


@dataclass(frozen=True)
class Proposition:
    kind: str
    predicate: str
    subject: str

    def __post_init__(self):
        if self.kind not in 'AEIO' or len(self.kind) != 1:
            raise ValueError('kind must be A, E, I, or O')
        if not self.predicate or not self.subject:
            raise ValueError('term names must be nonempty')


def darii(universal, particular):
    """One ordered schema only: A(X,M), I(M,Y) -> I(X,Y)."""
    if universal.kind != 'A' or particular.kind != 'I' or universal.subject != particular.predicate:
        raise ValueError('premises do not match this Darii schema')
    return Proposition('I', universal.predicate, particular.subject)


def disamis(universal, particular):
    """One ordered schema only: A(Y,M), I(X,M) -> I(X,Y)."""
    if universal.kind != 'A' or particular.kind != 'I' or universal.subject != particular.subject:
        raise ValueError('premises do not match this Disamis schema')
    return Proposition('I', particular.predicate, universal.predicate)


def convert_i(proposition):
    if proposition.kind != 'I':
        raise ValueError('this explicit conversion handles only I')
    return Proposition('I', proposition.subject, proposition.predicate)


def models(size, nonempty_terms=False):
    if not isinstance(size, int) or isinstance(size, bool) or size < 1:
        raise ValueError('domain size must be a positive integer')
    universe = frozenset(range(size))
    subsets = [frozenset(i for i in universe if mask & (1 << i)) for mask in range(2 ** size)]
    if nonempty_terms:
        subsets = [s for s in subsets if s]
    for a, b, c in product(subsets, repeat=3):
        yield universe, a, b, c


def rules(u, a, b, c):
    A = lambda x, y: categorical('A', x, y)
    E = lambda x, y: categorical('E', x, y)
    I = lambda x, y: categorical('I', x, y)
    O = lambda x, y: categorical('O', x, y)
    # Every entry is (premise conjunction, target). Naming distinguishes
    # genuine implications from intentionally invalid recovery proposals.
    return {
        'original_darapti_with_C_existence': (A(a,c) and A(b,c) and bool(c), I(a,b)),
        'original_felapton_with_C_existence': (E(a,c) and A(b,c) and bool(c), O(a,b)),
        'original_datisi': (A(a,c) and I(b,c), I(a,b)),
        'original_disamis': (A(b,c) and I(a,c), I(a,b)),
        'original_bocardo': (A(b,c) and O(a,c), O(a,b)),
        'original_ferison': (E(a,c) and I(b,c), O(a,b)),
        'major_universal_reverse_gives_converse_I': (A(c,a) and I(a,b), I(c,b)),
        'major_universal_reverse_semantic_target_I': (A(c,a) and I(a,b), I(b,c)),
        'minor_universal_reverse_recovers_I': (A(c,b) and I(a,b), I(a,c)),
        'minor_universal_reverse_recovers_O': (A(c,b) and O(a,b), O(a,c)),
        'negative_coverage_bridge_recovers_I': (O(a,b) and (u-a <= c), I(b,c)),
        'negative_shared_witness_bridge_recovers_I': (O(a,b) and bool((b-a)&c), I(b,c)),
        'invalid_darapti_without_existence': (A(a,c) and A(b,c), I(a,b)),
        'invalid_felapton_without_existence': (E(a,c) and A(b,c), O(a,b)),
        'invalid_recover_universal_A': (I(a,b) and A(c,b), A(a,c)),
        'invalid_recover_universal_E': (O(a,b) and A(c,b), E(a,c)),
        'invalid_negative_simple_conversion': (O(a,b) and E(c,a), I(b,c)),
        'invalid_independent_some_bridge': (O(a,b) and I(c,u-a), I(b,c)),
    }


def audit(max_size=4):
    if not isinstance(max_size, int) or isinstance(max_size, bool) or not 1 <= max_size <= 6:
        raise ValueError('max_size must be an integer from 1 to 6')
    report = {'scope': 'finite set semantics; no general theorem claimed', 'max_domain_size': max_size, 'regimes': {}}
    for nonempty in (False, True):
        counts = {}
        total = 0
        for size in range(1, max_size+1):
            for u,a,b,c in models(size, nonempty):
                total += 1
                for name,(premises,target) in rules(u,a,b,c).items():
                    row = counts.setdefault(name, {'premise_models':0, 'countermodels':0, 'first_countermodel':None})
                    if premises:
                        row['premise_models'] += 1
                        if not target:
                            row['countermodels'] += 1
                            if row['first_countermodel'] is None:
                                row['first_countermodel'] = {'U':sorted(u),'A':sorted(a),'B':sorted(b),'C':sorted(c)}
        for name,row in counts.items():
            if not name.startswith('invalid_') and (row['countermodels'] or not row['premise_models']):
                raise RuntimeError('failed or vacuous intended implication: '+name)
        report['regimes']['all_terms_nonempty' if nonempty else 'empty_terms_allowed'] = {'total_models':total,'rules':counts}
    p = darii(Proposition('A','C','A'), Proposition('I','A','B'))
    q = convert_i(p)
    report['ordered_syntax_demo'] = {'darii_result':p.__dict__, 'target':q.__dict__, 'same_ordered_proposition':p == q, 'conversion_step_required_by_this_trace':p != q}
    return report


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2, sort_keys=True))
