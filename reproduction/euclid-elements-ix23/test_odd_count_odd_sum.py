from itertools import product
import unittest
from odd_count_odd_sum import Witness,odd_count_odd_sum


class TestOddCountOddSum(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(odd_count_odd_sum((3,5,7)),Witness(4,3,7,15))
        self.assertEqual(odd_count_odd_sum((7,5,3)),Witness(6,1,7,15))

    def test_singleton_and_wrong_count(self):
        self.assertEqual(sum((5,)),5)
        for seq in ((),(5,),(3,5),(3,5,7,9)):
            with self.subTest(seq=seq),self.assertRaises(ValueError):
                odd_count_odd_sum(seq)

    def test_invalid(self):
        for seq in ((3,3,1),(3,3,-3),(3,3,0),(3,3,2),(3,3,True),(3,3,3.0)):
            with self.subTest(seq=seq),self.assertRaises(ValueError):
                odd_count_odd_sum(seq)

    def test_large_exact(self):
        a=10**100+1
        self.assertEqual(odd_count_odd_sum((a,a+2,a+4)).total,3*a+6)

    def test_grid(self):
        odds={h+h+1:h for h in range(1,4)}
        halves={h+h:h for h in range(1,15)}
        yes=no=0
        for length in range(1,6):
            for seq in product(range(1,8),repeat=length):
                if length not in (3,5) or not all(x in odds for x in seq):
                    with self.assertRaises(ValueError):
                        odd_count_odd_sum(seq)
                    no+=1
                    continue
                prefix=seq[:-1]
                paired=sum(halves[a+b] for a,b in zip(prefix[::2],prefix[1::2]))
                direct=sum(seq)
                half=paired+odds[seq[-1]]
                self.assertEqual(odd_count_odd_sum(seq),Witness(paired,odds[seq[-1]],half,direct))
                self.assertEqual(direct,half+half+1)
                yes+=1
        self.assertEqual((yes,no),(270,19337))
        print(f"Grid: {yes+no} ordered lists; {yes} witnesses; {no} rejected")
