import unittest
from fractions import Fraction as Q

from ratio_chains import construct, verify, sweep, sub, norm2


class TestVI11(unittest.TestCase):
    def test_original(self):
        c = construct(4, 6)
        self.assertEqual(c, ((0, 0), (4, 0), (0, 6), (10, 0), (0, 15)))
        self.assertTrue(verify(c, 4, 6))

    def test_wrong_copy(self):
        c = construct(4, 6, copy_length=4)
        self.assertEqual(c[-1], (0, 12))
        self.assertEqual(norm2(sub(c[-1], c[2])), 36)
        self.assertFalse(verify(c, 4, 6))

    def test_swapping_lengths(self):
        c = construct(6, 4)
        self.assertEqual(c[-1], (0, Q(20, 3)))
        self.assertTrue(verify(c, 6, 4))

    def test_equal_lengths(self):
        c = construct(5, 5)
        self.assertEqual(c[-1], (0, 10))
        self.assertTrue(verify(c, 5, 5))

    def test_reflection(self):
        c = construct(4, 6, (1, 2), (1, 0), (0, -1))
        self.assertEqual(c[-1], (1, -13))
        self.assertTrue(verify(c, 4, 6))

    def test_bad_inputs(self):
        for a, b, v in ((0, 5, (0, 1)), (3, -1, (0, 1)),
                        (3, 5, (-1, 0)), (3, 5, (0, 2)), (3.0, 5, (0, 1))):
            with self.subTest(a=a, b=b, v=v):
                with self.assertRaises(ValueError):
                    construct(a, b, v=v)

    def test_wrong_intersection(self):
        c = construct(4, 6)
        self.assertFalse(verify((*c[:-1], (1, 15)), 4, 6))
        self.assertFalse(verify((*c[:-1], (0, -3)), 4, 6))

    def test_sweep(self):
        count = sweep()
        print("configurations, reflected =", count, flush=True)
        self.assertEqual(count, (576, 288))


if __name__ == "__main__":
    unittest.main()
