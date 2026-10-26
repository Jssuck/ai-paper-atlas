import unittest
from itertools import product, permutations
from model import powerset, composition, pair_counts, inheritance, Goal, matches_target, dependency_order, graph_counts

class ModelTests(unittest.TestCase):
    def test_powerset(self):
        self.assertEqual(len(powerset(3)),8)
        self.assertEqual(powerset(0),(frozenset(),))
    def test_bad_sizes(self):
        for n in (-1, True, 1.5):
            with self.assertRaises(ValueError): powerset(n)
            with self.assertRaises(ValueError): dependency_order(n,())
    def test_composition(self):
        self.assertEqual(composition({0,1},{1,2}),{1})
    def test_composition_empty(self):
        self.assertEqual(composition(set(),{1}),set())
    def test_component_nonimplication(self):
        a,b = {0,1},{1,2}
        self.assertFalse(a <= b)
        self.assertFalse(b <= a)
        self.assertEqual(composition(a,b),{1})
    def test_count_formula(self):
        for n in range(6):
            c=pair_counts(n)
            self.assertEqual(c['pairs'],4**n)
            self.assertEqual(c['both_inclusions_fail'],4**n-2*3**n+2**n)
            self.assertEqual(c['composition_failures'],0)
    def test_pair_count_three(self):
        self.assertEqual(pair_counts(3)['both_inclusions_fail'],18)
    def test_inheritance_all_three_point_models(self):
        for s,t,p in product(powerset(3),repeat=3):
            r=inheritance(s,t,p)
            if r['premises']: self.assertTrue(r['conclusion'])
    def test_no_upward_inheritance(self):
        self.assertFalse(inheritance({0,1},{0},{0})['conclusion'])
    def test_empty_subject(self):
        self.assertTrue(inheritance(set(),set(),set())['conclusion'])
    def test_goal_kind(self):
        self.assertFalse(matches_target(Goal('attribute','T','P'),Goal('definition','T','P')))
    def test_goal_exact(self):
        g=Goal('definition','T','D')
        self.assertTrue(matches_target(g,g))
        self.assertFalse(matches_target(g,Goal('definition','S','D')))
    def test_goal_invalid(self):
        for args in [('other','T','P'),('attribute','','P'),('definition','T','')]:
            with self.assertRaises(ValueError): Goal(*args)
        with self.assertRaises(TypeError): matches_target('D','D')
    def test_chain(self):
        self.assertEqual(dependency_order(3,((0,1),(1,2))),{'roots':(0,),'order':(0,1,2)})
    def test_disconnected_roots(self):
        self.assertEqual(dependency_order(3,((0,2),))['roots'],(0,1))
    def test_empty_graph(self):
        self.assertEqual(dependency_order(0,()),{'roots':(),'order':()})
    def test_cycles(self):
        for edges in [((0,0),),((0,1),(1,0)),((0,1),(1,2),(2,0))]:
            with self.assertRaises(ValueError): dependency_order(3,edges)
    def test_unknown_nodes(self):
        for edges in [((0,3),),((-1,0),),((True,1),)]:
            with self.assertRaises(ValueError): dependency_order(3,edges)
    def test_graph_enumeration_independent_oracle(self):
        # Independent oracle: try every permutation rather than Kahn's algorithm.
        possible=tuple((i,j) for i in range(3) for j in range(3) if i != j)
        successes=0
        for bits in product((0,1),repeat=6):
            edges=tuple(e for e,bit in zip(possible,bits) if bit)
            oracle=any(all(order.index(a)<order.index(b) for a,b in edges) for order in permutations(range(3)))
            try: dependency_order(3,edges)
            except ValueError: actual=False
            else: actual=True
            self.assertEqual(actual,oracle)
            successes += actual
        self.assertEqual(successes,25)
    def test_graph_counts(self):
        self.assertEqual(graph_counts(3),{'n':3,'graphs':64,'acyclic':25,'cyclic':39,'rootless':27,'nonempty_acyclic_rootless':0})
        with self.assertRaises(ValueError): graph_counts(5)

if __name__ == '__main__': unittest.main(verbosity=2)
