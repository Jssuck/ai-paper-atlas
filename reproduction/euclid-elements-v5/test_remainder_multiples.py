import unittest
from fractions import Fraction as F

from remainder_multiples import Magnitude, Result, copies, grid, make_case, solve


class V5Tests(unittest.TestCase):
    def test_worked_example(self):
        self.assertEqual(solve(*make_case(15, 5, 6, 2)), Result(3, F(9), F(3), F(3), F(5), F(9), F(15)))

    def test_fractional_magnitudes(self):
        self.assertEqual(
            solve(*make_case(F(25, 6), F(5, 6), F(5, 3), F(1, 3), "area")),
            Result(5, F(5, 2), F(1, 2), F(1, 2), F(5, 6), F(5, 2), F(25, 6)),
        )

    def test_original_round_trip(self):
        r = solve(*make_case(14, 7, 10, 5))
        self.assertEqual(copies(r.auxiliary_small_remainder + 5, r.factor), 14)
        self.assertEqual(r.rebuilt_small_whole - 5, r.auxiliary_small_remainder)

    def test_addition_only_round_trip(self):
        r = solve(*make_case(21, 7, 12, 4))
        self.assertEqual(r.added_large_remainder, sum([F(3)] * 3))
        self.assertEqual(r.rebuilt_large_whole - 12, r.large_remainder)

    def test_unequal_factors(self):
        with self.assertRaisesRegex(ValueError, "strict integer factor"):
            solve(*make_case(15, 5, 4, 2))

    def test_noninteger_common_factor(self):
        with self.assertRaisesRegex(ValueError, "strict integer factor"):
            solve(*make_case(6, 4, 3, 2))

    def test_factor_one_out_of_scope(self):
        with self.assertRaisesRegex(ValueError, "strict integer factor"):
            solve(*make_case(5, 5, 2, 2))

    def test_equal_or_excessive_removed_part(self):
        for values in ((15, 5, 15, 5), (15, 5, 18, 6), (15, 5, 15, 2), (15, 5, 6, 5)):
            with self.subTest(values=values), self.assertRaisesRegex(ValueError, "proper parts"):
                solve(*make_case(*values))

    def test_nonpositive_or_inexact_input(self):
        for value in (0, -1, F(-1, 7), 0.5, True):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "positive exact"):
                Magnitude(value, "length")

    def test_all_four_must_be_same_kind(self):
        a, b, x, _ = make_case(15, 5, 6, 2)
        with self.assertRaisesRegex(ValueError, "same kind"):
            solve(a, b, x, Magnitude(2, "area"))

    def test_grid(self):
        self.assertEqual(grid(), (72, 72))
