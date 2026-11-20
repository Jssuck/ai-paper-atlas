import unittest
from fractions import Fraction as F
from nested_multiples import Magnitude as M, Certificate, compose, stage_count, regression_grid


class V3Tests(unittest.TestCase):
    def test_distinct_phase_counts(self):
        self.assertEqual(compose((M(2), M(5)), (M(4), M(10)), (M(12), M(30))),
                         Certificate(2, 3, 6, M(12), M(30)))

    def test_same_counts_allowed(self):
        self.assertEqual(compose((M(1), M(2)), (M(2), M(4)), (M(4), M(8))).total_count, 4)

    def test_swapped_phases_same_product(self):
        base, middle, large = (M(1), M(1)), (M(2), M(3)), (M(6), M(6))
        self.assertEqual(large[0].value / base[0].value, large[1].value / base[1].value)
        with self.assertRaisesRegex(ValueError, "within the stage"):
            compose(base, middle, large)

    def test_outer_mismatch_after_inner_success(self):
        with self.assertRaisesRegex(ValueError, "within the stage"):
            compose((M(1), M(1)), (M(2), M(2)), (M(4), M(6)))

    def test_fractional_inner_despite_integer_total(self):
        with self.assertRaisesRegex(ValueError, "strict integer"):
            compose((M(2), M(4)), (M(3), M(6)), (M(12), M(24)))

    def test_fractional_outer_despite_integer_total(self):
        with self.assertRaisesRegex(ValueError, "strict integer"):
            compose((M(2), M(4)), (M(4), M(8)), (M(10), M(20)))

    def test_fractional_coordinates(self):
        c = compose((M(F(1, 4)), M(F(3, 4))), (M(F(1, 2)), M(F(3, 2))), (M(2), M(6)))
        self.assertEqual(c.total_count, 8)

    def test_types(self):
        c = compose((M(1), M(2, "area")), (M(2), M(4, "area")), (M(6), M(12, "area")))
        self.assertEqual(c.right_total, M(12, "area"))
        with self.assertRaisesRegex(ValueError, "kind"):
            compose((M(1), M(2, "area")), (M(2), M(4, "area")), (M(6), M(12)))

    def test_domain_and_arity(self):
        with self.assertRaisesRegex(ValueError, "strict integer"):
            stage_count((M(1), M(2)), (M(1), M(2)))
        with self.assertRaises(ValueError):
            stage_count((M(2),), (M(1), M(2)))
        for bad in (0, -2):
            with self.assertRaises(ValueError):
                M(bad)
        for bad in (True, 0.5):
            with self.assertRaises(TypeError):
                M(bad)

    def test_grid(self):
        self.assertEqual(regression_grid(), (144, 108))
