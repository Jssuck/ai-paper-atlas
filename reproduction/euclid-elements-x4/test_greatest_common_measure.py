from fractions import Fraction as F
from itertools import permutations,product
from math import lcm
import unittest
from greatest_common_measure import Certificate,greatest_common_measure


class TestThreeMeasures(unittest.TestCase):
    def test_branches(self):
        self.assertEqual(greatest_common_measure(F(21,10),F(9,10),F(6,10)),
                         Certificate(F(3,10),F(3,10),"direct",(7,3,2)))
        self.assertEqual(greatest_common_measure(F(21,10),F(9,10),F(4,10)),
                         Certificate(F(3,10),F(1,10),"delayed",(21,9,4)))

    def test_all_orders(self):
        original=(6,10,15)
        rows=[greatest_common_measure(*terms) for terms in permutations(original)]
        self.assertEqual(len(rows),6)
        self.assertEqual({r.measure for r in rows},{1})
        self.assertEqual({r.pair_measure for r in rows},{2,3,5})
        self.assertTrue(all(r.branch=="delayed" for r in rows))

    def test_equal_and_invalid(self):
        self.assertEqual(greatest_common_measure(3,3,3).counts,(1,1,1))
        for terms in ((3,2,0),(3,-2,1),(3,2,1.0),(3,True,1)):
            with self.subTest(terms=terms),self.assertRaises(ValueError):
                greatest_common_measure(*terms)

    def test_large_exact(self):
        s=F(10**100+1,37)
        self.assertEqual(greatest_common_measure(21*s,9*s,4*s).measure,s)

    def test_bounded_oracle(self):
        values=sorted({F(i,j) for i,j in product(range(1,9),range(1,4))})
        direct=delayed=checks=0
        for a,b,c in product(values,repeat=3):
            scale=lcm(a.denominator,b.denominator,c.denominator)
            sizes=tuple(int(t*scale) for t in (a,b,c))
            candidates=range(1,min(sizes)+1)
            expected=max(d for d in candidates if all(t%d==0 for t in sizes))
            row=greatest_common_measure(a,b,c)
            self.assertEqual(row.measure,F(expected,scale))
            self.assertEqual(row.counts,tuple(t//expected for t in sizes))
            checks+=len(candidates)
            direct+=row.branch=="direct"
            delayed+=row.branch=="delayed"
        self.assertEqual(direct+delayed,len(values)**3)
        print(f"Grid: {len(values)} distinct rational values; {direct+delayed} ordered triples; {direct} direct; {delayed} delayed; {checks} divisor probes")
