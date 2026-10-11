"""Independent assertions and small labeled-model cross-checks; stdlib only."""

from itertools import product
import json
import subprocess
import sys
import unittest

from euler_cv import (
    ARGUMENTS, CORRECTED, INVALID, TERMS, VALID, Model, Proposition,
    check, from_support, models, named_examples, representatives,
)


class EncodingTests(unittest.TestCase):
    def test_type_bit_order(self):
        for atom in range(8):
            model = from_support(1 << atom)
            self.assertEqual(model.universe, {f"t{atom}"})
            self.assertEqual(bool(model.a), bool(atom & 1))
            self.assertEqual(bool(model.b), bool(atom & 2))
            self.assertEqual(bool(model.c), bool(atom & 4))
            self.assertEqual(model.atom(f"t{atom}"), atom)

    def test_all_supports_round_trip_and_no_extra_outside_element(self):
        for support in range(1, 256):
            model = from_support(support)
            self.assertEqual(model.support(), support)
            self.assertEqual(len(model.universe), support.bit_count())
            self.assertEqual("t0" in model.universe, bool(support & 1))

    def test_support_not_multiplicity(self):
        model = Model({"x", "y", "z"}, {"x", "y"}, {"x", "y"}, {"z"})
        self.assertEqual(model.support(), (1 << 3) | (1 << 4))
        self.assertEqual(len(from_support(model.support()).universe), 2)

    def test_reject_empty_universe_and_bad_supports(self):
        with self.assertRaises(ValueError):
            Model(set(), set(), set(), set())
        for bad in (0, -1, 256, True, 1.0, "1"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                from_support(bad)

    def test_reject_non_subsets_and_unknown_terms(self):
        with self.assertRaises(ValueError):
            Model({"x"}, {"y"}, set(), set())
        with self.assertRaises(ValueError):
            from_support(1).term("D")
        with self.assertRaises(ValueError):
            from_support(1).atom("missing")
        with self.assertRaises(ValueError):
            Proposition("X", "A", "B")
        with self.assertRaises(ValueError):
            Proposition("I", "D", "B")

    def test_inputs_are_frozen(self):
        universe, subset = {"x"}, {"x"}
        model = Model(universe, subset, set(), set())
        subset.clear()
        universe.add("y")
        self.assertEqual(model.universe, {"x"})
        self.assertEqual(model.a, {"x"})


class SemanticTests(unittest.TestCase):
    def test_empty_subject_vacuity(self):
        model = from_support(1)  # One outside element; all three classes empty.
        for subject in TERMS:
            for predicate in TERMS:
                for kind, expected in (("A", True), ("E", True), ("I", False), ("O", False)):
                    self.assertEqual(Proposition(kind, subject, predicate).holds(model), expected)

    def test_some_means_at_least_one_not_some_but_not_all(self):
        model = Model({"x"}, {"x"}, {"x"}, set())
        self.assertTrue(Proposition("A", "A", "B").holds(model))
        self.assertTrue(Proposition("I", "A", "B").holds(model))
        self.assertFalse(Proposition("O", "A", "B").holds(model))

    def test_witness_api_rejects_universal_claims(self):
        for kind in ("A", "E"):
            with self.assertRaises(ValueError):
                Proposition(kind, "A", "B").witnesses(from_support(1))

    def test_reduction_preserves_all_aeio_and_existential_witnesses(self):
        # Every assignment of 1, 2, or 3 labeled elements to eight types.
        # Repetition deliberately checks collapse of duplicate type members.
        for size in (1, 2, 3):
            for assignment in product(range(8), repeat=size):
                universe = {f"x{i}" for i in range(size)}
                subsets = [{f"x{i}" for i, atom in enumerate(assignment) if atom & bit} for bit in (1, 2, 4)]
                original = Model(universe, *subsets)
                reduced = from_support(original.support())
                mapping = representatives(original)
                self.assertEqual(set(mapping.values()), reduced.universe)
                self.assertEqual(original.all_classes_nonempty(), reduced.all_classes_nonempty())
                for subject, predicate in product(TERMS, repeat=2):
                    for kind in "AEIO":
                        claim = Proposition(kind, subject, predicate)
                        self.assertEqual(claim.holds(original), claim.holds(reduced))
                        if kind in "IO":
                            self.assertEqual({mapping[x] for x in claim.witnesses(original)}, claim.witnesses(reduced))

    def test_nonempty_filter_exactly_matches_sets(self):
        filtered = list(models(True))
        self.assertEqual(len(list(models())), 255)
        self.assertEqual(len(filtered), 218)
        self.assertEqual({m.support() for m in filtered}, {m.support() for m in models() if m.a and m.b and m.c})


class ArgumentTests(unittest.TestCase):
    def test_exact_counts(self):
        for nonempty, expected_total, expected_premises, expected_bad in ((False, 255, 32, 16), (True, 218, 24, 8)):
            for argument in ARGUMENTS:
                result = check(argument, nonempty)
                self.assertEqual(result["total_support_models"], expected_total)
                self.assertEqual(result["premise_models"], expected_premises)
                self.assertEqual(result["countermodels"], expected_bad if argument is INVALID else 0)

    def test_valid_witness_transfers_to_conclusion(self):
        for model in models():
            p, q, _ = VALID.statuses(model)
            if p and q:
                self.assertLessEqual(VALID.second.witnesses(model), VALID.conclusion.witnesses(model))

    def test_corrected_witness_transfers_to_conclusion(self):
        for model in models():
            p, q, _ = CORRECTED.statuses(model)
            if p and q:
                self.assertLessEqual(CORRECTED.first.witnesses(model), CORRECTED.conclusion.witnesses(model))

    def test_explicit_nonempty_countermodel_is_minimal(self):
        model = named_examples()["invalid_countermodel_nonempty"]
        self.assertEqual(model.as_dict()["U"], ["s", "v"])
        self.assertEqual(model.a, {"s", "v"})
        self.assertEqual(model.b, {"s"})
        self.assertEqual(model.c, {"v"})
        self.assertEqual(INVALID.statuses(model), (True, True, False))
        self.assertEqual(CORRECTED.statuses(model), (True, True, True))
        self.assertEqual(model.support(), 40)
        self.assertEqual(check(INVALID, True)["minimal_countermodel_size"], 2)
        self.assertFalse(any(INVALID.countermodel(m) for m in models(True) if len(m.universe) < 2))

    def test_empty_C_allows_one_element_countermodel(self):
        model = from_support(1 << 3)
        self.assertFalse(model.c)
        self.assertTrue(INVALID.countermodel(model))
        self.assertEqual(check(INVALID)["minimal_countermodel_size"], 1)

    def test_candidate_conclusion_can_also_be_true(self):
        model = named_examples()["invalid_true_conclusion_alternative"]
        self.assertEqual(INVALID.statuses(model), (True, True, True))
        self.assertEqual(model.a, model.b)
        self.assertEqual(model.support(), 24)

    def test_three_remainder_possibilities(self):
        examples = named_examples()
        for suffix in ("disjoint_A", "subset_A", "mixed_A"):
            model = examples[f"valid_remainder_{suffix}"]
            self.assertTrue(model.all_classes_nonempty())
            self.assertEqual(VALID.statuses(model), (True, True, True))
            remainder = model.c - model.b
            self.assertTrue(remainder)
            if suffix == "disjoint_A":
                self.assertTrue(remainder.isdisjoint(model.a))
            elif suffix == "subset_A":
                self.assertLessEqual(remainder, model.a)
            else:
                self.assertTrue(remainder & model.a)
                self.assertTrue(remainder - model.a)

    def test_remainder_not_required_to_exist(self):
        model = named_examples()["valid_no_remainder"]
        self.assertFalse(model.c - model.b)
        self.assertEqual(VALID.statuses(model), (True, True, True))

    def test_contrapositive_requires_validity(self):
        for argument in (VALID, CORRECTED):
            for model in models():
                p, q, r = argument.statuses(model)
                if not r:
                    self.assertFalse(p and q)
        self.assertTrue(any(INVALID.countermodel(m) for m in models(True)))

    def test_false_premises_can_have_true_conclusion(self):
        model = named_examples()["valid_both_premises_false_conclusion_true"]
        self.assertEqual(VALID.statuses(model), (False, False, True))

    def test_cli_json(self):
        completed = subprocess.run([sys.executable, "euler_cv.py", "--json"], check=True, capture_output=True, text=True)
        data = json.loads(completed.stdout)
        self.assertEqual(data["results"]["all_classes_nonempty"]["invalid"]["countermodels"], 8)


if __name__ == "__main__":
    unittest.main()
