"""Explicit unittest checks remain active under Python -O and -OO."""

import unittest
from fractions import Fraction as Q

from habit_model import action_inputs, habit_closed_form, habit_trace
from action_model import Policy, admissible_norms, behavioral_classes, compatible_intentions, normative_status
from demo import example_policy, run_demo


class HabitTests(unittest.TestCase):
    def test_connected_trace(self):
        self.assertEqual(habit_trace(Q(1, 2), 0, (1, 1, 1, 0, 0)),
                         (Q(0), Q(1, 2), Q(3, 4), Q(7, 8), Q(7, 16), Q(7, 32)))

    def test_closed_form_nonzero_initial(self):
        self.assertEqual(habit_closed_form(Q(2, 3), Q(1, 4), (1, 0, 1)), Q(3, 4))
        self.assertEqual(habit_trace(Q(2, 3), Q(1, 4), (1, 0, 1))[-1], Q(3, 4))

    def test_empty_input(self):
        self.assertEqual(habit_trace(Q(1, 3), Q(2, 5), ()), (Q(2, 5),))
        self.assertEqual(habit_closed_form(Q(1, 3), Q(2, 5), ()), Q(2, 5))

    def test_repetition_and_disuse(self):
        self.assertEqual(habit_trace(Q(1, 2), 0, (1,) * 8)[-1], Q(255, 256))
        self.assertEqual(habit_trace(Q(1, 2), 1, (0,) * 8)[-1], Q(1, 256))

    def test_order_matters(self):
        self.assertEqual(habit_trace(Q(1, 2), 0, (1, 0))[-1], Q(1, 4))
        self.assertEqual(habit_trace(Q(1, 2), 0, (0, 1))[-1], Q(1, 2))
        self.assertEqual(habit_closed_form(Q(1, 2), 0, (1, 0)), Q(1, 4))
        self.assertEqual(habit_closed_form(Q(1, 2), 0, (0, 1)), Q(1, 2))

    def test_initial_difference_contracts(self):
        a, path = Q(2, 5), (1, 0, 1, 1)
        difference = habit_trace(a, Q(4, 5), path)[-1] - habit_trace(a, Q(1, 5), path)[-1]
        self.assertEqual(difference, (1 - a) ** len(path) * Q(3, 5))

    def test_endpoint_fixed_points(self):
        self.assertEqual(habit_trace(Q(1, 3), 1, (1, 1)), (Q(1),) * 3)
        self.assertEqual(habit_trace(Q(1, 3), 0, (0, 0)), (Q(0),) * 3)

    def test_action_indicator(self):
        self.assertEqual(action_inputs(("withdraw", "stay", "withdraw"), "withdraw"), (1, 0, 1))
        self.assertEqual(action_inputs((), "withdraw"), ())

    def test_bad_rationals(self):
        for function in (habit_trace, habit_closed_form):
            for bad in (0.5, True, "1/2", None):
                with self.subTest(function=function.__name__, bad=bad):
                    with self.assertRaises(TypeError):
                        function(bad, 0, ())
                    with self.assertRaises(TypeError):
                        function(Q(1, 2), bad, ())

    def test_bad_domains(self):
        for function in (habit_trace, habit_closed_form):
            for scalar in ("", "01", b"", b"\x00\x01"):
                with self.assertRaises(TypeError):
                    function(Q(1, 2), 0, scalar)
            for alpha in (-1, 0, 1, 2):
                with self.assertRaises(ValueError):
                    function(alpha, 0, ())
            for initial in (-1, 2):
                with self.assertRaises(ValueError):
                    function(Q(1, 2), initial, ())
            for inputs in ((True,), (Q(1),), (2,), (-1,), (0.0,)):
                with self.assertRaises(ValueError):
                    function(Q(1, 2), 0, inputs)

    def test_bad_action_labels(self):
        for scalar in ("", "withdraw", b"", b"withdraw"):
            with self.assertRaises(TypeError):
                action_inputs(scalar, "withdraw")
        for actions, tracked in ((("",), "a"), ((None,), "a"), (("a",), "")):
            with self.assertRaises(ValueError):
                action_inputs(actions, tracked)


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = example_policy()

    def test_prefix_candidates(self):
        observations = (("alarm", "withdraw"), ("quiet", "stay"), ("invitation", "approach"))
        self.assertEqual(compatible_intentions(self.policy, observations[:1]), self.policy.intentions)
        self.assertEqual(compatible_intentions(self.policy, observations[:2]), ("fear_harm", "desire_rest"))
        self.assertEqual(compatible_intentions(self.policy, observations), ("fear_harm",))

    def test_equivalence_refinement(self):
        self.assertEqual(behavioral_classes(self.policy, ()), (self.policy.intentions,))
        self.assertEqual(behavioral_classes(self.policy, ("alarm",)), (self.policy.intentions,))
        self.assertEqual(behavioral_classes(self.policy, ("alarm", "quiet")),
                         (("fear_harm", "desire_rest"), ("desire_quiet",)))
        self.assertEqual(behavioral_classes(self.policy, self.policy.contexts),
                         tuple((i,) for i in self.policy.intentions))

    def test_impossible_and_conflicting(self):
        self.assertEqual(compatible_intentions(self.policy, (("alarm", "approach"),)), ())
        self.assertEqual(compatible_intentions(self.policy, (("alarm", "withdraw"), ("alarm", "stay"))), ())

    def test_repeated_observation(self):
        observation = (("quiet", "stay"),)
        self.assertEqual(compatible_intentions(self.policy, observation),
                         compatible_intentions(self.policy, observation * 3))

    def test_empty_policy(self):
        empty = Policy((), (), (), ())
        self.assertEqual(compatible_intentions(empty, ()), ())
        self.assertEqual(behavioral_classes(empty, ()), ())
        no_contexts = Policy((), ("i", "j"), (), ((), ()))
        self.assertEqual(behavioral_classes(no_contexts, ()), (("i", "j"),))

    def test_transfer_counterexample(self):
        data = run_demo()["inference"]["transfer_counterexample"]
        self.assertEqual(data["target_true_intention"], "desire_quiet")
        self.assertEqual(data["inferred_with_observers_table"], ("fear_harm",))

    def test_invalid_policy(self):
        bad = [(("x", "x"), ("i",), ("a",), (("a", "a"),)),
               (("x",), ("i", "i"), ("a",), (("a",), ("a",))),
               (("x",), ("i",), ("a", "a"), (("a",),)),
               (("x",), ("i",), ("a",), ()),
               (("x",), ("i",), ("a",), ((),)),
               (("x",), ("i",), ("a",), (("b",),)),
               (("",), ("i",), ("a",), (("a",),))]
        for arguments in bad:
            with self.subTest(arguments=arguments):
                with self.assertRaises(ValueError):
                    Policy(*arguments)
        with self.assertRaises(TypeError):
            Policy(("x",), ("i",), ("a",), ("a",))
        for scalar in ("", b""):
            with self.assertRaises(TypeError):
                Policy((), (), (), scalar)
            with self.assertRaises(TypeError):
                Policy((), ("i",), (), (scalar,))
            for position in range(3):
                arguments = [(), (), (), ()]
                arguments[position] = scalar
                with self.assertRaises(TypeError):
                    Policy(*arguments)

    def test_invalid_observations_and_contexts(self):
        for observations in ((("unknown", "stay"),), (("alarm", "unknown"),), (("alarm",),)):
            with self.assertRaises(ValueError):
                compatible_intentions(self.policy, observations)
        with self.assertRaises(TypeError):
            compatible_intentions(self.policy, ("ab",))
        for scalar in ("", b""):
            with self.assertRaises(TypeError):
                compatible_intentions(self.policy, scalar)
            with self.assertRaises(TypeError):
                compatible_intentions(self.policy, (scalar,))
            with self.assertRaises(TypeError):
                behavioral_classes(self.policy, scalar)
        for contexts in (("unknown",), ("alarm", "alarm")):
            with self.assertRaises(ValueError):
                behavioral_classes(self.policy, contexts)
        with self.assertRaises(ValueError):
            self.policy.action("unknown", "alarm")


class NormTests(unittest.TestCase):
    def setUp(self):
        self.universe = ("withdraw", "stay", "approach")

    def test_unconstrained_family(self):
        codes = admissible_norms(self.universe)
        self.assertEqual(len(codes), 8)
        for action in self.universe:
            self.assertEqual(normative_status(action, self.universe, codes), "underdetermined")

    def test_partial_bridge(self):
        codes = admissible_norms(self.universe, ("stay",), ("approach",))
        self.assertEqual(set(codes), {frozenset(("stay",)), frozenset(("stay", "withdraw"))})
        self.assertEqual(normative_status("withdraw", self.universe, codes), "underdetermined")
        self.assertEqual(normative_status("stay", self.universe, codes), "all_permit")
        self.assertEqual(normative_status("approach", self.universe, codes), "all_forbid")

    def test_full_bridge(self):
        codes = admissible_norms(self.universe, ("withdraw", "stay"), ("approach",))
        self.assertEqual(codes, (frozenset(("withdraw", "stay")),))
        self.assertEqual(normative_status("withdraw", self.universe, codes), "all_permit")

    def test_inconsistent_bridge(self):
        codes = admissible_norms(self.universe, ("withdraw",), ("withdraw",))
        self.assertEqual(codes, ())
        self.assertEqual(normative_status("withdraw", self.universe, codes), "inconsistent")

    def test_empty_universe_has_one_code(self):
        self.assertEqual(admissible_norms(()), (frozenset(),))
        with self.assertRaises(ValueError):
            normative_status("a", (), (frozenset(),))

    def test_single_empty_code_forbids(self):
        self.assertEqual(normative_status("withdraw", self.universe, (frozenset(),)), "all_forbid")

    def test_invalid_norms(self):
        for required, forbidden in ((("unknown",), ()), ((), ("unknown",)), (("stay", "stay"), ())):
            with self.assertRaises(ValueError):
                admissible_norms(self.universe, required, forbidden)
        for action, codes in (("unknown", ()), ("withdraw", (("unknown",),))):
            with self.assertRaises(ValueError):
                normative_status(action, self.universe, codes)
        with self.assertRaises(TypeError):
            admissible_norms("abc")
        for scalar in ("", b""):
            for position in range(3):
                arguments = [(), (), ()]
                arguments[position] = scalar
                with self.assertRaises(TypeError):
                    admissible_norms(*arguments)
            with self.assertRaises(TypeError):
                normative_status("withdraw", self.universe, scalar)
            with self.assertRaises(TypeError):
                normative_status("withdraw", self.universe, (scalar,))

    def test_same_habit_opposite_norms(self):
        value = habit_trace(Q(1, 2), 0, (1, 1, 1))[-1]
        self.assertEqual(value, Q(7, 8))
        self.assertEqual(normative_status("withdraw", self.universe, (("stay",),)), "all_forbid")
        self.assertEqual(normative_status("withdraw", self.universe, (("stay", "withdraw"),)), "all_permit")


if __name__ == "__main__":
    unittest.main()
