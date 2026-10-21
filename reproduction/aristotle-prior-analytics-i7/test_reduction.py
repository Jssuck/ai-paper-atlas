import copy
import unittest
from itertools import product
import reduction as r

class ReductionTests(unittest.TestCase):
    def test_support_count(self):
        self.assertEqual(len(r.supports()),255)
        self.assertEqual(len(r.supports('all-nonempty')),218)
    def test_truth_against_sets(self):
        for s in r.supports():
            sets={x:{t for t in s if t&r.BITS[x]} for x in r.TERMS}
            for q,x,y in product(r.QS,r.TERMS,r.TERMS):
                a,b=sets[x],sets[y]
                expected={'A':a<=b,'E':not(a&b),'I':bool(a&b),'O':bool(a-b)}[q]
                self.assertEqual(r.truth((q,x,y),s),expected)
    def test_contradiction(self):
        for s in r.supports():
            for p in product(r.QS,r.TERMS,r.TERMS):
                self.assertNotEqual(r.truth(p,s),r.truth(r.negate(p),s))
    def test_conversion_e_i(self):
        for s in r.supports():
            for q,x,y in product(('E','I'),r.TERMS,r.TERMS):
                self.assertEqual(r.truth((q,x,y),s),r.truth((q,y,x),s))
    def test_a_conversion_needs_existence(self):
        self.assertTrue(r.truth(('A','S','P'),(0,)))
        self.assertFalse(r.truth(('I','P','S'),(0,)))
        for s in r.supports():
            if r.truth(('A','S','P'),s) and r.truth(('I','S','S'),s):
                self.assertTrue(r.truth(('I','P','S'),s))
    def test_o_conversion_counterexample(self):
        self.assertTrue(r.truth(('O','S','P'),(2,6)))
        self.assertFalse(r.truth(('O','P','S'),(2,6)))
    def test_all_named_nonempty(self):
        for name,(f,q,z,c) in r.MOODS.items():
            self.assertIsNone(r.countermodel(r.premises(f,q,z),(c,'S','P'),'all-nonempty'),name)
            self.assertTrue(r.verify_certificate(r.named_certificate(name)),name)
    def test_empty_policy_named(self):
        missing=[]
        for name,(f,q,z,c) in r.MOODS.items():
            cm=r.countermodel(r.premises(f,q,z),(c,'S','P'))
            cert=r.named_certificate(name,'allow-empty')
            self.assertEqual(cm is None,cert is not None)
            if cm is not None: missing.append(name)
        self.assertEqual(missing,['Darapti','Felapton'])
    def test_short_darii_ferio(self):
        for name in ('Darii','Ferio'):
            cert=r.explicit_first_figure(name)
            self.assertTrue(r.verify_certificate(cert))
            self.assertTrue(all(x['rule'] not in ('Darii','Ferio') for x in cert['lines']))
    def test_reverse_conclusion(self):
        result=r.classify(1,'A','E','all-nonempty')
        self.assertEqual(result['forward'],[])
        self.assertEqual(result['reverse'],['O'])
    def test_reverse_with_particular(self):
        self.assertEqual(r.classify(1,'I','E')['reverse'],['O'])
    def test_reverse_empty_failure(self):
        self.assertEqual(r.classify(1,'A','E')['reverse'],[])
    def test_semantic_lines(self):
        for name in r.MOODS:
            cert=r.named_certificate(name)
            ps=cert['premises']; assumption=r.negate(cert['goal'])
            for s in r.supports(cert['policy']):
                for line in cert['lines']:
                    if line['rule'] in ('Barbara','Celarent','conversion'):
                        parents=[cert['lines'][i]['p'] for i in line['refs']]
                        if all(r.truth(p,s) for p in parents): self.assertTrue(r.truth(line['p'],s))
    def test_mutated_goal_rejected(self):
        c=r.explicit_first_figure('Darii'); c['goal'][0]='O'
        with self.assertRaises(ValueError): r.verify_certificate(c)
    def test_forward_reference_rejected(self):
        c=r.explicit_first_figure('Darii'); c['lines'][3]['refs']=[3]
        with self.assertRaises(ValueError): r.verify_certificate(c)
    def test_fake_conversion_rejected(self):
        c=r.explicit_first_figure('Darii'); c['lines'][3]['p']=['A','P','S']
        with self.assertRaises(ValueError): r.verify_certificate(c)
    def test_wrong_middle_rejected(self):
        c=r.explicit_first_figure('Darii'); c['lines'][4]['refs']=[3,2]
        with self.assertRaises(ValueError): r.verify_certificate(c)
    def test_missing_clash_rejected(self):
        c=r.explicit_first_figure('Darii'); c['clash']=[0,1]
        with self.assertRaises(ValueError): r.verify_certificate(c)
    def test_unauthorized_existence_rejected(self):
        c=r.named_certificate('Darapti'); c['policy']='allow-empty'
        with self.assertRaises(ValueError): r.verify_certificate(c)
    def test_bad_supports(self):
        for s in ([],(),None,'123',[True],[8],[-1],[1,1],[1.0]):
            with self.assertRaises((ValueError,TypeError)): r.checked_support(s)
    def test_bad_propositions(self):
        for p in (None,[],('Z','S','P'),('A','X','S'),('A','S'),('A',None,'M')):
            with self.assertRaises((ValueError,TypeError)): r.prop(p)
    def test_bad_public_symbols(self):
        for f in (0,4,True,'1',1.0):
            with self.assertRaises(ValueError): r.premises(f,'A','E')
        with self.assertRaises(ValueError): r.supports('unknown')
        with self.assertRaises(ValueError): r.named_certificate('fake')
        with self.assertRaises(ValueError): r.explicit_first_figure('Barbara')
    def test_kernel_does_not_need_semantic_oracle(self):
        cert=r.explicit_first_figure('Darii'); old=r.countermodel
        def unavailable(*a,**kw): raise RuntimeError('oracle unavailable')
        r.countermodel=unavailable
        try: self.assertTrue(r.verify_certificate(cert))
        finally: r.countermodel=old
    def test_inconsistent_premises_explicit(self):
        cert=r.make_certificate([('I','S','P'),('E','S','P')],('I','S','P'))
        self.assertTrue(r.verify_certificate(cert))

if __name__=='__main__': unittest.main()
