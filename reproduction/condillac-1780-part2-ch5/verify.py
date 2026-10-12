"""Dedicated tests, independent finite oracles, and semantic mutations."""
import ast
from itertools import permutations, product
import json
from pathlib import Path
import sys
import unittest
from named_classes import ClassSystem, InvalidGraph
from semantic_probes import CheckFailure, check
import mutation_check
import test_named_classes


def exhaustive():
    objects, labels = ("x", "y"), ("A", "B", "C")
    positions = tuple((a, b) for a in range(3) for b in range(3) if a != b)
    totals = dict(extension_assignments=0, graph_contexts=0, valid_graphs=0,
                  invalid_graphs=0, reachability_queries=0, semantic_queries=0,
                  certified_queries=0, true_unencoded_queries=0,
                  failed_inclusions=0, mutual_reachability_pairs=0,
                  renamed_valid_graphs=0, renamed_queries=0)
    for masks in product(range(4), repeat=3):
        totals["extension_assignments"] += 1
        extensions = tuple(frozenset(objects[i] for i in range(2) if mask & (1 << i)) for mask in masks)
        for graph_mask in range(64):
            edges_i = tuple(edge for k, edge in enumerate(positions) if graph_mask & (1 << k))
            edges = tuple((labels[a], labels[b]) for a, b in edges_i)
            system = ClassSystem(objects, labels, extensions, edges)
            totals["graph_contexts"] += 1
            # Integer bit masks establish semantic truth without calling system.includes.
            valid = all((masks[a] & ~masks[b]) == 0 for a, b in edges_i)
            check((not system.violations()) == valid, "edge validity differs from bit-mask oracle")
            # Floyd-Warshall computes distances without any call to the implementation's BFS.
            distance = [[0 if a == b else 99 for b in range(3)] for a in range(3)]
            for a, b in edges_i:
                distance[a][b] = 1
            for k in range(3):
                for a in range(3):
                    for b in range(3):
                        distance[a][b] = min(distance[a][b], distance[a][k] + distance[k][b])
            expected_groups = []
            assigned = set()
            for a in range(3):
                if a not in assigned:
                    group = tuple(b for b in range(3) if distance[a][b] < 99 and distance[b][a] < 99)
                    expected_groups.append(tuple(labels[b] for b in group))
                    assigned.update(group)
            check(system.components() == tuple(expected_groups), "SCC partition differs from matrix oracle")
            totals["valid_graphs" if valid else "invalid_graphs"] += 1
            if not valid:
                try:
                    system.prove("A", "A")
                except InvalidGraph:
                    pass
                else:
                    raise CheckFailure("invalid graph was certified")
            for a in range(3):
                for b in range(3):
                    source, target = labels[a], labels[b]
                    truth = (masks[a] & ~masks[b]) == 0
                    totals["semantic_queries"] += 1
                    check(system.includes(source, target) == truth, "subset result differs from mask oracle")
                    expected_witness = next((objects[i] for i in range(2)
                                             if (masks[a] & (1 << i)) and not (masks[b] & (1 << i))), None)
                    check(system.witness(source, target) == expected_witness, "wrong witness or order")
                    totals["failed_inclusions"] += not truth
                    path = system.find_path(source, target)
                    reachable = distance[a][b] < 99
                    totals["reachability_queries"] += 1
                    check((path is not None) == reachable, "BFS differs from matrix reachability")
                    if path is not None:
                        check(path[0] == source and path[-1] == target, "wrong path endpoints")
                        check(len(path) - 1 == distance[a][b], "path is not shortest")
                        check(len(set(path)) == len(path), "path repeats a vertex")
                        check(all(edge in edges for edge in zip(path, path[1:])), "path invents an edge")
                    if valid:
                        totals["certified_queries"] += 1
                        check(system.prove(source, target) == path, "certified path differs from raw path")
                        check(not reachable or truth, "valid graph derived a false inclusion")
                        totals["true_unencoded_queries"] += truth and not reachable
                        if reachable and distance[b][a] < 99:
                            totals["mutual_reachability_pairs"] += 1
                            check(masks[a] == masks[b], "valid cycle has unequal extensions")
            if valid:
                for new_labels in permutations(("P", "Q", "R")):
                    renamed = system.rename(new_labels)
                    totals["renamed_valid_graphs"] += 1
                    check(renamed.objects == objects and renamed.extensions == extensions, "rename changes world or E")
                    mapping = dict(zip(labels, new_labels))
                    for a in range(3):
                        for b in range(3):
                            old_path = system.find_path(labels[a], labels[b])
                            expected = None if old_path is None else tuple(mapping[x] for x in old_path)
                            check(renamed.prove(new_labels[a], new_labels[b]) == expected, "rename breaks proof transport")
                            check(renamed.includes(new_labels[a], new_labels[b]) == ((masks[a] & ~masks[b]) == 0), "rename breaks truth")
                            totals["renamed_queries"] += 1
    return totals


def main():
    print("RUNTIME " + json.dumps({"optimization_level": sys.flags.optimize,
                                   "python_version": sys.version,
                                   "python_executable": sys.executable}, sort_keys=True))
    for path in Path(__file__).parent.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        check(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)), f"optimization-sensitive assert in {path.name}")
    try:
        check(False, "failure-path control")
    except CheckFailure:
        pass
    else:
        raise RuntimeError("verification failure path is broken")
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_named_classes)
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    check(result.wasSuccessful(), "dedicated unit tests failed")
    counts = exhaustive()
    expected_counts = {
        "extension_assignments": 64, "graph_contexts": 4096,
        "valid_graphs": 904, "invalid_graphs": 3192,
        "reachability_queries": 36864, "semantic_queries": 36864,
        "certified_queries": 8136, "true_unencoded_queries": 1620,
        "failed_inclusions": 10752, "mutual_reachability_pairs": 3564,
        "renamed_valid_graphs": 5424, "renamed_queries": 48816,
    }
    check(counts == expected_counts, f"enumeration coverage changed: {counts}")
    mutation = mutation_check.run()
    print("EXHAUSTIVE " + json.dumps(counts, sort_keys=True))
    print("MUTATION " + json.dumps(mutation, sort_keys=True))
    print("PASS: unit tests, finite oracles, semantic mutants, controls, and no-assert audit")


if __name__ == "__main__":
    main()
