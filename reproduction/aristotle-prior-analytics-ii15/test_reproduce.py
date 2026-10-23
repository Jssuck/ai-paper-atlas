import unittest
import reproduce as r

class Checks(unittest.TestCase):
    def test_model_counts(self):
        self.assertEqual(len(list(r.models())),255)
        self.assertEqual(sum(all(m[t] for t in 'PMS') for m in r.models()),218)
    def test_invalid_inputs(self):
        for args in [('X','P','S'),('U','PP','S'),('', 'P','S'),(None,'P','S')]:
            with self.assertRaises(ValueError):r.proposition(*args)
        for args in [(True,'UE'),(4,'UE'),(2,'UX'),(2,None)]:
            with self.assertRaises(ValueError):r.premises(*args)
        with self.assertRaises(ValueError):r.assess((),('U','P','S'),nonempty=('X',))
        with self.assertRaises(ValueError):r.formal_conclusions(2,'UE',None)
    def test_assumption_generator(self):
        ps=(('U','P','S'),('O','P','S'))
        self.assertEqual(r.assess(ps,('E','P','S')),r.assess((p for p in ps),('E','P','S')))
    def test_complements(self):
        for m in r.models():
            self.assertNotEqual(r.holds(('U','P','S'),m),r.holds(('O','P','S'),m))
            self.assertNotEqual(r.holds(('E','P','S'),m),r.holds(('I','P','S'),m))
    def test_standard_rules(self):
        x=r.run()['standard_rule_checks'];self.assertEqual(len(x),14)
        self.assertTrue(all(row['premise_models']>0 for row in x))
    def test_route_count(self):
        self.assertEqual(len(r.routes()),12)
        self.assertTrue(all(x['conclusion'][0] in 'EO' for x in r.routes()))
    def test_route_sound_distinct(self):
        self.assertTrue(all(x['distinct_terms']['semantic_entailment'] for x in r.routes()))
        self.assertTrue(all(x['distinct_terms']['premise_models']>0 for x in r.routes()))
    def test_opposed_nonempty(self):
        for x in r.routes():
            self.assertEqual(x['identified_extremes']['premise_models'],0)
            self.assertEqual(x['identified_extremes']['conclusion_false_in_background'],x['identified_extremes']['background_models'])
    def test_first_figure_slots(self):
        for pair in r.PAIRS:
            p,q=r.premises(1,pair)
            collapse=lambda t:'P' if t=='S' else t
            self.assertNotEqual(tuple(map(collapse,p[1:])),tuple(map(collapse,q[1:])))
    def test_io_not_opposed(self):
        m={k:set(v) for k,v in r.run()['particulars_coexist'].items()}
        self.assertTrue(r.holds(('I','P','S'),m) and r.holds(('O','P','S'),m))
        for f in (1,2,3):self.assertEqual(r.formal_conclusions(f,'IO',('P','M','S')),())
    def test_existential_gap(self):
        for x in r.routes():
            if x['figure']==3 and x['pair'] in ('UE','EU'):
                self.assertFalse(x['empty_terms_allowed']['semantic_entailment'])
                self.assertEqual(r.formal_conclusions(3,'EU'),())
    def test_empty_contraries(self):
        for x in r.routes():
            if x['figure']==2 and x['pair'] in ('UE','EU'):
                self.assertEqual(x['empty_terms_allowed']['premise_models'],3)
                self.assertTrue(x['empty_terms_allowed']['semantic_entailment'])
    def test_not_explosion_rule(self):
        e=r.run()['vacuous_entailment_not_a_formal_rule'];self.assertTrue(e['vacuous'])
        self.assertTrue(e['semantic_entailment'])
        self.assertNotIn(('U','P','S'),r.formal_conclusions(2,'UO',('P','M','S')))
    def test_subset_boundary(self):
        a,b,c=r.subset_examples()
        self.assertGreater(a['premise_models'],0);self.assertGreater(b['premise_models'],0)
        self.assertEqual(c['premise_models'],0)
        self.assertEqual(c['background_models'],c['conclusion_false_in_background'])
    def test_swapped_direction(self):
        x=next(x for x in r.routes() if x['figure']==2 and x['pair']=='OU')
        self.assertEqual(x['conclusion'],('O','S','P'));self.assertTrue(x['exchanged_extremes'])

if __name__=='__main__':unittest.main(verbosity=2)
