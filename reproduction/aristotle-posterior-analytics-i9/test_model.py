import unittest
from model import ALL, Declarations, assess, atom, certificate, experiment, implication, minimal_supports, models

class PremiseTests(unittest.TestCase):
    def setUp(self):
        self.x, self.y, self.z = map(atom, range(3))
        self.route = [implication(self.y, self.z), self.x, implication(self.x, self.y)]
        self.good = Declarations(True, True, True)

    def test_atoms(self):
        self.assertEqual([self.x, self.y, self.z], [170, 204, 240])
    def test_empty_models(self):
        self.assertEqual(models([]), ALL)
    def test_common_insufficient(self):
        self.assertFalse(assess(self.route[:1], self.z)["entails"])
    def test_specific_sufficient(self):
        self.assertTrue(assess(self.route, self.z)["entails"])
    def test_remove_fact(self):
        self.assertFalse(assess([self.route[0], self.route[2]], self.z)["entails"])
    def test_remove_bridge(self):
        self.assertFalse(assess(self.route[:2], self.z)["entails"])
    def test_inconsistent_entails_not_accepted(self):
        result = certificate([0], self.z, self.good)
        self.assertTrue(result["entails"])
        self.assertFalse(result["policy_pass"])
    def test_empty_support_tautology(self):
        self.assertEqual(minimal_supports([self.x], ALL), [()])
    def test_supports_unique(self):
        self.assertEqual(minimal_supports(self.route, self.z), [(0, 1, 2)])
    def test_alternative_supports(self):
        self.assertEqual(minimal_supports([self.y, self.route[0], self.x, self.route[2]], self.z), [(0, 1), (1, 2, 3)])
    def test_false_goal_no_consistent_support(self):
        self.assertEqual(minimal_supports([0, self.x], 0), [])
    def test_same_semantics_different_annotations(self):
        a = certificate(self.route, self.z, self.good)
        b = certificate(self.route, self.z, Declarations(False, False, True))
        self.assertEqual(a["models"], b["models"])
        self.assertNotEqual(a["policy_pass"], b["policy_pass"])
    def test_superior_bridge(self):
        self.assertTrue(certificate(self.route, self.z, Declarations(True, True, False, True, True))["policy_pass"])
    def test_superior_without_bridge(self):
        self.assertFalse(certificate(self.route, self.z, Declarations(True, True, False, True))["policy_pass"])
    def test_bridge_without_superior(self):
        self.assertFalse(certificate(self.route, self.z, Declarations(True, True, False, False, True))["policy_pass"])
    def test_truth_without_cause(self):
        self.assertFalse(certificate(self.route, self.z, Declarations(True, False, True))["policy_pass"])
    def test_invalid_masks(self):
        for bad in [-1, 256, True, "1", 1.0]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                assess([bad], self.z)
    def test_invalid_goal(self):
        with self.assertRaises(ValueError):
            assess([], -1)
    def test_invalid_declarations(self):
        with self.assertRaises(ValueError):
            certificate(self.route, self.z, Declarations(1, True, True))
    def test_exhaustive_oracle(self):
        result = experiment()
        self.assertEqual(result["oracle_disagreements"], 0)
        self.assertEqual(result["consistent_entailment_pairs"], 6305)

if __name__ == "__main__":
    unittest.main(verbosity=2)
