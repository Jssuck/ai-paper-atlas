import unittest
from model import inheritance, taxonomy_path, observation, relation_map, experiments

class InheritanceTests(unittest.TestCase):
    def test_valid(self): self.assertTrue(inheritance({1},{1,2},{1,2,3})['premises'])
    def test_first_premise(self): self.assertFalse(inheritance({3},{1},{1,3})['premises'])
    def test_second_premise(self): self.assertFalse(inheritance({1},{1,2},{1})['premises'])
    def test_true_conclusion_not_certificate(self): self.assertTrue(inheritance({1},{1,2},{1})['conclusion'])
    def test_empty(self): self.assertFalse(inheritance(set(),set(),set())['subject_nonempty'])
    def test_generator(self): self.assertTrue(inheritance(iter([1]),iter([1,2]),iter([1,2]))['premises'])
    def test_path(self): self.assertTrue(taxonomy_path({'d':{1},'a':{1,2},'g':{1,2,3}},['d','a','g'],{1,2,3})['certificate'])
    def test_bad_edge(self): self.assertFalse(taxonomy_path({'d':{1},'a':{2}},['d','a'],{1,2})['certificate'])
    def test_bad_root(self): self.assertFalse(taxonomy_path({'d':{1},'a':{1,2}},['d','a'],{1})['certificate'])
    def test_single_node(self): self.assertTrue(taxonomy_path({'d':{1}},['d'],{1})['certificate'])
    def test_empty_path(self): self.assertRaises(ValueError,taxonomy_path,{},[],set())
    def test_repeated_path(self): self.assertRaises(ValueError,taxonomy_path,{'a':{1}},['a','a'],{1})
    def test_unknown(self): self.assertRaises(ValueError,taxonomy_path,{},['a'],{1})
    def test_path_generator(self): self.assertTrue(taxonomy_path({'a':iter([1])},iter(['a']),iter([1]))['certificate'])

class ObservationTests(unittest.TestCase):
    def test_missed(self): self.assertEqual(observation({0},{0,1},{0})['counterexamples'],[1])
    def test_positive_sample_not_class(self): self.assertFalse(observation({0},{0,1},{0})['class_positive'])
    def test_covered(self): self.assertTrue(observation({0,1},{0,1},{0,1})['sample_covers_class'])
    def test_empty_sample(self): self.assertTrue(observation(set(),{0},set())['sample_positive'])
    def test_outside(self): self.assertRaises(ValueError,observation,{2},{0},{0})

class AnalogyTests(unittest.TestCase):
    def test_identity(self): self.assertTrue(relation_map({0,1},{0,1},{(0,1)},{(0,1)},{0:0,1:1})['preserves_relation'])
    def test_broken(self): self.assertFalse(relation_map({0,1},{0,1},{(0,1)},set(),{0:0,1:1})['preserves_relation'])
    def test_not_injective(self): self.assertTrue(relation_map({0,1},{0},{(0,1)},{(0,0)},{0:0,1:0})['preserves_relation'])
    def test_no_relation_vacuous(self): self.assertTrue(relation_map({0},{1},set(),set(),{0:1})['preserves_relation'])
    def test_partial(self): self.assertRaises(ValueError,relation_map,{0,1},{0},set(),set(),{0:0})
    def test_bad_value(self): self.assertRaises(ValueError,relation_map,{0},{0},set(),set(),{0:2})
    def test_bad_source_edge(self): self.assertRaises(ValueError,relation_map,{0},{0},{(0,1)},set(),{0:0})
    def test_bad_target_edge(self): self.assertRaises(ValueError,relation_map,{0},{0},set(),{(0,1)},{0:0})
    def test_no_unary_transfer(self):
        r=relation_map({0},{1},set(),set(),{0:1})
        self.assertTrue(r['preserves_relation']); self.assertNotIn(1,{0})
    def test_exhaustive(self):
        e=experiments(); self.assertEqual(e['inheritance']['triples'],4681)
        self.assertEqual(e['inheritance']['valid_chains'],341)
        self.assertEqual(e['analogy']['maps_checked'],1024)
        self.assertEqual(e['analogy']['oracle_disagreements'],0)

if __name__ == '__main__': unittest.main()
