"""Original bounded teaching model for Prior Analytics I.23, Python standard library.

No claim to recover a unique ancient semantics or prove a general theorem by testing.
"""
from dataclasses import dataclass
from math import gcd


def _int(x, name, lo, hi):
    if type(x) is not int or not lo <= x <= hi:
        raise ValueError(f'{name} must be an integer in [{lo}, {hi}]')
    return x


@dataclass(frozen=True)
class Model:
    """One representative for each occupied membership atom; domain is nonempty."""
    terms: tuple
    occupied_mask: int

    def __post_init__(self):
        if type(self.terms) is not tuple or not 1 <= len(self.terms) <= 4:
            raise ValueError('terms must be a tuple of 1..4 distinct names')
        if any(type(t) is not str or not t or not t.isidentifier() for t in self.terms):
            raise ValueError('term names must be nonempty identifiers')
        if len(set(self.terms)) != len(self.terms):
            raise ValueError('duplicate term name')
        _int(self.occupied_mask, 'occupied_mask', 1, (1 << (1 << len(self.terms))) - 1)

    def extension(self, term):
        if type(term) is not str or term not in self.terms:
            raise ValueError('unknown term')
        k = self.terms.index(term)
        return frozenset(a for a in range(1 << len(self.terms))
                         if self.occupied_mask & (1 << a) and a & (1 << k))

    def holds(self, quality, predicate, subject):
        if type(quality) is not str or quality not in ('A', 'E', 'I', 'O'):
            raise ValueError('quality must be A/E/I/O')
        p, s = self.extension(predicate), self.extension(subject)
        return {'A': s <= p, 'E': s.isdisjoint(p),
                'I': bool(s & p), 'O': bool(s - p)}[quality]


def all_models(terms=('P', 'M', 'S'), require_nonempty_terms=False):
    if type(require_nonempty_terms) is not bool:
        raise ValueError('require_nonempty_terms must be bool')
    Model(terms, 1)  # Validate even before enumeration.
    for mask in range(1, 1 << (1 << len(terms))):
        m = Model(terms, mask)
        if not require_nonempty_terms or all(m.extension(t) for t in terms):
            yield m


def entails(premises, conclusion, require_nonempty_terms=False):
    """Three-term, finite atom-complete AEIO semantics; returns first countermodel."""
    if type(premises) is not tuple or not premises:
        raise ValueError('premises must be a nonempty tuple')
    if type(conclusion) is not tuple or len(conclusion) != 3:
        raise ValueError('conclusion must be a proposition tuple')
    if any(type(x) is not tuple or len(x) != 3 for x in (*premises, conclusion)):
        raise ValueError('propositions must be (quality, predicate, subject) tuples')
    probe = Model(('P', 'M', 'S'), 1)
    for proposition in (*premises, conclusion):
        probe.holds(*proposition)
    for m in all_models(require_nonempty_terms=require_nonempty_terms):
        if all(m.holds(*x) for x in premises) and not m.holds(*conclusion):
            return False, m.occupied_mask
    return True, None


def skeleton(edges):
    """Classify two directed subject->predicate edges; no validity claim.

    Reverse chain is figure I only after exchanging the extremal roles.
    With a fixed S-to-P conclusion it is NOT identified as ordinary figure I.
    """
    if type(edges) is not tuple or len(edges) != 2:
        raise ValueError('edges must be a pair')
    if any(type(e) is not tuple or len(e) != 2 or
           any(type(t) is not str or t not in ('S', 'M', 'P') for t in e) or
           e[0] == e[1] for e in edges):
        raise ValueError('bad directed edge')
    e = frozenset(edges)
    patterns = {
        frozenset((('S', 'M'), ('M', 'P'))): 'chain_forward',
        frozenset((('P', 'M'), ('M', 'S'))): 'chain_reverse',
        frozenset((('S', 'M'), ('P', 'M'))): 'common_predicate',
        frozenset((('M', 'S'), ('M', 'P'))): 'common_subject',
    }
    if e not in patterns:
        raise ValueError('not a distinct two-edge S-M-P skeleton')
    return patterns[e]


def check_chain(model, chain):
    """Check antecedent and conclusion for directed all-A chain, no search."""
    if type(model) is not Model or type(chain) is not tuple or len(chain) < 2:
        raise ValueError('Model and tuple chain required')
    for t in chain:
        model.extension(t)
    if len(set(chain)) != len(chain):
        raise ValueError('chain names must be distinct')
    premises = all(model.holds('A', chain[i+1], chain[i]) for i in range(len(chain)-1))
    return {'premises': premises, 'conclusion': model.holds('A', chain[-1], chain[0])}


def raa_certificate(model, premise, negated_target, derived):
    """Validate one internal AEIO contradiction witness, not the outer proof.

    derived must be the pointwise contradictory form of negated_target.
    All premises true is NOT required: a contradiction has no such model.
    This function checks syntactic discharge pairing and model truth values;
    it cannot infer derived from premise, nor establish validity of a RAA proof.
    """
    if type(model) is not Model:
        raise ValueError('Model required')
    for x in (premise, negated_target, derived):
        if type(x) is not tuple or len(x) != 3:
            raise ValueError('proposition tuple required')
        model.holds(*x)
    opposites = {'A': 'O', 'O': 'A', 'E': 'I', 'I': 'E'}
    paired = derived[0] == opposites[negated_target[0]] and derived[1:] == negated_target[1:]
    return {'contradictory_pair': paired,
            'premise_true': model.holds(*premise),
            'assumption_true': model.holds(*negated_target),
            'derived_true': model.holds(*derived),
            'outer_discharge_verified': False}


def parity_probe(limit):
    """Bounded diagnostics only; no finite bound proves sqrt(2) irrational."""
    _int(limit, 'limit', 1, 1000)
    failures = []
    reduced_solutions = []
    checks = 0
    for n in range(limit+1):
        checks += 1
        if (n*n) % 2 == 0 and n % 2 != 0:
            failures.append(n)
    for p in range(1, limit+1):
        for q in range(1, limit+1):
            if p*p == 2*q*q and gcd(p,q) == 1:
                reduced_solutions.append([p,q])
    return {'limit':limit, 'parity_checks': checks, 'positive_pairs':limit*limit,
            'parity_failures':failures, 'reduced_solutions':reduced_solutions,
            'general_irrationality_proved':False}
