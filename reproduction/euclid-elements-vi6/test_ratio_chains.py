import unittest
from fractions import Fraction as Q

from ratio_chains import (A, B, C, D, E, F, WRONG_ANGLE, angle_key,
                          exhaustive, squared_sides, sub, verify, witnesses)


class TestVI6(unittest.TestCase):

    def test_witnesses_both_sides(self):
        certificates = verify(A, B, C, D, E, F)
        self.assertEqual({g for g, _, _ in certificates}, {(Q(11, 2), 0), E})
        self.assertEqual(certificates[0][1], (Q(81, 4), 36, Q(225, 4)))

    def test_wrong_included_angle(self):
        self.assertEqual(squared_sides(D, WRONG_ANGLE, F), (Q(81, 4), 36, Q(261, 20)))
        self.assertEqual(angle_key(sub(WRONG_ANGLE, D), sub(F, D)), (1, Q(16, 25)))
        with self.assertRaisesRegex(ValueError, "unequal included"):
            witnesses(A, B, C, D, WRONG_ANGLE, F)

    def test_wrong_ratio(self):
        with self.assertRaisesRegex(ValueError, "ratios unequal"):
            witnesses(A, B, C, D, (14, 0), F)

    def test_nonincluded_angle_ambiguity(self):
        a, b, c, cp = (0, 0), (3, 0), (1, 2), (2, 1)
        sides, sides_p = squared_sides(a, b, c), squared_sides(a, b, cp)
        self.assertEqual(sides, (9, 5, 8))
        self.assertEqual(sides_p, (9, 5, 2))
        self.assertEqual(angle_key(sub(a, b), sub(c, b)),
                         angle_key(sub(a, b), sub(cp, b)))
        with self.assertRaisesRegex(ValueError, "unequal included"):
            witnesses(a, b, c, a, b, cp)

    def test_cosine_sign(self):
        self.assertEqual(angle_key((1, 0), (1, 1)), (1, Q(1, 2)))
        self.assertEqual(angle_key((1, 0), (-1, 1)), (-1, Q(1, 2)))

    def test_degenerate(self):
        with self.assertRaisesRegex(ValueError, "nondegenerate"):
            witnesses(A, B, B, D, E, F)

    def test_sweep(self):
        counts = exhaustive()
        print("configurations, mirrored inputs, certificates =", counts, flush=True)
        self.assertEqual(counts, (288, 144, 576))


if __name__ == "__main__":
    unittest.main(verbosity=2)
