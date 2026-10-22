import unittest
from fractions import Fraction
import model as m


class ModelTests(unittest.TestCase):
    def test_domain(self):
        self.assertEqual(m.domain(1), frozenset({0}))
        self.assertEqual(len(m.domain(255)), 8)
    def test_membership(self):
        self.assertEqual(m.extension(255, 'S'), frozenset({1,3,5,7}))
        self.assertEqual(m.extension(255, 'P'), frozenset({2,3,6,7}))
        self.assertEqual(m.extension(255, 'M'), frozenset({4,5,6,7}))
    def test_empty_subject(self):
        self.assertEqual([m.proposition(1,f,'S','P') for f in m.FORMS], [True,True,False,False])
    def test_complements(self):
        for mask in range(1,256):
            for s in m.TERMS:
                for p in m.TERMS:
                    self.assertNotEqual(m.proposition(mask,'A',s,p), m.proposition(mask,'O',s,p))
                    self.assertNotEqual(m.proposition(mask,'E',s,p), m.proposition(mask,'I',s,p))
    def test_models(self):
        self.assertEqual(len(m.models()),255)
        self.assertTrue(set(m.models('all_terms_nonempty')) < set(m.models()))
        self.assertIn(128,m.models('all_terms_nonempty'))
    def test_barbara(self):
        self.assertTrue(m.classify(1,'AAA')['valid'])
    def test_two_particulars(self):
        self.assertFalse(m.classify(1,'III','all_terms_nonempty')['valid'])
    def test_two_negatives(self):
        self.assertFalse(m.classify(2,'EEE','all_terms_nonempty')['valid'])
    def test_necessary_not_sufficient(self):
        self.assertFalse(m.classify(2,'AAA','all_terms_nonempty')['valid'])
    def test_darapti(self):
        self.assertFalse(m.classify(3,'AAI')['valid'])
        self.assertTrue(m.classify(3,'AAI','all_terms_nonempty')['valid'])
        self.assertFalse(m.classify(3,'AAA','all_terms_nonempty')['valid'])
    def test_census_constraints(self):
        for policy in m.POLICIES:
            rows=m.census(policy)
            self.assertEqual(len(rows),192)
            for r in rows:
                if r['valid']:
                    x,y,z=r['mood']
                    self.assertTrue(x in 'AI' or y in 'AI')
                    self.assertTrue(x in 'AE' or y in 'AE')
                    if z in 'AE':
                        self.assertTrue(x in 'AE' and y in 'AE')
                    self.assertTrue((z in 'AI') == (x in 'AI') or (z in 'AI') == (y in 'AI'))
    def test_countermodel_replay(self):
        for p in m.POLICIES:
            for r in m.census(p):
                if not r['valid']:
                    self.assertEqual(m.evaluate(r['first_countermodel'],r['figure'],r['mood']), (True,True,False))
    def test_bad_masks(self):
        for v in (True,False,0,-1,256,1.0,'1',None,[],{}):
            with self.assertRaises(ValueError): m.domain(v)
    def test_bad_symbols(self):
        for v in ('a','X','',None,[],{}):
            with self.assertRaises(ValueError): m.proposition(1,v,'S','P')
        for v in ('s','X','',None,[],{}):
            with self.assertRaises(ValueError): m.extension(1,v)
    def test_bad_figures_moods_policies(self):
        for v in (True,0,4,1.0,'1',None,[]):
            with self.assertRaises(ValueError): m.classify(v,'AAA')
        for v in ('AA','AAAA','aaa','AAX',None,[],123):
            with self.assertRaises(ValueError): m.classify(1,v)
        for v in ('all','',None,[],True):
            with self.assertRaises(ValueError): m.models(v)
    def test_exact_remainders(self):
        r=m.equal_remainders(Fraction(9,2),Fraction(9,2),Fraction(1,3),Fraction(1,3))
        self.assertTrue(r['assumptions'] and r['conclusion'])
        self.assertEqual(r['remainders'],(Fraction(25,6),Fraction(25,6)))
    def test_false_assumptions_not_equality_proof(self):
        r=m.equal_remainders(4,5,1,1)
        self.assertFalse(r['assumptions']);self.assertFalse(r['conclusion']);self.assertTrue(r['implication'])
    def test_invalid_remainders(self):
        for values in ((True,1,0,0),(1.,1,0,0),(-1,-1,0,0),(1,1,2,2),(1,1,-1,-1)):
            with self.assertRaises(ValueError): m.equal_remainders(*values)

if __name__=='__main__': unittest.main(verbosity=2)
