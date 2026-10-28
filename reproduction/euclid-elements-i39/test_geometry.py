import unittest,copy,json
from fractions import Fraction as Q
from geometry import *
from cases import *

class GeometryTests(unittest.TestCase):
    def test_finite_positives(self):
        count=0
        for data in positives():
            c=make_certificate(data);self.assertTrue(verify_certificate(data,c));t=c['trace']
            self.assertEqual(t['cross']['BC_AD'],'0');self.assertEqual(t['E'],t['input']['D'])
            self.assertEqual(t['area']['ABC'],t['area']['DBC']);count+=1
        self.assertEqual(count,180)
    def test_inner(self):self.branch(4,'inner')
    def test_outer(self):self.branch(1,'outer')
    def branch(self,k,name):
        for m in MATRICES:
            for h in [2,-2]:
                data=build(h=h,k=k if h>0 else -k,matrix=m);t=construction_trace(data)
                self.assertEqual(t['branch'],name);a={n:Q(v) for n,v in t['area'].items()}
                self.assertEqual(a['ABC'],a['EBC']);self.assertEqual(a[t['whole']],a[t['part']]+a['EDC'])
                self.assertGreater(a['EDC'],0);self.assertEqual(t['cross']['BC_AE'],'0')
                with self.assertRaises(ValueError):make_certificate(data)
    def test_invalid_geometry_direct(self):
        for label,data in negatives():
            with self.subTest(label=label),self.assertRaises(ValueError):make_certificate(data)
    def test_zero_auxiliary_segment(self):
        # A=E does not define line AE. Its supporting line is A+lambda(C-B).
        t=construction_trace(build(a=1,d=2,h=2,k=4))
        self.assertEqual(t['E'],t['input']['A']);self.assertEqual(t['branch'],'inner')
    def test_same_area_other_side_counterexample(self):
        p=parse(build(k=-2));self.assertEqual(area(p['A'],p['B'],p['C']),area(p['D'],p['B'],p['C']))
        self.assertNotEqual(cross(sub(p['C'],p['B']),sub(p['D'],p['A'])),0)
    def test_scalar_invalid(self):
        for v in [True,False,1.0,None,{},[],float('nan'),float('inf'),'2/4','01','1.0','1/0']:
            with self.subTest(value=repr(v)),self.assertRaises(ValueError):scalar(v)
    def test_input_shape(self):
        for data in [None,[],{},dict(EXAMPLE,Z=[0,0]),dict(EXAMPLE,A=(1,2)),dict(EXAMPLE,A=[1]),dict(EXAMPLE,A=[1,2,3])]:
            with self.assertRaises(ValueError):make_certificate(data)
    def test_scalar_valid(self):
        for v in [0,-2,'1/2','-1/3','0','2']:self.assertEqual(scalar(v),Q(v))
    def test_full_input_binding(self):
        c=make_certificate(EXAMPLE)
        for data in [build(a=2),build(d=4),build(shift=(1,0)),build(h=-2)]:self.assertFalse(verify_certificate(data,c))
    def test_type_attacks(self):
        c=make_certificate(EXAMPLE)
        for val in [True,False,0,1,0.0,None,float('nan'),float('inf'),[],{}]:
            bad=copy.deepcopy(c);bad['trace']['cross']['BC_AD']=val
            self.assertFalse(verify_certificate(EXAMPLE,bad))
    def test_all_leaf_tampering(self):
        c=make_certificate(EXAMPLE)
        def paths(v,p=()):
            if type(v) is dict:
                for k,x in v.items():yield from paths(x,p+(k,))
            elif type(v) is list:
                for k,x in enumerate(v):yield from paths(x,p+(k,))
            else:yield p
        for path in paths(c):
            bad=copy.deepcopy(c);target=bad
            for k in path[:-1]:target=target[k]
            target[path[-1]]+='tampered'
            self.assertFalse(verify_certificate(EXAMPLE,bad))
    def test_extra_missing_fields(self):
        c=make_certificate(EXAMPLE);bad=copy.deepcopy(c);bad['extra']='x';self.assertFalse(verify_certificate(EXAMPLE,bad))
        for key in c:
            bad=copy.deepcopy(c);del bad[key];self.assertFalse(verify_certificate(EXAMPLE,bad))
    def test_json_roundtrip(self):
        c=make_certificate(EXAMPLE);self.assertTrue(verify_certificate(EXAMPLE,json.loads(json.dumps(c))))
    def test_normalized_coordinates(self):
        c=make_certificate(EXAMPLE);data={k:[int(x) for x in v] for k,v in EXAMPLE.items()}
        self.assertTrue(verify_certificate(data,c))
    def test_invalid_cert_containers(self):
        for v in [None,[],True,{},'certificate'] : self.assertFalse(verify_certificate(EXAMPLE,v))
    def test_no_assumption_from_empty_certificate(self):
        for _,data in negatives():self.assertFalse(verify_certificate(data,{}))

if __name__=='__main__':unittest.main(verbosity=2)
