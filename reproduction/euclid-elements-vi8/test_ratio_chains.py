import unittest
from fractions import Fraction as Q

from ratio_chains import angle_key, dist2, projection, sweep, witnesses


class TestVI8(unittest.TestCase):
    def test_15_20_25_example(self):
        a, b, c = (0, 0), (15, 0), (0, 20)
        foot, t, similarities, identities = witnesses(a, b, c)
        self.assertEqual(foot, (Q(48, 5), Q(36, 5)))
        self.assertEqual(t, Q(9, 25))
        self.assertEqual(tuple(dist2(*pair) for pair in [(b, foot), (a, foot),
                         (foot, c), (b, c)]), (81, 144, 256, 625))
        self.assertEqual(similarities, ((True, True),)*3)
        self.assertEqual(identities, ((144**2,)*2, (225**2,)*2, (400**2,)*2))

    def test_wrong_vertex_with_interior_perpendicular(self):
        a, b, c = (0, 0), (3, 0), (2, 4)
        foot, t = projection(a, b, c)
        self.assertEqual(foot, (Q(48, 17), Q(12, 17)))
        self.assertEqual(t, Q(3, 17))
        self.assertEqual(dist2(a, foot), Q(144, 17))
        self.assertEqual(t * (1 - t) * dist2(b, c), Q(42, 17))
        with self.assertRaises(ValueError):
            witnesses(a, b, c)

    def test_right_isosceles_and_vertex_swap(self):
        for b,c in [((2, 0),(0, 2)), ((0, 2),(2, 0))]:
            foot, t, similarities, _ = witnesses((0, 0), b, c)
            self.assertEqual((foot,t), ((1,1), Q(1,2)))
            self.assertEqual(similarities, ((True,True),)*3)

    def test_sign_kept(self):
        self.assertNotEqual(angle_key((0,0), (1,0), (1,1)),
                            angle_key((0,0), (1,0), (-1,1)))

    def test_degenerate(self):
        for a,b,c in [((0,0),(1,1),(1,1)), ((0,0),(0,0),(1,2)),
                      ((0,0),(2,0),(5,0))]:
            with self.assertRaises(ValueError):
                witnesses(a,b,c)

    def test_floats_not_silently_accepted(self):
        with self.assertRaises(TypeError):
            witnesses((0,0),(1.0,0),(0,1))

    def test_matrix(self):
        result = sweep()
        print("configurations, mirrors, similarity pairs, identities =", result, flush=True)
        self.assertEqual(result, (216, 108, 648, 648))


if __name__ == "__main__":
    unittest.main()
