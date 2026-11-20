import unittest
from fractions import Fraction
from equimultiples import Magnitude as M, aggregate_certificate, common_multiple, proof_columns, regression_grid, totals


class V1Tests(unittest.TestCase):
    def test_copy_grid(self):
        bases = (M(Fraction(3, 2)), M(Fraction(5, 2)))
        k, rows, columns = proof_columns((M(Fraction(9, 2)), M(Fraction(15, 2))), bases)
        self.assertEqual(k, 3)
        self.assertEqual(rows, ((bases[0],) * 3, (bases[1],) * 3))
        self.assertEqual(columns, (bases,) * 3)
        self.assertEqual(totals(columns[0]), M(4))

    def test_one_pair(self):
        self.assertEqual(aggregate_certificate((M(7),), (M(1),)), (7, M(7), M(1)))

    def test_aggregate_converse_fails(self):
        large, bases = (M(3), M(5)), (M(1), M(1))
        self.assertEqual(totals(large).value / totals(bases).value, 4)
        with self.assertRaisesRegex(ValueError, "differ"):
            common_multiple(large, bases)

    def test_pair_types(self):
        self.assertEqual(proof_columns((M(3), M(6, "area")), (M(1), M(2, "area")))[0], 3)
        with self.assertRaisesRegex(ValueError, "same kind"):
            common_multiple((M(3),), (M(1, "area"),))

    def test_no_mixed_sum(self):
        with self.assertRaisesRegex(ValueError, "homogeneous"):
            aggregate_certificate((M(3), M(6, "area")), (M(1), M(2, "area")))

    def test_empty_and_mismatched_lengths(self):
        with self.assertRaises(ValueError):
            common_multiple((), ())
        with self.assertRaises(ValueError):
            common_multiple((M(3), M(4)), (M(1),))

    def test_noninteger_and_equal(self):
        for value in (2, 3):
            with self.assertRaisesRegex(ValueError, "strict integer"):
                common_multiple((M(value),), (M(2),))

    def test_domain(self):
        for value in (0, -1):
            with self.assertRaises(ValueError):
                M(value)
        for value in (1.0, "2", True):
            with self.assertRaises(TypeError):
                M(value)

    def test_regression_grid(self):
        self.assertEqual(regression_grid(), (162, 162))
