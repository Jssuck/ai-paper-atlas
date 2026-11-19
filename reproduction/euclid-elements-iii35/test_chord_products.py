import unittest
from fractions import Fraction as Q

from chord_products import EXAMPLES, audit, sweep


class ChordTests(unittest.TestCase):
    def example(self,name):
        return audit((0,0),5,*EXAMPLES[name])

    def test_center(self):
        z = self.example("center two diameters")
        self.assertTrue(z["iii35_premises"] and z["signed_match"])
        self.assertEqual(z["point"], (0,0))
        self.assertEqual(z["unsigned_products"], (25,25))
        self.assertEqual(z["diameter_count"], 2)

    def test_one_diameter_perpendicular(self):
        z = self.example("one diameter perpendicular")
        self.assertTrue(z["perpendicular"] and z["iii35_premises"])
        self.assertEqual(z["diameter_count"], 1)
        self.assertEqual(z["unsigned_products"], (16,16))
        self.assertEqual(z["midpoints"][1]["offset_sq"], 0)

    def test_neither_diameter(self):
        z = self.example("neither diameter")
        self.assertEqual(z["point"], (3,3))
        self.assertEqual(z["unsigned_products"], (7,7))
        self.assertEqual(z["diameter_count"], 0)
        self.assertTrue(all(m["midpoint_normal"] and m["half_sq"]-m["offset_sq"]==7
                            for m in z["midpoints"]))

    def test_exterior_sign_not_original(self):
        z = self.example("exterior supports")
        self.assertEqual(z["point"], (7,0))
        self.assertEqual(z["directed_products"], (24,24))
        self.assertTrue(z["same_circle"] and z["signed_match"])
        self.assertFalse(z["iii35_premises"])

    def test_invalid_and_off_circle(self):
        z = self.example("off-circle endpoint")
        self.assertTrue(z["inside_both_segments"])
        self.assertFalse(z["iii35_premises"] or z["signed_match"])
        self.assertEqual(z["unsigned_products"], (16,12))
        with self.assertRaises(ValueError):
            audit((0,0),5,(-5,0),(5,0),(-4,3),(4,3))
        with self.assertRaises(ValueError):
            audit((0,0),5,(-5,0),(5,0),(-5,0),(4,3))
        with self.assertRaises(ValueError):
            audit((0,0),0,*EXAMPLES["center two diameters"])

    def test_exact_similarity_and_order(self):
        a,c,b,d = EXAMPLES["neither diameter"]
        def change(p):
            return 1+Q(3,2)*p[1], -2+Q(3,2)*p[0]
        z = audit(change((0,0)),Q(15,2),*(change(p) for p in (d,b,c,a)))
        self.assertTrue(z["iii35_premises"] and z["signed_match"])
        self.assertEqual(z["unsigned_products"],(Q(63,4),Q(63,4)))

    def test_cyclic_sweep(self):
        pts,n,counts,orthogonal = sweep()
        self.assertGreater(pts, 4)
        self.assertEqual(sum(counts),n)
        self.assertGreater(min(counts),0)
        self.assertGreater(orthogonal,0)


if __name__ == "__main__":
    unittest.main()
