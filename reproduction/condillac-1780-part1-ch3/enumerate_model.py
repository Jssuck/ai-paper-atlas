"""Exact finite census. This is not an empirical or historical experiment."""
from __future__ import annotations

import json
from collections import defaultdict
from math import comb

from model import display, evaluate, generate_trees, leaf_bag, leaf_count, ordered_leaves, parse, serialize


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def census() -> dict:
    levels = {n: generate_trees(n) for n in range(1, 5)}
    domain = tuple(tree for level in levels.values() for tree in level)
    # This closed-form oracle is independent of the generator recurrence.
    closed_form = {n: comb(2 * (n - 1), n - 1) // n * 2 ** (n - 1) * 3 ** n for n in levels}
    recurrence = {1: 3}
    for n in range(2, 5):
        recurrence[n] = 2 * sum(recurrence[k] * recurrence[n - k] for k in range(1, n))
    require(all(len(levels[n]) == closed_form[n] == recurrence[n] for n in levels), "counts disagree")
    require(len(domain) == 3477, "unexpected total domain size")
    prefixes = [serialize(tree) for tree in domain]
    require(len(set(prefixes)) == len(domain), "generator duplicated a syntax tree")
    require(all(parse(serialize(tree)) == tree for tree in domain), "tree round trip failed")
    require(all(serialize(parse(prefix)) == prefix for prefix in prefixes), "prefix round trip failed")

    projections = {"full_prefix": serialize, "ordered_leaves": ordered_leaves, "leaf_bag": leaf_bag, "integer_output": evaluate}
    stats = {}
    for name, key in projections.items():
        groups = defaultdict(list)
        for tree in domain:
            groups[key(tree)].append(tree)
        sizes = [len(group) for group in groups.values()]
        stats[name] = {
            "classes": len(groups),
            "singleton_classes": sum(size == 1 for size in sizes),
            "collision_classes": sum(size > 1 for size in sizes),
            "colliding_unordered_pairs": sum(size * (size - 1) // 2 for size in sizes),
            "largest_class": max(sizes),
            "minimal_structural_collision": minimal_collision(groups),
        }
    return {
        "scope": "Original modern syntactic teaching model; no empirical or historical-algorithm claim.",
        "leaf_alphabet": [0, 1, 2],
        "operations": ["ADD", "SUB"],
        "leaf_counts": {str(n): len(levels[n]) for n in levels},
        "closed_form_counts": {str(n): closed_form[n] for n in levels},
        "recurrence_counts": {str(n): recurrence[n] for n in levels},
        "total": len(domain),
        "unique_full_prefixes": len(set(prefixes)),
        "tree_round_trips": len(domain),
        "prefix_round_trips": len(domain),
        "output_values": sorted(set(evaluate(tree) for tree in domain)),
        "output_histogram": {str(value): sum(evaluate(tree) == value for tree in domain)
                             for value in sorted(set(evaluate(tree) for tree in domain))},
        "projections": stats,
        "minimality_rule": "Minimize (maximum leaf count, sum of leaf counts, first tree rank, second tree rank); tree rank is (leaf count, typed prefix), with the pair sorted by tree rank.",
    }


def minimal_collision(groups: dict) -> dict | None:
    # Within a key-class, its first two members in tree-rank order give the
    # least pair under the stated rule. Then minimize across all key-classes.
    candidates = []
    for group in groups.values():
        if len(group) < 2:
            continue
        ordered = sorted(group, key=lambda tree: (leaf_count(tree), serialize(tree)))
        a, b = ordered[:2]
        ar, br = (leaf_count(a), serialize(a)), (leaf_count(b), serialize(b))
        candidates.append(((max(ar[0], br[0]), ar[0] + br[0], ar, br), a, b))
    if not candidates:
        return None
    rank, a, b = min(candidates, key=lambda entry: entry[0])
    return {
        "first": display(a), "second": display(b),
        "first_prefix": serialize(a), "second_prefix": serialize(b),
        "first_output": evaluate(a), "second_output": evaluate(b),
        "max_leaves": rank[0], "sum_leaves": rank[1],
    }


if __name__ == "__main__":
    print(json.dumps(census(), ensure_ascii=False, indent=2))
