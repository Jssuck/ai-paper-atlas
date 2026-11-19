import math
import unittest
from fractions import Fraction as Q
from segment_angles import Segment, classify, dot, examples, rational_grid, square, sub


class SegmentAngleTests(unittest.TestCase):
    def test_exact_grid(self):
        counts = {"major": 0, "minor": 0, "half": 0}
        mapping = {"major": "acute", "minor": "obtuse", "half": "right"}
        for s in rational_grid():
            kind = s.kind()
            counts[kind] += 1
            self.assertEqual(classify(s.inscribed_sign_value()), mapping[kind])
            self.assertEqual(dot(sub(s.a, s.center), s.toward_arc_tangent()), 0)
            # Tangent-side comparison is a modern angle, not the historical curvilinear angle.
            tangent_sign = dot(sub(s.b, s.a), s.toward_arc_tangent())
            self.assertEqual(classify(tangent_sign),
                             {"acute": "obtuse", "obtuse": "acute", "right": "right"}[mapping[kind]])
        self.assertEqual(counts, {"major": 11022, "minor": 3282, "half": 384})

    def test_examples_and_tangent_complement(self):
        for s, expected, tangent_value in zip(examples(), (48, -12, 0), (-24, 24, 0)):
            self.assertEqual(s.inscribed_sign_value(), expected)
            self.assertEqual(dot(sub(s.b, s.a), s.toward_arc_tangent()), tangent_value)
            self.assertAlmostEqual(s.inscribed_angle()+s.modern_limit_angle(), math.pi)

    def test_one_sided_secants(self):
        for s in examples():
            limit = s.modern_limit_angle()
            errors = []
            for i in (8, 64, 512, 4096):
                sample = s.sample_toward_endpoint(i)
                self.assertEqual(square(sub(sample, s.center)), square(sub(s.a, s.center)))
                self.assertGreater(s.chord_side(sample)*s.chord_side(s.p), 0)
                error = limit-s.secant_angle_at_a(sample)
                self.assertAlmostEqual(error, math.atan(Q(1, i)), delta=2e-13)
                errors.append(error)
            self.assertTrue(errors[0] > errors[1] > errors[2] > errors[3] > 0)

    def test_tangent_ray_direction_changes_conclusion(self):
        more, less, _ = tuple(examples())
        for s in (more, less):
            values = tuple(-x for x in s.toward_arc_tangent())
            self.assertNotEqual(classify(dot(sub(s.b, s.a), values)),
                                classify(dot(sub(s.b, s.a), s.toward_arc_tangent())))

    def test_same_segment_other_vertices(self):
        a, b, o = (3, -4), (3, 4), (0, 0)
        for p in ((-5, 0), (0, -5), (-3, 4)):
            s = Segment(o, a, b, p)
            self.assertEqual(s.kind(), "major")
            self.assertAlmostEqual(s.inscribed_angle(), math.atan(Q(4, 3)))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            Segment((0, 0), (3, 4), (3, 4), (5, 0))
        with self.assertRaises(ValueError):
            Segment((0, 0), (3, 4), (3, -4), (6, 0))
        with self.assertRaises(TypeError):
            Segment((0, 0), (3.0, 4), (3, -4), (5, 0))


if __name__ == "__main__":
    unittest.main()
