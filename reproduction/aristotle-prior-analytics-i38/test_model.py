import unittest
from model import Term, Inclusion as I, Model, chain_certificate as cert
from run_checks import check

C, B = Term('justice'), Term('good')
Q, R, U = Term('knowable','as-good'), Term('knowable','as-being'), Term('knowable')
M = Term('good','as-good')


class Tests(unittest.TestCase):
    def test_valid_shape(self):
        self.assertTrue(cert(I(C,B),I(B,Q),I(C,Q)))
    def test_target_not_relabelled(self):
        self.assertFalse(cert(I(C,B),I(B,R),I(C,Q)))
    def test_qualifier_not_stripped(self):
        self.assertFalse(cert(I(C,B),I(B,Q),I(C,U)))
    def test_qualifier_not_added(self):
        self.assertFalse(cert(I(C,B),I(B,U),I(C,Q)))
    def test_qualifier_not_moved(self):
        self.assertFalse(cert(I(C,B),I(M,Q),I(C,Q)))
    def test_direction(self):
        self.assertFalse(cert(I(C,B),I(B,Q),I(Q,C)))
    def test_shape_is_not_truth(self):
        m=Model({0},{C:{0},B:{0},Q:set()})
        self.assertTrue(cert(I(C,B),I(B,Q),I(C,Q)))
        self.assertFalse(m.holds(I(B,Q)))
    def test_rejected_shape_can_have_true_conclusion(self):
        m=Model({0},{C:{0},B:{0},Q:{0},R:{0}})
        self.assertFalse(cert(I(C,B),I(B,R),I(C,Q)))
        self.assertTrue(m.holds(I(C,Q)))
    def test_empty_domain(self):
        m=Model(set(),{C:set(),B:set(),Q:set()})
        self.assertTrue(all(m.holds(x) for x in (I(C,B),I(B,Q),I(C,Q))))
    def test_empty_subject_no_existence(self):
        m=Model({0},{C:set(),B:set()})
        self.assertTrue(m.holds(I(C,B)))
        self.assertFalse(m.extensions[C])
    def test_missing_is_not_empty(self):
        with self.assertRaises(KeyError): Model({0},{C:set()}).holds(I(C,Q))
    def test_outside_domain(self):
        with self.assertRaises(ValueError): Model({0},{C:{1}})
    def test_bad_key(self):
        with self.assertRaises(TypeError): Model({0},{'C':{0}})
    def test_bad_term(self):
        with self.assertRaises(ValueError): Term('')
        with self.assertRaises(ValueError): Term('x',' ')
        with self.assertRaises(TypeError): Term('x',1)
    def test_bad_edge(self):
        with self.assertRaises(TypeError): I('C',B)
    def test_bad_certificate(self):
        with self.assertRaises(TypeError): cert((C,B),I(B,Q),I(C,Q))
    def test_bad_holds(self):
        with self.assertRaises(TypeError): Model(set(),{}).holds((C,B))
    def test_input_set_copied(self):
        s={0}; m=Model({0},{C:s,B:s}); s.clear()
        self.assertEqual(m.extensions[C],frozenset({0}))
    def test_opaque_label_identity(self):
        self.assertNotEqual(Q,R)
        self.assertNotEqual(Q,U)
        self.assertEqual(Q,Term('knowable','as-good'))
    def test_explicit_guard_survives_optimization(self):
        with self.assertRaises(AssertionError): check(False)


if __name__=='__main__': unittest.main()
