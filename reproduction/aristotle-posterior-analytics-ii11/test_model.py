import unittest
from itertools import product
from model import *

class Checks(unittest.TestCase):
    def test_01_chain(self): self.assertTrue(chain({1,2},{1},{1})['c_in_a'])
    def test_02_empty(self): self.assertTrue(all(chain(set(),set(),set()).values()))
    def test_03_missing_major(self): self.assertEqual(chain(set(),{1},{1}),dict(c_in_b=True,b_in_a=False,c_in_a=False))
    def test_04_missing_minor(self): self.assertEqual(chain(set(),set(),{1}),dict(c_in_b=False,b_in_a=True,c_in_a=False))
    def test_05_truth_not_premises(self): self.assertFalse(chain({1},set(),{1})['c_in_b'])
    def test_06_domain(self): self.assertRaises(ValueError,element_oracle,{1},set(),set(),set())
    def test_07_oracle(self): self.assertEqual(element_oracle({1},{1},set(),{1}),chain({1},{1},set()))
    def test_08_subsets(self): self.assertEqual(len(subsets(4)),16)
    def test_09_negative(self): self.assertRaises(ValueError,subsets,-1)
    def test_10_bool_bound(self): self.assertRaises(ValueError,subsets,True)
    def test_11_exhaustive(self):
        r=enumerate_chains(); self.assertEqual(r['combinations'],4681); self.assertEqual(r['valid_chains'],341); self.assertEqual(r['violations'],0);self.assertEqual(r['oracle_disagreements'],0)
    def test_12_bound(self): self.assertRaises(ValueError,enumerate_chains,-1)
    def test_13_roles(self):
        for role in ROLES:self.assertFalse(Explanation(role,'A','B',('B implies A','C implies B'),'teaching').report()['certifies_real_cause'])
    def test_14_role_invalid(self): self.assertRaises(ValueError,Explanation,'magic','a','b',('x','y'),'s')
    def test_15_label_invalid(self): self.assertRaises(ValueError,Explanation,'end',' ','b',('x','y'),'s')
    def test_16_missing_premise(self): self.assertRaises(ValueError,Explanation,'end','a','b',('x',),'s')
    def test_17_blank_premise(self): self.assertRaises(ValueError,Explanation,'end','a','b',('x',''),'s')
    def test_18_source_invalid(self): self.assertRaises(ValueError,Explanation,'end','a','b',('x','y'),'')
    def test_19_desire_not_action(self): self.assertFalse(Scenario(True,False,True,True).outcome)
    def test_20_success(self): self.assertTrue(Scenario(True,True,True,True).goal_and_success)
    def test_21_failed_mechanism(self): self.assertFalse(Scenario(True,True,False,True).outcome)
    def test_22_failed_background(self): self.assertFalse(Scenario(True,True,True,False).outcome)
    def test_23_unintended(self):
        s=Scenario(False,True,True,True);self.assertTrue(s.outcome);self.assertFalse(s.goal_and_success)
    def test_24_strict_bool(self): self.assertRaises(ValueError,Scenario,1,True,True,True)
    def test_25_truth_table(self):
        r=enumerate_scenarios();self.assertEqual(r,dict(cases=16,goal_without_action=4,goal_without_outcome=7,goal_and_success=1,outcome_without_goal=1,goal_toggle_changes_mechanism=0))
    def test_26_chronology(self): self.assertTrue(planning_order(0,1,2));self.assertTrue(planning_order(0,0,1))
    def test_27_chronology_bad(self): self.assertFalse(planning_order(2,0,1));self.assertFalse(planning_order(0,1,1))
    def test_28_chronology_inputs(self): self.assertRaises(ValueError,planning_order,True,1,2)
    def test_29_order_count(self): self.assertEqual(sum(planning_order(*v) for v in product(range(3),repeat=3)),4)
    def test_30_role_not_logic(self):
        reports=[Explanation(role,'A','B',('p','q'),'s').report() for role in ROLES]
        self.assertEqual(len(reports),4);self.assertTrue(all(r['premises']==['p','q'] for r in reports))
if __name__=='__main__':unittest.main()
