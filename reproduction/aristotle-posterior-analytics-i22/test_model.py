"""Tests use unittest checks, not optimized-away assert statements."""
import unittest
from model import definition_link, strict_ranks, order_closure, refinement_successors, all_refinements, horn_closure, experiment

class ModelTests(unittest.TestCase):
    def test_definition_first_direction(self):
        self.assertEqual(definition_link('human','animal',1), ('human','animal'))
    def test_definition_second_direction(self):
        self.assertEqual(definition_link('number','odd',2), ('odd','number'))
    def test_definition_invalid_kind(self):
        with self.assertRaises(ValueError): definition_link('a','b',3)
    def test_definition_invalid_name(self):
        with self.assertRaises(ValueError): definition_link('','b',1)
    def test_rank_chain(self):
        self.assertEqual(strict_ranks({0,1,2}, {(0,1),(1,2)}), {0:2,1:1,2:0})
    def test_empty_graph(self):
        self.assertEqual(strict_ranks(set(), set()), {})
    def test_cycle(self):
        with self.assertRaises(ValueError): strict_ranks({0,1}, {(0,1),(1,0)})
    def test_self_loop(self):
        with self.assertRaises(ValueError): strict_ranks({0}, {(0,0)})
    def test_unknown_edge(self):
        with self.assertRaises(ValueError): strict_ranks({0}, {(0,1)})
    def test_transitive_closure(self):
        self.assertEqual(order_closure({0,1,2}, {(0,1),(1,2)}), {(0,1),(1,2),(0,2)})
    def test_insert_chain(self):
        states, terminal = all_refinements(0,2,{0,1,2},{(0,1),(1,2)})
        self.assertEqual(states, {(0,2),(0,1,2)})
        self.assertEqual(terminal, {(0,1,2)})
    def test_diamond_has_two_terminal_paths(self):
        states, terminal = all_refinements(0,3,{0,1,2,3},{(0,1),(0,2),(1,3),(2,3)})
        self.assertEqual(terminal, {(0,1,3),(0,2,3)})
        self.assertNotIn((0,1,2,3), states)
    def test_nontransitive_rejected(self):
        with self.assertRaises(ValueError): refinement_successors((0,1,2),{0,1,2},{(0,1),(1,2)})
    def test_invalid_chain(self):
        with self.assertRaises(ValueError): refinement_successors((0,0),{0},set())
    def test_incomparable_endpoints(self):
        with self.assertRaises(ValueError): all_refinements(0,1,{0,1},set())
    def test_horn_unseeded_cycle(self):
        result, rounds=horn_closure({'p','q'}, [({'p'},'q'),({'q'},'p')], set())
        self.assertEqual(result,set()); self.assertEqual(rounds,[])
    def test_horn_seeded_cycle(self):
        result, rounds=horn_closure({'p','q','r'}, [({'p'},'q'),({'q'},'p'),({'q'},'r')], {'p'})
        self.assertEqual(result,{'p','q','r'}); self.assertEqual(rounds,[{'q'},{'r'}])
    def test_horn_empty_rule_is_axiom(self):
        self.assertEqual(horn_closure({'p'},[(set(),'p')],set())[0], {'p'})
    def test_horn_requires_all_premises(self):
        self.assertEqual(horn_closure({'p','q','r'},[({'p','q'},'r')],{'p'})[0], {'p'})
    def test_horn_unknown_atom(self):
        with self.assertRaises(ValueError): horn_closure({'p'},[({'p'},'q')],set())
    def test_exhaustive_finite_orders(self):
        result=experiment()['finite_orders']
        self.assertEqual(result['graphs'],75)
        for name,value in result.items():
            if name.endswith('violations'):self.assertEqual(value,0,name)

if __name__=='__main__':unittest.main(verbosity=2)
