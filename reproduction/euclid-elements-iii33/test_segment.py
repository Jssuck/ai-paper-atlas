import unittest
from fractions import Fraction as F
from segment import construct, check, sweep

class SegmentTest(unittest.TestCase):
    A, B=(0,0),(4,0)

    def test_three_branches_and_known_centers(self):
        for u, k in [(3,F(-3,2)),(0,0),(-3,F(3,2))]:
            r=construct(self.A,self.B,u,4)
            self.assertEqual(r["center"],(2,k))
            self.assertTrue(all(check(self.A,self.B,u,4,r).values()))

    def test_known_special_witness(self):
        r=construct(self.A,self.B,0,4)
        self.assertEqual(r["alternate"],(2,-2))
        self.assertEqual(r["control"],(2,2))

    def test_wrong_arc_detected(self):
        for u in (1,0,-1):
            r=construct(self.A,self.B,u,1)
            r["alternate"],r["control"]=r["control"],r["alternate"]
            c=check(self.A,self.B,u,1,r)
            self.assertFalse(c["alternate_side"])
            self.assertEqual(c["alternate_angle"],u==0)

    def test_invalid_input(self):
        for a,b,u,v in [(self.A,self.A,1,1),(self.A,self.B,1,0),
                        (self.A,self.B,-1,0),(self.A,self.B,0,-1)]:
            with self.assertRaises(ValueError):
                construct(a,b,u,v)
        with self.assertRaises(TypeError):
            construct(self.A,self.B,1.0,2)

    def test_rational_similarity_and_ray_scaling(self):
        def sim(p): return 1+F(3,5)*p[0]-F(4,5)*p[1], -3+F(4,5)*p[0]+F(3,5)*p[1]
        for u in (-3,0,3):
            r=construct(self.A,self.B,u,4)
            q=construct(sim(self.A),sim(self.B),u*7,28)
            for key in ("center","alternate","control"):
                self.assertEqual(q[key],sim(r[key]))

    def test_sweep(self):
        counts=sweep()
        self.assertEqual(counts,{"acute":156,"right":3,"obtuse":156})

if __name__=="__main__":
    unittest.main()
