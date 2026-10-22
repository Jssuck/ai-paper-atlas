import unittest
from model import KnowledgeBase, Inclusion, Exclusion, model_holds

class Tests(unittest.TestCase):
    def setUp(self):
        self.k = KnowledgeBase(('human','animal','stone','student'),
                               (('human','animal'),('student','human')),
                               (('animal','stone'),))
    def test_01_direct(self):
        self.assertEqual(self.k.inclusion('human','animal'), Inclusion(('human','animal')))
    def test_02_transitive(self):
        p=self.k.inclusion('student','animal')
        self.assertEqual(p.path, ('student','human','animal'))
        self.assertTrue(self.k.verify('student','animal',p))
    def test_03_reflexive(self):
        self.assertTrue(self.k.verify('human','human',self.k.inclusion('human','human')))
    def test_04_no_reverse(self):
        self.assertIsNone(self.k.inclusion('animal','human'))
    def test_05_no_missing_negative(self):
        self.assertIsNone(self.k.exclusion('animal','human'))
    def test_06_negative_symmetry(self):
        p=self.k.exclusion('stone','animal'); self.assertTrue(self.k.verify('stone','animal',p))
    def test_07_subclass_negative(self):
        p=self.k.exclusion('student','stone'); self.assertTrue(self.k.verify('student','stone',p))
    def test_08_both_subclasses(self):
        k=KnowledgeBase(('a','b','c','d'),(('a','b'),('c','d')),(('b','d'),))
        self.assertTrue(k.verify('a','c',k.exclusion('a','c')))
    def test_09_catalog_direction(self):
        c=self.k.catalog('human')
        self.assertEqual(set(c['sup']),{'human','animal'})
        self.assertEqual(set(c['sub']),{'human','student'})
        self.assertEqual(c['excl'],('stone',))
    def test_10_common_sup_not_include(self):
        k=KnowledgeBase(('x','y','top'),(('x','top'),('y','top')))
        self.assertIsNone(k.inclusion('x','y'))
    def test_11_cycles_terminate(self):
        k=KnowledgeBase(('a','b','c'),(('a','b'),('b','a')))
        self.assertIsNone(k.inclusion('a','c'))
    def test_12_empty_term_not_explosion(self):
        k=KnowledgeBase(('a','b'),(),(('a','a'),))
        self.assertIsNone(k.inclusion('a','b'))
        self.assertTrue(model_holds(k,{'a':set(),'b':{1}}))
    def test_13_forged_path_rejected(self):
        self.assertFalse(self.k.verify('student','animal',Inclusion(('student','animal'))))
    def test_14_wrong_endpoint_rejected(self):
        self.assertFalse(self.k.verify('human','stone',Inclusion(('human','animal'))))
    def test_15_forged_exclusion_rejected(self):
        self.assertFalse(self.k.verify('human','stone',Exclusion(('human',),('stone',),('human','stone'))))
    def test_16_invalid_constructor(self):
        for args in [((),), (('x','x'),), ('x',), ((' x',),), ((True,),), (('x',),[('x','z')]), (('x',),[('x',)]), (('x',),{'x':'x'})]:
            with self.subTest(args=args), self.assertRaises(ValueError): KnowledgeBase(*args)
    def test_17_invalid_queries(self):
        for x in ('missing','',True,[],None):
            with self.subTest(x=x), self.assertRaises(ValueError): self.k.catalog(x)
    def test_18_malformed_certificates(self):
        for p in (None, [], Inclusion([]), Inclusion(([],)), Exclusion((),(),()),Exclusion(('human',),('stone',),([],[]))):
            with self.subTest(p=p): self.assertFalse(self.k.verify('human','stone',p))
    def test_19_interpretation(self):
        e={'student':{1},'human':{1,2},'animal':{1,2,3},'stone':{4}}
        self.assertTrue(model_holds(self.k,e))
        e['stone'].add(1);self.assertFalse(model_holds(self.k,e))
        with self.assertRaises(ValueError):model_holds(self.k,{'human':set()})
    def test_20_determinism_and_dedup(self):
        k=KnowledgeBase(('a','b','c'),(('a','b'),('a','b'),('b','c')))
        self.assertEqual(len(k.inclusions),2)
        self.assertEqual(k.inclusion('a','c'),k.inclusion('a','c'))

if __name__=='__main__':unittest.main(verbosity=2)
