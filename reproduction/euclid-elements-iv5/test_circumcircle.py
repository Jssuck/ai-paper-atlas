import unittest
from fractions import Fraction as Q
from itertools import permutations

from circumcircle import circumcircle, grid


class CircumcircleTests(unittest.TestCase):
    def test_acute(self):
        result = circumcircle((0, 0), (4, 0), (1, 3))
        self.assertEqual(result.center, (2, 1))
        self.assertEqual(result.radius_squared, 5)
        self.assertEqual((result.angle_type, result.location), ("acute", "inside"))
        self.assertTrue(all(x > 0 for x in result.barycentric))

    def test_right_labels_and_finite_midpoint(self):
        right = (0, 0)
        tri = (right, (4, 0), (0, 3))
        for order in permutations(tri):
            with self.subTest(order=order):
                result = circumcircle(*order)
                self.assertEqual(result.center, (2, Q(3, 2)))
                self.assertEqual(result.radius_squared, Q(25, 4))
                self.assertEqual((result.angle_type, result.location), ("right", "on_side"))
                self.assertEqual(result.right_vertex, order.index(right))
                self.assertEqual(result.barycentric[result.right_vertex], 0)
                self.assertEqual(sorted(result.barycentric), [0, Q(1, 2), Q(1, 2)])

    def test_obtuse_center_beyond_opposite_side(self):
        tri = ((0, 0), (4, 0), (1, 1))
        o = circumcircle(*tri)
        self.assertEqual(o.center, (2, -1))
        self.assertEqual(o.radius_squared, 5)
        self.assertEqual(o.barycentric, (Q(5, 4), Q(3, 4), -1))
        self.assertEqual((o.angle_type, o.location), ("obtuse", "outside"))

    def test_irrational_radius_squared_exact(self):
        o = circumcircle((0, 0), (1, 0), (0, 1))
        self.assertIsInstance(o.radius_squared, Q)
        self.assertEqual(o.radius_squared, Q(1, 2))

    def test_rational_similarity_with_reflection(self):
        def transform(p):
            x, y = map(Q, p)
            return 1 + (3*x + 4*y)/10, -2 + (4*x - 3*y)/10

        for tri in (((0, 0), (4, 0), (1, 3)),
                    ((0, 0), (4, 0), (0, 3)),
                    ((0, 0), (4, 0), (1, 1))):
            original = circumcircle(*tri)
            reflected = circumcircle(*map(transform, tri))
            self.assertEqual(reflected.center, transform(original.center))
            self.assertEqual(reflected.radius_squared, original.radius_squared / 4)
            self.assertEqual(reflected.barycentric, original.barycentric)

    def test_nearly_collinear_nonzero_is_not_rejected(self):
        o = circumcircle((0, 0), (2, 0), (1, Q(1, 100)))
        self.assertEqual(o.center, (1, Q(-9999, 200)))
        self.assertEqual(o.location, "outside")

    def test_duplicates_collinear_and_float(self):
        for tri in (((1, 1), (1, 1), (4, 0)), ((0, 0), (1, 1), (2, 2))):
            with self.assertRaisesRegex(ValueError, "noncollinear"):
                circumcircle(*tri)
        for bad_point in ((0.0, 0.0), iter((0.0, 0.0))):
            with self.assertRaisesRegex(TypeError, "int or Fraction"):
                circumcircle(bad_point, (1, 0), (0, 1))

    def test_grid(self):
        counts, right_labels = grid()
        self.assertEqual(sum(counts.values()), 1656)
        self.assertEqual(counts, dict(acute=192, right=480, obtuse=816, degenerate=168))
        self.assertEqual(right_labels, (160, 160, 160))


if __name__ == "__main__":
    unittest.main()
