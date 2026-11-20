import unittest
from fractions import Fraction as F

from ratio import Q2, Magnitude, Ratio, example_ratio, examples, exceeding_multipliers, measure, witness


class RatioTests(unittest.TestCase):
    def test_exact_signs(self):
        self.assertEqual([Q2(*p).sign() for p in
                          [(0, 0), (0, 1), (1, 1), (1, -1), (3, -2),
                           (-3, 2), (-1, 1), (-1, -1), (-1, 0)]],
                         [0, 1, 1, -1, 1, -1, 1, -1, -1])

    def test_reject_float(self):
        with self.assertRaises(TypeError):
            Q2(1.414)

    def test_part_and_multiple(self):
        m = lambda a, b=0: Magnitude(Q2(a, b), "length")
        self.assertEqual(measure(m(0, 1), m(0, 7)), 7)
        self.assertEqual(measure(m(1, 1), m(8, 8)), 8)
        self.assertIsNone(measure(m(0, 1), m(2)))
        self.assertIsNone(measure(m(4), m(6)))
        self.assertIsNone(measure(m(4), m(4)))
        self.assertIsNone(measure(m(5), m(4)))

    def test_kind_check(self):
        l, a = Magnitude(Q2(1), "length"), Magnitude(Q2(2), "area")
        for f in (Ratio, measure, exceeding_multipliers):
            with self.subTest(f=f), self.assertRaises(ValueError):
                f(l, a)
        self.assertIsNone(witness(example_ratio(Q2(2), Q2(1)),
                                  example_ratio(Q2(6), Q2(3), "area"), 8))

    def test_positive_domain(self):
        for v in [Q2(), Q2(-1), Q2(1, -1)]:
            with self.assertRaises(ValueError):
                Magnitude(v, "length")
        r = example_ratio(Q2(1), Q2(2))
        for m, n in [(0, 1), (1, -1), (F(3, 2), 1), (True, 1)]:
            with self.assertRaises(ValueError):
                r.compare_multiples(m, n)
        with self.assertRaises(ValueError):
            witness(r, r, 0)

    def test_def4_strict_witnesses(self):
        values = [Q2(1), Q2(0, 1), Q2(-1, 1), Q2(1, 1), Q2(F(1, 20)), Q2(7)]
        for x in values:
            for y in values:
                left, right = Magnitude(x, "length"), Magnitude(y, "length")
                m, n = exceeding_multipliers(left, right)
                self.assertGreater((x.scale(m) - y).sign(), 0)
                self.assertGreater((y.scale(n) - x).sign(), 0)
        a = Magnitude(Q2(1), "area")
        self.assertEqual(exceeding_multipliers(a, a), (2, 2))

    def test_proportional_irrationals(self):
        s, *_ = examples()
        same = example_ratio(Q2(2), Q2(0, 1), "area")
        self.assertIsNone(witness(s, same, 16))

    def test_finite_agreement_surd(self):
        s, r, _, _ = examples()
        self.assertIsNone(witness(s, r, 6))
        self.assertEqual(witness(s, r, 7), (5, 7, 1, 0))
        self.assertEqual(witness(s, r, 7, greater=True), (5, 7, 1, 0))
        self.assertIsNone(witness(r, s, 14, greater=True))

    def test_finite_agreement_rational(self):
        _, _, h, l = examples()
        self.assertIsNone(witness(h, l, 100))
        self.assertEqual(witness(h, l, 101), (100, 101, 0, -1))
        self.assertIsNone(witness(h, l, 101, greater=True))
        self.assertEqual(witness(h, l, 102, greater=True), (101, 102, 1, 0))

    def test_rational_grid_independent_cross_product(self):
        for a in range(1, 5):
            for b in range(1, 5):
                for c in range(1, 5):
                    for d in range(1, 5):
                        left, right = example_ratio(Q2(a), Q2(b)), example_ratio(Q2(c), Q2(d))
                        self.assertEqual(witness(left, right, 4) is None, a*d == b*c)
                        self.assertEqual(witness(left, right, 4, greater=True) is not None, a*d > b*c)


if __name__ == "__main__":
    unittest.main()
