"""Independent finite review: simple-path oracle, boundaries, semantic transport.

Run from the package root. This deliberately does not import verify.py or its
oracles. An explicit ReviewFailure remains active under -O and -OO.
"""
from collections import Counter
from dataclasses import FrozenInstanceError
from hashlib import sha256
from itertools import permutations, product
import ast
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from named_classes import ClassSystem, InvalidGraph, prototype_accepts
import mutation_check


class ReviewFailure(Exception):
    pass


COUNTS = Counter()


def require(condition, message):
    if not condition:
        raise ReviewFailure(message)


def reject(error_type, function, name):
    try:
        function()
    except error_type:
        COUNTS["rejected_cases"] += 1
    except Exception as error:
        raise ReviewFailure(f"{name}: wrong exception {type(error).__name__}") from None
    else:
        raise ReviewFailure(f"{name}: unexpectedly accepted")


def reference_paths(labels, edges, start):
    """Enumerate simple paths by depth-first recursion, never by BFS.

    For each endpoint minimize (number of edges, sequence of input edge ranks).
    The lexicographic tie rule is the ordered-neighbor BFS first-discovery rule.
    """
    best = {}
    rank = {edge: index for index, edge in enumerate(edges)}

    def visit(path):
        key = (len(path) - 1, tuple(rank[e] for e in zip(path, path[1:])))
        prior = best.get(path[-1])
        if prior is None or key < prior[0]:
            best[path[-1]] = (key, path)
        for a, b in edges:
            if a == path[-1] and b not in path:
                visit(path + (b,))

    visit((start,))
    return {target: best[target][1] if target in best else None for target in labels}


def check_graph(labels, edges, counter):
    system = ClassSystem((), labels, (frozenset(),) * len(labels), edges)
    expected = {a: reference_paths(labels, edges, a) for a in labels}
    groups = []
    assigned = set()
    for a in labels:
        if a not in assigned:
            group = tuple(b for b in labels if expected[a][b] is not None and expected[b][a] is not None)
            groups.append(group)
            assigned.update(group)
    require(system.components() == tuple(groups), "SCC partition differs from simple paths")
    for a, b in product(labels, repeat=2):
        path = expected[a][b]
        require(system.find_path(a, b) == path, "shortest path or edge-order tie differs")
        require(system.prove(a, b) == path, "valid-graph certification differs")
        COUNTS[counter + "_queries"] += 1
    COUNTS[counter + "_graphs"] += 1


def graph_cases():
    labels = ("A", "B", "C", "D")
    positions = tuple((a, b) for a in labels for b in labels if a != b)
    for mask in range(1 << len(positions)):
        edges = tuple(edge for k, edge in enumerate(positions) if mask & (1 << k))
        check_graph(labels, edges, "four_label_loopless")
    shapes = ((), (("A", "B"), ("B", "C"), ("C", "D")),
              (("A", "B"), ("B", "A"), ("C", "D"), ("D", "C")),
              (("A", "C"), ("A", "B"), ("C", "D"), ("B", "D")))
    for edges in shapes:
        for mask in range(16):
            loops = tuple((a, a) for i, a in enumerate(labels) if mask & (1 << i))
            check_graph(labels, loops + edges, "self_loop")
    diamond = (("A", "C"), ("A", "B"), ("C", "D"), ("B", "D"))
    for edges in permutations(diamond):
        check_graph(labels, edges, "diamond_edge_order")


def semantic_cases():
    objects = ("z", "a", "m")
    labels = ("A", "B")
    positions = tuple(product(labels, repeat=2))
    for left_mask, right_mask in product(range(8), repeat=2):
        memberships = tuple(tuple(bool(mask & (1 << i)) for i in range(3))
                            for mask in (left_mask, right_mask))
        extensions = tuple(frozenset(obj for obj, present in zip(objects, row) if present)
                           for row in memberships)
        for edge_mask in range(16):
            edges = tuple(edge for i, edge in enumerate(positions) if edge_mask & (1 << i))
            expected_witnesses = {}
            for a, b in positions:
                row_a, row_b = memberships[labels.index(a)], memberships[labels.index(b)]
                expected_witnesses[a, b] = next((objects[i] for i in range(3) if row_a[i] and not row_b[i]), None)
            expected_bad = tuple((a, b, expected_witnesses[a, b]) for a, b in edges
                                 if expected_witnesses[a, b] is not None)
            s = ClassSystem(objects, labels, extensions, edges)
            require(s.violations() == expected_bad, "ordered violations differ")
            for new_labels in (("P", "Q"), ("B", "A")):
                renamed = s.rename(new_labels)
                mapping = dict(zip(labels, new_labels))
                require(renamed.objects == objects and renamed.extensions == extensions,
                        "renaming changed universe or extensions")
                require(renamed.edges == tuple((mapping[a], mapping[b]) for a, b in edges),
                        "renaming did not transport ordered edges")
                require(renamed.violations() == tuple((mapping[a], mapping[b], w) for a, b, w in expected_bad),
                        "bad-graph rename changed validity or witnesses")
                require(renamed.components() == tuple(tuple(mapping[a] for a in component) for component in s.components()),
                        "renaming did not transport SCCs")
                for a, b in positions:
                    expected = expected_witnesses[a, b]
                    require(s.includes(a, b) == (expected is None), "semantic membership formula differs")
                    require(s.witness(a, b) == expected, "object-order witness differs")
                    require(renamed.includes(mapping[a], mapping[b]) == (expected is None), "rename changed truth")
                    require(renamed.witness(mapping[a], mapping[b]) == expected, "rename changed witness")
                    old_path = reference_paths(labels, edges, a)[b]
                    new_path = None if old_path is None else tuple(mapping[x] for x in old_path)
                    require(renamed.find_path(mapping[a], mapping[b]) == new_path, "rename changed raw path")
                    if expected_bad:
                        reject(InvalidGraph, lambda: s.prove(a, b), "bad original graph")
                        reject(InvalidGraph, lambda: renamed.prove(mapping[a], mapping[b]), "bad renamed graph")
                        COUNTS["invalid_certification_queries"] += 2
                    else:
                        require(s.prove(a, b) == old_path, "valid original proof differs")
                        require(renamed.prove(mapping[a], mapping[b]) == new_path, "valid renamed proof differs")
                    COUNTS["semantic_transport_queries"] += 1
                COUNTS["renamed_semantic_contexts"] += 1
            COUNTS["semantic_contexts"] += 1
            COUNTS["invalid_semantic_contexts" if expected_bad else "valid_semantic_contexts"] += 1


def boundaries():
    valid = {"objects": ("x",), "labels": ("A", "B"),
             "extensions": (frozenset(("x",)), frozenset()), "edges": ()}
    cases = (
        ("objects", [], TypeError), ("objects", None, TypeError),
        ("objects", ("",), ValueError), ("objects", (1,), ValueError),
        ("objects", (True,), ValueError), ("objects", ("x", "x"), ValueError),
        ("labels", ["A", "B"], TypeError), ("labels", "AB", TypeError),
        ("labels", (), ValueError), ("labels", ("A", "A"), ValueError),
        ("labels", ("A", ""), ValueError), ("labels", ("A", None), ValueError),
        ("extensions", [], ValueError), ("extensions", None, ValueError),
        ("extensions", (frozenset(),), ValueError),
        ("extensions", (set(), frozenset()), TypeError),
        ("extensions", ([], frozenset()), TypeError),
        ("extensions", (frozenset(("outside",)), frozenset()), ValueError),
        ("extensions", (frozenset((1,)), frozenset()), ValueError),
        ("edges", [], TypeError), ("edges", None, TypeError),
        ("edges", ([],), ValueError), ("edges", (("A",),), ValueError),
        ("edges", (("A", "B", "A"),), ValueError),
        ("edges", (("A", "missing"),), ValueError),
        ("edges", (("A", []),), ValueError),
        ("edges", (("A", "B"), ("A", "B")), ValueError),
    )
    for field, value, error in cases:
        data = dict(valid)
        data[field] = value
        reject(error, lambda: ClassSystem(**data), "constructor " + field)
        COUNTS["constructor_boundary_cases"] += 1
    class StringSubclass(str):
        pass
    class TupleSubclass(tuple):
        pass
    class FrozenSubclass(frozenset):
        pass
    for field, value, error in (("objects", TupleSubclass(("x",)), TypeError),
                                ("labels", (StringSubclass("A"), "B"), ValueError),
                                ("extensions", (FrozenSubclass(("x",)), frozenset()), TypeError)):
        data = dict(valid)
        data[field] = value
        reject(error, lambda: ClassSystem(**data), "exact builtin " + field)
        COUNTS["constructor_boundary_cases"] += 1
    s = ClassSystem(**valid)
    for unknown in ("missing", "", None, [], 1, True, StringSubclass("A")):
        reject(ValueError, lambda: s.extension(unknown), "extension unknown")
        for method in (s.includes, s.witness, s.find_path, s.prove, s.same_extension):
            reject(ValueError, lambda: method(unknown, "A"), "left unknown")
            reject(ValueError, lambda: method("A", unknown), "right unknown")
        COUNTS["query_boundary_values"] += 1
    for labels in ((), ["P", "Q"], ("P",), ("P", "P"), ("", "Q"), (1, "Q"),
                   (StringSubclass("P"), "Q"), TupleSubclass(("P", "Q"))):
        reject(ValueError, lambda: s.rename(labels), "rename boundary")
        COUNTS["rename_boundary_cases"] += 1
    for prototype in ("missing", "", None, [], 1, StringSubclass("x")):
        reject(ValueError, lambda: prototype_accepts(s, "A", "B", prototype), "prototype boundary")
    reject(ValueError, lambda: prototype_accepts(s, "B", "A", "x"), "empty source prototype")
    require(prototype_accepts(s, "A", "A", "x"), "singleton positive case")
    require(not prototype_accepts(s, "A", "B", "x"), "singleton negative case")
    reject(FrozenInstanceError, lambda: setattr(s, "edges", ()), "frozen instance")
    reject(FrozenInstanceError, lambda: delattr(s, "objects"), "frozen delete")
    # Separate namespaces may have identical spellings. Whitespace is nonempty.
    namespace = ClassSystem(("A",), ("A", " "), (frozenset(("A",)), frozenset()))
    require(namespace.extension("A") == frozenset(("A",)), "namespace collision mishandled")
    empty = ClassSystem((), ("A",), (frozenset(),), (("A", "A"),))
    require(empty.prove("A", "A") == ("A",), "empty singleton reflexivity")
    # Valid endpoints are checked before the graph gate; invalid endpoints are not empty classes.
    bad = ClassSystem(**{**valid, "edges": (("A", "B"),)})
    try:
        bad.prove("missing", "A")
    except InvalidGraph:
        raise ReviewFailure("invalid graph masked unknown query") from None
    except ValueError:
        COUNTS["query_precedence_controls"] += 1
    else:
        raise ReviewFailure("unknown query accepted in invalid graph")


def harness_cases():
    source = (ROOT / "named_classes.py").read_text(encoding="utf-8")
    for name, changed, status in (
        ("independent_unchanged", source, "survived"),
        ("independent_bad_syntax", source + "\nthis is not valid !!!\n", "harness_error"),
        ("independent_bad_import", "raise ImportError('controlled import error')\n", "harness_error"),
        ("independent_runtime", source.replace("return left <= right", "return 1 / 0"), "harness_error"),
        ("independent_mixed_failure_and_error", source.replace("return left <= right", "return False").replace(
            "return next((x for x in self.objects if x in left and x not in right), None)", "return 1 / 0"), "harness_error"),
    ):
        report = mutation_check.evaluate(name, changed)
        require(report["status"] == status, "mutation harness misclassified " + name)
        require("_condillac_mutant_" + name not in sys.modules, "temporary mutant module leaked")
        if name == "independent_mixed_failure_and_error":
            require(report["failures"] and report["errors"], "mixed control did not exercise both categories")
        COUNTS["mutation_framework_controls"] += 1
    reports = mutation_check.run()
    require(reports["counts"] == {"killed_semantic": 10, "survived": 0, "harness_error": 0},
            "ten semantic mutant result counts differ")
    for report in reports["semantic_mutants"]:
        require(report["failures"] and not report["errors"], "kill includes unexpected error")
    COUNTS["semantic_mutants_rechecked"] = len(reports["semantic_mutants"])


def main():
    print("RUNTIME " + json.dumps({"optimization_level": sys.flags.optimize, "python_version": sys.version,
                                    "module_docstring_present": __doc__ is not None}, sort_keys=True))
    try:
        require(False, "review failure-path control")
    except ReviewFailure:
        pass
    else:
        raise RuntimeError("review checks disabled")
    files = tuple(sorted(ROOT.glob("*.py"))) + (Path(__file__),)
    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)), "bare assert found")
    boundaries()
    graph_cases()
    semantic_cases()
    harness_cases()
    print("INDEPENDENT_COUNTS " + json.dumps(dict(sorted(COUNTS.items())), sort_keys=True))
    print("SOURCE_SHA256 " + json.dumps({p.relative_to(ROOT).as_posix(): sha256(p.read_bytes()).hexdigest()
                                            for p in files}, sort_keys=True))
    print("PASS: independent simple-path oracle, self-loops, edge-order ties, semantic transport, boundaries, and mutation controls")


if __name__ == "__main__":
    main()
