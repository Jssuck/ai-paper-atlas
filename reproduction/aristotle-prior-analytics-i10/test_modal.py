import unittest
from modal import Model, ordinary, boxed, anchored, strong_e, relation, models, run

class Tests(unittest.TestCase):
    def setUp(self): self.m=Model(2,((1,2,1),(3,2,3)))
    def test_a(self): self.assertTrue(relation('A',3,1))
    def test_e(self): self.assertTrue(relation('E',1,2))
    def test_i(self): self.assertTrue(relation('I',3,2))
    def test_o(self): self.assertTrue(relation('O',1,3))
    def test_empty_a(self): self.assertTrue(relation('A',0,0))
    def test_empty_i(self): self.assertFalse(relation('I',3,0))
    def test_union(self): self.assertEqual(self.m.possible(0),3)
    def test_intersection(self): self.assertEqual(self.m.necessary(0),1)
    def test_ordinary(self): self.assertTrue(ordinary(self.m,'A',0,2))
    def test_anchor_a(self): self.assertTrue(anchored(self.m,'A',0,2))
    def test_anchor_o(self): self.assertFalse(anchored(self.m,'O',0,2))
    def test_box(self): self.assertTrue(boxed(self.m,'A',0,2))
    def test_strong_symmetry(self): self.assertEqual(strong_e(self.m,0,1),strong_e(self.m,1,0))
    def test_e_not_symmetric(self):
        m=Model(2,((1,2,0),(1,3,0)))
        self.assertTrue(anchored(m,'E',0,1));self.assertFalse(anchored(m,'E',1,0))
    def test_box_not_cross_world(self):
        m=Model(2,((1,2,0),(2,1,0)))
        self.assertTrue(boxed(m,'E',0,1));self.assertFalse(strong_e(m,0,1))
    def test_count(self): self.assertEqual(sum(1 for _ in models()),4096)
    def test_complete_run(self): self.assertEqual(run()['models'],4096)
    def test_bad_n(self):
        for n in (0,-1,9,True,2.0,'2'):
            with self.assertRaises(ValueError): Model(n,((0,0,0),))
    def test_bad_worlds(self):
        for w in ((),[],None,((0,0),),((0,0,0,0),),([0,0,0],)):
            with self.assertRaises(ValueError): Model(2,w)
    def test_bad_mask(self):
        for x in (-1,4,True,1.0,'1'):
            with self.assertRaises(ValueError): Model(2,((x,0,0),))
    def test_bad_term(self):
        for x in (-1,3,True,1.0):
            with self.assertRaises(ValueError): self.m.extent(x)
    def test_bad_world(self):
        for x in (-1,2,True,1.0):
            with self.assertRaises(ValueError): self.m.extent(0,x)
    def test_bad_kind(self):
        with self.assertRaises(ValueError): ordinary(self.m,'X',0,1)
        with self.assertRaises(ValueError): anchored(self.m,'X',0,1)
    def test_nonempty_cesare_gap(self):
        m=Model(2,((1,2,1),(1,2,3)))
        self.assertTrue(strong_e(m,0,1) and ordinary(m,'A',0,2))
        self.assertTrue(anchored(m,'E',1,2)); self.assertFalse(strong_e(m,1,2))
    def test_nonempty_camestres_gap(self):
        m=Model(2,((1,1,2),(1,3,2)))
        self.assertTrue(strong_e(m,0,2) and ordinary(m,'A',0,1))
        self.assertTrue(anchored(m,'E',2,1)); self.assertFalse(anchored(m,'E',1,2))
    def test_nonempty_affirmative_universal(self):
        m=Model(2,((1,1,2),(3,3,2)))
        self.assertTrue(anchored(m,'A',0,1) and ordinary(m,'E',0,2))
        self.assertFalse(anchored(m,'E',1,2))
    def test_nonempty_affirmative_particular(self):
        m=Model(2,((1,1,2),(3,3,2)))
        self.assertTrue(anchored(m,'A',0,1) and ordinary(m,'O',0,2))
        self.assertFalse(anchored(m,'O',1,2))
    def test_nonempty_necessary_particular_negative(self):
        m=Model(2,((1,1,2),(1,3,2)))
        self.assertTrue(ordinary(m,'A',0,1) and anchored(m,'O',0,2))
        self.assertFalse(anchored(m,'O',1,2))
    def test_nonempty_conversion(self):
        m=Model(2,((1,2,1),(1,3,1)))
        self.assertTrue(anchored(m,'E',0,1)); self.assertFalse(anchored(m,'E',1,0))
    def test_three_worlds(self):
        m=Model(2,((3,1,2),(1,2,0),(2,3,1)))
        self.assertEqual(m.possible(0),3);self.assertEqual(m.necessary(0),0)
    def test_one_object(self): self.assertEqual(sum(1 for _ in models(1)),64)
    def test_one_world_anchor(self):
        m=Model(2,((1,2,3),))
        for k in 'AEIO': self.assertEqual(ordinary(m,k,0,2),anchored(m,k,0,2))

if __name__=='__main__': unittest.main(verbosity=2)
