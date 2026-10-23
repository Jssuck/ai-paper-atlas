#!/usr/bin/env python3
"""Regression tests using unittest (checks remain active under -O and -OO)."""
import unittest
from check import P, MOODS, POLICIES, cases, model, models, holds, evaluate_case, report, witness

class TeachingTests(unittest.TestCase):
    def test_model_input(self):
        for value in (0,256,-1,True,1.0,'1',None):
            with self.assertRaises(ValueError): model(value)
        self.assertEqual(model(1), dict(A=frozenset(),B=frozenset(),C=frozenset()))
        self.assertEqual(model(128), dict(A=frozenset({7}),B=frozenset({7}),C=frozenset({7})))

    def test_prop_input(self):
        for args in [('Q','A','B'),('A','X','B'),('I','A','X')]:
            with self.assertRaises(ValueError): P(*args)
        with self.assertRaises(ValueError): list(models('nonempty-ish'))

    def test_truth_definitions(self):
        m = {'A':{1},'B':{1,2},'C':set()}
        for kind,expected in [('A',False),('E',False),('I',True),('O',True)]:
            self.assertEqual(holds(P(kind,'A','B'),m),expected)
        self.assertTrue(holds(P('A','A','C'),m))
        self.assertTrue(holds(P('E','A','C'),m))
        self.assertFalse(holds(P('I','A','C'),m))
        self.assertFalse(holds(P('O','A','C'),m))

    def test_contradictory_complements(self):
        for _,m in models('empty_allowed'):
            for x in 'ABC':
                for y in 'ABC':
                    self.assertNotEqual(holds(P('A',x,y),m),holds(P('O',x,y),m))
                    self.assertNotEqual(holds(P('E',x,y),m),holds(P('I',x,y),m))

    def test_policy_counts(self):
        self.assertEqual([len(list(models(p))) for p in POLICIES],[255,240,218])

    def test_case_coverage(self):
        cs=list(cases())
        self.assertEqual(len(cs),24)
        self.assertEqual(len({c['id'] for c in cs}),24)
        self.assertEqual(sum(c['mode']=='contrary' for c in cs),12)

    def test_original_moods(self):
        for policy,data in report()['policies'].items():
            for name,row in data['original_moods'].items():
                self.assertGreater(row['background_count'],0)
                self.assertEqual(row['countermodels']>0, policy=='empty_allowed' and name in ('Darapti','Felapton'))

    def test_replacement_results_and_refutations(self):
        for policy in POLICIES:
            for c in cases():
                row=evaluate_case(c,policy)
                self.assertGreater(row['background_count'],0)
                if c['mode']=='contradictory':
                    self.assertEqual(row['result_countermodels'],0)
                    exception=policy=='empty_allowed' and c['mood'] in ('Darapti','Felapton')
                    self.assertEqual(row['refutation_countermodels']>0,exception)
                else:
                    self.assertGreater(row['refutation_countermodels'],0)
                    self.assertEqual(row['valid_target_pair_forms'],[])

    def test_saved_countermodels_replay(self):
        for policy in POLICIES:
            for c in cases():
                row=evaluate_case(c,policy)
                w=row['first_refutation_countermodel']
                if w is not None:
                    m=model(w['mask'])
                    self.assertTrue(holds(c['retained'],m))
                    self.assertTrue(holds(c['replacement'],m))
                    self.assertTrue(holds(c['target'],m))
                    self.assertEqual(w,witness(w['mask']))

    def test_two_distinct_existential_witnesses(self):
        m={'A':{1},'B':{1,2},'C':{1}}
        self.assertTrue(holds(P('I','A','B'),m))
        self.assertTrue(holds(P('O','A','B'),m))
        # Original Darapti and its particular-negative replacement coexist.
        self.assertTrue(all(holds(p,m) for p in MOODS['Darapti']))
        # Likewise original Felapton with its particular-affirmative replacement.
        n={'A':{1},'B':{1,2},'C':{2}}
        self.assertTrue(all(holds(p,n) for p in MOODS['Felapton']))
        self.assertTrue(holds(P('I','A','B'),n))

    def test_empty_C_is_not_refutation(self):
        m={'A':{1},'B':{2},'C':set()}
        self.assertTrue(holds(P('A','A','C'),m))
        self.assertTrue(holds(P('E','A','C'),m))
        self.assertFalse(holds(P('I','A','B'),m))

    def test_reverse_direction_not_no_consequence(self):
        c=next(c for c in cases() if c['id']=='Darapti/contrary/retain_AC')
        row=evaluate_case(c,'all_nonempty')
        self.assertEqual(row['valid_target_pair_forms'],[])
        self.assertIn('O(C,B)',row['valid_reverse_pair_forms'])

if __name__=='__main__': unittest.main(verbosity=2)
