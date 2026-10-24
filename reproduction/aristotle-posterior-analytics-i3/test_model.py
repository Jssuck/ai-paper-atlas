import unittest
from model import Rule, closure, truth_oracle, certificate_ok, inclusion_cycle, finite_chain
R = lambda p, h: Rule(frozenset(p), h)

class Tests(unittest.TestCase):
    def test_empty_cycle(self):
        self.assertEqual(closure('AB', [], [R('A','B'),R('B','A')])[0], frozenset())
    def test_rooted_cycle(self):
        self.assertEqual(closure('AB', ['A'], [R('A','B'),R('B','A')])[0], frozenset('AB'))
    def test_self_loop(self):
        self.assertEqual(closure('A', [], [R('A','A')])[0], frozenset())
    def test_no_rules(self):
        self.assertEqual(closure('AB', ['A'], [])[0], frozenset('A'))
    def test_conjunction_not_disjunction(self):
        self.assertEqual(closure('ABC', ['A'], [R('AB','C')])[0], frozenset('A'))
    def test_conjunction_complete(self):
        self.assertEqual(closure('ABC', ['A','B'], [R('AB','C')])[0], frozenset('ABC'))
    def test_rounds(self):
        self.assertEqual(closure('ABC', ['A'], [R('A','B'),R('B','C')])[1], {'A':0,'B':1,'C':2})
    def test_rule_order(self):
        r=[R('A','B'),R('B','C')]
        self.assertEqual(closure('ABC',['A'],r)[0:2],closure('ABC',['A'],r[::-1])[0:2])
    def test_duplicate_rules(self):
        r=[R('A','B')]*2
        self.assertEqual(closure('AB',['A'],r)[0],frozenset('AB'))
    def test_semantic_nonfoundation(self):
        got, worlds=truth_oracle('AB',[],[R('A','B'),R('B','A')])
        self.assertEqual(got,frozenset());self.assertEqual(set(worlds),{frozenset(),frozenset('AB')})
    def test_good_certificate(self):
        r=[R('A','B'),R('B','C')]; result=closure('ABC',['A'],r)
        self.assertTrue(certificate_ok('ABC',['A'],r,*result))
    def test_cycle_certificate_rejected(self):
        self.assertFalse(certificate_ok('AB',[],[R('A','B'),R('B','A')],frozenset('AB'),{'A':1,'B':2},{'A':1,'B':0}))
    def test_inclusion_equal(self):
        self.assertTrue(inclusion_cycle({1},{1},{1}))
    def test_inclusion_strict_not_cycle(self):
        self.assertFalse(inclusion_cycle({1},{1,2},{1,2,3}))
    def test_empty_sets_allowed(self):
        self.assertTrue(inclusion_cycle(set(),set(),set()))
    def test_chain_boundary(self):
        for root in [False,True]:
            a,s,r=finite_chain(1,root)
            self.assertEqual(closure(a,s,r)[0],frozenset(a) if root else frozenset())
    def test_bad_seed(self):
        with self.assertRaises(ValueError):closure('A',['B'],[])
    def test_empty_antecedent_rejected(self):
        with self.assertRaises(ValueError):closure('A',[],[R('','A')])
    def test_bad_chain_length(self):
        with self.assertRaises(ValueError):finite_chain(0,False)
    def test_bad_certificate_type(self):
        self.assertFalse(certificate_ok('A',['A'],[],{'A'},{'A':False},{}))

if __name__=='__main__':unittest.main(verbosity=2)
