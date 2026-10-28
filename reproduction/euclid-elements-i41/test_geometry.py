import unittest, copy
from geometry import *
from cases import *
class GeometryTests(unittest.TestCase):
    def test_original(self): self.assertTrue(verify_certificate(example(),make_certificate(example())))
    def test_batch(self):
        for p in valid_cases(): self.assertTrue(verify_certificate(p,make_certificate(p)))
    def test_invalid_direct(self):
        for _,p in invalid_cases():
            with self.assertRaises(ValueError): make_certificate(p)
    def test_end_a(self): self.assertEqual(make_certificate(example(0))['upper_position'],'E=A')
    def test_end_d(self): self.assertEqual(make_certificate(example(1))['upper_position'],'E=D')
    def test_inside(self): self.assertEqual(make_certificate(example(F(1,2)))['upper_position'],'inside AD')
    def test_outside(self): self.assertEqual(make_certificate(example(-2))['upper_position'],'outside AD')
    def test_area(self): self.assertEqual(make_certificate(example())['double_areas'],dict(ABC='12',ACD='12',EBC='12',ABCD='24'))
    def test_extra_input(self):
        p=example();p['F']=[0,0]
        with self.assertRaises(ValueError): make_certificate(p)
    def test_missing_input(self):
        p=example();del p['A']
        with self.assertRaises(ValueError): make_certificate(p)
    def test_tuple_point(self):
        p=example();p['A']=(1,3)
        with self.assertRaises(ValueError): make_certificate(p)
    def test_bad_string(self):
        for x in ['NaN','inf','1/0','+1','1.0','01']:
            p=example();p['A'][0]=x
            with self.assertRaises(ValueError): make_certificate(p)
    def test_tamper_area(self):
        c=make_certificate(example());c['double_areas']['ABCD']='25';self.assertFalse(verify_certificate(example(),c))
    def test_tamper_chain(self):
        c=make_certificate(example());c['chain'][0]='wrong';self.assertFalse(verify_certificate(example(),c))
    def test_rebind(self): self.assertFalse(verify_certificate(example(0),make_certificate(example(1))))
    def test_extra_certificate(self):
        c=make_certificate(example());c['extra']='x';self.assertFalse(verify_certificate(example(),c))
    def test_boolean_certificate(self):
        c=make_certificate(example());c['upper_parameter']=True;self.assertFalse(verify_certificate(example(),c))
    def test_number_certificate(self):
        c=make_certificate(example());c['upper_parameter']=3;self.assertFalse(verify_certificate(example(),c))
    def test_cycle(self):
        c=make_certificate(example());c['cycle']=c;self.assertFalse(verify_certificate(example(),c))
    def test_normalization(self):
        p={k:[int(F(x)) for x in v] for k,v in example().items()};self.assertEqual(make_certificate(p),make_certificate(example()))
    def test_invalid_verifier(self): self.assertFalse(verify_certificate({},{}))
    def test_schema(self):
        c=make_certificate(example());c['schema']='other';self.assertFalse(verify_certificate(example(),c))
if __name__=='__main__': unittest.main()
