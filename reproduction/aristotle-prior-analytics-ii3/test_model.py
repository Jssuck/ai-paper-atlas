"""Author tests; independent review is recorded separately."""
import unittest
from model import Model, proposition as q, classify, type_model, all_models, census, evaluate, true_combinations

class Tests(unittest.TestCase):
    def setUp(self): self.m = Model(frozenset({0,1,2}),frozenset({0,1}),frozenset({0}),frozenset({1,2}))
    def test_argument_direction(self):
        self.assertTrue(q(self.m,'A','M','P')); self.assertFalse(q(self.m,'A','P','M'))
    def test_four_kinds(self):
        self.assertTrue(q(self.m,'E','P','S')); self.assertTrue(q(self.m,'I','M','S')); self.assertTrue(q(self.m,'O','M','S'))
    def test_empty_subject(self):
        m=type_model([4]); self.assertTrue(q(m,'A','M','P')); self.assertTrue(q(m,'E','M','P'))
        self.assertEqual(classify(m,'A','M','P'),'vacuous_true'); self.assertEqual(classify(m,'E','M','P'),'vacuous_true')
        self.assertFalse(q(m,'I','M','P')); self.assertFalse(q(m,'O','M','P'))
    def test_wholly_false(self):
        self.assertEqual(classify(type_model([2]),'A','M','P'),'wholly_false')
        self.assertEqual(classify(type_model([6]),'E','M','P'),'wholly_false')
    def test_partly_false(self):
        for kind in ('A','E'): self.assertEqual(classify(type_model([2,6]),kind,'M','P'),'partly_false')
    def test_particular_has_no_partial_state(self):
        for kind in ('I','O'): self.assertEqual(classify(self.m,kind,'M','S'),'true')
    def test_both_false_true_conclusion(self):
        self.assertEqual(evaluate(type_model([2,5]),'Camestres')['truth_signature'],'FFT')
        self.assertEqual(evaluate(type_model([1,6]),'Cesare')['truth_signature'],'FFT')
    def test_particular_both_false(self):
        self.assertEqual(evaluate(type_model([1,6]),'Festino')['truth_signature'],'FFT')
        self.assertEqual(evaluate(type_model([2,5]),'Baroco')['truth_signature'],'FFT')
    def test_true_conclusion_not_true_premises(self):
        self.assertEqual(evaluate(type_model([1,4,6]),'Festino')['truth_signature'],'FFT')
    def test_jenkinson_literal_does_not_give_two_false(self):
        # M includes all P and all S. E(M,P) false, I(M,S) true if S nonempty.
        self.assertEqual(evaluate(type_model([5,6]),'Festino')['truth_signature'],'FTT')
    def test_type_counts(self):
        self.assertEqual(len(list(all_models())),255); self.assertEqual(len(list(all_models(True))),218)
    def test_all_rules_valid(self):
        for m in all_models():
            for mood in ('Cesare','Camestres','Festino','Baroco'):
                self.assertNotEqual(evaluate(m,mood)['truth_signature'],'TTF')
    def test_universal_full_grid(self):
        report=census(True); states=('true','wholly_false','partly_false')
        for mood in ('Cesare','Camestres'):
            self.assertEqual(true_combinations(report,mood),{(x,y) for x in states for y in states})
    def test_particular_full_grid(self):
        report=census(True); states=('true','wholly_false','partly_false')
        for mood in ('Festino','Baroco'):
            self.assertEqual(true_combinations(report,mood),{(x,y) for x in states for y in ('true','false')})
    def test_unknown_terms(self):
        for pred,subj in [('X','M'),('M','X')]:
            with self.assertRaises(ValueError): q(self.m,'A',pred,subj)
    def test_invalid_kind_and_mood(self):
        with self.assertRaises(ValueError): q(self.m,'Z','M','P')
        with self.assertRaises(ValueError): evaluate(self.m,'Barbara')
    def test_invalid_model(self):
        with self.assertRaises(ValueError): Model(frozenset(),frozenset(),frozenset(),frozenset())
        with self.assertRaises(ValueError): Model(frozenset({0}),frozenset({1}),frozenset(),frozenset())
        with self.assertRaises(TypeError): Model({0},frozenset(),frozenset(),frozenset())
    def test_bool_object_rejected(self):
        with self.assertRaises(ValueError): Model(frozenset({True}),frozenset(),frozenset(),frozenset())
    def test_invalid_types(self):
        for x in ([8],[True],[1,1],[-1]):
            with self.assertRaises(ValueError): type_model(x)
    def test_filter_type(self):
        with self.assertRaises(TypeError): list(all_models(1))
    def test_minimal_witnesses(self):
        report=census()
        for mood,rows in report['rows'].items():
            for key,row in rows.items():
                d=row['smallest_type_witness']; witness=Model(**{k:frozenset(v) for k,v in d.items()})
                r=evaluate(witness,mood)
                self.assertEqual('|'.join((r['major'],r['minor'],'T' if r['conclusion'] else 'F')),key)
                for smaller in all_models():
                    if len(smaller.universe)>=len(witness.universe): break
                    s=evaluate(smaller,mood)
                    self.assertNotEqual('|'.join((s['major'],s['minor'],'T' if s['conclusion'] else 'F')),key)

if __name__=='__main__': unittest.main(verbosity=2)
