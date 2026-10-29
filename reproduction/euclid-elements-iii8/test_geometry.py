import unittest
from fractions import Fraction as F
from geometry import certificate, equal_shell, secant, compare, sample, verify, grid

class GeometryTests(unittest.TestCase):
    def test_nearest(self): self.assertEqual(certificate(5,13,(5,0))['squared_distance'],64)
    def test_farthest(self): self.assertEqual(certificate(5,13,(-5,0))['squared_distance'],324)
    def test_mirror(self): self.assertEqual(certificate(5,13,(3,4))['mirror'],(3,-4))
    def test_near(self): self.assertEqual(certificate(5,13,(3,4))['branch'],'near')
    def test_far(self): self.assertEqual(certificate(5,13,(-3,4))['branch'],'far')
    def test_tangent(self): self.assertEqual(certificate(3,5,(F(9,5),F(12,5)))['branch'],'tangent')
    def test_not_near_semicircle(self): self.assertEqual(certificate(5,13,(0,5))['branch'],'far')
    def test_positive_x_far(self): self.assertEqual(certificate(5,6,(3,4))['branch'],'far')
    def test_shell_two(self): self.assertEqual(equal_shell(5,13,116)['count'],2)
    def test_shell_min(self): self.assertEqual(equal_shell(5,13,64)['count'],1)
    def test_shell_max(self): self.assertEqual(equal_shell(5,13,324)['count'],1)
    def test_shell_below(self): self.assertEqual(equal_shell(5,13,63)['count'],0)
    def test_shell_above(self): self.assertEqual(equal_shell(5,13,325)['count'],0)
    def test_shell_negative(self): self.assertEqual(equal_shell(5,13,-1)['count'],0)
    def test_center_rejected(self):
        with self.assertRaises(ValueError): certificate(5,0,(3,4))
    def test_interior_rejected(self):
        with self.assertRaises(ValueError): certificate(5,2,(3,4))
    def test_boundary_rejected(self):
        with self.assertRaises(ValueError): certificate(5,5,(3,4))
    def test_radius_rejected(self):
        with self.assertRaises(ValueError): certificate(0,1,(0,0))
    def test_off_circle(self):
        with self.assertRaises(ValueError): certificate(5,13,(3,3))
    def test_float_rejected(self):
        with self.assertRaises(TypeError): certificate(5.,13,(3,4))
    def test_bool_rejected(self):
        with self.assertRaises(TypeError): certificate(True,13,(0,1))
    def test_projection(self): self.assertEqual(compare(5,13,(-3,4),(3,4)),{'delta':-156,'projection_identity':-156})
    def test_axis_secant(self): self.assertEqual(secant(5,13,(5,0))['points'],((5,0),(-5,0)))
    def test_tangent_secant(self): self.assertTrue(secant(3,5,(F(9,5),F(12,5)))['tangent'])
    def test_secant_known(self): self.assertEqual(secant(5,13,(3,4))['parameters'],(F(1),F(36,29)))
    def test_same_ray_two_distances(self):
        s=secant(5,13,(3,4));a,b=s['points'];self.assertEqual(a[1]/(13-a[0]),b[1]/(13-b[0]));self.assertLess(s['squared_lengths'][0],s['squared_lengths'][1])
    def test_tampering(self):
        c=certificate(5,13,(3,4));c['squared_distance']+=1;self.assertFalse(verify(c))
    def test_boolean_tampering(self):
        c=certificate(5,13,(3,4));c['distinct_mirror']=1;self.assertFalse(verify(c))
    def test_extra_key(self):
        c=certificate(5,13,(3,4));c['extra']=0;self.assertFalse(verify(c))
    def test_grid(self):
        count=0
        for r,d,p in grid():
            c=certificate(r,d,p);self.assertTrue(verify(c));self.assertEqual(c['identity'],c['squared_distance'])
            self.assertLessEqual(c['minimum_squared'],c['squared_distance']);self.assertLessEqual(c['squared_distance'],c['maximum_squared'])
            self.assertEqual(equal_shell(r,d,c['squared_distance'])['count'],c['equal_point_count'])
            self.assertEqual(certificate(r,d,c['mirror'])['squared_distance'],c['squared_distance'])
            s=secant(r,d,p);self.assertGreater(s['parameters'][0],0)
            for t,pt in zip(s['parameters'],s['points']):
                self.assertEqual(s['a']*t*t+s['b']*t+s['c'],0);self.assertEqual(pt[0]**2+pt[1]**2,r*r)
            self.assertEqual(s['squared_lengths'][0]*s['squared_lengths'][1],(d*d-r*r)**2)
            branches=tuple(certificate(r,d,pt)['branch'] for pt in s['points'])
            self.assertEqual(branches,('tangent','tangent') if s['tangent'] else ('near','far'))
            count+=1
        self.assertEqual(count,1071)
if __name__=='__main__': unittest.main()
