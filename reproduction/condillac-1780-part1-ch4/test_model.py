"""Fixture checks plus independent exhaustive small-domain property tests."""
import itertools
import math
import unittest
from fixtures import garden
from model import (Item, Truth, boundary_name, claims_are_accurate, common_refinement,
                   is_refinement, is_sufficient, normalize_partition,
                   observation_conflicts, observation_partition, observed_truth,
                   task_partition)
from run_experiments import experiments, summary


def all_partitions(ids):
    """Enumerate every set partition, independently of model grouping code."""
    if not ids:
        yield ()
        return
    first, rest = ids[0], ids[1:]
    for partition in all_partitions(rest):
        yield tuple(sorted(((first,),) + partition))
        for index in range(len(partition)):
            blocks = list(partition)
            blocks[index] = tuple(sorted((first,) + blocks[index]))
            yield tuple(sorted(blocks))


class FixtureTests(unittest.TestCase):
    def setUp(self):
        self.items = garden()

    def test_pipeline_counts(self):
        self.assertEqual([s["classes"] for s in experiments()["stages"]], [1, 2, 5, 7, 8, 5])

    def test_pipeline_all_declared_sufficient(self):
        self.assertTrue(all(s["sufficient"] for s in experiments()["stages"]))

    def test_overgeneralization_breaks_harvest(self):
        self.assertFalse(is_sufficient(self.items, task_partition(self.items, ()), ("harvest",)))

    def test_joint_refines_each_need(self):
        joint = task_partition(self.items, ("sort_fruit", "shade"))
        for need in ("sort_fruit", "shade"):
            self.assertTrue(is_refinement(joint, task_partition(self.items, (need,))))

    def test_redundant_new_need_does_not_strictly_refine(self):
        self.assertEqual(task_partition(self.items, ("sort_fruit",)),
                         task_partition(self.items, ("sort_fruit", "harvest")))

    def test_removed_need_can_coarsen(self):
        joint = task_partition(self.items, ("sort_fruit", "shade"))
        reduced = task_partition(self.items, ("sort_fruit",))
        self.assertTrue(is_refinement(joint, reduced))
        self.assertFalse(is_refinement(reduced, joint))

    def test_individual_partition_sufficient_but_needlessly_fine(self):
        singletons = normalize_partition((item.object_id,) for item in self.items)
        self.assertTrue(is_sufficient(self.items, singletons, ("sort_fruit", "shade")))
        self.assertGreater(len(singletons), len(task_partition(self.items, ("sort_fruit", "shade"))))

    def test_observation_conflicts_and_resolution(self):
        conflicts = observation_conflicts(self.items, ("visible_green",), ("harvest",))
        self.assertEqual(len(conflicts), 15)
        self.assertEqual(conflicts[0], {"objects": ["a1", "g1"], "different_needs": ["harvest"]})
        self.assertEqual(observation_conflicts(self.items, ("fruit_kind",), ("harvest",)), [])

    def test_target_outputs_not_inferred_from_attributes(self):
        items = (Item("x", {"color": "green"}, {"act": "left"}),
                 Item("y", {"color": "green"}, {"act": "right"}))
        self.assertEqual(len(observation_partition(items, ("color",))), 1)
        self.assertEqual(len(task_partition(items, ("act",))), 2)

    def test_object_and_field_order_do_not_change_partition(self):
        self.assertEqual(task_partition(self.items, ("shade", "sort_fruit")),
                         task_partition(tuple(reversed(self.items)), ("sort_fruit", "shade")))

    def test_repeated_need_is_idempotent(self):
        self.assertEqual(task_partition(self.items, ("harvest", "harvest")),
                         task_partition(self.items, ("harvest",)))

    def test_renaming_class_labels_preserves_membership(self):
        partition = task_partition(self.items, ("sort_fruit",))
        renamed = {f"new-name-{index}": block for index, block in enumerate(partition)}
        self.assertEqual(normalize_partition(renamed.values()), partition)

    def test_summary_uses_actual_values_not_fixed_success_text(self):
        result = experiments()
        result["refinement"]["joint_equals_common_refinement"] = False
        result["boundary_names"]["all_plant_sufficient_for_display"] = False
        result["accuracy_and_completeness"]["partial_claim_accurate"] = False
        result["unknown"]["unknown_equals_false"] = True
        result["observation_limit"]["remaining_conflicts_after_enrichment"] = [{"dummy": True}]
        report = summary(result)
        self.assertIn("共同细化: False", report)
        self.assertIn("仍充分: False", report)
        self.assertIn("未知 = 假: True", report)
        self.assertIn("采收冲突数: 1", report)
        self.assertIn("部分断言：准确 False", report)

    def test_summary_contains_the_computed_class_counts(self):
        result = experiments()
        report = summary(result)
        for stage in result["stages"]:
            self.assertIn(f"{stage['stage']}: {stage['classes']} classes", report)


class GeneralPropertyTests(unittest.TestCase):
    def test_partition_enumerator_bell_counts(self):
        for n, bell in enumerate((1, 1, 2, 5, 15, 52)):
            partitions = list(all_partitions(tuple(str(i) for i in range(n))))
            self.assertEqual(len(partitions), bell)
            self.assertEqual(len(set(partitions)), bell)

    def test_coarsest_sufficient_exhaustive_binary_up_to_five(self):
        # 1955 independent (target assignment, candidate partition) cases.
        checks = 0
        for n in range(6):
            ids = tuple(str(i) for i in range(n))
            for values in itertools.product(("0", "1"), repeat=n):
                items = tuple(Item(oid, {}, {"need": value}) for oid, value in zip(ids, values))
                ideal = task_partition(items, ("need",))
                for candidate in all_partitions(ids):
                    sufficient = is_sufficient(items, candidate, ("need",))
                    self.assertEqual(sufficient, is_refinement(candidate, ideal))
                    if sufficient:
                        self.assertGreaterEqual(len(candidate), len(ideal))
                        if len(candidate) == len(ideal):
                            self.assertEqual(candidate, ideal)
                    checks += 1
        self.assertEqual(checks, 1955)

    def test_coarsest_sufficient_exhaustive_ternary_four(self):
        checks = 0
        ids = ("0", "1", "2", "3")
        for values in itertools.product(("0", "1", "2"), repeat=4):
            items = tuple(Item(oid, {}, {"need": value}) for oid, value in zip(ids, values))
            ideal = task_partition(items, ("need",))
            for candidate in all_partitions(ids):
                self.assertEqual(is_sufficient(items, candidate, ("need",)),
                                 is_refinement(candidate, ideal))
                checks += 1
        self.assertEqual(checks, 1215)

    def test_combining_needs_is_common_refinement_all_binary_pairs_on_four(self):
        for values in itertools.product(("0", "1"), repeat=8):
            items = tuple(Item(str(i), {}, {"a": values[i], "b": values[i + 4]}) for i in range(4))
            self.assertEqual(task_partition(items, ("a", "b")),
                             common_refinement(task_partition(items, ("a",)), task_partition(items, ("b",))))

    def test_observation_identifiability_iff_no_conflict_exhaustive(self):
        ids = ("0", "1", "2", "3")
        checks = 0
        for observations in all_partitions(ids):
            obs_label = {oid: str(index) for index, block in enumerate(observations) for oid in block}
            for values in itertools.product(("0", "1"), repeat=4):
                items = tuple(Item(oid, {"obs": obs_label[oid]}, {"need": value})
                              for oid, value in zip(ids, values))
                conflicts = observation_conflicts(items, ("obs",), ("need",))
                self.assertEqual(not conflicts,
                                 is_refinement(observation_partition(items, ("obs",)), task_partition(items, ("need",))))
                checks += 1
        self.assertEqual(checks, 240)

    def test_common_refinement_symmetric_and_idempotent(self):
        partitions = list(all_partitions(("a", "b", "c", "d")))
        for a in partitions:
            self.assertEqual(common_refinement(a, a), a)
            for b in partitions:
                self.assertEqual(common_refinement(a, b), common_refinement(b, a))

    def test_empty_domain(self):
        self.assertEqual(task_partition((), ()), ())
        self.assertTrue(is_sufficient((), (), ()))
        self.assertTrue(is_refinement((), ()))
        self.assertEqual(common_refinement((), ()), ())
        self.assertEqual(observation_conflicts((), (), ()), [])

    def test_singleton_domain(self):
        self.assertEqual(task_partition((Item("x", {}, {"a": "yes"}),), ("a",)), (("x",),))


class ValidationTests(unittest.TestCase):
    def test_one_shot_iterators_rejected_instead_of_silently_consumed(self):
        generator = (item for item in garden())
        with self.assertRaises(ValueError):
            task_partition(generator, ("harvest",))

    def test_non_items_and_non_mapping_fields_rejected(self):
        for items in (("x",), (None,), (Item("x", [], {}),), (Item("x", {}, []),)):
            with self.assertRaises(ValueError):
                task_partition(items, ())

    def test_duplicate_object_id_rejected(self):
        with self.assertRaises(ValueError):
            task_partition((Item("x", {}, {}), Item("x", {}, {})), ())

    def test_empty_or_nonstring_object_id_rejected(self):
        for oid in ("", 1):
            with self.assertRaises(ValueError):
                task_partition((Item(oid, {}, {}),), ())

    def test_empty_block_and_repeated_members_rejected(self):
        for bad in (((),), (("x", "x"),), (("x",), ("x",))):
            with self.assertRaises(ValueError):
                normalize_partition(bad)

    def test_bare_strings_not_accepted_as_collection(self):
        for bad in ("xy", ("xy",)):
            with self.assertRaises(ValueError):
                normalize_partition(bad)
        with self.assertRaises(ValueError):
            task_partition(garden(), "harvest")

    def test_nonmatching_partition_domains_rejected(self):
        with self.assertRaises(ValueError):
            is_refinement((("a",),), (("b",),))
        with self.assertRaises(ValueError):
            common_refinement((("a",),), (("b",),))
        with self.assertRaises(ValueError):
            is_sufficient((Item("a", {}, {}),), (("b",),), ())

    def test_missing_field_rejected(self):
        for function in (task_partition, observation_partition):
            with self.assertRaises(ValueError):
                function((Item("x", {}, {}),), ("missing",))
        with self.assertRaises(ValueError):
            is_sufficient((Item("x", {}, {}),), (("x",),), ("missing",))

    def test_unknown_or_nonstring_target_not_treated_as_known_output(self):
        for value in (None, "", False, 1):
            with self.assertRaises(ValueError):
                task_partition((Item("x", {}, {"task": value}),), ("task",))

    def test_target_string_subclasses_rejected_consistently(self):
        class Label(str):
            pass
        items = (Item("x", {}, {"task": Label("yes")}),)
        with self.assertRaises(ValueError):
            task_partition(items, ("task",))
        with self.assertRaises(ValueError):
            is_sufficient(items, (("x",),), ("task",))

    def test_nonfinite_or_compound_attributes_rejected(self):
        for value in (math.nan, math.inf, -math.inf, [], {}):
            with self.assertRaises(ValueError):
                observation_partition((Item("x", {"field": value}, {}),), ("field",))

    def test_observation_equality_is_type_sensitive(self):
        items = tuple(Item(str(i), {"x": value}, {}) for i, value in enumerate((True, 1, 1.0, "1", None, False)))
        self.assertEqual(len(observation_partition(items, ("x",))), 6)


class BoundaryAndEvidenceTests(unittest.TestCase):
    def test_threshold_edges_use_parent_name(self):
        for height, expected in ((3.9, "shrub"), (4.0, "plant"), (5.0, "plant"),
                                 (6.0, "plant"), (6.1, "tree"), (None, "plant")):
            self.assertEqual(boundary_name(height), expected)

    def test_boundary_thresholds_are_explicit_convention(self):
        self.assertEqual(boundary_name(5.0, low=2, high=4), "tree")
        self.assertEqual(boundary_name(5.0, low=6, high=8), "shrub")

    def test_invalid_thresholds_rejected(self):
        for low, high in ((4, 4), (6, 4), (math.nan, 6), (4, math.inf), (True, 6), ("4", 6)):
            with self.assertRaises(ValueError):
                boundary_name(5, low, high)

    def test_arbitrary_size_finite_integers_do_not_overflow(self):
        self.assertEqual(boundary_name(10**500), "tree")
        self.assertEqual(boundary_name(5, 0, 10**500), "plant")

    def test_invalid_height_rejected(self):
        for height in (-1, math.nan, math.inf, True, "5"):
            with self.assertRaises(ValueError):
                boundary_name(height)

    def test_common_name_sufficient_only_for_current_need(self):
        items = (Item("x", {}, {"display": "keep", "move": "large-pot"}),
                 Item("y", {}, {"display": "keep", "move": "small-pot"}))
        shared = (("x", "y"),)
        self.assertTrue(is_sufficient(items, shared, ("display",)))
        self.assertFalse(is_sufficient(items, shared, ("move",)))

    def test_unknown_distinct_from_false(self):
        self.assertIs(observed_truth(None), Truth.UNKNOWN)
        self.assertIs(observed_truth(False), Truth.FALSE)
        self.assertIs(observed_truth(True), Truth.TRUE)
        self.assertIsNot(observed_truth(None), Truth.FALSE)

    def test_three_valued_truth_cannot_silently_coerce_to_boolean(self):
        for value in Truth:
            with self.assertRaises(TypeError):
                bool(value)
        with self.assertRaises(ValueError):
            observed_truth(0)

    def test_unknown_reports_do_not_identify_true_state(self):
        items = (Item("x", {"p": None}, {"need": "yes"}), Item("y", {"p": None}, {"need": "no"}))
        self.assertEqual(len(observation_partition(items, ("p",))), 1)
        self.assertEqual(len(observation_conflicts(items, ("p",), ("need",))), 1)

    def test_accurate_does_not_imply_complete(self):
        truth, claim = {"a": True, "b": "green"}, {"a": True}
        self.assertTrue(claims_are_accurate(truth, claim))
        self.assertNotEqual(set(truth), set(claim))

    def test_wrong_or_unverifiable_claim_rejected(self):
        self.assertFalse(claims_are_accurate({"a": True}, {"a": False}))
        self.assertFalse(claims_are_accurate({"a": True}, {"essence": "known"}))
        self.assertFalse(claims_are_accurate({"a": True}, {"a": 1}))

    def test_unknown_reference_does_not_verify_a_claim(self):
        self.assertFalse(claims_are_accurate({"x": None}, {"x": None}))
        self.assertFalse(claims_are_accurate({"x": None}, {"x": False}))
        self.assertFalse(claims_are_accurate({"x": True}, {"x": None}))

    def test_claim_field_names_and_mapping_types_validated(self):
        for truth, claims in (({1: True}, {1: True}), ({"": True}, {}), ([], {}), ({}, [])):
            with self.assertRaises(ValueError):
                claims_are_accurate(truth, claims)

    def test_empty_claims_accurate_vacuously_but_not_informative(self):
        self.assertTrue(claims_are_accurate({"a": True}, {}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
