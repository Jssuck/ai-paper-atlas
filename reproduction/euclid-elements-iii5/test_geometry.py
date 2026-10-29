import copy
from fractions import Fraction
import unittest
import geometry as g

class GeometryTests(unittest.TestCase):
    def test_crossing_upper(self):
        c=g.certificate(*g.EXAMPLES['crossing_upper']);self.assertEqual(c['center_distance_squared'],'36');self.assertFalse(c['same_center']);self.assertTrue(g.verify(c))
    def test_crossing_lower(self):
        self.assertEqual(g.certificate(*g.EXAMPLES['crossing_lower'])['classification'],'distinct-common-point')
    def test_external_tangent(self):
        c=g.certificate(*g.EXAMPLES['external_tangent']);self.assertEqual(c['linear_lhs'],'4');self.assertEqual(c['linear_rhs'],'4')
    def test_internal_tangent(self):
        c=g.certificate(*g.EXAMPLES['internal_tangent']);self.assertEqual(c['linear_rhs'],'30');self.assertFalse(c['same_radius_squared'])
    def test_coincident(self):
        c=g.certificate(*g.EXAMPLES['coincident']);self.assertEqual(c['classification'],'coincident');self.assertFalse(c['distinct_circles'])
    def test_concentric_disjoint(self):
        self.assertEqual(g.circle_relation((0,0),25,(0,0),9),'concentric-disjoint')
    def test_relation_coincident(self):
        self.assertEqual(g.circle_relation((1,2),3,(1,2),3),'coincident')
    def test_nonconcentric_not_sufficient(self):
        self.assertEqual(g.circle_relation((0,0),1,(5,0),1),'different-centers-unresolved')
    def test_no_common_point(self):
        with self.assertRaises(ValueError):g.certificate((0,0),25,(0,0),9,(3,4))
    def test_point_on_first_only(self):
        with self.assertRaises(ValueError):g.certificate((0,0),1,(5,0),1,(1,0))
    def test_point_on_second_only(self):
        with self.assertRaises(ValueError):g.certificate((0,0),1,(5,0),1,(4,0))
    def test_positive_radius(self):
        for r in (0,-1,'-1/2'):
            with self.assertRaises(ValueError):g.circle((0,0),r)
    def test_exact_types(self):
        for x in (True,False,1.0,None,[],{},complex(1,0)):
            with self.assertRaises(ValueError):g.rational(x)
    def test_canonical_strings(self):
        for x in ('01','+1','1/1','2/4','-0',' 1','1.0','1/0'):
            with self.assertRaises(ValueError):g.rational(x)
        self.assertEqual(g.rational('-2/3'),Fraction(-2,3))
    def test_point_shape(self):
        for p in (None,{},'00',[],[1],[1,2,3],(True,0)):
            with self.assertRaises(ValueError):g.point(p)
    def test_rational_radius_squared(self):
        c=g.certificate((0,0),'1/2',(0,0),'1/2',('1/2','1/2'));self.assertTrue(g.verify(c))
    def test_tampered_scalar(self):
        c=g.certificate(*g.EXAMPLES['crossing_upper']);c['linear_rhs']='1';self.assertFalse(g.verify(c))
    def test_bool_confusion(self):
        for key in ('same_center','same_radius_squared','distinct_circles'):
            c=g.certificate(*g.EXAMPLES['crossing_upper']);c[key]=int(c[key]);self.assertFalse(g.verify(c))
    def test_extra_missing(self):
        c=g.certificate(*g.EXAMPLES['crossing_upper']);c['extra']=0;self.assertFalse(g.verify(c));del c['extra'];del c['scope'];self.assertFalse(g.verify(c))
    def test_malformed(self):
        for c in (None,True,[],{}, {'input':[]},{'input':{}},{'input':{'O1':None}}):self.assertFalse(g.verify(c))
    def test_input_tampering(self):
        c=g.certificate(*g.EXAMPLES['crossing_upper']);c['input']['P']=['0','5'];self.assertFalse(g.verify(c))
    def test_grid(self):
        rows=list(g.grid());self.assertEqual(len(rows),600)
        for args in rows:
            c=g.certificate(*args);self.assertTrue(g.verify(c));self.assertEqual(c['linear_lhs'],c['linear_rhs']);self.assertEqual(c['same_center'],c['classification']=='coincident')
    def test_swap_symmetry(self):
        for args in g.EXAMPLES.values():
            o1,r1,o2,r2,p=args;a=g.certificate(*args);b=g.certificate(o2,r2,o1,r1,p)
            self.assertEqual(a['classification'],b['classification']);self.assertEqual(Fraction(a['linear_lhs']),-Fraction(b['linear_lhs']))
    def test_transform_controls(self):
        for s in (0,True,1.0):
            with self.assertRaises(ValueError):g.transformed(g.EXAMPLES['coincident'],s)
        self.assertEqual(g.transformed(g.EXAMPLES['coincident'],-1)[-1],(-3,-4))

if __name__=='__main__':unittest.main()
