import unittest
from model import Model, models, examples

class TeachingTests(unittest.TestCase):
    def setUp(self): self.e=examples()
    def test_witness_transfer(self):
        m=self.e['witness_transfer_success']
        self.assertTrue(m.holds('D','a','B','C'))
        self.assertTrue(m.holds('C','i','A','C'))
        self.assertTrue(m.holds('C','i','A','B'))
    def test_affirmative_failure(self):
        m=self.e['affirmative_actual_subject_failure']
        self.assertTrue(m.holds('D','a','A','C') and m.holds('C','a','B','C'))
        self.assertFalse(m.holds('P','i','A','B'))
        self.assertFalse(m.holds('C','i','A','B'))
    def test_negative_failure(self):
        m=self.e['negative_background_failure']
        self.assertTrue(m.holds('D','e','A','C') and m.holds('C','a','B','C'))
        self.assertFalse(m.holds('P','o','A','B'))
    def test_weak_not_strong(self):
        m=self.e['weak_not_strong']
        self.assertTrue(m.holds('P','o','A','C'))
        self.assertFalse(m.holds('C','o','A','C'))
    def test_distinct_witnesses(self):
        m=self.e['different_particular_witnesses']
        self.assertTrue(m.holds('D','i','A','C') and m.holds('C','i','B','C'))
        self.assertFalse(m.holds('C','i','A','B'))
        self.assertEqual(m.extension('A') & m.extension('C'),1)
        self.assertEqual(m.varying('B') & m.extension('C'),2)
    def test_contingent_not_actual(self):
        m=self.e['contingent_conclusion_not_actual']
        self.assertTrue(m.holds('C','i','A','B'))
        self.assertFalse(m.holds('D','i','A','B'))
    def test_empty_universal_not_existential(self):
        m=self.e['empty_middle']
        self.assertTrue(m.holds('C','a','A','C'))
        self.assertFalse(m.holds('C','i','A','C'))
    def test_box_not_n(self):
        m=self.e['worldwise_not_anchored_necessity']
        self.assertTrue(m.holds('BOX','a','A','B'))
        self.assertFalse(m.holds('N','a','A','B'))
    def test_c_sign_symmetry(self):
        for m in self.e.values():
            self.assertEqual(m.holds('C','a','A','B'),m.holds('C','e','A','B'))
            self.assertEqual(m.holds('C','i','A','B'),m.holds('C','o','A','B'))
    def test_weak_necessary_dual(self):
        for m in self.e.values():
            self.assertEqual(m.holds('P','o','A','B'),not m.holds('N','a','A','B'))
    def test_nonempty_counterexamples(self):
        for name in ('affirmative_actual_subject_failure','negative_background_failure','different_particular_witnesses'):
            self.assertTrue(all(self.e[name].extension(t) for t in 'ABC'))
    def test_bad_models(self):
        for args in [(True,((1,1,1),)),(0,((0,0,0),)),(1,()),(1,[(0,0,0)]),(1,((2,0,0),)),(1,((True,0,0),)),(1,((0,0),))]:
            with self.assertRaises(ValueError): Model(*args)
    def test_bad_queries(self):
        m=self.e['weak_not_strong']
        for args in [('Q','a','A','B'),('D','u','A','B'),('D','a','Z','B'),('D','a','A',None)]:
            with self.assertRaises(ValueError): m.holds(*args)
        for w in (-1,2,True):
            with self.assertRaises(ValueError): m.extension('A',w)
    def test_generation(self): self.assertEqual(len(list(models(1,1))),8)
    def test_bad_dimensions(self):
        for args in [(0,1),(1,0),(True,1),(1,1.5)]:
            with self.assertRaises(ValueError): next(models(*args))
    def test_serialization(self):
        self.assertEqual(self.e['affirmative_actual_subject_failure'].as_dict()['worlds'][0],{'A':[0],'B':[1],'C':[0]})

if __name__=='__main__': unittest.main(verbosity=2)
