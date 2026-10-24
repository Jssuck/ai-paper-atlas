"""Modern teaching models, not an implementation of Aristotle's whole logic."""
from dataclasses import dataclass
from itertools import product
import json

@dataclass(frozen=True, order=True)
class Literal:
    predicate_id: str
    positive: bool = True
    def __post_init__(self):
        if not isinstance(self.predicate_id, str) or not self.predicate_id:
            raise ValueError('predicate_id must be a nonempty string')
        if type(self.positive) is not bool:
            raise ValueError('positive must be bool')

@dataclass(frozen=True)
class Rule:
    antecedents: frozenset
    consequent: Literal
    def __post_init__(self):
        if not isinstance(self.antecedents, frozenset) or not all(isinstance(x, Literal) for x in self.antecedents):
            raise ValueError('antecedents must be a frozenset of literals')
        if not isinstance(self.consequent, Literal):
            raise ValueError('consequent must be a literal')

def closure(facts, rules):
    """Positive and negative support are distinct atoms. No explosion or contraposition."""
    known = set(facts)
    if not all(isinstance(x, Literal) for x in known):
        raise ValueError('facts must be literals')
    rules = tuple(rules)
    if not all(isinstance(x, Rule) for x in rules):
        raise ValueError('rules must be Rule objects')
    while True:
        additions = {r.consequent for r in rules if r.antecedents <= known}
        if additions <= known:
            return frozenset(known)
        known.update(additions)

def support_status(known, predicate_id):
    return (Literal(predicate_id, True) in known, Literal(predicate_id, False) in known)

VALUES = ('F', 'U', 'T')
def neg(value):
    if value not in VALUES:
        raise ValueError('expected F/U/T')
    return {'F':'T', 'U':'U', 'T':'F'}[value]
def disj(left, right):
    if left not in VALUES or right not in VALUES:
        raise ValueError('expected F/U/T')
    return VALUES[max(VALUES.index(left), VALUES.index(right))]
def cases_exhaustive(allowed, cases):
    allowed, cases = set(allowed), set(cases)
    if not allowed or not allowed <= set(VALUES) or not cases <= set(VALUES):
        raise ValueError('nonempty allowed subset and cases subset of F/U/T required')
    return allowed <= cases

def graph_oracle(seed_mask, edge_mask, n=4):
    """Independent transitive reachability matrix for unary-rule special case."""
    edges = [(i,j) for i in range(n) for j in range(n) if i != j]
    reach = [[i == j for j in range(n)] for i in range(n)]
    for k,(i,j) in enumerate(edges):
        if edge_mask & (1 << k):
            reach[i][j] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
    return {j for j in range(n) if any(seed_mask & (1<<i) and reach[i][j] for i in range(n))}

def enumerate_checks():
    atoms = [Literal('human', True), Literal('human', False), Literal('animal', True), Literal('animal', False)]
    edges = [(i,j) for i in range(4) for j in range(4) if i != j]
    differences = 0
    checks = 0
    for edge_mask in range(1 << len(edges)):
        rules = [Rule(frozenset([atoms[i]]), atoms[j]) for k,(i,j) in enumerate(edges) if edge_mask & (1 << k)]
        for seed in range(16):
            got = closure([atoms[i] for i in range(4) if seed & (1<<i)], rules)
            expected = {atoms[i] for i in graph_oracle(seed,edge_mask)}
            differences += got != expected
            checks += 1
    lem = {v: disj(v,neg(v)) for v in VALUES}
    return {'unary_graph_seed_cases': checks, 'oracle_differences':differences,
            'lem_K3':lem, 'classical_TF_cases_exhaustive':cases_exhaustive(('T','F'),('T','F')),
            'K3_TF_cases_exhaustive':cases_exhaustive(VALUES,('T','F'))}

if __name__ == '__main__':
    result=enumerate_checks()
    if result['oracle_differences']:
        raise RuntimeError('independent graph oracle mismatch')
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
