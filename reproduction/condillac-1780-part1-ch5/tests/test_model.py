import unittest
from fractions import Fraction as F
from finite_model import FiniteModel
from ratios import (response, infer_product, calibrated_coefficient,
                    equivalent_parameters, relative_coefficient, exact)
from demo import example_model, report


class FiniteTests(unittest.TestCase):
    def setUp(self):
        self.model, self.q = example_model()

    def test_existence_does_not_identify_count_identity_or_attribute(self):
        self.assertEqual(self.model.answer((1,), self.q["cause_exists"]).status, "identified")
        for query in ("number_of_causes", "cause_identity", "attribute"):
            self.assertEqual(self.model.answer((1,), self.q[query]).status, "ambiguous")
        self.assertEqual(self.model.answer((1,), self.q["number_of_causes"]).values, (1, 2))

    def test_no_vacuous_answer(self):
        result = self.model.answer((9,), self.q["cause_exists"])
        self.assertEqual((result.status, result.candidates, result.values), ("inconsistent", (), ()))

    def test_global_differs_from_at_observation(self):
        self.assertEqual(self.model.answer((0,), self.q["cause_identity"]).status, "identified")
        self.assertFalse(self.model.globally_identifiable(self.q["cause_identity"]))
        self.assertTrue(self.model.globally_identifiable(self.q["cause_exists"]))

    def test_naming_is_not_observing_even_unique_names(self):
        named = self.model.with_labels({s: "word:" + s for s in self.model.states})
        self.assertEqual(named.fibers(), self.model.fibers())
        self.assertEqual(named.signatures, self.model.signatures)
        self.assertEqual(named.answer((1,), self.q["cause_identity"]),
                         self.model.answer((1,), self.q["cause_identity"]))

    def test_derived_coordinate_gives_no_new_discrimination(self):
        new = self.model.append_observation("word", {
            s: 100 + row[0] for s, row in zip(self.model.states, self.model.signatures)})
        self.assertTrue(new.refines(self.model))
        self.assertTrue(self.model.refines(new))
        self.assertEqual(new.fibers(), self.model.fibers())

    def test_added_probe_identifies_attribute_not_count(self):
        new = self.model.append_observation("probe", {"none": 0, "A": 7, "B": 8, "A+B": 7})
        self.assertTrue(new.refines(self.model))
        self.assertFalse(self.model.refines(new))
        self.assertEqual(new.candidates((1, 7)), ("A", "A+B"))
        self.assertEqual(new.answer((1, 7), self.q["attribute"]).values, ("red",))
        self.assertEqual(new.answer((1, 7), self.q["number_of_causes"]).status, "ambiguous")
        self.assertEqual(tuple(row[:-1] for row in new.signatures), self.model.signatures)

    def test_assumption_filters_without_observation(self):
        new = self.model.restrict(("B",))
        self.assertEqual(new.columns, self.model.columns)
        self.assertEqual(new.signatures, ((1,),))
        self.assertEqual(new.answer((1,), {"B": "B"}).status, "identified")
        self.assertEqual(self.model.states, ("none", "A", "B", "A+B"))

    def test_empty_assumption_has_no_current_answer(self):
        new = self.model.restrict(())
        self.assertTrue(new.globally_identifiable({}))  # universal global statement
        self.assertEqual(new.answer((1,), {}).status, "inconsistent")

    def test_relaxing_causal_premise_loses_existence_identification(self):
        wide = FiniteModel.from_rows(("effect",), {"caused": (1,), "uncaused": (1,)})
        self.assertEqual(wide.answer((1,), {"caused": True, "uncaused": False}).status, "ambiguous")

    def test_zero_columns_all_states_equivalent(self):
        model = FiniteModel.from_rows((), {"x": (), "y": ()})
        self.assertEqual(model.fibers(), (("x", "y"),))
        self.assertEqual(model.answer((), {"x": 1, "y": 2}).status, "ambiguous")

    def test_refinement_is_independent_of_row_order(self):
        reordered = FiniteModel.from_rows(("effect",), {"B": (1,), "A+B": (1,), "none": (0,), "A": (1,)})
        self.assertTrue(reordered.refines(self.model))
        self.assertTrue(self.model.refines(reordered))

    def test_reject_mismatched_domains(self):
        for operation in (lambda: self.model.answer((1,), {"A": True}),
                          lambda: self.model.with_labels({"A": "force"}),
                          lambda: self.model.append_observation("probe", {"A": 1}),
                          lambda: self.model.restrict(("missing",)),
                          lambda: self.model.refines(self.model.restrict(("A",)))):
            with self.assertRaises(ValueError):
                operation()

    def test_reject_bad_signatures_and_duplicate_identifiers(self):
        for operation in (lambda: self.model.candidates((1, 2)),
                          lambda: FiniteModel.from_rows(("x",), {"A": ()}),
                          lambda: FiniteModel(("x",), ("A", "A"), ((0,), (1,)), ("A", "A")),
                          lambda: self.model.append_observation("effect", dict.fromkeys(self.model.states, 1))):
            with self.assertRaises(ValueError):
                operation()
        with self.assertRaises(TypeError):
            self.model.candidates((1.0,))
        with self.assertRaises(TypeError):
            self.model.candidates((True,))
        with self.assertRaises(TypeError):
            self.model.answer((1,), dict.fromkeys(self.model.states, []))


class RatioTests(unittest.TestCase):
    def test_exact_decimal_fraction(self):
        self.assertEqual(response((F(1, 10),), F(1, 3), 3), (F(1, 10),))
        with self.assertRaises(TypeError):
            exact(0.1)
        with self.assertRaises(TypeError):
            exact(True)

    def test_product_from_multiple_measurements(self):
        result = infer_product((0, 1, 2, -3), (0, 6, 12, -18))
        self.assertEqual((result.status, result.product), ("identified", F(6)))

    def test_gain_cannot_be_silently_assumed_one(self):
        self.assertEqual(calibrated_coefficient((1, 2), (6, 12), 2), F(3))
        self.assertEqual(calibrated_coefficient((1, 2), (6, 12), 1), F(6))

    def test_gauge_symmetry(self):
        for scale in (F(1, 7), F(1), F(9, 2)):
            k, g = equivalent_parameters(3, 2, scale)
            self.assertEqual(k * g, F(6))
            self.assertEqual(response((-4, 0, F(3, 5)), k, g),
                             response((-4, 0, F(3, 5)), 3, 2))

    def test_zero_only_is_uninformative(self):
        self.assertEqual(infer_product((0, 0), (0, 0)).status, "uninformative")
        self.assertIsNone(infer_product((0,), (0,)).product)
        with self.assertRaises(ValueError):
            calibrated_coefficient((0,), (0,), 1)

    def test_inconsistent_data(self):
        for inputs, outputs in (((0,), (1,)), ((1, 2), (6, 13)), ((1,), (0,)), ((1,), (-1,))):
            self.assertEqual(infer_product(inputs, outputs).status, "inconsistent")
        with self.assertRaises(ValueError):
            calibrated_coefficient((1, 2), (6, 13), 1)

    def test_bad_shapes_and_nonpositive_parameters(self):
        for inputs, outputs in (((), ()), ((1,), (1, 2))):
            with self.assertRaises(ValueError):
                infer_product(inputs, outputs)
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                response((1,), bad)
            with self.assertRaises(ValueError):
                calibrated_coefficient((1,), (1,), bad)
            with self.assertRaises(ValueError):
                equivalent_parameters(1, 1, bad)

    def test_relative_coefficient_requires_common_gain(self):
        self.assertEqual(relative_coefficient(iter((1, 2)), (6, 12), (10, 20)), F(3, 5))
        # If gains differ, the same computation need not equal the coefficient ratio.
        self.assertEqual(relative_coefficient((1,), response((1,), 3, 2), response((1,), 5, 3)), F(2, 5))
        self.assertNotEqual(F(2, 5), F(3, 5))

    def test_relative_coefficient_rejects_unidentified_products(self):
        with self.assertRaises(ValueError):
            relative_coefficient((0,), (0,), (0,))

    def test_demo_contract(self):
        data = report()
        self.assertTrue(data["finite"]["labels_preserve_fibers"])
        self.assertTrue(data["ratios"]["all_pairs_match"])
        self.assertEqual(data["ratios"]["product"]["product"], F(6))


if __name__ == "__main__":
    unittest.main()
