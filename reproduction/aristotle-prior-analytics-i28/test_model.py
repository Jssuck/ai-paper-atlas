import unittest
from dataclasses import replace
from model import (Certificate, normalize, requirements, conclusion, search,
                   verify, true_fact, facts_from_model)


class MatchingTests(unittest.TestCase):
    def certificate(self, rule):
        fs = requirements(rule, "A", "E", "M")
        c = next(c for c in search(fs) if c.rule == rule)
        self.assertTrue(verify(c, fs))
        return c, fs

    def test_cf(self): self.certificate("CF")
    def test_cg(self): self.certificate("CG")
    def test_df(self): self.certificate("DF")
    def test_bh(self): self.certificate("BH")
    def test_dg(self): self.certificate("DG")
    def test_bg(self): self.certificate("BG")

    def test_no_existential_import_without_witness(self):
        for rule in ("CG", "DG", "BG"):
            fs = [f for f in requirements(rule, "A", "E", "M")
                  if f[0] != "nonempty"]
            self.assertFalse(any(c.rule == rule for c in search(fs)))

    def test_empty_universals_are_valid(self):
        for rule in ("CF", "DF", "BH"):
            c, fs = self.certificate(rule)
            model = {x: set() for x in ("A", "E", "M")}
            self.assertTrue(all(true_fact(f, model) for f in fs))
            self.assertTrue(true_fact(c.conclusion, model))

    def test_missing_premise_rejected(self):
        c, fs = self.certificate("CF")
        self.assertFalse(verify(c, fs[:-1]))

    def test_forged_conclusion_rejected(self):
        c, fs = self.certificate("BG")
        self.assertFalse(verify(replace(c, conclusion=("A", "E", "A")), fs))

    def test_forged_middle_rejected(self):
        c, fs = self.certificate("CF")
        self.assertFalse(verify(replace(c, middle="X"), fs))

    def test_forged_premise_list_rejected(self):
        c, fs = self.certificate("CF")
        self.assertFalse(verify(replace(c, premises=fs[:-1]), fs))

    def test_unknown_rule_rejected(self):
        c, fs = self.certificate("CF")
        self.assertFalse(verify(replace(c, rule="BF"), fs))

    def test_disjoint_is_symmetric(self):
        fs = [("none", "A", "M"), ("all", "E", "M")]
        self.assertTrue(any(c.rule == "DF" for c in search(fs)))

    def test_unknown_is_not_negative(self):
        self.assertEqual(search([("all", "E", "M")]), [])

    def test_shared_supertype_does_not_suffice(self):
        self.assertEqual(search([("all", "A", "M"), ("all", "E", "M")]), [])

    def test_two_negatives_do_not_suffice(self):
        self.assertEqual(search([("none", "A", "M"), ("none", "E", "M")]), [])

    def test_ch_does_not_suffice(self):
        self.assertEqual(search([("all", "M", "A"), ("none", "E", "M")]), [])

    def test_overlap_is_not_identity(self):
        model = {"A": {0}, "E": {1}, "M1": {0}, "M2": {0, 1}}
        fs = [("all", "M1", "A"), ("all", "E", "M2")]
        self.assertTrue(model["M1"] & model["M2"])
        self.assertEqual(search(fs), [])
        self.assertFalse(true_fact(("A", "E", "A"), model))

    def test_genus_failure_not_species_failure(self):
        model = {"A": {0}, "E": {0}, "F": {0}, "K": {0, 1}}
        self.assertFalse(true_fact(("all", "K", "A"), model))
        self.assertTrue(true_fact(("all", "F", "A"), model))
        fs = [("all", "E", "F"), ("all", "F", "A")]
        self.assertTrue(any(c.rule == "CF" for c in search(fs)))

    def test_bg_incompatibility_does_not_imply_bh(self):
        model = {"A": {1}, "B": {1}, "G": {0}, "E": {0, 1}}
        for f in [("all", "A", "B"), ("all", "G", "E"),
                  ("none", "B", "G"), ("nonempty", "G")]:
            self.assertTrue(true_fact(f, model))
        self.assertFalse(true_fact(("none", "B", "E"), model))
        self.assertTrue(true_fact(("O", "E", "A"), model))
        # Valid teaching reduction: G is disjoint from A, hence D/G.
        self.assertTrue(true_fact(("none", "G", "A"), model))

    def test_inverse_bg_is_not_target_universal(self):
        model = {"A": {0}, "M": {0, 1}, "E": {0, 1, 2}}
        c, fs = self.certificate("BG")
        self.assertTrue(all(true_fact(f, model) for f in fs))
        self.assertTrue(true_fact(("A", "A", "E"), model))
        self.assertFalse(true_fact(("A", "E", "A"), model))
        self.assertTrue(true_fact(c.conclusion, model))

    def test_empty_match_does_not_mean_false_goal(self):
        self.assertEqual(search([]), [])
        self.assertTrue(true_fact(("A", "E", "A"), {"A": {0}, "E": {0}}))

    def test_premise_truth_not_certificate_truth(self):
        c, fs = self.certificate("CF")
        self.assertTrue(verify(c, fs))
        model = {"A": set(), "E": {0}, "M": {0}}
        self.assertFalse(all(true_fact(f, model) for f in fs))

    def test_same_endpoint_rejected(self):
        with self.assertRaises(ValueError):
            search([("all", "M", "A"), ("all", "A", "M")], a="A", e="A")

    def test_invalid_fact_term_names(self):
        for bad in (None, 7, "", "  ", [], {}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                normalize(("none", "A", bad))
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                normalize(("nonempty", bad))

    def test_invalid_endpoint_names(self):
        for bad in (None, 7, "", "  ", [], {}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                search([], a=bad)
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                search([], e=bad)

    def test_invalid_certificate_term_names(self):
        c, fs = self.certificate("CF")
        for bad in (None, 7, "", "  ", [], {}):
            for field in ("predicate", "subject", "middle"):
                self.assertFalse(verify(replace(c, **{field: bad}), fs))

    def test_bad_fact_rejected(self):
        with self.assertRaises(ValueError): normalize(("maybe", "A", "E"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
