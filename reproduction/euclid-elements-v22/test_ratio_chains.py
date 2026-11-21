import itertools
import unittest
from fractions import Fraction
from ratio_chains import compare_scaled_endpoints as run, magnitudes as col


class TestV22(unittest.TestCase):
    def test_three_signs_at_length_four(self):
        x = col((8, 4, 2, 1), "length")
        y = col((12, 6, 3, Fraction(3, 2)), "area")
        for n, sign in ((7, 1), (8, 0), (9, -1)):
            self.assertEqual(run(x, y, (1, 5, 3, n)), (sign, sign))

    def test_base_case(self):
        self.assertEqual(run(col((1, 2), "length"), col((3, 6), "area"), (4, 2)), (0, 0))

    def test_constructive_fraction_grid(self):
        count = 0
        for a,b,c,d in itertools.product(range(1, 9), repeat=4):
            raw = (Fraction(a, b), Fraction(c, d), Fraction(b, c), Fraction(d, a))
            other = tuple(val * Fraction(a, d) for val in raw)
            k = (b, a, d, c)
            # Independent rational oracle: endpoint magnitude multiplication.
            u, v = raw[0] * b, raw[-1] * c
            sign = (1 if u > v else -1 if u < v else 0)
            self.assertEqual(run(col(raw, "x"), col(other, "y"), k), (sign, sign))
            count += 1
        self.assertEqual(count, 4096)

    def test_exhaustive_small_integer_triples(self):
        accepted = rejected = 0
        for a,b,c,d,e,f in itertools.product(range(1, 6), repeat=6):
            x, y = col((a,b,c), "x"), col((d,e,f), "y")
            # Whole-column oracle, independent of the adjacency traversal.
            if (a*e, a*f) == (d*b, d*c):
                expected = ((2*a > 3*c)-(2*a < 3*c), (2*d > 3*f)-(2*d < 3*f))
                self.assertEqual(run(x,y,(2,5,3)), expected)
                accepted += 1
            else:
                with self.assertRaises(ValueError):
                    run(x,y,(2,5,3))
                rejected += 1
        self.assertEqual((accepted, rejected), (157, 15468))

    def test_longer_chain(self):
        x = tuple(Fraction(1, n) for n in range(1, 41))
        y = tuple(n * Fraction(40, 3) for n in x)
        self.assertEqual(run(col(x, "x"), col(y, "y"), tuple(range(1, 41))), (0, 0))

    def test_endpoints_can_match_despite_bad_middle(self):
        with self.assertRaises(ValueError):
            run(col((8,4,1), "x"), col((16,9,2), "y"), (1,1,1))

    def test_perturbed_is_not_ordered(self):
        with self.assertRaises(ValueError):
            run(col((6,4,3), "x"), col((16,12,8), "y"), (1,1,1))

    def test_reject_mixed_kind_or_bad_magnitude(self):
        y = col((2,4), "y")
        for bad in (0, -1, False, 1.0):
            with self.assertRaises((ValueError, TypeError)):
                run(col((1,bad), "x"), y, (1,1))
        with self.assertRaises(ValueError):
            run(((1,"area"),(2,"length")), y, (1,1))

    def test_reject_bad_scales_or_lengths(self):
        x, y = col((1,2), "x"), col((3,6), "y")
        for k in ((1,), (True,1), (0,1), (-1,1), (1.0,1)):
            with self.assertRaises(ValueError):
                run(x,y,k)
        with self.assertRaises(ValueError):
            run(x, col((3,6,9), "y"), (1,1))
        with self.assertRaises(ValueError):
            run(col((1,), "x"), col((3,), "y"), (1,))


if __name__ == "__main__":
    unittest.main()
