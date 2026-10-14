"""Author-written finite checks; direct quantifier oracle is independently coded.

This is not an independent audit and is not a general mathematical proof.
"""

from dataclasses import FrozenInstanceError
import ast
from itertools import combinations_with_replacement, product
import json
from pathlib import Path
import unittest

from demo import build_report, existential_witness
from logic import (
    Language, Model, Prop, ValidationError, entails, enumerate_models, evaluate,
    is_admissible,
)
from proofs import Step, check_certificate


def oracle_models(terms, required=frozenset()):
    """Independent support generation via Boolean products, not integer masks."""
    assignments = list(product((False, True), repeat=len(terms)))
    for included in product((False, True), repeat=len(assignments)):
        universe = tuple(dict(zip(terms, row)) for row, used in zip(assignments, included) if used)
        if universe and all(any(obj[t] for obj in universe) for t in required):
            yield universe


def oracle_truth(prop, universe):
    """Direct quantifiers over a concrete dictionary-valued domain."""
    s, p = prop.subject, prop.predicate
    if prop.kind == "A":
        return all((not obj[s]) or obj[p] for obj in universe)
    if prop.kind == "E":
        return all((not obj[s]) or (not obj[p]) for obj in universe)
    if prop.kind == "I":
        return any(obj[s] and obj[p] for obj in universe)
    if prop.kind == "O":
        return any(obj[s] and not obj[p] for obj in universe)
    raise ValueError("oracle received an unknown kind")


def encode_universe(terms, universe):
    return tuple(sorted(sum(2 ** i for i, term in enumerate(terms) if obj[term]) for obj in universe))


class ValidationTests(unittest.TestCase):
    def test_production_validation_does_not_use_assert(self):
        root = Path(__file__).resolve().parent
        for name in ("logic.py", "proofs.py", "demo.py", "verify.py"):
            tree = ast.parse((root / name).read_text(encoding="utf-8"))
            self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(tree)), name)

    def test_prop_validation_and_immutability(self):
        for kind, subject, predicate in [("a", "S", "P"), (True, "S", "P"),
                                         ("A", "", "P"), ("I", " S", "P"), ("E", 1, "P")]:
            with self.subTest(values=(kind, subject, predicate)), self.assertRaises(ValidationError):
                Prop(kind, subject, predicate)
        p = Prop("A", "人", "动物")
        with self.assertRaises(FrozenInstanceError):
            p.kind = "E"

    def test_language_validation(self):
        for terms in [[], (), ("S", "S"), ("S", "M", "P", "Q"), (1,), ("",)]:
            with self.subTest(terms=terms), self.assertRaises(ValidationError):
                Language(terms)
        for required in [set(), ("S",), frozenset(("X",)), frozenset((1,))]:
            with self.subTest(required=required), self.assertRaises(ValidationError):
                Language(("S",), required)
        with self.assertRaises(FrozenInstanceError):
            Language(("S",)).terms = ("P",)

    def test_model_validation(self):
        for support in [[], (), (True,), (-1,), (4,), (0, 0), (2, 1), ("1",), (0.0,)]:
            with self.subTest(support=support), self.assertRaises(ValidationError):
                Model(("S", "P"), support)
        model = Model(("S", "P"), (0, 1, 3))
        self.assertEqual(model.members("S"), (1, 3))
        with self.assertRaises(ValidationError):
            model.members("X")
        with self.assertRaises(FrozenInstanceError):
            model.support = (0,)

    def test_public_api_rejects_bad_types_and_undeclared_terms(self):
        lang = Language(("S", "P"))
        p = Prop("A", "S", "P")
        bad = Prop("A", "X", "P")
        invalid_calls = [
            lambda: entails(None, (), p), lambda: entails(lang, [p], p),
            lambda: entails(lang, ("A",), p), lambda: entails(lang, (), bad),
            lambda: entails(lang, (bad,), p), lambda: evaluate(p, None),
            lambda: evaluate(None, Model(lang.terms, (0,))),
            lambda: evaluate(bad, Model(lang.terms, (0,))),
            lambda: enumerate_models(None), lambda: is_admissible(None, None),
            lambda: is_admissible(lang, Model(("P", "S"), (0,))),
        ]
        for call in invalid_calls:
            with self.assertRaises(ValidationError):
                call()

    def test_step_validation(self):
        p = Prop("A", "S", "P")
        invalid_calls = [
            lambda: Step("A", "assume", assumption=0),
            lambda: Step(p, "import", assumption=0), lambda: Step(p, [], assumption=0),
            lambda: Step(p, "assume"), lambda: Step(p, "assume", assumption=True),
            lambda: Step(p, "assume", assumption=-1), lambda: Step(p, "assume", (0,), 0),
            lambda: Step(p, "a_trans", [0, 1]), lambda: Step(p, "a_trans", (0,)),
            lambda: Step(p, "a_trans", (False, 1)), lambda: Step(p, "a_trans", (-1, 0)),
            lambda: Step(p, "a_trans", (0, 1), 0),
        ]
        for call in invalid_calls:
            with self.assertRaises(ValidationError):
                call()

    def test_boundary_revalidates_forged_frozen_inputs(self):
        lang = Language(("S", "P"))
        prop = Prop("A", "S", "P")
        for field, value in [("assumption", -1), ("assumption", True), ("refs", (0,)),
                             ("rule", "invented"), ("claim", "A")]:
            step = Step(prop, "assume", assumption=0)
            object.__setattr__(step, field, value)
            with self.subTest(field=field, value=value), self.assertRaises(ValidationError):
                check_certificate(lang, (prop,), prop, (step,))
        for field, value in [("kind", "invalid"), ("subject", ""), ("predicate", 1)]:
            forged = Prop("A", "S", "P")
            object.__setattr__(forged, field, value)
            with self.assertRaises(ValidationError):
                entails(lang, (forged,), prop)
        for field, value in [("terms", ["S", "P"]), ("required_nonempty", {"S"}),
                             ("required_nonempty", frozenset(("X",)))]:
            forged = Language(("S", "P"))
            object.__setattr__(forged, field, value)
            with self.assertRaises(ValidationError):
                enumerate_models(forged)
        for support in [(), (True,), (-1,), (4,), (1, 0), [0]]:
            forged = Model(lang.terms, (0,))
            object.__setattr__(forged, "support", support)
            with self.assertRaises(ValidationError):
                evaluate(prop, forged)
            with self.assertRaises(ValidationError):
                forged.members("S")

    def test_incomplete_instances_rejected_at_boundaries(self):
        lang, prop = Language(("S", "P")), Prop("A", "S", "P")
        invalid_calls = [
            lambda: entails(object.__new__(Language), (), prop),
            lambda: entails(lang, (), object.__new__(Prop)),
            lambda: evaluate(prop, object.__new__(Model)),
            lambda: check_certificate(lang, (prop,), prop, (object.__new__(Step),)),
        ]
        for call in invalid_calls:
            with self.assertRaises(ValidationError):
                call()


class SemanticsTests(unittest.TestCase):
    def test_support_counts_and_independent_generation_all_policies(self):
        for n, expected in [(1, 3), (2, 15), (3, 255)]:
            terms = ("S", "M", "P")[:n]
            self.assertEqual(len(enumerate_models(Language(terms))), expected)
            for required_flags in product((False, True), repeat=n):
                required = frozenset(t for t, flag in zip(terms, required_flags) if flag)
                actual = {m.support for m in enumerate_models(Language(terms, required))}
                expected_set = {encode_universe(terms, u) for u in oracle_models(terms, required)}
                self.assertEqual(actual, expected_set)

    def test_truth_against_direct_quantifiers_every_support_and_proposition(self):
        checked = 0
        for n in (1, 2, 3):
            terms = ("S", "M", "P")[:n]
            props = [Prop(k, s, p) for k, s, p in product("AEIO", terms, terms)]
            for universe in oracle_models(terms):
                model = Model(terms, encode_universe(terms, universe))
                for prop in props:
                    self.assertEqual(evaluate(prop, model), oracle_truth(prop, universe))
                    checked += 1
        self.assertEqual(checked, 9432)

    def test_entailment_every_one_premise_problem_one_and_two_terms_all_policies(self):
        for n in (1, 2):
            terms = ("S", "P")[:n]
            props = [Prop(k, s, p) for k, s, p in product("AEIO", terms, terms)]
            for flags in product((False, True), repeat=n):
                required = frozenset(t for t, f in zip(terms, flags) if f)
                lang = Language(terms, required)
                universes = list(oracle_models(terms, required))
                for premise, conclusion in product(props, repeat=2):
                    satisfying = [u for u in universes if oracle_truth(premise, u)]
                    expected = all(oracle_truth(conclusion, u) for u in satisfying)
                    result = entails(lang, (premise,), conclusion)
                    self.assertEqual(result.holds, expected)
                    self.assertEqual(result.satisfying_premise_models, len(satisfying))
                    self.assertEqual(result.admissible_models, len(universes))
                    if result.countermodel is not None:
                        self.assertTrue(evaluate(premise, result.countermodel))
                        self.assertFalse(evaluate(conclusion, result.countermodel))

    def test_every_two_premise_problem_three_terms_against_oracle_bitsets(self):
        # Precompute independent oracle truth sets for all 666 unordered premise
        # multisets and 36 conclusions (23,976). This uses cached truth sets,
        # not repeated full calls to entails. Compare with direct quantifiers;
        # the full entails control flow is sampled separately below.
        terms = ("S", "M", "P")
        lang = Language(terms)
        models = enumerate_models(lang)
        props = [Prop(k, s, p) for k, s, p in product("AEIO", terms, terms)]
        universes = list(oracle_models(terms))
        production_sets = {p: frozenset(m.support for m in models if evaluate(p, m)) for p in props}
        oracle_sets = {p: frozenset(encode_universe(terms, u) for u in universes if oracle_truth(p, u)) for p in props}
        checked = 0
        for p, q in combinations_with_replacement(props, 2):
            production_common = production_sets[p] & production_sets[q]
            oracle_common = oracle_sets[p] & oracle_sets[q]
            for c in props:
                self.assertEqual(production_common <= production_sets[c], oracle_common <= oracle_sets[c])
                checked += 1
        self.assertEqual(checked, 23976)

    def test_full_entails_three_term_samples_all_policies(self):
        terms = ("S", "M", "P")
        props = [Prop(k, s, p) for k, s, p in product("AEIO", terms, terms)]
        # Deterministic 144 triples, across every required-nonempty policy.
        for flags in product((False, True), repeat=3):
            required = frozenset(t for t, f in zip(terms, flags) if f)
            lang = Language(terms, required)
            universes = list(oracle_models(terms, required))
            for i in range(144):
                premises = (props[i % 36], props[(i * 7 + i // 36) % 36])
                conclusion = props[(i * 11 + 3 * (i // 36)) % 36]
                good = [u for u in universes if all(oracle_truth(p, u) for p in premises)]
                result = entails(lang, premises, conclusion)
                self.assertEqual(result.holds, all(oracle_truth(conclusion, u) for u in good))
                self.assertEqual(result.satisfying_premise_models, len(good))
                self.assertEqual(result.admissible_models, len(universes))
                if result.countermodel is not None:
                    self.assertTrue(is_admissible(lang, result.countermodel))
                    self.assertTrue(all(evaluate(p, result.countermodel) for p in premises))
                    self.assertFalse(evaluate(conclusion, result.countermodel))

    def test_empty_terms_vacuity_and_explicit_policy(self):
        a, i = Prop("A", "S", "P"), Prop("I", "S", "P")
        result = entails(Language(("S", "P")), (a,), i)
        self.assertFalse(result.holds)
        self.assertEqual(result.countermodel.support, (0,))
        self.assertTrue(entails(Language(("S", "P"), frozenset(("S",))), (a,), i).holds)
        inconsistent = (Prop("E", "S", "S"), Prop("I", "S", "S"))
        result = entails(Language(("S", "P")), inconsistent, a)
        self.assertTrue(result.holds)
        self.assertEqual(result.satisfying_premise_models, 0)
        self.assertIsNone(result.countermodel)

    def test_empty_premises_and_duplicate_premises(self):
        lang = Language(("S", "P"))
        tautology = Prop("A", "S", "S")
        non_tautology = Prop("I", "S", "S")
        self.assertTrue(entails(lang, (), tautology).holds)
        self.assertFalse(entails(lang, (), non_tautology).holds)
        self.assertEqual(entails(lang, (non_tautology,), tautology),
                         entails(lang, (non_tautology, non_tautology), tautology))

    def test_repeated_objects_do_not_change_AEIO_truth(self):
        terms = ("S", "P")
        props = [Prop(k, s, p) for k, s, p in product("AEIO", terms, terms)]
        for universe in oracle_models(terms):
            expanded = tuple(obj for index, obj in enumerate(universe) for _ in range(index + 2))
            for prop in props:
                self.assertEqual(oracle_truth(prop, universe), oracle_truth(prop, expanded))


class CertificateTests(unittest.TestCase):
    def setUp(self):
        self.lang = Language(("S", "M", "P"))
        self.premises = (Prop("A", "S", "M"), Prop("A", "M", "P"))
        self.conclusion = Prop("A", "S", "P")
        self.assumptions = tuple(Step(p, "assume", assumption=i) for i, p in enumerate(self.premises))

    def test_chain_and_dependencies(self):
        result = check_certificate(self.lang, self.premises, self.conclusion,
                                   self.assumptions + (Step(self.conclusion, "a_trans", (0, 1)),))
        self.assertTrue(result.accepted)
        self.assertEqual(result.used_assumptions, (0, 1))
        self.assertEqual(result.unused_assumptions, ())
        self.assertFalse(result.repeats_assumption)

    def test_unused_repeated_and_duplicate_premises_are_not_hidden(self):
        premise = self.premises[0]
        result = check_certificate(self.lang, (premise, premise), premise,
                                   (Step(premise, "assume", assumption=1),))
        self.assertEqual(result.used_assumptions, (1,))
        self.assertEqual(result.unused_assumptions, (0,))
        self.assertTrue(result.repeats_assumption)

    def test_rules_all_term_substitutions_against_direct_oracle(self):
        terms = self.lang.terms
        universes = list(oracle_models(terms))
        accepted = 0
        for s, m, p in product(terms, repeat=3):
            for rule, k1, k2, out in [
                ("a_trans", "A", "A", "A"), ("e_down", "A", "E", "E"),
                ("i_up", "I", "A", "I"), ("o_from_i_e", "I", "E", "O"),
            ]:
                premises = (Prop(k1, s, m), Prop(k2, m, p))
                conclusion = Prop(out, s, p)
                steps = (Step(premises[0], "assume", assumption=0),
                         Step(premises[1], "assume", assumption=1),
                         Step(conclusion, rule, (0, 1)))
                self.assertTrue(check_certificate(self.lang, premises, conclusion, steps).accepted)
                self.assertTrue(all(not all(oracle_truth(a, u) for a in premises) or oracle_truth(conclusion, u) for u in universes))
                accepted += 1
        for s, p in product(terms, repeat=2):
            premise, conclusion = Prop("E", s, p), Prop("E", p, s)
            steps = (Step(premise, "assume", assumption=0), Step(conclusion, "e_sym", (0,)))
            self.assertTrue(check_certificate(self.lang, (premise,), conclusion, steps).accepted)
            self.assertTrue(all(not oracle_truth(premise, u) or oracle_truth(conclusion, u) for u in universes))
            accepted += 1
        self.assertEqual(accepted, 117)

    def test_imported_and_mismatched_premises_rejected(self):
        for steps in [(Step(self.premises[1], "assume", assumption=1),),
                      (Step(self.premises[1], "assume", assumption=0),)]:
            with self.assertRaises(ValidationError):
                check_certificate(self.lang, (self.premises[0],), self.premises[1], steps)

    def test_forward_self_negative_and_wrong_conclusion_references_rejected(self):
        for refs in [(0, 2), (0, 3)]:
            with self.subTest(refs=refs), self.assertRaises(ValidationError):
                check_certificate(self.lang, self.premises, self.conclusion,
                                  self.assumptions + (Step(self.conclusion, "a_trans", refs),))
        with self.assertRaises(ValidationError):
            check_certificate(self.lang, self.premises, self.conclusion, self.assumptions)
        with self.assertRaises(ValidationError):
            check_certificate(self.lang, self.premises, self.conclusion,
                              self.assumptions + (Step(Prop("A", "P", "S"), "a_trans", (0, 1)),))

    def test_invalid_converse_and_wrong_rule_kinds_rejected(self):
        bad_premises = (Prop("A", "S", "M"), Prop("A", "P", "M"))
        steps = tuple(Step(p, "assume", assumption=i) for i, p in enumerate(bad_premises))
        with self.assertRaises(ValidationError):
            check_certificate(self.lang, bad_premises, self.conclusion,
                              steps + (Step(self.conclusion, "a_trans", (0, 1)),))
        with self.assertRaises(ValidationError):
            check_certificate(self.lang, self.premises, Prop("E", "M", "S"),
                              self.assumptions + (Step(Prop("E", "M", "S"), "e_sym", (0,)),))

    def test_malformed_or_unused_bad_steps_rejected(self):
        p = self.premises[0]
        for steps in [(), [], (None,), (Step(Prop("A", "X", "M"), "assume", assumption=0),),
                      (Step(p, "assume", assumption=5), Step(p, "assume", assumption=0))]:
            with self.subTest(steps=steps), self.assertRaises(ValidationError):
                check_certificate(self.lang, self.premises, p, steps)

    def test_true_semantic_result_need_not_have_supported_certificate(self):
        # Deliberately no existential-import rule is implemented.
        lang = Language(("S", "P"), frozenset(("S",)))
        a, i = Prop("A", "S", "P"), Prop("I", "S", "P")
        self.assertTrue(entails(lang, (a,), i).holds)
        with self.assertRaises(ValidationError):
            check_certificate(lang, (a,), i, (Step(a, "assume", assumption=0),))


class ReportTests(unittest.TestCase):
    def test_actual_existential_witnesses_and_false_claims(self):
        lang = Language(("S", "M", "P"))
        props = [Prop(k, s, p) for k, s, p in product("AEIO", lang.terms, lang.terms)]
        for model in enumerate_models(lang):
            for prop in props:
                witness = existential_witness(prop, model)
                if prop.kind in ("I", "O") and evaluate(prop, model):
                    self.assertIn(witness, model.members(prop.subject))
                    if prop.kind == "I":
                        self.assertIn(witness, model.members(prop.predicate))
                    else:
                        self.assertNotIn(witness, model.members(prop.predicate))
                else:
                    self.assertIsNone(witness)
        examples = build_report()["explicit_witness_propagation"]
        self.assertEqual([e["conclusion_existential_witness"] for e in examples], [7, 3])
        for example in examples:
            self.assertEqual(example["particular_premise_truths"], [True, True])
            self.assertTrue(example["particular_conclusion_truth"])
            self.assertTrue(example["certificate"]["accepted"])

    def test_deterministic_json_and_expected_examples(self):
        report = build_report()
        self.assertEqual(json.dumps(report, sort_keys=True), json.dumps(build_report(), sort_keys=True))
        valid = report["valid_form_with_false_premises_in_one_model"]
        self.assertTrue(valid["holds"])
        self.assertEqual(valid["particular_premise_truths"], [False, False])
        self.assertFalse(valid["particular_conclusion_truth"])
        invalid = report["true_conclusion_in_one_model_but_invalid_argument"]
        self.assertFalse(invalid["holds"])
        self.assertTrue(invalid["particular_conclusion_truth"])
        self.assertEqual(invalid["countermodel_premise_truths"], [True, True])
        self.assertFalse(invalid["countermodel_conclusion_truth"])
        self.assertFalse(report["unsupported_imported_premise"]["accepted"])
        self.assertTrue(report["valid_proof_using_E_conversion"]["certificate"]["accepted"])
        hand = report["named_object_hand_examples"]
        self.assertEqual(hand["mixed_true_false_premises"]["premise_truths"], [False, True])
        self.assertFalse(hand["mixed_true_false_premises"]["conclusion_truth"])
        self.assertTrue(hand["A_is_not_symmetric"]["A_S_P_truth"])
        self.assertFalse(hand["A_is_not_symmetric"]["A_P_S_truth"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
