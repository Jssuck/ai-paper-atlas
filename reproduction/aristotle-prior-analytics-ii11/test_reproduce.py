"""Regression tests; unittest checks remain active under -O and -OO."""
import unittest
from reproduce import Proposition as P, FORMS, models, truth, implication, classify, route, named_checks

class TeachingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.empty = list(models(False)); cls.occupied = list(models(True))
        cls.results = [classify(False), classify(True)]

    def test_model_counts_and_encoding(self):
        self.assertEqual([len(self.empty),len(self.occupied)], [255,218])
        for mask,m in self.empty:
            for bit,term in enumerate('ABC'):
                self.assertEqual(m[term],frozenset(t for t in range(8) if mask&(1<<t) and t&(1<<bit)))

    def test_contradictories_are_exact(self):
        for _,m in self.empty:
            for f in FORMS:
                p=P(f,'A','B')
                self.assertNotEqual(truth(p,m), truth(p.negate(),m))
                self.assertEqual(p,p.negate().negate())

    def test_candidate_counts(self):
        for r in self.results:
            self.assertEqual(r['candidate_count'],128)
            self.assertEqual(len(set(x['id'] for x in r['rows'])),128)

    def test_allowed_empty_route_inventory(self):
        actual={x['id'] for x in self.results[0]['rows'] if x['certificate']}
        self.assertEqual(actual, {'E-minor-U-I','E-minor-E-O','I-major-U-E','I-major-I-O',
                                 'O-major-U-U','O-major-I-I','O-minor-U-U','O-minor-E-E'})

    def test_nonempty_extra_routes(self):
        a={x['id'] for x in self.results[0]['rows'] if x['certificate']}
        b={x['id'] for x in self.results[1]['rows'] if x['certificate']}
        self.assertEqual(b-a, {'I-major-U-O','O-major-U-I','O-minor-U-I','O-minor-E-O'})
        self.assertTrue(a<=b)

    def test_internal_witness_replay(self):
        for result in self.results:
            for row in result['rows']:
                if row['internal_countermodel'] is not None:
                    w=row['internal_countermodel']; m={k:frozenset(w[k]) for k in 'ABC'}
                    q,pos,x,r=row['id'].split('-')
                    _,h,e,d,_,_=route(q,pos,x,r)
                    self.assertTrue(truth(h,m)); self.assertTrue(truth(e,m)); self.assertFalse(truth(d,m))

    def test_discharge_and_nonvacuity(self):
        for result in self.results:
            for row in result['rows']:
                if row['certificate']:
                    self.assertTrue(row['discharge_valid'])
                    self.assertGreater(row['background_models'],0)
                    self.assertGreater(row['internal_antecedent_models'],0)

    def test_C_existence_is_sufficient(self):
        ps=[P('U','B','C'),P('U','A','C')]; q=P('I','A','B')
        ce,_=implication(ps,q,self.empty)
        self.assertIsNotNone(ce); self.assertEqual(ce['C'],[])
        ce,count=implication(ps,q,[(i,m) for i,m in self.empty if m['C']])
        self.assertIsNone(ce); self.assertGreater(count,0)

    def test_particular_premise_supplies_witness(self):
        ce,count=implication([P('I','B','C'),P('U','A','C')],P('I','A','B'),self.empty)
        self.assertIsNone(ce); self.assertGreater(count,0)

    def test_named_relations_expected(self):
        for case in named_checks()[:11]:
            expected=not(case['id'].startswith('not-') or case['id']=='I-is-not-negation-of-O')
            self.assertEqual(case['all_terms_nonempty']['valid'],expected)
            self.assertEqual(case['empty_allowed']['valid'],expected and case['id']!='I-universal-background-needs-C')

    def test_mixed_case_has_no_false_contradiction(self):
        c=named_checks()[-1]
        self.assertTrue(c['I_A_B']); self.assertTrue(c['O_A_B']); self.assertTrue(c['U_C_A'])
        self.assertTrue(c['I_C_B']); self.assertFalse(c['E_C_B'])
        support=c['model']['support']
        self.assertEqual(c['model']['A'],[t for t in support if t&1])
        self.assertEqual(c['model']['B'],[t for t in support if t&2])
        self.assertEqual(c['model']['C'],[t for t in support if t&4])

    def test_invalid_inputs(self):
        for args in [('A','A','B'),('U','D','B'),('I','A','Z'),('','A','B'),('UE','A','B'),('I','','B'),('I','AB','B'),('I','A','')]:
            with self.assertRaises(ValueError): P(*args)
        with self.assertRaises(ValueError): route('U','unknown','U','U')

if __name__=='__main__': unittest.main(verbosity=2)
