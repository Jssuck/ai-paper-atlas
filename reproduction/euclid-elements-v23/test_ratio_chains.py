"""Deterministic unit checks with independent integer cross-product oracle."""
from fractions import Fraction as F
from itertools import product
import unittest

from ratio_chains import first_mismatch, probe


class PerturbedTests(unittest.TestCase):
    def test_three_branches_and_labels(self):
        for q, sign in [(1, 1), (2, 0), (3, -1)]:
            row = probe((6, 4, 3), (16, 12, 8), 1, q)
            self.assertEqual(row["scaled"], (6, 4, 16, q*3, q*12, q*8))
            self.assertEqual(row["signs"], (sign, sign))
            self.assertEqual(tuple(x for x, _ in row["original"]),
                             (F(3,2), F(3,2), F(3,2), F(1,4), F(1,4),
                              F(1,4), F(1,4), F(4,3*q)))
            self.assertEqual(row["alternative"][-1], (F(4,3*q), F(4,3*q)))

    def test_rational_input(self):
        row = probe((F(3,7), F(2,7), F(3,14)), (F(4,5), F(3,5), F(2,5)), 5, 10)
        self.assertEqual(row["signs"], (0, 0))

    def test_small_integer_grid(self):
        valid = examined = 0
        for a, b, c, d, e, f in product(range(1, 5), repeat=6):
            left, right = (a,b,c), (d,e,f)
            # Cross-multiplication is an external oracle in this rational model.
            if a*f != b*e or b*e != c*d:
                with self.assertRaises(ValueError):
                    probe(left, right, 1, 1)
                continue
            valid += 1
            self.assertEqual(a*f, c*d)
            for p, q in product(range(1, 5), repeat=2):
                row = probe(left, right, p, q)
                dx, dy = p*a-q*c, p*d-q*f
                self.assertEqual(row["signs"], ((dx>0)-(dx<0), (dy>0)-(dy<0)))
                self.assertEqual(*row["signs"])
                for u, v in row["original"] + row["alternative"]:
                    self.assertEqual(u, v)
                examined += 1
        self.assertEqual(valid, 70)
        self.assertEqual(examined, 1120)
        print(f"grid: 4096 six-tuples, {valid} satisfy premises, {examined} valid multiplier probes")

    def test_premises_not_optional(self):
        for left, right in [((7,4,3),(16,12,8)), ((6,4,3),(15,12,8))]:
            with self.assertRaises(ValueError):
                probe(left, right, 1, 2)
            self.assertEqual(first_mismatch((left[0],left[2]), (right[0],right[2]), 2), (1,2))

    def test_wrong_scale(self):
        # Position-wise scaling p=1, middle=2, q=3 breaks the first pairing.
        self.assertNotEqual(F(6, 2*4), F(2*12, 3*8))

    def test_finite_probe_can_miss(self):
        self.assertIsNone(first_mismatch((65,64), (66,65), 64))
        self.assertEqual(first_mismatch((65,64), (66,65), 65), (64,65))

    def test_bad_domains(self):
        for bad in (0,-1,F(-1,2)):
            with self.assertRaises(ValueError):
                probe((bad,4,3),(16,12,8),1,1)
        for bad in (True,6.0,"6"):
            with self.assertRaises(TypeError):
                probe((bad,4,3),(16,12,8),1,1)
        for bad in (True, 1.0, F(1,1)):
            with self.assertRaises(TypeError):
                probe((6,4,3),(16,12,8),bad,1)
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                probe((6,4,3),(16,12,8),1,bad)


if __name__ == "__main__":
    unittest.main()
