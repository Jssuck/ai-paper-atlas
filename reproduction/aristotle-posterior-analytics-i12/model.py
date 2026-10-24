"""Original finite teaching models for Posterior Analytics I.12, not historical algorithms."""
from itertools import product
import json


def mask(value, n=3):
    if type(n) is not int or n < 1:
        raise ValueError('n must be a positive integer')
    if type(value) is not int or not 0 <= value < (1 << n):
        raise ValueError('mask outside finite universe')
    return value


def included(a, b, n=3):
    """All members of a belong to b; empty a is allowed and reported separately."""
    return mask(a, n) & ~mask(b, n) == 0


def shared_attribute(a, b, attribute, n=3):
    return included(a, attribute, n) and included(b, attribute, n)


def same_middle(left, right):
    """Pairs are (surface spelling, stipulated sense ID); spelling is not identity."""
    for term in (left, right):
        if not isinstance(term, tuple) or len(term) != 2 or any(type(x) is not str or not x for x in term):
            raise ValueError('term must contain two nonempty strings')
    return left[1] == right[1]


def question_route(science, question_domain, role, bridges=()):
    """Classify explicit declarations only, never truth or scientific appropriateness."""
    if any(type(x) is not str or not x for x in (science, question_domain)):
        raise ValueError('domains must be nonempty strings')
    if role not in ('principle', 'derived', 'foreign'):
        raise ValueError('unknown question role')
    if not isinstance(bridges, (tuple, list)):
        raise ValueError('bridges must be an explicit sequence')
    for pair in bridges:
        if not isinstance(pair, tuple) or len(pair) != 2 or any(type(x) is not str or not x for x in pair):
            raise ValueError('invalid bridge declaration')
    if role == 'foreign':
        return 'outside-declared-scope'
    if question_domain != science and (science, question_domain) not in bridges:
        return 'outside-declared-scope'
    if role == 'principle':
        return 'principle-not-proved-here'
    return 'eligible-for-domain-explanation'


def closure(nodes, edges):
    """Transitive reflexive closure of stipulated inclusion edges, not causal knowledge."""
    if not isinstance(nodes, (set, frozenset)) or not nodes or any(type(x) is not str or not x for x in nodes):
        raise ValueError('nodes must be a nonempty set of labels')
    relation = {(x, x) for x in nodes}
    for edge in edges:
        if not isinstance(edge, tuple) or len(edge) != 2 or any(x not in nodes for x in edge):
            raise ValueError('edge outside declared nodes')
        relation.add(edge)
    for k in sorted(nodes):
        for i in sorted(nodes):
            for j in sorted(nodes):
                if (i, k) in relation and (k, j) in relation:
                    relation.add((i, j))
    return relation


def set_included(a, b, n):
    """Independent pointwise oracle rather than a bitwise subset expression."""
    return all(not ((a >> i) % 2) or ((b >> i) % 2) for i in range(n))


def reachable_oracle(nodes, edges):
    out = set()
    for origin in nodes:
        seen, pending = {origin}, [origin]
        while pending:
            current = pending.pop()
            for left, right in edges:
                if left == current and right not in seen:
                    seen.add(right)
                    pending.append(right)
        out.update((origin, x) for x in seen)
    return out


def enumerate_models():
    n = 3
    shared_valid = shared_counter = shared_nonempty_counter = 0
    subset_mismatch = chain_counter = 0
    for a, b, c in product(range(1 << n), repeat=3):
        subset_mismatch += included(a, b, n) != set_included(a, b, n)
        if shared_attribute(a, b, c, n):
            shared_valid += 1
            if not included(a, b, n):
                shared_counter += 1
                shared_nonempty_counter += bool(a and b)
        if included(a, b, n) and included(b, c, n) and not included(a, c, n):
            chain_counter += 1
    reverse_counter = reverse_nonempty = equivalent_counter = 0
    for a, b in product(range(1 << n), repeat=2):
        if included(a, b, n) and not included(b, a, n):
            reverse_counter += 1
            reverse_nonempty += bool(a and b)
        if included(a, b, n) and included(b, a, n) and a != b:
            equivalent_counter += 1
    nodes = {'a', 'b', 'c'}
    candidates = list(product(sorted(nodes), repeat=2))
    closure_mismatch = 0
    for bits in range(1 << len(candidates)):
        edges = {edge for k, edge in enumerate(candidates) if bits & (1 << k)}
        closure_mismatch += closure(nodes, edges) != reachable_oracle(nodes, edges)
    return {
        'universe_size': n, 'triples_checked': 512, 'pairs_checked': 64,
        'subset_oracle_mismatches': subset_mismatch,
        'shared_attribute_premise_models': shared_valid,
        'shared_attribute_inclusion_countermodels': shared_counter,
        'shared_attribute_nonempty_countermodels': shared_nonempty_counter,
        'valid_chain_countermodels': chain_counter,
        'reverse_inclusion_countermodels': reverse_counter,
        'reverse_inclusion_nonempty_countermodels': reverse_nonempty,
        'two_way_inclusion_inequality_countermodels': equivalent_counter,
        'graphs_checked': 512, 'closure_oracle_mismatches': closure_mismatch,
        'scope': 'finite teaching checks; no certification of historical science, causal truth or all models'
    }


if __name__ == '__main__':
    print(json.dumps(enumerate_models(), ensure_ascii=False, indent=2, sort_keys=True))
