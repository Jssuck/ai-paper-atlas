"""Author tests: unittest checks survive -O and -OO; no bare assert statements."""
import unittest
from dataclasses import FrozenInstanceError
from model import FixedPoint, HornSystem, Rule, filter_evidence
from demo import examples


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.H = frozenset({"a", "b", "c"})

    def test_no_observations(self):
        self.assertEqual(filter_evidence(self.H, ()), (self.H,))

    def test_two_stage_filter(self):
        self.assertEqual(filter_evidence(self.H, ({"a", "b"}, {"b", "c"})),
                         (self.H, frozenset({"a", "b"}), frozenset({"b"})))

    def test_initial_restriction(self):
        self.assertEqual(filter_evidence(self.H, ({"a", "b"},), {"b", "c"})[-1], {"b"})

    def test_empty_initial_stays_empty(self):
        self.assertEqual(filter_evidence(self.H, (self.H,), ())[-1], frozenset())

    def test_empty_observation(self):
        self.assertEqual(filter_evidence(self.H, ((), self.H))[-1], frozenset())

    def test_noisy_observation_can_remove_truth(self):
        self.assertNotIn("a", filter_evidence(self.H, ({"b"},))[-1])

    def test_unrepresented_truth_not_created(self):
        self.assertNotIn("a", filter_evidence(self.H, ({"a"},), {"b"})[-1])

    def test_order_final_not_intermediate(self):
        left = filter_evidence(self.H, ({"a", "b"}, {"b", "c"}))
        right = filter_evidence(self.H, ({"b", "c"}, {"a", "b"}))
        self.assertEqual(left[-1], right[-1])
        self.assertNotEqual(left[1], right[1])

    def test_repeated_evidence_idempotent(self):
        self.assertEqual(filter_evidence(self.H, ({"a", "b"},) * 3)[-1], {"a", "b"})

    def test_empty_universe(self):
        self.assertEqual(filter_evidence((), ((),)), (frozenset(), frozenset()))

    def test_unknown_evidence_rejected_after_empty(self):
        with self.assertRaises(ValueError):
            filter_evidence(self.H, ((), {"outside"}))

    def test_unknown_initial_rejected(self):
        with self.assertRaises(ValueError):
            filter_evidence(self.H, (), {"outside"})

    def test_bare_strings_rejected(self):
        for args in (("abc", ()), (self.H, "a"), (self.H, ("a",))):
            with self.subTest(args=args):
                with self.assertRaises(TypeError):
                    filter_evidence(*args)

    def test_invalid_labels_rejected(self):
        for bad in (("",), (1,), (None,)):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    filter_evidence(bad, ())

    def test_generators_and_input_immutability(self):
        initial = {"a", "b"}
        evidence = {"b", "c"}
        trace = filter_evidence(iter(self.H), (x for x in (evidence,)), initial)
        initial.clear()
        evidence.clear()
        self.assertEqual(trace, (frozenset({"a", "b"}), frozenset({"b"})))
        self.assertIsInstance(trace[-1], frozenset)


class HornTests(unittest.TestCase):
    def setUp(self):
        self.V = frozenset({"a", "b", "c"})
        self.cycle = HornSystem(self.V, (
            Rule({"a"}, "b"), Rule({"b"}, "c"), Rule({"c"}, "a")))
        self.chain = HornSystem(self.V, (Rule({"a"}, "b"), Rule({"b"}, "c")))

    def test_unanchored_cycle_gap(self):
        self.assertEqual(self.cycle.fixed_point("least").result, frozenset())
        self.assertEqual(self.cycle.fixed_point("greatest").result, self.V)

    def test_anchor_grounds_cycle(self):
        self.assertEqual(self.cycle.fixed_point("least", {"a"}).result, self.V)
        self.assertEqual(self.cycle.fixed_point("greatest", {"a"}).result, self.V)

    def test_least_trace_rounds(self):
        result = self.chain.fixed_point("least", {"a"})
        self.assertEqual(result.states, (frozenset(), frozenset({"a"}),
                                        frozenset({"a", "b"}), self.V))
        self.assertEqual(result.changes, 3)

    def test_greatest_trace_rounds(self):
        result = self.chain.fixed_point("greatest")
        self.assertEqual(result.states, (self.V, frozenset({"b", "c"}),
                                        frozenset({"c"}), frozenset()))
        self.assertEqual(result.changes, 3)

    def test_one_withdrawal_collapses_cycle(self):
        self.assertEqual(self.cycle.fixed_point("greatest", (), {"b"}).result, frozenset())

    def test_anchor_removal_differs_from_claim_withdrawal(self):
        self.assertEqual(self.cycle.fixed_point("greatest").result, self.V)
        self.assertEqual(self.cycle.fixed_point("greatest", (), {"a"}).result, frozenset())

    def test_anchor_removed_chain_collapses(self):
        self.assertEqual(self.chain.fixed_point("greatest").result, frozenset())

    def test_alternative_anchor_survives(self):
        system = HornSystem({"a", "b", "c", "d"}, (
            Rule({"a"}, "b"), Rule({"b"}, "c"), Rule({"d"}, "c")))
        self.assertEqual(system.fixed_point("least", {"d"}).result, {"c", "d"})

    def test_conjunction_needs_every_premise(self):
        system = HornSystem(self.V, (Rule({"a", "b"}, "c"),))
        self.assertEqual(system.fixed_point("least", {"a"}).result, {"a"})
        self.assertEqual(system.fixed_point("least", {"a", "b"}).result, self.V)

    def test_distinct_rules_are_alternatives(self):
        system = HornSystem(self.V, (Rule({"a"}, "c"), Rule({"b"}, "c")))
        self.assertEqual(system.fixed_point("least", {"a"}).result, {"a", "c"})
        self.assertEqual(system.fixed_point("least", {"b"}).result, {"b", "c"})

    def test_withdrawal_overrides_anchor(self):
        self.assertEqual(self.cycle.fixed_point("least", {"a"}, {"a"}).result, frozenset())
        self.assertEqual(self.cycle.fixed_point("greatest", {"a"}, {"a"}).result, frozenset())

    def test_withdrawal_blocks_derived_heads(self):
        self.assertEqual(self.chain.fixed_point("least", {"a"}, {"b"}).result, {"a"})

    def test_withdrawn_premise_not_available(self):
        self.assertEqual(self.chain.fixed_point("greatest", {"a"}, {"b"}).result, {"a"})

    def test_empty_system(self):
        system = HornSystem((), ())
        for kind in ("least", "greatest"):
            self.assertEqual(system.fixed_point(kind).states, (frozenset(),))

    def test_no_rules_keeps_anchors_only(self):
        system = HornSystem(self.V, ())
        self.assertEqual(system.fixed_point("least", {"b"}).result, {"b"})
        self.assertEqual(system.fixed_point("greatest", {"b"}).result, {"b"})

    def test_self_loop_is_not_external_ground(self):
        system = HornSystem({"a"}, (Rule({"a"}, "a"),))
        self.assertEqual(system.fixed_point("least").result, frozenset())
        self.assertEqual(system.fixed_point("greatest").result, {"a"})

    def test_immediate_is_not_inflationary(self):
        self.assertEqual(self.chain.immediate({"a"}), {"b"})

    def test_duplicates_and_rule_order_do_not_change_result(self):
        altered = HornSystem(self.V, tuple(reversed(self.chain.rules)) + self.chain.rules)
        for kind in ("least", "greatest"):
            self.assertEqual(altered.fixed_point(kind, {"a"}), self.chain.fixed_point(kind, {"a"}))

    def test_rule_immutable_snapshot(self):
        body = {"a"}
        rule = Rule(body, "b")
        body.clear()
        self.assertEqual(rule.body, {"a"})
        with self.assertRaises(FrozenInstanceError):
            rule.head = "c"

    def test_invalid_rule_rejected(self):
        for body, head in (((), "a"), ({"a"}, ""), ({"a"}, None), ({""}, "a")):
            with self.subTest(body=body, head=head):
                with self.assertRaises(ValueError):
                    Rule(body, head)

    def test_unknown_rule_labels_rejected(self):
        for rule in (Rule({"z"}, "a"), Rule({"a"}, "z")):
            with self.assertRaises(ValueError):
                HornSystem(self.V, (rule,))
        with self.assertRaises(TypeError):
            HornSystem(self.V, ("not a rule",))

    def test_unknown_context_and_invalid_state_rejected(self):
        for kwargs in ({"anchors": {"z"}}, {"withdrawn": {"z"}}):
            with self.assertRaises(ValueError):
                self.chain.fixed_point("least", **kwargs)
        with self.assertRaises(ValueError):
            self.chain.immediate({"b"}, withdrawn={"b"})
        with self.assertRaises(ValueError):
            self.chain.fixed_point("unsupported kind")

    def test_system_immutable_snapshot(self):
        claims = {"a", "b"}
        rules = [Rule({"a"}, "b")]
        system = HornSystem(claims, rules)
        claims.clear()
        rules.clear()
        self.assertEqual(system.claims, {"a", "b"})
        self.assertEqual(len(system.rules), 1)
        self.assertIsInstance(system.fixed_point("least", {"a"}).result, frozenset)
        raw = [{"a"}]
        snapshot = FixedPoint("least", raw)
        raw[0].clear()
        self.assertEqual(snapshot.states, (frozenset({"a"}),))
        for kind, states in (("invalid", [set()]), ("least", [])):
            with self.assertRaises(ValueError):
                FixedPoint(kind, states)
        with self.assertRaises(TypeError):
            FixedPoint("least", "a")

    def test_fixed_point_is_stable_and_trace_bounded(self):
        for system in (self.chain, self.cycle):
            for kind in ("least", "greatest"):
                point = system.fixed_point(kind, {"a"}, {"c"})
                self.assertEqual(system.immediate(point.result, {"a"}, {"c"}), point.result)
                self.assertLessEqual(point.changes, 2)

    def test_demo_lexical_indeterminacy(self):
        data = examples()
        self.assertEqual(len(data["lexical"]["warm_bright_examples_only"][-1]), 2)
        self.assertEqual(data["lexical"]["contrasting_example"][-1], ["q_means_warm"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
