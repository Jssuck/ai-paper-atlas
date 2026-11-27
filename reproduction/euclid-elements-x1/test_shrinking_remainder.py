from fractions import Fraction as F
from itertools import product
import unittest
from shrinking_remainder import Audit,audit_remainders


class TestRemainders(unittest.TestCase):
    def test_example_and_generator(self):
        self.assertEqual(audit_remainders(5,iter((12,5,2))),Audit(3,2,2))

    def test_diagram_and_mixed_cuts(self):
        self.assertEqual(audit_remainders(2, (5, 2, F(3, 4))), Audit(3, 2, 2))
        self.assertEqual(audit_remainders(1, (8, 4, F(3, 2), F(3, 4)), allow_half=True), Audit(9, 4, 3))

    def test_exact_half_and_threshold_equality(self):
        with self.assertRaises(ValueError):
            audit_remainders(4,(8,4,2))
        self.assertEqual(audit_remainders(4,(8,4,2),allow_half=True),Audit(3,2,2))
        with self.assertRaises(ValueError):
            audit_remainders(5,(12,5))

    def test_monotone_not_sufficient_and_types(self):
        r=[F(5)+F(1,2**i) for i in range(10)]
        self.assertTrue(all(a>b>5 for a,b in zip(r,r[1:])))
        for x,rows in ((5,r),(5,(12,4,0)),(5,(12,4,-1)),(5.0,(12,4)),(5,(12,True))):
            with self.subTest(x=x,rows=rows), self.assertRaises(ValueError):
                audit_remainders(x,rows)

    def test_grid(self):
        strict=weak=checked=0
        for start,x,scale in product(range(2,33),range(1,32),(F(1,3),F(2,5),F(1,2))):
            if x>=start:
                continue
            rows=[start*scale**i for i in range(10)]
            cutoff=next(i for i,t in enumerate(rows) if t<x)
            n=next(j for j in range(1,start+2) if j*x>start)
            k=next(j for j in range(10) if start<x*2**j)
            self.assertEqual(audit_remainders(x,rows,allow_half=scale==F(1,2)),Audit(n,k,cutoff))
            checked+=len(rows)
            if scale==F(1,2):
                weak+=1
            else:
                strict+=1
        self.assertEqual((strict,weak,checked),(992,496,14880))
        print(f"Grid: {strict} strict chains, {weak} equality chains, {checked} remainders")
