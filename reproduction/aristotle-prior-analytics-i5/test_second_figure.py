"""Regression tests with an independent set-based oracle (stdlib unittest)."""
import ast
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import second_figure as sf

PYTHON = [sys.executable] + (["-" + "O" * sys.flags.optimize] if sys.flags.optimize else [])


def oracle_model(mask):
    """Independent Boolean-tuple decoding, using all 8 possible memberships."""
    selected = [bits for index, bits in enumerate(product((False, True), repeat=3))
                if (mask // (2 ** index)) % 2]
    return selected, {name: {index for index, bits in enumerate(selected) if bits[column]}
                      for column, name in enumerate(("P", "M", "S"))}


def oracle_truth(q, x, y):
    if q == "A":
        return all(obj in y for obj in x)
    if q == "E":
        return all(obj not in y for obj in x)
    if q == "I":
        return any(obj in y for obj in x)
    if q == "O":
        return any(obj not in y for obj in x)
    raise ValueError(q)


def oracle_policy(terms, policy):
    if policy == sf.Policy.ALLOW_EMPTY:
        return True
    if policy == sf.Policy.SUBJECT_NONEMPTY:
        return bool(terms["S"])
    if policy == sf.Policy.ALL_NONEMPTY:
        return all(terms.values())
    raise ValueError(policy)


def oracle_countermodels(mood, policy):
    q, r, t = mood
    out = []
    for mask in range(1, 256):
        universe, terms = oracle_model(mask)
        p, m, s = terms["P"], terms["M"], terms["S"]
        if (oracle_policy(terms, policy) and oracle_truth(q, p, m)
                and oracle_truth(r, s, m) and not oracle_truth(t, s, p)):
            out.append((len(universe), mask))
    return sorted(out)


class SemanticTests(unittest.TestCase):
    def test_defining_examples(self):
        examples = [(set(), set(), (True, True, False, False)),
                    ({1}, {1, 2}, (True, False, True, False)),
                    ({1, 2}, {1}, (False, False, True, True)),
                    ({1}, {2}, (False, True, False, True))]
        for x, y, expected in examples:
            self.assertEqual(tuple(sf.evaluate_categorical(q, x, y) for q in sf.QUANTIFIERS), expected)

    def test_duplicates_do_not_change_set_semantics(self):
        for q in sf.QUANTIFIERS:
            self.assertEqual(sf.evaluate_categorical(q, [1, 1, 2], [1, 1]),
                             sf.evaluate_categorical(q, {1, 2}, {1}))

    def test_atom_bits_are_explicit(self):
        expected = {0: (), 1: ("S",), 2: ("M",), 3: ("M", "S"),
                    4: ("P",), 5: ("P", "S"), 6: ("P", "M"), 7: ("P", "M", "S")}
        for atom, names in expected.items():
            self.assertEqual(tuple(t for t in sf.TERMS if sf.extension(1 << atom, t)), names)

    def test_all_atomic_truths_agree_with_independent_oracle(self):
        comparisons = 0
        for mask in range(1, 256):
            _, terms = oracle_model(mask)
            for q, x, y in product(sf.QUANTIFIERS, sf.TERMS, sf.TERMS):
                expected = oracle_truth(q, terms[x], terms[y])
                self.assertEqual(sf.holds(mask, q, x, y), expected, (mask, q, x, y))
                self.assertEqual(sf.evaluate_categorical(q, sf.extension(mask, x),
                                                        sf.extension(mask, y)), expected)
                comparisons += 1
        self.assertEqual(comparisons, 9180)

    def test_A_O_and_E_I_are_complements(self):
        for mask, x, y in product(range(1, 256), sf.TERMS, sf.TERMS):
            self.assertNotEqual(sf.holds(mask, "A", x, y), sf.holds(mask, "O", x, y))
            self.assertNotEqual(sf.holds(mask, "E", x, y), sf.holds(mask, "I", x, y))

    def test_E_and_I_are_symmetric(self):
        for mask, q, x, y in product(range(1, 256), ("E", "I"), sf.TERMS, sf.TERMS):
            self.assertEqual(sf.holds(mask, q, x, y), sf.holds(mask, q, y, x))

    def test_A_and_O_are_not_generally_symmetric(self):
        mask = (1 << 4) | (1 << 5)  # P={x1,x2}, S={x2}
        self.assertTrue(sf.holds(mask, "A", "S", "P"))
        self.assertFalse(sf.holds(mask, "A", "P", "S"))
        self.assertTrue(sf.holds(mask, "O", "P", "S"))
        self.assertFalse(sf.holds(mask, "O", "S", "P"))

    def test_Clause_representation(self):
        clause = sf.Clause("E", "S", "M")
        self.assertEqual(str(clause), "E(S,M)")
        self.assertTrue(clause.holds(1))


class SupportTests(unittest.TestCase):
    def test_policy_counts(self):
        self.assertEqual(len(list(sf.iter_supports(sf.Policy.ALLOW_EMPTY))), 255)
        self.assertEqual(len(list(sf.iter_supports(sf.Policy.ALL_NONEMPTY))), 218)
        self.assertEqual(len(list(sf.iter_supports(sf.Policy.SUBJECT_NONEMPTY))), 240)

    def test_supports_unique_complete_and_size_sorted(self):
        for policy in sf.Policy:
            masks = list(sf.iter_supports(policy))
            self.assertEqual(len(masks), len(set(masks)))
            self.assertEqual(masks, sorted(masks, key=lambda n: (n.bit_count(), n)))
            expected = {mask for mask in range(1, 256) if oracle_policy(oracle_model(mask)[1], policy)}
            self.assertEqual(set(masks), expected)

    def test_string_policy_equals_enum(self):
        for policy in sf.Policy:
            self.assertEqual(list(sf.iter_supports(policy)), list(sf.iter_supports(policy.value)))

    def test_all_supports_realize_and_round_trip(self):
        for mask in range(1, 256):
            model = sf.concrete_model(mask)
            self.assertEqual(sf.compress_model(**model), mask)
            self.assertEqual(len(model["universe"]), mask.bit_count())
            self.assertEqual(len(model["universe"]), len(set(model["universe"])))
            self.assertEqual(model, sf.concrete_model(mask))

    def test_outside_all_terms_is_preserved(self):
        self.assertEqual(sf.compress_model(["outside"], [], [], []), 1)
        self.assertEqual(sf.occupied_atoms(1), (0,))
        self.assertEqual(sf.concrete_model(1), {"universe": ["x1"], "P": [], "M": [], "S": []})

    def test_multiplicity_is_compressed(self):
        self.assertEqual(sf.compress_model(range(100), range(100), range(100), range(100)), 128)
        self.assertEqual(sf.compress_model(range(5), [0, 1, 2], [2, 3], [3]),
                         (1 << 0) | (1 << 4) | (1 << 6) | (1 << 3))

    def test_exhaustive_labeled_models_of_sizes_one_through_three(self):
        checked = 0
        for n in (1, 2, 3):
            universe = set(range(n))
            for memberships in product(range(8), repeat=n):
                terms = {term: {obj for obj in universe if memberships[obj] & bit}
                         for term, bit in (("P", 4), ("M", 2), ("S", 1))}
                support = sf.compress_model(universe, **terms)
                self.assertEqual(set(sf.occupied_atoms(support)), set(memberships))
                for q, x, y in product(sf.QUANTIFIERS, sf.TERMS, sf.TERMS):
                    self.assertEqual(sf.holds(support, q, x, y), oracle_truth(q, terms[x], terms[y]))
                for policy in sf.Policy:
                    self.assertEqual(sf.satisfies_policy(support, policy), oracle_policy(terms, policy))
                checked += 1
        self.assertEqual(checked, 584)


class ClassificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = {(policy, mood): sf.classify_mood(mood, policy)
                       for policy in sf.Policy for mood in sf.all_moods()}

    def test_64_distinct_moods(self):
        self.assertEqual(len(sf.all_moods()), 64)
        self.assertEqual(len(set(sf.all_moods())), 64)

    def test_exact_valid_moods_empty_terms_allowed(self):
        valid = {mood for mood in sf.all_moods() if self.results[sf.Policy.ALLOW_EMPTY, mood].valid}
        self.assertEqual(valid, {"EAE", "AEE", "EIO", "AOO"})

    def test_exact_valid_moods_all_terms_nonempty(self):
        valid = {mood for mood in sf.all_moods() if self.results[sf.Policy.ALL_NONEMPTY, mood].valid}
        self.assertEqual(valid, {"EAE", "AEE", "EIO", "AOO", "EAO", "AEO"})

    def test_subject_existence_is_enough_for_weakened_conclusions(self):
        valid = {mood for mood in sf.all_moods() if self.results[sf.Policy.SUBJECT_NONEMPTY, mood].valid}
        self.assertEqual(valid, {"EAE", "AEE", "EIO", "AOO", "EAO", "AEO"})

    def test_no_affirmative_conclusion_under_any_tested_policy(self):
        for (policy, mood), result in self.results.items():
            if mood[2] in "AI":
                self.assertFalse(result.valid, (policy, mood))

    def test_every_premise_pair_is_satisfiable(self):
        for result in self.results.values():
            self.assertGreater(result.premise_support_count, 0)
            self.assertFalse(result.vacuous)

    def test_full_classification_and_smallest_witness_independently(self):
        comparisons = 0
        for (policy, mood), result in self.results.items():
            witnesses = oracle_countermodels(mood, policy)
            self.assertEqual(result.valid, not witnesses, (policy, mood))
            if witnesses:
                self.assertEqual(result.countermodel_support, witnesses[0][1], (policy, mood))
            else:
                self.assertIsNone(result.countermodel_support)
            comparisons += 1
        self.assertEqual(comparisons, 192)

    def test_every_published_witness_satisfies_premises_and_falsifies_conclusion(self):
        checked = 0
        for (policy, mood), result in self.results.items():
            if result.valid:
                continue
            model = result.as_dict()["countermodel"]
            q, r, t = mood
            p, m, s = set(model["P"]), set(model["M"]), set(model["S"])
            self.assertTrue(oracle_policy({"P": p, "M": m, "S": s}, policy))
            self.assertTrue(oracle_truth(q, p, m))
            self.assertTrue(oracle_truth(r, s, m))
            self.assertFalse(oracle_truth(t, s, p))
            self.assertEqual(len(model["universe"]), result.countermodel_support.bit_count())
            checked += 1
        self.assertEqual(checked, 176)

    def test_premise_support_counts_independently(self):
        for policy in sf.Policy:
            for q, r in product(sf.QUANTIFIERS, repeat=2):
                count = 0
                for mask in range(1, 256):
                    _, terms = oracle_model(mask)
                    if (oracle_policy(terms, policy) and oracle_truth(q, terms["P"], terms["M"])
                            and oracle_truth(r, terms["S"], terms["M"])):
                        count += 1
                self.assertEqual(self.results[policy, q+r+"A"].premise_support_count, count)

    def test_IE_reversal_not_forward_inference(self):
        premises = (sf.Clause("I", "P", "M"), sf.Clause("E", "S", "M"))
        for policy in sf.Policy:
            self.assertTrue(sf.classify(premises, sf.Clause("O", "P", "S"), policy).valid)
            self.assertFalse(sf.classify(premises, sf.Clause("O", "S", "P"), policy).valid)
        # Nonempty P, M, S: P={a,b}, M={a}, S={b}.
        support = sf.compress_model({"a", "b"}, {"a", "b"}, {"a"}, {"b"})
        self.assertTrue(all(clause.holds(support) for clause in premises))
        self.assertFalse(sf.holds(support, "O", "S", "P"))
        self.assertTrue(sf.holds(support, "O", "P", "S"))
        self.assertEqual(support, 96)

    def test_EI_forward_and_reverse_are_not_conflated(self):
        premises = (sf.Clause("E", "P", "M"), sf.Clause("I", "S", "M"))
        for policy in sf.Policy:
            self.assertTrue(sf.classify(premises, sf.Clause("O", "S", "P"), policy).valid)
            self.assertFalse(sf.classify(premises, sf.Clause("O", "P", "S"), policy).valid)

    def test_weakening_counterexamples_have_empty_S(self):
        for mood in ("EAO", "AEO"):
            result = self.results[sf.Policy.ALLOW_EMPTY, mood]
            self.assertFalse(result.valid)
            self.assertFalse(sf.extension(result.countermodel_support, "S"))

    def test_inconsistent_premises_are_flagged_vacuous(self):
        result = sf.classify([sf.Clause("A", "P", "M"), sf.Clause("O", "P", "M")],
                             sf.Clause("I", "S", "P"))
        self.assertTrue(result.valid)
        self.assertTrue(result.vacuous)
        self.assertEqual(result.premise_support_count, 0)

    def test_empty_premise_list_means_no_assumptions(self):
        self.assertTrue(sf.classify([], sf.Clause("A", "P", "P")).valid)
        self.assertFalse(sf.classify([], sf.Clause("I", "P", "P")).valid)
        self.assertTrue(sf.classify([], sf.Clause("I", "P", "P"), sf.Policy.ALL_NONEMPTY).valid)


class InvalidInputTests(unittest.TestCase):
    def test_validation_does_not_use_optimizable_assert_statements(self):
        tree = ast.parse(Path(sf.__file__).read_text())
        self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(tree)))

    def test_bad_support_values(self):
        for value in (0, -1, 256, 1024):
            with self.subTest(value=value), self.assertRaises(ValueError):
                sf.occupied_atoms(value)
        for value in (True, False, 1.0, "1", None):
            with self.subTest(value=value), self.assertRaises(TypeError):
                sf.occupied_atoms(value)

    def test_bad_quantifiers(self):
        for value in ("", "a", "U", "AE"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                sf.holds(1, value, "P", "M")
            with self.assertRaises(ValueError):
                sf.evaluate_categorical(value, [], [])
        with self.assertRaises(TypeError):
            sf.evaluate_categorical(None, [], [])

    def test_bad_terms(self):
        for value in ("", "p", "X"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                sf.extension(1, value)
            with self.assertRaises(ValueError):
                sf.Clause("A", "P", value)
        with self.assertRaises(TypeError):
            sf.Clause("A", [], "P")

    def test_bad_policies(self):
        for value in ("", "nonempty", "ALLOW_EMPTY"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                sf.iter_supports(value)
        for value in (None, 1, []):
            with self.subTest(value=value), self.assertRaises(TypeError):
                sf.iter_supports(value)

    def test_bad_moods(self):
        for value in ("", "AE", "AEEE", "eae", "AXO", "E A"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                sf.classify_mood(value)
        for value in (None, 123, ["E", "A", "E"]):
            with self.subTest(value=value), self.assertRaises(TypeError):
                sf.classify_mood(value)

    def test_bad_model(self):
        with self.assertRaises(ValueError):
            sf.compress_model([], [], [], [])
        with self.assertRaises(ValueError):
            sf.compress_model([1], [2], [], [])
        with self.assertRaises(TypeError):
            sf.compress_model([[1]], [], [], [])

    def test_bad_classify_clauses(self):
        with self.assertRaises(TypeError):
            sf.classify(["A(P,M)"], sf.Clause("E", "S", "P"))
        with self.assertRaises(TypeError):
            sf.classify([], "E(S,P)")


class ReportTests(unittest.TestCase):
    def test_saved_reports_match_generated_results(self):
        root = Path(sf.__file__).resolve().parent
        report = sf.make_report()
        self.assertEqual(json.loads((root / "report.json").read_text()), report)
        self.assertEqual((root / "REPORT.md").read_text(), sf.render_markdown(report))

    def test_json_report_round_trip_and_completeness(self):
        report = sf.make_report()
        self.assertEqual(json.loads(json.dumps(report)), report)
        for policy in sf.Policy:
            self.assertEqual(set(report["policies"][policy.value]["results"]), set(sf.all_moods()))
        self.assertIn("Direction matters: IE", sf.render_markdown(report))

    def test_cli_generates_both_reports(self):
        script = Path(sf.__file__).resolve()
        with tempfile.TemporaryDirectory() as tmp:
            json_path, md_path = Path(tmp) / "report.json", Path(tmp) / "REPORT.md"
            proc = subprocess.run(PYTHON + [str(script), "--json", str(json_path),
                                   "--markdown", str(md_path)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(json_path.read_text()), sf.make_report())
            self.assertEqual(md_path.read_text(), sf.render_markdown(sf.make_report()))

    def test_cli_rejects_unknown_argument(self):
        proc = subprocess.run(PYTHON + [sf.__file__, "--not-a-real-option"],
                              capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("unrecognized arguments", proc.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
