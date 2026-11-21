import unittest
from fractions import Fraction as Q
from ratio_chains import A, B, C, D, E, audit, equal_angles, exercise_grid, length, point, require_audit


class VI4Tests(unittest.TestCase):
    def test_exact_example(self):
        r = audit(A, B, C, D, E)
        require_audit(r)
        self.assertEqual(r["f"], point(0, Q(15, 2)))
        self.assertEqual(tuple(length(x,y) for x,y in ((A,B),(B,C),(C,A))), (3,4,5))
        self.assertEqual(tuple(length(x,y) for x,y in ((D,C),(C,E),(E,D))),
                         (Q(9,2),6,Q(15,2)))
        self.assertEqual(r["cuts"], (Q(4,9),)*3)
        self.assertEqual(r["chains"], ((Q(9,16),)*2,(Q(16,25),)*2,(Q(9,25),)*2))

    def test_plain_int_intersection(self):
        r = audit((0,3),(0,0),(4,0),(4,6),(12,0))
        require_audit(r)
        self.assertEqual(r["f"], point(0,9))
        self.assertTrue(all(isinstance(x,Q) for x in r["f"]))

    def test_broken_angles(self):
        bad = point(4,5)
        self.assertFalse(equal_angles(A,B,C,bad,E))
        with self.assertRaisesRegex(ValueError,"equiangular"):
            audit(A,B,C,bad,E)

    def test_reflection_needs_repositioning(self):
        reflected = point(4,Q(-9,2))
        self.assertTrue(equal_angles(A,B,C,reflected,E))
        with self.assertRaisesRegex(ValueError,"same side"):
            audit(A,B,C,reflected,E)
        require_audit(audit(point(0,-3),B,C,reflected,E))

    def test_boundaries(self):
        with self.assertRaises(ValueError):
            audit(A,B,C,D,C)
        with self.assertRaises(ValueError):
            equal_angles(C,B,C,D,E)
        with self.assertRaisesRegex(ValueError,"irrational"):
            length(B,point(1,1))

    def test_grid(self):
        self.assertEqual(exercise_grid(),216)


if __name__ == "__main__":
    unittest.main()
