import unittest
from model import Premise as P, find_path, verify_path, interpretation_holds, sample_support

N = ('S', 'M', 'P')
E = (P('a','S','M','verified','definition A'), P('b','M','P','verified','survey B'))

class Tests(unittest.TestCase):
    def test_path(self): self.assertEqual(find_path(N,E,'S','P'), ('a','b'))
    def test_certificate(self): self.assertTrue(verify_path(N,E,'S','P',('a','b')))
    def test_direction(self): self.assertIsNone(find_path(N,E,'P','S'))
    def test_wrong_order(self): self.assertFalse(verify_path(N,E,'S','P',('b','a')))
    def test_unknown_edge(self): self.assertFalse(verify_path(N,E,'S','P',('missing',)))
    def test_reflexive(self): self.assertEqual(find_path(N,(),'S','S'),())
    def test_empty_wrong_endpoint(self): self.assertFalse(verify_path(N,E,'S','P',()))
    def test_missing_unknown(self): self.assertIsNone(find_path(N,E[:1],'S','P'))
    def test_mode_isolation(self): self.assertIsNone(find_path(N,E,'S','P','dialectic'))
    def test_endoxon_mode(self):
        e=tuple(P(p.id,p.subject,p.predicate,'endoxon',p.source) for p in E)
        self.assertEqual(find_path(N,e,'S','P','dialectic'),('a','b'))
        self.assertFalse(verify_path(N,e,'S','P',('a','b'),'truth'))
    def test_shortest(self):
        e=E+(P('c','S','P','verified','direct'),)
        self.assertEqual(find_path(N,e,'S','P'),('c',))
    def test_cycle(self):
        e=E+(P('c','M','S','verified','cycle'),)
        self.assertEqual(find_path(N,e,'S','P'),('a','b'))
    def test_truth_not_label(self):
        self.assertFalse(interpretation_holds(N,E,{'S':{1},'M':{2},'P':{2}},{1,2}))
        self.assertTrue(verify_path(N,E,'S','P',('a','b')))
    def test_sound_instance(self):
        self.assertTrue(interpretation_holds(N,E,{'S':{1},'M':{1,2},'P':{1,2}},{1,2}))
    def test_empty_term(self):
        self.assertTrue(interpretation_holds(N,E,dict.fromkeys(N,frozenset()),{1}))
    def test_sample_gap(self):
        self.assertEqual(sample_support({1,2,3},{1,2},{1,2},{1,2,3}),'sample_support')
        self.assertFalse({1,2,3}<={1,2})
    def test_sample_counterexample(self):
        self.assertEqual(sample_support({1,2,3},{1,2},{3},{1,2,3}),'sample_counterexample')
    def test_no_subject_sample(self):
        self.assertEqual(sample_support({1},{1},{2},{1,2}),'no_subject_observations')
    def test_rename(self):
        names={'S':'L','M':'Q','P':'R'}
        e=tuple(P(p.id,names[p.subject],names[p.predicate],p.basis,p.source) for p in E)
        self.assertEqual(find_path(tuple(names.values()),e,'L','R'),('a','b'))
    def test_invalid(self):
        cases=[((),E,'S','P','truth'),(N,E,'X','P','truth'),(N,E,'S','P','bad'),
               (('S','S','P'),E,'S','P','truth'),(N,E+(E[0],),'S','P','truth'),
               (N,(P('x','S','X','verified','source'),),'S','P','truth'),
               (N,(P('x','S','P','bad','source'),),'S','P','truth'),
               (N,(P('x','S','P','verified',''),),'S','P','truth'),
               (N,{},'S','P','truth'),((' S','M','P'),E,'S','P','truth')]
        for args in cases:
            with self.subTest(args=args):
                with self.assertRaises(ValueError):find_path(*args)
    def test_invalid_certificate(self):
        for c in (None, 'ab', (1,), ('',)):
            with self.assertRaises(ValueError):verify_path(N,E,'S','P',c)
    def test_invalid_interpretation(self):
        with self.assertRaises(ValueError):interpretation_holds(N,E,{'S':{1}}, {1})
        with self.assertRaises(ValueError):interpretation_holds(N,E,dict.fromkeys(N,{2}),{1})
    def test_invalid_sample(self):
        with self.assertRaises(ValueError):sample_support({1},{1},{2},{1})

if __name__=='__main__': unittest.main()
