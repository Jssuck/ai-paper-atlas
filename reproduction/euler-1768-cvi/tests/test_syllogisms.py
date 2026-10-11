"""Executable specifications; expected source order is independently pinned."""
import json
from itertools import combinations, product
from pathlib import Path
import subprocess
import sys
import unittest

import syllogisms as s

EXPECTED_SOURCE = {
    1: ("AAA", "AII", "EAE", "EIO"),
    2: ("AEE", "AOO", "EAE", "EIO"),
    3: ("AAI", "IAI", "AII", "EAO", "EIO", "OAO"),
    4: ("AAI", "IAI", "AEE", "EAO", "EIO"),
}
EXPECTED_BOOLEAN = {
    (1, "AAA"), (1, "AII"), (1, "EAE"), (1, "EIO"),
    (2, "AEE"), (2, "AOO"), (2, "EAE"), (2, "EIO"),
    (3, "IAI"), (3, "AII"), (3, "EIO"), (3, "OAO"),
    (4, "IAI"), (4, "AEE"), (4, "EIO"),
}


def set_holds(mood, subject, predicate):
    """Independent set-operation oracle, with no bit masks."""
    if mood == "A":
        return subject <= predicate
    if mood == "E":
        return subject.isdisjoint(predicate)
    if mood == "I":
        return bool(subject & predicate)
    if mood == "O":
        return bool(subject - predicate)
    raise ValueError(mood)


class SourceAndModelTests(unittest.TestCase):
    def test_exact_source_order_and_figures(self):
        self.assertEqual(s.EULER_LIST, EXPECTED_SOURCE)
        self.assertEqual(s.FIGURES, {
            1: (("M", "Q"), ("P", "M")),
            2: (("Q", "M"), ("P", "M")),
            3: (("M", "Q"), ("M", "P")),
            4: (("Q", "M"), ("M", "P")),
        })

    def test_support_counts_and_coverage(self):
        self.assertEqual({m.support for m in s.MODELS}, set(range(1, 256)))
        self.assertEqual(len(s.models_with()), 255)
        self.assertEqual(len(s.models_with(s.TERMS)), 218)
        self.assertEqual(len(s.all_forms()), 256)
        self.assertEqual(len(set(s.all_forms())), 256)

    def test_all_atomic_propositions_against_independent_sets(self):
        for model in s.MODELS:
            classes = {term: set(objects) for term, objects in model.as_dict()["classes"].items()}
            for subject, predicate, mood in product(s.TERMS, s.TERMS, s.MOODS):
                with self.subTest(support=model.support, subject=subject, predicate=predicate, mood=mood):
                    self.assertEqual(model.holds(mood, subject, predicate),
                                     set_holds(mood, classes[subject], classes[predicate]))

    def test_empty_terms_universals_vacuous_particulars_false(self):
        model = s.Model(1)  # atom 000: one object outside every class.
        for subject, predicate in product(s.TERMS, repeat=2):
            self.assertTrue(model.holds("A", subject, predicate))
            self.assertTrue(model.holds("E", subject, predicate))
            self.assertFalse(model.holds("I", subject, predicate))
            self.assertFalse(model.holds("O", subject, predicate))

    def test_multiplicity_does_not_affect_truth(self):
        # Independent object domains, including duplicate membership profiles.
        for memberships in product(range(8), repeat=3):
            support = sum(1 << atom for atom in set(memberships))
            model = s.Model(support)
            classes = {term: {i for i, atom in enumerate(memberships) if atom & bit}
                       for term, bit in s.TERM_BITS.items()}
            for subject, predicate, mood in product(s.TERMS, s.TERMS, s.MOODS):
                self.assertEqual(model.holds(mood, subject, predicate),
                                 set_holds(mood, classes[subject], classes[predicate]))


class ExhaustiveValidityTests(unittest.TestCase):
    def test_15_24_19_are_computed_not_assumed(self):
        self.assertEqual(set(s.valid_forms()), EXPECTED_BOOLEAN)
        self.assertEqual(len(s.valid_forms(s.TERMS)), 24)
        expected_list = {(f, mood) for f, moods in EXPECTED_SOURCE.items() for mood in moods}
        self.assertEqual(set(s.nonweakened_valid_forms(s.TERMS)), expected_list)
        self.assertEqual(len(s.nonweakened_valid_forms()), 15)
        extras = set(s.valid_forms(s.TERMS)) - expected_list
        self.assertEqual(extras, {(1, "AAI"), (1, "EAO"), (2, "AEO"), (2, "EAO"), (4, "AEO")})

    def test_alternative_Q_M_nonempty_background(self):
        expected = {(f, mood) for f, moods in EXPECTED_SOURCE.items() for mood in moods}
        self.assertEqual(set(s.valid_forms(["Q", "M"])), expected)
        self.assertEqual(len(s.models_with(["Q", "M"])), 228)

    def test_all_premise_pairs_satisfiable_in_every_regime(self):
        for figure in s.FIGURES:
            for premises in product(s.MOODS, repeat=2):
                for assumption in s.all_assumptions():
                    self.assertTrue(s.premise_models(figure, "".join(premises), assumption))

    def test_all_2048_checks_and_countermodel_certificates(self):
        for figure, mood in s.all_forms():
            for assumptions in s.all_assumptions():
                result = s.check_form(figure, mood, assumptions)
                major, minor = s.FIGURES[figure]
                # Independent direct set semantics over every permitted support.
                invalid_supports = []
                premise_count = 0
                for model in s.models_with(assumptions):
                    data = model.as_dict()
                    cls = {term: set(values) for term, values in data["classes"].items()}
                    if (set_holds(mood[0], cls[major[0]], cls[major[1]])
                            and set_holds(mood[1], cls[minor[0]], cls[minor[1]])):
                        premise_count += 1
                        if not set_holds(mood[2], cls["P"], cls["Q"]):
                            invalid_supports.append(model.support)
                self.assertEqual(result["premise_models"], premise_count)
                self.assertEqual(result["valid"], not invalid_supports)
                self.assertEqual(result["countermodel_count"], len(invalid_supports))
                if invalid_supports:
                    certificate = result["countermodel"]
                    self.assertEqual(certificate["support"], invalid_supports[0])
                    self.assertEqual(len(certificate["domain"]),
                                     min(support.bit_count() for support in invalid_supports))
                else:
                    self.assertIsNone(result["countermodel"])

    def test_minimal_assumptions_sufficiency_necessity_and_completeness(self):
        for figure, mood in s.all_forms():
            minima = [set(group) for group in s.minimal_existence_assumptions(figure, mood)]
            for assumption in s.all_assumptions():
                # Every sufficient assumption contains a minimal one, and conversely.
                self.assertEqual(s.check_form(figure, mood, assumption)["valid"],
                                 any(minimum <= set(assumption) for minimum in minima))
            for minimum in minima:
                for term in minimum:
                    self.assertFalse(s.check_form(figure, mood, minimum - {term})["valid"])

    def test_four_conditional_source_moods(self):
        expected = {(3, "AAI"): [["M"]], (3, "EAO"): [["M"]],
                    (4, "AAI"): [["Q"]], (4, "EAO"): [["M"]]}
        for figure, moods in EXPECTED_SOURCE.items():
            for mood in moods:
                self.assertEqual(s.minimal_existence_assumptions(figure, mood),
                                 expected.get((figure, mood), [[]]))
        for (figure, mood), minimum in expected.items():
            missing = minimum[0][0]
            other_terms = [term for term in s.TERMS if term != missing]
            result = s.check_form(figure, mood, other_terms)
            self.assertFalse(result["valid"])
            self.assertEqual(result["countermodel"]["classes"][missing], [])

    def test_dominance_is_regime_global_not_premise_relative(self):
        self.assertFalse(s.strictly_implies("A", "I"))
        self.assertFalse(s.strictly_implies("E", "O"))
        self.assertTrue(s.strictly_implies("A", "I", ["P"]))
        self.assertTrue(s.strictly_implies("E", "O", ["P"]))
        pairs = {(a, b) for a in s.MOODS for b in s.MOODS if s.strictly_implies(a, b, s.TERMS)}
        self.assertEqual(pairs, {("A", "I"), ("E", "O")})

    def test_equivocation_really_has_true_premises_false_conclusion(self):
        result = s.equivocation_example()
        self.assertTrue(result["major_M1_subset_Q"])
        self.assertTrue(result["minor_P_subset_M2"])
        self.assertFalse(result["claimed_conclusion_P_subset_Q"])
        self.assertFalse(result["same_middle_term"])


class ValidationAndCLITests(unittest.TestCase):
    def test_invalid_model_inputs(self):
        for support in [0, 256, -1, True, 1.0, "1", None]:
            with self.subTest(support=support), self.assertRaises(ValueError):
                s.Model(support)

    def test_invalid_public_api_inputs(self):
        for figure in [0, 5, True, 1.0, "I", None, []]:
            with self.assertRaises(ValueError):
                s.check_form(figure, "AAA")
        for mood in ["", "AA", "AAAA", "aaa", "AAX", None, 123, []]:
            with self.assertRaises(ValueError):
                s.check_form(1, mood)
        for assumptions in ["P", ["X"], ["P", "P"], [None], None, [1]]:
            with self.assertRaises(ValueError):
                s.check_form(1, "AAA", assumptions)
        for term in ["A", "X", None, [], 1]:
            with self.assertRaises(ValueError):
                s.Model(1).nonempty(term)

    def test_cli_good_query(self):
        path = Path(s.__file__)
        completed = subprocess.run([sys.executable, str(path), "query", "3", "AAI", "--exists", "M"],
                                   capture_output=True, text=True, check=True)
        result = json.loads(completed.stdout)
        self.assertTrue(result["valid"])
        self.assertEqual(result["minimal_existence_assumptions"], [["M"]])

    def test_cli_bad_inputs_fail_cleanly(self):
        for arguments in [["query", "5", "AAA"], ["query", "1", "aai"],
                          ["query", "1", "AAA", "--exists", "X"],
                          ["query", "1", "AAA", "--exists", "P", "P"]]:
            completed = subprocess.run([sys.executable, str(Path(s.__file__)), *arguments],
                                       capture_output=True, text=True)
            self.assertEqual(completed.returncode, 2)
            self.assertIn("error:", completed.stderr)
            self.assertNotIn("Traceback", completed.stderr)

    def test_report_structure(self):
        report = s.build_report()
        self.assertEqual(len(report["all_256_forms"]), 256)
        self.assertEqual(len(report["source_listing_in_original_order"]), 19)
        self.assertEqual(report["summary"]["valid_without_term_existence"], 15)
        self.assertTrue(report["summary"]["nonweakened_set_equals_euler_list"])


if __name__ == "__main__":
    unittest.main()
