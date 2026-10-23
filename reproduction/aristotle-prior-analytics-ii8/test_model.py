"""Regression tests; unittest checks remain active under -O and -OO."""
import unittest
from model import (MOODS, KINDS, TERMS, models, extension, holds, conjunction,
                   opposite, analyse, report)


class ConversionTests(unittest.TestCase):
    def test_model_counts(self):
        self.assertEqual(report()['model_counts'], {
            'empty_terms_allowed':255, 'C_nonempty':240, 'all_terms_nonempty':218})

    def test_original_four_moods(self):
        for model in models():
            for mood in MOODS:
                if conjunction(model,(mood.major,mood.minor)):
                    self.assertTrue(holds(model,mood.conclusion))

    def test_contradictories_exact_negation(self):
        for model in models():
            for kind in KINDS:
                for pred in TERMS:
                    for subj in TERMS:
                        statement=(kind,pred,subj)
                        self.assertNotEqual(holds(model,statement),holds(model,opposite(statement,'contradictory')))

    def test_all_eight_contradictory_refutations(self):
        for mood in MOODS:
            for keep in ('major','minor'):
                row=analyse(mood,'contradictory',keep,'empty_terms_allowed')
                self.assertGreater(row['satisfying_models'],0)
                self.assertEqual(row['refutation_counterexamples'],0)
                self.assertEqual(row['stated_result_counterexamples'],0)

    def test_universal_contrary_refutations_need_existence(self):
        for mood in MOODS[:2]:
            for keep in ('major','minor'):
                row=analyse(mood,'contrary',keep,'C_nonempty')
                self.assertEqual(row['refutation_counterexamples'],0)
                self.assertEqual(row['stated_result_counterexamples'],0)
                empty=analyse(mood,'contrary',keep,'empty_terms_allowed')
                self.assertGreater(empty['refutation_counterexamples'],0)
                self.assertEqual(empty['first_refutation_countermodel']['C'],[])
                if keep=='major':
                    self.assertEqual(empty['stated_result_counterexamples'],0)
                else:
                    self.assertGreater(empty['stated_result_counterexamples'],0)

    def test_particular_contrary_neither_refutes(self):
        for mood in MOODS[2:]:
            for keep in ('major','minor'):
                row=analyse(mood,'contrary',keep,'all_terms_nonempty')
                self.assertGreater(row['refutation_counterexamples'],0)
                if keep=='major':
                    self.assertEqual(row['stated_result_counterexamples'],0)
                else:
                    self.assertIsNone(row['stated_result'])
                    self.assertEqual(row['entailed_ordered_pair_results'],[])

    def test_shared_countermodel_particular_opposition(self):
        # C has two witnesses: type 7 belongs to all three terms; type 4 only to C.
        # Thus A=B={7}, C={4,7}.
        model=frozenset({4,7})
        for statement in [('I','A','C'),('O','A','C'),('I','B','C'),('O','B','C')]:
            self.assertTrue(holds(model,statement))
        self.assertTrue(holds(model,('U','A','B')))

    def test_countermodel_replay(self):
        for row in report()['rows']:
            w=row['first_refutation_countermodel']
            if w:
                model=frozenset(w['inhabited_types'])
                self.assertTrue(conjunction(model,row['assumptions']))
                self.assertTrue(holds(model,row['dropped_premise']))
                self.assertFalse(holds(model,row['refutation_target']))

    def test_invalid_inputs_are_rejected(self):
        for bad in (frozenset(), frozenset({8}), frozenset({True}), {1}):
            with self.assertRaises(ValueError): holds(bad,('U','A','B'))
        for bad in (('Q','A','B'), ('U','D','B'), ['U','A','B'], ('U','A')):
            with self.assertRaises(ValueError): holds(frozenset({1}),bad)
        with self.assertRaises(ValueError): list(models('unknown'))
        with self.assertRaises(ValueError): opposite(('U','A','B'),'unknown')
        with self.assertRaises(ValueError): analyse(MOODS[0],'contrary','unknown','C_nonempty')

    def test_generator_and_validation_before_short_circuit(self):
        model=frozenset({1})
        valid=[('U','A','A'),('E','A','B')]
        self.assertEqual(conjunction(model,iter(valid)),conjunction(model,valid))
        with self.assertRaises(ValueError):
            conjunction(model,iter([('E','A','A'),('bad','A','B')]))


if __name__=='__main__':
    unittest.main(verbosity=2)
