import unittest
from model import derive,normalize,typed_rules,minimal_supports,check_certificate,shares_root,examples

class ModelTests(unittest.TestCase):
    def test_empty(self): self.assertEqual(derive([],[]),(frozenset(),()))
    def test_seeds_preserved(self): self.assertEqual(derive(['p'],[])[0],{'p'})
    def test_chain(self): self.assertEqual(derive(['p'],[(('q',),'r'),(('p',),'q')])[0],set('pqr'))
    def test_conjunction_requires_both(self): self.assertNotIn('r',derive(['p'],[(('p','q'),'r')])[0])
    def test_conjunction_fires(self): self.assertIn('r',derive(['p','q'],[(('p','q'),'r')])[0])
    def test_cycle_no_seed(self): self.assertEqual(derive([],[(('p',),'q'),(('q',),'p')])[0],set())
    def test_cycle_seed(self): self.assertEqual(derive(['p'],[(('p',),'q'),(('q',),'p')])[0],set('pq'))
    def test_empty_body_rejected(self): self.assertRaises(ValueError,normalize,[((),'p')])
    def test_bad_atom_rejected(self): self.assertRaises(ValueError,normalize,[((1,),'p')])
    def test_rule_dedup(self): self.assertEqual(len(normalize([(('p',),'q'),(('p',),'q')])),1)
    def test_certificate(self):
        r=[(('p',),'q'),(('q',),'r')]; c=derive(['p'],r)[1]
        self.assertTrue(check_certificate(['p'],r,c,'r'))
        self.assertFalse(check_certificate(['p'],r,c[::-1],'r'))
    def test_forged_step(self): self.assertFalse(check_certificate(['p'],[],[(('p',),'q')],'q'))
    def test_duplicate_step(self): self.assertFalse(check_certificate(['p'],[(('p',),'q')],[(('p',),'q'),(('p',),'q')],'q'))
    def test_missing_target(self): self.assertFalse(check_certificate(['p'],[],[],'r'))
    def test_same_type(self): self.assertEqual(len(typed_rules([(('p',),'q')],{'p':'N','q':'N'})[0]),1)
    def test_cross_type(self): self.assertEqual(len(typed_rules([(('p',),'q')],{'p':'N','q':'G'})[1]),1)
    def test_explicit_bridge(self): self.assertEqual(len(typed_rules([(('p',),'q')],{'p':'N','q':'G'},[(('p',),'q')])[0]),1)
    def test_unknown_type_even_bridge(self): self.assertEqual(len(typed_rules([(('p',),'q')],{'p':'N'},[(('p',),'q')])[1]),1)
    def test_alternative_minimal_supports(self): self.assertEqual(set(minimal_supports('r',{'p','q'},[(('p',),'r'),(('q',),'r')])),{frozenset('p'),frozenset('q')})
    def test_support_no_self_justification(self): self.assertEqual(minimal_supports('r',{'p'},[(('r',),'r')]),())
    def test_nontransitive_overlap(self):
        self.assertTrue(shares_root({'p'},{'p','q'}));self.assertTrue(shares_root({'p','q'},{'q'}));self.assertFalse(shares_root({'p'},{'q'}))
    def test_teaching_examples(self):
        e=examples();self.assertFalse(e['without_bridge_w']);self.assertTrue(e['with_declared_bridge_w']);self.assertFalse(e['same_label_without_rule']);self.assertEqual(e['shared_generic_rule_does_not_supply_roots'],[])

if __name__=='__main__': unittest.main()
