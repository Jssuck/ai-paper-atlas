import unittest
from fractions import Fraction as F
from equimultiple_sum import Magnitude as M, Certificate, compose, row_count, regression_grid


class V2Tests(unittest.TestCase):
    def test_distinct_counts(self):
        self.assertEqual(compose((M(6), M(10)), (M(9), M(15)), (M(3), M(5))),
                         Certificate(2, 3, 5, M(15), M(25)))

    def test_same_count_allowed(self):
        self.assertEqual(compose((M(2), M(4)), (M(2), M(4)), (M(1), M(2))).total_count, 4)

    def test_compensating_converse(self):
        first, second, bases = (M(2), M(3)), (M(4), M(3)), (M(1), M(1))
        self.assertEqual(first[0].value + second[0].value, first[1].value + second[1].value)
        with self.assertRaisesRegex(ValueError, "within the row"):
            compose(first, second, bases)

    def test_valid_first_cannot_mask_wrong_second(self):
        with self.assertRaisesRegex(ValueError, "within the row"):
            compose((M(2), M(2)), (M(3), M(4)), (M(1), M(1)))

    def test_equal_fractional_ratios_are_not_integer_multiple_hypotheses(self):
        first, second, bases = (M(3), M(6)), (M(5), M(10)), (M(2), M(4))
        self.assertEqual(first[0].value / bases[0].value, first[1].value / bases[1].value)
        self.assertEqual(second[0].value / bases[0].value, second[1].value / bases[1].value)
        self.assertEqual((first[0].value + second[0].value) / bases[0].value, 4)
        with self.assertRaisesRegex(ValueError, "strict integer"):
            compose(first, second, bases)

    def test_column_types(self):
        self.assertEqual(compose((M(2), M(4, "area")), (M(3), M(6, "area")),
                                 (M(1), M(2, "area"))).right_total, M(10, "area"))
        with self.assertRaisesRegex(ValueError, "kind"):
            compose((M(2), M(4, "area")), (M(3, "area"), M(6, "area")), (M(1), M(2, "area")))

    def test_exact_values(self):
        self.assertEqual(compose((M(F(1, 2)), M(F(3, 2))), (M(F(3, 4)), M(F(9, 4))),
                                 (M(F(1, 4)), M(F(3, 4)))).left_total, M(F(5, 4)))

    def test_strict_and_positive(self):
        with self.assertRaisesRegex(ValueError, "strict integer"):
            row_count((M(1), M(1)), (M(1), M(1)))
        for x in (0, -1):
            with self.assertRaises(ValueError):
                M(x)
        for x in (True, 0.5, "3/2"):
            with self.assertRaises(TypeError):
                M(x)

    def test_row_arity(self):
        with self.assertRaises(ValueError):
            compose((M(3),), (M(2), M(2)), (M(1), M(1)))

    def test_grid(self):
        self.assertEqual(regression_grid(), (144, 135))
