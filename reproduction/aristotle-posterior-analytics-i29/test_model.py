import unittest
from model import subset, middle, candidates, pair_kind, paths, negative_routes, enumerate_sets, enumerate_negative

class Tests(unittest.TestCase):
    def test_subset_empty(self): self.assertTrue(subset(0, 5))
    def test_subset_direction(self): self.assertTrue(subset(1, 3)); self.assertFalse(subset(3, 1))
    def test_two_routes(self): self.assertTrue(middle(7, 1, 3)); self.assertTrue(middle(7, 1, 5))
    def test_bad_lower(self): self.assertFalse(middle(7, 3, 1))
    def test_bad_upper(self): self.assertFalse(middle(3, 1, 5))
    def test_incomparable_overlap(self): self.assertEqual(pair_kind(3,5),'incomparable'); self.assertEqual(3 & 5,1)
    def test_equal(self): self.assertEqual(pair_kind(3,3),'equal')
    def test_comparable(self): self.assertEqual(pair_kind(1,3),'comparable_distinct')
    def test_empty_subject_disjoint(self): self.assertTrue(middle(3,0,1)); self.assertTrue(middle(3,0,2)); self.assertEqual(1&2,0)
    def test_candidates(self): self.assertEqual(candidates(7,1,3),(1,3,5,7))
    def test_no_candidates(self): self.assertEqual(candidates(1,2,2),())
    def test_zero_universe(self): self.assertEqual(candidates(0,0,0),(0,))
    def test_bad_universe(self):
        for args in [(8,0,3),(-1,0,3),(0,0,-1)]:
            with self.assertRaises(ValueError): candidates(*args)
    def test_chain(self): self.assertEqual(paths([('B','C'),('C','D'),('D','A')],'B','A'),(('B','C','D','A'),))
    def test_diamond(self): self.assertEqual(len(paths([('B','D'),('D','A'),('B','H'),('H','A')],'B','A')),2)
    def test_cycle(self): self.assertEqual(paths([('B','D'),('D','B'),('D','A')],'B','A'),(('B','D','A'),))
    def test_no_path(self): self.assertEqual(paths([('B','D')],'B','A'),())
    def test_duplicate_edge(self): self.assertEqual(paths([('B','A'),('B','A')],'B','A'),(('B','A'),))
    def test_negative_both(self): self.assertEqual(negative_routes(4,1,3,1),(True,True,True))
    def test_conclusion_not_premises(self): self.assertEqual(negative_routes(4,1,4,4),(False,False,True))
    def test_set_enumeration(self):
        r=enumerate_sets(); self.assertEqual(r['overlap_failures'],0); self.assertEqual(r['conclusion_failures'],0); self.assertEqual(r['candidate_count_failures'],0); self.assertGreater(r['incomparable'],0)
    def test_negative_enumeration(self): self.assertEqual(enumerate_negative()['invalid_conclusions'],0)

if __name__=='__main__': unittest.main(verbosity=2)
