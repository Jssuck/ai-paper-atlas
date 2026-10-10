"""Standard-library tests, including an independent quantified oracle."""

import unittest
from collections import Counter
from itertools import combinations

from euler_semantics import (
    ATOM_NAMES, FORMS, Mode, Model, canonical_model, counterexample,
    labeled_models, representatives,
)


def quantified_oracle(model):
    """Uses per-element quantifiers rather than set operations/occupancy bits."""
    u, s, p = model.universe, model.subject, model.predicate
    return {
        "A": all(x not in s or x in p for x in u),
        "E": all(not (x in s and x in p) for x in u),
        "I": any(x in s and x in p for x in u),
        "O": any(x in s and x not in p for x in u),
    }


class CategoricalSemanticsTests(unittest.TestCase):
    def test_universe_and_term_validation(self):
        with self.assertRaises(ValueError):
            Model(set(), set(), set())
        with self.assertRaises(ValueError):
            Model({0}, {1}, set())
        with self.assertRaises(ValueError):
            Model({0}, set(), {1})
        self.assertIsInstance(Model({0}, {0}, {0}).subject, frozenset)

    def test_mask_validation_and_roundtrip(self):
        for mask in (0, 16, -1, True, 1.0, "1"):
            with self.assertRaises(ValueError):
                canonical_model(mask)
        for mask in range(1, 16):
            model = canonical_model(mask)
            self.assertEqual(model.occupancy(), mask)
            self.assertEqual(len(model.universe), mask.bit_count())

    def test_invalid_modes_forms_and_sizes_raise(self):
        with self.assertRaises(ValueError):
            representatives("typo")
        with self.assertRaises(ValueError):
            canonical_model(1).admitted("typo")
        for premises, conclusion in ((["X"], "A"), (["A"], "x")):
            with self.assertRaises(ValueError):
                counterexample(premises, conclusion, Mode.ALLOW_EMPTY_TERMS)
        for size in (0, -1, True, 1.5):
            with self.assertRaises(ValueError):
                list(labeled_models(size))

    def test_inclusion_is_not_strict(self):
        equal = Model({0}, {0}, {0})
        self.assertTrue(equal.truth()["A"])
        self.assertFalse(equal.subject < equal.predicate)

    def test_some_does_not_mean_some_but_not_all(self):
        equal = canonical_model(1)
        self.assertTrue(equal.truth()["A"])
        self.assertTrue(equal.truth()["I"])
        self.assertFalse(equal.truth()["O"])

    def test_empty_subject_vacuity(self):
        model = Model({0}, set(), {0})
        self.assertEqual(model.truth(), dict(A=True, E=True, I=False, O=False))
        self.assertTrue(model.admitted(Mode.ALLOW_EMPTY_TERMS))
        self.assertFalse(model.admitted(Mode.NONEMPTY_TERMS))

    def test_empty_predicate_is_separate_from_empty_subject(self):
        model = Model({0}, {0}, set())
        self.assertEqual(model.truth(), dict(A=False, E=True, I=False, O=True))
        self.assertFalse(model.admitted(Mode.NONEMPTY_TERMS))

    def test_strict_overlap_is_an_example_not_a_definition(self):
        overlap = canonical_model(7)
        self.assertEqual(overlap.truth(), dict(A=False, E=False, I=True, O=True))
        equal = canonical_model(1)
        disjoint = canonical_model(6)
        proper_superset = canonical_model(3)
        self.assertTrue(equal.truth()["I"])
        self.assertFalse(equal.truth()["O"])
        self.assertTrue(disjoint.truth()["O"])
        self.assertFalse(disjoint.truth()["I"])
        self.assertTrue(proper_superset.truth()["I"] and proper_superset.truth()["O"])
        self.assertFalse(proper_superset.predicate - proper_superset.subject)

    def test_all_340_labeled_models_match_quantified_oracle_and_compression(self):
        checked = 0
        for size in range(1, 5):
            models = list(labeled_models(size))
            self.assertEqual(len(models), 4 ** size)
            for model in models:
                checked += 1
                self.assertEqual(model.truth(), quantified_oracle(model))
                reduced = canonical_model(model.occupancy())
                self.assertEqual(model.truth(), reduced.truth())
                for mode in Mode:
                    self.assertEqual(model.admitted(mode), reduced.admitted(mode))
        self.assertEqual(checked, 340)

    def test_atom_partition(self):
        for model in labeled_models(4):
            atoms = model.atoms()
            self.assertEqual(len(atoms), len(ATOM_NAMES))
            self.assertEqual(frozenset().union(*atoms), model.universe)
            for left, right in combinations(atoms, 2):
                self.assertFalse(left & right)

    def test_exact_mode_and_form_counts(self):
        expected = {
            Mode.ALLOW_EMPTY_TERMS: (15, dict(A=7, E=7, I=8, O=8)),
            Mode.NONEMPTY_TERMS: (10, dict(A=4, E=2, I=8, O=6)),
        }
        for mode, (total, counts) in expected.items():
            models = representatives(mode)
            self.assertEqual(len(models), total)
            self.assertEqual({f: sum(m.truth()[f] for m in models) for f in FORMS}, counts)

    def test_exact_joint_truth_patterns(self):
        for mode, expected in (
            (Mode.ALLOW_EMPTY_TERMS, {"AE": 3, "AI": 4, "EO": 4, "IO": 4}),
            (Mode.NONEMPTY_TERMS, {"AI": 4, "EO": 2, "IO": 4}),
        ):
            actual = Counter("".join(f for f in FORMS if m.truth()[f]) for m in representatives(mode))
            self.assertEqual(dict(actual), expected)

    def test_contradictory_pairs_in_both_modes(self):
        for mode in Mode:
            for model in representatives(mode):
                values = model.truth()
                self.assertNotEqual(values["A"], values["O"])
                self.assertNotEqual(values["E"], values["I"])

    def test_exact_single_premise_entailments(self):
        identities = {(f, f) for f in FORMS}
        for mode in Mode:
            actual = {(p, q) for p in FORMS for q in FORMS if counterexample([p], q, mode) is None}
            expected = identities | ({("A", "I"), ("E", "O")} if mode is Mode.NONEMPTY_TERMS else set())
            self.assertEqual(actual, expected)

    def test_subalternation_has_empty_subject_counterexamples(self):
        for premise, conclusion in (("A", "I"), ("E", "O")):
            example = counterexample([premise], conclusion, Mode.ALLOW_EMPTY_TERMS)
            self.assertIsNotNone(example)
            self.assertFalse(example.subject)
            self.assertEqual(len(example.universe), 1)
            self.assertIsNone(counterexample([premise], conclusion, Mode.NONEMPTY_TERMS))

    def test_every_premise_subset_checked_against_labeled_models(self):
        # 16 premise subsets × 4 conclusions × 2 modes = 128 consequence queries.
        all_models = [m for size in range(1, 5) for m in labeled_models(size)]
        for mode in Mode:
            allowed = [m for m in all_models if m.admitted(mode)]
            self.assertEqual(len(allowed), 340 if mode is Mode.ALLOW_EMPTY_TERMS else 284)
            for bits in range(16):
                premises = [f for i, f in enumerate(FORMS) if bits & (1 << i)]
                for conclusion in FORMS:
                    brute = [m for m in allowed if all(quantified_oracle(m)[p] for p in premises)
                             and not quantified_oracle(m)[conclusion]]
                    example = counterexample(premises, conclusion, mode)
                    self.assertEqual(example is None, not brute)
                    if example is not None:
                        self.assertEqual(len(example.universe), min(len(m.universe) for m in brute))
                        self.assertTrue(all(example.truth()[p] for p in premises))
                        self.assertFalse(example.truth()[conclusion])


if __name__ == "__main__":
    unittest.main()
