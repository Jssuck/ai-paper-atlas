"""Exhaustive and independent-oracle checks; run with unittest discovery."""

import itertools
import json
from pathlib import Path
import tempfile
import unittest

from gergonne import (
    ELEVEN, FIGURES, FOURTEEN, LETTERS, MODERN_FIGURE, RELATIONS,
    REVERSE_RELATION, SIX, Literal, Model, Mood, base_inference,
    candidates, conversion_targets, countermodel, equivalence_classes,
    models, proposition, reduction_closure, reductio_certificates,
    relation, relation_triple, reverse_conclusion, reverse_premise,
    rule59_violations, valid_moods, weakened_neighbors,
)
from reproduce import (create_results, example_record, opposition_record,
                       reductions_record, source_table_crosscheck)


def independent_truth(kind, left, right):
    """Different implementation: explicit quantifiers over concrete objects."""
    if kind == "A":
        return all(x in right for x in left)
    if kind == "N":
        return all(x not in right for x in left)
    if kind == "a":
        return any(x in right for x in left)
    if kind == "n":
        return any(x not in right for x in left)
    raise ValueError(kind)


def independent_valid_moods(nonempty):
    """All 343 / 512 triples of subsets of a concrete THREE-object universe.

    This finite oracle is a separate crosscheck, not the completeness proof.
    Its figure directions are intentionally written independently of FIGURES.
    """
    subsets = [frozenset(x for x in range(3) if bits & (1 << x))
               for bits in range(1 if nonempty else 0, 8)]
    answer = set()
    for figure in (1, 2, 3, 4):
        for a, b, c in itertools.product("ANan", repeat=3):
            valid = True
            for P, M, G in itertools.product(subsets, repeat=3):
                if figure == 1:
                    first, second = (M, G), (P, M)
                elif figure == 2:
                    first, second = (G, M), (M, P)
                elif figure == 3:
                    first, second = (G, M), (P, M)
                else:
                    first, second = (M, G), (M, P)
                if (independent_truth(a, *first) and independent_truth(b, *second)
                        and not independent_truth(c, P, G)):
                    valid = False
                    break
            if valid:
                answer.add(f"{figure}:{a}{b}{c}")
    return answer


class CanonicalModelTests(unittest.TestCase):
    def test_pattern_count_by_inclusion_exclusion(self):
        self.assertEqual(len(models()), 2**7 - 3 * 2**3 + 3 * 2**1 - 1)
        self.assertEqual(len(models(False)), 128)
        self.assertTrue(all(m.all_terms_nonempty for m in models()))

    def test_masks_atoms_and_terms(self):
        for model in models(False):
            self.assertEqual(sum(1 << (a - 1) for a in model.atoms), model.mask)
            for t, bit in zip(("P", "M", "G"), (1, 2, 4)):
                self.assertEqual(model.term(t), frozenset(a for a in model.atoms if a & bit))

    def test_five_relations_exclusive_and_exhaustive(self):
        seen = set()
        for model in models():
            for a, b in itertools.permutations(("P", "M", "G"), 2):
                left, right = model.term(a), model.term(b)
                conditions = {"H": not left & right, "I": left == right,
                              "C": left < right, "D": right < left,
                              "X": bool(left & right and left - right and right - left)}
                self.assertEqual(sum(conditions.values()), 1)
                actual = relation(left, right)
                self.assertTrue(conditions[actual])
                self.assertEqual(relation(right, left), REVERSE_RELATION[actual])
                seen.add(actual)
        self.assertEqual(seen, set(RELATIONS))

    def test_relations_reject_empty_terms(self):
        for a, b in ((frozenset(), frozenset()), (frozenset(), frozenset({1})),
                     (frozenset({1}), frozenset())):
            with self.assertRaises(ValueError):
                relation(a, b)

    def test_relation_count_and_every_pair_present(self):
        triples = {relation_triple(m) for m in models()}
        self.assertEqual(len(triples), 54)
        self.assertEqual({t[:2] for t in triples}, set(itertools.product(RELATIONS, repeat=2)))

    def test_predicates_against_quantifier_oracle(self):
        for model in models(False):
            for a, b in itertools.product(("P", "M", "G"), repeat=2):
                for k in LETTERS:
                    self.assertEqual(proposition(k, model.term(a), model.term(b)),
                                     independent_truth(k, model.term(a), model.term(b)))

    def test_multiplicity_and_outside_objects_do_not_matter(self):
        for model in models(False):
            expanded = {t: frozenset((a, j) for a in model.term(t) for j in range(a + 1))
                        for t in ("P", "M", "G")}
            # An extra object (0,0) outside all terms is deliberately irrelevant.
            for a, b in itertools.product(("P", "M", "G"), repeat=2):
                for k in LETTERS:
                    self.assertEqual(proposition(k, expanded[a], expanded[b]),
                                     proposition(k, model.term(a), model.term(b)))

    def test_input_validation(self):
        for value in (-1, 128, True, 0.5):
            with self.assertRaises(ValueError):
                Model(value)
        with self.assertRaises(ValueError):
            Model(0).term("Q")
        with self.assertRaises(ValueError):
            proposition("E", frozenset(), frozenset())
        with self.assertRaises(ValueError):
            Mood(5, "A", "A", "A")
        with self.assertRaises(ValueError):
            Mood(1, "E", "A", "A")


class PropositionTests(unittest.TestCase):
    def test_original_conversion_table(self):
        self.assertEqual({k: conversion_targets(k) for k in LETTERS},
                         {"A": ("a",), "N": ("N", "n"), "a": ("a",), "n": ()})

    def test_original_opposition(self):
        report = opposition_record()
        self.assertEqual(len(report["truth_patterns"]), 3)
        self.assertTrue(all(v for k, v in report.items()
                            if k not in ("column_order", "truth_patterns")))

    def test_empty_boundary_conversion_and_opposition(self):
        self.assertEqual({k: conversion_targets(k, False) for k in LETTERS},
                         {"A": (), "N": ("N",), "a": ("a",), "n": ()})
        report = opposition_record(False)
        self.assertTrue(report["contradictories_A_n"])
        self.assertTrue(report["contradictories_N_a"])
        for key in ("contraries_A_N_never_both_true", "subcontraries_a_n_never_both_false",
                    "subalternation_A_a", "subalternation_N_n"):
            self.assertFalse(report[key])


class SyllogismTests(unittest.TestCase):
    def test_enumeration_counts_and_no_vacuous_premise_pairs(self):
        self.assertEqual(len(candidates()), 256)
        self.assertEqual(len(valid_moods()), 24)
        for f in FIGURES:
            self.assertEqual(sum(m.figure == f for m in valid_moods()), 6)
        self.assertEqual([sum(m.conclusion == k for m in valid_moods()) for k in LETTERS],
                         [1, 4, 7, 12])
        for mood in candidates():
            self.assertTrue(any(mood.premises_hold(m) for m in models()))

    def test_independent_concrete_set_oracle(self):
        self.assertEqual({m.id for m in valid_moods()}, independent_valid_moods(True))
        self.assertEqual({m.id for m in valid_moods(False)}, independent_valid_moods(False))

    def test_all_232_countermodels_and_minimality(self):
        count = 0
        for mood in candidates():
            witness = countermodel(mood)
            if witness is None:
                continue
            count += 1
            self.assertTrue(witness.all_terms_nonempty)
            literals = mood.literals()
            self.assertTrue(independent_truth(literals[0].kind,
                                             witness.term(literals[0].subject),
                                             witness.term(literals[0].predicate)))
            self.assertTrue(independent_truth(literals[1].kind,
                                             witness.term(literals[1].subject),
                                             witness.term(literals[1].predicate)))
            self.assertFalse(independent_truth(literals[2].kind,
                                              witness.term("P"), witness.term("G")))
            self.assertTrue(all(not mood.is_countermodel(m) for m in models()
                                if len(m.atoms) < len(witness.atoms)))
        self.assertEqual(count, 232)

    def test_rule59_matches_all_256_candidates(self):
        for mood in candidates():
            self.assertEqual(not rule59_violations(mood), countermodel(mood) is None, mood.id)

    def test_source_figure_order(self):
        self.assertEqual(MODERN_FIGURE, {1: 1, 2: 4, 3: 2, 4: 3})
        self.assertEqual(Mood(2, *"ANn").original_ascii, "rA rN n")
        self.assertEqual(Mood(3, *"ANn").original_ascii, "rA N n")
        self.assertEqual(Mood(4, *"Aaa").original_ascii, "A ra a")

    def test_exact_section51_example(self):
        record = example_record(2, "A", "N")
        self.assertEqual(record["premises"], ["A(G,M)", "N(M,P)"])
        self.assertEqual(record["original_premises_ascii"], "rA rN")
        self.assertEqual(record["relation_pairs"], ["DH", "IH"])
        self.assertEqual(record["possible_conclusion_relations"], ["H"])
        self.assertEqual(record["entailed_conclusion_kinds"], ["N", "n"])

    def test_exact_section52_example(self):
        record = example_record(4, "A", "N")
        self.assertEqual(record["premises"], ["A(M,G)", "N(M,P)"])
        self.assertEqual(record["original_premises_ascii"], "A rN")
        self.assertEqual(record["relation_pairs"], ["CH", "IH"])
        self.assertEqual(record["possible_conclusion_relations"], ["C", "H", "X"])
        self.assertEqual(record["entailed_conclusion_kinds"], [])

    def test_empty_term_boundary_loses_exactly_nine(self):
        self.assertEqual(len(valid_moods(False)), 15)
        lost = set(valid_moods()) - set(valid_moods(False))
        self.assertEqual(len(lost), 9)
        for mood in lost:
            witness = countermodel(mood, False)
            self.assertFalse(witness.all_terms_nonempty)
            self.assertTrue(mood.is_countermodel(witness))


class ReductionTests(unittest.TestCase):
    def test_premise_conversion_preserves_premise_truth(self):
        for mood in valid_moods():
            for i in (0, 1):
                if mood.kinds[i] not in "Na":
                    continue
                converse = reverse_premise(mood, i)
                self.assertEqual(reverse_premise(converse, i), mood)
                for model in models():
                    self.assertEqual(mood.premises_hold(model), converse.premises_hold(model))

    def test_conclusion_conversion_renaming(self):
        for mood in valid_moods():
            if mood.conclusion not in "Na":
                continue
            converse = reverse_conclusion(mood)
            self.assertEqual(reverse_conclusion(converse), mood)
            for model in models():
                swapped_atoms = [((a & 1) << 2) | (a & 2) | ((a & 4) >> 2) for a in model.atoms]
                swapped = Model(sum(1 << (a - 1) for a in swapped_atoms))
                self.assertEqual(mood.premises_hold(model), converse.premises_hold(swapped))
                self.assertEqual(mood.literals()[2].holds(model), converse.literals()[2].holds(swapped))

    def test_24_to_14_to_11_computed_classes(self):
        for allow_conclusion, representatives, count in ((False, FOURTEEN, 14), (True, ELEVEN, 11)):
            groups = equivalence_classes(allow_conclusion)
            self.assertEqual(len(groups), count)
            self.assertEqual(set(itertools.chain.from_iterable(groups)), set(valid_moods()))
            self.assertEqual(len(representatives), count)
            for group in groups:
                self.assertEqual(sum(r in group for r in representatives), 1)

    def test_11_to_6_entailment_sources_and_closure(self):
        record = reductions_record()
        groups = equivalence_classes(True)
        sources = [groups[i] for i in record["source_class_indices"]]
        self.assertEqual(len(sources), 6)
        for source in sources:
            self.assertEqual(sum(r in source for r in SIX), 1)
        self.assertEqual(reduction_closure(SIX), frozenset(valid_moods()))
        for mood in valid_moods():
            self.assertTrue(set(weakened_neighbors(mood)) <= set(valid_moods()))

    def test_6_to_2_explicit_reductio_certificates(self):
        certs = reductio_certificates()
        self.assertEqual([c["target"] for c in certs], [m.id for m in SIX[2:]])
        self.assertEqual([c["base"] for c in certs], ["NAN", "NAN", "AAA", "AAA"])
        # Check soundness of every base instance under every canonical model.
        for middle, small, large in itertools.permutations(("P", "M", "G")):
            for kind in "AN":
                major = Literal(kind, middle, large)
                minor = Literal("A", small, middle)
                conclusion = base_inference(major, minor)
                self.assertEqual(conclusion, Literal(kind, small, large))
                for model in models(False):
                    self.assertTrue(not (major.holds(model) and minor.holds(model))
                                    or conclusion.holds(model))

    def test_invalid_conversion_and_base_are_rejected(self):
        with self.assertRaises(ValueError):
            reverse_premise(Mood(1, *"AAA"), 0)
        with self.assertRaises(ValueError):
            reverse_conclusion(Mood(1, *"NAn"))
        with self.assertRaises(ValueError):
            base_inference(Literal("a", "M", "G"), Literal("A", "P", "M"))


class ArtifactTests(unittest.TestCase):
    def test_section55_printed_discrepancy_and_emended_match(self):
        result = source_table_crosscheck()
        self.assertFalse(result["section55_printed_exact_match"])
        self.assertTrue(result["section55_proposed_emended_exact_match"])
        self.assertEqual(result["section55_printed_discrepancies"],
                         {"N": {"printed_but_not_valid": ["CH"], "valid_but_not_printed": ["DH"]}})
        self.assertEqual(result["section55_pair_counts"], {"A": 4, "N": 4, "a": 12, "n": 13})
        self.assertTrue(result["section58_exact_match"])

    def test_printed_section55_CH_N_error_has_nonempty_counterexample(self):
        witness = Model(48)
        self.assertTrue(witness.all_terms_nonempty)
        self.assertEqual(relation_triple(witness), ("C", "H", "C"))
        self.assertEqual(witness.term("P"), frozenset({5}))
        self.assertEqual(witness.term("M"), frozenset({6}))
        self.assertEqual(witness.term("G"), frozenset({5, 6}))
        self.assertFalse(Literal("N", "P", "G").holds(witness))
        self.assertTrue(all(Literal("N", "P", "G").holds(m) for m in models()
                            if relation_triple(m)[:2] == ("D", "H")))

    def test_reduction_representatives_match_source_selection(self):
        self.assertTrue(source_table_crosscheck()["sections63_64_representatives_exact_match"])

    def test_historical_table_exact_image_transcription_match(self):
        result = source_table_crosscheck()
        self.assertTrue(result["exact_set_match"])
        self.assertEqual(result["expected_count"], 54)
        self.assertEqual(result["missing"], [])
        self.assertEqual(result["extra"], [])
        self.assertEqual(result["computed_rows_H_X_I_C_D"],
                         {"H": 13, "X": 14, "I": 5, "C": 11, "D": 11})

    def test_generation_is_deterministic_and_auditable(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            summary = create_results(out)
            first = {p.name: p.read_bytes() for p in out.iterdir()}
            create_results(out)
            self.assertEqual(first, {p.name: p.read_bytes() for p in out.iterdir()})
            self.assertEqual(summary["reductions"], [24, 14, 11, 6, 2])
            cases = json.loads((out / "invalid_countermodels_232.json").read_text())
            self.assertEqual(len(cases), 232)
            for record in cases:
                f, word = record["id"].split(":")
                self.assertTrue(Mood(int(f), *word).is_countermodel(Model(record["countermodel"]["mask"])))


if __name__ == "__main__":
    unittest.main()
