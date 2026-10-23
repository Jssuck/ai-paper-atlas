import unittest
from model import Proposition as P, categorical, models, rules, audit, darii, disamis, convert_i


class ModelTests(unittest.TestCase):
    def test_predicate_first_orientation(self):
        self.assertTrue(categorical('A', {0,1}, {0}))
        self.assertFalse(categorical('A', {0}, {0,1}))
        self.assertTrue(categorical('O', {0}, {1}))
        self.assertFalse(categorical('O', {0,1}, {1}))
        self.assertTrue(categorical('E', {0}, {1}))
        self.assertTrue(categorical('I', {0}, {0,1}))
        with self.assertRaises(ValueError): categorical('bad', set(), set())

    def test_enumeration_complete_and_distinct(self):
        for n in range(1,5):
            for nonempty in (False,True):
                rows = list(models(n, nonempty))
                self.assertEqual(len(rows), ((2**n-1) if nonempty else 2**n)**3)
                self.assertEqual(len(rows), len(set(rows)))
                self.assertTrue(all(len(row[0]) == n for row in rows))

    def test_all_intended_implications_and_counts(self):
        result = audit()
        self.assertEqual(result['regimes']['empty_terms_allowed']['total_models'], 4680)
        self.assertEqual(result['regimes']['all_terms_nonempty']['total_models'], 3746)
        for regime in result['regimes'].values():
            for name,row in regime['rules'].items():
                if not name.startswith('invalid_'):
                    self.assertGreater(row['premise_models'], 0, name)
                    self.assertEqual(row['countermodels'], 0, name)
        self.assertFalse(result['ordered_syntax_demo']['same_ordered_proposition'])

    def test_invalid_proposals_have_countermodels(self):
        result = audit()
        for regime_name,regime in result['regimes'].items():
            for name,row in regime['rules'].items():
                if name.startswith('invalid_'):
                    if regime_name == 'all_terms_nonempty' and name in ('invalid_darapti_without_existence','invalid_felapton_without_existence'):
                        self.assertEqual(row['countermodels'],0)
                    else:
                        self.assertGreater(row['countermodels'],0,name)

    def test_different_witnesses_are_not_identical(self):
        r = rules({0,1,2},{0},{1},{2})
        self.assertEqual(r['invalid_negative_simple_conversion'], (True,False))
        self.assertEqual(r['invalid_independent_some_bridge'], (True,False))
        self.assertEqual(r['negative_shared_witness_bridge_recovers_I'], (False,False))
        self.assertEqual(r['negative_coverage_bridge_recovers_I'], (False,False))

    def test_conclusion_cannot_restore_universal(self):
        self.assertEqual(rules({0,1},{0},{0},{0,1})['invalid_recover_universal_A'], (True,False))
        self.assertEqual(rules({0,1},{0},{1},{0,1})['invalid_recover_universal_E'], (True,False))

    def test_empty_middle_requires_explicit_existence(self):
        r = rules({0},set(),set(),set())
        self.assertEqual(r['invalid_darapti_without_existence'],(True,False))
        self.assertEqual(r['invalid_felapton_without_existence'],(True,False))
        self.assertFalse(r['original_darapti_with_C_existence'][0])
        self.assertFalse(r['original_felapton_with_C_existence'][0])

    def test_ordered_syntax_not_semantic_counterexample(self):
        direct = darii(P('A','C','A'),P('I','A','B'))
        target = P('I','B','C')
        self.assertEqual(direct,P('I','C','B'))
        self.assertNotEqual(direct,target)
        self.assertEqual(convert_i(direct),target)
        self.assertEqual(disamis(P('A','C','B'),P('I','A','B')),P('I','A','C'))
        for _,a,b,c in models(3):
            self.assertEqual(categorical('I',b,c),categorical('I',c,b))

    def test_schema_guards_remain_active_under_optimization(self):
        with self.assertRaises(ValueError): darii(P('A','C','A'),P('I','B','A'))
        with self.assertRaises(ValueError): disamis(P('A','C','B'),P('I','B','A'))
        with self.assertRaises(ValueError): convert_i(P('O','A','B'))
        for bad in ('', 'AE', 'bad'):
            with self.assertRaises(ValueError): P(bad,'A','B')
        for bad in (0, -1, True, 1.5):
            with self.assertRaises(ValueError): list(models(bad))
        for bad in (0,7,True,1.5):
            with self.assertRaises(ValueError): audit(bad)


if __name__ == '__main__':
    unittest.main(verbosity=2)
