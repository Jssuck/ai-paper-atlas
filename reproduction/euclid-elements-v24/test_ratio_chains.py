from fractions import Fraction as Q
import unittest

from ratio_chains import addition_trace, grid_evidence, lex_probe


class V24Tests(unittest.TestCase):
    def test_named_trace(self):
        self.assertEqual(addition_trace(6, 4, 15, 10, 2, 5), {
            "V.7 cor.": (Q(2), Q(2)),
            "V.22 first": (Q(3), Q(3)),
            "V.18": (Q(4), Q(4)),
            "V.22 second": (Q(2), Q(2)),
        })

    def test_exact_fraction(self):
        left, right = addition_trace(Q(1, 2), 3, Q(1, 3), 2, Q(2, 5), Q(4, 15))["V.22 second"]
        self.assertEqual((left, right), (Q(3, 10), Q(3, 10)))

    def test_missing_first_premise(self):
        with self.assertRaisesRegex(ValueError, "first premise"):
            addition_trace(7, 4, 15, 10, 2, 5)

    def test_missing_second_premise(self):
        with self.assertRaisesRegex(ValueError, "second premise"):
            addition_trace(6, 4, 15, 10, 2, 6)

    def test_bad_domain(self):
        good = [6, 4, 15, 10, 2, 5]
        for i in range(6):
            for bad, err in [(0, ValueError), (-1, ValueError), (True, TypeError), (1.5, TypeError)]:
                with self.subTest(i=i, bad=bad):
                    data = good.copy()
                    data[i] = bad
                    with self.assertRaises(err):
                        addition_trace(*data)

    def test_distinct_denominator_failure(self):
        # u:v=w:x=1 and y:s=z:t=1, but v != s; keeping v,x no longer works.
        u, v, w, x, y, s, z, t = 2, 2, 3, 3, 4, 4, 5, 5
        self.assertEqual((Q(u, v), Q(y, s)), (Q(w, x), Q(z, t)))
        self.assertNotEqual(Q(u + y, v), Q(w + z, x))

    def test_non_archimedean_boundary(self):
        for m in range(1, 13):
            for n in range(1, 13):
                first, second, result = lex_probe(m, n)
                self.assertEqual(*first)
                self.assertEqual(*second)
                self.assertEqual(result[0] != result[1], 2 * m == n)
        self.assertEqual(lex_probe(1, 2)[2], (0, 1))

    def test_integer_grid(self):
        scanned, admissible = grid_evidence(5)
        print(f"grid: {scanned} integer sextuples, {admissible} satisfy both premises")
        # Independent count: each fixed (v,x) permits floor(5/max(a,b))^2 cases;
        # a,b are the primitive denominator components.
        from math import gcd

        predicted = sum(
            (5 * gcd(v, x) // max(v, x)) ** 2
            for v in range(1, 6) for x in range(1, 6)
        )
        self.assertEqual((scanned, admissible), (5 ** 6, predicted))


if __name__ == "__main__":
    unittest.main()
