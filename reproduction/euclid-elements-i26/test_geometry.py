import unittest
from geometry import make_certificate, verify_certificate, angle_key, triangle, rational, strict_equal, length2
from cases import example, positive_cases, negative_cases
class GeometryTests(unittest.TestCase):
    def test_included_example(self):
        c=make_certificate(example())
        self.assertEqual(c['angle_keys'][0],['3/4','0','4/3'])
        self.assertEqual(c['squared_sides_AB_BC_AC'][0],['9','16','25'])
        self.assertTrue(verify_certificate(example(),c))
    def test_opposite_example(self):
        d=example('opposite'); self.assertEqual(make_certificate(d)['given_edge_index'],0)
        self.assertTrue(verify_certificate(d,make_certificate(d)))
    def test_all_216(self):
        inputs=list(positive_cases()); self.assertEqual(len(inputs),216)
        for d in inputs:self.assertTrue(verify_certificate(d,make_certificate(d)))
    def test_four_negative_models(self):
        for d in negative_cases().values():
            with self.assertRaises(ValueError):make_certificate(d)
            self.assertFalse(verify_certificate(d,make_certificate(example())))
    def test_duplicate_vertex(self):
        d=example(); d['triangle_1'][0]=d['triangle_1'][1]
        with self.assertRaises(ValueError):make_certificate(d)
    def test_obtuse_key(self):
        self.assertLess(angle_key(triangle([['-2','1'],['0','0'],['4','0']]),1),0)
    def test_boolean_coordinate(self):
        d=example();d['triangle_1'][0][0]=False;self.assertFalse(verify_certificate(d,{}))
    def test_noncanonical_fraction(self):
        for x in ('2/2','0.0','01','nan','1/0',' 1 '):
            with self.assertRaises(ValueError):rational(x)
    def test_numeric_coordinates(self):
        for x in (0,0.0,True,None):
            with self.assertRaises(ValueError):rational(x)
    def test_extra_input_field(self):
        d=example();d['extra']=1;self.assertFalse(verify_certificate(d,{}))
    def test_missing_input_field(self):
        d=example();del d['side_case'];self.assertFalse(verify_certificate(d,{}))
    def test_bad_branch(self):
        for branch in ('SSA',1,True,None):
            d=example();d['side_case']=branch;self.assertFalse(verify_certificate(d,{}))
    def test_bad_dimensions(self):
        for points in ([],[[1]],None,'ABC',[(1,2)]*3):
            d=example();d['triangle_1']=points;self.assertFalse(verify_certificate(d,{}))
    def test_schema_bool(self):
        c=make_certificate(example());c['schema']=True;self.assertFalse(verify_certificate(example(),c))
    def test_index_bool(self):
        for branch in ('included','opposite'):
            d=example(branch);c=make_certificate(d);c['given_edge_index']=bool(c['given_edge_index'])
            self.assertFalse(verify_certificate(d,c))
    def test_tampered_length(self):
        c=make_certificate(example());c['squared_sides_AB_BC_AC'][0][0]='10';self.assertFalse(verify_certificate(example(),c))
    def test_tampered_angle(self):
        c=make_certificate(example());c['angle_keys'][0][0]='4/3';self.assertFalse(verify_certificate(example(),c))
    def test_tampered_hash(self):
        c=make_certificate(example());c['input_sha256']='0'*64;self.assertFalse(verify_certificate(example(),c))
    def test_tampered_claim(self):
        c=make_certificate(example());c['conclusion']=True;self.assertFalse(verify_certificate(example(),c))
    def test_extra_certificate_field(self):
        c=make_certificate(example());c['extra']=1;self.assertFalse(verify_certificate(example(),c))
    def test_missing_certificate_field(self):
        c=make_certificate(example());del c['angle_keys'];self.assertFalse(verify_certificate(example(),c))
    def test_other_valid_input_certificate_rejected(self):
        other=example();other['triangle_2']=[['20','3'],['20','0'],['16','0']]
        self.assertFalse(verify_certificate(example(),make_certificate(other)))
    def test_certificate_input_tamper(self):
        c=make_certificate(example());c['input']['triangle_1'][0][1]='4';self.assertFalse(verify_certificate(example(),c))
    def test_branch_binding(self):
        self.assertFalse(verify_certificate(example('opposite'),make_certificate(example())))
    def test_no_alias(self):
        d=example();c=make_certificate(d);d['triangle_1'][0][1]='4';self.assertEqual(c['input']['triangle_1'][0][1],'3')
    def test_strict_structures(self):
        for a,b in (([1],[True]),([1],(1,)),({'1':1},{1:1}),(1,1.0)):
            self.assertFalse(strict_equal(a,b))
    def test_no_floating_tolerance(self):
        d=example();d['triangle_2'][0][1]='3000000000001/1000000000000'
        with self.assertRaises(ValueError):make_certificate(d)
    def test_ssa_counterexample_is_genuine(self):
        d=negative_cases()["ssa_not_two_angles"]
        p,q=triangle(d["triangle_1"]),triangle(d["triangle_2"])
        self.assertEqual(angle_key(p,0),angle_key(q,0))
        self.assertEqual(length2(p[0],p[1]),length2(q[0],q[1]))
        self.assertEqual(length2(p[1],p[2]),length2(q[1],q[2]))
        self.assertNotEqual(length2(p[0],p[2]),length2(q[0],q[2]))
    def test_repeated_deterministic(self):
        self.assertEqual(make_certificate(example()),make_certificate(example()))
if __name__=='__main__':unittest.main()
