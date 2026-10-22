import unittest
from model import Model, models, examples

class Tests(unittest.TestCase):
    def test_bad_dimensions(self):
        for n in (0,-1,True,1.5,'1',None):
            with self.assertRaises(ValueError): Model(n,((0,0,0),))
    def test_bad_worlds(self):
        for worlds in ((), [], ((0,0),), ([0,0,0],), ((0,0,True),), ((0,0,2),), ((0,0,-1),)):
            with self.assertRaises(ValueError): Model(1,worlds)
    def test_bad_queries(self):
        m=Model(1,((0,0,0),))
        for mode,q,p,s in [('bad','a','A','B'),('C','bad','A','B'),('C','a','D','B'),('C','a','A','D'),([], 'a','A','B')]:
            with self.assertRaises(ValueError): m.holds(mode,q,p,s)
        for w in (-1,True,1):
            with self.assertRaises(ValueError): m.extension('A',w)
    def test_enumerator_dimensions(self):
        for n,w in ((True,1),(1,False),(0,1),(1,0)):
            with self.assertRaises(ValueError): list(models(n,w))
    def test_count(self): self.assertEqual(len(list(models(1,2))),64)
    def test_vacuity(self):
        m=Model(1,((0,0,0),))
        for mode in ('D','P','N','C','BOX'):
            self.assertTrue(m.holds(mode,'a','A','B'))
            self.assertTrue(m.holds(mode,'e','A','B'))
            self.assertFalse(m.holds(mode,'i','A','B'))
            self.assertFalse(m.holds(mode,'o','A','B'))
    def test_single_world(self):
        m=Model(1,((1,1,1),))
        self.assertFalse(m.holds('C','i','A','B'))
        self.assertTrue(m.holds('P','i','A','B'))
        self.assertTrue(m.holds('N','i','A','B'))
    def test_universal_failure(self):
        m=examples()['all_actual_terms_nonempty_universal_failure']
        self.assertTrue(m.holds('C','a','A','C'))
        self.assertTrue(m.holds('C','a','B','C'))
        self.assertFalse(m.holds('C','i','A','B'))
        self.assertFalse(m.holds('C','i','C','B'))
    def test_bridge(self):
        m=examples()['bridge_success']
        self.assertTrue(m.extension('B') & m.extension('C'))
        self.assertTrue(m.holds('C','i','A','B'))
    def test_separate_witnesses(self):
        m=examples()['separate_particular_witnesses']
        self.assertTrue(m.holds('C','i','A','C'))
        self.assertTrue(m.holds('C','i','B','C'))
        self.assertFalse(m.varying('A') & m.varying('B'))
        self.assertFalse(m.holds('C','i','A','B'))
    def test_necessary_backgrounds(self):
        for name,q in [('necessary_inclusion_background','a'),('necessary_exclusion_background','e')]:
            m=examples()[name]
            self.assertTrue(m.holds('C','i','A','C'))
            self.assertTrue(m.holds('C','i','B','C'))
            self.assertTrue(m.holds('N',q,'A','B'))
            self.assertFalse(m.holds('C','i','A','B'))
    def test_box_not_n(self):
        m=examples()['worldwise_inclusion_not_anchored_necessity']
        self.assertTrue(m.holds('BOX','a','A','B'))
        self.assertFalse(m.holds('N','a','A','B'))
        self.assertTrue(m.holds('C','i','A','B'))
    def test_independent_possibilities(self):
        m=examples()['no_joint_positive_world']
        self.assertTrue(m.holds('C','a','A','C'))
        self.assertTrue(m.holds('C','a','B','C'))
        self.assertFalse(any(w[0]&w[1] for w in m.worlds))
    def test_actual_bridge_not_conversion(self):
        m=examples()['actual_membership_not_modal_conversion']
        self.assertTrue(m.holds('C','i','A','B'))
        self.assertFalse(m.holds('C','i','C','B'))
    def test_immutability(self):
        from dataclasses import FrozenInstanceError
        m=Model(1,((0,0,0),))
        with self.assertRaises(FrozenInstanceError): m.n=2
    def test_quantifier_order(self):
        m=Model(2,((1,3,0),(2,3,0)))
        self.assertTrue(m.holds('P','a','A','B'))
        self.assertFalse(any(w[0]==3 for w in m.worlds))
        self.assertTrue(m.holds('BOX','i','A','B'))
        self.assertFalse(m.holds('N','i','A','B'))

if __name__=='__main__': unittest.main(verbosity=2)
