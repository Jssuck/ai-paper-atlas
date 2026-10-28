import unittest,copy,json
from fractions import Fraction as Q
from geometry import *
from cases import *

class GeometryTests(unittest.TestCase):
    def test_example(self):
        c=make_certificate(EXAMPLE);self.assertTrue(verify_certificate(EXAMPLE,c));self.assertEqual(c['conclusion'],'AD parallel BC')
    def test_batch(self):
        for p in positives():self.assertTrue(verify_certificate(p,make_certificate(p)))
    def test_invalid_geometry_direct(self):
        for name,p in negatives():
            with self.subTest(name=name):
                with self.assertRaises(ValueError):make_certificate(p)
                self.assertFalse(verify_certificate(p,{}))
    def test_inner(self):
        t=construction_trace(build(k=4));self.assertEqual(t['branch'],'inner');self.assertEqual(t['t'],'1/2');self.assertEqual(t['double_area'],{'ABC':'6','DEF':'12','GEF':'6','GDF':'6'})
    def test_outer(self):
        t=construction_trace(build(k=1));self.assertEqual(t['branch'],'outer');self.assertEqual(t['t'],'2');self.assertEqual(t['double_area'],{'ABC':'6','DEF':'3','GEF':'6','GDF':'3'})
    def test_coincident(self):
        c=make_certificate(build(d=1));self.assertIn('undefined',c['conclusion']);self.assertEqual(c['trace']['apex_relation'],'coincident')
    def test_same_base(self):
        c=make_certificate(build(reverse=True));self.assertEqual(c['trace']['base_direction'],'reversed')
    def test_fraction(self):
        p=build();p['A']=['1/2','2'];self.assertTrue(verify_certificate(p,make_certificate(p)))
    def test_representations(self):
        p={k:list(map(str,v)) for k,v in EXAMPLE.items()};self.assertEqual(make_certificate(p),make_certificate(EXAMPLE))
    def test_bad_scalar(self):
        for v in [True,False,1.0,None,{},[],Q(1,2),'2/4','01','1.0','nan','1/0',' 2 ']:
            p=copy.deepcopy(EXAMPLE);p['A'][0]=v
            with self.assertRaises(ValueError):make_certificate(p)
    def test_bad_container(self):
        for p in [None,[],{},dict(EXAMPLE,Z=[1,2]),{k:tuple(v) for k,v in EXAMPLE.items()}]:
            with self.assertRaises(ValueError):make_certificate(p)
    def test_bad_point(self):
        for v in [[1],[1,2,3],'12']:
            p=copy.deepcopy(EXAMPLE);p['A']=v
            with self.assertRaises(ValueError):make_certificate(p)
    def test_field_mutation(self):
        c=make_certificate(EXAMPLE)
        for key in c['trace']:
            bad=copy.deepcopy(c);bad['trace'][key]='tampered';self.assertFalse(verify_certificate(EXAMPLE,bad))
    def test_bool_numeric_certificate(self):
        c=make_certificate(EXAMPLE)
        for v in [True,False,0,0.0,None]:
            bad=copy.deepcopy(c);bad['trace']['cross']['BC_AD']=v;self.assertFalse(verify_certificate(EXAMPLE,bad))
    def test_input_binding(self):
        self.assertFalse(verify_certificate(build(a=2),make_certificate(EXAMPLE)))
    def test_json_roundtrip(self):
        c=json.loads(json.dumps(make_certificate(EXAMPLE)));self.assertTrue(verify_certificate(EXAMPLE,c))
    def test_extra_certificate_field(self):
        c=make_certificate(EXAMPLE);c['extra']='x';self.assertFalse(verify_certificate(EXAMPLE,c))
    def test_each_input_coordinate_binding(self):
        c=make_certificate(EXAMPLE)
        for key in EXAMPLE:
            for axis in [0,1]:
                p=copy.deepcopy(EXAMPLE);p[key][axis]+=1;self.assertFalse(verify_certificate(p,c))
    def test_affine_shear(self):
        p={key:[2*x+3*y+7,3*y-4] for key,(x,y) in EXAMPLE.items()};self.assertTrue(verify_certificate(p,make_certificate(p)))
    def test_trace_invalid(self):
        for name,p in list(negatives())[:-1]:
            with self.assertRaises(ValueError):construction_trace(p)

if __name__=='__main__':unittest.main(verbosity=2)
