import unittest
from fractions import Fraction as Q
from same_part import ratios,witness


class SamePartTests(unittest.TestCase):
    def test_worked(self):
        w=witness(3,12,5,20)
        self.assertEqual(w.divisor,4)
        self.assertEqual(w.left,(3,3,3,3))
        self.assertEqual(w.right,(5,5,5,5))
        self.assertEqual(w.pooled,(8,8,8,8))
        self.assertEqual(w.totals(),(12,20,32))

    def test_copy_pools_and_fraction_grid(self):
        count=0
        for a in range(2,25):
            for c in range(2,25):
                for n in range(2,15):
                    b,d=n*a,n*c
                    result=witness(a,b,c,d)
                    self.assertEqual(result.totals(),(b,d,b+d))
                    self.assertEqual(len(result.pooled),n)
                    self.assertEqual(result.pooled,(a+c,)*n)
                    self.assertEqual(ratios(a,b,c,d),(Q(1,n),)*3)
                    count+=1
        self.assertEqual(count,6877)

    def test_unequal_denominators(self):
        self.assertEqual(ratios(3,12,5,15),(Q(1,4),Q(1,3),Q(8,27)))
        with self.assertRaises(ValueError):
            witness(3,12,5,15)

    def test_same_nonunit_fraction_is_not_hypothesis(self):
        self.assertEqual(ratios(4,6,6,9),(Q(2,3),)*3)
        with self.assertRaises(ValueError):
            witness(4,6,6,9)

    def test_unit_precedes_modern_extension(self):
        with self.assertRaises(ValueError):
            witness(1,4,5,20)
        self.assertEqual(witness(1,4,5,20,True).totals(),(4,20,24))

    def test_invalid_distinct_inputs(self):
        for args in ((3,3,4,12),(3,2,4,12),(2,6,0,3),(2,6,True,3),(2,6,3.0,9)):
            with self.assertRaises(ValueError):
                witness(*args)


if __name__=='__main__':
    unittest.main()
