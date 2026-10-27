import unittest
from decimal import Decimal,localcontext
from fractions import Fraction as R
from geometry import *
from run_examples import examples

class FieldTests(unittest.TestCase):
    def test_square_root(self): self.assertEqual(S*S,Q3(3))
    def test_division(self):
        for a in range(-3,4):
          for b in range(-3,4):
            x=Q3(a,b)
            if a or b: self.assertEqual(x/x,Q3(1))
    def test_sign_finite_independent_decimal_check(self):
        with localcontext() as c:
            c.prec=70
            for a in range(-20,21):
              for b in range(-20,21):
                x=Decimal(a)+Decimal(b)*Decimal(3).sqrt()
                self.assertEqual(Q3(a,b).sign(),(x>0)-(x<0))
    def test_zero_division(self):
        with self.assertRaises(ZeroDivisionError): Q3(1)/Q3()

class GeometryTests(unittest.TestCase):
    def test_equilateral_both(self):
        d,e=point(R(1,2),-2),point(3,R(2,3))
        for f in equilateral_vertices(d,e):
            self.assertEqual(dist2(d,f),dist2(d,e)); self.assertEqual(dist2(e,f),dist2(d,e))
    def test_correct_apex(self):
        a,d,e=canonical(1,1)
        self.assertEqual(construct(a,d,e),point(1+S,0))
    def test_same_side_is_sometimes_internal(self):
        a,d,e=canonical(2,1); c=certificate(a,d,e,point(2-S,0))
        self.assertTrue(c['strictly_inside']); self.assertTrue(c['equal_angles']); self.assertFalse(c['opposite_side'])
    def test_same_side_zero(self):
        a,d,e=canonical(S,1); c=certificate(a,d,e,point(0,0))
        self.assertTrue(c['equilateral']); self.assertFalse(c['nonzero_output_ray']); self.assertFalse(c['equal_angles'])
    def test_equal_angles_not_interior(self):
        a,d,e=canonical(1,1); c=certificate(a,d,e,point(1-S,0))
        self.assertTrue(c['equal_angles']); self.assertFalse(c['strictly_inside'])
    def test_unequal_rejected(self):
        with self.assertRaises(ValueError): construct(point(0,0),point(1,1),point(2,-2))
    def test_degeneracies_rejected(self):
        for d,e in [(point(0,0),point(1,0)),(point(1,0),point(1,0)),(point(1,0),point(-1,0))]:
            with self.assertRaises(ValueError): construct(point(0,0),d,e)
    def test_positive_enumeration(self): self.assertEqual(examples()['positive_certificates'],1536)

if __name__=='__main__': unittest.main(verbosity=2)
