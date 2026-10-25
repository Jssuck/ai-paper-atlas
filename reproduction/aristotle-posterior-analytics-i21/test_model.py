import unittest
from model import All,E,O,semantic_results,measure,successors,ranking_results,has_cycle,switching_example

class Tests(unittest.TestCase):
    def test_all_direction(self):
        self.assertTrue(All(3,1));self.assertFalse(All(1,3))
    def test_disjoint_symmetry(self):
        for p in range(8):
            for s in range(8):self.assertEqual(E(p,s),E(s,p))
    def test_empty_subject(self):
        self.assertTrue(All(1,0));self.assertTrue(E(1,0));self.assertFalse(O(1,0))
    def test_particular_not_universal(self):
        self.assertTrue(O(1,3));self.assertFalse(E(1,3))
    def test_third_figure_witness(self):
        self.assertTrue(All(3,1) and O(2,1));self.assertTrue(O(2,3));self.assertFalse(E(2,3))
    def test_all_enumerated_rules(self):
        data=semantic_results()
        self.assertEqual(data['assignments'],4681)
        for row in data['rules'].values():
            self.assertGreater(row['premise_cases'],0);self.assertEqual(row['counterexamples'],0)
        self.assertEqual(data['E_to_O_with_nonempty_subject']['counterexamples'],0)
    def test_enumeration_rejects_bad_bounds(self):
        for n in [-1,7,1.5]:
            with self.assertRaises(ValueError):semantic_results(n)
    def test_measure_formula(self):
        self.assertEqual(measure(('E',0,0),4),8)
        self.assertEqual(measure(('O',0,4),4),17)
    def test_all_edges_strict_decrease(self):
        for h in range(6):
            for q in ('E','O'):
                for p in range(h+1):
                    for s in range(h+1):
                        state=(q,p,s)
                        for _,t in successors(state,h,True):self.assertLess(measure(t,h),measure(state,h))
    def test_no_false_quantifier_upgrade(self):
        for _,t in successors(('E',0,0),4,True):self.assertEqual(t[0],'E')
    def test_weakening_requires_witness(self):
        self.assertFalse(any(t[0]=='E' for _,t in successors(('O',1,2),4)))
        self.assertIn(('existential_weakening_backwards',('E',1,2)),successors(('O',1,2),4,True))
    def test_no_same_or_equivalent_progress(self):
        for q in ('E','O'):
            state=(q,2,2)
            self.assertNotIn(state,[t for _,t in successors(state,4,True)])
    def test_zero_height(self):
        data=ranking_results(0)
        self.assertEqual(data['states'],2);self.assertEqual(data['edges'],1);self.assertEqual(data['max_backward_steps'],1)
    def test_invalid_states(self):
        for st in [('A',0,0),('E',-1,0),('O',5,0)]:
            with self.assertRaises(ValueError):measure(st,4)
    def test_finite_rank_bounds(self):
        d=ranking_results(4)
        self.assertEqual(d['strict_decrease_violations'],0)
        self.assertLessEqual(d['max_backward_steps'],d['max_initial_measure'])
    def test_switching_counterexample(self):
        d=switching_example();self.assertFalse(d['R_has_cycle']);self.assertFalse(d['S_has_cycle']);self.assertTrue(d['union_has_cycle'])
    def test_cycle_detector(self):
        self.assertFalse(has_cycle([]));self.assertFalse(has_cycle([('a','b'),('a','c')]))
        self.assertTrue(has_cycle([('a','a')]))

if __name__=='__main__':unittest.main()
