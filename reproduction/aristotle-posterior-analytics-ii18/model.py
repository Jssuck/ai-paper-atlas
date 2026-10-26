"""II.18 teaching reconstruction, not a real-world causal inference algorithm.

Edges are declared explanatory steps. Validation checks their finite extensional
truth, NOT explanatory appropriateness, scientific necessity or immediacy.
"""
from dataclasses import dataclass
from itertools import product
import json


@dataclass(frozen=True)
class ChainCertificate:
    """Ordered named terms, subject first and property last."""
    path: tuple[str, ...]

    def __post_init__(self):
        if not isinstance(self.path, tuple):
            raise TypeError('path must be a tuple')
        if len(self.path) < 2:
            raise ValueError('a certificate needs distinct subject and target names')
        if not all(isinstance(term, str) and term for term in self.path):
            raise ValueError('terms must be nonempty names')
        if len(set(self.path)) != len(self.path):
            raise ValueError('repeated names are not an acyclic explanatory chain')

    @property
    def subject(self):
        return self.path[0]

    @property
    def target(self):
        return self.path[-1]

    @property
    def internal_middles(self):
        return self.path[1:-1]

    @property
    def nearest_declared_reason(self):
        # The length-two endpoint convention represents the subject itself,
        # not an extra middle, self-causation, or a proof of the direct premise.
        return self.path[1] if self.internal_middles else self.subject

    def suffix(self, subject):
        """Re-ask the same target question for a later subject on this chain."""
        index = self.path.index(subject)
        return ChainCertificate(self.path[index:])


def validate(certificate, extensions, declared_edges):
    """Return finite relation evidence or raise; does NOT certify causality."""
    edges = frozenset(declared_edges)
    for term in certificate.path:
        if term not in extensions:
            raise ValueError('missing extension: ' + term)
        if not isinstance(extensions[term], (set, frozenset)):
            raise TypeError('extensions must be sets or frozensets')
    for source, target in zip(certificate.path, certificate.path[1:]):
        if (source, target) not in edges:
            raise ValueError('undeclared step: ' + source + ' -> ' + target)
        if not extensions[source] <= extensions[target]:
            raise ValueError('false finite inclusion: ' + source + ' -> ' + target)
    return {
        'subject': certificate.subject,
        'target': certificate.target,
        'finite_inclusion_holds': extensions[certificate.subject] <= extensions[certificate.target],
        'subject_nonempty': bool(extensions[certificate.subject]),
        'internal_middles': list(certificate.internal_middles),
        'nearest_declared_reason': certificate.nearest_declared_reason,
        'direct_endpoint_convention': not bool(certificate.internal_middles),
        'certifies_real_explanation': False,
    }


def finite_middle_candidates(subject, target, extensions, names):
    """Check only S <= M <= T; order/causation cannot be read from this list."""
    return tuple(name for name in names
                 if name not in (subject, target)
                 and extensions[subject] <= extensions[name] <= extensions[target])


def nearest_choices(certificates, subject, target):
    """Reasons across supplied structural certificates, not all possible paths.

Use validate first if their finite truth is also required. Empty input means no
supplied support, not proof that no explanation exists.
"""
    choices = set()
    for certificate in certificates:
        if certificate.subject != subject or certificate.target != target:
            raise ValueError('mixed questions')
        choices.add(certificate.nearest_declared_reason)
    return frozenset(choices)


def transitive_closure(edges):
    """Derived inclusion reachability; never a source of primitive causes."""
    closure = set(edges)
    while True:
        new = {(a, d) for a, b in closure for c, d in closure if b == c}
        if new <= closure:
            return frozenset(closure)
        closure |= new


def enumerate_four_sets(universe_size=3):
    """Exhaust all A/B/C/D extensions over a fixed finite labelled universe."""
    if isinstance(universe_size, bool) or not isinstance(universe_size, int) or not 0 <= universe_size <= 4:
        raise ValueError('enumeration supports integer sizes 0 through 4')
    subsets = [frozenset(i for i in range(universe_size) if bits & (1 << i))
               for bits in range(1 << universe_size)]
    total = valid = nonempty = counterexamples = 0
    for a, b, c, d in product(subsets, repeat=4):
        total += 1
        if d <= c <= b <= a:
            valid += 1
            nonempty += bool(d)
            counterexamples += not (d <= a and d <= c <= a and d <= b <= a)
    return {'universe_size': universe_size, 'assignments': total,
            'chain_satisfying': valid, 'nonempty_subject': nonempty,
            'transitivity_counterexamples': counterexamples}


def demo():
    ext = {'D': {0}, 'C': {0, 1}, 'B': {0, 1, 2}, 'A': {0, 1, 2, 3}}
    declared = {('D', 'C'), ('C', 'B'), ('B', 'A')}
    chain = ChainCertificate(('D', 'C', 'B', 'A'))
    records = [validate(chain.suffix(s), ext, declared) for s in ('D', 'C', 'B')]
    # Same external result, distinct declared explanations. E is coextensive
    # with C only for this deliberately constructed teaching example.
    branch_ext = dict(ext, E={0, 1})
    branch_edges = declared | {('D', 'E'), ('E', 'B')}
    other = ChainCertificate(('D', 'E', 'B', 'A'))
    validate(other, branch_ext, branch_edges)
    closure = transitive_closure(declared)
    return {'chain_questions': records,
            'extension_only_middles_for_D_A': finite_middle_candidates('D', 'A', ext, ('C', 'B')),
            'branch_choices': sorted(nearest_choices([chain, other], 'D', 'A')),
            'closure_adds_D_A_shortcut': ('D', 'A') in closure,
            'declared_has_D_A_shortcut': ('D', 'A') in declared,
            'enumeration': enumerate_four_sets()}


if __name__ == '__main__':
    print(json.dumps(demo(), ensure_ascii=False, indent=2))
