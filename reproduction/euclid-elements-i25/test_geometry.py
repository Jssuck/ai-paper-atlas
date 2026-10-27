import unittest
import copy
import json
from geometry import certify, classify, verify, verify_json, rational, load_json
from cases import case, positives

class Checks(unittest.TestCase):
    def test_grid(self):
        for d in positives(): self.assertTrue(verify(d,certify(d)))
    def test_example(self):
        m=certify(case())['metric']
        self.assertEqual(m['BC2'],[13,1]);self.assertEqual(m['EF2'],[7,1])
        self.assertEqual(m['angle_relation'],'greater')
    def test_equal(self):
        self.assertEqual(classify(case(d=3,e=3))['angle_relation'],'equal')
        with self.assertRaises(ValueError):certify(case(d=3,e=3))
    def test_reverse(self):
        self.assertEqual(classify(case(d=3,e=0))['angle_relation'],'less')
        with self.assertRaises(ValueError):certify(case(d=3,e=0))
    def test_schema(self):
        c=certify(case());c['schema_version']=True;self.assertFalse(verify(case(),c))
    def test_bool_dot(self):
        c=case();c['ABC']['dot']=[False,1];self.assertFalse(verify(c,{}))
    def test_float(self):
        c=case();c['ABC']['a2']=[4.0,1];self.assertFalse(verify(c,{}))
    def test_noncanonical(self):
        for q in ([0,2],[2,2],[1,-1],[1,0],[True,1],[1,True],(1,1),[1],['1',1]):
            with self.assertRaises(ValueError):rational(q)
    def test_extra_input(self):
        c=case();c['extra']=1;self.assertFalse(verify(c,{}))
    def test_missing_input(self):
        c=case();del c['ABC']['dot'];self.assertFalse(verify(c,{}))
    def test_side_mismatch(self):
        c=case();c['DEF']['a2']=[5,1];self.assertFalse(verify(c,{}))
    def test_collinear(self):
        for d in (-6,6):
            with self.assertRaises(ValueError):certify(case(d=d))
    def test_impossible(self):
        with self.assertRaises(ValueError):certify(case(d=7))
    def test_zero_side(self):
        with self.assertRaises(ValueError):certify(case(a=0))
    def test_negative_side(self):
        with self.assertRaises(ValueError):certify(case(a=-1))
    def test_negative_dots(self):
        self.assertTrue(verify(case(d=-3,e=-1),certify(case(d=-3,e=-1))))
    def test_swap_flag(self):
        c=certify(case());c['branches']['less']['swap_triangles']=1;self.assertFalse(verify(case(),c))
    def test_lemma(self):
        c=certify(case());c['branches']['less']['lemma']='I.25';self.assertFalse(verify(case(),c))
    def test_certificate_number_bool(self):
        c=certify(case());c['metric']['BC2'][1]=True;self.assertFalse(verify(case(),c))
    def test_certificate_extra(self):
        c=certify(case());c['metric']['extra']=1;self.assertFalse(verify(case(),c))
    def test_certificate_missing(self):
        c=certify(case());del c['branches']['equal'];self.assertFalse(verify(case(),c))
    def test_certificate_tamper(self):
        c=certify(case());c['metric']['angle_relation']='less';self.assertFalse(verify(case(),c))
    def test_replay_wrong_input(self):
        self.assertFalse(verify(case(d=-1),certify(case())))
    def test_same_sum_different_sides(self):
        self.assertFalse(verify(case(a=5,b=8),certify(case())))
    def test_json_roundtrip(self):
        self.assertTrue(verify_json(json.dumps(case()),json.dumps(certify(case()))))
    def test_duplicate(self):
        with self.assertRaises(ValueError):load_json('{"a":1,"a":2}')
    def test_nan(self):
        for x in ('NaN','Infinity','-Infinity'):
            with self.assertRaises(ValueError):load_json(x)
    def test_bad_json(self):self.assertFalse(verify_json('{','{}'))
    def test_all_leaf_mutations(self):
        c=certify(case())
        def paths(x,p=()):
            if type(x) is dict:
                for k,v in x.items():yield from paths(v,p+(k,))
            elif type(x) is list:
                for k,v in enumerate(x):yield from paths(v,p+(k,))
            else:yield p
        for p in paths(c):
            z=copy.deepcopy(c);v=z
            for k in p[:-1]:v=v[k]
            v[p[-1]]=None
            self.assertFalse(verify(case(),z),str(p))

if __name__=='__main__':unittest.main(verbosity=2)
