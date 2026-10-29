import unittest
from fractions import Fraction as Q
from copy import deepcopy
from geometry import *

class GeometryTests(unittest.TestCase):
    def test_non_diameter(self):
        r=recover_center(*sample()); self.assertEqual(r['F'],(0,0)); self.assertEqual(r['D'],(0,4)); self.assertEqual(r['radius_squared'],25)
    def test_diameter(self):
        r=recover_center(*sample(True)); self.assertEqual(r['D'],r['F']); self.assertEqual(r['branch'],'diameter')
    def test_lower(self): self.assertEqual(recover_center(*sample(lower=True))['D'],(0,-4))
    def test_swapped_ab(self):
        a,b,c,e=sample(); self.assertEqual(recover_center(b,a,c,e)['F'],(0,0))
    def test_swapped_ce(self):
        a,b,c,e=sample(); self.assertEqual(recover_center(a,b,e,c)['F'],(0,0))
    def test_grid(self):
        count=0
        for diameter in (False,True):
          for lower in (False,True):
           for scale in (Q(1,3),1,2,-2,10**30):
            for co,si in ((1,0),(0,1),(Q(3,5),Q(4,5)),(Q(-5,13),Q(12,13))):
             for offset in ((0,0),(3,-7),(Q(1,2),Q(-4,3))):
              r=recover_center(*sample(diameter,scale,co,si,offset,lower)); count+=1
              self.assertEqual(r['F'],offset); self.assertEqual(r['radius_squared'],25*scale*scale); self.assertTrue(verify_certificate(r))
        self.assertEqual(count,240)
    def test_repeated_a(self):
        a,b,c,e=sample()
        with self.assertRaises(ValueError): recover_center(a,a,c,e)
    def test_repeated_c(self):
        a,b,c,e=sample()
        with self.assertRaises(ValueError): recover_center(a,b,c,c)
    def test_not_collinear(self):
        a,b,c,e=sample()
        with self.assertRaises(ValueError): recover_center(a,b,(1,5),e)
    def test_not_perpendicular(self):
        with self.assertRaises(ValueError): recover_center((-1,0),(1,0),(-2,-2),(2,2))
    def test_not_circular(self):
        a,b,c,e=sample()
        with self.assertRaises(ValueError): recover_center(a,b,(0,6),e)
    def test_d_outside(self):
        with self.assertRaises(ValueError): recover_center((-1,8),(1,8),(0,5),(0,-5))
    def test_d_endpoint(self):
        with self.assertRaises(ValueError): recover_center((-1,5),(1,5),(0,5),(0,-5))
    def test_coordinate_types(self):
        for bad in (True,False,1.0,'1',None):
            with self.subTest(bad=bad):
                with self.assertRaises(TypeError): recover_center((bad,4),(3,4),(0,5),(0,-5))
    def test_point_shape(self):
        for bad in ((1,),[1,2,3],None,'12',{'x':1,'y':2}):
            with self.assertRaises(TypeError): recover_center(bad,(3,4),(0,5),(0,-5))
    def test_wrong_midpoint(self):
        r=recover_center(*sample());r['D']=(0,3);self.assertFalse(verify_certificate(r))
    def test_wrong_center(self):
        r=recover_center(*sample());r['F']=(0,1);self.assertFalse(verify_certificate(r))
    def test_wrong_radius(self):
        r=recover_center(*sample());r['radius_squared']=24;self.assertFalse(verify_certificate(r))
    def test_wrong_branch(self):
        r=recover_center(*sample());r['branch']='diameter';self.assertFalse(verify_certificate(r))
    def test_malformed_certificate(self):
        r=recover_center(*sample())
        for bad in ({},None,list(r),{**r,'extra':1}): self.assertFalse(verify_certificate(bad))
    def test_bool_tamper(self):
        r=recover_center(*sample());r['F']=(False,False);self.assertFalse(verify_certificate(r))
    def test_transform_invalid(self):
        for args in ((0,1,0),(1,1,1),(True,1,0)):
            with self.assertRaises((ValueError,TypeError)): transform((1,2),*args)
    def test_extreme_exact(self):
        r=recover_center(*sample(scale=Q(1,10**80),offset=(10**100,-10**100)))
        self.assertEqual(r['radius_squared'],Q(25,10**160));self.assertTrue(verify_certificate(r))

if __name__=='__main__': unittest.main(verbosity=2)
