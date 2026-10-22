import unittest
from division import FiniteModel, Step

class Tests(unittest.TestCase):
    def setUp(self):
        self.m = FiniteModel({0,1,2}, {'A':{0,1,2},'B':{0,1},'C':{2},'D':{0},'E':{0},'F':{1},'empty':set()})
    def test_cover(self): self.assertTrue(self.m.division_report('A','B','C','D')['premises'])
    def test_pointwise_not_uniform(self):
        r=self.m.division_report('A','B','C','A');self.assertTrue(r['pointwise_disjunction']);self.assertFalse(r['uniform_disjunction'])
    def test_no_certificate(self):
        with self.assertRaises(ValueError): self.m.select_branch('A','B','C','D','left')
    def test_left(self): self.assertEqual(self.m.select_branch('A','B','C','D','left',exclude_other=True),'B')
    def test_right(self): self.assertEqual(self.m.select_branch('A','B','C','C','right',exclude_other=True),'C')
    def test_false_exclusion(self):
        with self.assertRaises(ValueError): self.m.select_branch('A','B','C','A','left',exclude_other=True)
    def test_bad_cover(self):
        with self.assertRaises(ValueError): self.m.select_branch('A','E','F','D','left',exclude_other=True)
    def test_bad_membership(self):
        with self.assertRaises(ValueError): self.m.select_branch('B','E','F','C','left',exclude_other=True)
    def test_path(self): self.assertEqual(self.m.follow_path('D',[Step('A','B','C','left',True),Step('B','E','F','left',True)]),('B','E'))
    def test_path_missing_second_evidence(self):
        with self.assertRaises(ValueError): self.m.follow_path('D',[Step('A','B','C','left',True),Step('B','E','F','left')])
    def test_disconnected(self):
        with self.assertRaises(ValueError): self.m.follow_path('D',[Step('A','B','C','left',True),Step('A','B','C','left',True)])
    def test_empty_path(self):
        with self.assertRaises(ValueError): self.m.follow_path('D',[])
    def test_wrong_step(self):
        with self.assertRaises(TypeError): self.m.follow_path('D',[{}])
    def test_definition_only_necessary(self): self.assertEqual(self.m.definition_report('D','B'),{'necessary':True,'sufficient':False,'coextensive':False})
    def test_definition_equal(self): self.assertTrue(self.m.definition_report('D','E')['coextensive'])
    def test_empty_target(self):
        r=self.m.division_report('A','B','C','empty');self.assertTrue(r['all_left']);self.assertTrue(r['all_right']);self.assertFalse(r['target_nonempty'])
    def test_overlap(self):
        m=FiniteModel({0,1},{'A':{0,1},'B':{0,1},'C':{1},'D':{0}})
        self.assertEqual(m.select_branch('A','B','C','D','left',exclude_other=True),'B')
    def test_unknown(self):
        with self.assertRaises(ValueError): self.m.term('missing')
    def test_bool_member(self):
        with self.assertRaises(ValueError): FiniteModel({False},{'A':set()})
    def test_outside(self):
        with self.assertRaises(ValueError): FiniteModel({0},{'A':{1}})
    def test_empty_universe(self):
        with self.assertRaises(ValueError): FiniteModel(set(),{'A':set()})
    def test_list_members(self):
        with self.assertRaises(TypeError): FiniteModel({0},{'A':[0]})
    def test_bad_name(self):
        with self.assertRaises(ValueError): FiniteModel({0},{' A':set()})
    def test_nonbool_evidence(self):
        with self.assertRaises(TypeError): self.m.select_branch('A','B','C','D','left',exclude_other=1)
    def test_bad_side(self):
        with self.assertRaises(ValueError): self.m.select_branch('A','B','C','D','LEFT',exclude_other=True)
    def test_copy(self):
        v={0};t={'A':v};m=FiniteModel({0},t);v.clear();t.clear();self.assertEqual(m.term('A'),frozenset({0}))
    def test_negative_member(self):
        with self.assertRaises(ValueError): FiniteModel({-1},{'A':set()})
    def test_wrong_term_name_type(self):
        with self.assertRaises(TypeError): self.m.term(1)
    def test_empty_terms(self):
        with self.assertRaises(TypeError): FiniteModel({0},{})
    def test_bad_path_container(self):
        with self.assertRaises(ValueError): self.m.follow_path('D',iter([]))
    def test_overlap_exclusion_not_necessary_for_truth(self):
        m=FiniteModel({0},{'A':{0},'B':{0},'C':{0},'D':{0}})
        self.assertTrue(m.division_report('A','B','C','D')['all_left'])
        with self.assertRaises(ValueError): m.select_branch('A','B','C','D','left',exclude_other=True)
    def test_child_outside_parent_allowed_for_cover(self):
        r=self.m.division_report('D','B','C','D')
        self.assertTrue(r['premises']);self.assertFalse(r['children_within_parent'])
    def test_mapping_immutable(self):
        with self.assertRaises(TypeError): self.m.terms['A']=frozenset()

if __name__ == '__main__': unittest.main(verbosity=2)
