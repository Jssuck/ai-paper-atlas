import unittest
from itertools import product
from model import Prop, analyze, holds, find_countermodel, candidate_completions, implication_chain_rows


def q(kind, s, p):
    return Prop(kind, s, p)


class Tests(unittest.TestCase):
    def setUp(self):
        self.major = q('A', 'M', 'P')
        self.minor = q('A', 'S', 'M')
        self.goal = q('A', 'S', 'P')

    def test_01_first(self):
        self.assertEqual(analyze([self.major, self.minor], self.goal)['figure'], 1)
    def test_02_second(self):
        self.assertEqual(analyze([q('E','P','M'), self.minor], q('E','S','P'))['figure'], 2)
    def test_03_third(self):
        self.assertEqual(analyze([self.major,q('A','M','S')],q('I','S','P'))['figure'],3)
    def test_04_swap(self):
        self.assertEqual(analyze([self.major,self.minor], self.goal), analyze([self.minor,self.major],self.goal))
    def test_05_shape_not_validity(self):
        ps=[q('A','P','M'),self.minor]
        self.assertEqual(analyze(ps,self.goal)['figure'],2)
        self.assertEqual(find_countermodel(ps,self.goal)['status'],'countermodel_found')
    def test_06_missing(self):
        self.assertEqual(analyze([self.major],self.goal)['status'],'not_two_premises')
    def test_07_extra(self):
        self.assertEqual(analyze([self.major,self.minor,self.goal],self.goal)['status'],'not_two_premises')
    def test_08_four_terms(self):
        self.assertEqual(analyze([self.major,q('A','S','X')],self.goal)['status'],'not_three_terms')
    def test_09_not_repeated(self):
        self.assertEqual(analyze([self.major,self.goal],self.goal)['status'],'middle_not_repeated')
    def test_10_missing_extreme(self):
        self.assertEqual(analyze([self.major,self.major],self.goal)['status'],'not_three_terms')
    def test_11_fourth_not_first(self):
        self.assertEqual(analyze([q('A','P','M'),q('A','M','S')],self.goal)['status'],'outside_first_three_figures')
    def test_12_identity_extremes(self):
        self.assertEqual(analyze([self.major,self.minor],q('A','S','S'))['status'],'distinct_extremes_required')
    def test_13_quantity_recorded(self):
        self.assertEqual(analyze([self.major,q('I','S','M')],q('I','S','P'))['mood'],'AII')
    def test_14_polarity_recorded(self):
        self.assertEqual(analyze([q('E','M','P'),self.minor],q('E','S','P'))['mood'],'EAE')
    def test_15_barbara(self):
        self.assertEqual(find_countermodel([self.major,self.minor],self.goal)['status'],'no_countermodel_in_bound')
    def test_16_cesare(self):
        self.assertEqual(find_countermodel([q('E','P','M'),self.minor],q('E','S','P'))['status'],'no_countermodel_in_bound')
    def test_17_darii(self):
        self.assertEqual(find_countermodel([self.major,q('I','S','M')],q('I','S','P'))['status'],'no_countermodel_in_bound')
    def test_18_darapti_empty(self):
        r=find_countermodel([self.major,q('A','M','S')],q('I','S','P'))
        self.assertEqual(r['status'],'countermodel_found')
        self.assertEqual(r['model']['M'],[])
    def test_19_darapti_nonempty(self):
        r=find_countermodel([self.major,q('A','M','S')],q('I','S','P'),nonempty=['M'])
        self.assertEqual(r['status'],'no_countermodel_in_bound')
    def test_20_semantics_against_quantification(self):
        u=set(range(3))
        for xm,ym in product(range(8),repeat=2):
            x={i for i in u if xm&(1<<i)}; y={i for i in u if ym&(1<<i)}
            expected={'A':all(i not in x or i in y for i in u),
                      'E':all(i not in x or i not in y for i in u),
                      'I':any(i in x and i in y for i in u),
                      'O':any(i in x and i not in y for i in u)}
            for kind in expected:
                self.assertEqual(holds(q(kind,'X','Y'),{'X':x,'Y':y}),expected[kind])
    def test_21_witness_rechecked(self):
        ps=[q('A','P','M'),self.minor]
        r=find_countermodel(ps,self.goal,nonempty=['S','M','P'])
        m={t:set(v) for t,v in r['model'].items()}
        self.assertTrue(all(holds(p,m) for p in ps)); self.assertFalse(holds(self.goal,m))
    def test_22_completion_label(self):
        r=candidate_completions(self.major,self.goal,[self.minor])
        self.assertEqual(r[0]['status'],'hypothesis_not_fact')
    def test_23_exclude_goal_and_duplicate(self):
        r=candidate_completions(self.major,self.goal,[self.goal,self.major])
        self.assertTrue(all(x['status']=='excluded_goal_or_duplicate' for x in r))
    def test_24_reversed_completion_fails(self):
        r=candidate_completions(self.major,self.goal,[q('A','M','S')])
        self.assertEqual(r[0]['finite_check']['status'],'countermodel_found')
    def test_25_boolean_chain(self):
        rows=implication_chain_rows()
        self.assertEqual(len(rows),8)
        self.assertTrue(all(not r['premises'] or r['conclusion'] for r in rows))
        self.assertEqual(sum(r['premises'] for r in rows),4)
    def test_26_sentence_not_parsed(self):
        with self.assertRaises(TypeError): analyze(['if man exists then animal exists', self.major],self.goal)
    def test_27_bad_kind(self):
        with self.assertRaises(ValueError): q('N','S','P')
    def test_28_bad_terms(self):
        for term in ['', ' S', 4, None]:
            with self.assertRaises(ValueError): q('A',term,'P')
    def test_29_bad_bound(self):
        for bound in [True,0,5,1.5]:
            with self.assertRaises(ValueError): find_countermodel([self.major],self.goal,max_size=bound)
    def test_30_bad_existence(self):
        with self.assertRaises(ValueError): find_countermodel([self.major],self.goal,nonempty=['X'])
    def test_31_renaming(self):
        ps=[q('A','pred','mid'),q('A','sub','mid')]; c=q('A','sub','pred')
        self.assertEqual(analyze(ps,c)['figure'],2)
        self.assertEqual(find_countermodel(ps,c)['status'],'countermodel_found')
    def test_32_empty_universal_not_existential(self):
        m={'X':set(),'Y':set()}
        self.assertTrue(holds(q('A','X','Y'),m)); self.assertTrue(holds(q('E','X','Y'),m))
        self.assertFalse(holds(q('I','X','Y'),m)); self.assertFalse(holds(q('O','X','Y'),m))
    def test_33_two_particulars_wrong_witness(self):
        ps=[q('I','M','P'),q('I','S','M')]
        self.assertEqual(analyze(ps,q('I','S','P'))['figure'],1)
        self.assertEqual(find_countermodel(ps,q('I','S','P'))['status'],'countermodel_found')
    def test_34_two_negatives(self):
        ps=[q('E','M','P'),q('E','S','M')]
        self.assertEqual(find_countermodel(ps,q('E','S','P'))['status'],'countermodel_found')
    def test_35_counts_bound_three(self):
        r=find_countermodel([self.major,self.minor],self.goal)
        self.assertEqual(r['checked'],8+64+512)
        self.assertEqual(r['admissible'],r['checked'])
    def test_36_generator_existence_multiple_candidates(self):
        candidate=q('A','M','S')
        result=candidate_completions(self.major,q('I','S','P'),
            [candidate,candidate],nonempty=(t for t in ['M']))
        self.assertEqual(result[0],result[1])
        self.assertEqual(result[0]['finite_check']['status'],'no_countermodel_in_bound')

if __name__ == '__main__':
    unittest.main(verbosity=2)
