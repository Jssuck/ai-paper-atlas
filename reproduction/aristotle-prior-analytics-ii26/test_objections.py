"""Tests use unittest checks that remain active under -O and -OO."""
import unittest
from objections import certificate, enumerate_models, propositions

class ObjectionTests(unittest.TestCase):
    def test_upper_negative(self):
        self.assertTrue(certificate(2,0,1,3,'upper_negative')['rejects_target'])
    def test_lower_negative(self):
        self.assertTrue(certificate(2,2,3,1,'lower_negative')['rejects_target'])
    def test_upper_positive(self):
        self.assertTrue(certificate(2,3,1,3,'upper_positive')['rejects_target'])
    def test_lower_positive(self):
        self.assertTrue(certificate(2,1,3,1,'lower_positive')['rejects_target'])
    def test_empty_subject_universals_cotrue(self):
        self.assertEqual(propositions(1,1,0),{'A':True,'E':True,'I':False,'O':False})
    def test_empty_upper_negative_not_refutation(self):
        q=certificate(1,0,0,1,'upper_negative')
        self.assertTrue(q['accepted']);self.assertTrue(q['conclusion_true'])
        self.assertFalse(q['rejects_target'])
    def test_empty_upper_positive_not_refutation(self):
        self.assertFalse(certificate(1,1,0,1,'upper_positive')['rejects_target'])
    def test_empty_lower_rejected(self):
        for r in ('lower_negative','lower_positive'):
            self.assertFalse(certificate(1,0,1,0,r)['accepted'])
    def test_local_negative_not_universal(self):
        q=certificate(2,2,3,1,'lower_negative')
        self.assertTrue(q['accepted']);self.assertFalse(propositions(2,2,3)['E'])
    def test_local_positive_not_universal(self):
        q=certificate(2,1,3,1,'lower_positive')
        self.assertTrue(q['accepted']);self.assertFalse(propositions(2,1,3)['A'])
    def test_wrong_upper_inclusion(self):
        self.assertFalse(certificate(2,2,3,1,'upper_negative')['accepted'])
    def test_false_premise_despite_true_conclusion(self):
        q=certificate(2,0,1,2,'upper_negative')
        self.assertTrue(q['conclusion_true']);self.assertFalse(q['accepted'])
    def test_second_figure_negative(self):
        self.assertTrue(certificate(2,1,2,1,'second_negative')['rejects_target'])
    def test_first_figure_particular(self):
        self.assertTrue(certificate(2,1,3,1,'first_particular')['rejects_target'])
    def test_invalid_inputs(self):
        for n,a,b,c in [(-1,0,0,0),(9,0,0,0),(1,2,0,0),(1,-1,0,0),(True,0,0,0),(1,True,0,0)]:
            with self.assertRaises(ValueError):certificate(n,a,b,c,'upper_positive')
        with self.assertRaises(ValueError):certificate(1,0,0,0,'missing')
    def test_all_finite_models(self):
        r=enumerate_models(4)
        self.assertEqual(r['worlds'],4681)
        self.assertEqual(r['square_contradiction_failures'],0)
        for route,v in r['routes'].items():
            self.assertEqual(v['conclusion_failures'],0,route)
            self.assertGreater(v['genuine_rejections'],0,route)
            self.assertEqual(v['premises_hold'],v['genuine_rejections']+v['empty_subject_nonrejections'])

if __name__ == '__main__':unittest.main(verbosity=2)
