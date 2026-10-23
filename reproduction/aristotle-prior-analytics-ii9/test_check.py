import unittest
import check as c

class Checks(unittest.TestCase):
    def test_population(self):
        self.assertEqual([sum(1 for _ in c.models(p)) for p in c.POLICIES],[255,240,218])
    def test_invalid_inputs(self):
        for mask in (0,256,-1,True,'1'):
            with self.assertRaises(ValueError): c.model(mask)
        with self.assertRaises(ValueError): c.Prop('Q','A','B')
        with self.assertRaises(ValueError): list(c.models('unknown'))
    def test_exact_negations(self):
        for _,m in c.models('empty_allowed'):
            for pred in 'ABC':
                for sub in 'ABC':
                    self.assertNotEqual(c.holds(c.P('A',pred,sub),m),c.holds(c.P('O',pred,sub),m))
                    self.assertNotEqual(c.holds(c.P('E',pred,sub),m),c.holds(c.P('I',pred,sub),m))
    def test_four_original_moods(self):
        for p in c.POLICIES:
            for a,b,z in c.MOODS.values():
                for _,m in c.models(p):
                    if c.holds(a,m) and c.holds(b,m): self.assertTrue(c.holds(z,m))
    def test_all_contradictory_refutations(self):
        for p in c.POLICIES:
            for case in c.cases():
                if case['mode']=='contradictory':
                    row=c.evaluate_case(case,p)
                    self.assertGreater(row['background_count'],0)
                    self.assertEqual(row['refutation_countermodel_count'],0)
                    self.assertEqual(row['result_countermodel_count'],0)
    def test_universal_contrary_nonempty(self):
        for p in ('C_nonempty','all_nonempty'):
            for case in c.cases():
                if case['mode']=='contrary' and case['mood'] in ('Camestres','Cesare'):
                    row=c.evaluate_case(case,p)
                    self.assertEqual(row['result_countermodel_count'],0)
                    self.assertEqual(row['refutation_countermodel_count'],0)
    def test_universal_contrary_empty_c(self):
        for case in c.cases():
            if case['mode']=='contrary' and case['mood'] in ('Camestres','Cesare'):
                row=c.evaluate_case(case,'empty_allowed')
                self.assertGreater(row['refutation_countermodel_count'],0)
                self.assertEqual(row['first_refutation_countermodel']['sets']['C'],[])
                if case['retain']=='major': self.assertEqual(row['result_countermodel_count'],0)
                else: self.assertGreater(row['result_countermodel_count'],0)
    def test_particular_contrary_does_not_refute(self):
        for p in c.POLICIES:
            for case in c.cases():
                if case['mode']=='contrary' and case['mood'] in ('Festino','Baroco'):
                    row=c.evaluate_case(case,p)
                    self.assertGreater(row['refutation_countermodel_count'],0)
                    if case['retain']=='major': self.assertEqual(row['result_countermodel_count'],0)
                    else: self.assertEqual(row['all_valid_target_pair_forms'],[])
    def test_some_and_some_not_can_both_hold(self):
        m={'A':{1},'B':{0},'C':{0,1}}
        self.assertTrue(c.holds(c.P('I','A','C'),m))
        self.assertTrue(c.holds(c.P('O','A','C'),m))
    def test_all_rows_and_witnesses_replay(self):
        for p in c.POLICIES:
            rows=c.report()['policies'][p]['cases']
            self.assertEqual(len(rows),16)
            for case,row in zip(c.cases(),rows):
                w=row['first_refutation_countermodel']
                if w:
                    m={k:set(v) for k,v in w['sets'].items()}
                    self.assertTrue(c.holds(case['retained'],m))
                    self.assertTrue(c.holds(case['replacement'],m))
                    self.assertTrue(c.holds(case['target'],m))

if __name__=='__main__': unittest.main(verbosity=2)
