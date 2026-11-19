from fractions import Fraction
import unittest

from alternate_segments import A, B, C, D, E, F, O, audit, equal_angles, finite_sweep, signature


class AlternateSegmentsTest(unittest.TestCase):
    def test_both_tangent_rays(self):
        self.assertEqual(audit(O, B, D, A, F),
                         {"same_circle": True, "distinct": True, "tangent": True,
                          "opposite": True, "pair": ((4, 2), (80, 40)), "equal": True})
        self.assertEqual(audit(O, B, D, C, E),
                         {"same_circle": True, "distinct": True, "tangent": True,
                          "opposite": True, "pair": ((-4, 2), (-4, 2)), "equal": True})

    def test_same_side_and_non_tangent(self):
        wrong_side = audit(O, B, D, C, F)
        self.assertFalse(wrong_side["opposite"])
        self.assertFalse(wrong_side["equal"])
        secant = audit(O, B, D, A, C)
        self.assertTrue(secant["opposite"])
        self.assertFalse(secant["tangent"])
        self.assertFalse(secant["equal"])

    def test_diameter_exception(self):
        for p, t in (((-5, 5), F), ((5, 5), E)):
            for u in (t, (-t[0], -t[1])):
                result = audit(O, B, A, p, u)
                self.assertEqual(result["opposite"], u == t)
                self.assertTrue(result["equal"])
                self.assertEqual([v[0] for v in result["pair"]], [0, 0])

    def test_predicates_do_not_treat_degeneracy_as_proof(self):
        self.assertFalse(audit(O, B, D, (0, 9), F)["same_circle"])
        for p, t in ((B, F), (D, F), (A, (0, 0))):
            self.assertIsNone(audit(O, B, D, p, t)["equal"])
        self.assertRaises(ValueError, signature, (0, 0), F)
        self.assertFalse(equal_angles((1, 0), (-1, 0)))

    def test_rational_similarity_and_reflection(self):
        def linear(p):
            return ((3*p[0]+4*p[1])*Fraction(2, 5),
                    (4*p[0]-3*p[1])*Fraction(2, 5))

        def invert(p):
            x, y = linear(p)
            return (x+3, y+7)

        for p, t in ((A, F), (C, E)):
            result = audit(*map(invert, (O, B, D, p)), linear(t))
            self.assertTrue(all(result[k] for k in ("same_circle", "distinct", "tangent", "opposite", "equal")))

    def test_finite_sweep(self):
        n, good, same, bad, right = finite_sweep()
        self.assertEqual((n, good, same, bad, right), (47, 4324, 4324, 4232, 92))


if __name__ == "__main__":
    unittest.main()
