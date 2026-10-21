import unittest
from itertools import product
import third_figure as m

class ThirdFigureTests(unittest.TestCase):
    def test_support_counts(self):
        self.assertEqual([len(m.supports(p)) for p in m.POLICIES], [255,240,218])
    def test_no_empty_domain(self):
        with self.assertRaises(ValueError): m.truth('A','M','P',())
    def test_bool_type_rejected(self):
        with self.assertRaises(TypeError): m.checked_support((True,))
    def test_duplicate_type_rejected(self):
        with self.assertRaises(ValueError): m.checked_support((1,1))
    def test_range_rejected(self):
        for s in [(-1,), (8,)]:
            with self.assertRaises(ValueError): m.checked_support(s)
    def test_collection_rejected(self):
        with self.assertRaises(TypeError): m.checked_support('7')
    def test_quantifier_rejected(self):
        for q in ['a','U','']:
            with self.assertRaises(ValueError): m.truth(q,'M','P',(7,))
        with self.assertRaises(TypeError): m.truth(None,'M','P',(7,))
    def test_term_rejected(self):
        with self.assertRaises(ValueError): m.truth('A','X','P',(7,))
        with self.assertRaises(TypeError): m.truth('A',0,'P',(7,))
    def test_policy_rejected(self):
        with self.assertRaises(ValueError): m.supports('other')
        with self.assertRaises(TypeError): m.supports(0)
    def test_vacuity(self):
        self.assertTrue(m.truth('A','M','P',(0,)))
        self.assertTrue(m.truth('E','M','P',(0,)))
        self.assertFalse(m.truth('I','M','P',(0,)))
        self.assertFalse(m.truth('O','M','P',(0,)))
    def test_independent_set_truth(self):
        for s in m.supports():
            sets={x:{i for i,t in enumerate(s) if t&m.BITS[x]} for x in m.TERMS}
            for x,y in product(m.TERMS, repeat=2):
                expected={'A':sets[x]<=sets[y], 'E':not sets[x]&sets[y],
                          'I':bool(sets[x]&sets[y]), 'O':bool(sets[x]-sets[y])}
                for q in m.QUANTIFIERS: self.assertEqual(m.truth(q,x,y,s),expected[q])
    def test_contradictories(self):
        for s in m.supports():
            for x,y in product(m.TERMS, repeat=2):
                self.assertNotEqual(m.truth('A',x,y,s),m.truth('O',x,y,s))
                self.assertNotEqual(m.truth('E',x,y,s),m.truth('I',x,y,s))
    def test_symmetric_e_i(self):
        for s in m.supports():
            for q in ('E','I'):
                self.assertEqual(m.truth(q,'M','P',s),m.truth(q,'P','M',s))
    def test_six_moods(self):
        for name,(q,r,c) in m.MOODS.items():
            self.assertTrue(m.entails(q,r,c,'middle-nonempty'),name)
            self.assertTrue(m.entails(q,r,c,'all-nonempty'),name)
            self.assertEqual(m.entails(q,r,c), name not in ('Darapti','Felapton'))
    def test_exact_all_nonempty_classification(self):
        got={(q,r,c) for q,r,c in product(m.QUANTIFIERS,repeat=3) if m.entails(q,r,c,'all-nonempty')}
        self.assertEqual(got,set(m.MOODS.values()))
    def test_exact_empty_allowed_classification(self):
        got={(q,r,c) for q,r,c in product(m.QUANTIFIERS,repeat=3) if m.entails(q,r,c)}
        self.assertEqual(got,{v for k,v in m.MOODS.items() if k not in ('Darapti','Felapton')})
    def test_no_universal_conclusions(self):
        for p in m.POLICIES:
            for q,r,c in product(m.QUANTIFIERS,m.QUANTIFIERS,('A','E')):
                self.assertFalse(m.entails(q,r,c,p))
    def test_countermodels_and_minimality(self):
        for policy in m.POLICIES:
            for q,r,c in product(m.QUANTIFIERS,repeat=3):
                witness=m.countermodel(q,r,c,policy)
                if witness is None: continue
                self.assertTrue(m.premises(q,r,witness)); self.assertFalse(m.truth(c,'S','P',witness))
                self.assertTrue(m.admissible(witness,policy))
                for small in m.supports(policy):
                    if len(small)>=len(witness): break
                    self.assertFalse(m.premises(q,r,small) and not m.truth(c,'S','P',small))
    def test_each_premise_pair_satisfiable(self):
        for p in m.POLICIES:
            for q,r in product(m.QUANTIFIERS,repeat=2):
                self.assertTrue(any(m.premises(q,r,s) for s in m.supports(p)))
    def test_all_six_shared_witness_routes(self):
        for name,(q,r,c) in m.MOODS.items():
            for s in m.supports('middle-nonempty'):
                if m.premises(q,r,s):
                    t=m.proof_witness(name,s)
                    self.assertIn(t,s); self.assertTrue(t&m.BITS['M']); self.assertTrue(t&m.BITS['S'])
                    self.assertEqual(bool(t&m.BITS['P']),c=='I')
    def test_missing_middle_witness(self):
        for name in ('Darapti','Felapton'):
            with self.assertRaises(ValueError): m.proof_witness(name,(0,))
    def test_false_premises_rejected(self):
        with self.assertRaises(ValueError): m.proof_witness('Darapti',(1,))
    def test_bad_route_name(self):
        with self.assertRaises(ValueError): m.proof_witness('Barbara',(7,))
        with self.assertRaises(TypeError): m.proof_witness(1,(7,))
    def test_compression_round_trip(self):
        for s in m.supports(): self.assertEqual(m.compress(m.expand(s)),s)
    def test_duplicate_objects_do_not_change_truth(self):
        for rows in product(tuple(product((False,True), repeat=3)), repeat=2):
            s=m.compress(rows); duplicated=m.compress(rows+rows)
            self.assertEqual(s,duplicated)
    def test_invalid_object_rows(self):
        for rows in [[],[(True,False)],[(True,False,True,False)]]:
            with self.assertRaises(ValueError): m.compress(rows)
        with self.assertRaises(TypeError): m.compress([(1,False,True)])
        with self.assertRaises(TypeError): m.compress({(True,False,True)})
    def test_ps_swap_symmetry(self):
        def swap(s): return tuple(sorted((t&1)|((t&4)>>1)|((t&2)<<1) for t in s))
        for s in m.supports():
            for q,r in product(m.QUANTIFIERS,repeat=2):
                self.assertEqual(m.premises(q,r,s),m.premises(r,q,swap(s)))
    def test_direction_of_conclusion(self):
        s=(3,7) # M=S={both}, P={one}; all M are S, some M are not P
        self.assertTrue(m.premises('O','A',s))
        self.assertTrue(m.truth('O','S','P',s))
        self.assertFalse(m.truth('O','P','S',s))
    def test_distinct_witness_trap(self):
        s=(3,5) # some M are P and some M are S, with disjoint witnesses
        self.assertTrue(m.premises('I','I',s)); self.assertFalse(m.truth('I','S','P',s))
    def test_report_complete(self):
        r=m.report()
        self.assertEqual(len(r['policies']),3)
        self.assertTrue(all(len(v['premise_pairs'])==16 for v in r['policies'].values()))

if __name__=='__main__': unittest.main(verbosity=2)
