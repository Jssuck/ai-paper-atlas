import unittest
from itertools import product
from model import all_of, none_of, status, profile, subsets, scenarios, enumerate_models

class ModelTests(unittest.TestCase):
    def setUp(self):
        self.results = enumerate_models()
    def test_direction(self):
        self.assertTrue(all_of({1}, {1, 2}))
        self.assertFalse(all_of({1, 2}, {1}))
    def test_status_distinctions(self):
        self.assertEqual(status('all', {1}, {2}), 'wholly_false')
        self.assertEqual(status('all', {1, 2}, {1}), 'partly_false')
        self.assertEqual(status('none', {1, 2}, {1}), 'partly_false')
    def test_empty_is_true_not_wholly_false(self):
        self.assertEqual(status('all', set(), {1}), 'true')
        self.assertEqual(status('none', set(), {1}), 'true')
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): status('some', {1}, {1})
        with self.assertRaises(ValueError): subsets(-1)
    def test_validity(self):
        for result in self.results['validity'].values():
            self.assertEqual(result, {'interpretations': 512, 'counterexamples': 0})
    def test_fixed_true_chains(self):
        for name in ('negative_fixed_true_chain','positive_fixed_true_chain'):
            self.assertEqual(set(self.results['structural_scenarios'][name]['profiles']), {'wholly_false/true'})
    def test_negative_wrong_middle(self):
        groups = self.results['structural_scenarios']
        self.assertEqual(set(groups['negative_under_disjoint_minor']['profiles']), {'wholly_false/wholly_false'})
        self.assertEqual(set(groups['negative_disjoint_major']['profiles']), {'true/wholly_false'})
    def test_positive_under(self):
        self.assertEqual(set(self.results['structural_scenarios']['positive_under_major']['profiles']), {'true/wholly_false'})
    def test_positive_not_under_major_always_false(self):
        keys = self.results['structural_scenarios']['positive_not_under_major']['profiles']
        self.assertTrue(all(not key.startswith('true/') for key in keys))
        self.assertIn('wholly_false/true', keys)
        self.assertIn('wholly_false/wholly_false', keys)
    def test_second_figure_not_both_wholly_false(self):
        for form in ('Cesare','Camestres'):
            keys = self.results['structural_scenarios']['second_figure_'+form]['profiles']
            self.assertNotIn('wholly_false/wholly_false',keys)
            self.assertIn('partly_false/partly_false',keys)
    def test_second_figure_four_element_check(self):
        for a,b,c in product(subsets(4,True),repeat=3):
            if b <= a:
                for form in ('Cesare','Camestres'):
                    self.assertNotEqual(profile(form,a,b,c)[:2], ('wholly_false','wholly_false'))
    def test_noninclusion_not_disjointness(self):
        a,b,c = {0,1},{0},{1,2}
        self.assertFalse(c <= a)
        self.assertFalse(none_of(c,a))
        self.assertEqual(profile('Celarent',a,b,c), ('partly_false','wholly_false','wholly_false'))
    def test_music_example_structure(self):
        self.assertEqual(profile('Barbara',{0},{1},{1,2}), ('wholly_false','true','wholly_false'))
    def test_readme_examples(self):
        for form,a,b,c,expected in [
            ('Celarent',{0,1},{0},{0,1},('wholly_false','true')),
            ('Celarent',{0,1},{0},{1},('wholly_false','wholly_false')),
            ('Celarent',{0},{0},{1},('true','wholly_false')),
            ('Barbara',{0,1},{2},{1},('true','wholly_false')),
            ('Barbara',{0},{1},{2},('wholly_false','wholly_false')),
            ('Camestres',{0,1,2},{0,1},{0},('partly_false','partly_false'))]:
            self.assertEqual(profile(form,a,b,c)[:2],expected)
    def test_saved_witnesses(self):
        for group in self.results['structural_scenarios'].values():
            self.assertEqual(group['count'],sum(group['profiles'].values()))
            for key,w in group['witnesses'].items():
                p = profile(w['form'],set(w['A']),set(w['B']),set(w['C']))
                self.assertEqual('/'.join(p[:2]),key)
                self.assertNotEqual(p[2],'true')
    def test_zero_universe(self):
        self.assertEqual(enumerate_models(0)['nonempty_triples'],0)

if __name__ == '__main__':
    unittest.main()
