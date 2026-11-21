import unittest
from fractions import Fraction as Q

from ratio_chains import ambiguity, compare, normalized_model, signature, sides2, sweep, transform


class TestVI7(unittest.TestCase):
    def test_opposite_branch_counterexample(self):
        acute, obtuse = ambiguity()
        self.assertEqual(sides2(acute), (9, 5, 8))
        self.assertEqual(sides2(obtuse), (9, 5, 2))
        self.assertEqual(signature(acute)[2], Q(1, 3))
        self.assertEqual(signature(obtuse)[2], Q(-1, 3))
        self.assertEqual(compare(acute, obtuse), (True, True, False, False, False))

    def test_acute_shape(self):
        tri, _ = ambiguity()
        self.assertEqual(compare(tri, transform(tri, Q(3, 5), False, (3, 4))), (True,)*5)

    def test_obtuse_reflected_shape(self):
        _, tri = ambiguity()
        self.assertEqual(compare(tri, transform(tri, Q(7, 3), True, (5, -2))), (True,)*5)

    def test_tangent_right(self):
        tri = (0, 0), (4, 0), (2, 2)
        self.assertEqual(signature(tri)[2], 0)
        self.assertEqual(normalized_model(4, (1, 1), 8), (2, 0, "right"))
        self.assertEqual(compare(tri, transform(tri, Q(3, 2), True, (2, 5))), (True,)*5)

    def test_no_positive_root(self):
        self.assertEqual(normalized_model(4, (1, 1), 4), (2, -8, "none"))
        self.assertEqual(normalized_model(4, (-1, 1), 16), (-2, 16, "none"))

    def test_only_acute_root(self):
        self.assertEqual(normalized_model(4, (1, 1), 16), (2, 16, "one-acute"))
        self.assertEqual(normalized_model(4, (-1, 1), 25), (-2, 34, "one-acute"))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            signature(((0, 0), (1, 0), (2, 0)))
        for args in ((0, (1, 1), 2), (4, (1, 0), 2), (4, (1, 1), 0)):
            with self.assertRaises(ValueError):
                normalized_model(*args)

    def test_sweep(self):
        result = sweep()
        print(f"same branch, opposite branch, right subset, no-root inputs = {result}", flush=True)
        self.assertEqual(result, (504, 432, 72, 12))
