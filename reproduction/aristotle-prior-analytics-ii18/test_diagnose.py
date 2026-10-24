import unittest
from diagnose import STEPS, NODES, diagnose, report, prepare

class DiagnosisTests(unittest.TestCase):
    def vals(self, **changes):
        return {n: changes.get(n, True) for n in NODES}
    def test_single_false_leaf(self):
        r=diagnose(STEPS,self.vals(A=False,C=False,D=False),'C')
        self.assertEqual(r['false_leaf_paths'],[['C','A','D']])
    def test_multiple_sources(self):
        r=diagnose(STEPS,self.vals(A=False,B=False,C=False,D=False,F=False),'C')
        self.assertEqual(r['false_leaves'],['D','F'])
    def test_true_conclusion_false_premise(self):
        r=diagnose(STEPS,self.vals(D=False),'C')
        self.assertTrue(r['valuation_condition_holds'])
        self.assertEqual(r['false_leaves'],[])
    def test_invalid_inference_not_misdiagnosed(self):
        r=diagnose(STEPS,self.vals(C=False),'C')
        self.assertEqual(r['violating_steps'],['C'])
        self.assertEqual(r['false_leaves'],[])
    def test_false_target_leaf(self):
        self.assertEqual(diagnose([],{'x':False},'x')['false_leaf_paths'],[['x']])
    def test_shared_dag_paths(self):
        steps=(('a',('d','e')),('b',('d','f')),('c',('a','b')))
        vals={'a':False,'b':False,'c':False,'d':False,'e':True,'f':True}
        r=diagnose(steps,vals,'c')
        self.assertEqual(r['false_leaves'],['d'])
        self.assertEqual(len(r['false_leaf_paths']),2)
    def test_unrelated_invalid_step_is_not_target_source(self):
        steps=STEPS+(('X',('Y','Z')),)
        vals=self.vals(A=False,C=False,D=False)|{'X':False,'Y':True,'Z':True}
        self.assertTrue(diagnose(steps,vals,'C')['valuation_condition_holds'])
    def test_generator_steps_supported(self):
        self.assertEqual(diagnose(iter(STEPS),self.vals(A=False,C=False,D=False),'C'),
                         diagnose(STEPS,self.vals(A=False,C=False,D=False),'C'))
    def test_cycles_rejected(self):
        with self.assertRaises(ValueError):
            diagnose((('a',('b','c')),('b',('a','c'))),{'a':False,'b':False,'c':True},'a')
    def test_duplicate_output_rejected(self):
        with self.assertRaises(ValueError):
            diagnose(STEPS+STEPS[:1],self.vals(),'C')
    def test_missing_value_rejected(self):
        with self.assertRaises(ValueError):
            diagnose(STEPS,{'C':False},'C')
    def test_non_boolean_rejected(self):
        with self.assertRaises(ValueError):
            diagnose(STEPS,self.vals(C=0),'C')
    def test_duplicate_or_single_premises_rejected(self):
        for parents in [('A',),('A','A')]:
            with self.assertRaises(ValueError):
                diagnose((('C',parents),),self.vals(),'C')
    def test_unknown_target_rejected(self):
        with self.assertRaises(ValueError):
            diagnose(STEPS,self.vals(),'X')
    def test_all_records_and_paths(self):
        r=report()
        self.assertEqual(r['total_valuations'],128)
        for row in r['records']:
            if row['valuation_condition_holds'] and not row['target_value']:
                self.assertGreater(len(row['false_leaves']),0)
                for path in row['false_leaf_paths']:
                    self.assertEqual(path[0],'C')
                    self.assertIn(path[-1],'DEFG')
                    self.assertTrue(all(not row['values'][n] for n in path))
                    for child,parent in zip(path,path[1:]):
                        self.assertIn(parent,dict(STEPS)[child])

if __name__=='__main__':
    unittest.main(verbosity=2)
