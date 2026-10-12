"""Independent finite checks of article claims, using no production-model imports.

These checks are finite witnesses, not replacements for the written general proofs.
Run: python3 audit/argument_oracle.py
"""
from collections import deque
from fractions import Fraction
from itertools import product
import json


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def tree_checks():
    domain = tuple(product((0, 1), repeat=2))
    leaves = (("leaf", 0), ("leaf", 1))
    depth_one = leaves + tuple(("branch", p, l, r)
        for p in range(2) for l in leaves for r in leaves)
    trees = leaves + tuple(("branch", p, l, r)
        for p in range(2) for l in depth_one for r in depth_one)
    def run(tree, item):
        cost = 0
        while tree[0] != "leaf":
            tree = tree[2 + item[tree[1]]]
            cost += 1
        return tree[1], cost
    # Bottom-up table construction is independent of path-walking run().
    def compile_table(tree):
        if tree[0] == "leaf":
            return {item: tree[1] for item in domain}
        left, right = compile_table(tree[2]), compile_table(tree[3])
        return {item: (left if item[tree[1]] == 0 else right)[item]
                for item in domain}
    comparisons = 0
    for tree in trees:
        table = compile_table(tree)
        for item in domain:
            check(run(tree, item)[0] == table[item], "tree semantics")
            comparisons += 1
    xor_tree = ("branch", 0, ("branch", 1, leaves[0], leaves[1]),
                            ("branch", 1, leaves[1], leaves[0]))
    wrong_tree = ("branch", 0, ("branch", 1, leaves[0], leaves[1]),
                              ("branch", 1, leaves[1], leaves[1]))
    check(sum(run(xor_tree, x)[1] for x in domain) == 8, "XOR build cost")
    risk = Fraction(sum(run(wrong_tree, x)[0] != (x[0] ^ x[1]) for x in domain), 4)
    check(risk == Fraction(1, 4), "error preserved")
    check(run(leaves[0], domain[0])[1] == 0, "root leaf cost")
    # No unseen-point impossibility theorem with a singleton label set.
    singleton_truths = tuple(product((0,), repeat=2))
    check(len(singleton_truths) == 1, "singleton-label counterexample")
    return {"tree_specs": len(trees), "pointwise_checks": comparisons,
            "XOR_compilation_predicate_queries": 8,
            "wrong_tree_risk": str(risk), "root_leaf_queries": 0,
            "singleton_label_hypothesis_necessary": True}


def formula(codes, labels, weights):
    total = sum(weights)
    error = 0
    for code in set(codes):
        ids = [i for i, v in enumerate(codes) if v == code]
        mass = sum(weights[i] for i in ids)
        masses = [sum(weights[i] for i in ids if labels[i] == a) for a in (0, 1)]
        error += mass - max(masses)
    return Fraction(error, total)


def brute(codes, labels, weights):
    code_values = sorted(set(codes))
    risks, all_correct = [], False
    for values in product((0, 1), repeat=len(code_values)):
        decoder = dict(zip(code_values, values))
        wrong = tuple(decoder[codes[i]] != labels[i] for i in range(len(labels)))
        all_correct |= not any(wrong)
        risks.append(Fraction(sum(w for w, bad in zip(weights, wrong) if bad), sum(weights)))
    return min(risks), all_correct


def representation_checks():
    cases = 0
    for n in range(1, 5):
        for codes in product((0, 1), repeat=n):
            for labels in product((0, 1), repeat=n):
                fiber_ok = all(len({labels[i] for i in range(n) if codes[i] == z}) <= 1
                               for z in set(codes))
                for weights in product((0, 1, 2), repeat=n):
                    if not sum(weights):
                        continue
                    expected, all_correct = brute(codes, labels, weights)
                    support_ok = all(len({labels[i] for i in range(n)
                                         if codes[i] == z and weights[i] > 0}) <= 1
                                     for z in set(codes))
                    check(formula(codes, labels, weights) == expected, "minimum risk")
                    check(fiber_ok == all_correct, "fiber necessity/sufficiency")
                    check(support_ok == (expected == 0), "zero-weight support")
                    cases += 1
    refinements = 0
    n = 3
    for fine in product(range(3), repeat=n):
        for coarse in product((0, 1), repeat=n):
            if any(fine[i] == fine[j] and coarse[i] != coarse[j]
                   for i in range(n) for j in range(n)):
                continue
            for labels in product((0, 1), repeat=n):
                for weights in product((0, 1, 2), repeat=n):
                    if not sum(weights):
                        continue
                    check(formula(fine, labels, weights) <= formula(coarse, labels, weights),
                          "refinement monotonicity")
                    refinements += 1
    check(formula((0, 0, 0), (0, 0, 1), (2, 1, 3)) == Fraction(1, 2), "weighted example")
    check(formula((0, 0, 1, 1), (0, 0, 1, 1), (1, 1, 1, 1)) == 0, "source example")
    check(formula((0, 0, 1, 1), (0, 1, 0, 1), (1, 1, 1, 1)) == Fraction(1, 2), "target example")
    return {"weighted_domains_checked": cases, "refinement_instances_checked": refinements,
            "weight_alphabet": [0, 1, 2], "labels": [0, 1],
            "weighted_example_minimum_risk": "1/2", "transfer_example_minimum_risk": "1/2"}


def histories(n, edges, seeds):
    result = [frozenset(seeds)]
    for _ in range(n + 1):
        old = result[-1]
        new = old | {v for u, v in edges if u in old}
        result.append(frozenset(new))
    return result


def bfs(n, edges, seeds):
    adjacency = {v: [] for v in range(n)}
    for u, v in edges:
        adjacency[u].append(v)
    distances = {v: 0 for v in seeds}
    queue = deque(seeds)
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if v not in distances:
                distances[v] = distances[u] + 1
                queue.append(v)
    return distances


def graph_checks():
    graphs = cases = additions = 0
    for n in range(4):
        possible_edges = tuple(product(range(n), repeat=2))
        for bits in product((0, 1), repeat=len(possible_edges)):
            edges = {edge for edge, selected in zip(possible_edges, bits) if selected}
            graphs += 1
            for seed_bits in product((0, 1), repeat=n):
                seeds = {v for v in range(n) if seed_bits[v]}
                series = histories(n, edges, seeds)
                distances = bfs(n, edges, seeds)
                for t, reached in enumerate(series):
                    check(reached == {v for v, distance in distances.items() if distance <= t},
                          "path correspondence")
                check(series[-1] == series[-2], "finite stabilization")
                cases += 1
                for extra in set(possible_edges) - edges:
                    expanded = histories(n, edges | {extra}, seeds)
                    check(all(old <= new for old, new in zip(series, expanded)), "edge monotonicity")
                    additions += 1
    chain = {(0, 1), (1, 2), (2, 3)}
    check(bfs(4, chain, {0})[3] == 3, "chain arrival")
    check(bfs(4, chain | {(0, 3)}, {0})[3] == 1, "shortcut arrival")
    return {"directed_graphs_including_self_loops": graphs,
            "graph_seed_instances_checked": cases,
            "single_edge_additions_checked": additions,
            "node_counts": [0, 1, 2, 3], "chain_last_arrival": 3,
            "shortcut_last_node_arrival": 1}


def main():
    print(json.dumps({"status": "PASS", "scope": "Independent finite mathematical witnesses; no production model import; not empirical psychology or a general proof.",
                      "tree": tree_checks(), "representation": representation_checks(),
                      "diffusion": graph_checks()}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
