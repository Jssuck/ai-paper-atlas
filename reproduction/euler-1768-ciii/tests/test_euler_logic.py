"""Regression, boundary, and cross-representation tests (standard library only).

These implementation tests do not replace the mathematical abstraction proof or
the separately requested independent oracle review.
"""

import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from euler_logic import (
    Argument, CATALOG, KINDS, REGIMES, TERMS, RegionModel, Statement,
    audit_fixed_first, catalog_matches, check_argument, ei_conversion_variants,
    evaluate_sets, explicit_examples, fixed_first_candidates, mask_for_sets,
    models, s,
)
from reproduce import build_report, render_text


class ModelTests(unittest.TestCase):
    def test_all_256_masks_and_255_distinct_nonempty_universes(self):
        selected = models()
        self.assertEqual(len(selected), 256)
        self.assertEqual(len({m.occupied_mask for m in selected}), 255)
        self.assertTrue(all(m.as_sets()["universe"] for m in selected))

    def test_empty_raw_mask_adds_only_an_outside_witness(self):
        model = RegionModel(0)
        self.assertEqual(model.occupied_mask, 1)
        self.assertEqual(model.region_types, (0,))
        self.assertEqual(model.as_sets()["terms"], {"A": [], "B": [], "C": []})
        self.assertTrue(model.as_sets()["outside_witness_added"])
        for kind, left, right in itertools.product(KINDS, TERMS, TERMS):
            statement = s(kind, left, right)
            self.assertEqual(model.evaluate(statement), RegionModel(1).evaluate(statement))

    def test_regime_counts_and_term_conditions(self):
        self.assertEqual(len(models("all_terms_nonempty")), 218)
        self.assertEqual(len(models("A_nonempty_only")), 240)
        self.assertTrue(all(all(m.term_nonempty(t) for t in TERMS) for m in models("all_terms_nonempty")))
        self.assertTrue(all(m.term_nonempty("A") for m in models("A_nonempty_only")))

    def test_invalid_masks_and_regimes_rejected(self):
        for mask in (-1, 256, 1.5, "4", True):
            with self.subTest(mask=mask), self.assertRaises(ValueError):
                RegionModel(mask)
        with self.assertRaises(ValueError):
            models("not_a_regime")
        with self.assertRaises(ValueError):
            RegionModel(1).satisfies_regime("not_a_regime")

    def test_invalid_statements_rejected(self):
        for values in (("Q", "A", "B"), ("A", "D", "B"), ("E", "A", "Z")):
            with self.subTest(values=values), self.assertRaises(ValueError):
                Statement(*values)

    def test_all_masks_roundtrip_through_sets(self):
        for model in models():
            named = model.as_sets()
            self.assertEqual(mask_for_sets(named["universe"], named["terms"]), model.occupied_mask)

    def test_bit_evaluator_agrees_with_set_evaluator_exhaustively(self):
        # 256 raw masks x 4 categorical kinds x 9 ordered pairs = 9,216 checks.
        for model in models():
            named = model.as_sets()
            for kind, left, right in itertools.product(KINDS, TERMS, TERMS):
                statement = s(kind, left, right)
                self.assertEqual(model.evaluate(statement), evaluate_sets(statement, named["terms"]),
                                 (model.raw_mask, statement))

    def test_arbitrary_small_models_preserve_relations_when_abstracted(self):
        # Includes multiple witnesses per region, unlike the canonical models.
        for size in (1, 2, 3):
            universe = tuple(f"u{i}" for i in range(size))
            subsets = [set(itertools.compress(universe, bits))
                       for bits in itertools.product((False, True), repeat=size)]
            for a, b, c in itertools.product(subsets, repeat=3):
                terms = {"A": a, "B": b, "C": c}
                abstract = RegionModel(mask_for_sets(universe, terms))
                for kind, left, right in itertools.product(KINDS, TERMS, TERMS):
                    statement = s(kind, left, right)
                    self.assertEqual(evaluate_sets(statement, terms), abstract.evaluate(statement))

    def test_named_universe_validation(self):
        with self.assertRaises(ValueError):
            mask_for_sets([], {"A": [], "B": [], "C": []})
        with self.assertRaises(ValueError):
            mask_for_sets(["x"], {"A": ["y"], "B": [], "C": []})


class SemanticsTests(unittest.TestCase):
    def test_empty_subject_universals_are_vacuously_true(self):
        model = RegionModel(1)
        self.assertTrue(model.evaluate(s("A", "A", "B")))
        self.assertTrue(model.evaluate(s("E", "A", "B")))
        self.assertFalse(model.evaluate(s("I", "A", "B")))
        self.assertFalse(model.evaluate(s("O", "A", "B")))

    def test_contradictory_pairs_for_every_model_and_term_pair(self):
        for model in models():
            for left, right in itertools.product(TERMS, repeat=2):
                self.assertNotEqual(model.evaluate(s("A", left, right)), model.evaluate(s("O", left, right)))
                self.assertNotEqual(model.evaluate(s("E", left, right)), model.evaluate(s("I", left, right)))

    def test_only_E_and_I_have_unconditional_simple_converse(self):
        for kind in KINDS:
            argument = Argument(kind, (s(kind, "A", "B"),), s(kind, "B", "A"))
            result = check_argument(argument, "empty_terms_allowed")
            self.assertEqual(result["valid"], kind in ("E", "I"))

    def test_I_does_not_imply_O_even_when_all_terms_exist(self):
        argument = Argument("bad", (s("I", "A", "B"),), s("O", "A", "B"))
        for regime in REGIMES:
            self.assertFalse(check_argument(argument, regime)["valid"])
        equal = RegionModel(128)
        self.assertTrue(equal.evaluate(s("I", "A", "B")))
        self.assertFalse(equal.evaluate(s("O", "A", "B")))


class DisplayedFormsTests(unittest.TestCase):
    def test_nine_unique_catalog_labels(self):
        self.assertEqual([a.label for a in CATALOG], ["A1", "A2", "A3", "A4", "A5", "E1", "E2", "E3", "E4"])

    def test_catalog_under_all_three_regimes(self):
        for regime in REGIMES:
            for argument in CATALOG:
                with self.subTest(regime=regime, argument=argument.label):
                    result = check_argument(argument, regime)
                    self.assertTrue(result["premises_satisfiable"])
                    self.assertEqual(result["valid"], not (regime == "empty_terms_allowed" and argument.label == "A5"))

    def test_A5_exact_counterexample_masks(self):
        result = check_argument(CATALOG[4], "empty_terms_allowed")
        self.assertEqual(result["premise_satisfying_raw_masks"], 16)
        self.assertEqual(result["distinct_premise_satisfying_models"], 15)
        self.assertEqual(result["counterexample_raw_masks"], [0, 1, 16, 17, 64, 65, 80, 81])
        self.assertEqual(result["distinct_counterexample_models"], 7)

    def test_A5_conclusion_iff_A_exists_under_its_premises(self):
        a5 = CATALOG[4]
        for model in models():
            if all(model.evaluate(p) for p in a5.premises):
                self.assertEqual(model.evaluate(a5.conclusion), model.term_nonempty("A"))

    def test_all_28_explicit_conversion_variants_have_same_results(self):
        self.assertEqual(sum(len(ei_conversion_variants(a)) for a in CATALOG), 28)
        for argument in CATALOG:
            for variant in ei_conversion_variants(argument):
                for regime in REGIMES:
                    self.assertEqual(check_argument(variant, regime)["counterexample_raw_masks"],
                                     check_argument(argument, regime)["counterexample_raw_masks"])


class ExamplesTests(unittest.TestCase):
    def test_all_named_example_premises_are_true(self):
        for value in explicit_examples().values():
            for example in value if isinstance(value, list) else [value]:
                self.assertTrue(example["all_premises_true"], example["name"])

    def test_disjoint_wholly_contained_and_partial_overlap_models(self):
        examples = explicit_examples()["no_inference_from_A_subset_B_and_C_disjoint_A"]
        expected = [
            {"A": False, "E": True, "I": False, "O": True},
            {"A": True, "E": False, "I": True, "O": False},
            {"A": False, "E": False, "I": True, "O": True},
        ]
        self.assertEqual([e["C_to_B_relations"] for e in examples], expected)
        self.assertTrue(all(all(e["terms"][t] for t in TERMS) for e in examples))

    def test_explicit_counterexamples_really_falsify_conclusions(self):
        examples = explicit_examples()
        for name in ("A5_empty_A_counterexample", "I_does_not_imply_O",
                     "pear_tree_equality_counterexample", "common_subject_empty_A_counterexample"):
            self.assertFalse(examples[name]["conclusion_true"], name)

    def test_strict_pear_tree_model_has_extra_tree_witness(self):
        example = explicit_examples()["pear_tree_strict_inclusion_example"]
        self.assertTrue(example["conclusion_true"])
        self.assertEqual(set(example["terms"]["A"]) - set(example["terms"]["B"]), {"oak"})


class InventoryTests(unittest.TestCase):
    def test_exact_candidate_scope_and_no_duplicate_ordered_formulas(self):
        for kind in ("A", "E"):
            candidates = fixed_first_candidates(kind)
            self.assertEqual(len(candidates), 128)
            self.assertEqual(len({str(a) for a in candidates}), 128)
            self.assertEqual(len({str(a.premises[1]) for a in candidates}), 16)
            for second in {a.premises[1] for a in candidates}:
                matching = [a for a in candidates if a.premises[1] == second]
                self.assertEqual(len(matching), 8)
                shared = ({second.subject, second.predicate} & {"A", "B"}).pop()
                remaining = "B" if shared == "A" else "A"
                self.assertTrue(all({a.conclusion.subject, a.conclusion.predicate} == {"C", remaining} for a in matching))
        with self.assertRaises(ValueError):
            fixed_first_candidates("I")

    def test_each_displayed_form_matches_itself_and_renamings(self):
        for argument in CATALOG:
            self.assertIn(argument.label, catalog_matches(argument))
            for permutation in itertools.permutations(TERMS):
                renamed = argument.renamed(dict(zip(TERMS, permutation)))
                self.assertIn(argument.label, catalog_matches(renamed))

    def test_A_and_O_are_not_silently_converted_by_matching(self):
        self.assertNotEqual(s("A", "A", "B").canonical(), s("A", "B", "A").canonical())
        self.assertNotEqual(s("O", "A", "B").canonical(), s("O", "B", "A").canonical())
        self.assertEqual(s("E", "A", "B").canonical(), s("E", "B", "A").canonical())
        self.assertEqual(s("I", "A", "B").canonical(), s("I", "B", "A").canonical())

    def test_premise_exchange_is_explicit_and_optional(self):
        chain = Argument("chain", (s("A", "A", "B"), s("A", "B", "C")), s("A", "A", "C"))
        self.assertEqual(catalog_matches(chain), ())
        self.assertEqual(catalog_matches(chain, True), ("A1",))

    def test_common_subject_case_is_existence_dependent_and_unmatched(self):
        common = Argument("common", (s("A", "A", "B"), s("A", "A", "C")), s("I", "C", "B"))
        self.assertEqual(catalog_matches(common), ())
        self.assertEqual(catalog_matches(common, True), ())
        for regime in REGIMES:
            self.assertEqual(check_argument(common, regime)["valid"], regime != "empty_terms_allowed")

    def test_inventory_has_witnesses_for_every_invalid_candidate(self):
        for regime in REGIMES:
            for kind in ("A", "E"):
                audit = audit_fixed_first(kind, regime)
                self.assertEqual(len(audit["rows"]), 128)
                for row in audit["rows"]:
                    self.assertTrue(row["premises_satisfiable"])
                    self.assertEqual(row["valid"], not bool(row["counterexample_raw_masks"]))
                    self.assertEqual(row["first_counterexample"] is None, row["valid"])


class ReportTests(unittest.TestCase):
    def test_report_is_serializable_and_core_results_are_explicit(self):
        report = build_report()
        self.assertEqual(json.loads(json.dumps(report)), report)
        self.assertEqual(len(report["fixed_first_audits"]), 6)
        self.assertTrue(report["A5_conclusion_equivalent_to_A_existence_given_premises"])
        rendered = render_text(report)
        self.assertIn("255 distinct nonempty-universe models", rendered)
        self.assertIn("Historical 'form' equivalence may be broader", rendered)
        self.assertIn("A(A,B) & A(A,C) => I(C,B)", rendered)

    def test_cli_writes_parseable_outputs_and_succeeds(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            completed = subprocess.run(
                [sys.executable, str(root / "reproduce.py"), "--output", temporary],
                cwd=root, text=True, capture_output=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            destination = Path(temporary)
            report = json.loads((destination / "report.json").read_text(encoding="utf-8"))
            environment = json.loads((destination / "environment.json").read_text(encoding="utf-8"))
            self.assertEqual(report["model_space"]["raw_masks"], 256)
            self.assertFalse(environment["network_used_by_reproduction"])
            self.assertEqual(len(environment["source_sha256"]), 3)
            self.assertEqual((destination / "report.txt").read_text(encoding="utf-8"), render_text(report))


if __name__ == "__main__":
    unittest.main()
