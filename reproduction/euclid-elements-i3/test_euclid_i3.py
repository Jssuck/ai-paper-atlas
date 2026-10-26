"""Distinct obligations and adversarial cases; no disabled assert statements."""
import unittest
from fractions import Fraction as F
from euclid_i3 import (Point, Certificate, analytic_witness, verify, domain_status,
                       squared_distance, rational_sqrt, RationalWitnessUnavailable)
from experiments import run_families, mutations


class ExactI3Tests(unittest.TestCase):
    def setUp(self):
        self.a, self.b, self.c = Point(0, 0), Point(5, 0), F(4)
        self.cert = analytic_witness(self.a, self.b, self.c)

    def test_horizontal_known_answer(self):
        self.assertEqual(self.cert.e, Point(2, 0))
        self.assertTrue(verify(self.a, self.b, self.c, self.cert).valid)

    def test_vertical_known_answer(self):
        a, b = Point(2, -3), Point(2, 7)
        self.assertEqual(analytic_witness(a, b, 9).e, Point(2, 0))

    def test_translated_pythagorean_diagonal(self):
        a, b = Point(-2, 7), Point(1, 11)
        self.assertEqual(analytic_witness(a, b, F(25, 4)).e, Point(F(-1, 2), 9))

    def test_reversed_direction(self):
        self.assertEqual(analytic_witness(self.b, self.a, 4).e, Point(3, 0))

    def test_valid_supplied_D_is_not_required_on_AB(self):
        cert = analytic_witness(self.a, self.b, 4, Point(F(6, 5), F(8, 5)))
        self.assertTrue(verify(self.a, self.b, 4, cert).valid)

    def test_incorrect_supplied_D_raises(self):
        with self.assertRaisesRegex(ValueError, "supplied D"):
            analytic_witness(self.a, self.b, 4, Point(0, 3))

    def test_witness_rejects_irrational_target_length(self):
        with self.assertRaises(RationalWitnessUnavailable):
            analytic_witness(self.a, self.b, 2)

    def test_witness_rejects_irrational_AB_length(self):
        with self.assertRaises(RationalWitnessUnavailable):
            analytic_witness(Point(0, 0), Point(1, 1), 1)

    def test_verifier_is_broader_than_witness_builder(self):
        # Both lengths irrational, but their ratio and E are rational.
        a, b, d = Point(0, 0), Point(1, 1), Point(F(1, 2), F(1, 2))
        self.assertTrue(verify(a, b, F(1, 2), Certificate(d, d)).valid)
        with self.assertRaises(RationalWitnessUnavailable):
            analytic_witness(a, b, F(1, 2))

    def test_tiny_exact_segment(self):
        unit = F(1, 10**100)
        a, b = Point(0, 0), Point(unit, 0)
        cert = analytic_witness(a, b, (unit/3)**2)
        self.assertEqual(cert.e.x, unit/3)
        self.assertTrue(verify(a, b, (unit/3)**2, cert).valid)

    def test_huge_translated_coordinates(self):
        a, b = Point(10**100, -10**100), Point(10**100+5, -10**100)
        cert = analytic_witness(a, b, 4)
        self.assertEqual(cert.e.x, 10**100+2)
        self.assertTrue(verify(a, b, 4, cert).valid)

    def test_extremely_close_to_B_still_strict(self):
        r = 1-F(1, 10**100)
        cert = analytic_witness(self.a, Point(1, 0), r*r)
        self.assertTrue(verify(self.a, Point(1, 0), r*r, cert).valid)
        self.assertNotEqual(cert.e, Point(1, 0))

    def test_rational_square_root(self):
        self.assertEqual(rational_sqrt(F(49, 121)), F(7, 11))

    def test_non_square_root_explicitly_unavailable(self):
        for c in (F(2), F(1, 2), F(2, 9)):
            with self.subTest(c=c), self.assertRaises(RationalWitnessUnavailable):
                rational_sqrt(c)

    def test_negative_square_root_rejected(self):
        with self.assertRaises(ValueError):
            rational_sqrt(-1)

    def test_zero_square_root_not_a_strict_cut(self):
        self.assertEqual(rational_sqrt(0), 0)
        with self.assertRaisesRegex(ValueError, "zero_target"):
            analytic_witness(self.a, self.b, 0)

    def test_inexact_coordinate_inputs_rejected(self):
        for value in (0.1, True, "1/2"):
            with self.subTest(value=value), self.assertRaises(TypeError):
                Point(value, 0)

    def test_inexact_squared_length_inputs_rejected(self):
        for value in (4.0, False, "4"):
            with self.subTest(value=value), self.assertRaises(TypeError):
                verify(self.a, self.b, value, self.cert)

    def test_equal_length_policy(self):
        self.assertEqual(domain_status(self.a, self.b, 25), "equal_target")
        cert = Certificate(Point(0, 5), self.b)
        self.assertFalse(verify(self.a, self.b, 25, cert).valid)
        with self.assertRaisesRegex(ValueError, "equal_target"):
            analytic_witness(self.a, self.b, 25)

    def test_longer_length_policy(self):
        self.assertEqual(domain_status(self.a, self.b, 36), "longer_target")
        cert = Certificate(Point(0, 6), Point(6, 0))
        self.assertFalse(verify(self.a, self.b, 36, cert).valid)
        with self.assertRaisesRegex(ValueError, "longer_target"):
            analytic_witness(self.a, self.b, 36)

    def test_zero_length_policy(self):
        self.assertEqual(domain_status(self.a, self.b, 0), "zero_target")
        self.assertFalse(verify(self.a, self.b, 0, Certificate(self.a, self.a)).valid)

    def test_negative_squared_length_policy(self):
        self.assertEqual(domain_status(self.a, self.b, -1), "negative_squared_length")
        self.assertFalse(verify(self.a, self.b, -1, self.cert).valid)
        with self.assertRaisesRegex(ValueError, "negative_squared_length"):
            analytic_witness(self.a, self.b, -1)

    def test_degenerate_AB_policy(self):
        self.assertEqual(domain_status(self.a, self.a, 4), "degenerate_segment")
        self.assertFalse(verify(self.a, self.a, 4, self.cert).valid)
        with self.assertRaisesRegex(ValueError, "degenerate_segment"):
            analytic_witness(self.a, self.a, 4)

    def test_degenerate_all_zero_does_not_pass_vacuously(self):
        result = verify(self.a, self.a, 0, Certificate(self.a, self.a))
        self.assertEqual(set(result.failures), {"admissible_strict_input", "strict_dot_bounds"})

    def test_opposite_circle_intersection_only_fails_direction_bound(self):
        cert = mutations(self.a, self.b, self.cert)["opposite_circle_point"]
        self.assertEqual(verify(self.a, self.b, 4, cert).failures, ("strict_dot_bounds",))

    def test_off_line_equal_distance_only_fails_line_incidence(self):
        cert = mutations(self.a, self.b, self.cert)["off_line_same_distance"]
        self.assertEqual(verify(self.a, self.b, 4, cert).failures, ("E_on_line_AB",))

    def test_beyond_B_is_not_a_cut(self):
        cert = mutations(self.a, self.b, self.cert)["beyond_B"]
        result = verify(self.a, self.b, 4, cert)
        self.assertIn("strict_dot_bounds", result.failures)
        self.assertIn("AE_has_target_length", result.failures)

    def test_radius_transfer_error_not_masked_by_correct_E(self):
        cert = mutations(self.a, self.b, self.cert)["incorrect_transferred_radius"]
        result = verify(self.a, self.b, 4, cert)
        self.assertEqual(set(result.failures), {"supplied_AD_has_target_length",
                                             "E_on_circle_center_A_radius_AD"})
        self.assertTrue(dict(result.checks)["AE_has_target_length"])

    def test_circle_equality_without_target_length_is_insufficient(self):
        result = verify(self.a, self.b, 4, Certificate(Point(0, 1), Point(1, 0)))
        self.assertTrue(dict(result.checks)["E_on_circle_center_A_radius_AD"])
        self.assertFalse(result.valid)

    def test_start_endpoint_is_excluded(self):
        self.assertIn("strict_dot_bounds", verify(self.a, self.b, 4,
                      Certificate(self.cert.d, self.a)).failures)

    def test_end_endpoint_is_excluded(self):
        self.assertIn("strict_dot_bounds", verify(self.a, self.b, 4,
                      Certificate(self.cert.d, self.b)).failures)

    def test_exact_squared_distance_is_translation_invariant(self):
        shift = Point(F(17, 29), F(-31, 37))
        self.assertEqual(squared_distance(self.a, self.b),
                         squared_distance(self.a+shift, self.b+shift))

    def test_finite_family_and_four_adversarial_mutations(self):
        metrics = run_families()
        self.assertEqual(metrics["valid_certificates_accepted"], 600)
        self.assertEqual(metrics["invalid_certificates_rejected"], 2400)
        self.assertEqual(set(metrics["rejections_by_kind"].values()), {600})


if __name__ == "__main__":
    unittest.main(verbosity=2)
