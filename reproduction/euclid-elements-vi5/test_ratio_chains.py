import unittest
from fractions import Fraction as Q
from ratio_chains import ABC, A, B, C, D, E, F, M, N, angles, probe, sides, exercise_grid


class VI5Tests(unittest.TestCase):
    def test_common_base(self):
        p = probe(ABC, (D, E, F))
        self.assertEqual(p["g"], D)
        self.assertTrue(p["same_half_plane"])
        self.assertEqual(sides(ABC), (9, 16, 25))
        self.assertEqual(sides((D, E, F)), (Q(81, 4), 36, Q(225, 4)))
        self.assertEqual(p["side_ratios_sq"], (Q(9, 4),)*3)
        self.assertTrue(all(p[k] for k in ("proportional", "copied_angles", "equal_angles", "ss_equal")))

    def test_reflection(self):
        p = probe(ABC, (M, E, F))
        self.assertEqual(p["g"], D)
        self.assertFalse(p["same_half_plane"])
        self.assertTrue(all(p[k] for k in ("proportional", "copied_angles", "equal_angles", "ss_equal")))

    def test_third_side_needed(self):
        p = probe(ABC, (N, E, F))
        self.assertEqual(p["side_ratios_sq"], (Q(9, 4), Q(9, 4), Q(477, 500)))
        self.assertTrue(p["copied_angles"])
        self.assertFalse(any(p[k] for k in ("proportional", "equal_angles", "ss_equal")))

    def test_bad_correspondence(self):
        p = probe(ABC, (D, F, E))
        self.assertFalse(p["proportional"])
        self.assertFalse(p["equal_angles"])
        self.assertNotEqual(angles(ABC), angles((D, F, E)))

    def test_domain_guard(self):
        with self.assertRaises(ValueError):
            probe((B, B, C), (D, E, F))
        with self.assertRaises(ValueError):
            probe((A, B, C), (D, E, E))

    def test_grid(self):
        self.assertEqual(exercise_grid(), 216)
