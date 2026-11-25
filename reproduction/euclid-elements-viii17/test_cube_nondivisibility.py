from fractions import Fraction
from itertools import product
import unittest
from cube_nondivisibility import Trace, inspect


class TestCubeNonmeasurement(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(inspect(6,9),Trace((216,324,486,729),81,3,(8,2),(True,True)))

    def test_vacuous_and_direction(self):
        self.assertEqual(inspect(4,12).cube_then_side_antecedents,(False,False))
        self.assertEqual(inspect(12,4),Trace((1728,576,192,64),64,4,(27,3),(True,True)))

    def test_grid(self):
        n=0
        for c,d in product(range(1,41),repeat=2):
            t=inspect(c,d,modern=True)
            plain,cube = Fraction(d,c),Fraction(d**3,c**3)
            self.assertEqual(t.cube_then_side_denominators,(cube.denominator,plain.denominator))
            _,r=divmod(d,c)
            _,s=divmod(d**3,c**3)
            self.assertEqual((t.cube_remainder,t.side_remainder),(s,r))
            self.assertEqual(t.cube_then_side_antecedents,(s!=0,r!=0))
            self.assertEqual(r==0,s==0)
            a,h,k,b=t.cube_chain
            self.assertEqual(Fraction(h,a),plain)
            self.assertEqual(Fraction(k,h),plain)
            self.assertEqual(Fraction(b,k),plain)
            n+=r!=0
        self.assertEqual(n,1442)
        print("Exact grid: 1600; 1442 triggered and 158 vacuous in each branch")

    def test_remainders_are_not_cubes(self):
        t=inspect(6,10)
        self.assertEqual((t.cube_remainder,t.side_remainder),(136,4))
        self.assertNotEqual(t.cube_remainder,t.side_remainder**3)
        c=10**80+1
        self.assertEqual(inspect(c,7*c+1).cube_then_side_denominators,(c**3,c))

    def test_domain(self):
        self.assertEqual(inspect(1,3,modern=True).cube_then_side_antecedents,(False,False))
        self.assertEqual(inspect(8,8,modern=True).cube_then_side_antecedents,(False,False))
        for pair in ((1,3),(8,8),(0,2),(-2,3),(True,3),(2.0,3)):
            with self.subTest(pair=pair),self.assertRaises(ValueError):
                inspect(*pair)
