from itertools import product
import unittest

from power_positions import Term, power_positions


def factor_exponents(n):
    """Independent prime-factor exponent oracle for small bases."""
    exponents=[]
    p=2
    while n>1:
        power=0
        while n%p==0:
            n//=p
            power+=1
        if power:
            exponents.append(power)
        p+=1
    return exponents


class TestPowerPositions(unittest.TestCase):
    def test_unit_and_first_common_position(self):
        seq=power_positions(2,7)
        self.assertEqual(seq[0],Term(1,0,1,None,None,True,True))
        self.assertEqual(seq[6],Term(7,6,64,8,4,True,True))

    def test_extra_powers(self):
        for q,flags in ((4,(True,False)),(8,(False,True)),(64,(True,True))):
            t=power_positions(q,2)[1]
            self.assertEqual((t.actual_square,t.actual_cube),flags)
            self.assertIsNone(t.guaranteed_square_root)
            self.assertIsNone(t.guaranteed_cube_root)

    def test_boundary_and_invalid(self):
        self.assertEqual(len(power_positions(2,1)),1)
        for args in ((1,3),(0,2),(2,0),(2,-1),(True,2),(2,True),(2,3.0)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                power_positions(*args)

    def test_large_exact(self):
        q=10**40+3
        self.assertEqual(power_positions(q,7)[-1],Term(7,6,q**6,q**3,q**2,True,True))

    def test_finite_grid(self):
        actual_sq=actual_cube=guaranteed_sq=guaranteed_cube=guaranteed_both=0
        for q,k in product(range(2,65),range(1,13)):
            e=k
            t=power_positions(q,k+1)[-1]
            self.assertEqual((t.position,t.exponent,t.value),(k+1,e,q**e))
            factors=factor_exponents(q)
            sq=all(e*v%2==0 for v in factors)
            cu=all(e*v%3==0 for v in factors)
            self.assertEqual((t.actual_square,t.actual_cube),(sq,cu))
            self.assertEqual(t.guaranteed_square_root,q**(e//2) if e%2==0 else None)
            self.assertEqual(t.guaranteed_cube_root,q**(e//3) if e%3==0 else None)
            actual_sq+=sq
            actual_cube+=cu
            guaranteed_sq+=e%2==0
            guaranteed_cube+=e%3==0
            guaranteed_both+=e%6==0
        print(f"Grid: 756 nonunit terms; guaranteed square/cube/both {guaranteed_sq}/{guaranteed_cube}/{guaranteed_both}; actual square/cube {actual_sq}/{actual_cube}")
