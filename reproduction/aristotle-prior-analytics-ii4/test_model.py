import unittest
import model as m

class ModelTests(unittest.TestCase):
    def test_01_model_count(self): self.assertEqual(len(list(m.models())), 255)
    def test_02_nonempty_terms(self): self.assertEqual(sum(all(m.members(x,t) for t in m.TERMS) for x in m.models()),218)
    def test_03_predicate_first(self):
        self.assertTrue(m.proposition((4,6),'A','A','B'))
        self.assertFalse(m.proposition((4,6),'A','B','A'))
    def test_04_empty_universals(self):
        for k in ('A','E'): self.assertTrue(m.proposition((0,), k,'A','C'))
    def test_05_empty_existentials(self):
        for k in ('I','O'): self.assertFalse(m.proposition((0,), k,'A','C'))
    def test_06_wholly_false(self): self.assertEqual(m.classify((1,), 'A','A','C'),'wholly_false')
    def test_07_partly_false(self): self.assertEqual(m.classify((1,5), 'A','A','C'),'partly_false')
    def test_08_negative_wholly_false(self): self.assertEqual(m.classify((5,), 'E','A','C'),'wholly_false')
    def test_09_negative_partly_false(self): self.assertEqual(m.classify((1,5), 'E','A','C'),'partly_false')
    def test_10_vacuity_not_wholly_false(self): self.assertEqual(m.classify((0,), 'E','A','C'),'vacuous_true')
    def test_11_soundness_all_six(self):
        for x in m.models():
            for name in m.MODES:
                e=m.evaluate(x,name)
                if e['eligible'] and all(e['premises']): self.assertTrue(e['conclusion'],(name,x))
    def test_12_existence_really_required(self):
        for name in ('Darapti','Felapton'):
            e=m.evaluate((0,),name)
            self.assertTrue(all(e['premises'])); self.assertFalse(e['conclusion']); self.assertFalse(e['eligible'])
    def test_13_two_false_true_outside_C(self):
        e=m.evaluate((1,6),'Darapti')
        self.assertEqual(e['classes'],['wholly_false','wholly_false']); self.assertTrue(e['conclusion'])
        self.assertFalse(m.members((1,6),'A') & m.members((1,6),'B') & m.members((1,6),'C'))
    def test_14_negative_outside_C(self):
        e=m.evaluate((2,5),'Felapton')
        self.assertEqual(e['classes'],['wholly_false','wholly_false']); self.assertTrue(e['conclusion'])
    def test_15_invalid_models(self):
        for x in [(),(True,),(-1,),(8,),(1,1),('1',),None]:
            with self.assertRaises(ValueError): m.validate(x)
    def test_16_invalid_proposition(self):
        for k,p,s in [('X','A','C'),('A','X','C'),('A','A','X')]:
            with self.assertRaises(ValueError): m.proposition((1,),k,p,s)
    def test_17_invalid_mode(self):
        with self.assertRaises(ValueError): m.evaluate((1,), 'Barbara')
    def test_18_generator_consumed_safely(self): self.assertTrue(m.proposition(iter([1,5]),'I','A','C'))
    def test_19_ending_equivalence(self):
        for r in m.ending_table(): self.assertEqual(r['both'],r['Q'])
    def test_20_ending_not_contradiction(self):
        self.assertTrue(m.implication(True,True) and m.implication(False,True))
        self.assertEqual(sum(r['both'] for r in m.ending_table()),2)
    def test_21_boolean_validation(self):
        with self.assertRaises(ValueError): m.implication(1,True)
    def test_22_minimum_witness_order(self):
        r=m.survey()
        for name, data in r['modes'].items():
            for key,w in data['minimum_witnesses'].items():
                for x in m.models():
                    if len(x)>=len(w): break
                    e=m.evaluate(x,name)
                    self.assertNotEqual('|'.join(e['classes']+[str(e['conclusion']).lower()]),key)

if __name__=='__main__': unittest.main(verbosity=2)
