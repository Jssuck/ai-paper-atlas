import unittest
import model as m

class TestModel(unittest.TestCase):
    def test_population(self): self.assertEqual((len(m.models()),len(m.models(True))),(255,218))
    def test_canonical_counts(self): self.assertEqual(m.canonical_counts(),{'A':1,'E':3,'I':4,'O':6})
    def test_canonical_valid(self):
        for f,mode in m.CANONICAL:self.assertEqual(m.countermodels(f,mode,True),())
    def test_classification(self):self.assertEqual((len(m.classifications()),len(m.classifications(True))),(12,18))
    def test_extra_weakening(self):
        self.assertEqual(set(m.classifications(True))-set(m.CANONICAL),{(1,'AAI'),(1,'EAO'),(2,'EAO'),(2,'AEO')})
    def test_existential_import(self):
        self.assertTrue(m.countermodels(3,'AAI')); self.assertTrue(m.countermodels(3,'EAO'))
    def test_contradictions(self):
        for model in m.models():
            for k in m.KINDS:self.assertNotEqual(m.truth(k,'S','P',model),m.truth(m.CONTRADICTORY[k],'S','P',model))
    def test_subalternation(self):
        for model in m.models():
            if m.term_nonempty('S',model):
                for a,b in [('A','I'),('E','O')]:self.assertFalse(m.truth(a,'S','P',model) and not m.truth(b,'S','P',model))
    def test_empty_subject(self):
        self.assertTrue(m.truth('A','S','P',1));self.assertTrue(m.truth('E','S','P',1));self.assertFalse(m.truth('I','S','P',1));self.assertFalse(m.truth('O','S','P',1))
    def test_refutation_strong(self):
        for model in m.models():
            if m.term_nonempty('S',model):
                self.assertFalse(m.truth('A','S','P',model) and m.truth('E','S','P',model))
    def test_reverse_subaltern_fails(self):
        model=(1<<1)|(1<<3)
        self.assertTrue(m.truth('I','S','P',model));self.assertFalse(m.truth('A','S','P',model))
    def test_search_cost(self):
        self.assertEqual(m.search('A',((1,'AAA'),))['inspections'],1)
        self.assertEqual(m.search('O',((3,'EIO'),))['inspections'],6)
        self.assertIsNone(m.search('A',((1,'EIO'),))['found'])
        self.assertEqual(m.search('O',((1,'EIO'),))['inspections'],1)
    def test_bad_models(self):
        for bad in [True,False,0,256,-1,1.0,'1',None]:
            with self.assertRaises(ValueError):m.truth('A','S','P',bad)
    def test_bad_kind_term(self):
        for bad in [None,[],{},1,'a','AA']:
            with self.assertRaises(ValueError):m.truth(bad,'S','P',1)
            with self.assertRaises(ValueError):m.truth('A',bad,'P',1)
    def test_bad_routes(self):
        for f,mode in [(True,'AAA'),(0,'AAA'),(4,'AAA'),(1,'aaa'),(1,'AA'),(1,None)]:
            with self.assertRaises(ValueError):m.premises(f,mode)
    def test_bad_policy(self):
        for bad in [None,0,1,'yes']:
            with self.assertRaises(ValueError):m.models(bad)
    def test_bad_search(self):
        for bad in [[],((4,'AAA'),),((1,'AAI'),),((1,'AAA'),(1,'AAA')),('AAA',)]:
            with self.assertRaises(ValueError):m.search('A',bad)
    def test_all_figures_distinct(self):
        self.assertEqual(m.premises(1,'AAA'),(('A','M','P'),('A','S','M')))
        self.assertEqual(m.premises(2,'AAA'),(('A','P','M'),('A','S','M')))
        self.assertEqual(m.premises(3,'AAA'),(('A','M','P'),('A','M','S')))

if __name__=='__main__': unittest.main()
