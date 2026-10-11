import itertools
import unittest

from model import ObservationBook, Relation, anchor_unresolved, reconstruct
from walkthrough import EDGES, NAMES, TRUTH, full_book, run_examples


class ModelTests(unittest.TestCase):
    def test_empty_observation_book(self):
        result = reconstruct(ObservationBook(("A",), 1))
        self.assertTrue(result.consistent)
        self.assertFalse(result.relative_complete)
        self.assertEqual(result.missing_objects, ("A",))
        self.assertEqual(result.instantiate({}), {})
        self.assertIsNone(result.difference("A", "A"))
        with self.assertRaises(TypeError):
            anchor_unresolved(None, "A")

    def test_single_object_gauge(self):
        result = reconstruct(ObservationBook(("A",), 2, ("A",)))
        self.assertTrue(result.relative_complete)
        self.assertEqual(result.difference("A", "A"), (0, 0))
        self.assertEqual(result.translation_parameters, 2)
        self.assertEqual(result.instantiate({"A": (7, -3)}), {"A": (7, -3)})

    def test_spanning_tree_identifies_unobserved_pairs(self):
        result = reconstruct(full_book())
        self.assertEqual(dict(result.coordinates), TRUTH)
        self.assertEqual(result.difference("C", "E"), (10,))
        summary = result.summary()
        self.assertEqual(summary["observed_objects"], 5)
        self.assertEqual(summary["directly_observed_pairs"], 4)
        self.assertEqual(summary["identifiable_pairs"], 10)
        self.assertTrue(result.relative_complete)

    def test_object_inventory_is_not_relational_knowledge(self):
        result = reconstruct(full_book(()))
        self.assertEqual(result.missing_objects, ())
        self.assertEqual(len(result.components), 5)
        self.assertEqual(result.summary()["identifiable_pairs"], 0)
        self.assertFalse(result.relative_complete)

    def test_missing_object_and_disconnected_relations_are_different(self):
        result = reconstruct(ObservationBook(NAMES, 1, NAMES[:-1], EDGES[:-1]))
        self.assertEqual(result.missing_objects, ("E",))
        self.assertEqual(len(result.components), 1)
        self.assertEqual(result.summary()["identifiable_pairs"], 6)
        self.assertFalse(result.relative_complete)
        disconnected = reconstruct(full_book(EDGES[1:]))
        self.assertEqual(disconnected.components, (("A", "C"), ("B", "D", "E")))
        self.assertEqual(disconnected.summary()["identifiable_pairs"], 4)
        self.assertIsNone(disconnected.difference("A", "B"))

    def test_component_translations_preserve_all_equations(self):
        book = full_book(EDGES[1:])
        result = reconstruct(book)
        for a, b in itertools.product((-100, 0, 100), repeat=2):
            positions = result.instantiate({"A": (a,), "B": (b,)})
            for edge in book.relations:
                self.assertEqual(positions[edge.v][0] - positions[edge.u][0], edge.offset[0])

    def test_misbinding_can_be_consistent_and_wrong(self):
        book = full_book((EDGES[0], Relation("B", "C", (2,)), *EDGES[2:]))
        result = reconstruct(book)
        self.assertTrue(result.relative_complete)
        self.assertEqual(dict(result.coordinates)["C"], (8,))
        self.assertNotEqual(dict(result.coordinates), TRUTH)
        self.assertFalse(reconstruct(book.observe_relation("A", "C", (2,))).consistent)

    def test_cycle_inconsistency_never_returns_a_picture(self):
        result = reconstruct(full_book((*EDGES, Relation("A", "D", (8,)))))
        self.assertFalse(result.consistent)
        self.assertEqual(result.coordinates, ())
        self.assertIsNone(result.translation_parameters)
        self.assertIsNone(result.summary()["identifiable_pairs"])
        with self.assertRaises(ValueError):
            result.difference("A", "B")
        with self.assertRaises(ValueError):
            result.instantiate({"A": (0,)})

    def test_repetition_and_reverse_edge_add_no_information(self):
        book = full_book()
        self.assertIs(book.observe_object("A"), book)
        self.assertIs(book.observe_relation("A", "B", (6,)), book)
        reverse = book.observe_relation("B", "A", (-6,))
        self.assertEqual(reconstruct(reverse).summary(), reconstruct(book).summary())

    def test_zero_and_nonzero_self_relations(self):
        book = ObservationBook(("A",), 1, ("A",))
        self.assertTrue(reconstruct(book.observe_relation("A", "A", (0,))).consistent)
        self.assertFalse(reconstruct(book.observe_relation("A", "A", (1,))).consistent)

    def test_parallel_inconsistent_relations(self):
        book = ObservationBook(("A", "B"), 1, ("A", "B"),
                               (Relation("A", "B", (1,)), Relation("A", "B", (2,))))
        self.assertFalse(reconstruct(book).consistent)

    def test_vector_offsets_and_negative_values(self):
        book = ObservationBook(("P", "Q", "R"), 3, ("P", "Q", "R"),
             (Relation("P", "Q", (-2, 3, 1)), Relation("Q", "R", (5, -3, -4))))
        result = reconstruct(book)
        self.assertEqual(result.difference("P", "R"), (3, 0, -3))
        self.assertEqual(result.difference("R", "P"), (-3, 0, 3))

    def test_inventory_order_changes_only_component_origins(self):
        one = reconstruct(full_book())
        two = reconstruct(ObservationBook(tuple(reversed(NAMES)), 1, NAMES, EDGES))
        self.assertEqual(dict(two.coordinates)["E"], (0,))
        for u, v in itertools.product(NAMES, repeat=2):
            self.assertEqual(one.difference(u, v), two.difference(u, v))

    def test_all_24_relation_orders_have_same_final_result(self):
        expected = reconstruct(full_book()).summary()
        for perm in itertools.permutations(EDGES):
            self.assertEqual(reconstruct(full_book(perm)).summary(), expected)

    def test_order_score_is_only_a_declared_prefix_metric(self):
        traces = []
        for order in (EDGES, (EDGES[2], EDGES[3], EDGES[1], EDGES[0])):
            book = full_book(())
            values = []
            for edge in order:
                book = book.observe_relation(edge.u, edge.v, edge.offset)
                values.append(anchor_unresolved(book, "A"))
            traces.append(values)
        self.assertEqual(traces, [[3, 2, 1, 0], [4, 4, 3, 0]])

    def test_invalid_books_rejected(self):
        invalid = [
            ((), 1, (), ()), (["A"], 1, (), ()), ("A", 1, (), ()),
            (("A", "A"), 1, (), ()), (("",), 1, (), ()),
            ((" A",), 1, (), ()), ((1,), 1, (), ()),
            (("A",), 0, (), ()), (("A",), -1, (), ()),
            (("A",), True, (), ()), (("A",), 1.0, (), ()),
            (("A",), 1, ["A"], ()), (("A",), 1, ("B",), ()),
            (("A",), 1, ("A", "A"), ()), (("A",), 1, (), []),
            (("A",), 1, ("A",), ("edge",)),
            (("A",), 1, (), (Relation("A", "A", (0,)),)),
            (("A",), 1, ("A",), (Relation("A", "B", (0,)),)),
            (("A",), 1, ("A",), (Relation("A", "A", (True,)),)),
            (("A",), 1, ("A",), (Relation("A", "A", (1.0,)),)),
            (("A",), 1, ("A",), (Relation("A", "A", [0]),)),
            (("A",), 1, ("A",), (Relation("A", "A", (0, 0)),)),
            (("A",), 1, ("A",), (Relation("A", "A", ()),)),
        ]
        for args in invalid:
            with self.subTest(args=args), self.assertRaises((TypeError, ValueError)):
                ObservationBook(*args)
        self.assertEqual(len(invalid), 23)

    def test_invalid_operations_rejected(self):
        book = full_book()
        result = reconstruct(book)
        invalid = [
            lambda: book.observe_object("Z"), lambda: book.observe_object(None),
            lambda: book.observe_relation("A", "Z", (1,)),
            lambda: book.observe_relation("A", "B", (True,)),
            lambda: book.observe_relation("A", "B", (1.0,)),
            lambda: book.observe_relation("A", "B", [1]),
            lambda: book.observe_relation("A", "B", (1, 2)),
            lambda: result.difference("A", "Z"), lambda: reconstruct(None),
            lambda: result.instantiate({}), lambda: result.instantiate({"Z": (0,)}),
            lambda: result.instantiate({"A": (0,), "B": (1,)}),
            lambda: result.instantiate({"A": (True,)}),
            lambda: result.instantiate({"A": [0]}), lambda: result.instantiate([]),
            lambda: anchor_unresolved(book, "Z"),
            lambda: ObservationBook(NAMES, 1).observe_relation("A", "B", (6,)),
        ]
        for index, operation in enumerate(invalid):
            with self.subTest(index=index), self.assertRaises((TypeError, ValueError)):
                operation()
        self.assertEqual(len(invalid), 17)

    def test_full_tutorial(self):
        result = run_examples()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["order_permutations"]["permutations"], 24)


if __name__ == "__main__":
    unittest.main()
