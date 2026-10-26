"""Independent membership/counting oracles, no removable bare assert statements."""
import unittest
from itertools import product, permutations
from model import intersection,describe,greedy_reduce,split_check,common_features,subsets,experiment

class DefinitionTests(unittest.TestCase):
    def test_empty_family(self):self.assertEqual(intersection({0,1},[]),{0,1})
    def test_empty_universe(self):self.assertEqual(intersection(set(),[set()]),set())
    def test_generators(self):self.assertEqual(intersection(range(3),(x for x in [{0,1},{0,2}])),{0})
    def test_describe_universe_generator(self):
        self.assertEqual(describe((x for x in range(3)),{0},[{0,1},{0,2}]),describe(range(3),{0},[{0,1},{0,2}]))
    def test_outside_feature(self):
        with self.assertRaises(ValueError):intersection({0},[{1}])
    def test_outside_target(self):
        with self.assertRaises(ValueError):describe({0},{1},[])
    def test_exact_wider(self):self.assertEqual(describe(range(3),{0},[{0,1},{0,2}]),dict(sound=True,exact=True,severally_wider=True,irredundant=True))
    def test_sound_not_exact(self):self.assertFalse(describe(range(3),{0},[{0,1},{0,1}])['exact'])
    def test_unsound(self):self.assertFalse(describe(range(3),{0,1},[{0},{0,2}])['sound'])
    def test_exact_not_wider(self):self.assertFalse(describe(range(3),{0},[{0},{0,2}])['severally_wider'])
    def test_duplicate_redundant(self):self.assertFalse(describe(range(2),{0},[{0},{0}])['irredundant'])
    def test_empty_target_possible(self):self.assertTrue(describe(range(2),set(),[{0},{1}])['exact'])
    def test_empty_description(self):self.assertTrue(describe(range(2),{0,1},[])['irredundant'])
    def test_permutations(self):
        fs=[{0,1},{0,2},{0,3}]
        for perm in permutations(fs):self.assertEqual(intersection(range(4),perm),{0})
    def test_membership_oracle(self):
        for n in range(4):
            u=set(range(n));ss=subsets(n)
            for a,b,c in product(ss,repeat=3):
                self.assertEqual(intersection(u,[a,b,c]),{x for x in u if x in a and x in b and x in c})

class ReductionTests(unittest.TestCase):
    def setUp(self):
        self.u=frozenset(range(5));self.t={0}
        self.fs=[self.u-{1,2,3},self.u-{4},self.u-{1,4},self.u-{2},self.u-{3}]
    def test_forward(self):self.assertEqual(greedy_reduce(self.u,self.t,self.fs),(2,3,4))
    def test_reduce_universe_generator(self):
        self.assertEqual(greedy_reduce((x for x in range(5)),self.t,self.fs),(2,3,4))
    def test_reverse(self):self.assertEqual(greedy_reduce(self.u,self.t,self.fs,reversed(range(5))),(0,1))
    def test_not_minimum(self):
        a=greedy_reduce(self.u,self.t,self.fs);b=greedy_reduce(self.u,self.t,self.fs,reversed(range(5)))
        self.assertGreater(len(a),len(b))
        for ids in [a,b]:self.assertTrue(describe(self.u,self.t,[self.fs[i] for i in ids])['irredundant'])
        self.assertFalse(any(f==self.t for f in self.fs))
    def test_nonexact_rejected(self):
        with self.assertRaises(ValueError):greedy_reduce({0,1},{0},[{0,1}])
    def test_bad_order(self):
        with self.assertRaises(ValueError):greedy_reduce({0,1},{0},[{0},{0}], [0,0])
    def test_exhaustive_small(self):
        for n in range(4):
            u=set(range(n));ss=subsets(n)
            for fs in product(ss,repeat=3):
                t={x for x in u if all(x in f for f in fs)}
                ids=greedy_reduce(u,t,fs);kept=[fs[i] for i in ids]
                self.assertEqual({x for x in u if all(x in f for f in kept)},t)
                for k in range(len(kept)):
                    rem=kept[:k]+kept[k+1:]
                    self.assertNotEqual({x for x in u if all(x in f for f in rem)},t)

class DivisionTests(unittest.TestCase):
    def test_partition_branch(self):self.assertTrue(split_check({0,1},{0},{1},{0})['nonempty_unique_branch'])
    def test_gap(self):self.assertFalse(split_check({0,1,2},{0},{1},{0})['covers'])
    def test_overlap(self):self.assertFalse(split_check({0,1},{0,1},{1},{0})['disjoint'])
    def test_empty_target(self):
        d=split_check({0,1},{0},{1},set());self.assertTrue(d['target_left']);self.assertTrue(d['target_right']);self.assertFalse(d['nonempty_unique_branch'])
    def test_straddling_target(self):self.assertFalse(split_check({0,1},{0},{1},{0,1})['nonempty_unique_branch'])
    def test_outside_parent(self):
        with self.assertRaises(ValueError):split_check({0},{0},{1},{0})
    def test_common(self):self.assertEqual(common_features([{'a','b'},{'a','c'}]),{'a'})
    def test_no_common(self):self.assertEqual(common_features([{'a'},{'b'}]),set())
    def test_no_observations(self):
        with self.assertRaises(ValueError):common_features([])
    def test_sample_not_universal(self):
        self.assertEqual(common_features([{'a'},{'a','b'}]),{'a'})
        self.assertEqual(common_features([{'a'},{'a','b'},{'b'}]),set())
    def test_closed_form_counts(self):
        d=experiment();self.assertEqual(d['triples'],sum(8**n for n in range(5)))
        self.assertEqual(d['sound'],sum(5**n for n in range(5)))
        self.assertEqual(d['exact'],sum(4**n for n in range(5)))
        self.assertEqual(d['exact_severally_wider'],sum(4**n-2*3**n+2**n for n in range(5)))
        self.assertEqual(d['irredundant_exact'],130);self.assertEqual(d['membership_oracle_differences'],0)
        self.assertEqual(d['nonempty_unique_branch'],sum(2*3**n-2*2**n for n in range(5)))
if __name__=='__main__':unittest.main()
