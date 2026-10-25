"""Finite educational strict orders; not a model of scientific explanation."""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
import json


def natural(value, name, maximum):
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= maximum:
        raise ValueError(f'{name} must be an integer in 0..{maximum}')
    return value


class StrictOrder:
    """Transitive closure of a finite DAG, with nodes numbered 0 through n-1."""
    def __init__(self, n, edges):
        natural(n, 'n', 128)
        relation = set()
        for edge in edges:
            if not isinstance(edge, (tuple, list)) or len(edge) != 2:
                raise ValueError('each edge must be a pair')
            a, b = edge
            natural(a, 'edge endpoint', n - 1)
            natural(b, 'edge endpoint', n - 1)
            if a == b:
                raise ValueError('self edges violate strictness')
            relation.add((a, b))
        # Floyd-Warshall reachability, independent of input edge/node ordering.
        for k in range(n):
            for a in range(n):
                if (a, k) in relation:
                    for b in range(n):
                        if (k, b) in relation:
                            relation.add((a, b))
        if any((a, a) in relation for a in range(n)):
            raise ValueError('cycles violate strictness')
        self.n = n
        self.relation = frozenset(relation)

    def middle(self, lower, upper):
        natural(lower, 'lower', self.n - 1)
        natural(upper, 'upper', self.n - 1)
        if (lower, upper) not in self.relation:
            raise ValueError('endpoints must be strictly ordered')
        return tuple(v for v in range(self.n)
                     if (lower, v) in self.relation and (v, upper) in self.relation)

    def interval(self, lower, upper):
        middle = self.middle(lower, upper)
        vertices = (lower,) + middle + (upper,)
        total = all((a, b) in self.relation or (b, a) in self.relation
                    for a, b in combinations(vertices, 2))

        @lru_cache(None)
        def distance(v):
            if v == upper:
                return 0
            return 1 + max(distance(w) for w in vertices if (v, w) in self.relation)

        return {'lower': lower, 'upper': upper, 'middle': list(middle),
                'middle_count': len(middle), 'is_total': total,
                'longest_edges': distance(lower)}


def diamond(m):
    """m incomparable candidates between bottom=0 and top=m+1; m>=1."""
    natural(m, 'm', 126)
    if m == 0:
        raise ValueError('diamond needs at least one middle')
    return StrictOrder(m + 2, [(0, i) for i in range(1, m + 1)]
                       + [(i, m + 1) for i in range(1, m + 1)])


def dyadic_prefix(steps):
    """Exact finite values 0,1/2,3/4,...,1-2**(-steps),1."""
    natural(steps, 'steps', 256)
    return (Fraction(0),) + tuple(Fraction(2**k - 1, 2**k)
                                for k in range(1, steps + 1)) + (Fraction(1),)


def buffered_prefix(steps):
    """A finite sample of {-1} union ([0,1] intersect Q), not its enumeration."""
    return (Fraction(-1),) + dyadic_prefix(steps)


def enumerate_forward_dags(n=4):
    natural(n, 'n', 5)
    possible = list(combinations(range(n), 2))
    closures = set()
    intervals = total_intervals = nontotal_intervals = failures = 0
    excess = 0
    for mask in range(1 << len(possible)):
        edges = [e for i, e in enumerate(possible) if mask & (1 << i)]
        order = StrictOrder(n, edges)
        closures.add(order.relation)
        for lower, upper in sorted(order.relation):
            info = order.interval(lower, upper)
            intervals += 1
            if info['is_total']:
                total_intervals += 1
                if info['middle_count'] != info['longest_edges'] - 1:
                    failures += 1
            else:
                nontotal_intervals += 1
                excess = max(excess, info['middle_count'] - info['longest_edges'] + 1)
    return {'nodes': n, 'forward_edge_slots': len(possible),
            'raw_dags': 1 << len(possible), 'distinct_transitive_closures': len(closures),
            'ordered_interval_occurrences': intervals, 'total_interval_occurrences': total_intervals,
            'nontotal_interval_occurrences': nontotal_intervals,
            'total_interval_identity_failures': failures,
            'maximum_middle_count_minus_chain_internals': excess,
            'scope': 'All edge subsets compatible with the fixed order 0<1<...; closure duplicates retained in interval counts.'}


def report():
    samples = []
    for m in (1, 2, 8, 32):
        info = diamond(m).interval(0, m + 1)
        samples.append({k: info[k] for k in ('middle_count', 'is_total', 'longest_edges')})
    prefix = buffered_prefix(8)
    return {'enumeration': enumerate_forward_dags(), 'diamonds': samples,
            'buffered_dyadic_sample': {'steps': 8, 'values': [str(q) for q in prefix],
                                       'last_inserted': str(prefix[-2]),
                                       'remaining_gap_to_1': str(1 - prefix[-2]),
                                       'next_midpoint': str((prefix[-2] + 1) / 2)},
            'limitations': ['Finite checks do not establish an infinite theorem.',
                           'Candidate width is not chain depth.',
                           'No scientific, causal, modal, or essential predication is certified.']}


if __name__ == '__main__':
    print(json.dumps(report(), ensure_ascii=False, indent=2))
