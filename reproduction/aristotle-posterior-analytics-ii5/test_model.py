import unittest
from model import subsets, division, elimination, check_path, conjunction, relative_atom, enumerate_models, examples
F = frozenset

class Tests(unittest.TestCase):
    def test_subsets(self): self.assertEqual(len(subsets(3)), 8)
    def test_empty_universe(self): self.assertEqual(subsets(0), [F()])
    def test_bad_size(self):
        for n in (-1, 1.5, True):
            with self.assertRaises(ValueError): subsets(n)
    def test_partition(self): self.assertEqual(division(F({0,1}), F({0}), F({1})), dict(within=True,covers=True,disjoint=True))
    def test_overlap(self): self.assertFalse(division(F({0}), F({0}), F({0}))['disjoint'])
    def test_gap(self): self.assertFalse(examples()['coverage_gap']['premises'])
    def test_gap_conclusion(self): self.assertFalse(examples()['coverage_gap']['conclusion'])
    def test_partition_does_not_select(self): self.assertFalse(examples()['partition_without_selection']['conclusion'])
    def test_eliminate(self): self.assertTrue(elimination(F({0}),F({0,1}),F({0}),F({1}))['premises'])
    def test_overlap_elimination_valid(self): self.assertTrue(elimination(F({0}),F({0,1}),F({0,1}),F({1}))['premises'])
    def test_empty_target_vacuous(self): self.assertTrue(elimination(F(),F({0}),F(),F({0}))['conclusion'])
    def test_outside_parent(self): self.assertFalse(elimination(F({2}),F({0}),F({0}),F())['premises'])
    def test_path(self): self.assertTrue(examples()['path']['extensional_certificate'])
    def test_no_essence(self): self.assertFalse(examples()['path']['essence_certified'])
    def test_bad_path_target(self): self.assertFalse(check_path(F({1}), F({0,1}), [(F({0}),F({1}),'left','assumption')])['extensional_certificate'])
    def test_bad_choice(self):
        with self.assertRaises(ValueError): check_path(F(),F(),[(F(),F(),'maybe','assumption')])
    def test_bad_provenance(self):
        with self.assertRaises(ValueError): check_path(F(),F(),[(F(),F(),'left','oracle')])
    def test_omissions(self):
        e=examples(); self.assertEqual(e['formula_full'],[0]);self.assertEqual(e['omit_last'],[0,1]);self.assertEqual(e['skip_middle'],[0,2])
    def test_redundant(self): self.assertTrue(examples()['redundant_addition_same_extension'])
    def test_atom_relative(self):
        e=examples();self.assertTrue(e['relative_atom_before_new_predicate']);self.assertFalse(e['relative_atom_after_new_predicate'])
    def test_empty_not_atom(self): self.assertFalse(relative_atom(F(),[F()]))
    def test_outside_predicate(self):
        with self.assertRaises(ValueError): conjunction(F({0}),[F({1})])
    def test_enumeration(self):
        r=enumerate_models();self.assertEqual(r['models'],4369);self.assertEqual(r['oracle_mismatches'],0);self.assertEqual(r['elimination_violations'],0);self.assertGreater(r['selection_failures'],0)
    def test_limit(self):
        with self.assertRaises(ValueError): enumerate_models(5)

if __name__ == '__main__': unittest.main(verbosity=2)
