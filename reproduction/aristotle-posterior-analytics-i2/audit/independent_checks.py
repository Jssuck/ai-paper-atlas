"""Independent reviewer checks. Finite semantics, not ancient knowledge certification."""
import itertools
import json
import sys
import unittest
from pathlib import Path
from dataclasses import replace
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model import entails, counterworlds, Premise, Candidate, inspect_candidate, classify_starting_point


def worlds(mask):
    return {i for i, bit in enumerate(reversed(format(mask, '08b'))) if bit == '1'}

class ReviewTests(unittest.TestCase):
    def test_all_single_premise_sets(self):
        valid = 0
        for p, q in itertools.product(range(256), repeat=2):
            bad = worlds(p) - worlds(q)
            self.assertEqual(entails([p], q), not bad)
            self.assertEqual(set(counterworlds([p], q)), bad)
            valid += not bad
        self.assertEqual(valid, 3 ** 8)

    def test_two_premise_complete_four_world_subspace(self):
        # Low four worlds suffice for this explicitly bounded subspace.
        for p, r, q in itertools.product(range(16), repeat=3):
            bad = (worlds(p) & worlds(r)) - worlds(q)
            self.assertEqual(entails([p, r], q), not bad)
            self.assertEqual(set(counterworlds([p, r], q)), bad)

    def test_modus_ponens_all_valuations(self):
        for p, q in itertools.product((False, True), repeat=2):
            implication = (not p) or q
            self.assertFalse(p and implication and not q)
        # A false premise and true conclusion do not make the schema invalid.
        p, q = False, True
        self.assertFalse(p)
        self.assertTrue((not p) or q)
        self.assertTrue(q)

    def test_empty_extension_definition(self):
        for n in (1, 2, 3):
            domain = range(n)
            u, d = set(), set()
            self.assertTrue(all((x in u) == (x in d) for x in domain))
            self.assertFalse(any(x in u for x in domain))

    def test_metadata_variants_two_premises(self):
        p = Premise('p', 170, True, True, 0, 3)
        r = Premise('r', 204, True, True, 0, 3)
        c = Candidate((p, r), 'q', 238, 3, 1, 2, frozenset({('p', 'q'), ('r', 'q')}))
        self.assertTrue(inspect_candidate(c)['declared_policy_pass'])
        # Independent toggles on each premise; all ten checks must survive.
        passes = 0
        for flags in itertools.product((False, True), repeat=10):
            newp = []
            links = set()
            for i, old in enumerate((p, r)):
                prim, imm, prior, conf, cause = flags[5*i:5*i+5]
                newp.append(replace(old, primary_declared=prim, immediate_declared=imm,
                                    priority_rank=0 if prior else 1, confidence_rank=3 if conf else 2))
                if cause:
                    links.add((old.name, 'q'))
            result = inspect_candidate(replace(c, premises=tuple(newp), cause_links_declared=frozenset(links)))
            self.assertEqual(result['declared_policy_pass'], all(flags))
            self.assertFalse(result['scientific_knowledge_certified'])
            passes += result['declared_policy_pass']
        self.assertEqual(passes, 1)

    def test_input_boundaries_and_polarity(self):
        for item in (True, -1, 256, 1.0, '1'):
            with self.assertRaises(ValueError):
                entails([item], 255)
        self.assertTrue(entails([], 255))
        self.assertFalse(entails([], 254))
        for v in (False, True):
            self.assertEqual(classify_starting_point(indispensable_for_any_learning=False, existence_assertion=v), 'hypothesis')
        self.assertEqual(classify_starting_point(indispensable_for_any_learning=False, existence_assertion=None), 'definition')

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ReviewTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({'single_premise_pairs':65536, 'two_premise_cases':4096,
                      'two_premise_metadata_cases':1024, 'definition_empty_domain_sizes':[1,2,3],
                      'passed':result.wasSuccessful()}, sort_keys=True))
    sys.exit(0 if result.wasSuccessful() else 1)
