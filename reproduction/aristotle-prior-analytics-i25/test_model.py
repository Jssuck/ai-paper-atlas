import unittest
from model import closure, chain_report, verify_certificate, proof_tree_stats

class ModelTests(unittest.TestCase):
    def test_two_terms(self):
        self.assertEqual(chain_report(['A','B'])['conclusion_count'], 0)
    def test_three_terms(self):
        self.assertEqual(chain_report(['A','B','C'])['conclusions'], [('A','C')])
    def test_four_terms(self):
        self.assertEqual(chain_report(list('ABCD'))['conclusion_count'], 3)
    def test_certificates(self):
        r = chain_report(list('ABCDE'))
        self.assertTrue(verify_certificate(r['premises'], r['steps'], ('A','E')))
    def test_premise_not_proof(self):
        self.assertFalse(verify_certificate([('A','B')], [], ('A','B')))
    def test_wrong_middle(self):
        self.assertFalse(verify_certificate([('A','B'),('C','D')], [('A','B','D')], ('A','D')))
    def test_forward_reference(self):
        self.assertFalse(verify_certificate([('A','B'),('B','C'),('C','D')], [('A','C','D'),('A','B','C')], ('A','D')))
    def test_bad_target(self):
        self.assertFalse(verify_certificate([('A','B'),('B','C')], [('A','B','C')], ('C','A')))
    def test_duplicate_edges(self):
        self.assertEqual(closure([('A','B'),('A','B')]), {('A','B')})
    def test_branch(self):
        self.assertEqual(closure([('A','B'),('A','C')]), {('A','B'),('A','C')})
    def test_cycle(self):
        self.assertEqual(len(closure([('A','B'),('B','A')])), 4)
    def test_no_reflexive_default(self):
        self.assertNotIn(('A','A'), closure([('A','B')]))
    def test_tree(self):
        t=('via',('given','A','B'),('via',('given','B','C'),('given','C','D')))
        self.assertEqual(proof_tree_stats(t), {'conclusion':('A','D'),'inferences':2,'leaf_occurrences':3,'premise_slots':4,'node_occurrences':5})
    def test_shared_tree_occurrences(self):
        t=('via',('given','A','B'),('given','B','A'))
        self.assertEqual(proof_tree_stats(('via',t,t))['inferences'], 3)
    def test_tree_wrong_middle(self):
        with self.assertRaises(ValueError): proof_tree_stats(('via',('given','A','B'),('given','C','D')))
    def test_invalid_chains(self):
        for x in [[], ['A'], ['A','A'], 'AB', ['','B'], [True,'B'], [' A','B']]:
            with self.subTest(x=x), self.assertRaises(ValueError): chain_report(x)
    def test_invalid_edges(self):
        for x in [None, 'AB', [('A',)], [(1,'B')], [('A','B','C')]]:
            with self.subTest(x=x), self.assertRaises(ValueError): closure(x)
    def test_invalid_steps(self):
        for x in [None, 'ABC', [('A','B')], [('A',3,'B')]]:
            with self.subTest(x=x), self.assertRaises(ValueError): verify_certificate([],x,('A','B'))
    def test_invalid_trees(self):
        for x in [None, ['given','A','B'], ('bad','A','B'), ('given','','B')]:
            with self.subTest(x=x), self.assertRaises(ValueError): proof_tree_stats(x)
    def test_depth_guard(self):
        t=('given','A','A')
        for _ in range(202): t=('via',t,('given','A','A'))
        with self.assertRaises(ValueError): proof_tree_stats(t)

if __name__ == '__main__': unittest.main()
