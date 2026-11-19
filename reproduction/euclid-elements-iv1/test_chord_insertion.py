import unittest
from fractions import Fraction as Q

from chord_insertion import Point, intersections, sweep, verifies


class ChordInsertionTests(unittest.TestCase):
    def test_radical_pair(self):
        pts = intersections(5, 6)
        self.assertEqual(pts, (Point(Q(7,5), Q(576,25), -1), Point(Q(7,5), Q(576,25), 1)))
        self.assertTrue(all(verifies(5, 6, p) for p in pts))

    def test_irrational_height(self):
        self.assertEqual(intersections(1, 1)[1], Point(Q(1,2), Q(3,4), 1))

    def test_diameter(self):
        self.assertEqual(intersections(5, 10), (Point(Q(-5), Q(0), 0),))

    def test_impossible(self):
        self.assertEqual(intersections(5, 11), ())

    def test_zero_not_chord(self):
        self.assertEqual(intersections(5, 0), (Point(Q(5), Q(0), 0),))

    def test_reject_malformed_witness(self):
        self.assertFalse(verifies(5, 6, Point(Q(7,5), Q(576,25), 0)))
        self.assertFalse(verifies(5, 6, Point(Q(5), Q(0), 0)))

    def test_parameter_domain(self):
        with self.assertRaises(ValueError):
            intersections(0, 1)
        with self.assertRaises(ValueError):
            intersections(1, -1)
        with self.assertRaises(TypeError):
            intersections(1, 0.5)

    def test_grid(self):
        self.assertEqual(sweep(), dict(zero=16, interior=304, diameter=16, impossible=80))
