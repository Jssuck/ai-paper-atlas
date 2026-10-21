import unittest
from fractions import Fraction
from model import Model, necessary, possible, contingent, models, extensions, probability

F = frozenset
class Tests(unittest.TestCase):
    def setUp(self):
        self.alt = Model(2, (F({0}), F({1})), (F({0,1}), F({0,1})))
        self.U = F({0,1})
    def test_modal_truth_table(self):
        for v, expected in [((False,False),(False,False,False)),((False,True),(False,True,True)),((True,False),(False,True,True)),((True,True),(True,True,False))]:
            self.assertEqual((necessary(v),possible(v),contingent(v)),expected)
    def test_non_necessary_not_possible(self):
        self.assertFalse(necessary((False,False)))
        self.assertFalse(possible((False,False)))
    def test_alternating_individuals(self):
        self.assertTrue(self.alt.all_each_contingent(self.U))
        self.assertTrue(self.alt.some_each_contingent(self.U))
    def test_no_joint_all_none(self):
        for form in ('all','none'):
            self.assertEqual(self.alt.sentence(self.U,form),(False,False))
    def test_joint_some_notall_necessary(self):
        for form in ('some','notall'):
            self.assertEqual(self.alt.sentence(self.U,form),(True,True))
            self.assertFalse(self.alt.sentence_contingent(self.U,form))
    def test_empty_subject(self):
        self.assertTrue(self.alt.all_each_contingent(F()))
        self.assertFalse(self.alt.some_each_contingent(F()))
        for form in ('all','none','some','notall'):
            self.assertFalse(self.alt.sentence_contingent(F(),form))
    def test_possible_stricter(self):
        m=Model(2,(F({0,1}),F({1})),(F({0}),F({1})))
        self.assertTrue(m.all_each_contingent(m.subject()))
        self.assertFalse(m.all_each_contingent(m.subject('possible')))
    def test_no_term_swap(self):
        self.assertTrue(self.alt.all_each_contingent(self.alt.subject()))
        self.assertFalse(self.alt.swap().all_each_contingent(self.alt.swap().subject()))
    def test_complement_extensions_directly(self):
        m=Model(3,(F(),F({0,2}),F({0,1,2})),(F({1}),F(),F({0})))
        c=m.complement()
        self.assertEqual(c.n,3)
        self.assertEqual(c.A,(F({0,1,2}),F({1}),F()))
        self.assertEqual(c.B,m.B)
        self.assertEqual(c.complement(),m)
        self.assertEqual(m.A,(F(),F({0,2}),F({0,1,2})))
    def test_swap_extensions_directly(self):
        m=Model(3,(F(),F({0,2}),F({0,1,2})),(F({1}),F(),F({0})))
        s=m.swap()
        self.assertEqual(s.n,3)
        self.assertEqual(s.A,(F({1}),F(),F({0})))
        self.assertEqual(s.B,(F(),F({0,2}),F({0,1,2})))
        self.assertEqual(s.swap(),m)
        self.assertEqual(m.B,(F({1}),F(),F({0})))
    def test_sentence_contingency_not_each(self):
        m=Model(2,(self.U,F({1})),(self.U,self.U))
        self.assertTrue(m.sentence_contingent(self.U,'all'))
        self.assertFalse(m.all_each_contingent(self.U))
    def test_weighted_not_half(self):
        self.assertEqual(probability((True,False),(9,1)),Fraction(9,10))
        self.assertEqual(probability((True,False),(1,9)),Fraction(1,10))
        self.assertTrue(contingent((True,False)))
    def test_zero_weight_not_modal_necessity(self):
        self.assertEqual(probability((True,False),(1,0)),1)
        self.assertFalse(necessary((True,False)))
    def test_one_world_no_contingency(self):
        for m in models(2,1):
            for x in range(2): self.assertFalse(m.individual(x))
    def test_exhaustive_two_worlds(self):
        count=0
        for m in models(2,2):
            count+=1
            for S in extensions(2):
                self.assertEqual(m.all_each_contingent(S),m.complement().all_each_contingent(S))
                self.assertEqual(m.some_each_contingent(S),m.complement().some_each_contingent(S))
                self.assertEqual(m.sentence_contingent(S,'all'),m.sentence_contingent(S,'notall'))
                self.assertEqual(m.sentence_contingent(S,'none'),m.sentence_contingent(S,'some'))
                if S and m.all_each_contingent(S): self.assertTrue(m.some_each_contingent(S))
            if m.all_each_contingent(m.subject('possible')):
                self.assertTrue(m.all_each_contingent(m.subject('actual')))
        self.assertEqual(count,256)
    def test_invalid_model(self):
        for args in [(0,(F(),),(F(),)),(True,(F(),),(F(),)),(1,(),()),(1,[F()],[F()]),(1,(set(),),(F(),)),(1,(F({1}),),(F(),)),(1,(F({True}),),(F(),)),(1,(F(),F()),(F(),))]:
            with self.assertRaises(ValueError): Model(*args)
    def test_invalid_modal_vector(self):
        for func in (necessary,possible,contingent):
            for v in ([],(),[0],(1,),None,'true'):
                with self.assertRaises(ValueError): func(v)
    def test_invalid_subject(self):
        for S in (set(),F({2}),F({True}),None):
            with self.assertRaises(ValueError): self.alt.all_each_contingent(S)
    def test_invalid_object(self):
        for x in (-1,2,True,'0'):
            with self.assertRaises(ValueError): self.alt.individual(x)
    def test_invalid_policies(self):
        with self.assertRaises(ValueError): self.alt.subject('unknown')
        with self.assertRaises(ValueError): self.alt.sentence(self.U,'X')
    def test_invalid_enumeration(self):
        for n in (0,True,-1):
            with self.assertRaises(ValueError): extensions(n)
        for w in (0,True,-1):
            with self.assertRaises(ValueError): list(models(1,w))
    def test_invalid_weights(self):
        for weights in ((),(0,0),(-1,2),(True,1),(0.5,0.5),None):
            with self.assertRaises(ValueError): probability((True,False),weights)

if __name__=='__main__': unittest.main(verbosity=2)
