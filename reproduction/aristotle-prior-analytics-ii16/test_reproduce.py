import unittest
from reproduce import Rule, closure, supports, semantic_consequences, examples, exhaustive

class Tests(unittest.TestCase):
    def test_direct_cycle(self):
        self.assertEqual(closure([Rule(('T',),'T')],[]),frozenset())
    def test_long_cycle(self):
        rr=[Rule(('A',),'B'),Rule(('B',),'C'),Rule(('C',),'A')]
        self.assertEqual(closure(rr,[]),frozenset())
        self.assertEqual(closure(rr,['A']),frozenset('ABC'))
    def test_conjunction(self):
        rr=[Rule(('A','B'),'C')]
        self.assertNotIn('C',closure(rr,['A']))
        self.assertIn('C',closure(rr,['A','B']))
    def test_no_reverse(self):
        self.assertNotIn('A',closure([Rule(('A',),'B')],['B']))
    def test_minimal_supports(self):
        rr=[Rule(('A',),'T'),Rule(('B','C'),'T')]
        self.assertEqual(supports(rr,'T',['A','B','C']), (frozenset('A'),frozenset('BC')))
    def test_generator_rules(self):
        rr=[Rule(('A',),'T'),Rule(('B',),'T')]
        self.assertEqual(supports(iter(rr),'T',['A','B']),supports(rr,'T',['A','B']))
    def test_generator_seeds(self):
        self.assertIn('T',closure([Rule(('A',),'T')],iter(['A'])))
    def test_identity_and_extensivity(self):
        self.assertEqual(closure([],['A']),frozenset('A'))
    def test_idempotence(self):
        rr=[Rule(('A',),'B'),Rule(('B',),'C')]
        c=closure(rr,['A']); self.assertEqual(c,closure(rr,c))
    def test_bad_rule(self):
        for args in [((),'A'),(('A','A'),'B'),(('A',),''),(['A'],'B'),((1,),'B')]:
            with self.assertRaises(ValueError): Rule(*args)
    def test_bad_facts(self):
        for value in ['A',[1],['']]:
            with self.assertRaises(ValueError): closure([],value)
    def test_missing_universe(self):
        with self.assertRaises(ValueError): semantic_consequences([Rule(('A',),'B')],[],['A'])
    def test_examples(self):
        ex=examples(); self.assertEqual(len(ex),12)
        self.assertEqual([x['target_reached'] for x in ex],[False,False,True,True,False,True,False,False,True,False,True,False])
    def test_exhaustive(self):
        self.assertEqual(exhaustive()['closure_semantic_comparisons'],4096)
    def test_semantic_empty(self):
        self.assertEqual(semantic_consequences([],[],[]),frozenset())

if __name__=='__main__': unittest.main(verbosity=2)
