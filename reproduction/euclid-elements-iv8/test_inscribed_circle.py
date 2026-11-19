from fractions import Fraction as F
import unittest
from inscribed_circle import EXAMPLE, RECTANGLE, build_square, inscribe, line_distance_squares, run_grid, verify


class InscribedCircleTests(unittest.TestCase):
    def test_axis_aligned(self):
        p = ((0, 0), (4, 0), (4, 4), (0, 4))
        result = ((2, 2), 4, ((2, 0), (4, 2), (2, 4), (0, 2)))
        self.assertEqual(inscribe(p), result)
        self.assertTrue(verify(p, result))

    def test_rational_rotated(self):
        result = ((F(3, 2), F(8, 3)), 5,
                  ((F(5, 2), F(2, 3)), (F(7, 2), F(11, 3)),
                   (F(1, 2), F(14, 3)), (F(-1, 2), F(5, 3))))
        self.assertEqual(inscribe(EXAMPLE), result)
        self.assertTrue(verify(EXAMPLE, result))
        self.assertEqual(line_distance_squares(EXAMPLE, result[0]), (5,) * 4)

    def test_both_boundary_orientations(self):
        p = EXAMPLE[::-1]
        self.assertEqual(inscribe(p)[:2], inscribe(EXAMPLE)[:2])
        self.assertTrue(verify(p, inscribe(p)))

    def test_nonsquare_rectangle(self):
        self.assertEqual(line_distance_squares(RECTANGLE, (2, 1)), (1, 4, 1, 4))
        with self.assertRaises(ValueError):
            inscribe(RECTANGLE)

    def test_zero_side_and_crossed_order(self):
        for p in (build_square((2, 3), (0, 0)),
                  (EXAMPLE[0], EXAMPLE[2], EXAMPLE[1], EXAMPLE[3])):
            with self.assertRaises(ValueError):
                inscribe(p)

    def test_false_certificate(self):
        o, r2, contacts = inscribe(EXAMPLE)
        self.assertFalse(verify(EXAMPLE, (o, r2 + 1, contacts)))
        self.assertFalse(verify(EXAMPLE, (o, r2, contacts[::-1])))
        self.assertFalse(verify(EXAMPLE, (o, r2, (EXAMPLE[0],) + contacts[1:])))

    def test_nonexact_input_rejected(self):
        for x in (0.1, True):
            with self.assertRaises(TypeError):
                build_square((x, 0), (1, 1))

    def test_grid(self):
        self.assertEqual(run_grid(), (360, 3))


if __name__ == "__main__":
    unittest.main()
