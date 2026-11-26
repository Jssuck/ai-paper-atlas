from itertools import product
import unittest
from odd_pair_difference import Witness,odd_pair_difference


class TestDifference(unittest.TestCase):
    def test_worked_and_minimum(self):
        self.assertEqual(odd_pair_difference(19,9),Witness((18,8),(9,4),5,10))
        self.assertEqual(odd_pair_difference(5,3),Witness((4,2),(2,1),1,2))

    def test_modern_boundaries(self):
        for a,b in ((9,9),(9,19),(3,1),(3,-1),(9,0)):
            with self.subTest(a=a,b=b),self.assertRaises(ValueError):
                odd_pair_difference(a,b)
        self.assertEqual([a-b for a,b in ((9,9),(9,19),(3,1),(3,-1))],[0,-10,2,4])

    def test_wrong_parity_and_type(self):
        for args in ((9,4),(10,5),(8,4),(9,3.0),(9,True)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                odd_pair_difference(*args)

    def test_large_exact(self):
        a=10**100+1
        self.assertEqual(odd_pair_difference(a,a-2).half,1)

    def test_paired_counting_oracle(self):
        odd_table={k+k+1:k for k in range(1,32)}
        success=probes=rejected=0
        for a,b in product(range(1,65),repeat=2):
            if a<=b or a not in odd_table or b not in odd_table:
                with self.assertRaises(ValueError):
                    odd_pair_difference(a,b)
                rejected+=1
                continue
            cursor=b
            half=0
            while cursor<a:
                cursor+=2
                half+=1
                probes+=1
            self.assertEqual(cursor,a)
            self.assertEqual(odd_pair_difference(a,b),
                             Witness((a-1,b-1),(odd_table[a],odd_table[b]),half,half+half))
            success+=1
        self.assertEqual((success,rejected,probes),(465,3631,4960))
        print(f"Grid: {success+rejected} ordered pairs; {success} witnesses; {rejected} rejected; {probes} pair increments")
