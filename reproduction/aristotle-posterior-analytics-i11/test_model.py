import unittest
from model import Literal as L, Rule as R, closure, support_status, neg, disj, cases_exhaustive, graph_oracle

class TestModel(unittest.TestCase):
    def test_chain(self):
        a,b,c=map(L,['a','b','c']); self.assertEqual(closure([a],[R(frozenset([a]),b),R(frozenset([b]),c)]),frozenset([a,b,c]))
    def test_cycle_without_seed(self):
        a,b=map(L,['a','b']); self.assertEqual(closure([],[R(frozenset([a]),b),R(frozenset([b]),a)]),frozenset())
    def test_conjunctive_rule(self):
        a,b,c=map(L,['a','b','c']); rule=R(frozenset([a,b]),c)
        self.assertNotIn(c,closure([a],[rule])); self.assertIn(c,closure([a,b],[rule]))
    def test_empty_antecedent(self):
        self.assertIn(L('a'),closure([],[R(frozenset(),L('a'))]))
    def test_homonyms(self):
        self.assertNotIn(L('animal'),closure([L('bank.financial')],[R(frozenset([L('bank.river')]),L('animal'))]))
    def test_both_middle(self):
        h,a=L('human'),L('animal'); r=R(frozenset([h]),a)
        self.assertIn(a,closure([h,L('human',False)],[r]))
    def test_no_explosion(self):
        got=closure([L('human'),L('human',False)],[])
        self.assertNotIn(L('moon_is_cheese'),got)
    def test_no_negative_from_absence(self):
        got=closure([L('animal')],[])
        self.assertEqual(support_status(got,'animal'),(True,False))
        self.assertNotIn(L('not_not_animal'),got)
    def test_explicit_negative(self):
        got=closure([L('human')],[R(frozenset([L('human')]),L('animal',False))])
        self.assertEqual(support_status(got,'animal'),(False,True))
    def test_both_and_neither_status(self):
        self.assertEqual(support_status([L('a'),L('a',False)],'a'),(True,True))
        self.assertEqual(support_status([],'a'),(False,False))
    def test_no_contraposition(self):
        got=closure([L('b',False)],[R(frozenset([L('a')]),L('b'))])
        self.assertNotIn(L('a',False),got)
    def test_monotonicity(self):
        rules=[R(frozenset([L('a')]),L('b'))]
        self.assertLessEqual(closure([L('a')],rules),closure([L('a'),L('a',False)],rules))
    def test_lem(self):
        self.assertEqual([disj(x,neg(x)) for x in ['F','U','T']],['T','U','T'])
    def test_local_case_exhaustion(self):
        self.assertTrue(cases_exhaustive(['T','F'],['T','F']))
        self.assertFalse(cases_exhaustive(['T','U','F'],['T','F']))
    def test_double_negation(self):
        self.assertEqual(neg(neg('U')),'U')
    def test_validation(self):
        for f in [lambda:L(''),lambda:L('x',1),lambda:neg('X'),lambda:disj('T','X'),lambda:cases_exhaustive([],[])]:
            with self.assertRaises(ValueError):f()
    def test_rule_validation(self):
        with self.assertRaises(ValueError):R(set(),L('a'))
        with self.assertRaises(ValueError):closure(['a'],[])
    def test_graph_oracle_edges(self):
        self.assertEqual(graph_oracle(1,0),{0})
        self.assertEqual(graph_oracle(0,4095),set())
        self.assertEqual(graph_oracle(1,4095),{0,1,2,3})

if __name__=='__main__': unittest.main(verbosity=2)
