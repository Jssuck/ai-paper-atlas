"""Regression and adversarial tests; unittest checks survive -O and -OO."""

from decimal import Decimal
from fractions import Fraction as F
import itertools
import unittest
from unittest.mock import patch

from euclid_i4 import (
    Certificate, IDENTITY, InputError, Triangle, VerificationError, compare_sas,
    cross, dot, json_exact, matmul, point, rational, result_record, sub, triangle,
    transpose, verify_certificate,
)


class ExactSASTests(unittest.TestCase):
    def setUp(self):
        self.base = Triangle((0, 0), (3, 0), (0, 2))

    def moved(self, cert, source=None):
        return Triangle(*(cert.apply(p) for p in (source or self.base).vertices))

    def test_identity(self):
        r = compare_sas(self.base, self.base)
        self.assertTrue(r.accepted)
        self.assertTrue(r.congruent)
        self.assertTrue(r.orientation_preserving)
        self.assertEqual(r.certificate.q, IDENTITY)
        self.assertEqual(r.certificate.t, (F(0), F(0)))
        self.assertTrue(all(dict(r.checks).values()))

    def test_translation(self):
        cert = Certificate(IDENTITY, (F(2, 3), F(-7, 11)))
        r = compare_sas(self.base, self.moved(cert))
        self.assertEqual(r.certificate, cert)

    def test_rational_rotation_and_offset_origin(self):
        source = Triangle((F(1, 7), F(-2, 3)), (F(5, 7), 2), (-1, F(4, 9)))
        cert = Certificate(((F(3, 5), F(-4, 5)), (F(4, 5), F(3, 5))), (F(7, 3), F(-5, 2)))
        r = compare_sas(source, self.moved(cert, source), require_direct=True)
        self.assertEqual(r.certificate, cert)
        self.assertTrue(r.accepted)
        self.assertEqual(r.certificate.determinant, 1)

    def test_reflection_congruence_and_direct_policy(self):
        cert = Certificate(((1, 0), (0, -1)), (2, 3))
        target = self.moved(cert)
        r = compare_sas(self.base, target)
        self.assertTrue(r.congruent)
        self.assertTrue(r.accepted)
        self.assertFalse(r.orientation_preserving)
        self.assertEqual(r.certificate.determinant, -1)
        direct = compare_sas(self.base, target, require_direct=True)
        self.assertTrue(direct.congruent)
        self.assertFalse(direct.accepted)
        self.assertEqual(direct.reason, "reflection_excluded")

    def test_remaining_side_and_all_vertex_angle_data(self):
        r = compare_sas(self.base, self.moved(Certificate(((0, -1), (1, 0)), (5, 7))))
        self.assertEqual(self.base.side_squares, (9, 4, 13))
        self.assertEqual(self.base.angle_data, ((9, 0, 4), (9, 9, 13), (4, 4, 13)))
        self.assertTrue(dict(r.checks)["remaining_side_squared_equal"])
        self.assertTrue(dict(r.checks)["all_corresponding_angle_data_equal"])

    def test_wrong_correspondence_rejected_for_scalene_triangle(self):
        target = Triangle(self.base.a, self.base.c, self.base.b)
        r = compare_sas(self.base, target)
        self.assertEqual(r.sas_equal, (False, False, True))
        self.assertFalse(r.congruent)
        self.assertIsNone(r.certificate)

    def test_symmetric_relabelling_is_not_always_wrong(self):
        source = Triangle((0, 0), (1, 0), (0, 1))
        target = Triangle(source.a, source.c, source.b)
        r = compare_sas(source, target)
        self.assertTrue(r.congruent)
        self.assertFalse(r.orientation_preserving)

    def test_shear_preserves_two_lengths_but_fails_included_dot(self):
        source = Triangle((0, 0), (1, 0), (F(-1, 2), 1))
        shear = Certificate(((1, 1), (0, 1)), (0, 0))
        target = self.moved(shear, source)
        r = compare_sas(source, target)
        self.assertEqual(r.sas_equal, (True, True, False))
        self.assertFalse(r.accepted)
        checks = verify_certificate(source, target, shear)
        self.assertTrue(all(checks[k] for k in ("maps_A_to_D", "maps_B_to_E", "maps_C_to_F")))
        self.assertFalse(checks["orthogonal"])
        self.assertEqual(shear.determinant, 1)  # area/orientation alone is insufficient

    def test_ssa_counterexample_nonincluded_angle(self):
        one = Triangle((0, 0), (4, 0), (1, 1))
        two = Triangle((0, 0), (4, 0), (3, 3))
        self.assertEqual(one.side_squares, (16, 2, 10))
        self.assertEqual(two.side_squares, (16, 18, 10))
        self.assertEqual(one.side_squares[0], two.side_squares[0])
        self.assertEqual(one.side_squares[2], two.side_squares[2])
        self.assertEqual(cross(one.v, two.v), 0)
        self.assertGreater(dot(one.v, two.v), 0)  # same ray, hence same angle at A
        self.assertEqual(compare_sas(one, two).sas_equal, (True, False, False))
        self.assertFalse(compare_sas(one, two).congruent)

    def test_scale_not_isometry(self):
        target = self.moved(Certificate(((2, 0), (0, 2)), (0, 0)))
        self.assertFalse(compare_sas(self.base, target).accepted)

    def test_wrong_translation_invalidates_mapping(self):
        checks = verify_certificate(self.base, self.base, Certificate(IDENTITY, (1, 0)))
        self.assertTrue(checks["orthogonal"])
        self.assertFalse(checks["maps_A_to_D"])
        self.assertFalse(checks["maps_B_to_E"])
        self.assertFalse(checks["maps_C_to_F"])

    def test_independent_checker_never_calls_sas(self):
        with patch("euclid_i4.compare_sas", side_effect=RuntimeError("must not be called")):
            self.assertTrue(all(verify_certificate(self.base, self.base, Certificate(IDENTITY, (0, 0))).values()))

    def test_runtime_invariant_is_not_an_assert_statement(self):
        with patch("euclid_i4.verify_certificate", return_value={"orthogonal": False}):
            with self.assertRaisesRegex(VerificationError, "failed exact"):
                compare_sas(self.base, self.base)

    def test_inverse_certificate_and_composition(self):
        q = ((F(3, 5), F(-4, 5)), (F(4, 5), F(3, 5)))
        cert = Certificate(q, (2, -1))
        target = self.moved(cert)
        backward = compare_sas(target, self.base).certificate
        self.assertEqual(matmul(backward.q, q), IDENTITY)
        for p in self.base.vertices:
            self.assertEqual(backward.apply(cert.apply(p)), p)

    def test_very_large_and_small_rationals_remain_exact(self):
        n = 10**80
        source = Triangle((0, 0), (F(1, n), 0), (0, F(n, 7)))
        cert = Certificate(((0, 1), (-1, 0)), (F(1, 13), n))
        self.assertEqual(compare_sas(source, self.moved(cert, source)).certificate, cert)

    def test_negative_source_orientation(self):
        source = Triangle((0, 0), (0, 2), (3, 0))
        cert = Certificate(((0, -1), (1, 0)), (3, 1))
        r = compare_sas(source, self.moved(cert, source))
        self.assertLess(source.determinant, 0)
        self.assertTrue(r.orientation_preserving)
        self.assertEqual(r.certificate, cert)

    def test_all_six_simultaneous_vertex_permutations(self):
        cert = Certificate(((0, 1), (1, 0)), (F(1, 2), F(2, 3)))
        target = self.moved(cert)
        for permutation in itertools.permutations(range(3)):
            with self.subTest(permutation=permutation):
                source_p = Triangle(*(self.base.vertices[i] for i in permutation))
                target_p = Triangle(*(target.vertices[i] for i in permutation))
                self.assertEqual(compare_sas(source_p, target_p).certificate, cert)

    def test_raw_list_input_and_fraction_output(self):
        r = compare_sas([[0, 0], [3, 0], [0, 2]], self.base)
        self.assertTrue(r.accepted)
        self.assertIs(type(r.certificate.q[0][0]), F)

    def test_exact_json_schema(self):
        record = result_record(compare_sas(self.base, self.base))
        self.assertEqual(record["Q"], [["1", "0"], ["0", "1"]])
        self.assertEqual(record["det_Q"], "1")
        self.assertEqual(json_exact({"x": F(2, 3)}), {"x": "2/3"})


class InputValidationTests(unittest.TestCase):
    def test_coordinate_types_rejected(self):
        bad = [True, False, 1.0, float("nan"), float("inf"), float("-inf"),
               "1", "1/2", "NaN", None, complex(1, 0), Decimal("0.5"), [], {}]
        for value in bad:
            with self.subTest(type=type(value).__name__, value=str(value)):
                with self.assertRaisesRegex(InputError, "expected int or Fraction"):
                    Triangle((value, 0), (1, 0), (0, 1))

    def test_allowed_scalars_are_normalized(self):
        self.assertEqual(rational(-3), F(-3))
        self.assertEqual(rational(F(2, 6)), F(1, 3))

    def test_malformed_points(self):
        for value in [None, 1, "12", {0: 1, 1: 2}, (), (1,), (1, 2, 3), iter([1, 2])]:
            with self.subTest(value=type(value).__name__):
                with self.assertRaises(InputError):
                    point(value)

    def test_malformed_triangle_containers(self):
        for value in [None, 1, "abc", {}, [], [(0, 0)], [(0, 0)] * 4, iter([])]:
            with self.subTest(value=type(value).__name__):
                with self.assertRaises(InputError):
                    triangle(value)

    def test_repeated_and_collinear_vertices_rejected(self):
        for vertices in [((0, 0), (0, 0), (1, 1)), ((0, 0), (1, 1), (1, 1)),
                         ((0, 0), (1, 1), (2, 2)), ((0, 0), (0, 1), (0, 2)),
                         ((F(1, 3), F(1, 3)), (F(2, 3), F(2, 3)), (1, 1))]:
            with self.subTest(vertices=vertices):
                with self.assertRaisesRegex(InputError, "nonzero determinant"):
                    Triangle(*vertices)

    def test_degenerate_target_is_not_a_sas_false_result(self):
        with self.assertRaises(InputError):
            compare_sas(((0, 0), (1, 0), (0, 1)), ((0, 0), (1, 0), (2, 0)))

    def test_invalid_policy(self):
        valid = ((0, 0), (1, 0), (0, 1))
        for value in [0, 1, None, "false"]:
            with self.subTest(value=value):
                with self.assertRaisesRegex(InputError, "require_direct"):
                    compare_sas(valid, valid, require_direct=value)

    def test_bad_certificate_matrix_and_translation(self):
        for value in [None, (), ((1, 0),), ((1, 0, 0), (0, 1)), ((1.0, 0), (0, 1))]:
            with self.subTest(matrix=value):
                with self.assertRaises(InputError):
                    Certificate(value, (0, 0))
        with self.assertRaises(InputError):
            Certificate(IDENTITY, (0, float("inf")))

    def test_wrong_certificate_object(self):
        valid = ((0, 0), (1, 0), (0, 1))
        with self.assertRaisesRegex(InputError, "expected Certificate"):
            verify_certificate(valid, valid, {"q": IDENTITY, "t": (0, 0)})


if __name__ == "__main__":
    unittest.main(verbosity=2)
