"""Independent exact-linear-algebra audit. All checks survive python -O.

Run from any directory. This script does not modify the production model.
Finite cases supplement structural proofs in MODEL.zh-CN.md and
independent-review/review.zh-CN.md; they do not replace those proofs.
"""
from __future__ import annotations

from dataclasses import FrozenInstanceError
from fractions import Fraction
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
import model


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def matrix_oracle(names, dimension, edges):
    """RREF of an incidence matrix with d right-hand sides, over Q.

    No adjacency, path summation, graph traversal, or model helpers.
    Query identifiability is coefficient-row membership in the row space.
    """
    index = {name: i for i, name in enumerate(names)}
    n = len(names)
    rows = []
    for u, v, offset in edges:
        row = [Fraction(0) for _ in range(n)]
        row[index[u]] -= 1
        row[index[v]] += 1
        rows.append(row + list(map(Fraction, offset)))
    rank = 0
    pivots = []
    for column in range(n):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        denominator = rows[rank][column]
        rows[rank] = [value / denominator for value in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][column]:
                coefficient = rows[i][column]
                rows[i] = [a - coefficient * b for a, b in zip(rows[i], rows[rank])]
        pivots.append(column)
        rank += 1
    consistent = all(any(row[:n]) or not any(row[n:]) for row in rows)

    def query(u, v):
        coefficients = [Fraction(0) for _ in range(n)]
        coefficients[index[u]] -= 1
        coefficients[index[v]] += 1
        value = [Fraction(0) for _ in range(dimension)]
        for row, pivot in zip(rows, pivots):
            factor = coefficients[pivot]
            coefficients = [a - factor * b for a, b in zip(coefficients, row[:n])]
            value = [a + factor * b for a, b in zip(value, row[n:])]
        return None if any(coefficients) else tuple(value)

    return consistent, rank, query


COUNTS = {"graphs": 0, "consistent_graphs": 0, "inconsistent_graphs": 0,
          "ordered_pair_queries": 0, "instantiated_equations": 0}


def crosscheck(inventory, seen, dimension, edges, module=model, count=True):
    book = module.ObservationBook(inventory, dimension, seen,
                                 tuple(module.Relation(*edge) for edge in edges))
    before = repr(book)
    result = module.reconstruct(book)
    expected_consistent, rank, query = matrix_oracle(seen, dimension, edges)
    require(result.consistent == expected_consistent, ("consistency", book))
    require(repr(book) == before, "reconstruct mutated input")
    expected_missing = tuple(name for name in inventory if name not in seen)
    require(result.missing_objects == expected_missing, "missing inventory")
    require(sum(map(len, result.components)) == len(seen), "component size")
    require(len(result.components) == len(seen) - rank, ("rank/nullity", book))
    require({name for part in result.components for name in part} == set(seen), "membership")
    if count:
        COUNTS["graphs"] += 1
        COUNTS["consistent_graphs" if expected_consistent else "inconsistent_graphs"] += 1
    if not expected_consistent:
        require(result.coordinates == (), "inconsistent coordinates leaked")
        require(result.translation_parameters is None, "inconsistent translation family")
        require(result.relative_complete is False, "inconsistent marked complete")
        require(result.summary()["identifiable_pairs"] is None, "inconsistent pair count")
        require(bool(result.conflicts), "missing conflict witness")
        for method, arguments in ((result.difference, (inventory[0], inventory[0])),
                                  (result.instantiate, ({},))):
            try:
                method(*arguments)
            except ValueError:
                pass
            else:
                raise AssertionError("inconsistent API did not reject operation")
        return
    identified = 0
    for u, v in product(inventory, repeat=2):
        expected = query(u, v) if u in seen and v in seen else None
        actual = result.difference(u, v)
        require(actual == expected, ("query", u, v, book, actual, expected))
        if count:
            COUNTS["ordered_pair_queries"] += 1
        if u != v and expected is not None:
            identified += 1
    require(result.summary()["identifiable_pairs"] == identified // 2, "pair count")
    require(result.translation_parameters == dimension * (len(seen) - rank), "nullity")
    require(result.relative_complete == (not expected_missing and rank == len(seen) - 1),
            "relative completion")
    require(all(dict(result.coordinates)[part[0]] == (0,) * dimension
                for part in result.components), "nonzero component root")
    for seed in (0, 11):
        shifts = {part[0]: tuple((i + 1) * (axis + 1) * seed
                                for axis in range(dimension))
                  for i, part in enumerate(result.components)}
        original_shifts = shifts.copy()
        positions = result.instantiate(shifts)
        require(shifts == original_shifts, "shift input mutated")
        for u, v, offset in edges:
            require(tuple(positions[v][axis] - positions[u][axis]
                          for axis in range(dimension)) == offset, "instantiated equation")
            if count:
                COUNTS["instantiated_equations"] += 1
        positions.clear()
        require(repr(book) == before and len(result.coordinates) == len(seen), "output aliases")


def finite_families():
    families = []
    for names, dimension, values in ((("A", "B", "C"), 1, (-2, -1, 0, 1, 2)),
                                     (("A", "B", "C"), 2, (-1, 0, 1)),
                                     (("A", "B", "C", "D"), 1, (-1, 0, 1))):
        pairs = tuple(combinations(names, 2))
        states = (None,) + tuple(product(values, repeat=dimension))
        start = COUNTS["graphs"]
        consistent_start = COUNTS["consistent_graphs"]
        for offsets in product(states, repeat=len(pairs)):
            edges = tuple((u, v, offset) for (u, v), offset in zip(pairs, offsets)
                          if offset is not None)
            crosscheck(names, names, dimension, edges)
        families.append({"vertices": len(names), "dimension": dimension,
                         "coordinate_edge_values": values,
                         "graphs": COUNTS["graphs"] - start,
                         "consistent_graphs": COUNTS["consistent_graphs"] - consistent_start})
    return families


def adversarial_cases(module=model, count=True):
    huge = 10 ** 120
    cases = [
        (("A",), (), 3, ()),
        (("A",), ("A",), 3, (("A", "A", (0, 0, 0)),)),
        (("A",), ("A",), 3, (("A", "A", (0, 1, 0)),)),
        (("A", "B", "C"), ("A", "B", "C"), 1,
         (("A", "B", (2,)), ("A", "B", (2,)), ("B", "A", (-2,)))),
        (("A", "B"), ("A", "B"), 1,
         (("A", "B", (2,)), ("A", "B", (3,)))),
        (("A", "B"), ("A", "B"), 1,
         (("A", "B", (2,)), ("B", "A", (2,)))),
        (("桥", "塔", "林", "空"), ("林", "塔", "桥"), 3,
         (("桥", "塔", (huge, -huge, 0)), ("塔", "林", (-huge + 1, huge, -9)),
          ("桥", "林", (1, 0, -9)))),
    ]
    for case in cases:
        crosscheck(*case, module=module, count=count)
    # Every partial observation set, including missing and empty observations;
    # every inventory permutation is covered separately in production tests.
    inventory = ("Z", "A", "Y", "B", "X")
    for flags in product((False, True), repeat=len(inventory)):
        seen = tuple(name for name, flag in zip(inventory, flags) if flag)
        edges = tuple((u, v, (i - 2, -i)) for i, (u, v)
                      in enumerate(zip(seen, seen[1:])))
        crosscheck(inventory, tuple(reversed(seen)), 2, edges, module, count)
    return len(cases) + 2 ** len(inventory)


def immutable_inputs():
    book = model.ObservationBook(("A", "B", "C"), 1)
    with_a = book.observe_object("A")
    with_b = with_a.observe_object("B")
    related = with_b.observe_relation("A", "B", (2,))
    require(book.seen == () and with_a.seen == ("A",), "observe_object mutated input")
    require(with_b.relations == () and len(related.relations) == 1, "observe_relation mutated input")
    require(related.observe_object("B") is related, "duplicate object identity")
    require(related.observe_relation("A", "B", (2,)) is related, "duplicate edge identity")
    for obj, attribute, value in ((book, "seen", ("A",)),
                                  (related.relations[0], "offset", (9,))):
        try:
            setattr(obj, attribute, value)
        except FrozenInstanceError:
            pass
        else:
            raise AssertionError("frozen input became writable")
    result = model.reconstruct(related)
    summary = result.summary()
    summary["components"][0].clear()
    summary["component_relative_positions"]["A"][0] = 999
    require(result.difference("A", "B") == (2,), "summary aliases internal state")


def invalid_inputs():
    book = model.ObservationBook(("A", "B", "C"), 2, ("A", "B"))
    result = model.reconstruct(book)
    operations = [
        lambda: model.ObservationBook((), 1),
        lambda: model.ObservationBook(["A"], 1),
        lambda: model.ObservationBook(("A", "A"), 1),
        lambda: model.ObservationBook((" A",), 1),
        lambda: model.ObservationBook(("A\t",), 1),
        lambda: model.ObservationBook(("",), 1),
        lambda: model.ObservationBook((1,), 1),
        lambda: model.ObservationBook(("A",), False),
        lambda: model.ObservationBook(("A",), 2.0),
        lambda: model.ObservationBook(("A",), 0),
        lambda: model.ObservationBook(("A",), -3),
        lambda: model.ObservationBook(("A",), 1, ("B",)),
        lambda: model.ObservationBook(("A",), 1, ("A", "A")),
        lambda: model.ObservationBook(("A",), 1, ("A",), []),
        lambda: model.ObservationBook(("A",), 1, ("A",), (("A", "A", (0,)),)),
        lambda: book.observe_object("D"),
        lambda: book.observe_object(None),
        lambda: book.observe_relation("A", "C", (0, 0)),
        lambda: book.observe_relation("A", "B", (0, True)),
        lambda: book.observe_relation("A", "B", (0, 1.0)),
        lambda: book.observe_relation("A", "B", (0, "1")),
        lambda: book.observe_relation("A", "B", (0,)),
        lambda: book.observe_relation("A", "B", [0, 0]),
        lambda: book.observe_relation("A", "B", iter((0, 0))),
        lambda: book.observe_relation("A", "B", None),
        lambda: model.reconstruct(None),
        lambda: model.reconstruct({}),
        lambda: result.difference("A", "D"),
        lambda: result.difference(True, "B"),
        lambda: result.instantiate(None),
        lambda: result.instantiate({"A": (0, 0)}),
        lambda: result.instantiate({"A": (0, 0), "B": (0, 0), "C": (0, 0)}),
        lambda: result.instantiate({"A": (0, 0), "B": (0, False)}),
        lambda: result.instantiate({"A": (0, 0), "B": (0, 0, 0)}),
        lambda: model.anchor_unresolved(book, "C"),
    ]
    before = repr(book)
    for i, operation in enumerate(operations):
        try:
            operation()
        except (TypeError, ValueError):
            pass
        else:
            raise AssertionError(("invalid input accepted", i))
        require(repr(book) == before, ("failed operation mutated input", i))
    return len(operations)


def mutation_checks():
    source = (ROOT / "model.py").read_text()
    mutations = [
        ("reverse_sign", "tuple(-x for x in edge.offset)", "tuple(x for x in edge.offset)"),
        ("difference_sign", "tuple(x - y for x, y in zip(a, b))", "tuple(y - x for x, y in zip(a, b))"),
        ("ignore_conflicts", "consistent = not conflicts", "consistent = True"),
        ("ignore_disconnection", "and len(self.components) == 1", "and True"),
        ("omit_vector_dimension", "self.book.dimension * len(self.components)", "len(self.components)"),
        ("drop_missing_objects", "return tuple(x for x in self.book.inventory if x not in self.book.seen)", "return ()"),
    ]
    results = []
    for name, before, after in mutations:
        require(source.count(before) == 1, ("mutation target changed", name))
        module_name = "audit_mutant_" + name
        module = types.ModuleType(module_name)
        sys.modules[module_name] = module
        exec(compile(source.replace(before, after, 1), module_name, "exec"), module.__dict__)
        try:
            adversarial_cases(module, False)
        except (AssertionError, ValueError, KeyError) as error:
            results.append({"mutation": name, "detected": True,
                            "reason": str(error)[:400]})
        else:
            raise AssertionError(("surviving mutation", name))
        finally:
            del sys.modules[module_name]
    return results


def main():
    families = finite_families()
    adversarial = adversarial_cases()
    immutable_inputs()
    invalid = invalid_inputs()
    mutations = mutation_checks()
    print(json.dumps({"status": "PASS", "python": sys.version, "optimized": not __debug__,
                      "working_directory": "package root" if Path.cwd() == ROOT else "outside package root",
                      "model_sha256": hashlib.sha256((ROOT / "model.py").read_bytes()).hexdigest(),
                      "oracle": "exact Fraction RREF and row-space query membership",
                      "finite_families": families, "adversarial_graphs": adversarial,
                      "additional_invalid_operation_checks": invalid,
                      "counts": COUNTS, "mutations": mutations,
                      "limits": "Finite code checks are not the general structural proof."},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
