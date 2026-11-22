import unittest
from fractions import Fraction as Q
from straight_on import construct,data,det,mul,sub


class StraightOnTests(unittest.TestCase):
    def test_worked(self):
        a,b,c=(0,0),(0,2),(3,0)
        d,e=construct(a,b,c,2)
        self.assertEqual((d,e),((3,-4),(9,-4)))
        self.assertEqual(data(a,b,c,d,e),{"pairs_parallel":(True,True),
                         "pairs_codirected":(True,True),"length_ratio":True,"det":0,"straight_on":True})

    def test_exact_grid(self):
        count=0
        for ab,ac in (((0,2),(3,0)),((1,3),(-2,1)),((Q(3,7),-2),(4,Q(5,6))),((2,1),(1,2))):
            for a in ((0,0),(-5,6),(Q(2,5),Q(-3,7))):
                b,c=tuple(tuple(x+y for x,y in zip(a,v)) for v in (ab,ac))
                for k in (Q(1,7),Q(2,3),1,2,Q(7,3)):
                    d,e=construct(a,b,c,k)
                    out=data(a,b,c,d,e)
                    self.assertTrue(all(out["pairs_codirected"]))
                    self.assertTrue(out["length_ratio"])
                    self.assertTrue(out["straight_on"])
                    self.assertEqual(sub(e,c),mul(k,sub(c,b)))
                    count+=1
        self.assertEqual(count,60)

    def test_one_reversal_is_noncollinear(self):
        a,b,c=(0,0),(0,2),(3,0)
        d,e=construct(a,b,c,2,-1,1)
        self.assertEqual((d,e),((3,4),(9,4)))
        out=data(a,b,c,d,e)
        self.assertEqual(out["pairs_parallel"],(True,True))
        self.assertEqual(out["pairs_codirected"],(False,True))
        self.assertTrue(out["length_ratio"])
        self.assertEqual(out["det"],24)

    def test_two_reversals_overlap(self):
        a,b,c=(0,0),(0,2),(3,0)
        d,e=construct(a,b,c,2,-1,-1)
        out=data(a,b,c,d,e)
        self.assertEqual(out["det"],0)
        self.assertTrue(out["length_ratio"])
        self.assertFalse(out["straight_on"])
        self.assertEqual(sub(e,c),mul(2,sub(b,c)))

    def test_ratios_alone_without_parallelism(self):
        out=data((0,0),(0,2),(3,0),(7,0),(7,6))
        self.assertTrue(out["length_ratio"])
        self.assertEqual(out["pairs_parallel"],(False,False))
        self.assertFalse(out["straight_on"])

    def test_reject_degenerate(self):
        with self.assertRaises(ValueError):
            data((0,0),(1,0),(2,0),(3,0),(3,1))


if __name__=='__main__':
    unittest.main()
