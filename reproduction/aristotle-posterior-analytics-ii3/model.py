"""Finite teaching models for Posterior Analytics II.3, not essence discovery."""
from dataclasses import dataclass
from itertools import product
import json


def powerset(n):
    if type(n) is not int or n < 0:
        raise ValueError('n must be a nonnegative integer')
    return tuple(frozenset(i for i in range(n) if mask & (1 << i))
                 for mask in range(1 << n))


def composition(a, b):
    """Interpret a stipulated conjunction extensionally, not as a real essence."""
    return frozenset(a) & frozenset(b)


def pair_counts(n):
    sets = powerset(n)
    pairs = list(product(sets, repeat=2))
    return {'n': n, 'pairs': len(pairs),
            'both_inclusions_fail': sum(not a <= b and not b <= a for a, b in pairs),
            'formula': 4**n - 2 * 3**n + 2**n,
            'composition_failures': sum(any(x not in a or x not in b for x in composition(a,b))
                                        for a,b in pairs)}


def inheritance(subclass, subject, attribute):
    """Return truth of premises and conclusion; never labels essence."""
    s,t,p = map(frozenset, (subclass, subject, attribute))
    return {'premises': s <= t and t <= p, 'conclusion': s <= p}


@dataclass(frozen=True)
class Goal:
    kind: str
    subject: str
    content: str
    def __post_init__(self):
        if self.kind not in ('definition', 'attribute'):
            raise ValueError('unknown goal kind')
        if not isinstance(self.subject, str) or not self.subject:
            raise ValueError('subject must be a nonempty string')
        if not isinstance(self.content, str) or not self.content:
            raise ValueError('content must be a nonempty string')


def matches_target(certificate_goal, requested_goal):
    """Metadata check only: matching labels do NOT certify truth or knowledge."""
    if not isinstance(certificate_goal, Goal) or not isinstance(requested_goal, Goal):
        raise TypeError('both targets must be Goal records')
    return certificate_goal == requested_goal


def dependency_order(n, edges):
    """Edges (premise, conclusion). Return roots and order; reject cycles.

    This tests finite well-founded structure only, not inference validity.
    """
    if type(n) is not int or n < 0:
        raise ValueError('n must be a nonnegative integer')
    edges = set(edges)
    for edge in edges:
        if (not isinstance(edge, tuple) or len(edge) != 2 or
                any(type(v) is not int or v < 0 or v >= n for v in edge)):
            raise ValueError('edge endpoints must be known integer nodes')
    incoming = {i: set() for i in range(n)}
    outgoing = {i: set() for i in range(n)}
    for a,b in edges:
        incoming[b].add(a)
        outgoing[a].add(b)
    roots = tuple(i for i in range(n) if not incoming[i])
    pending = list(roots)
    order = []
    while pending:
        node = pending.pop(0)
        order.append(node)
        for target in sorted(outgoing[node]):
            incoming[target].remove(node)
            if not incoming[target]:
                pending.append(target)
        pending.sort()
    if len(order) != n:
        raise ValueError('cyclic dependency is not a well-founded finite proof')
    return {'roots': roots, 'order': tuple(order)}


def graph_counts(n=3):
    if type(n) is not int or not 0 <= n <= 4:
        raise ValueError('enumeration limited to 0..4 nodes')
    possible = tuple((i,j) for i in range(n) for j in range(n) if i != j)
    counts = {'n': n, 'graphs': 0, 'acyclic': 0, 'cyclic': 0,
              'rootless': 0, 'nonempty_acyclic_rootless': 0}
    for bits in product((0,1), repeat=len(possible)):
        edges = tuple(e for e,bit in zip(possible,bits) if bit)
        counts['graphs'] += 1
        rootless = n > 0 and all(any(b == node for _,b in edges) for node in range(n))
        counts['rootless'] += rootless
        try:
            dependency_order(n, edges)
        except ValueError:
            counts['cyclic'] += 1
        else:
            counts['acyclic'] += 1
            counts['nonempty_acyclic_rootless'] += rootless
    return counts


def demo():
    a,b = frozenset((0,1)),frozenset((1,2))
    result = {'pair_counts': pair_counts(3),
              'component_example': {'a': sorted(a), 'b': sorted(b),
                                    'intersection': sorted(composition(a,b)),
                                    'a_subset_b': a <= b, 'b_subset_a': b <= a},
              'inheritance_example': inheritance({0}, {0,1}, {0,1,2}),
              'attribute_is_definition': matches_target(Goal('attribute','triangle','angle_sum'),
                                                       Goal('definition','triangle','angle_sum')),
              'graph_counts': graph_counts(3),
              'chain': dependency_order(3, ((0,1),(1,2))),
              'limitations': 'finite structural checks do not certify essence, true premises, scientific knowledge, or infinite regress'}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    demo()
