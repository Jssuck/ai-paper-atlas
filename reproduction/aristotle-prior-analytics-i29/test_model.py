import copy
import unittest
from model import InvalidProof, atom, examples, finite_report, given, holds, node, assume, verify

class CertificateTests(unittest.TestCase):
    def reject(self, p, ps, target):
        with self.assertRaises(InvalidProof):
            verify(p,ps,target)

    def test_six_certificates(self):
        for name,ps,target,p in examples():
            with self.subTest(name=name):
                self.assertTrue(verify(p,ps,target))

    def test_changed_goal(self):
        _,ps,_,p=examples()[0]
        self.reject(p,ps,('ALL','A','E'))

    def test_changed_middle(self):
        _,ps,target,p=copy.deepcopy(examples()[0])
        p['inputs'][0]['claim']=('ALL','A','C')
        self.reject(p,ps,target)

    def test_missing_existence(self):
        _,ps,target,p=examples()[2]
        self.reject(p,ps[1:],target)

    def test_universal_cannot_supply_witness(self):
        ps=[('ALL','G','G'),('ALL','G','A')]
        self.reject(node('witness',('SOME','G','A'),given(0,ps[0]),given(1,ps[1])),ps,('SOME','G','A'))

    def test_unbound_assumption(self):
        self.reject(assume('h',('NO','A','E')),[],('NO','A','E'))

    def test_bad_discharge(self):
        _,ps,target,p=copy.deepcopy(examples()[1])
        p['assumption']=('SOME','E','A')
        self.reject(p,ps,target)

    def test_noncontradiction_body(self):
        p=node('raa',('NO','A','E'),assume('h',('SOME','A','E')),label='h',assumption=('SOME','A','E'))
        self.reject(p,[],('NO','A','E'))

    def test_vacuous_discharge_rejected(self):
        ps=[('SOME','A','E'),('NO','A','E')]
        clash=node('clash',('FALSE',),given(0,ps[0]),given(1,ps[1]))
        self.reject(node('raa',('NO','A','E'),clash,label='h',assumption=ps[0]),ps,ps[1])

    def test_clash_requires_same_order(self):
        ps=[('SOME','A','E'),('NO','E','A')]
        clash=node('clash',('FALSE',),given(0,ps[0]),given(1,ps[1]))
        self.reject(node('raa',('NO','A','E'),clash,label='h',assumption=ps[0]),ps,('NO','A','E'))

    def test_missing_only_cannot_be_given(self):
        _,_,target,p=examples()[4]
        self.reject(p,[('ALL','G','E'),('ALL','G','A')],target)

    def test_boolean_index(self):
        self.reject(given(True,('EX','G')),[('EX','G'),('EX','G')],('EX','G'))

    def test_negative_index(self):
        self.reject(given(-1,('EX','G')),[('EX','G')],('EX','G'))

    def test_unknown_rule(self):
        self.reject(node('oracle',('EX','G')),[],('EX','G'))

    def test_extra_field(self):
        p=given(0,('EX','G')); p['trust_me']=True
        self.reject(p,[('EX','G')],('EX','G'))

    def test_false_not_a_premise(self):
        self.reject(given(0,('FALSE',)),[('FALSE',)],('EX','G'))

    def test_invalid_terms(self):
        for x in [('EX',''),('EX','a b'),('ALL','A'),('EX',4),([],),('SOME','A','E','F')]:
            with self.subTest(x=x), self.assertRaises(InvalidProof): atom(x)

    def test_lexical_assumption_does_not_escape(self):
        _,ps,_,p=examples()[1]
        bad=node('some_map',('SOME','A','B'),assume('h',('SOME','A','A')),given(0,ps[0]))
        self.reject(bad,ps,('SOME','A','B'))
        self.assertTrue(verify(p,ps,('NO','A','E')))

    def test_depth_bound(self):
        p=given(0,('NO','A','A'))
        for _ in range(70): p=node('no_sym',('NO','A','A'),p)
        self.reject(p,[('NO','A','A')],('NO','A','A'))

    def test_empty_terms_allowed(self):
        m={'A':frozenset(),'E':frozenset()}
        self.assertTrue(holds(('ALL','A','E'),m))
        self.assertTrue(holds(('NO','A','E'),m))
        self.assertFalse(holds(('SOME','A','E'),m))

    def test_finite_semantics_and_counterexamples(self):
        report=finite_report()
        self.assertEqual(report['models'],4368)
        self.assertEqual(report['certificates'],6)
        self.assertEqual(report['counterexamples'],3)
        self.assertTrue(report['two_world_boundary'])

if __name__ == '__main__': unittest.main(verbosity=2)
