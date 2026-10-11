"""Independent reviewer tests. No import of the author's tests or finite oracle.

The habit oracle integrates a finite reset-process sample space. The policy
oracle intersects relational fibers and successively splits blocks. The norm
oracle constructs free choices recursively. unittest checks survive -O/-OO.
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from habit_model import action_inputs, habit_closed_form, habit_trace
from action_model import Policy, admissible_norms, behavioral_classes, compatible_intentions, normative_status

COUNTS = Counter()


def subsets(values):
    return tuple(combinations(values, n) for n in range(len(values) + 1))


def flat_subsets(values):
    return tuple(item for level in subsets(values) for item in level)


def reset_sample_oracle(alpha, initial, inputs):
    """Enumerate every refresh/no-refresh history and integrate its final state.

    A refresh at t sets the state to inputs[t]. Otherwise the previous state
    persists. Initial state 1 has probability initial. This code neither
    iterates the production mean recurrence nor evaluates its weighted sum.
    """
    mass = Q(0)
    for resets in product((False, True), repeat=len(inputs)):
        probability = Q(1)
        last_refresh = None
        for index, refresh in enumerate(resets):
            probability *= alpha if refresh else 1 - alpha
            if refresh:
                last_refresh = index
        terminal = initial if last_refresh is None else inputs[last_refresh]
        mass += probability * terminal
    return mass


def relational_candidates(intentions, contexts, rows, observations):
    fibers = {}
    for i, intention in enumerate(intentions):
        for j, context in enumerate(contexts):
            fibers.setdefault((context, rows[i][j]), set()).add(intention)
    answer = set(intentions)
    for observation in observations:
        answer.intersection_update(fibers.get(observation, set()))
    return tuple(i for i in intentions if i in answer)


def split_partition(intentions, contexts, actions, rows, selected):
    blocks = [set(intentions)] if intentions else []
    for context in selected:
        column = contexts.index(context)
        next_blocks = []
        for block in blocks:
            for action in actions:
                child = {intentions[i] for i in range(len(intentions))
                         if intentions[i] in block and rows[i][column] == action}
                if child:
                    next_blocks.append(child)
        blocks = next_blocks
    return frozenset(frozenset(block) for block in blocks)


def recursive_norms(universe, required, forbidden):
    if set(required).intersection(forbidden):
        return set()
    family = {frozenset(required)}
    for action in universe:
        if action not in required and action not in forbidden:
            family |= {code | {action} for code in family}
    return family


class RegressionTests(unittest.TestCase):
    """Small, independently authored mutation detectors and boundary checks."""

    def test_habit_fraction_and_empty(self):
        self.assertEqual(habit_trace(Q(3, 7), Q(2, 5), ()), (Q(2, 5),))
        self.assertEqual(habit_closed_form(Q(3, 7), Q(2, 5), ()), Q(2, 5))
        for bits in ((0,), (1,), (1, 0, 0), (0, 1, 1), (1, 0, 1, 0)):
            expected = reset_sample_oracle(Q(3, 7), Q(2, 5), bits)
            self.assertEqual(habit_trace(Q(3, 7), Q(2, 5), bits)[-1], expected)
            self.assertEqual(habit_closed_form(Q(3, 7), Q(2, 5), bits), expected)

    def test_habit_order(self):
        alpha, initial = Q(3, 7), Q(2, 5)
        earlier = (1, 0, 1, 0)
        later = (0, 1, 1, 0)
        delta = alpha ** 2 * (1 - alpha) ** 2
        for evaluator in (lambda a, h, u: habit_trace(a, h, u)[-1], habit_closed_form):
            self.assertEqual(evaluator(alpha, initial, later) - evaluator(alpha, initial, earlier), delta)

    def test_habit_rejects_malformed_numbers(self):
        for function in (habit_trace, habit_closed_form):
            for bad in (True, False, 0.2, "1/3", None, 1j):
                with self.assertRaises(TypeError):
                    function(bad, 0, ())
                with self.assertRaises(TypeError):
                    function(Q(1, 3), bad, ())
            for alpha in (Q(-1, 2), 0, 1, Q(3, 2)):
                with self.assertRaises(ValueError):
                    function(alpha, 0, ())
            for initial in (Q(-1, 7), Q(8, 7)):
                with self.assertRaises(ValueError):
                    function(Q(1, 3), initial, ())
            for bits in ((True,), (False,), (Q(1),), (0.0,), (-1,), (2,), (None,)):
                with self.assertRaises(ValueError):
                    function(Q(1, 3), 0, bits)
            with self.assertRaises(TypeError):
                function(Q(1, 3), 0, None)

    def test_action_indicator(self):
        self.assertEqual(action_inputs(iter(("pause", "go", "pause")), "pause"), (1, 0, 1))
        self.assertEqual(action_inputs([], "pause"), ())
        for actions, tracked in ((("",), "pause"), ((3,), "pause"), (("go",), ""), (("go",), None)):
            with self.assertRaises(ValueError):
                action_inputs(actions, tracked)

    def test_scalar_collection_regression(self):
        p = Policy(("c",), ("i",), ("a",), (("a",),))
        for scalar in ("", "a", "withdraw", b"", b"a", b"\x00\x01"):
            calls = (
                lambda: habit_trace(Q(1, 3), 0, scalar),
                lambda: habit_closed_form(Q(1, 3), 0, scalar),
                lambda: action_inputs(scalar, "withdraw"),
                lambda: Policy(scalar, (), (), ()),
                lambda: Policy((), (), (), scalar),
                lambda: Policy(("c",), ("i",), ("a",), (scalar,)),
                lambda: compatible_intentions(p, scalar),
                lambda: compatible_intentions(p, (scalar,)),
                lambda: behavioral_classes(p, scalar),
                lambda: admissible_norms(scalar),
                lambda: admissible_norms(("a",), required=scalar),
                lambda: admissible_norms(("a",), forbidden=scalar),
                lambda: normative_status("a", ("a",), scalar),
                lambda: normative_status("a", ("a",), (scalar,)),
            )
            for call in calls:
                with self.assertRaises(TypeError):
                    call()

    def test_policy_intersection(self):
        p = Policy(("c0", "c1", "c2"), ("i0", "i1", "i2"), ("a", "b"),
                   (("a", "a", "b"), ("a", "b", "a"), ("b", "a", "a")))
        self.assertEqual(compatible_intentions(p, ()), p.intentions)
        self.assertEqual(compatible_intentions(p, (("c0", "a"), ("c1", "a"))), ("i0",))
        self.assertEqual(compatible_intentions(p, (("c0", "a"), ("c0", "b"))), ())
        self.assertEqual(compatible_intentions(p, (("c2", "b"),) * 3), ("i0",))

    def test_partition_refinement(self):
        p = Policy(("c0", "c1"), ("i0", "i1", "i2"), ("a", "b"),
                   (("a", "a"), ("a", "b"), ("b", "a")))
        self.assertEqual(behavioral_classes(p, ()), (("i0", "i1", "i2"),))
        self.assertEqual(behavioral_classes(p, ("c0",)), (("i0", "i1"), ("i2",)))
        self.assertEqual(behavioral_classes(p, ("c0", "c1")), (("i0",), ("i1",), ("i2",)))
        self.assertEqual(behavioral_classes(p, ("c1", "c0")), (("i0",), ("i1",), ("i2",)))

    def test_empty_shapes_and_snapshot(self):
        p = Policy((), (), (), ())
        self.assertEqual(compatible_intentions(p, ()), ())
        self.assertEqual(behavioral_classes(p, ()), ())
        p = Policy((), ("i0", "i1"), (), ((), ()))
        self.assertEqual(compatible_intentions(p, ()), ("i0", "i1"))
        self.assertEqual(behavioral_classes(p, ()), (("i0", "i1"),))
        contexts, intentions, actions, rows = ["c"], ["i"], ["a", "b"], [["a"]]
        p = Policy(contexts, intentions, actions, rows)
        rows[0][0] = "b"
        contexts[0] = "changed"
        self.assertEqual(p.action("i", "c"), "a")

    def test_policy_malformed(self):
        cases = (
            (("c", "c"), ("i",), ("a",), (("a", "a"),)),
            (("c",), ("i", "i"), ("a",), (("a",), ("a",))),
            (("c",), ("i",), ("a", "a"), (("a",),)),
            (("c",), ("i",), ("a",), ()),
            (("c",), ("i",), ("a",), (("a", "a"),)),
            (("c",), ("i",), ("a",), (("z",),)),
            (("",), ("i",), ("a",), (("a",),)),
        )
        for args in cases:
            with self.assertRaises(ValueError):
                Policy(*args)
        for args in (("c", ("i",), ("a",), (("a",),)),
                     (("c",), ("i",), ("a",), ("a",))):
            with self.assertRaises(TypeError):
                Policy(*args)
        p = Policy(("c",), ("i",), ("a",), (("a",),))
        for observations in ((("unknown", "a"),), (("c", "z"),), (("c",),), ((),), (("c", "a", "x"),)):
            with self.assertRaises(ValueError):
                compatible_intentions(p, observations)
        for observations in (("ca",), (None,)):
            with self.assertRaises(TypeError):
                compatible_intentions(p, observations)
        for selected in (("c", "c"), ("z",), (None,)):
            with self.assertRaises(ValueError):
                behavioral_classes(p, selected)
        for i, c in (("z", "c"), ("i", "z")):
            with self.assertRaises(ValueError):
                p.action(i, c)

    def test_norm_family_constraints(self):
        u = ("a", "b", "c", "d")
        self.assertEqual(set(admissible_norms(u, ("a",), ("b", "d"))),
                         {frozenset(("a",)), frozenset(("a", "c"))})
        self.assertEqual(admissible_norms(u, ("a",), ("a",)), ())
        self.assertEqual(admissible_norms(()), (frozenset(),))

    def test_four_normative_statuses(self):
        u = ("a", "b")
        self.assertEqual(normative_status("a", u, ()), "inconsistent")
        self.assertEqual(normative_status("a", u, ((),)), "all_forbid")
        self.assertEqual(normative_status("a", u, (("a",),)), "all_permit")
        self.assertEqual(normative_status("a", u, ((), ("a",))), "underdetermined")
        self.assertEqual(normative_status("a", u, (("a",), ("a", "b"))), "all_permit")
        self.assertEqual(normative_status("a", u, ((), ("b",))), "all_forbid")

    def test_norm_malformed(self):
        for required, forbidden in ((("z",), ()), ((), ("z",)), (("a", "a"), ())):
            with self.assertRaises(ValueError):
                admissible_norms(("a", "b"), required, forbidden)
        with self.assertRaises(ValueError):
            normative_status("z", ("a",), ())
        for family in ((("z",),), (("a", "a"),)):
            with self.assertRaises(ValueError):
                normative_status("a", ("a",), family)
        with self.assertRaises(TypeError):
            normative_status("a", ("a",), ("a",))


class ExhaustiveTests(unittest.TestCase):
    def test_documented_demo_examples(self):
        from demo import run_demo
        output = run_demo()
        self.assertEqual(output["habit"]["trace"], ["0", "1/2", "3/4", "7/8", "7/16", "7/32"])
        self.assertEqual(output["habit"]["closed_form_final"], "7/32")
        self.assertEqual(output["habit"]["same_count_different_order"], {"10": "1/4", "01": "1/2"})
        self.assertEqual(output["inference"]["candidates_by_prefix"],
                         [["fear_harm", "desire_quiet", "desire_rest"],
                          ["fear_harm", "desire_quiet", "desire_rest"],
                          ["fear_harm", "desire_rest"], ["fear_harm"]])
        counterexample = output["inference"]["transfer_counterexample"]
        self.assertEqual(counterexample["target_true_intention"], "desire_quiet")
        self.assertEqual(counterexample["inferred_with_observers_table"], ("fear_harm",))
        self.assertEqual(output["norms"]["unconstrained_code_count"], 8)
        self.assertEqual(output["norms"]["withdraw_unconstrained"], "underdetermined")
        self.assertEqual(output["norms"]["partial_bridge"]["withdraw_status"], "underdetermined")
        self.assertEqual(output["norms"]["full_bridge"]["withdraw_status"], "all_permit")
        self.assertEqual(output["norms"]["contradictory_bridge_status"], "inconsistent")

    def test_habit_reset_sample_space(self):
        alphas = (Q(1, 5), Q(1, 3), Q(1, 2), Q(3, 5), Q(5, 7))
        initials = (Q(0), Q(1, 5), Q(1, 2), Q(4, 5), Q(1))
        for alpha, initial in product(alphas, initials):
            for length in range(7):
                for bits in product((0, 1), repeat=length):
                    expected = reset_sample_oracle(alpha, initial, bits)
                    trace = habit_trace(alpha, initial, bits)
                    self.assertEqual(trace[-1], expected)
                    self.assertEqual(habit_closed_form(alpha, initial, bits), expected)
                    self.assertEqual(len(trace), length + 1)
                    self.assertEqual(trace[0], initial)
                    self.assertTrue(all(isinstance(h, Q) and 0 <= h <= 1 for h in trace))
                    COUNTS["habit_histories"] += 1
                    COUNTS["reset_histories_integrated"] += 2 ** length

    def test_habit_metamorphic_laws(self):
        for alpha in (Q(1, 101), Q(3, 7), Q(100, 101)):
            for n in (0, 1, 2, 9, 40):
                q = 1 - alpha
                initial = Q(5, 9)
                self.assertEqual(habit_trace(alpha, initial, (1,) * n)[-1], 1 - (1 - initial) * q ** n)
                self.assertEqual(habit_closed_form(alpha, initial, (0,) * n), initial * q ** n)
                periodic_even_limit = q / (1 + q)
                self.assertEqual(habit_trace(alpha, initial, (1, 0) * n)[-1],
                                 periodic_even_limit + q ** (2 * n) * (initial - periodic_even_limit))
                bits = tuple((k * 7 + 1) % 2 for k in range(n))
                low = habit_trace(alpha, Q(2, 9), bits)
                high = habit_trace(alpha, Q(8, 9), bits)
                self.assertEqual(high[-1] - low[-1], Q(2, 3) * q ** n)
                self.assertEqual(habit_trace(alpha, 1 - initial, tuple(1 - u for u in bits))[-1],
                                 1 - habit_trace(alpha, initial, bits)[-1])
                for k, u in enumerate(bits):
                    self.assertGreaterEqual(low[k + 1], low[k]) if u else self.assertLessEqual(low[k + 1], low[k])
                split = n // 2
                self.assertEqual(habit_trace(alpha, low[split], bits[split:]), low[split:])
                self.assertEqual(habit_trace(alpha, initial, iter(bits)), habit_trace(alpha, initial, bits))
                COUNTS["habit_metamorphic_cases"] += 1

    def test_policy_relations_and_refinement(self):
        contexts, intentions, actions = ("x", "y", "z"), ("i", "j", "k"), ("a", "b")
        observation_alphabet = tuple(product(contexts, actions))
        records = tuple(record for n in range(4) for record in product(observation_alphabet, repeat=n))
        selected_sets = flat_subsets(contexts)
        for cells in product(actions, repeat=9):
            rows = (cells[:3], cells[3:6], cells[6:])
            p = Policy(contexts, intentions, actions, rows)
            COUNTS["policy_tables"] += 1
            for record in records:
                actual = compatible_intentions(p, record)
                expected = relational_candidates(intentions, contexts, rows, record)
                self.assertEqual(actual, expected)
                self.assertEqual(compatible_intentions(p, iter(record)), expected)
                COUNTS["policy_records"] += 1
            partitions = {}
            for selected in selected_sets:
                result = behavioral_classes(p, selected)
                actual = frozenset(frozenset(block) for block in result)
                self.assertEqual(actual, split_partition(intentions, contexts, actions, rows, selected))
                self.assertEqual(Counter(i for block in result for i in block), Counter(intentions))
                partitions[frozenset(selected)] = actual
                for index, intention in enumerate(intentions):
                    record = tuple((context, rows[index][contexts.index(context)]) for context in selected)
                    selected_block = next(block for block in actual if intention in block)
                    self.assertEqual(frozenset(compatible_intentions(p, record)), selected_block)
                    COUNTS["candidate_equals_equivalence_class"] += 1
                COUNTS["policy_partitions"] += 1
            for small, large in product(partitions, repeat=2):
                if small <= large:
                    self.assertTrue(all(any(block <= parent for parent in partitions[small])
                                        for block in partitions[large]))
                    COUNTS["partition_refinements"] += 1

    def test_norm_families_recursive_oracle(self):
        for size in range(5):
            universe = tuple("abcd"[:size])
            choices = flat_subsets(universe)
            for required, forbidden in product(choices, repeat=2):
                actual = admissible_norms(universe, required, forbidden)
                expected = recursive_norms(universe, required, forbidden)
                self.assertEqual(set(actual), expected)
                self.assertEqual(len(actual), len(expected))
                expected_size = 0 if set(required) & set(forbidden) else 2 ** (size - len(set(required) | set(forbidden)))
                self.assertEqual(len(actual), expected_size)
                for action in universe:
                    expected_status = ("inconsistent" if not expected else
                                       "all_permit" if action in required else
                                       "all_forbid" if action in forbidden else "underdetermined")
                    self.assertEqual(normative_status(action, universe, actual), expected_status)
                    COUNTS["bridge_status_queries"] += 1
                COUNTS["norm_bridge_pairs"] += 1

    def test_arbitrary_norm_families_via_union_intersection(self):
        universe = ("a", "b", "c")
        codes = tuple(frozenset(code) for code in flat_subsets(universe))
        for family in flat_subsets(codes):
            union = frozenset().union(*family)
            intersection = frozenset(universe).intersection(*family)
            for action in universe:
                expected = ("inconsistent" if not family else "all_permit" if action in intersection else
                            "all_forbid" if action not in union else "underdetermined")
                self.assertEqual(normative_status(action, universe, family), expected)
                self.assertEqual(normative_status(action, universe, tuple(reversed(family)) + family), expected)
                self.assertEqual(normative_status(action, universe, iter(family)), expected)
                COUNTS["arbitrary_family_status_queries"] += 1
            COUNTS["arbitrary_norm_families"] += 1


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RegressionTests)
    if "--quick" not in sys.argv:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ExhaustiveTests))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({"status": "PASS" if result.wasSuccessful() else "FAIL",
                      "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
                      "optimize": sys.flags.optimize, "counts": dict(sorted(COUNTS.items()))}, indent=2))
    sys.exit(0 if result.wasSuccessful() else 1)
