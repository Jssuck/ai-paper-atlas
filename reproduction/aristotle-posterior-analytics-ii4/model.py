"""Original finite teaching model for Posterior Analytics II.4.

No extensional computation certifies essence or epistemic independence.
The role rules below are declared conventions, not a full Aristotelian calculus.
"""
from dataclasses import dataclass
from itertools import product

ROLES = ('attribute', 'essential_part', 'full_definition')


def classify_chain(c, b, a):
    """Return extensional facts only; never infer a semantic role."""
    c, b, a = frozenset(c), frozenset(b), frozenset(a)
    valid = c <= b and b <= a
    return {'chain': valid, 'conclusion': c <= a,
            'endpoints_equal': c == a, 'all_equal': c == b == a}


@dataclass(frozen=True)
class Premise:
    subject: str
    predicate: str
    role: str
    sources: tuple

    def __post_init__(self):
        if not all(isinstance(x, str) and x.strip() for x in (self.subject, self.predicate)):
            raise ValueError('Term names must be nonempty strings')
        if self.role not in ROLES:
            raise ValueError('Unknown declared role')
        if not isinstance(self.sources, tuple) or not self.sources or not all(
                isinstance(x, str) and x.strip() for x in self.sources):
            raise ValueError('Supply a nonempty tuple of explicit source labels')


def compose(minor, major, extensions, target_source='target:C-definition'):
    """Check a two-premise certificate, including its declared source labels.

    Full-definition labels must at least pass equal-extension checks. This is
    necessary only in this model and is NOT sufficient for actual definition.
    """
    if not isinstance(minor, Premise) or not isinstance(major, Premise):
        raise TypeError('Expected two Premise records')
    if minor.predicate != major.subject:
        raise ValueError('Middle term mismatch')
    if not isinstance(target_source, str) or not target_source.strip():
        raise ValueError('Target source label must be nonempty')
    for p in (minor, major):
        if p.subject not in extensions or p.predicate not in extensions:
            raise ValueError('Missing term extension')
        s, t = frozenset(extensions[p.subject]), frozenset(extensions[p.predicate])
        if not s <= t:
            raise ValueError('False universal premise in supplied finite domain')
        if p.role == 'full_definition' and s != t:
            raise ValueError('Full-definition label fails extensional minimum')
    rank = min(ROLES.index(minor.role), ROLES.index(major.role))
    sources = sorted(set(minor.sources) | set(major.sources))
    return {'subject': minor.subject, 'predicate': major.predicate,
            'declared_result_role': ROLES[rank], 'sources': sources,
            'explicit_target_dependency': target_source in sources,
            'minor_already_declares_subject_definition': minor.role == 'full_definition',
            'actual_essence_certified': False}


def enumerate_chains(max_n=4):
    if type(max_n) is not int or not 0 <= max_n <= 6:
        raise ValueError('max_n must be an integer from 0 to 6')
    out = {'triples': 0, 'chains': 0, 'nonempty_c_chains': 0,
           'equal_endpoint_chains': 0, 'nonempty_equal_endpoint_chains': 0,
           'transitivity_failures': 0, 'sandwich_failures': 0,
           'chains_without_endpoint_equality': 0}
    for n in range(max_n + 1):
        subsets = [frozenset(i for i in range(n) if mask >> i & 1)
                   for mask in range(1 << n)]
        for c, b, a in product(subsets, repeat=3):
            out['triples'] += 1
            r = classify_chain(c, b, a)
            if r['chain']:
                out['chains'] += 1
                out['nonempty_c_chains'] += bool(c)
                out['transitivity_failures'] += not r['conclusion']
                if r['endpoints_equal']:
                    out['equal_endpoint_chains'] += 1
                    out['nonempty_equal_endpoint_chains'] += bool(c)
                    out['sandwich_failures'] += not r['all_equal']
                else:
                    out['chains_without_endpoint_equality'] += 1
    return out


def independent_oracle(max_n=4):
    """Count directly from per-object membership bits, not classify_chain."""
    out = {'triples': 0, 'chains': 0, 'nonempty_c_chains': 0,
           'equal_endpoint_chains': 0, 'nonempty_equal_endpoint_chains': 0,
           'transitivity_failures': 0, 'sandwich_failures': 0,
           'chains_without_endpoint_equality': 0}
    for n in range(max_n + 1):
        for assignment in product(range(8), repeat=n):
            out['triples'] += 1
            # Membership bits: bit0 C, bit1 B, bit2 A.
            chain = all(not (x & 1) or bool(x & 2) for x in assignment) and all(
                not (x & 2) or bool(x & 4) for x in assignment)
            if not chain:
                continue
            nonempty = any(x & 1 for x in assignment)
            eq = all(bool(x & 1) == bool(x & 4) for x in assignment)
            out['chains'] += 1
            out['nonempty_c_chains'] += nonempty
            out['transitivity_failures'] += any(x & 1 and not x & 4 for x in assignment)
            out['chains_without_endpoint_equality'] += not eq
            if eq:
                out['equal_endpoint_chains'] += 1
                out['nonempty_equal_endpoint_chains'] += nonempty
                out['sandwich_failures'] += any(
                    not (bool(x & 1) == bool(x & 2) == bool(x & 4)) for x in assignment)
    return out


def examples():
    ext = {'C': {0}, 'B': {0}, 'A': {0}}
    reports = []
    for r1, r2 in product(ROLES, repeat=2):
        reports.append(compose(Premise('C', 'B', r1, ('minor',)),
                               Premise('B', 'A', r2, ('major',)), ext))
    return reports


if __name__ == '__main__':
    import json
    print(json.dumps({'finite_enumeration': enumerate_chains(),
                      'independent_oracle': independent_oracle(),
                      'same_extensions_nine_role_pairs': examples()}, indent=2))
