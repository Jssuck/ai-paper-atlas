import unittest
from modal import Model, categorical, evaluate, models, satisfies, classify, fixed_shared_witness, MODES

class ModalTests(unittest.TestCase):
    def setUp(self): self.m=Model(2,((3,3,1),(1,2,0)))
    def test_actual(self): self.assertEqual(self.m.actual(0),3)
    def test_stable(self): self.assertEqual(self.m.stable(0),1)
    def test_possible(self): self.assertEqual(self.m.possible(1),3)
    def test_world_count(self): self.assertEqual(len(list(models())),4096)
    def test_one_object_count(self): self.assertEqual(len(list(models(1))),64)
    def test_one_world_collapse(self):
        for m in models(2,1):
            for q in 'AEIO':
                for s in range(3):
                    for p in range(3):
                        self.assertEqual(evaluate(m,q,s,p),evaluate(m,q,s,p,'anchored'))
                        self.assertEqual(evaluate(m,q,s,p),evaluate(m,q,s,p,'sentence'))
    def test_empty_universal(self):
        self.assertTrue(categorical('A',0,0)); self.assertTrue(categorical('E',0,0))
    def test_empty_particular(self):
        self.assertFalse(categorical('I',0,0)); self.assertFalse(categorical('O',0,0))
    def test_aeio_values(self):
        self.assertTrue(categorical('A',1,3));self.assertTrue(categorical('E',1,2))
        self.assertTrue(categorical('I',3,2));self.assertTrue(categorical('O',3,1))
    def test_necessity_implies_actual(self):
        for m in models():
            for q in 'AEIO':
                for sem in ('anchored','sentence'):
                    if evaluate(m,q,1,0,sem): self.assertTrue(evaluate(m,q,1,0))
    def test_actual_middle_required(self):
        self.assertFalse(satisfies(Model(1,((1,1,0),(1,1,0))),'Darapti','major','anchored'))
    def test_inverse_not_forward(self):
        m=Model(1,((1,1,1),(0,1,0)))
        self.assertTrue(satisfies(m,'Darapti','minor','anchored'))
        self.assertTrue(evaluate(m,'I',0,1,'anchored'))
        self.assertFalse(evaluate(m,'I',1,0,'anchored'))
    def test_inverse_general_route(self):
        for m in models():
            if satisfies(m,'Darapti','minor','anchored'): self.assertTrue(evaluate(m,'I',0,1,'anchored'))
    def test_stability_bridge(self):
        for m in models():
            if satisfies(m,'Darapti','minor','anchored') and m.actual(2)&m.stable(0):
                self.assertTrue(evaluate(m,'I',1,0,'anchored'))
    def test_symmetric_shared_witness(self):
        for m in models(): self.assertEqual(fixed_shared_witness(m,0,1),fixed_shared_witness(m,1,0))
    def test_shared_stronger_than_anchored(self):
        for m in models():
            if fixed_shared_witness(m,0,1):
                self.assertTrue(evaluate(m,'I',0,1,'anchored'));self.assertTrue(evaluate(m,'I',1,0,'anchored'))
    def test_sentence_witness_switch(self):
        m=Model(2,((1,1,1),(2,2,2)))
        self.assertTrue(evaluate(m,'I',1,0,'sentence'))
        self.assertFalse(fixed_shared_witness(m,1,0))
    def test_one_object_countermodels(self):
        for sem in ('anchored','sentence'):
            for mode in MODES:
                for side in ('major','minor'):
                    if sem=='anchored' and side=='major':continue
                    self.assertTrue(any(satisfies(m,mode,side,sem) and not evaluate(m,MODES[mode][2],1,0,sem) for m in models(1)))
    def test_classification(self):
        data=classify()
        self.assertEqual(len(data['rows']),24)
        for r in data['rows']:
            self.assertEqual(r['finite_valid'],r['semantics']=='anchored' and r['necessary']=='major')
            self.assertGreater(r['premise_models'],0)
    def test_exact_failure_counts(self):
        rows=classify()['rows']
        self.assertEqual([r['countermodels'] for r in rows[:12]],[0,116,0,116,0,132,0,156,0,132,0,156])
    def test_anchored_major_general_finite(self):
        for m in models():
            for name,(_,_,q) in MODES.items():
                if satisfies(m,name,'major','anchored'): self.assertTrue(evaluate(m,q,1,0,'anchored'))
    def test_plain_all_six_modes(self):
        for m in models(2,1):
            if not m.actual(2): continue
            for name,(a,b,c) in MODES.items():
                if evaluate(m,a,2,0) and evaluate(m,b,2,1):self.assertTrue(evaluate(m,c,1,0))
    def test_model_reject_bad_domain(self):
        for n in (0,-1,True,1.0,'2'):
            with self.assertRaises(ValueError):Model(n,((0,0,0),))
    def test_model_reject_bad_worlds(self):
        for ws in ((),[],[[0,0,0]],((0,0),),((0,0,0,0),)):
            with self.assertRaises(ValueError):Model(1,ws)
    def test_model_reject_bad_masks(self):
        for v in (-1,2,True,0.0,'0'):
            with self.assertRaises(ValueError):Model(1,((v,0,0),))
    def test_invalid_terms(self):
        for t in (-1,3,True,'0',0.0):
            with self.assertRaises(ValueError):evaluate(self.m,'A',t,0)
            with self.assertRaises(ValueError):self.m.stable(t)
    def test_invalid_kind(self):
        with self.assertRaises(ValueError):evaluate(self.m,'X',0,1)
        with self.assertRaises(ValueError):categorical('X',0,1)
    def test_invalid_semantics(self):
        with self.assertRaises(ValueError):evaluate(self.m,'A',0,1,'unknown')
    def test_invalid_mode_and_side(self):
        with self.assertRaises(ValueError):satisfies(self.m,'x','major','anchored')
        with self.assertRaises(ValueError):satisfies(self.m,'Darapti','x','anchored')
        with self.assertRaises(ValueError):satisfies(self.m,'Darapti','major','actual')
    def test_invalid_model(self):
        with self.assertRaises(TypeError):evaluate(None,'A',0,1)
    def test_invalid_generator_sizes(self):
        for a,b in ((0,2),(2,0),(True,2),(2,False)):
            with self.assertRaises(ValueError):list(models(a,b))
    def test_invalid_categorical_masks(self):
        for s,p in ((-1,0),(True,0),(0,1.0)):
            with self.assertRaises(ValueError):categorical('A',s,p)

if __name__=='__main__':unittest.main(verbosity=2)
