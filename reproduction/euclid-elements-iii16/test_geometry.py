import unittest
from geometry import *
class GeometryTests(unittest.TestCase):
 def setUp(self):self.c=Circle((0,5),25);self.p=(0,0)
 def test_tangent(self):self.assertEqual(analyze(self.c,self.p,(1,0))['kind'],'tangent')
 def test_tangent_reverse(self):self.assertEqual(analyze(self.c,self.p,(-1,0))['kind'],'tangent')
 def test_inward(self):self.assertEqual(analyze(self.c,self.p,(3,4))['kind'],'inward')
 def test_outward(self):self.assertEqual(analyze(self.c,self.p,(3,-4))['kind'],'outward')
 def test_second(self):self.assertEqual(analyze(self.c,self.p,(3,4))['second_point'],(F(24,5),F(32,5)))
 def test_witness(self):self.assertLess(analyze(self.c,self.p,(3,4))['interior_power'],0)
 def test_second_boundary(self):self.assertEqual(power(self.c,analyze(self.c,self.p,(3,4))['second_point']),0)
 def test_diameter(self):self.assertEqual(analyze(self.c,self.p,(0,1))['second_point'],(0,10))
 def test_projection(self):self.assertEqual(analyze(self.c,self.p,(3,4))['distance2'],9)
 def test_tangent_power(self):self.assertEqual(ray_power(self.c,self.p,(2,0),3),36)
 def test_outward_power(self):self.assertGreater(ray_power(self.c,self.p,(2,-1),3),0)
 def test_zero_parameter(self):self.assertEqual(ray_power(self.c,self.p,(3,4),0),0)
 def test_after_second(self):self.assertGreater(ray_power(self.c,self.p,(3,4),2),0)
 def test_zero_direction(self):self.assertRaises(ValueError,analyze,self.c,self.p,(0,0))
 def test_bad_contact(self):self.assertRaises(ValueError,analyze,self.c,(0,1),(1,1))
 def test_zero_radius(self):self.assertRaises(ValueError,Circle,(0,0),0)
 def test_negative_radius(self):self.assertRaises(ValueError,Circle,(0,0),-1)
 def test_float(self):self.assertRaises(TypeError,Circle,(0.0,0),1)
 def test_bool(self):self.assertRaises(TypeError,Circle,(0,0),True)
 def test_bad_point(self):self.assertRaises(TypeError,analyze,self.c,(0,), (1,1))
 def test_negative_parameter(self):self.assertRaises(ValueError,ray_power,self.c,self.p,(1,1),-1)
 def test_narrow(self):self.assertLess(narrow_example(1000000)['interior_power'],0)
 def test_narrow_zero(self):self.assertRaises(ValueError,narrow_example,0)
 def test_certificate(self):self.assertTrue(verify(self.c,self.p,(1,1),analyze(self.c,self.p,(1,1))))
 def test_tamper(self):
  a=analyze(self.c,self.p,(1,1));a['distance2']=F(0);self.assertFalse(verify(self.c,self.p,(1,1),a))
 def test_bool_tamper(self):
  a=analyze(self.c,self.p,(1,0));a['k']=False;self.assertFalse(verify(self.c,self.p,(1,0),a))
 def test_missing(self):self.assertFalse(verify(self.c,self.p,(1,0),{}))
 def test_exact_grid(self):
  count=0
  for center in [(0,0),(2,-3),(F(1,3),F(2,7))]:
   for r in [F(1),F(5),F(3,2)]:
    c=Circle(center,r*r)
    for v in [(1,0),(0,1),(F(3,5),F(4,5)),(F(-4,5),F(3,5))]:
     p=add(center,scale(v,r))
     for x in range(-3,4):
      for y in range(-3,4):
       if x==y==0:continue
       u=(x,y);a=analyze(c,p,u);count+=1
       self.assertTrue(verify(c,p,u,a));self.assertEqual(dot(sub(c.center,a['foot']),u),0)
       self.assertEqual(a['distance2'],c.radius2-a['k']**2/a['q'])
       for t in [F(0),F(1,10),F(1),F(10)]:self.assertEqual(ray_power(c,p,u,t),t*(t*a['q']-2*a['k']))
       if a['kind']=='inward':
        self.assertGreater(a['second_parameter'],0);self.assertLess(a['interior_power'],0);self.assertEqual(power(c,a['second_point']),0)
       elif a['kind']=='tangent':self.assertEqual(a['distance2'],c.radius2)
       else:self.assertLess(a['second_parameter'],0)
  self.assertEqual(count,1728);print('grid: 1728 point-direction configurations; 6912 ray-power checks')
if __name__=='__main__':unittest.main()
