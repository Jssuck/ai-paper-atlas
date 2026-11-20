from fractions import Fraction as F
import unittest
from equal_ratio_probes import Quantity as Q, probes, verify, equality_witness, finite_grid


class RatioTests(unittest.TestCase):
    def test_less_forward(self):
        self.assertEqual(verify(Q(2), Q(2), Q(3), 1, 1), ((-1,-1),(1,1)))

    def test_equal_forward(self):
        self.assertEqual(verify(Q(2), Q(2), Q(3), 3, 2)[0], (0,0))

    def test_equal_reverse(self):
        self.assertEqual(verify(Q(2), Q(2), Q(3), 2, 3)[1], (0,0))

    def test_greater_forward(self):
        self.assertEqual(verify(Q(2), Q(2), Q(3), 2, 1)[0], (1,1))

    def test_distinct_objects_same_magnitude(self):
        self.assertEqual(verify(Q(F(2,3)), Q(F(4,6)), Q(1), 3, 2)[0], (0,0))

    def test_mismatch_premise(self):
        with self.assertRaisesRegex(ValueError, "not equal"):
            verify(Q(F(17,16)), Q(F(18,17)), Q(1), 1, 1)

    def test_no_witness_in_finite_grid(self):
        t = Q(F(17,16)), Q(F(18,17)), Q(1)
        for p in range(1, 9):
            for q in range(1, 9):
                f, r = probes(*t, p, q)
                self.assertEqual(f[0], f[1])
                self.assertEqual(r[0], r[1])

    def test_exact_witness_both_directions(self):
        t = Q(F(17,16)), Q(F(18,17)), Q(1)
        self.assertEqual(equality_witness(*t), (16,17,(0,-1)))
        self.assertEqual(probes(*t,17,16)[1], (0,1))
        self.assertIsNone(equality_witness(Q(2), Q(2), Q(3)))

    def test_invalid_domains(self):
        with self.assertRaises(ValueError):
            Q(0)
        with self.assertRaises(TypeError):
            Q(0.1)
        with self.assertRaises(ValueError):
            verify(Q(2), Q(2), Q(3, "area"), 1, 1)
        for p in (0, True, F(1,2)):
            with self.subTest(p=p), self.assertRaises(ValueError):
                verify(Q(2), Q(2), Q(3), p, 1)

    def test_grid(self):
        self.assertEqual(finite_grid(), (1152,(-1,0,1)))
