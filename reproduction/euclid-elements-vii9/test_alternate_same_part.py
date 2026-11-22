from fractions import Fraction
import unittest

from alternate_same_part import PairedRows, paired_rows


class TestPairedRows(unittest.TestCase):
    def test_part(self):
        self.assertEqual(paired_rows(4, 12, 12, 36), PairedRows(3, "part", 1, 3, 4, 12))

    def test_parts(self):
        self.assertEqual(paired_rows(6, 18, 10, 30), PairedRows(3, "parts", 3, 5, 2, 6))

    def test_grid(self):
        counts = {"part": 0, "parts": 0}
        for d in range(3, 31):
            for a in range(2, d):
                for n in range(2, 9):
                    bc, ef = n * a, n * d
                    row = paired_rows(a, bc, d, ef)
                    baseline = Fraction(a, d)
                    self.assertEqual(baseline, Fraction(bc, ef))
                    self.assertEqual((row.m, row.k), (baseline.numerator, baseline.denominator))
                    self.assertEqual(row.local_measure, a // baseline.numerator)
                    self.assertEqual(row.pooled_measure, bc // baseline.numerator)
                    expected_kind = "part" if d % a == 0 else "parts"
                    self.assertEqual(row.kind, expected_kind)
                    counts[row.kind] += 1
        self.assertEqual(counts["part"] + counts["parts"], 2842)
        print("Exact grid:", counts, flush=True)

    def test_wrong_premises(self):
        fixtures = ((6, 18, 10, 40), (6, 9, 10, 15), (6, 6, 10, 10), (6, 19, 10, 30))
        for values in fixtures:
            with self.subTest(values=values), self.assertRaises(ValueError):
                paired_rows(*values)
        self.assertNotEqual(Fraction(6, 10), Fraction(18, 40))
        # Ratio equality alone does not meet the original unit-part premise.
        self.assertEqual(Fraction(6, 10), Fraction(9, 15))

    def test_scope(self):
        for values in ((6, 18, 6, 18), (10, 30, 6, 18), (1, 3, 6, 18), (False, 0, 4, 12)):
            with self.subTest(values=values), self.assertRaises(ValueError):
                paired_rows(*values)
        self.assertEqual(Fraction(6, 6), Fraction(18, 18))
        self.assertEqual(Fraction(10, 6), Fraction(30, 18))


if __name__ == "__main__":
    unittest.main()
