import unittest
from fractions import Fraction as F

from circumcircle import (circumscribe, diagonal_intersection, examples,
                         rectangle_circumcircle, run_grid, verify_square_circle,
                         vertex_distances2)


class Tests(unittest.TestCase):
    def test_rotated(self):
        sq, _, _ = examples()
        self.assertEqual(circumscribe(sq), ((F(3, 2), F(8, 3)), F(10)))
        self.assertTrue(verify_square_circle(sq, *circumscribe(sq)))

    def test_order_both_orientations(self):
        sq, _, _ = examples()
        for i in range(4):
            shifted = sq[i:] + sq[:i]
            for shape in (shifted, shifted[::-1]):
                self.assertEqual(circumscribe(shape), circumscribe(sq))
                self.assertTrue(verify_square_circle(shape, *circumscribe(sq)))
        a, b, c, d = sq
        crossed = a, c, b, d
        with self.assertRaises(ValueError):
            circumscribe(crossed)
        self.assertFalse(verify_square_circle(crossed, *circumscribe(sq)))

    def test_rectangle_extension(self):
        _, rect, _ = examples()
        with self.assertRaises(ValueError):
            circumscribe(rect)
        o, r2 = rectangle_circumcircle(rect)
        self.assertEqual((o, r2), ((2, 1), 5))
        self.assertEqual(vertex_distances2(o, rect), (5, 5, 5, 5))
        self.assertFalse(verify_square_circle(rect, o, r2))

    def test_rhombus_negative_control(self):
        _, _, rhombus = examples()
        o = diagonal_intersection(rhombus)
        self.assertEqual(o, (4, 2))
        self.assertEqual(vertex_distances2(o, rhombus), (20, 5, 20, 5))
        with self.assertRaises(ValueError):
            rectangle_circumcircle(rhombus)

    def test_invalid(self):
        for ps in ([(0, 0)]*4, [(0, 0), (1, 0), (2, 0), (3, 0)],
                   [(0, 0), (1, 0), (1, 0), (0, 1)]):
            with self.assertRaises(ValueError):
                circumscribe(ps)
        with self.assertRaises(ValueError):
            diagonal_intersection([(0, 0)]*4)

    def test_wrong_certificate(self):
        sq, _, _ = examples()
        (x, y), r2 = circumscribe(sq)
        self.assertFalse(verify_square_circle(sq, (x+1, y), r2))
        self.assertFalse(verify_square_circle(sq, (x, y), r2*2))

    def test_inexact_input(self):
        for coordinate in (0.0, False):
            with self.assertRaises(TypeError):
                circumscribe([(coordinate, 0), (2, 0), (2, 2), (0, 2)])

    def test_grid(self):
        self.assertEqual(run_grid(), (360, 3))


if __name__ == "__main__":
    unittest.main()
