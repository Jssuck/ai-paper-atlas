"""Unit and bounded exhaustive checks, effective under normal Python, -O and -OO."""

import unittest
from itertools import product

from finite_checks import multiset_checks, policy_checks, relation_checks, unary_checks
from model import (DeterministicPolicy, Multiset, descend_relation, descend_unary,
                   enumerate_policies, version_space)


class RelationTests(unittest.TestCase):
    def setUp(self):
        self.domain = ("x", "y", "z")
        self.rep = {"x": "red", "y": "red", "z": "blue"}
        self.relation = {pair: False for pair in product(self.domain, repeat=2)}

    def test_empty_image_has_unique_empty_quotient(self):
        result = descend_relation((), {}, {})
        self.assertTrue(result.descends)
        self.assertEqual(result.quotient, {})
        self.assertEqual(result.conflicts, ())

    def test_singleton_relation(self):
        result = descend_relation(("x",), {"x": "red"}, {("x", "x"): True})
        self.assertEqual(result.quotient, {("red", "red"): True})

    def test_all_false_is_not_failure(self):
        result = descend_relation(self.domain, self.rep, self.relation)
        self.assertTrue(result.descends)
        self.assertEqual(set(result.quotient.values()), {False})

    def test_ordered_pairs_are_not_symmetrized(self):
        relation = {(x, y): self.rep[x] == "red" and self.rep[y] == "blue"
                    for x, y in product(self.domain, repeat=2)}
        result = descend_relation(self.domain, self.rep, relation)
        self.assertTrue(result.quotient["red", "blue"])
        self.assertFalse(result.quotient["blue", "red"])

    def test_conflict_in_one_rectangle_returns_explicit_witnesses(self):
        self.relation["x", "y"] = True
        result = descend_relation(self.domain, self.rep, self.relation)
        self.assertIsNone(result.quotient)
        self.assertFalse(result.descends)
        self.assertEqual(len(result.conflicts), 1)
        conflict = result.conflicts[0]
        self.assertEqual(conflict.representation_pair, ("red", "red"))
        self.assertEqual(conflict.true_pair, ("x", "y"))
        self.assertEqual(conflict.false_pair, ("x", "x"))

    def test_one_witness_for_every_bad_rectangle(self):
        self.relation["x", "y"] = True
        self.relation["x", "z"] = True
        result = descend_relation(self.domain, self.rep, self.relation)
        self.assertEqual(tuple(c.representation_pair for c in result.conflicts),
                         (("red", "red"), ("red", "blue")))

    def test_injective_representation_preserves_any_relation(self):
        self.relation["x", "y"] = True
        result = descend_relation(self.domain, dict(zip(self.domain, self.domain)), self.relation)
        self.assertEqual(result.quotient, self.relation)

    def test_missing_or_extra_relation_pair_rejected(self):
        missing = dict(self.relation)
        del missing["x", "x"]
        extra = dict(self.relation, **{})
        extra["outside", "x"] = False
        for bad in (missing, extra):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                descend_relation(self.domain, self.rep, bad)

    def test_integer_boolean_surrogates_rejected(self):
        for bad in (0, 1, None, "False"):
            relation = dict(self.relation)
            relation["x", "y"] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                descend_relation(self.domain, self.rep, relation)

    def test_invalid_domain_rejected(self):
        for bad in (("x", "x"), ("",), (1,), "xyz"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                descend_relation(bad, {}, {})

    def test_representation_requires_exact_keys_and_valid_labels(self):
        for bad in ({"x": "red"}, {**self.rep, "extra": "red"}, {**self.rep, "x": ""},
                    {**self.rep, "x": 1}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                descend_relation(self.domain, bad, self.relation)

    def test_unary_color_survives_while_rank_order_does_not(self):
        predicate = {x: self.rep[x] == "red" for x in self.domain}
        self.assertEqual(descend_unary(self.domain, self.rep, predicate).quotient,
                         {"red": True, "blue": False})
        rank = {"x": 1, "y": 2, "z": 1}
        relation = {(x, y): rank[x] < rank[y] for x, y in product(self.domain, repeat=2)}
        self.assertFalse(descend_relation(self.domain, self.rep, relation).descends)

    def test_unary_conflict_and_empty_domain(self):
        result = descend_unary(self.domain, self.rep, {"x": True, "y": False, "z": False})
        self.assertIsNone(result.quotient)
        self.assertEqual(result.conflicts, (("red", "x", "y"),))
        self.assertEqual(descend_unary((), {}, {}).quotient, {})

    def test_invalid_unary_table_rejected(self):
        for bad in ({"x": True}, {"x": True, "y": 1, "z": False}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                descend_unary(self.domain, self.rep, bad)

    def test_bounded_relation_oracle(self):
        result = relation_checks()
        self.assertEqual(result["relation_cases"], 4165)
        self.assertEqual(result["successful_descents"], 141)

    def test_bounded_unary_oracle(self):
        result = unary_checks()
        self.assertEqual(result["predicate_cases"], 85)
        self.assertEqual(result["successful_descents"], 45)


class MultisetTests(unittest.TestCase):
    def test_empty_alphabet_and_empty_support(self):
        empty = Multiset.from_pairs(())
        self.assertEqual(empty.counts, ())
        self.assertEqual(empty.support, ())
        self.assertEqual(empty.total, 0)
        self.assertEqual(empty.add(empty), empty)
        self.assertEqual(empty.rename((), {}), empty)
        self.assertEqual(empty.rename(("a",), {}), Multiset.from_pairs(("a",)))

    def test_repeated_atoms_add_and_zero_is_canonical(self):
        value = Multiset.from_pairs(("unit", "unused"), (("unit", 5), ("unit", 7), ("unused", 0)))
        self.assertEqual(value.as_dict(), {"unit": 12})
        self.assertEqual(value.support, ("unit",))
        self.assertEqual(value.total, 12)

    def test_dozen_is_not_singleton(self):
        unit = Multiset.from_pairs(("unit",), (("unit", 1),))
        self.assertNotEqual(unit.scale(12), unit)
        self.assertEqual(unit.scale(12).total, 12)
        self.assertEqual(len(set(["unit"] * 12)), 1)

    def test_alphabet_input_order_is_normalized(self):
        self.assertEqual(Multiset.from_pairs(("b", "a"), (("a", 1),)),
                         Multiset.from_pairs(("a", "b"), (("a", 1),)))

    def test_duplicate_alphabet_rejected(self):
        with self.assertRaises(ValueError):
            Multiset.from_pairs(("a", "a"))

    def test_bad_counts_and_factors_rejected_including_boolean(self):
        unit = Multiset.from_pairs(("unit",), (("unit", 1),))
        for bad in (-1, True, False, 1.0, "1", None):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    Multiset.from_pairs(("unit",), (("unit", bad),))
                with self.assertRaises(ValueError):
                    unit.scale(bad)

    def test_negative_entry_cannot_cancel_positive(self):
        with self.assertRaises(ValueError):
            Multiset.from_pairs(("unit",), (("unit", 2), ("unit", -1)))

    def test_unknown_atom_even_at_zero_rejected(self):
        with self.assertRaises(ValueError):
            Multiset.from_pairs(("a",), (("outside", 0),))

    def test_direct_constructor_validates_canonical_storage(self):
        bad_values = [(("b", "a"), (0, 0)), (("a",), ()), (("a",), (-1,)),
                      (("a",), (True,)), (["a"], (1,)), (("a",), [1])]
        for alphabet, counts in bad_values:
            with self.subTest(alphabet=alphabet, counts=counts), self.assertRaises(ValueError):
                Multiset(alphabet, counts)

    def test_addition_rejects_different_alphabets(self):
        with self.assertRaises(ValueError):
            Multiset.from_pairs(("a",)).add(Multiset.from_pairs(("b",)))

    def test_zero_scaling_and_projection_to_empty(self):
        value = Multiset.from_pairs(("a",), (("a", 4),))
        self.assertEqual(value.scale(0).as_dict(), {})
        self.assertEqual(value.project(()), Multiset.from_pairs(()))

    def test_noninjective_renaming_loses_color_preserves_total(self):
        mixed = Multiset.from_pairs(("blue", "red"), (("blue", 1), ("red", 1)))
        red = Multiset.from_pairs(("blue", "red"), (("red", 2),))
        mapping = {"blue": "token", "red": "token"}
        self.assertNotEqual(mixed, red)
        self.assertEqual(mixed.rename(("token",), mapping), red.rename(("token",), mapping))
        self.assertEqual(mixed.rename(("token",), mapping).total, 2)

    def test_projection_loses_discarded_counts(self):
        left = Multiset.from_pairs(("a", "b"), (("a", 1),))
        right = Multiset.from_pairs(("a", "b"), (("a", 1), ("b", 7)))
        self.assertEqual(left.project(("a",)), right.project(("a",)))
        self.assertNotEqual(left.total, right.total)

    def test_invalid_projection_and_renaming_rejected(self):
        value = Multiset.from_pairs(("a", "b"))
        for bad in (("c",), ("a", "a")):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                value.project(bad)
        for bad in ({"a": "x"}, {"a": "x", "b": "outside"}, {"a": "x", "b": "x", "c": "x"}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                value.rename(("x",), bad)
        with self.assertRaises(ValueError):
            value.rename((), {"a": "x", "b": "x"})

    def test_bounded_multiset_checks(self):
        result = multiset_checks()
        self.assertEqual(result["renaming_homomorphism_cases"], 324)
        self.assertEqual(result["projection_homomorphism_cases"], 324)
        self.assertEqual(result["associativity_cases"], 729)


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.stimuli = ("tile_2", "tile_4", "tile_3", "tile_6")
        self.actions = ("even", "odd")
        self.rule = DeterministicPolicy("rule", self.stimuli, ("even", "even", "odd", "even"))
        self.lookup = DeterministicPolicy("lookup", self.stimuli, ("even", "even", "odd", "odd"))
        self.observed = (("tile_2", "even"), ("tile_4", "even"), ("tile_3", "odd"))

    def test_rule_and_lookup_agree_observed_but_disagree_held_out(self):
        space = version_space(self.stimuli, self.actions, (self.rule, self.lookup), self.observed)
        self.assertEqual(len(space.survivors), 2)
        self.assertEqual(space.unanimous("tile_2"), "even")
        self.assertIsNone(space.unanimous("tile_6"))
        self.assertEqual(space.possible_actions("tile_6"), ("even", "odd"))
        self.assertEqual(space.status("tile_6"), "underdetermined")

    def test_new_observation_separates_these_two_policies_only(self):
        space = version_space(self.stimuli, self.actions, (self.rule, self.lookup),
                              self.observed + (("tile_6", "even"),))
        self.assertEqual(space.survivors, (self.rule,))

    def test_restricting_class_creates_conditional_unanimity(self):
        space = version_space(self.stimuli, self.actions, (self.rule,), self.observed)
        self.assertEqual(space.unanimous("tile_6"), "even")
        self.assertEqual(space.status("tile_6"), "unanimous")

    def test_all_tables_cardinality_and_observation_filter(self):
        policies = enumerate_policies(self.stimuli, self.actions)
        self.assertEqual(len(policies), 16)
        self.assertEqual(len(version_space(self.stimuli, self.actions, policies, self.observed).survivors), 2)

    def test_empty_version_space_is_not_vacuous_unanimity(self):
        space = version_space(self.stimuli, self.actions, (self.lookup,),
                              self.observed + (("tile_6", "even"),))
        self.assertEqual(space.survivors, ())
        self.assertEqual(space.possible_actions("tile_6"), ())
        self.assertIsNone(space.unanimous("tile_6"))
        self.assertEqual(space.status("tile_6"), "empty_version_space")

    def test_empty_admissible_class_is_allowed_and_reported(self):
        self.assertEqual(version_space(self.stimuli, self.actions, (), ()).status("tile_2"),
                         "empty_version_space")

    def test_empty_stimulus_universe_has_one_total_table(self):
        policies = enumerate_policies((), ("left", "right"))
        self.assertEqual(len(policies), 1)
        self.assertEqual(policies[0].responses, ())
        self.assertEqual(len(version_space((), ("left", "right"), policies, ()).survivors), 1)

    def test_repeated_identical_observation_is_idempotent(self):
        once = version_space(self.stimuli, self.actions, (self.rule, self.lookup), self.observed)
        twice = version_space(self.stimuli, self.actions, (self.rule, self.lookup), self.observed * 2)
        self.assertEqual(once, twice)

    def test_conflicting_observation_rejected(self):
        with self.assertRaises(ValueError):
            version_space(self.stimuli, self.actions, (self.rule,),
                          (("tile_2", "even"), ("tile_2", "odd")))

    def test_unknown_observation_rejected(self):
        for bad in ((("outside", "even"),), (("tile_2", "outside"),)):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                version_space(self.stimuli, self.actions, (self.rule,), bad)

    def test_duplicate_names_and_invalid_labels_rejected(self):
        for stimuli, actions in ((("x", "x"), ("a",)), (("x",), ("a", "a")), (("x",), ()),
                                 (("",), ("a",)), ("xyz", ("a",))):
            with self.subTest(stimuli=stimuli, actions=actions), self.assertRaises(ValueError):
                enumerate_policies(stimuli, actions)
        with self.assertRaises(ValueError):
            version_space(self.stimuli, self.actions, (self.rule, self.rule), ())

    def test_policy_requires_total_table_and_valid_names(self):
        bad = [("", ("x",), ("a",)), ("p", ("x",), ()), ("p", ("x", "x"), ("a", "a")),
               ("p", ("x",), ("",)), ("p", ["x"], ("a",)), ("p", ("x",), ["a"])]
        for name, stimuli, responses in bad:
            with self.subTest(name=name, stimuli=stimuli, responses=responses), self.assertRaises(ValueError):
                DeterministicPolicy(name, stimuli, responses)

    def test_admissible_policy_must_match_domain_and_actions(self):
        wrong_domain = DeterministicPolicy("bad_domain", ("x",), ("even",))
        wrong_actions = DeterministicPolicy("bad_actions", self.stimuli, ("outside",) * 4)
        for bad in (wrong_domain, wrong_actions, object()):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                version_space(self.stimuli, self.actions, (bad,), ())

    def test_unknown_prediction_stimulus_rejected(self):
        space = version_space(self.stimuli, self.actions, (self.rule,), ())
        with self.assertRaises(ValueError):
            space.unanimous("outside")
        with self.assertRaises(ValueError):
            self.rule.response("outside")

    def test_equal_complete_behavior_does_not_identify_mechanism(self):
        equivalent = DeterministicPolicy("another_implementation", self.stimuli, self.rule.responses)
        observations = tuple(zip(self.stimuli, self.rule.responses))
        space = version_space(self.stimuli, self.actions, (self.rule, equivalent), observations)
        self.assertEqual(len(space.survivors), 2)
        self.assertEqual(space.unanimous("tile_6"), "even")

    def test_bounded_policy_checks(self):
        result = policy_checks()
        self.assertEqual(result["truth_observation_cases"], 85)
        self.assertEqual(result["individual_prediction_checks"], 228)


if __name__ == "__main__":
    unittest.main()
