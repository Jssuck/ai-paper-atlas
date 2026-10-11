import contextlib
import io
import itertools
import json
from pathlib import Path
import tempfile
import unittest

from experiments import run
from logic import MAX_ATOMS, Theory, evaluate
from main import check_payload, main


class EvaluationTests(unittest.TestCase):
    def test_truth_tables(self):
        for p, q in itertools.product([False, True], repeat=2):
            world = {"p": p, "q": q}
            for op, expected in [("and", p and q), ("or", p or q),
                                 ("implies", not p or q)]:
                self.assertIs(evaluate([op, "p", "q"], world), expected)
            self.assertIs(evaluate(["not", "p"], world), not p)

    def test_constants_and_zero_atoms(self):
        self.assertTrue(evaluate(True, {}))
        self.assertFalse(evaluate(False, {}))
        self.assertEqual(Theory([]).worlds, ((),))
        self.assertFalse(Theory([]).check([], False)["valid"])

    def test_nested_substitution(self):
        p, q = ["and", "a", "b"], ["or", "c", "d"]
        result = Theory(["a", "b", "c", "d"]).check([["implies", p, q], p], q)
        self.assertTrue(result["valid"])
        self.assertTrue(result["premises_consistent"])

    def test_no_short_circuit_validation_escape(self):
        with self.assertRaises(ValueError):
            evaluate(["and", False, "undeclared"], {})

    def test_unknown_operator_and_arity(self):
        for expression in [[], ["xor", "p", "p"], ["not", "p", "p"],
                           ["and", "p"], [["not"], "p"], 1, None, {}]:
            with self.subTest(expression=expression), self.assertRaises(ValueError):
                evaluate(expression, {"p": True})

    def test_boolean_values_are_strict(self):
        for value in [0, 1, "true", None]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                evaluate("p", {"p": value})

    def test_world_must_be_dictionary(self):
        with self.assertRaises(ValueError):
            evaluate(True, [])

    def test_depth_limit(self):
        expression = "p"
        for _ in range(66):
            expression = ["not", expression]
        with self.assertRaises(ValueError):
            evaluate(expression, {"p": True})


class TheoryTests(unittest.TestCase):
    def test_atom_validation(self):
        for atoms in ["pq", ["p", "p"], [""], ["a b"], [3],
                      [f"p{i}" for i in range(MAX_ATOMS + 1)]]:
            with self.subTest(atoms=atoms), self.assertRaises(ValueError):
                Theory(atoms)

    def test_constraints_validation(self):
        for constraints in ["p", [["implies", "p", "q"]]]:
            with self.subTest(constraints=constraints), self.assertRaises(ValueError):
                Theory(["p"], constraints)

    def test_world_validation(self):
        for worlds in [{}, [{}], [{"p": 1}], [{"p": True, "q": False}], [None]]:
            with self.subTest(worlds=worlds), self.assertRaises(ValueError):
                Theory(["p"], allowed_worlds=worlds)

    def test_duplicate_worlds_normalized_and_sorted(self):
        theory = Theory(["p"], allowed_worlds=[{"p": True}, {"p": False}, {"p": True}])
        self.assertEqual(theory.worlds, ((False,), (True,)))

    def test_constraints_intersect_explicit_worlds(self):
        theory = Theory(["p"], ["p"], [{"p": False}, {"p": True}])
        self.assertEqual(theory.worlds, ((True,),))

    def test_input_mutation_cannot_change_theory(self):
        rule, world = ["not", "p"], {"p": False}
        theory = Theory(["p"], [rule], [world])
        rule[1], world["p"] = "q", True
        self.assertEqual(theory.constraints, (("not", "p"),))
        self.assertEqual(theory.worlds, ((False,),))

    def test_explicit_empty_is_not_unrestricted(self):
        self.assertEqual(len(Theory(["p"]).worlds), 2)
        result = Theory(["p"], allowed_worlds=[]).check([], "p")
        self.assertTrue(result["valid"])
        self.assertFalse(result["theory_consistent"])
        self.assertIn("empty theory", result["warning"])

    def test_premises_must_be_sequence(self):
        with self.assertRaises(ValueError):
            Theory(["p"]).check("p", "p")

    def test_invalid_conclusion_checked_even_in_empty_theory(self):
        with self.assertRaises(ValueError):
            Theory(["p"], allowed_worlds=[]).check([], "q")

    def test_deterministic_atom_and_counterexample_order(self):
        a = Theory(["q", "p"]).check([], "p")
        b = Theory(["p", "q"]).check([], "p")
        self.assertEqual(a, b)
        self.assertEqual(a["counterexamples"], [{"p": False, "q": False},
                                                 {"p": False, "q": True}])


class ReadingExperimentsTests(unittest.TestCase):
    def setUp(self):
        self.report = run()
        self.cases = self.report["cases"]

    def test_mp_mt_valid_and_nonvacuous(self):
        for name in ["modus_ponens", "modus_tollens"]:
            self.assertTrue(self.cases[name]["valid"])
            self.assertTrue(self.cases[name]["premises_consistent"])

    def test_both_fallacies_same_counterexample(self):
        for name in ["denying_antecedent", "affirming_consequent"]:
            self.assertEqual(self.cases[name]["counterexamples"], [{"p": False, "q": True}])

    def test_conditional_alone_asserts_neither_constituent(self):
        for part in ["p", "q", "not_p", "not_q"]:
            self.assertFalse(self.cases["conditional_alone_not_" + part]["valid"])

    def test_single_truth_does_not_establish_law(self):
        self.assertTrue(self.report["single_assignment"]["material_implication_true"])
        self.assertFalse(self.cases["unrestricted_p_entails_q"]["valid"])
        self.assertTrue(self.cases["constrained_p_entails_q"]["valid"])
        self.assertEqual(self.cases["constrained_p_entails_q"],
                         self.cases["explicit_worlds_p_entails_q"])

    def test_exhaustiveness_and_exclusivity_separate(self):
        expected = {"neither": (False, False), "exhaustive": (True, False),
                    "exclusive": (False, True), "both": (True, True)}
        for label, results in expected.items():
            self.assertEqual(self.cases[label + "_not_body_to_spirit"]["valid"], results[0])
            self.assertEqual(self.cases[label + "_body_to_not_spirit"]["valid"], results[1])

    def test_disjunction_counterexamples(self):
        self.assertEqual(self.cases["exclusive_not_body_to_spirit"]["counterexamples"],
                         [{"body": False, "spirit": False}])
        self.assertEqual(self.cases["exhaustive_body_to_not_spirit"]["counterexamples"],
                         [{"body": True, "spirit": True}])

    def test_inconsistency_warnings(self):
        for name in ["inconsistent_premises", "empty_theory"]:
            self.assertTrue(self.cases[name]["valid"])
            self.assertFalse(self.cases[name]["premises_consistent"])
            self.assertIn("vacuous", self.cases[name]["warning"])
        self.assertTrue(self.cases["inconsistent_premises"]["theory_consistent"])
        self.assertFalse(self.cases["empty_theory"]["theory_consistent"])

    def test_counterexamples_really_refute(self):
        theory = Theory(["p", "q", "r"])
        premises = [["implies", "p", "q"], "r"]
        result = theory.check(premises, "p")
        for world in result["counterexamples"]:
            self.assertTrue(all(evaluate(p, world) for p in premises))
            self.assertFalse(evaluate("p", world))


class CLITests(unittest.TestCase):
    def test_payload_validation(self):
        good = {"atoms": ["p"], "premises": [], "conclusion": "p"}
        for bad in [[], {}, {**good, "typo": []}, {**good, "conclusion": "q"}]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                check_payload(bad)

    def test_demo_deterministic_json(self):
        outputs = []
        for _ in range(2):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main(["demo"]), 0)
            outputs.append(out.getvalue())
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(len(json.loads(outputs[0])["cases"]), 21)

    def test_check_invalid_argument_is_successful_computation(self):
        path = Path(__file__).resolve().parents[1] / "example.json"
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(main(["check", str(path)]), 0)
        self.assertFalse(json.loads(out.getvalue())["valid"])

    def test_malformed_or_duplicate_json(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            path = Path(directory) / "bad.json"
            for contents in ['{', '{"atoms": [], "atoms": []}']:
                path.write_text(contents, encoding="utf-8")
                error = io.StringIO()
                with contextlib.redirect_stderr(error):
                    self.assertEqual(main(["check", str(path)]), 2)
                self.assertIn("input error", error.getvalue())

    def test_missing_file(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(["check", str(Path(directory) / "missing")]), 2)


if __name__ == "__main__":
    unittest.main()
