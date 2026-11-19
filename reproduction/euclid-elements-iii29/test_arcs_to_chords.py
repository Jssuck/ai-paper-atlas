from fractions import Fraction as Q
import math
import unittest
from arcs_to_chords import Arc, pair_grid, unequal_radius_equal_length


class ArcChordTests(unittest.TestCase):
    def test_equal_selected_arc_pairs(self):
        counts = {"minor": 0, "major": 0, "half": 0}
        for a, b in pair_grid():
            self.assertEqual(a.radius, b.radius)
            self.assertEqual(a.radius*a.sweep, b.radius*b.sweep)
            key = "half" if a.sweep == Q(1, 2) else "minor" if a.sweep < Q(1, 2) else "major"
            counts[key] += 1
            x, y = a.coordinate_chord2(), b.coordinate_chord2()
            self.assertTrue(math.isclose(x, y, rel_tol=2e-13, abs_tol=2e-13))
            for chord2, arc in ((x, a), (y, b)):
                self.assertTrue(math.isclose(chord2, arc.trigonometric_chord2(),
                                             rel_tol=2e-13, abs_tol=2e-13))
        self.assertEqual(counts, {"minor": 585, "major": 585, "half": 39})

    def test_exact_axis_cases(self):
        for start in (Q(0), Q(1, 4), Q(1, 2), Q(3, 4)):
            for s, expected in ((Q(1, 4), Q(50, 9)), (Q(1, 2), Q(100, 9)), (Q(3, 4), Q(50, 9))):
                arc = Arc(Q(5, 3), s, start, (7, -8))
                self.assertEqual(arc.exact_quarter_grid_chord2(), expected)
                self.assertAlmostEqual(arc.coordinate_chord2(), float(expected), delta=2e-13)

    def test_turn_sign_and_major_selection(self):
        a = Arc(Q(1), Q(1, 4))
        b = Arc(Q(1), Q(3, 4))
        _, head_a = a.endpoints()
        _, head_b = b.endpoints()
        self.assertGreater(head_a[1], 0)
        self.assertLess(head_b[1], 0)
        self.assertNotEqual(a.radius*a.sweep, b.radius*b.sweep)
        self.assertEqual(a.exact_quarter_grid_chord2(), b.exact_quarter_grid_chord2())

    def test_unequal_radii_counterexample(self):
        a, b = unequal_radius_equal_length()
        self.assertEqual((a.radius*a.sweep, b.radius*b.sweep), (Q(1, 2), Q(1, 2)))
        self.assertEqual((a.exact_quarter_grid_chord2(), b.exact_quarter_grid_chord2()), (4, 8))
        self.assertAlmostEqual(a.coordinate_chord2(), 4, delta=2e-13)
        self.assertAlmostEqual(b.coordinate_chord2(), 8, delta=2e-13)

    def test_translation_and_negative_start_are_wrapped(self):
        a = Arc(Q(4), Q(5, 8), Q(-1, 3), (2, -13))
        b = Arc(Q(4), Q(5, 8), Q(2, 3), (2, -13))
        self.assertEqual(a.endpoints(), b.endpoints())

    def test_out_of_scope(self):
        for r, s in ((0, Q(1, 2)), (1, 0), (1, 1), (1, -Q(1, 2))):
            with self.assertRaises(ValueError):
                Arc(r, s)
        with self.assertRaises(TypeError):
            Arc(1, 0.5)
        with self.assertRaises(ValueError):
            Arc(1, Q(1, 8)).exact_quarter_grid_chord2()


if __name__ == "__main__":
    unittest.main()
