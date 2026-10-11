"""Run the Chinese tutorial's small examples and return reproducible JSON."""
import json
from itertools import permutations

from model import ObservationBook, Relation, anchor_unresolved, reconstruct

NAMES = ("A", "B", "C", "D", "E")
LABELS = {"A": "主楼", "B": "塔", "C": "磨坊", "D": "桥", "E": "树林"}
EDGES = (Relation("A", "B", (6,)), Relation("A", "C", (2,)),
         Relation("B", "D", (3,)), Relation("B", "E", (6,)))
TRUTH = {"A": (0,), "B": (6,), "C": (2,), "D": (9,), "E": (12,)}


def require(condition, message):
    """Verification remains active under python -O and -OO."""
    if not condition:
        raise AssertionError(message)


def full_book(edges=EDGES):
    return ObservationBook(NAMES, 1, NAMES, tuple(edges))


def run_examples():
    stages = []
    book = ObservationBook(NAMES, 1)

    def record(label):
        stages.append({"stage": label, **reconstruct(book).summary()})

    record("00_空白记录")
    for name in ("A", "B"):
        book = book.observe_object(name)
    record("01_辨出两个主要对象")
    book = book.observe_relation("A", "B", (6,))
    record("02_确定主要对象之间的关系")
    for name, edge in zip(("C", "D", "E"), EDGES[1:]):
        book = book.observe_object(name).observe_relation(edge.u, edge.v, edge.offset)
        record(f"03_至05_纳入{name}")
    result = reconstruct(book)
    require(dict(result.coordinates) == TRUTH and result.relative_complete,
            "ordered reconstruction must equal the teaching fixture")

    listed = full_book(())
    repeated = listed
    for _ in range(3):
        for name in NAMES:
            repeated = repeated.observe_object(name)
    require(repeated == listed, "repeated object list must be unchanged")
    duplicate = book.observe_relation("A", "B", (6,))
    require(duplicate == book, "repeated exact relation must be unchanged")
    reversed_duplicate = book.observe_relation("B", "A", (-6,))
    require(reconstruct(reversed_duplicate).summary() == result.summary(),
            "reverse equivalent relation must add no information")

    missing = ObservationBook(NAMES, 1, NAMES[:-1], EDGES[:-1])
    disconnected = reconstruct(full_book(EDGES[1:]))
    placement_1 = disconnected.instantiate({"A": (0,), "B": (6,)})
    placement_2 = disconnected.instantiate({"A": (0,), "B": (20,)})
    misbound_edges = (EDGES[0], Relation("B", "C", (2,)), *EDGES[2:])
    misbound = reconstruct(full_book(misbound_edges))
    wrong_against_fixture = [name for name, position in misbound.coordinates
                             if position != TRUTH[name]]
    inconsistent = reconstruct(full_book((*EDGES, Relation("A", "D", (8,)))))
    require(misbound.consistent and wrong_against_fixture == ["C"],
            "misbinding must be internally consistent but wrong at C")
    require(not inconsistent.consistent and not inconsistent.coordinates,
            "inconsistent input must not return coordinates")
    corrected_check = reconstruct(full_book((*misbound_edges, EDGES[1])))
    require(not corrected_check.consistent, "correct C relation must expose the misbinding")

    traces = []
    for ordering in permutations(EDGES):
        prefix = full_book(())
        unresolved = []
        for edge in ordering:
            prefix = prefix.observe_relation(edge.u, edge.v, edge.offset)
            unresolved.append(anchor_unresolved(prefix, "A"))
        final = reconstruct(prefix)
        require(final.coordinates == result.coordinates and final.relative_complete,
                "permutations must have identical final positions")
        traces.append({"edge_order": [f"{e.u}->{e.v}" for e in ordering],
                       "prefix_anchor_unresolved": unresolved,
                       "toy_prefix_sum": sum(unresolved)})
    scores = sorted({t["toy_prefix_sum"] for t in traces})
    # Three edges form the inconsistent triangle A-B-D-A; all six orders fail.
    bad_triangle = (EDGES[0], EDGES[2], Relation("A", "D", (8,)))
    require(all(not reconstruct(full_book(p)).consistent for p in permutations(bad_triangle)),
            "all six inconsistent triangle permutations must be rejected")

    return {
        "status": "PASS",
        "interpretation": "现代关系表示教学重构；不是原著算法、心理实验或性能结论",
        "labels": LABELS,
        "fixture_coordinates": TRUTH,
        "ordered_decomposition_recomposition": stages,
        "object_list_only": reconstruct(listed).summary(),
        "repeated_same_object_list": {"repetitions": 3, "state_changed": repeated != listed},
        "repeated_exact_relation": {"state_changed": duplicate != book},
        "missing_object": reconstruct(missing).summary(),
        "disconnected_relations": {"summary": disconnected.summary(),
            "valid_placement_1": placement_1, "valid_placement_2": placement_2,
            "A_to_B_is_identified": disconnected.difference("A", "B") is not None},
        "misbinding": {"summary": misbound.summary(),
            "fixture_comparison_wrong_objects": wrong_against_fixture,
            "adding_correct_A_C_relation_is_consistent": corrected_check.consistent},
        "inconsistent_cycle": inconsistent.summary(),
        "gauge_ambiguity": {"origin_at_zero": result.instantiate({"A": (0,)}),
            "same_relations_origin_at_100": result.instantiate({"A": (100,)})},
        "order_permutations": {"permutations": len(traces),
            "all_final_reconstructions_equal": True,
            "toy_prefix_sum_values": scores, "traces": traces,
            "inconsistent_triangle_orders_rejected": 6},
    }


if __name__ == "__main__":
    print(json.dumps(run_examples(), ensure_ascii=False, indent=2))
