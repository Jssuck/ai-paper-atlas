"""Independent set-oracle, source-fixture, exhaustiveness and regression tests."""
from itertools import combinations, permutations, product
from pathlib import Path
import json
import unittest

from euler_civ import (ALL_MODELS, TERMS, MOODS, ROMANS, TERM_BITS,
                       PRINTED_CODES, PRINTED_FORMS, REPAIRED_FORMS,
                       Argument, Model, Statement, canonical, check,
                       euler_style_candidates, minimal_nonempty_assumptions,
                       models_under, normalize_required, region_mask,
                       standard_candidates)
from report import build_report, encode_report


def oracle(statement, sets):
    """Direct Python-set interpretation; no bit-mask formula logic reused."""
    x, y = sets[statement.subject], sets[statement.predicate]
    return {"A": x <= y, "E": not bool(x & y),
            "I": bool(x & y), "O": bool(x - y)}[statement.mood]


class SemanticsTests(unittest.TestCase):
    def test_exact_255_occupancies_and_minimal_order(self):
        self.assertEqual({m.occupancy for m in ALL_MODELS}, set(range(1, 256)))
        self.assertEqual(len(ALL_MODELS), 255)
        self.assertEqual([(m.size, m.occupancy) for m in ALL_MODELS],
                         sorted((m.size, m.occupancy) for m in ALL_MODELS))
        self.assertEqual(len(models_under("ABC")), 218)
        self.assertEqual(ALL_MODELS[0], Model(1))

    def test_every_statement_every_model_against_set_oracle(self):
        formulas = [Statement(q, x, y) for q in MOODS for x in TERMS for y in TERMS if x != y]
        self.assertEqual(len(formulas), 24)
        for model in ALL_MODELS:
            sets = {t: set(model.members(t)) for t in TERMS}
            for statement in formulas:
                self.assertEqual(statement.holds(model), oracle(statement, sets),
                                 (model.occupancy, statement.code))

    def test_concrete_four_object_domains_collapse_without_truth_loss(self):
        # 8^4 = 4096 concrete assignments. Repeated atom inhabitants are
        # discarded by the quotient. This test supports, not replaces, the proof.
        formulas = [Statement(q, x, y) for q in MOODS for x in TERMS for y in TERMS if x != y]
        for membership in product(range(8), repeat=4):
            sets = {t: {i for i, atom in enumerate(membership) if atom & TERM_BITS[t]} for t in TERMS}
            mask = sum(1 << atom for atom in set(membership))
            model = Model(mask)
            for formula in formulas:
                self.assertEqual(oracle(formula, sets), formula.holds(model))

    def test_universal_vacuity_and_particular_existence(self):
        outside_only = Model(1)
        for q in MOODS:
            self.assertEqual(Statement.parse(q + "AB").holds(outside_only), q in "AE")
        a_only = Model(2)
        self.assertFalse(Statement.parse("AAB").holds(a_only))
        self.assertTrue(Statement.parse("OAB").holds(a_only))
        self.assertFalse(Statement.parse("OBA").holds(a_only))
        self.assertTrue(Statement.parse("ABA").holds(a_only))

    def test_e_i_symmetric_and_a_o_not_assumed_symmetric(self):
        for model in ALL_MODELS:
            for q in "EI":
                self.assertEqual(Statement.parse(q + "AB").holds(model),
                                 Statement.parse(q + "BA").holds(model))
        self.assertNotEqual(Statement.parse("AAB").holds(Model(2)), Statement.parse("ABA").holds(Model(2)))
        self.assertNotEqual(Statement.parse("OAB").holds(Model(2)), Statement.parse("OBA").holds(Model(2)))


class HistoricalFormsTests(unittest.TestCase):
    def test_all_twenty_scan_transcriptions(self):
        # Explicit transcription fixture, including XVI's printed repetition.
        expected = [
            "AAB,ACA=>ACB", "AAB,ICA=>ICB", "AAB,ECB=>ECA", "AAB,EBC=>ECA",
            "AAB,OCB=>OCA", "AAB,ABC=>ICA", "EAB,ACA=>ECB", "EAB,ACB=>ECA",
            "EAB,ICA=>OCB", "EAB,IAC=>OCB", "EAB,ICB=>OCA", "EAB,IBC=>OCA",
            "IAB,AAC=>ICB", "IAB,ABC=>ICA", "OAB,AAC=>OCB", "OAB,ACB=>OAB",
            "AAB,IAC=>ICB", "EAB,AAC=>OCB", "EAB,ABC=>OCA", "AAB,AAC=>ICB"]
        self.assertEqual(list(PRINTED_FORMS), list(ROMANS))
        self.assertEqual([a.code for a in PRINTED_FORMS.values()], expected)
        self.assertEqual(len(PRINTED_CODES), 20)
        self.assertEqual(REPAIRED_FORMS["XVI"].code, "OAB,ACB=>OAC")
        self.assertEqual([label for label in ROMANS if PRINTED_FORMS[label] != REPAIRED_FORMS[label]], ["XVI"])

    def test_all_twenty_under_both_regimes_and_minimal_assumptions(self):
        needed = {"VI": (("A",),), "XVIII": (("A",),),
                  "XIX": (("B",),), "XX": (("A",),)}
        for collection in (PRINTED_FORMS, REPAIRED_FORMS):
            for label, argument in collection.items():
                with self.subTest(label=label, code=argument.code):
                    self.assertTrue(check(argument, "ABC").valid)
                    self.assertGreater(check(argument, "ABC").premise_models, 0)
                    self.assertEqual(check(argument).valid, label not in needed)
                    self.assertEqual(minimal_nonempty_assumptions(argument), needed.get(label, ((),)))

    def test_every_reported_counterexample_is_smallest_and_sound(self):
        for label in ("VI", "XVIII", "XIX", "XX"):
            argument = REPAIRED_FORMS[label]
            result = check(argument)
            model = result.first_counterexample
            self.assertEqual(model, Model(1))
            self.assertTrue(all(p.holds(model) for p in argument.premises))
            self.assertFalse(argument.conclusion.holds(model))
            self.assertEqual(model.size, min(m.size for m in ALL_MODELS
                if all(p.holds(m) for p in argument.premises) and not argument.conclusion.holds(m)))

    def test_printed_xvi_tautology_and_repair_nontrivial(self):
        self.assertEqual(PRINTED_FORMS["XVI"].conclusion, PRINTED_FORMS["XVI"].premises[0])
        self.assertTrue(check(PRINTED_FORMS["XVI"]).valid)
        self.assertTrue(check(REPAIRED_FORMS["XVI"]).valid)
        self.assertNotEqual(canonical(PRINTED_FORMS["XVI"]), canonical(REPAIRED_FORMS["XVI"]))
        self.assertEqual(canonical(REPAIRED_FORMS["XVI"]), canonical(REPAIRED_FORMS["V"]))
        # Without C subset B, the proposed repaired conclusion can be false.
        a_c_outside_b = Model(1 << 5)
        self.assertTrue(REPAIRED_FORMS["XVI"].premises[0].holds(a_c_outside_b))
        self.assertFalse(REPAIRED_FORMS["XVI"].conclusion.holds(a_c_outside_b))


class ExhaustivenessTests(unittest.TestCase):
    def test_standard_generator_is_exact_cartesian_product(self):
        rows = standard_candidates()
        self.assertEqual(len(rows), 256)
        self.assertEqual({(mood, figure) for mood, figure, _ in rows},
                         {("".join(m), f) for m in product(MOODS, repeat=3) for f in range(1, 5)})
        self.assertEqual(len({a.code for _, _, a in rows}), 256)
        self.assertEqual(sum(check(a).valid for _, _, a in rows), 15)
        self.assertEqual(sum(check(a, "ABC").valid for _, _, a in rows), 24)

    def test_larger_scope_and_particular_first_exact_coverage(self):
        full = euler_style_candidates()
        particular = euler_style_candidates("IO")
        self.assertEqual(len(full), 512)
        self.assertEqual(len({a.code for a in full}), 512)
        self.assertEqual(len(particular), 256)
        self.assertEqual(set(particular), {a for a in full if a.premises[0].mood in "IO"})
        for a in full:
            pairs = {frozenset((s.subject, s.predicate)) for s in (*a.premises, a.conclusion)}
            self.assertEqual(pairs, {frozenset(x) for x in ("AB", "AC", "BC")})
        self.assertNotIn(PRINTED_FORMS["XVI"], full)
        self.assertTrue(set(REPAIRED_FORMS.values()) <= set(full))
        self.assertEqual(sum(check(a).valid for a in full), 30)
        self.assertEqual(sum(check(a, "ABC").valid for a in full), 48)
        self.assertEqual(sum(check(a).valid for a in particular), 10)
        self.assertEqual(sum(check(a, "ABC").valid for a in particular), 10)

    def test_all_candidates_validity_against_separate_set_oracle(self):
        # Re-evaluate the 512 arguments by ordinary set operations rather than
        # the formula bit-mask evaluator. Covers both regimes in one pass.
        models = [(m, {t: set(m.members(t)) for t in TERMS}) for m in ALL_MODELS]
        for a in euler_style_candidates():
            fail_any = fail_nonempty = False
            for _, sets in models:
                if all(oracle(p, sets) for p in a.premises) and not oracle(a.conclusion, sets):
                    fail_any = True
                    if all(sets[t] for t in TERMS):
                        fail_nonempty = True
            self.assertEqual(check(a).valid, not fail_any, a.code)
            self.assertEqual(check(a, "ABC").valid, not fail_nonempty, a.code)

    def test_particular_premise_no_existential_only_additions_in_fixed_scope(self):
        for a in euler_style_candidates("IO"):
            self.assertEqual(check(a).valid, check(a, "ABC").valid)
        bad = Argument.parse("IAB", "IAC", "IBC")
        self.assertFalse(check(bad, "ABC").valid)
        model = check(bad, "ABC").first_counterexample
        self.assertEqual(model.size, 2)
        self.assertTrue(all(p.holds(model) for p in bad.premises))
        self.assertFalse(bad.conclusion.holds(model))


class EquivalenceTests(unittest.TestCase):
    def test_equivalence_is_invariant_under_all_allowed_operations(self):
        for arg in REPAIRED_FORMS.values():
            key = canonical(arg)
            for names in permutations(TERMS):
                renamed = arg.renamed(dict(zip(TERMS, names)))
                self.assertEqual(canonical(renamed), key)
                self.assertEqual(canonical(Argument(renamed.premises[::-1], renamed.conclusion)), key)
                for idx, s in enumerate((*renamed.premises, renamed.conclusion)):
                    if s.mood in "EI":
                        parts = list((*renamed.premises, renamed.conclusion))
                        parts[idx] = Statement(s.mood, s.predicate, s.subject)
                        self.assertEqual(canonical(Argument(tuple(parts[:2]), parts[2])), key)
                for required in ((), tuple(TERMS)):
                    self.assertEqual(check(arg, required).valid, check(renamed, required).valid)

    def test_class_counts_and_specific_memberships(self):
        self.assertEqual(len({canonical(a) for a in PRINTED_FORMS.values()}), 10)
        self.assertEqual(len({canonical(a) for a in REPAIRED_FORMS.values()}), 9)
        for group in (("II", "XIII", "XIV", "XVII"), ("III", "IV", "VII", "VIII"),
                      ("IX", "X", "XI", "XII"), ("XVIII", "XIX"), ("V", "XVI")):
            self.assertEqual(len({canonical(REPAIRED_FORMS[label]) for label in group}), 1)
        self.assertNotEqual(canonical(REPAIRED_FORMS["I"]), canonical(REPAIRED_FORMS["VI"]))
        self.assertNotEqual(canonical(REPAIRED_FORMS["XV"]), canonical(REPAIRED_FORMS["XVI"]))

    def test_no_ei_conversion_gives_nineteen_and_five_uncovered_moods(self):
        self.assertEqual(len({canonical(a, False) for a in PRINTED_FORMS.values()}), 20)
        recap = {canonical(a, False) for a in REPAIRED_FORMS.values()}
        self.assertEqual(len(recap), 19)
        self.assertEqual(canonical(REPAIRED_FORMS["V"], False), canonical(REPAIRED_FORMS["XVI"], False))
        self.assertNotEqual(canonical(REPAIRED_FORMS["II"], False), canonical(REPAIRED_FORMS["XVII"], False))
        missing = {f"{m}-{f}" for m, f, a in standard_candidates()
                   if check(a, "ABC").valid and canonical(a, False) not in recap}
        self.assertEqual(missing, {"AAI-1", "EAO-1", "AEO-2", "EAO-2", "AEO-4"})
        for arg in REPAIRED_FORMS.values():
            for names in permutations(TERMS):
                renamed = arg.renamed(dict(zip(TERMS, names)))
                self.assertEqual(canonical(arg, False), canonical(Argument(renamed.premises[::-1], renamed.conclusion), False))
        with self.assertRaises(ValueError):
            canonical(REPAIRED_FORMS["I"], "false")

    def test_two_nonempty_classes_missing_from_repaired_recap(self):
        recap = {canonical(a) for a in REPAIRED_FORMS.values()}
        valid = {canonical(a) for _, _, a in standard_candidates() if check(a, "ABC").valid}
        self.assertEqual(len(valid), 11)
        self.assertEqual(valid - recap, {"AAB,EBC=>OAC", "AAB,EBC=>OCA"})
        for code, required in (("OAC", (("A",),)), ("OCA", (("C",),))):
            argument = Argument.parse("AAB", "EBC", code)
            self.assertEqual(minimal_nonempty_assumptions(argument), required)
        self.assertEqual(len({canonical(a) for _, _, a in standard_candidates() if check(a).valid}), 6)


class ValidationTests(unittest.TestCase):
    def test_reject_invalid_model_masks(self):
        for bad in (0, -1, 256, 1.0, "1", None, True, False, [], {}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                Model(bad)

    def test_reject_invalid_formulas(self):
        for bad in ("", "A", "AABX", " AAB", "aab", "XAB", "AAD", "AAA", None, 42, []):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                Statement.parse(bad)
        for values in (("", "A", "B"), ("AE", "A", "B"), ("A", "", "B"), ("A", "AB", "C")):
            with self.subTest(values=values), self.assertRaises(ValueError):
                Statement(*values)
        with self.assertRaises(ValueError):
            Statement.parse("AAB").holds(1)

    def test_reject_invalid_assumptions_arguments_and_generators(self):
        for bad in (None, 4, "AA", "D", "a", ["AB"], [None], [["A"]]):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                normalize_required(bad)
        self.assertEqual(normalize_required("CA"), ("A", "C"))
        for bad in ("", "II", "AX", None, ["I"]):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                euler_style_candidates(bad)
        for premises in ((), (Statement.parse("AAB"),), [Statement.parse("AAB"), Statement.parse("ACA")], ("AAB", "ACA")):
            with self.assertRaises(ValueError):
                Argument(premises, Statement.parse("ACB"))
        with self.assertRaises(ValueError):
            Argument((Statement.parse("AAB"), Statement.parse("ACA")), "ACB")
        with self.assertRaises(ValueError):
            check("AAB,ACA=>ACB")
        with self.assertRaises(ValueError):
            canonical(None)
        with self.assertRaises(ValueError):
            Statement.parse("AAB").renamed({"A": "B", "B": "B", "C": "C"})
        for mapping in (None, [], {"A": [], "B": "B", "C": "C"}):
            with self.subTest(mapping=mapping), self.assertRaises(ValueError):
                Statement.parse("AAB").renamed(mapping)
        with self.assertRaises(ValueError):
            region_mask("A", "B", "union")

    def test_unrepairable_inference_has_no_sufficient_term_existence_set(self):
        invalid = Argument.parse("IAB", "IAC", "IBC")
        self.assertEqual(minimal_nonempty_assumptions(invalid), ())


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = build_report()

    def test_json_is_deterministic_and_matches_checked_in_report(self):
        encoded = encode_report(self.report)
        self.assertEqual(encoded, encode_report(build_report()))
        stored = Path(__file__).resolve().parents[1] / "outputs" / "report.json"
        self.assertEqual(stored.read_text(encoding="utf-8"), encoded)
        self.assertEqual(json.loads(encoded), self.report)

    def test_report_has_full_census_and_explicit_xvi_caveat(self):
        for form in self.report["repaired_forms"]:
            self.assertEqual(len(form["all_nonempty_assumption_checks"]), 8)
        self.assertEqual(len(self.report["standard_256"]["cases"]), 256)
        self.assertEqual(len(self.report["euler_style_512"]["cases"]), 512)
        self.assertEqual(len(self.report["particular_first_256"]["cases"]), 256)
        self.assertIn("not a verified formal erratum", self.report["historical_scope"]["repair_status"])
        self.assertFalse(self.report["euler_style_512"]["printed_xvi_in_scope"])
        self.assertTrue(self.report["euler_style_512"]["all_repaired_entries_in_scope"])
        for scope in ("standard_256", "euler_style_512", "particular_first_256"):
            self.assertTrue(self.report[scope]["candidate_identifiers_unique"])
            self.assertTrue(self.report[scope]["candidate_codes_unique"])


if __name__ == "__main__":
    unittest.main()
