import unittest,copy
from fractions import Fraction as Q
from geometry import *
from cases import valid_cases,invalid_cases
class Tests(unittest.TestCase):
    def setUp(self): self.args=((0,0),(3,0),(0,4));self.p=construct(*self.args)
    def test_basic(self): self.assertTrue(verify(*self.args,self.p))
    def test_D(self): self.assertEqual(self.p['D'],(Q(-3),Q(0)))
    def test_side_chain(self): self.assertEqual(report(self.p)['DC_squared'],'25')
    def test_rational_sqrt(self): self.assertEqual(rational_sqrt(Q(9,16)),Q(3,4))
    def test_negative_sqrt(self): self.assertRaises(ValueError,rational_sqrt,-1)
    def test_irrational_sqrt(self): self.assertRaises(ValueError,rational_sqrt,Q(2))
    def test_sqrt_bool(self): self.assertRaises(ValueError,rational_sqrt,True)
    def test_family(self):
        for args in valid_cases(): self.assertTrue(verify(*args,construct(*args)))
    def test_invalid(self):
        for args in invalid_cases():
            with self.assertRaises(ValueError): construct(*args)
    def test_missing(self):
        for k in 'ABCD':
            p=self.p.copy();del p[k];self.assertFalse(verify(*self.args,p))
    def test_extra(self): p=self.p.copy();p['X']=(0,0);self.assertFalse(verify(*self.args,p))
    def test_tamper(self):
        for k in 'ABCD':
            for i in [0,1]:
                p=self.p.copy();v=list(p[k]);v[i]+=Q(1,7);p[k]=v;self.assertFalse(verify(*self.args,p))
    def test_same_side(self): p=self.p.copy();p['D']=self.p['B'];self.assertFalse(verify(*self.args,p))
    def test_origin_D(self): p=self.p.copy();p['D']=(0,0);self.assertFalse(verify(*self.args,p))
    def test_float_certificate(self): p=self.p.copy();p['D']=(-3.,0);self.assertFalse(verify(*self.args,p))
    def test_bool_certificate(self): p=self.p.copy();p['D']=(-3,False);self.assertFalse(verify(*self.args,p))
    def test_swap(self): p=self.p.copy();p['B'],p['D']=p['D'],p['B'];self.assertFalse(verify(*self.args,p))
    def test_wrong_args(self): self.assertFalse(verify((0,0),(4,0),(0,3),self.p))
    def test_no_certificate(self): self.assertFalse(verify(*self.args,None))
    def test_near_right_rejected(self): self.assertRaises(ValueError,construct,(0,0),(1,0),(Q(1,10**20),1))
    def test_nonhorizontal(self):
        a=((2,3),(4,4),(0,7));self.assertTrue(verify(*a,construct(*a)))
if __name__=='__main__': unittest.main()
