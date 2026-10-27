import copy
import unittest
from geometry import make_certificate,verify_certificate,angle,rational,strict_equal
from cases import EXAMPLE,positives,negatives

class GeometryTests(unittest.TestCase):
    def test_example(self):
        c=make_certificate(EXAMPLE)
        self.assertEqual(c['positive_scale'],'3/2')
        self.assertEqual(c['angles']['AGH'],{'cos_sign':-1,'cos_squared':'1/2'})
        self.assertTrue(verify_certificate(EXAMPLE,c))
    def test_all_positive(self):
        n=0
        for x in positives():
            self.assertTrue(verify_certificate(x,make_certificate(x)));n+=1
        self.assertEqual(n,336)
    def test_all_negative_direct(self):
        for x in negatives():
            with self.assertRaises(ValueError):make_certificate(x)
    def test_rebind(self):
        c=make_certificate(EXAMPLE);x=copy.deepcopy(EXAMPLE);x['B']=['3','1']
        self.assertFalse(verify_certificate(x,c))
    def test_right_angles(self):
        c=make_certificate({'G':['0','1'],'H':['0','0'],'B':['1','1'],'D':['2','0']})
        self.assertEqual(c['angles']['BGH'],{'cos_sign':0,'cos_squared':'0'})
    def test_zero_ray_angle(self):
        with self.assertRaises(ValueError):angle((0,0),(1,1))
    def test_bool_integer_distinct(self):self.assertFalse(strict_equal(True,1))
    def test_tuple_list_distinct(self):self.assertFalse(strict_equal([1],(1,)))
    def test_float_rejected(self):self.assertFalse(strict_equal(1.0,1.0))
    def test_extra_field(self):
        c=make_certificate(EXAMPLE);c['extra']=1;self.assertFalse(verify_certificate(EXAMPLE,c))
    def test_missing_field(self):
        c=make_certificate(EXAMPLE);del c['input'];self.assertFalse(verify_certificate(EXAMPLE,c))
    def test_hash_tamper(self):
        c=make_certificate(EXAMPLE);c['input_sha256']='0'*64;self.assertFalse(verify_certificate(EXAMPLE,c))
    def test_nested_tamper(self):
        c=make_certificate(EXAMPLE);c['angles']['AGH']['cos_sign']=True;self.assertFalse(verify_certificate(EXAMPLE,c))
    def test_conclusion_integer(self):
        c=make_certificate(EXAMPLE);c['conclusions']['alternate_equal']=1;self.assertFalse(verify_certificate(EXAMPLE,c))
    def test_scale_tamper(self):
        c=make_certificate(EXAMPLE);c['positive_scale']='2';self.assertFalse(verify_certificate(EXAMPLE,c))
    def test_certificate_none(self):self.assertFalse(verify_certificate(EXAMPLE,None))
    def test_certificate_list(self):self.assertFalse(verify_certificate(EXAMPLE,[]))
    def test_bad_expected(self):self.assertFalse(verify_certificate({},make_certificate(EXAMPLE)))

for name,value in [('bool',True),('integer',1),('float',0.5),('zero_div','1/0'),('unreduced','2/4'),('leading_zero','01'),('decimal','0.5'),('space',' 1'),('empty',''),('none',None)]:
    def bad(self,value=value):
        x=copy.deepcopy(EXAMPLE);x['G'][0]=value
        with self.assertRaises(ValueError):make_certificate(x)
    setattr(GeometryTests,'test_bad_coordinate_'+name,bad)
for name,mutate in [('extra',lambda x:x.update(Z=['0','0'])),('missing',lambda x:x.pop('G')),('tuple',lambda x:x.update(G=('0','1'))),('short',lambda x:x.update(G=['0']))]:
    def bad(self,mutate=mutate):
        x=copy.deepcopy(EXAMPLE);mutate(x)
        with self.assertRaises(ValueError):make_certificate(x)
    setattr(GeometryTests,'test_bad_shape_'+name,bad)
if __name__=='__main__':unittest.main()
