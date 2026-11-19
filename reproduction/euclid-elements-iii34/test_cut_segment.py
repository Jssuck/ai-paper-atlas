from fractions import Fraction as Q
import unittest

import cut_segment as m


class CutSegmentTest(unittest.TestCase):
    def test_cardinal_ray_gives_diameter(self):
        c, p, q = m.construct(5, (0, 4))
        self.assertEqual((c, p, q), ((0,10),(-5,5),(5,5)))
        self.assertEqual(m.signature(m.sub(m.B,p), m.sub(c,p)), (0,50))
        self.assertTrue(all(m.inspect(5,(0,4),c,p,q).values()))

    def test_two_nonright_branches(self):
        for u, sign in ((3,1),(-3,-1)):
            c,p,q = m.construct(5,(u,4))
            self.assertEqual(c, (Q(8*u,5), Q(32,5)))
            ap = m.signature(m.sub(m.B,p), m.sub(c,p))
            aq = m.signature(m.sub(m.B,q), m.sub(c,q))
            self.assertGreater(sign*ap[0],0)
            self.assertLess(sign*aq[0],0)
            self.assertTrue(all(m.inspect(5,(u,4),c,p,q).values()))

    def test_wrong_side_is_not_a_valid_certificate(self):
        for u in (3,0,-3):
            c,p,q = m.construct(5,(u,4))
            swapped = m.inspect(5,(u,4),c,q,p)
            self.assertFalse(swapped["alternate_side"])
            self.assertFalse(swapped["same_side_control"])
            self.assertEqual(swapped["matched_angle"], u == 0)

    def test_off_circle_and_collapsed_chord(self):
        c,p,q = m.construct(5,(3,4))
        self.assertFalse(m.inspect(5,(3,4),c,(-1,1),q)["same_circle"])
        record = m.inspect(5,(3,4),m.B,p,q)
        self.assertFalse(record["distinct"])
        self.assertFalse(record["positive_chord_ray"])
        self.assertFalse(record["matched_angle"])

    def test_positive_scale_invariance_and_invalid_domain(self):
        self.assertEqual(m.construct(5,(3,4)), m.construct(5,(Q(3,7),Q(4,7))))
        self.assertEqual(m.construct(Q(5,2),(3,4)), tuple(
            m.scale(Q(1,2), p) for p in m.construct(5,(3,4))))
        for r, ray in ((0,(1,1)),(-1,(2,1)),(5,(1,0)),(5,(-1,0)),(5,(1,-1)),(5,(0,0))):
            with self.subTest(r=r,ray=ray), self.assertRaises(ValueError):
                m.construct(r,ray)

    def test_exact_sweep(self):
        self.assertEqual(m.finite_sweep(), (237, {"acute":117, "right":3, "obtuse":117}))


if __name__ == "__main__":
    unittest.main()
