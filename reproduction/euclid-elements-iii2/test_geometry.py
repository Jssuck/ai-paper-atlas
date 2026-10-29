import unittest
from fractions import Fraction as Q
from geometry import certificate,verify_certificate,sqdist,grid_records

class GeometryTests(unittest.TestCase):
    def good(self,t=Q(1,2)): return certificate((0,0),25,(-3,4),(3,4),t)
    def test_midpoint(self): self.assertEqual(self.good()['E'],(Q(0),Q(4)))
    def test_gap(self): self.assertEqual(self.good()['gap'],9)
    def test_identity(self):
        r=self.good(Q(1,4));self.assertEqual(r['distance_squared']+r['gap'],r['radius_squared'])
    def test_endpoints(self):
        for t in (0,1):
            r=self.good(t);self.assertEqual(r['gap'],0);self.assertEqual(r['branch'],'endpoint')
    def test_diameter_center(self):
        r=certificate((0,0),25,(-5,0),(5,0),Q(1,2));self.assertEqual(r['branch'],'center');self.assertEqual(r['distance_squared'],0)
    def test_diameter_other(self): self.assertEqual(certificate((0,0),25,(-5,0),(5,0),Q(1,4))['gap'],Q(75,4))
    def test_coincident(self):
        with self.assertRaises(ValueError): certificate((0,0),25,(3,4),(3,4),Q(1,2))
    def test_wrong_circle(self):
        with self.assertRaises(ValueError): certificate((0,0),25,(3,4),(3,5),Q(1,2))
    def test_nonpositive(self):
        for r in (0,-1):
            with self.assertRaises(ValueError): certificate((0,0),r,(3,4),(-3,4),Q(1,2))
    def test_extrapolation(self):
        for t in (-1,2):
            with self.assertRaises(ValueError): self.good(t)
    def test_scalar_types(self):
        for t in (True,False,0.5,'1/2',None):
            with self.assertRaises(TypeError): self.good(t)
    def test_point_types(self):
        for p in ((True,0),(0.0,0),(0,),{},'00',None):
            with self.assertRaises(TypeError): certificate(p,25,(-3,4),(3,4),Q(1,2))
    def test_radius_bool(self):
        with self.assertRaises(TypeError): certificate((0,0),True,(-1,0),(1,0),Q(1,2))
    def test_verified(self): self.assertTrue(verify_certificate(self.good()))
    def test_tampered_fields(self):
        for key in ('radius_squared','t','chord_squared','distance_squared','gap'):
            r=self.good();r[key]+=1;self.assertFalse(verify_certificate(r))
        for key in ('center','A','B','E'):
            r=self.good();r[key]=(r[key][0]+1,r[key][1]);self.assertFalse(verify_certificate(r))
    def test_tampered_branch(self):
        r=self.good();r['branch']='endpoint';self.assertFalse(verify_certificate(r))
    def test_schema(self):
        for value in (None,[],True): self.assertFalse(verify_certificate(value))
        r=self.good();del r['gap'];self.assertFalse(verify_certificate(r))
        r=self.good();r['extra']=0;self.assertFalse(verify_certificate(r))
    def test_typed_certificate(self):
        r=self.good(0);r['t']=False;self.assertFalse(verify_certificate(r))
        r=self.good();r['E']=[Q(0),Q(4)];self.assertFalse(verify_certificate(r))
        r=self.good();r['E']=(False,Q(4));self.assertFalse(verify_certificate(r))
    def test_translation(self):
        r=certificate((10,-2),25,(7,2),(13,2),Q(1,2));self.assertEqual(r['gap'],self.good()['gap'])
    def test_rotation(self):
        r=certificate((0,0),25,(-4,-3),(-4,3),Q(1,2));self.assertEqual(r['gap'],9)
    def test_scaling(self):
        r=certificate((0,0),Q(25,9),(-1,Q(4,3)),(1,Q(4,3)),Q(1,2));self.assertEqual(r['gap'],1)
    def test_grid(self):
        n=0
        for r in grid_records():
            n+=1;self.assertTrue(verify_certificate(r));self.assertEqual(r['distance_squared']+r['gap'],r['radius_squared'])
            if 0<r['t']<1: self.assertGreater(r['gap'],0)
            else: self.assertEqual(r['gap'],0)
        self.assertEqual(n,900)
    def test_small_gap_exact(self):
        r=self.good(Q(1,10**30));self.assertGreater(r['gap'],0);self.assertTrue(verify_certificate(r))

if __name__=='__main__': unittest.main(verbosity=2)
