"""Independent review: bit-mask semantics, not author's set/model enumerator."""
import itertools, json, unittest
from model import Statement, Model, Proof, infer, premise, validate, examples
from run_experiment import run


def truth(k,s,p):
    return {'A':s & ~p == 0, 'E':s & p == 0,
            'I':s & p != 0, 'O':s & ~p != 0}[k]


def independent_counts():
    c=dict(models=0,A_conversion_cases=0,E_conversion_cases=0,I_conversion_cases=0,
           A_restriction_cases=0,E_restriction_cases=0,O_nonconversion_countermodels=0,
           particular_subclass_countermodels=0,A_empty_countermodels=0)
    for n in range(4):
        for s,p,d in itertools.product(range(1<<n),repeat=3):
            c['models']+=1
            conditions={
              'A_conversion_cases':truth('A',s,p) and s!=0,
              'E_conversion_cases':truth('E',s,p),
              'I_conversion_cases':truth('I',s,p),
              'A_restriction_cases':truth('A',d,s) and truth('A',s,p),
              'E_restriction_cases':truth('A',d,s) and truth('E',s,p),
              'O_nonconversion_countermodels':truth('O',s,p) and not truth('O',p,s),
              'particular_subclass_countermodels':truth('I',s,p) and truth('A',d,s) and d!=0 and not truth('I',d,p),
              'A_empty_countermodels':truth('A',s,p) and not truth('I',p,s)}
            for key,value in conditions.items(): c[key]+=int(value)
    return c


def leaves(p):
    if p.rule=='premise': return [p.statement]
    return [s for q in p.parents for s in leaves(q)]


class Independent(unittest.TestCase):
    def test_01_all_counts(self):
        self.assertEqual(independent_counts(),run()['counts'])
    def test_02_four_forms(self):
        for n in range(4):
            for s,p in itertools.product(range(1<<n),repeat=2):
                model=Model(n,{'S':[i for i in range(n) if s>>i&1], 'P':[i for i in range(n) if p>>i&1]})
                for k in 'AEIO': self.assertEqual(model.holds(Statement(k,'S','P')),truth(k,s,p))
    def test_03_all_rules_semantics(self):
        P=lambda label,k,s,p:premise(label,k,s,p)
        rules=[infer('convert_E',P('p','E','S','P')),
               infer('convert_I',P('p','I','S','P')),
               infer('convert_A_with_existence',P('p','A','S','P'),P('e','I','S','S')),
               infer('chain_A',P('p','A','S','M'),P('q','A','M','P')),
               infer('restrict_E',P('p','A','S','M'),P('q','E','M','P')),
               infer('Cesare',P('p','E','P','M'),P('q','A','S','M')),
               infer('Darii',P('p','A','M','P'),P('q','I','S','M'))]
        for n in range(4):
            for vals in itertools.product(range(1<<n),repeat=3):
                env=dict(zip(('S','M','P'),vals))
                ev=lambda s:truth(s.mood,env[s.subject],env[s.predicate])
                for proof in rules:
                    if all(ev(s) for s in leaves(proof)): self.assertTrue(ev(proof.statement))
    def test_04_given_trees(self):
        for vals in itertools.product(range(4),repeat=5):
            env=dict(zip('ABCDE',vals));ev=lambda s:truth(s.mood,env[s.subject],env[s.predicate])
            for proof in examples().values():
                if all(ev(s) for s in leaves(proof)): self.assertTrue(ev(proof.statement))
    def test_05_dependency_and_label_boundary(self):
        e=examples()
        self.assertEqual(e['second_original'].dependencies(),{'p1:B disjoint A','p2:C subset A'})
        self.assertEqual(e['second_submiddle'].dependencies(),{'p1:B disjoint A','s:E subset A'})
        self.assertEqual(e['particular_original'].dependencies(),{'d1:B subset A','d2:some C is B'})
        self.assertEqual(e['particular_submiddle'].dependencies(),{'d1:B subset A','t:D subset B'})
        # Labels are caller metadata: repeated IDs are not proof of minimum support.
        p=premise('x','A','S','M');q=premise('x','A','M','P')
        self.assertEqual(infer('chain_A',p,q).dependencies(),{'x'})
    def test_06_countermodels(self):
        self.assertTrue(truth('O',3,1));self.assertFalse(truth('O',1,3))
        self.assertTrue(truth('I',3,1) and truth('A',2,3));self.assertFalse(truth('I',2,1))
        self.assertTrue(truth('A',0,1));self.assertFalse(truth('I',1,0))
        # Original second-figure assumptions are individually indispensable relative to the pair.
        self.assertTrue(truth('A',1,1));self.assertFalse(truth('E',1,1))
        self.assertTrue(truth('E',1,2));self.assertFalse(truth('E',2,2))
    def test_07_bad_extensions(self):
        for n,t in [(True,{}),(-1,{}),(2,{'S':[True]}),(2,{'S':[2]}),(2,{'S':None}),(0,{'':[ ]})]:
            with self.assertRaises(ValueError):Model(n,t)
        with self.assertRaises(ValueError):Model(1,{'S':[]}).holds(Statement('A','S','missing'))
    def test_08_bad_proofs(self):
        p=premise('p','E','S','P')
        for tree in [Proof(Statement('I','P','S'),'convert_E',(p,)),Proof(Statement('E','P','S'),'convert_E',[p]),Proof(Statement('E','P','S'),'convert_E',(p,),'x')]:
            with self.assertRaises(ValueError):validate(tree)
    def test_09_reject_unlicensed_rules(self):
        p=premise('p','A','S','P');q=premise('q','I','P','P')
        with self.assertRaises(ValueError):infer('convert_A_with_existence',p,q)
        with self.assertRaises(ValueError):infer('convert_O',premise('o','O','S','P'))
        with self.assertRaises(ValueError):infer('chain_A',premise('d','A','D','S'),premise('i','I','S','P'))
    def test_10_inclusion_and_existence_restoration(self):
        for a,b,c,d in itertools.product(range(8),repeat=4):
            if truth('A',b,a) and truth('I',d,b):self.assertTrue(truth('I',d,a))
            if truth('A',b,c) and truth('A',c,a) and truth('A',d,b):self.assertTrue(truth('A',d,a))

if __name__=='__main__':
    print(json.dumps({'independent_counts':independent_counts(),'rule_instances_checked':585*7,
                      'given_tree_instances':1024*4,'four_set_cases':8**4},sort_keys=True),flush=True)
    unittest.main(verbosity=2)
