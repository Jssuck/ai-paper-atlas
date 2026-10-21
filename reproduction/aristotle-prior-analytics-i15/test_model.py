import unittest
from model import Model, models, possible, entails
from demo import run

class SemanticTests(unittest.TestCase):
    def test_direct_universal(self):
        m=Model(1,((1,1,1),(0,1,1)))
        self.assertTrue(m.modal('A','B'))
        self.assertTrue(m.categorical('B','C'))
        self.assertTrue(m.modal('A','C'))

    def test_direct_particular_not_universal(self):
        m=Model(2,((1,1,3),(0,1,3)))
        self.assertTrue(m.modal('A','B'))
        self.assertTrue(m.categorical('B','C','I'))
        self.assertTrue(m.modal('A','C',quantity='some'))
        self.assertFalse(m.modal('A','C'))

    def test_actual_index_matters(self):
        m=Model(1,((1,1,1),(0,1,0)),1)
        self.assertEqual(m.members('C'),())
        self.assertFalse(m.modal('A','C',quantity='some'))
        self.assertTrue(m.modal('A','C'))

    def test_stable_positive_not_strong(self):
        m=Model(1,((1,0,1),(1,1,1)))
        self.assertTrue(m.stable('A','B'))
        self.assertTrue(m.modal('B','C'))
        self.assertTrue(m.modal('A','C','M+'))
        self.assertFalse(m.modal('A','C'))
        self.assertFalse(m.reverse_strong_guard('A','B','C'))

    def test_stable_negative_not_strong(self):
        m=Model(1,((0,0,1),(0,1,1)))
        self.assertTrue(m.stable('A','B',True))
        self.assertTrue(m.modal('B','C'))
        self.assertTrue(m.modal('A','C','M-'))
        self.assertFalse(m.modal('A','C'))
        self.assertFalse(m.reverse_strong_guard('A','B','C',True))

    def test_positive_extra_guard(self):
        m=Model(1,((0,0,1),(1,1,1)))
        self.assertTrue(m.stable('A','B'))
        self.assertTrue(m.reverse_strong_guard('A','B','C'))
        self.assertTrue(m.modal('A','C'))

    def test_negative_extra_guard(self):
        m=Model(1,((1,0,1),(0,1,1)))
        self.assertTrue(m.stable('A','B',True))
        self.assertTrue(m.reverse_strong_guard('A','B','C',True))
        self.assertTrue(m.modal('A','C'))

    def test_particular_guard_requires_same_witness(self):
        # x=0 has contingent B and fixed A; x=1 supplies possible not-A only.
        m=Model(2,((1,0,3),(1,1,3)))
        self.assertTrue(m.stable('A','B'))
        self.assertTrue(m.modal('B','C',quantity='some'))
        self.assertTrue(m.modal('A','C','M-',quantity='some'))
        self.assertFalse(m.reverse_strong_guard('A','B','C',quantity='some'))
        self.assertFalse(m.modal('A','C',quantity='some'))

    def test_time_slice_positive_failure(self):
        m=Model(1,((0,0,1),(0,1,1)))
        self.assertTrue(m.categorical('A','B'))
        self.assertTrue(m.modal('B','C'))
        self.assertFalse(m.modal('A','C','M+'))
        self.assertFalse(m.stable('A','B'))

    def test_time_slice_negative_failure(self):
        m=Model(1,((1,0,1),(1,1,1)))
        self.assertTrue(m.categorical('A','B','E'))
        self.assertTrue(m.modal('B','C'))
        self.assertFalse(m.modal('A','C','M-'))
        self.assertFalse(m.stable('A','B',True))

    def test_actual_negative_minor_counterpair(self):
        for m in (Model(2,((3,1,2),(2,1,2))),Model(2,((1,1,2),(0,1,2)))):
            self.assertTrue(m.modal('A','B'))
            self.assertTrue(m.categorical('B','C','E'))
            self.assertTrue(m.categorical('B','C','O'))
            self.assertFalse(m.modal('A','C'))
            self.assertFalse(m.modal('A','C',quantity='some'))

    def test_weak_negative_not_actual_or_necessary_negative(self):
        m=Model(1,((0,1,1),(1,0,1)),1)
        self.assertTrue(m.stable('A','B',True))
        self.assertTrue(m.modal('B','C'))
        self.assertTrue(m.modal('A','C','M-'))
        self.assertFalse(m.categorical('A','C','E'))
        self.assertFalse(m.stable('A','C',True))

    def test_time_slice_failure_without_empty_actual_terms(self):
        positive=Model(2,((1,1,2),(1,2,2)))
        negative=Model(2,((2,1,2),(2,2,2)))
        for m in (positive,negative):
            self.assertTrue(all(m.extension(t) for t in ('A','B','C')))
            self.assertTrue(m.modal('B','C'))
        self.assertTrue(positive.categorical('A','B'))
        self.assertFalse(positive.modal('A','C','M+'))
        self.assertTrue(negative.categorical('A','B','E'))
        self.assertFalse(negative.modal('A','C','M-'))

    def test_pointwise_not_joint(self):
        m=Model(2,((1,0,3),(2,0,3)))
        self.assertTrue(m.modal('A','C'))
        self.assertFalse(m.jointly_possible('A','C'))
        self.assertFalse(m.jointly_possible('A','C',False))

    def test_joint_positive_and_negative(self):
        m=Model(2,((0,0,3),(3,0,3)))
        self.assertTrue(m.jointly_possible('A','C'))
        self.assertTrue(m.jointly_possible('A','C',False))

    def test_empty_subject_policies(self):
        m=Model(1,((0,0,0),))
        for mode in ('K','M+','M-'):
            self.assertTrue(m.modal('A','C',mode))
            self.assertFalse(m.modal('A','C',mode,'some'))
        self.assertTrue(m.categorical('A','C','A'))
        self.assertTrue(m.categorical('A','C','E'))
        self.assertFalse(m.categorical('A','C','I'))
        self.assertFalse(m.categorical('A','C','O'))

    def test_categorical_truths(self):
        m=Model(2,((1,0,3),(3,0,3)))
        self.assertFalse(m.categorical('A','C'))
        self.assertFalse(m.categorical('A','C','E'))
        self.assertTrue(m.categorical('A','C','I'))
        self.assertTrue(m.categorical('A','C','O'))
        self.assertTrue(m.categorical('A','C',world=1))

    def test_single_world_no_nonempty_contingency(self):
        m=Model(1,((1,1,1),))
        self.assertFalse(m.modal('A','C'))
        self.assertTrue(m.modal('A','C','M+'))
        self.assertFalse(m.modal('A','C','M-'))

    def test_false_premise_does_not_preserve_falsity(self):
        self.assertTrue(entails((False,True),(True,True)))
        self.assertTrue(possible((False,True)))

    def test_necessary_implication_not_necessary_conclusion(self):
        p=(True,False)
        self.assertTrue(entails(p,p))
        self.assertFalse(all(p))

    def test_separate_not_joint(self):
        p,r=(True,False),(False,True)
        self.assertTrue(possible(p));self.assertTrue(possible(r))
        self.assertFalse(possible(tuple(a and b for a,b in zip(p,r))))

    def test_fixed_background_counterexample(self):
        p,r,q=(False,True),(True,False),(False,False)
        self.assertTrue(r[0]);self.assertTrue(possible(p))
        self.assertTrue(entails(tuple(a and b for a,b in zip(p,r)),q))
        self.assertFalse(possible(q))

    def test_fixed_background_joint_success(self):
        p,r,q=(False,True),(True,True),(False,True)
        joint=tuple(a and b for a,b in zip(p,r))
        self.assertTrue(possible(joint));self.assertTrue(entails(joint,q))
        self.assertTrue(possible(q))

    def test_generator_counts(self):
        self.assertEqual(sum(1 for _ in models(1)),128)
        self.assertEqual(sum(1 for _ in models(2)),8192)

    def test_model_invalid(self):
        for args in ((0,((0,0,0),)),(True,((0,0,0),)),(1,()),(1,[[0,0,0]]),(1,((0,0),)),(1,((2,0,0),)),(1,((False,0,0),)),(1,((0,0,0),),True),(1,((0,0,0),),-1)):
            with self.subTest(args=args),self.assertRaises(ValueError):Model(*args)

    def test_methods_invalid(self):
        m=Model(1,((0,0,0),))
        operations=(lambda:m.extension('X'),lambda:m.extension('A',True),lambda:m.point('A',-1),lambda:m.point('A',0,1),lambda:m.modal('X','C'),lambda:m.modal('A','C','?'),lambda:m.modal('A','C',quantity='?'),lambda:m.categorical('A','C','?'),lambda:m.stable('A','B',1),lambda:m.reverse_strong_guard('A','B','C',quantity='?'),lambda:m.jointly_possible('A','C',1))
        for op in operations:
            with self.assertRaises(ValueError):op()

    def test_vectors_invalid(self):
        for vals in ((),(0,),(True,1)):
            with self.assertRaises(ValueError):possible(vals)
        with self.assertRaises(ValueError):entails((True,),(True,False))
        for args in ((0,),(1,0),(True,)):
            with self.assertRaises(ValueError):list(models(*args))

    def test_exhaustive_theorems(self):
        out=run();c=out['counts']
        self.assertEqual(c['model_actual_configurations'],8320)
        self.assertEqual(c['truth_vector_pairs'],340)
        self.assertGreater(c['time_slice_positive_failures'],0)
        self.assertGreater(c['time_slice_negative_failures'],0)
        self.assertGreater(c['not_strong_positive_all'],0)
        self.assertGreater(c['not_strong_negative_all'],0)
        self.assertGreater(c['strong_guard_positive_some'],0)

if __name__=='__main__':unittest.main(verbosity=2)
