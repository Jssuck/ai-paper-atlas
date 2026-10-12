"""Dedicated boundary and behavior tests, independent of optimization flags."""
from dataclasses import FrozenInstanceError
import unittest
from named_classes import ClassSystem, InvalidGraph, prototype_accepts
from examples import main_system, with_edges


class ClassTests(unittest.TestCase):
    def setUp(self):
        self.s = main_system()

    def test_chain(self):
        self.assertEqual(self.s.prove("三边形", "图形"), ("三边形", "三角形", "图形"))

    def test_reflexive_zero_edge(self):
        self.assertEqual(self.s.prove("红色", "红色"), ("红色",))

    def test_true_unencoded(self):
        self.assertTrue(self.s.includes("红色", "图形"))
        self.assertIsNone(self.s.prove("红色", "图形"))
        self.assertIsNone(self.s.witness("红色", "图形"))

    def test_false_inclusion_witness(self):
        self.assertFalse(self.s.includes("三角形", "红色"))
        self.assertEqual(self.s.witness("三角形", "红色"), "蓝三角")

    def test_overlap_is_not_inclusion(self):
        self.assertFalse(self.s.includes("红色", "三角形"))
        self.assertEqual(self.s.witness("红色", "三角形"), "红方块")

    def test_empty_vacuity(self):
        for label in self.s.labels:
            self.assertTrue(self.s.includes("空类", label))
            self.assertIsNone(self.s.witness("空类", label))

    def test_empty_universe(self):
        s = ClassSystem((), ("A", "B"), (frozenset(), frozenset()), (("A", "B"), ("B", "A")))
        self.assertEqual(s.components(), (("A", "B"),))
        self.assertEqual(s.prove("A", "B"), ("A", "B"))

    def test_one_label_and_self_loop(self):
        s = ClassSystem(("x",), ("A",), (frozenset(("x",)),), (("A", "A"),))
        self.assertEqual(s.prove("A", "A"), ("A",))
        self.assertEqual(s.components(), (("A",),))

    def test_synonyms_are_distinct(self):
        self.assertTrue(self.s.same_extension("三角形", "三边形"))
        self.assertNotEqual("三角形", "三边形")
        self.assertEqual(len(self.s.labels), 5)

    def test_equal_extensions_need_not_share_scc(self):
        self.assertNotIn(("三角形", "三边形"), self.s.components())

    def test_cycle_keeps_names(self):
        s = with_edges(self.s, ("三角形", "三边形"))
        self.assertEqual(s.components()[0], ("三角形", "三边形"))
        self.assertEqual(len(s.labels), 5)
        self.assertEqual(s.prove("三角形", "三边形"), ("三角形", "三边形"))

    def test_invalid_graph_raw_path(self):
        s = with_edges(self.s, ("红色", "三角形"))
        self.assertEqual(s.find_path("红色", "三角形"), ("红色", "三角形"))
        self.assertEqual(s.violations(), (("红色", "三角形", "红方块"),))
        with self.assertRaises(InvalidGraph):
            s.prove("红色", "三角形")

    def test_global_gate_even_unrelated_query(self):
        s = ClassSystem(("x",), ("A", "B", "C"), (frozenset(("x",)), frozenset(), frozenset()), (("A", "B"),))
        self.assertEqual(s.find_path("C", "C"), ("C",))
        with self.assertRaises(InvalidGraph):
            s.prove("C", "C")

    def test_shortest_path_and_edge_order(self):
        s = ClassSystem((), ("A", "B", "C", "D"), (frozenset(),) * 4,
                        (("A", "C"), ("A", "B"), ("C", "D"), ("B", "D")))
        self.assertEqual(s.prove("A", "D"), ("A", "C", "D"))
        self.assertEqual(with_edges(s, ("A", "D")).prove("A", "D"), ("A", "D"))

    def test_reverse_direction_not_assumed(self):
        self.assertIsNone(self.s.find_path("图形", "三角形"))

    def test_witness_respects_declared_order(self):
        s = ClassSystem(("z", "a"), ("A", "B"), (frozenset(("z", "a")), frozenset()))
        self.assertEqual(s.witness("A", "B"), "z")

    def test_prototype_is_not_universal(self):
        self.assertTrue(prototype_accepts(self.s, "三角形", "红色", "红三角"))
        self.assertFalse(self.s.includes("三角形", "红色"))

    def test_prototype_membership_required(self):
        for prototype in ("红方块", "missing", None):
            with self.assertRaises(ValueError):
                prototype_accepts(self.s, "三角形", "红色", prototype)
        with self.assertRaises(ValueError):
            prototype_accepts(self.s, "空类", "红色", "红三角")

    def test_bijective_rename(self):
        s = self.s.rename(("A", "B", "C", "D", "Z"))
        self.assertEqual(s.objects, self.s.objects)
        self.assertEqual(s.extensions, self.s.extensions)
        self.assertEqual(s.prove("D", "B"), ("D", "A", "B"))
        self.assertEqual(s.witness("A", "C"), "蓝三角")

    def test_rename_swapping_existing_labels(self):
        s = self.s.rename(tuple(reversed(self.s.labels)))
        self.assertEqual(s.extensions, self.s.extensions)
        self.assertEqual(s.prove("图形", "三边形"), ("图形", "空类", "三边形"))

    def test_bad_rename(self):
        for labels in ((), ("x",) * 5, ("x", "y", "z", "w", ""), ["a"] * 5):
            with self.assertRaises(ValueError):
                self.s.rename(labels)

    def test_immutable_fields(self):
        with self.assertRaises(FrozenInstanceError):
            self.s.objects = ()
        self.assertIsInstance(self.s.extensions[0], frozenset)

    def test_unknown_queries(self):
        for method in (self.s.includes, self.s.witness, self.s.find_path, self.s.prove, self.s.same_extension):
            with self.assertRaises(ValueError):
                method("unknown", "图形")
            with self.assertRaises(ValueError):
                method("图形", "unknown")
        with self.assertRaises(ValueError):
            self.s.extension([])

    def test_duplicate_objects_or_labels(self):
        with self.assertRaises(ValueError):
            ClassSystem(("x", "x"), ("A",), (frozenset(),))
        with self.assertRaises(ValueError):
            ClassSystem((), ("A", "A"), (frozenset(), frozenset()))

    def test_empty_labels_rejected(self):
        with self.assertRaises(ValueError):
            ClassSystem((), (), ())

    def test_bad_domain_names(self):
        for objects, labels in ((("",), ("A",)), ((1,), ("A",)), ((), (True,)), ((), ("",))):
            with self.assertRaises(ValueError):
                ClassSystem(objects, labels, (frozenset(),))
        with self.assertRaises(TypeError):
            ClassSystem([], ("A",), (frozenset(),))

    def test_bad_extension_shape(self):
        with self.assertRaises(ValueError):
            ClassSystem((), ("A",), ())
        with self.assertRaises(TypeError):
            ClassSystem((), ("A",), (set(),))

    def test_outside_extension_rejected(self):
        with self.assertRaises(ValueError):
            ClassSystem((), ("A",), (frozenset(("outside",)),))

    def test_bad_edges(self):
        for edges in ((("A",),), (("A", "missing"),), (("A", []),), (("A", "A"), ("A", "A"))):
            with self.assertRaises(ValueError):
                ClassSystem((), ("A",), (frozenset(),), edges)
        with self.assertRaises(TypeError):
            ClassSystem((), ("A",), (frozenset(),), [])

    def test_matching_partitions_need_not_be_complete(self):
        s = ClassSystem(("x", "y"), ("A", "B"),
                        (frozenset(("x",)), frozenset(("x", "y"))))
        self.assertEqual(s.components(), (("A",), ("B",)))
        self.assertFalse(s.same_extension("A", "B"))
        self.assertTrue(s.includes("A", "B"))
        self.assertIsNone(s.prove("A", "B"))

    def test_no_edges_does_not_mean_no_truth(self):
        s = ClassSystem(("x",), ("A", "B"), (frozenset(("x",)), frozenset(("x",))))
        self.assertIsNone(s.prove("A", "B"))
        self.assertTrue(s.includes("A", "B"))
        self.assertEqual(s.components(), (("A",), ("B",)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
