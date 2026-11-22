import unittest
from collections import Counter
from itertools import permutations,product
from three_measures import direct_common,three


class ThreeMeasureTests(unittest.TestCase):
    def test_direct_branch(self):
        result=three(84,30,42,True)
        self.assertEqual((result.first_measure,result.final_measure,result.branch),(6,6,"direct"))
        self.assertEqual(result.second_rows,())

    def test_reduce_branch(self):
        result=three(84,30,20,True)
        self.assertEqual((result.first_measure,result.final_measure,result.branch),(6,2,"reduce"))
        self.assertEqual(result.first_rows,((84,30,2,24),(30,24,1,6),(24,6,4,0)))
        self.assertEqual(result.second_rows,((20,6,3,2),(6,2,3,0)))

    def test_independent_oracle_and_two_way_grid(self):
        counts=Counter()
        for a,b,c in product(range(1,25),repeat=3):
            out=three(a,b,c)
            d,g=out.first_measure,out.final_measure
            ds=direct_common(a,b,c)
            self.assertEqual(g,max(ds))
            self.assertEqual(ds,direct_common(d,c))
            self.assertTrue(all(not (x%g) for x in (a,b,c)))
            self.assertTrue(all(not (g%x) for x in ds))
            self.assertEqual(out.branch,"direct" if not (c%d) else "reduce")
            for large,small,q,r in out.first_rows+out.second_rows:
                self.assertEqual(large,q*small+r)
                self.assertTrue(0<=r<small)
            counts[out.branch]+=1
        self.assertEqual(sum(counts.values()),13824)
        self.assertEqual(counts,{"direct":10356,"reduce":3468})

    def test_order_can_change_branch_not_measure(self):
        results=[three(*p,ancient_domain=True) for p in permutations((12,18,20))]
        self.assertEqual({x.final_measure for x in results},{2})
        self.assertEqual({x.branch for x in results},{"direct","reduce"})

    def test_pairwise_non_coprime_is_insufficient(self):
        values=(6,10,15)
        self.assertEqual(tuple(max(direct_common(a,b)) for a,b in ((6,10),(6,15),(10,15))),(2,3,5))
        self.assertEqual(three(*values).final_measure,1)
        with self.assertRaises(ValueError):
            three(*values,ancient_domain=True)

    def test_unit_equal_and_invalid_inputs(self):
        self.assertEqual(three(12,1,18).final_measure,1)
        self.assertEqual(three(8,8,8,True).final_measure,8)
        for args in ((0,1,2),(-1,4,6),(3,4,6.0),(True,4,6)):
            with self.assertRaises(ValueError):
                three(*args)


if __name__=='__main__':
    unittest.main()
