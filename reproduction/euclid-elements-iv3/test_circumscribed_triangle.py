"""Regression tests for the exact IV.3 example and its boundaries."""
from fractions import Fraction as Q
import unittest
from circumscribed_triangle import angle_type, construct, dot, grid, sub, unit


class CircumscribedTest(unittest.TestCase):
    def test_right_fixture(self):
        source, contacts, triangle, _ = construct(Q(1, 2), Q(1, 3), width=5)
        self.assertEqual(source, ((Q(9, 5), Q(12, 5)), (0, 0), (5, 0)))
        self.assertEqual(contacts, ((Q(-4, 5), Q(3, 5)), (0, -1), (Q(3, 5), Q(4, 5))))
        self.assertEqual(triangle, ((Q(-1, 5), Q(7, 5)), (-2, -1), (3, -1)))
        self.assertEqual(angle_type(triangle), "right")

    def test_obtuse_at_e(self):
        _, _, (l, m, n), _ = construct(Q(3, 2), Q(1, 4))
        self.assertLess(dot(sub(l, m), sub(n, m)), 0)

    def test_obtuse_at_f(self):
        _, _, (l, m, n), _ = construct(Q(1, 4), Q(3, 2))
        self.assertLess(dot(sub(l, n), sub(m, n)), 0)

    def test_obtuse_at_d(self):
        _, _, (l, m, n), _ = construct(Q(1, 5), Q(1, 4))
        self.assertLess(dot(sub(m, l), sub(n, l)), 0)

    def test_rotate_translate_scale(self):
        _, contacts, triangle, normals = construct(Q(1, 2), Q(1, 2),
            center=(2, 3), r=2, b=(1, 0))
        self.assertEqual(contacts[1], (4, 3))
        self.assertEqual(normals[1], (1, 0))
        self.assertEqual(triangle[1][0], 4)
        self.assertEqual(triangle[2][0], 4)
        self.assertEqual(angle_type(triangle), "acute")

    def test_near_degeneracy(self):
        eps = Q(1, 10**12)
        _, _, triangle, _ = construct(1, 1-eps, b=unit(Q(2, 3)))
        self.assertEqual(angle_type(triangle), "right")

    def test_invalid_inputs(self):
        for args, kws in (((1, 1), {}), ((2, 1), {}), ((0, 1), {}),
                          ((Q(1, 2), -1), {}), ((Q(1, 2), Q(1, 2)), {"r": 0}),
                          ((Q(1, 2), Q(1, 2)), {"width": 0}),
                          ((Q(1, 2), Q(1, 2)), {"b": (1, 1)})):
            with self.subTest(args=args, kws=kws), self.assertRaises(ValueError):
                construct(*args, **kws)
        with self.assertRaises(TypeError):
            construct(.5, Q(1, 2))

    def test_grid(self):
        self.assertEqual(grid(), {"acute": 456, "right": 384,
                                  "obtuse": 744, "inadmissible": 816})
