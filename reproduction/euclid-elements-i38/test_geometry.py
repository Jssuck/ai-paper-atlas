import copy
import unittest
from fractions import Fraction as Q
from geometry import make_certificate,verify_certificate
from cases import EXAMPLE,build,positives,negatives

class GeometryTests(unittest.TestCase):
    def test_example(self):
        c=make_certificate(EXAMPLE)
        self.assertEqual(c['area'],{'ABC':'3','DEF':'3','GBCA':'6','DEFH':'6'})
        self.assertEqual(c['vertices'],{'G':['-2','3'],'H':['6','3']})
    def test_finite_family(self):
        count=0
        for data in positives():
            c=make_certificate(data);self.assertTrue(verify_certificate(data,c))
            a=c['area'];self.assertEqual(a['ABC'],a['DEF'])
            self.assertEqual(a['GBCA'],a['DEFH']);self.assertEqual(Q(a['GBCA']),2*Q(a['ABC']))
            self.assertTrue(all(v=='0' for v in c['parallel_checks'].values()))
            self.assertEqual(len(set(c['halves'].values())),1);count+=1
        self.assertEqual(count,360)
    def test_geometry_negatives(self):
        for data in negatives():
            with self.assertRaises(ValueError):make_certificate(data)
            self.assertFalse(verify_certificate(data,{}))
    def test_same_base(self):self.assertTrue(verify_certificate(build(s=0),make_certificate(build(s=0))))
    def test_reversed_base(self):self.assertEqual(make_certificate(build(direction=-1))['base_direction'],'opposite')
    def test_same_vertex(self):self.assertEqual(make_certificate(build(a=0,d=0))['coincidences']['A_D'],'yes')
    def test_same_G_H(self):self.assertEqual(make_certificate(build(a=0,d=-2))['coincidences']['G_H'],'yes')
    def test_B_equals_F(self):self.assertEqual(build(s=-1)['B'],build(s=-1)['F'])
    def test_bool(self):self.bad_scalar(True)
    def test_float(self):self.bad_scalar(0.5)
    def test_fraction_object(self):self.bad_scalar(Q(1,2))
    def test_none(self):self.bad_scalar(None)
    def test_noncanonical_ratio(self):self.bad_scalar('2/4')
    def test_decimal_string(self):self.bad_scalar('0.5')
    def test_whitespace(self):self.bad_scalar(' 1')
    def test_denominator_zero(self):self.bad_scalar('1/0')
    def test_integer_string(self):
        d=copy.deepcopy(EXAMPLE);d['A'][0]='0';self.assertTrue(verify_certificate(d,make_certificate(d)))
    def bad_scalar(self,value):
        d=copy.deepcopy(EXAMPLE);d['A'][0]=value
        with self.assertRaises(ValueError):make_certificate(d)
    def test_missing_key(self):
        d=copy.deepcopy(EXAMPLE);del d['A']
        with self.assertRaises(ValueError):make_certificate(d)
    def test_extra_key(self):
        d=copy.deepcopy(EXAMPLE);d['Z']=[0,0]
        with self.assertRaises(ValueError):make_certificate(d)
    def test_point_tuple(self):
        d=copy.deepcopy(EXAMPLE);d['A']=(0,3)
        with self.assertRaises(ValueError):make_certificate(d)
    def test_point_length(self):
        d=copy.deepcopy(EXAMPLE);d['A']=[0,3,0]
        with self.assertRaises(ValueError):make_certificate(d)
    def test_container(self):
        with self.assertRaises(ValueError):make_certificate([])
    def test_every_leaf_tamper(self):
        c=make_certificate(EXAMPLE)
        def leaves(x,path=()):
            if isinstance(x,dict):
                for k,v in x.items():yield from leaves(v,path+(k,))
            elif isinstance(x,list):
                for k,v in enumerate(x):yield from leaves(v,path+(k,))
            else:yield path
        for path in leaves(c):
            modified=copy.deepcopy(c);node=modified
            for k in path[:-1]:node=node[k]
            node[path[-1]]='tampered';self.assertFalse(verify_certificate(EXAMPLE,modified))
    def test_bool_certificate(self):
        c=make_certificate(EXAMPLE);c['area']['ABC']=True;self.assertFalse(verify_certificate(EXAMPLE,c))
    def test_extra_certificate_field(self):
        c=make_certificate(EXAMPLE);c['extra']='0';self.assertFalse(verify_certificate(EXAMPLE,c))
    def test_missing_certificate_field(self):
        c=make_certificate(EXAMPLE);del c['input'];self.assertFalse(verify_certificate(EXAMPLE,c))
    def test_translation_binding(self):
        c=make_certificate(EXAMPLE);self.assertFalse(verify_certificate(build(origin=(10,10)),c))
    def test_vertex_slide_binding(self):
        c=make_certificate(EXAMPLE);self.assertFalse(verify_certificate(build(a=1),c))
    def test_base_slide_binding(self):
        c=make_certificate(EXAMPLE);self.assertFalse(verify_certificate(build(s=4),c))
    def test_endpoint_reversal_binding(self):
        d=copy.deepcopy(EXAMPLE);d['E'],d['F']=d['F'],d['E']
        self.assertFalse(verify_certificate(d,make_certificate(EXAMPLE)))
    def test_certificate_none(self):self.assertFalse(verify_certificate(EXAMPLE,None))
    def test_key_order_irrelevant(self):
        c=make_certificate(EXAMPLE);self.assertTrue(verify_certificate(dict(reversed(list(EXAMPLE.items()))),c))

if __name__=='__main__':unittest.main(verbosity=2)
