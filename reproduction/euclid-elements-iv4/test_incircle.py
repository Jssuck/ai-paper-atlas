import unittest
from fractions import Fraction as Q

from incircle import FIXTURES, Incircle, bisector_center, construct, grid, kind


class IncircleTests(unittest.TestCase):
    def test_right_and_contact_labels(self):
        self.assertEqual(construct(*FIXTURES["right"]),
                         Incircle((1, 1), 1, (1, 0), (Q(8, 5), Q(9, 5)), (0, 1)))

    def test_acute(self):
        P = FIXTURES["acute"]
        self.assertEqual(kind(*P), "acute")
        result = construct(*P)
        self.assertEqual((result.center, result.radius), ((6, 4), 4))

    def test_obtuse(self):
        P = FIXTURES["obtuse"]
        self.assertEqual(kind(*P), "obtuse")
        result = construct(*P)
        self.assertEqual((result.center, result.radius), ((3, Q(3, 2)), Q(3, 2)))

    def test_orientation_reversal(self):
        A, B, C = FIXTURES["acute"]
        first, reverse = construct(A, B, C), construct(A, C, B)
        self.assertEqual(reverse, Incircle(first.center, first.radius,
                                          first.G, first.F, first.E))

    def test_bisector_reconstruction(self):
        for P in FIXTURES.values():
            self.assertEqual(bisector_center(*P), construct(*P).center)

    def test_degenerate(self):
        with self.assertRaisesRegex(ValueError, "noncollinear"):
            construct((0, 0), (0, 0), (1, 1))
        with self.assertRaisesRegex(ValueError, "noncollinear"):
            construct((0, 0), (1, 1), (2, 2))

    def test_exact_domain(self):
        with self.assertRaisesRegex(ValueError, "irrational side"):
            construct((0, 0), (1, 0), (0, 1))
        with self.assertRaisesRegex(TypeError, "Fraction"):
            construct((0.0, 0), (4, 0), (0, 3))

    def test_similarity_grid(self):
        self.assertEqual(grid(), {"acute": 144, "right": 144,
                                  "obtuse": 288, "invalid": 3})


if __name__ == "__main__":
    unittest.main()
