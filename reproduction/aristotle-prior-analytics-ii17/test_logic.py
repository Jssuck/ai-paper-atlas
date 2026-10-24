import unittest
from logic import closure, minimal_supports, analyze, scenarios, exhaustive

class Tests(unittest.TestCase):
    def test_transitive(self):
        self.assertIn(('C','A'),closure([('C','B'),('B','A')],'ABC'))
    def test_identity(self):
        self.assertEqual(minimal_supports([],('A','A'),'A'),(frozenset(),))
    def test_no_reverse(self):
        self.assertNotIn(('A','B'),closure([('B','A')],'AB'))
    def test_down_irrelevant(self):
        self.assertTrue(scenarios()['down_irrelevant']['after_deleted'])
    def test_down_necessary(self):
        self.assertTrue(scenarios()['down_necessary']['necessary_within_graph'])
    def test_up_irrelevant(self):
        self.assertTrue(scenarios()['up_irrelevant']['after_deleted'])
    def test_up_necessary(self):
        self.assertTrue(scenarios()['up_necessary']['necessary_within_graph'])
    def test_used_but_redundant(self):
        r=scenarios()['used_but_redundant'];self.assertTrue(r['proof_uses_hypothesis']);self.assertTrue(r['after_deleted']);self.assertEqual(len(r['supports']),2)
    def test_replacement_not_deletion(self):
        r=scenarios()['replacement_not_deletion'];self.assertFalse(r['original_after_deleted']);self.assertTrue(r['changed_background_derives_target'])
    def test_not_initially_derived(self):
        r=scenarios()['not_initially_derived'];self.assertFalse(r['before']);self.assertFalse(r['necessary_within_graph'])
    def test_cycle_not_minimal(self):
        r=scenarios()['cyclic_detour'];self.assertTrue(r['proof_uses_hypothesis']);self.assertEqual(r['supports'],[[['C','A']]])
    def test_exhaustive(self):
        r=exhaustive();self.assertEqual(r['deletion_records'],1728);self.assertEqual(r['support_equivalence_checks'],1728)
    def test_generator_inputs(self):
        self.assertIn(('C','A'),closure((e for e in [('C','B'),('B','A')]),(x for x in 'ABC')))
    def test_bad_inputs(self):
        for f in [lambda:closure([('A','Z')],'AB'),lambda:closure([],['A','A']),lambda:closure(['AB'],'AB'),lambda:analyze([],('A','B'),('A','B'),'AB'),lambda:minimal_supports([],('A','Z'),'AB')]:
            with self.assertRaises(ValueError):f()
    def test_bad_proof(self):
        with self.assertRaises(ValueError):analyze([('A','B')],('A','B'),('A','B'),'ABC',['A','C','B'])
if __name__=='__main__': unittest.main(verbosity=2)
