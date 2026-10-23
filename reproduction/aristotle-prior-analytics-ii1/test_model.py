import unittest
from model import Statement as S, Model, Proof, models, premise, infer, validate, examples
from run_experiment import run


class Tests(unittest.TestCase):
    def test_four_forms(self):
        m = Model(2, {'S': {0,1}, 'P': {0}})
        self.assertEqual([m.holds(S(k,'S','P')) for k in 'AEIO'], [False,False,True,True])
    def test_empty(self):
        m = Model(0, {'S': set(), 'P': set()})
        self.assertEqual([m.holds(S(k,'S','P')) for k in 'AEIO'], [True,True,False,False])
    def test_bad_universe(self):
        for n in [-1, True, 1.5, '2']:
            with self.assertRaises(ValueError): Model(n,{})
    def test_bad_extensions(self):
        for values in [{2}, {-1}, {True}, [1.0], 7]:
            with self.assertRaises(ValueError): Model(2,{'S':values})
    def test_unknown_terms(self):
        with self.assertRaises(ValueError): Model(0,{}).holds(S('A','S','P'))
    def test_bad_statement(self):
        for data in [('Q','S','P'),('A','','P'),('A','S',None)]:
            with self.assertRaises(ValueError): S(*data)
    def test_generator_extensions(self):
        self.assertEqual(Model(2,{'S':(i for i in [0,1])}).extension('S'),{0,1})
    def test_models_count_and_duplicates(self):
        self.assertEqual(len(list(models(2,('S','P')))),16)
        with self.assertRaises(ValueError): list(models(2,('S','S')))
    def test_E_I_conversion(self):
        for k in 'EI':
            self.assertEqual(infer('convert_'+k,premise('p',k,'S','P')).statement,S(k,'P','S'))
    def test_A_conversion_needs_existence(self):
        p=premise('p','A','S','P')
        with self.assertRaises(ValueError): infer('convert_A_with_existence',p)
        with self.assertRaises(ValueError): infer('convert_A_with_existence',p,premise('wrong','I','P','P'))
        self.assertEqual(infer('convert_A_with_existence',p,premise('exists','I','S','S')).statement,S('I','P','S'))
    def test_O_conversion_rejected(self):
        with self.assertRaises(ValueError): infer('convert_O',premise('p','O','S','P'))
    def test_chain_and_negative_restriction(self):
        sub=premise('sub','A','D','S')
        self.assertEqual(infer('chain_A',sub,premise('p','A','S','P')).statement,S('A','D','P'))
        self.assertEqual(infer('restrict_E',sub,premise('p','E','S','P')).statement,S('E','D','P'))
    def test_no_arbitrary_particular_restriction(self):
        with self.assertRaises(ValueError): infer('chain_A',premise('sub','A','D','S'),premise('p','I','S','P'))
    def test_forged_proof(self):
        p=premise('p','E','S','P')
        with self.assertRaises(ValueError): validate(Proof(S('I','P','S'),'convert_E',(p,)))
        with self.assertRaises(ValueError): validate(Proof(S('E','P','S'),'convert_E',(p,),'extra'))
    def test_dependencies(self):
        x=examples()
        self.assertEqual(x['second_original'].dependencies(), {'p1:B disjoint A','p2:C subset A'})
        self.assertEqual(x['second_submiddle'].dependencies(), {'p1:B disjoint A','s:E subset A'})
        self.assertEqual(x['particular_submiddle'].dependencies(), {'d1:B subset A','t:D subset B'})
    def test_nonempty_O_countermodel(self):
        m=Model(2,{'S':{0,1},'P':{0}})
        self.assertTrue(m.holds(S('O','S','P')))
        self.assertFalse(m.holds(S('O','P','S')))
    def test_example_semantics(self):
        def leaves(p):
            if p.rule == 'premise': return [p.statement]
            return [s for q in p.parents for s in leaves(q)]
        for m in models(2,('A','B','C','D','E')):
            for p in examples().values():
                if all(m.holds(s) for s in leaves(p)):
                    self.assertTrue(m.holds(p.statement))
    def test_finite_experiment(self):
        x=run()
        self.assertEqual(x['counts']['models'],585)
        self.assertEqual(x['failures'],0)
        for k in ['O_nonconversion_countermodels','particular_subclass_countermodels','A_empty_countermodels']:
            self.assertGreater(x['counts'][k],0)


if __name__ == '__main__': unittest.main(verbosity=2)
