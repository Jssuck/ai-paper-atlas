import unittest
from model import *

class Tests(unittest.TestCase):
    def test_model_counts(self):
        self.assertEqual(len(list(canonical_models())), 128)
        self.assertEqual(len(list(canonical_models(True))), 109)
    def test_mood_counts(self):
        self.assertEqual([len(x) for x in valid_moods().values()], [4, 4, 4])
        self.assertEqual([len(x) for x in valid_moods(True).values()], [6, 6, 6])
    def test_candidates(self):
        for policy in (False, True):
            self.assertEqual({k:candidate_figures(k, policy) for k in KINDS},
                             {'A':(1,), 'E':(1,2), 'I':(1,3), 'O':(1,2,3)})
    def test_darapti_empty_middle(self):
        x=Model({0,1},{0},set(),{1})
        self.assertEqual(evaluate(x,3,'AAI'),(True,True,False))
        self.assertIsNotNone(countermodel(3,'AAI'))
        self.assertIsNone(countermodel(3,'AAI',True))
    def test_candidate_not_proof(self):
        self.assertIn(1,candidate_figures('A'))
        self.assertIsNotNone(countermodel(1,'IAA',True))
    def test_outside_only(self):
        x=next(canonical_models())
        self.assertEqual(x.domain,frozenset({0}))
        self.assertEqual(evaluate(x,1,'AAA'),(True,True,True))
    def test_all_four_kinds(self):
        x=Model({0,1},{0},{0,1},{1})
        self.assertFalse(x.satisfies('A','S','P'))
        self.assertTrue(x.satisfies('E','S','P'))
        self.assertFalse(x.satisfies('I','S','P'))
        self.assertTrue(x.satisfies('O','S','P'))
    def test_mixed_figures(self):
        self.assertEqual([x['figure'] for x in mixed_proof()],[1,2])
        self.assertEqual(classify_step(('E','P','Q'),('A','S','P'),('E','S','Q')),1)
    def test_label_is_not_validity(self):
        self.assertEqual(classify_step(('I','M','P'),('A','S','M'),('A','S','P')),1)
    def test_freeze_generators(self):
        x=Model(iter([0,1]),iter([0]),iter([0,1]),iter([1]))
        self.assertEqual(x.m,frozenset({0,1}))
    def test_bad_domains(self):
        for domain,s,m,p in [(set(),set(),set(),set()),({0},{1},set(),set()),({True},set(),set(),set()),({-1},set(),set(),set())]:
            with self.assertRaises(ValueError):Model(domain,s,m,p)
    def test_bad_figure(self):
        for f in (True,0,4,1.0,'1'):
            with self.assertRaises(ValueError):countermodel(f,'AAA')
    def test_bad_mood(self):
        for mood in ('','AA','AAAA','AXA',None):
            with self.assertRaises(ValueError):countermodel(1,mood)
    def test_bad_policy(self):
        for value in (0,1,None,'True'):
            with self.assertRaises(ValueError):list(canonical_models(value))
    def test_bad_step(self):
        for step in [(('A','S','P'),('A','S','P'),('A','S','P')),
                     (('A','M','P'),('A','S','M'),('A','S','S')),
                     (('X','M','P'),('A','S','M'),('A','S','P'))]:
            with self.assertRaises(ValueError):classify_step(*step)
    def test_unknown_figure_shape(self):
        self.assertIsNone(classify_step(('A','P','M'),('A','M','S'),('A','S','P')))

if __name__ == '__main__':unittest.main()
