"""Independent reviewer: tuple truth tables and subset-order checks."""
import itertools
import json
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from model import every_instance, counterexample, relative_partition, broadest_adequate, PerSeDeclarations


def encode(row):
    return sum(value * (2 ** index) for index, value in enumerate(row))


class IndependentChecks(unittest.TestCase):
    def test_all_two_object_three_time_tables(self):
        rows = list(itertools.product((0, 1), repeat=6))
        for s, p in itertools.product(rows, repeat=2):
            fails = [(i % 2, i // 2) for i, (a, b) in enumerate(zip(s, p)) if a and not b]
            self.assertEqual(every_instance(encode(s), encode(p), 6), not fails)
            self.assertEqual(counterexample(encode(s), encode(p), 2, 3), fails[0] if fails else None)

    def test_four_object_partitions(self):
        rows = list(itertools.product((0, 1), repeat=4))
        total = 0
        for g, a, b in itertools.product(rows, repeat=3):
            expected = all(sum((x, y)) == 1 for inside, x, y in zip(g, a, b) if inside)
            self.assertEqual(relative_partition(encode(g), encode(a), encode(b), 4), expected)
            total += expected
        self.assertEqual(total, 6 ** 4)

    def test_all_four_named_classes_two_objects(self):
        universe = (0, 1)
        subsets = [set(i for i in universe if mask & (1 << i)) for mask in range(4)]
        names = ('alpha', 'beta', 'gamma', 'delta')
        for choices in itertools.product(range(4), repeat=5):
            classes = dict(zip(names, choices[:4]))
            pset = subsets[choices[4]]
            adequate = [name for name in names if subsets[classes[name]] and subsets[classes[name]].issubset(pset)]
            maxima = []
            for name in adequate:
                current = subsets[classes[name]]
                if not any(current.issubset(subsets[classes[other]]) and current != subsets[classes[other]] for other in adequate):
                    maxima.append(name)
            self.assertEqual(broadest_adequate(classes, choices[4], 2), tuple(sorted(maxima)))

    def test_body_temporal_example(self):
        # a,b at t0; b,c at t1. Only c at t1 lacks the predicate.
        self.assertEqual(counterexample(0b110011, 0b010011, 3, 2), (2, 1))
        self.assertTrue(every_instance(0b011, 0b011, 3))

    def test_domain_restriction_and_vacuity(self):
        self.assertTrue(relative_partition(0, 7, 7, 3))
        self.assertTrue(relative_partition(3, 5, 6, 3))
        self.assertFalse(relative_partition(7, 5, 6, 3))
        self.assertTrue(every_instance(0, 0, 0))
        self.assertEqual(broadest_adequate({}, 0, 0), ())

    def test_incomparable_and_coextensive(self):
        self.assertEqual(broadest_adequate({'x': 3, 'y': 5, 'copy': 3}, 7, 3), ('copy', 'x', 'y'))
        self.assertEqual(broadest_adequate({'x': 3, 'y': 5, 'whole': 7}, 7, 3), ('whole',))
        self.assertEqual(broadest_adequate({'empty': 0}, 7, 3), ())

    def test_declarations_are_not_truth_certificates(self):
        declared = PerSeDeclarations(attribute_in_subject_definition=frozenset({('s', 'p')}), independent_subjects=frozenset({'s'}))
        self.assertEqual(declared.senses('s', 'p'), ('definition-1', 'subsistence-3'))
        self.assertEqual(declared.senses('s', 'q'), ('subsistence-3',))
        self.assertFalse(every_instance(3, 1, 2))
        self.assertEqual(PerSeDeclarations().senses('coincidence', 'effect'), ())

    def test_invalid_inputs(self):
        for width in (True, -1, 1.5):
            with self.assertRaises(ValueError): every_instance(0, 0, width)
        for mask in (False, -1, 4, 1.2):
            with self.assertRaises(ValueError): every_instance(mask, 0, 2)
        with self.assertRaises(ValueError): broadest_adequate({'': 1}, 1, 1)
        with self.assertRaises(ValueError): counterexample(0, 0, 1, False)

if __name__ == '__main__':
    print(json.dumps({'independent_checks': 8, 'temporal_pairs': 4096,
                      'partition_triples': 4096, 'valid_partitions': 1296,
                      'four_named_class_cases': 1024,
                      'limits': 'Finite diagnostic tests; no certification of essence, causal claims or modal necessity.'}, sort_keys=True), flush=True)
    unittest.main(verbosity=2)
