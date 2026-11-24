from fractions import Fraction
from itertools import product
import unittest
from square_nondivisibility import Trace, inspect


class TestSquareNonmeasurement(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(inspect(6,9),Trace((36,54,81),3,9,(2,4),(True,True)))

    def test_vacuous_and_direction(self):
        self.assertEqual(inspect(4,12).branches_triggered,(False,False))
        self.assertEqual(inspect(12,4),Trace((144,48,16),4,16,(3,9),(True,True)))

    def test_grid(self):
        n=0
        for c,d in product(range(1,41),repeat=2):
            t=inspect(c,d,modern=True)
            plain, square = Fraction(d,c),Fraction(d*d,c*c)
            self.assertEqual(t.denominators,(plain.denominator,square.denominator))
            _,r=divmod(d,c)
            _,s=divmod(d*d,c*c)
            self.assertEqual((t.side_remainder,t.square_remainder),(r,s))
            self.assertEqual(t.branches_triggered,(s!=0,r!=0))
            self.assertEqual(r==0,s==0)
            n+=r!=0
        self.assertEqual(n,1442)
        print("Exact grid: 1600; 1442 negative antecedents, 158 vacuous in each branch")

    def test_large(self):
        c=10**80+1
        self.assertEqual(inspect(c,7*c).branches_triggered,(False,False))
        self.assertEqual(inspect(c,7*c+1).denominators,(c,c*c))

    def test_domain(self):
        self.assertEqual(inspect(1,3,modern=True).branches_triggered,(False,False))
        self.assertEqual(inspect(8,8,modern=True).branches_triggered,(False,False))
        for pair in ((1,3),(8,8),(0,2),(-2,3),(True,3),(2.0,3)):
            with self.subTest(pair=pair),self.assertRaises(ValueError):
                inspect(*pair)
