import copy
import unittest
from geometry import construct,verify,ledger,strict_json,scalar
from cases import run_cases,negatives
P={'A':[1,2],'B':[0,0],'C':[3,0]}
class Checks(unittest.TestCase):
    def test_sample(self): self.assertTrue(verify(P,construct(P)))
    def test_all_pairs(self): self.assertEqual(set(construct(P)['pairs']),{'AB','BC','CA'})
    def test_pair_witness(self):
        for v in construct(P)['pairs'].values(): self.assertEqual(v['external_minus_remote_sine_numerator'],v['pair_sum_sine_numerator'])
    def test_rational(self): self.assertTrue(verify(dict(P,A=['1/3','2/7']),construct(dict(P,A=['1/3','2/7']))))
    def test_orientation(self): self.assertTrue(verify(dict(P,A=[1,-2]),construct(dict(P,A=[1,-2]))))
    def test_translation(self): self.assertEqual(construct(P)['pairs'],construct({k:[v[0]+7,v[1]-8] for k,v in P.items()})['pairs'])
    def test_permutation(self):
        for k in ('ABC','ACB','BAC','BCA','CAB','CBA'):
            p=dict(zip('ABC',[P[x] for x in k]));self.assertTrue(verify(p,construct(p)))
    def test_input_binding(self): self.assertFalse(verify(dict(P,A=[2,2]),construct(P)))
    def test_bool_schema(self):
        c=construct(P);c['schema']=True;self.assertFalse(verify(P,c))
    def test_float_schema(self):
        c=construct(P);c['schema']=1.0;self.assertFalse(verify(P,c))
    def test_changed_flag(self):
        c=construct(P);c['pairs']['AB']['external_gt_remote']=1;self.assertFalse(verify(P,c))
    def test_extra(self):
        c=construct(P);c['extra']=0;self.assertFalse(verify(P,c))
    def test_missing(self):
        c=construct(P);del c['input'];self.assertFalse(verify(P,c))
    def test_wrong_number(self):
        c=construct(P);c['pairs']['AB']['pair_sum_sine_numerator']='0';self.assertFalse(verify(P,c))
    def test_bad_json(self): self.assertFalse(verify(P,{'schema':float('nan')}))
    def test_ledger(self): self.assertEqual(ledger('1/2','1/2','3/2')['strict_gap'],'1')
    def test_ledger_scale(self): self.assertTrue(ledger(1,1,3,2)['conclusion'])
    def test_ledger_equality(self): self.assertRaises(ValueError,ledger,1,1,1)
    def test_ledger_false_supplement(self): self.assertRaises(ValueError,ledger,'1/2',1,'3/2')
    def test_ledger_bad_right(self): self.assertRaises(ValueError,ledger,1,1,3,0)
    def test_ledger_bool(self): self.assertRaises(ValueError,ledger,True,1,3,2)
    def test_finite(self): self.assertEqual(run_cases(),{'positive_certificates':120,'pair_checks':360,'negative_inputs':12,'angle_ledgers':63})
for i,p in enumerate(negatives()):
    def test(self,p=p): self.assertRaises(ValueError,construct,p)
    setattr(Checks,f'test_invalid_{i:02}',test)
if __name__=='__main__':unittest.main(verbosity=2)
