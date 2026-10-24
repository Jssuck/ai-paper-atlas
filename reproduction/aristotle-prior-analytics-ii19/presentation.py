"""Modern positive-inclusion teaching model for Prior Analytics II.19.

An edge (S, P) means every S is P. No psychological prediction is made.
"""
from collections import Counter, deque
from itertools import permutations
import json

CHAIN = (("B", "A"), ("C", "B"), ("D", "C"), ("E", "D"), ("F", "E"))
# Source specifies AB, DE, BC; the last two positions are our completion.
SEPARATED = (CHAIN[0], CHAIN[3], CHAIN[1], CHAIN[4], CHAIN[2])


def normalize(edges):
    """Materialize once; reject malformed edges; duplicate premises are idempotent."""
    result = []
    for edge in edges:
        if not isinstance(edge, (list, tuple)) or len(edge) != 2:
            raise ValueError("an edge must be a pair")
        s, p = edge
        if not all(isinstance(x, str) and x for x in (s, p)):
            raise ValueError("terms must be nonempty strings")
        if s == p:
            raise ValueError("explicit reflexive premises are outside this model")
        if (s, p) not in result:
            result.append((s, p))
    return tuple(result)


def witness(edges, source, target):
    """Shortest non-reflexive consequence certificate, or None.

    Reflexivity is valid in inclusion semantics but deliberately not reported.
    """
    edges = normalize(edges)
    if source == target:
        return None
    graph = {}
    for s, p in edges:
        graph.setdefault(s, set()).add(p)
    queue = deque([(source,)])
    seen = {source}
    while queue:
        path = queue.popleft()
        for nxt in sorted(graph.get(path[-1], ())):
            if nxt == target:
                return path + (nxt,)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(path + (nxt,))
    return None


def closure(edges):
    edges = normalize(edges)
    terms = sorted({x for edge in edges for x in edge})
    return frozenset((s, p) for s in terms for p in terms
                     if s != p and witness(edges, s, p) is not None)


def profile(order):
    """Descriptive presentation metrics, not measures of persuasion or deception."""
    order = normalize(order)
    return {
        "order": [list(edge) for edge in order],
        "adjacent_shared_term_pairs": sum(bool(set(a) & set(b))
                                         for a, b in zip(order, order[1:])),
        "prefix_closure_sizes": [len(closure(order[:i])) for i in range(1, len(order)+1)],
        "prefix_target_available": [("F", "A") in closure(order[:i])
                                    for i in range(1, len(order)+1)],
        "final_target_witness": witness(order, "F", "A"),
    }


def main():
    orders = list(permutations(CHAIN))
    histogram = Counter(profile(order)["adjacent_shared_term_pairs"] for order in orders)
    data = {
        "model": "positive universal inclusions; nonreflexive closure",
        "permutations": len(orders),
        "target_valid_in_all_orders": all(("F", "A") in closure(o) for o in orders),
        "final_closure_sizes": sorted({len(closure(o)) for o in orders}),
        "adjacency_histogram": dict(sorted(histogram.items())),
        "chain_order": profile(CHAIN),
        "source_prefix_with_modern_completion": profile(SEPARATED),
        "shared_middle_not_sufficient": {
            "premises": [["B", "A"], ["B", "C"]],
            "A_to_C": witness((("B", "A"), ("B", "C")), "A", "C"),
            "C_to_A": witness((("B", "A"), ("B", "C")), "C", "A"),
        },
        "one_middle_both_orders": [len(closure(o)) for o in permutations(CHAIN[:2])],
    }
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
