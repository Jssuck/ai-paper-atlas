import unittest
from model import Model, models, examples

class ModelTests(unittest.TestCase):
    def setUp(self): self.e=examples()
    def test_safe_witness(self):
        m=self.e['safe_contingent_not_actual']
        for q in [('C','a','A','C'),('N','a','B','C'),('C','i','A','B')]: self.assertTrue(m.holds(*q))
        for q in [('D','i','A','B'),('N','i','A','B'),('N','o','A','B')]: self.assertFalse(m.holds(*q))
    def test_missing_actual_positive(self):
        m=self.e['necessary_major_missing_actual_witness']
        self.assertTrue(m.holds('N','a','A','C'));self.assertTrue(m.holds('C','a','B','C'))
        self.assertFalse(m.holds('P','i','A','B'))
    def test_missing_actual_negative(self):
        m=self.e['necessary_negative_missing_actual_witness']
        self.assertTrue(m.holds('N','e','A','C'));self.assertTrue(m.holds('C','a','B','C'))
        self.assertFalse(m.holds('D','o','A','B'));self.assertFalse(m.holds('P','o','A','B'))
    def test_box_actual_not_necessary(self):
        m=self.e['box_negative_actual_not_necessary']
        for q in [('BOX','e','A','C'),('C','a','B','C'),('D','o','A','B'),('P','o','A','B')]: self.assertTrue(m.holds(*q))
        for q in [('N','e','A','C'),('N','o','A','B')]: self.assertFalse(m.holds(*q))
    def test_sleeping_horse(self):
        m=self.e['sleeping_horse']
        for q in [('C','a','A','C'),('N','e','B','C'),('N','a','A','B')]: self.assertTrue(m.holds(*q))
        self.assertFalse(m.holds('P','o','A','B'))
    def test_waking_horse(self):
        m=self.e['waking_horse']
        for q in [('C','a','A','C'),('N','e','B','C'),('N','e','A','B')]: self.assertTrue(m.holds(*q))
        self.assertFalse(m.holds('P','i','A','B'))
    def test_all_terms_nonempty(self):
        for key,m in self.e.items():
            if key=='empty_middle': continue
            for w in m.worlds:
                for term in w: self.assertNotEqual(term,0,key)
    def test_distinct_particulars(self):
        m=self.e['different_particular_witnesses']
        self.assertTrue(m.holds('N','i','B','C'));self.assertTrue(m.holds('C','i','A','C'))
        self.assertFalse(m.holds('C','i','A','B'))
    def test_weak_not_strong(self):
        m=self.e['weak_not_strong'];self.assertTrue(m.holds('P','o','A','C'));self.assertFalse(m.holds('C','o','A','C'))
    def test_empty_middle(self):
        m=self.e['empty_middle'];self.assertTrue(m.holds('C','a','A','C'));self.assertTrue(m.holds('N','a','B','C'));self.assertFalse(m.holds('C','i','A','C'));self.assertFalse(m.holds('C','i','A','B'))
    def test_anchored_not_convertible(self):
        m=self.e['anchored_negative_not_convertible'];self.assertTrue(m.holds('N','e','A','C'));self.assertFalse(m.holds('N','e','C','A'))
    def test_intersection_positive(self):
        m=self.e['necessary_positive_intersection'];self.assertTrue(m.holds('N','a','A','C'));self.assertNotEqual(m.extension('B')&m.extension('C'),0);self.assertTrue(m.holds('N','i','A','B'))
    def test_intersection_negative(self):
        m=self.e['necessary_negative_intersection'];self.assertTrue(m.holds('N','e','A','C'));self.assertNotEqual(m.extension('B')&m.extension('C'),0);self.assertTrue(m.holds('N','o','A','B'))
    def test_contingent_dualities(self):
        for m in self.e.values():
            self.assertEqual(m.holds('C','a','A','C'),m.holds('C','e','A','C'));self.assertEqual(m.holds('C','i','A','C'),m.holds('C','o','A','C'))
    def test_invalid_models(self):
        for n,w in [(True,((0,0,0),)),(0,((0,0,0),)),(1,()),(1,[(0,0,0)]),(1,((True,0,0),)),(1,((2,0,0),)),(1,((0,0),))]:
            with self.assertRaises(ValueError): Model(n,w)
    def test_invalid_queries(self):
        m=self.e['safe_contingent_not_actual']
        for q in [('bad','a','A','C'),('D','bad','A','C'),('D','a','Z','C'),('D','a','A','Z')]:
            with self.assertRaises(ValueError):m.holds(*q)
        for w in [-1,2,True]:
            with self.assertRaises(ValueError):m.extension('A',w)
    def test_dimensions(self):
        self.assertEqual(len(list(models(1,1))),8)
        for n,w in [(0,1),(1,0),(True,1),(1,False)]:
            with self.assertRaises(ValueError):next(models(n,w))
    def test_representation(self):
        m=self.e['box_negative_actual_not_necessary'];self.assertEqual(m.as_dict()['worlds'][1],{'A':[0,1],'B':[1],'C':[2]})

if __name__=='__main__':unittest.main()
