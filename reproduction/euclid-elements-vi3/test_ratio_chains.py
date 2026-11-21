import unittest
from fractions import Fraction as F

from ratio_chains import (A, B, C, D, P, Q, construct_e, exercise_grid,
                          point, probe, rational_norm, sub)


class VI3Tests(unittest.TestCase):
    def test_interior_bisector(self):
        got = probe(A, B, C, D)
        self.assertEqual(got["parameter"], F(3, 7))
        self.assertEqual(got["segment_ratio"], F(3, 4))
        self.assertEqual(got["side_ratio"], F(3, 4))
        self.assertTrue(got["interior_bisector"])
        self.assertFalse(got["external_bisector_line"])

    def test_transposed_ratio(self):
        got = probe(A, B, C, Q)
        self.assertEqual(got["segment_ratio"], F(4, 3))
        self.assertEqual(got["cosine_delta_times_ad"], -7)
        self.assertFalse(got["equal_ratio"])
        self.assertFalse(got["interior_bisector"])

    def test_external_unsigned_counterexample(self):
        got = probe(A, B, C, P)
        self.assertEqual(got["parameter"], -3)
        self.assertEqual(rational_norm(sub(P, B)), 105)
        self.assertEqual(rational_norm(sub(P, C)), 140)
        self.assertTrue(got["equal_ratio"])
        self.assertFalse(got["interior"])
        self.assertFalse(got["interior_bisector"])
        self.assertTrue(got["external_bisector_line"])

    def test_auxiliary_construction(self):
        e = construct_e(A, B, C, D)
        self.assertEqual(e, point(-28, 0))
        self.assertEqual(rational_norm(sub(e, A)), rational_norm(sub(C, A)))
        e2 = construct_e(A, B, C, Q)
        self.assertEqual(e2, point(F(-63, 4), 0))
        self.assertNotEqual(rational_norm(sub(e2, A)), rational_norm(sub(C, A)))
        int_result = construct_e((0, 0), (21, 0), (0, 28), (9, 16))
        self.assertEqual(int_result, (F(-63, 4), F(0)))
        self.assertIsInstance(int_result[0], F)

    def test_domains(self):
        for d in (B, C, point(0, 1)):
            with self.assertRaises(ValueError):
                probe(A, B, C, d)
        with self.assertRaises(ValueError):
            probe(A, B, point(5, 0), D)
        with self.assertRaises(ValueError):
            probe(A, B, point(1, 1), point(11, F(1, 2)))

    def test_grid(self):
        self.assertEqual(exercise_grid(), (1224, 45))


if __name__ == "__main__":
    unittest.main()
