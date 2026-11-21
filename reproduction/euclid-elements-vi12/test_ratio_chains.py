import unittest
from fractions import Fraction as Q
from ratio_chains import construct, certificate, positions, intersection, sweep


class FourthProportional(unittest.TestCase):
    def test_reference(self):
        points = construct(4, 6, 8)
        self.assertEqual(points, ((0,0), (4,0), (10,0), (0,8), (0,20)))
        self.assertEqual(certificate(4,6,8,points), 12)

    def test_special_third(self):
        self.assertEqual(certificate(4,6,6,construct(4,6,6)), 9)

    def test_swap_and_equal(self):
        self.assertEqual(certificate(6,4,8,construct(6,4,8)), Q(16,3))
        self.assertEqual(certificate(4,4,8,construct(4,4,8)), 8)

    def test_wrong_copy(self):
        D,G,E,H,v = positions(4,4,8,(0,0),(1,0),(0,1))
        F = intersection(D,G,E,H,v)
        self.assertEqual(F, (0,16))
        self.assertEqual(certificate(4,4,8,(D,G,E,H,F)), 8)
        with self.assertRaisesRegex(ValueError, "copied"):
            certificate(4,6,8,(D,G,E,H,F))

    def test_off_parallel(self):
        wrong = (*construct(4,6,8)[:-1], (0,19))
        with self.assertRaisesRegex(ValueError, "parallel"):
            certificate(4,6,8,wrong)

    def test_invalid(self):
        for args in ((0,6,8), (4,-1,8), (4,6,8.0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                construct(*args)
        for v in ((-1,0), (1,1)):
            with self.subTest(v=v), self.assertRaises(ValueError):
                construct(4,6,8,v=v)

    def test_reverse_tail(self):
        wrong = (*construct(4,6,8)[:-1], (0,6))
        with self.assertRaisesRegex(ValueError, "order"):
            certificate(4,6,8,wrong)

    def test_sweep(self):
        result = sweep()
        print("configurations, reflected =", result, flush=True)
        self.assertEqual(result, (1536,768))


if __name__ == "__main__":
    unittest.main()
