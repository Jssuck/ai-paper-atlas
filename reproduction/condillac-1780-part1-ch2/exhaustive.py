"""Finite cross-check against a separately written brute-force assignment oracle.

The oracle never uses graph traversal, path summation, production vector
helpers, or the production consistency flag to decide equation satisfaction.
This is algorithmic independence, not a claim of independent authorship.
"""
import json
from itertools import combinations, product

from model import ObservationBook, Relation, reconstruct


def require(condition, details):
    """Verification remains active under python -O and -OO."""
    if not condition:
        raise AssertionError(details)


def check_family(dimension, edge_values, coordinate_bound):
    names = ("A", "B", "C")
    pairs = tuple(combinations(names, 2))
    edge_vectors = tuple(product(edge_values, repeat=dimension))
    states = (None,) + edge_vectors
    points = tuple(product(range(-coordinate_bound, coordinate_bound + 1), repeat=dimension))
    assignments = tuple({"A": (0,) * dimension, "B": b, "C": c}
                        for b, c in product(points, repeat=2))
    counts = {"dimension": dimension, "vertices": 3,
              "edge_coordinate_values": list(edge_values),
              "oracle_coordinate_bound": coordinate_bound,
              "graph_cases": 0, "consistent_graphs": 0, "inconsistent_graphs": 0,
              "brute_force_assignments": 0, "pair_queries": 0,
              "reversed_graph_checks": 0}
    for choices in product(states, repeat=3):
        edges = tuple(Relation(u, v, displacement)
                      for (u, v), displacement in zip(pairs, choices)
                      if displacement is not None)
        book = ObservationBook(names, dimension, names, edges)
        actual = reconstruct(book)
        counts["graph_cases"] += 1
        solutions = []
        # Evaluate original equations directly on every bounded assignment.
        for candidate in assignments:
            counts["brute_force_assignments"] += 1
            satisfies = all(all(candidate[e.v][axis] - candidate[e.u][axis] == e.offset[axis]
                                for axis in range(dimension)) for e in edges)
            if satisfies:
                solutions.append(candidate)
            # Independently compare the solver's *entire* represented family
            # with equation satisfaction within this finite test domain.
            if actual.consistent:
                relative = dict(actual.coordinates)
                represented = all(
                    all(candidate[v][axis] == relative[v][axis] + candidate[component[0]][axis]
                        for axis in range(dimension))
                    for component in actual.components for v in component)
            else:
                represented = False
            require(represented == satisfies, (dimension, choices, candidate, "family"))
        require(actual.consistent == bool(solutions), (dimension, choices, "existence"))
        counts["consistent_graphs" if solutions else "inconsistent_graphs"] += 1
        if solutions:
            for u, v in pairs:
                displacements = {tuple(s[v][axis] - s[u][axis] for axis in range(dimension))
                                 for s in solutions}
                expected = next(iter(displacements)) if len(displacements) == 1 else None
                require(actual.difference(u, v) == expected, (dimension, choices, u, v, "pair"))
                counts["pair_queries"] += 1
        else:
            require(not actual.coordinates, (dimension, choices, "inconsistent output"))
        reversed_edges = tuple(Relation(e.v, e.u, tuple(-z for z in e.offset)) for e in edges)
        reversed_result = reconstruct(ObservationBook(names, dimension, names, reversed_edges))
        require(reversed_result.consistent == actual.consistent, (dimension, choices, "reverse consistency"))
        require(reversed_result.coordinates == actual.coordinates, (dimension, choices, "reverse positions"))
        require(reversed_result.components == actual.components, (dimension, choices, "reverse components"))
        counts["reversed_graph_checks"] += 1
    return counts


def run_exhaustive():
    families = [check_family(1, (-2, -1, 0, 1, 2), 4),
                check_family(2, (-1, 0, 1), 2)]
    return {"status": "PASS",
            "scope": "3 labeled vertices; each of 3 unordered pairs absent or one listed offset",
            "oracle": "direct bounded assignment enumeration; no production graph solver helpers",
            "families": families,
            "totals": {key: sum(f[key] for f in families) for key in
                       ("graph_cases", "consistent_graphs", "inconsistent_graphs",
                        "brute_force_assignments", "pair_queries", "reversed_graph_checks")}}


if __name__ == "__main__":
    print(json.dumps(run_exhaustive(), ensure_ascii=False, indent=2))
