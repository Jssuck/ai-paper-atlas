import unittest
from fractions import Fraction as Q
from ratio_chains import EXAMPLE, affine, certificate, construct, sweep


class VI10(unittest.TestCase):
    def test_example(self):
        w = construct(*EXAMPLE)
        self.assertEqual(w, ((4, 0), (10, 0), (8, 2), (12, 2)))
        self.assertEqual(certificate(*EXAMPLE, *w), ((Q(2, 3),)*3, (Q(3, 2),)*2))

    def test_off_parallel(self):
        f, _, h, k = construct(*EXAMPLE)
        with self.assertRaisesRegex(ValueError, "parallelism"):
            certificate(*EXAMPLE, f, (9, 0), h, k)

    def test_wrong_auxiliary_line(self):
        f, g, h, _ = construct(*EXAMPLE)
        with self.assertRaisesRegex(ValueError, "nonzero line"):
            certificate(*EXAMPLE, f, g, h, (12, 3))

    def test_reverse_order_and_duplicates(self):
        a, b, c, d, e = EXAMPLE
        for p, q in ((e, d), (d, d), (a, e), (d, c)):
            with self.assertRaisesRegex(ValueError, "strict order"):
                construct(a, b, c, p, q)
            with self.assertRaisesRegex(ValueError, "strictly interior"):
                affine(a, b, c, (p, q))

    def test_degenerate(self):
        a, b, c, d, e = EXAMPLE
        for target in (a, c, (-1, -1)):
            with self.assertRaisesRegex(ValueError, "nondegenerate"):
                construct(a, target, c, d, e)

    def test_nonrational_off_line(self):
        a, b, c, d, e = EXAMPLE
        with self.assertRaises(TypeError):
            construct(a, b, c, (2.0, 2), e)
        with self.assertRaises(ValueError):
            construct(a, b, c, (2, 3), e)

    def test_more_cuts(self):
        a, b, c, d, e = EXAMPLE
        self.assertEqual(affine(a, b, c, ((1, 1), d, e, (6, 6))),
                         ((2, 0), (4, 0), (10, 0), (12, 0)))

    def test_sweep(self):
        counts = sweep()
        print("configurations, opposite orientation =", counts)
        self.assertEqual(counts, (1008, 504))
