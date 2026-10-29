import unittest, copy
from fractions import Fraction as F
from geometry import *

class GeometryTests(unittest.TestCase):
    def setUp(self):
        self.pts=[(5,0),(0,5),(-3,-4)]; self.d=(0,0)
        self.cert=make_certificate(self.pts,self.d)
    def test_center(self): self.assertEqual(circumcenter(self.pts),(0,0))
    def test_equidistance(self): self.assertEqual(self.cert['radius_squared'],'25')
    def test_bisectors(self): self.assertEqual(self.cert['bisector_residuals'],['0','0'])
    def test_verify(self): self.assertTrue(verify_certificate(self.cert))
    def test_diameter_zero_direction(self):
        q=make_certificate([(5,0),(-5,0),(0,5)],(0,0))
        self.assertEqual(q['zero_midpoint_directions'],[True,False]); self.assertTrue(verify_certificate(q))
    def test_second_diameter(self): self.assertEqual(make_certificate([(0,5),(5,0),(-5,0)],(0,0))['zero_midpoint_directions'],[False,True])
    def test_obtuse_external_center(self):
        p=[(0,0),(4,0),(1,1)]; self.assertEqual(circumcenter(p),(2,-1))
        self.assertTrue(verify_certificate(make_certificate(p,(2,-1))))
    def test_known_circle(self): self.assertEqual(certify_known_circle(self.pts,self.d,self.d,25),self.cert)
    def test_wrong_circle(self):
        with self.assertRaises(ValueError): certify_known_circle(self.pts,self.d,(1,0),25)
    def test_zero_radius(self):
        with self.assertRaises(ValueError): certify_known_circle(self.pts,self.d,self.d,0)
    def test_wrong_candidate(self):
        with self.assertRaises(ValueError): make_certificate(self.pts,(1,0))
    def test_two_equal_insufficient(self):
        p=[(3,4),(3,-4),(-5,0)]; self.assertEqual(distance2(p[0],(3,0)),distance2(p[1],(3,0)))
        with self.assertRaises(ValueError): make_certificate(p,(3,0))
    def test_duplicate(self):
        with self.assertRaises(ValueError): circumcenter([(0,0),(0,0),(1,1)])
    def test_collinear(self):
        with self.assertRaises(ValueError): circumcenter([(0,0),(1,0),(2,0)])
    def test_bool_coordinate(self):
        with self.assertRaises(ValueError): point((True,0))
    def test_float_coordinate(self):
        with self.assertRaises(ValueError): point((0.1,0))
    def test_bad_fraction(self):
        for x in ['1/0','nan','abc']:
            with self.assertRaises(ValueError): scalar(x)
    def test_point_shapes(self):
        for p in [None,3,[1],[1,2,3],{'x':1,'y':2}]:
            with self.assertRaises(ValueError): point(p)
    def test_triangle_shapes(self):
        for p in [None,[],[(0,0)],self.pts+[(1,2)]]:
            with self.assertRaises(ValueError): triangle(p)
    def test_schema_bool_tamper(self):
        q=copy.deepcopy(self.cert);q['schema']=True;self.assertFalse(verify_certificate(q))
    def test_tamper_fields(self):
        for k in self.cert:
            q=copy.deepcopy(self.cert);q[k]=None;self.assertFalse(verify_certificate(q))
    def test_extra_missing(self):
        q=copy.deepcopy(self.cert);q['extra']=0;self.assertFalse(verify_certificate(q))
        del q['extra'];del q['center'];self.assertFalse(verify_certificate(q))
    def test_malformed(self):
        for q in [None,[],{}, {'points':None,'candidate':None}]:self.assertFalse(verify_certificate(q))
    def test_grid_600(self):
        count=0
        for x in range(-2,3):
          for y in range(-2,3):
            for s in [F(1,3),F(2,3),1,2]:
              for pts in [self.pts,[(5,0),(-5,0),(0,5)],[(0,5),(5,0),(-5,0)],[(0,-5),(3,4),(-3,4)],[(5,0),(3,4),(0,5)],[(5,0),(3,4),(3,-4)]]:
                q=[(x+s*a,y+s*b) for a,b in pts]
                cert=certify_known_circle(q,(x,y),(x,y),25*s*s)
                self.assertTrue(verify_certificate(cert));count+=1
        self.assertEqual(count,600)
if __name__=='__main__': unittest.main(verbosity=2)
