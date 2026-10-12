"""Bounded independent oracles and explicit API boundaries (stdlib unittest)."""

from itertools import combinations, permutations, product
import unittest

from demo import planning_example, teaching_example
from model import (
    HypothesisSpace, Lesson, PlanningProblem, closure, greedy_plan,
    is_identified, is_realizable, minimum_teaching_set, replay, shortest_plan,
    version_space,
)


def subsets(items):
    return tuple(choice for size in range(len(items) + 1) for choice in combinations(items, size))


def reference_paths(problem):
    """Enumerate lesson permutations, without closure or BFS.

    In a monotone model a second use of any lesson adds nothing, so an optimal
    path never needs a repeat. Redundant first uses are allowed by this oracle;
    they cannot improve its minimum length.
    """
    states = {problem.initial}
    best = 0 if problem.goal <= problem.initial else None
    for length in range(1, len(problem.lessons) + 1):
        for path in permutations(problem.lessons, length):
            state = set(problem.initial)
            for lesson in path:
                if not all(skill in state for skill in lesson.prerequisites):
                    break
                state.update(lesson.gains)
            else:
                states.add(frozenset(state))
                if all(skill in state for skill in problem.goal):
                    if best is None or length < best:
                        best = length
    union = frozenset().union(*states)
    return union, best


class PlanningTests(unittest.TestCase):
    def test_supplied_counterexample(self):
        problem = planning_example()
        self.assertEqual(closure(problem), problem.skills)
        self.assertEqual(shortest_plan(problem), ("E", "F"))
        self.assertEqual(greedy_plan(problem), ("D", "A", "B", "C"))
        self.assertEqual(replay(problem, ("E", "F")), frozenset("cg"))
        self.assertEqual(replay(problem, ("D", "A", "B", "C")), frozenset("abguvw"))

    def test_cycle_without_seed(self):
        problem = PlanningProblem(
            frozenset("ab"), frozenset(), frozenset("a"),
            (Lesson("P", frozenset("b"), frozenset("a")),
             Lesson("Q", frozenset("a"), frozenset("b"))),
        )
        self.assertEqual(closure(problem), frozenset())
        self.assertIsNone(shortest_plan(problem))
        self.assertIsNone(greedy_plan(problem))

    def test_cycle_with_seed(self):
        problem = PlanningProblem(
            frozenset("ab"), frozenset("a"), frozenset("b"),
            (Lesson("P", frozenset("b"), frozenset("a")),
             Lesson("Q", frozenset("a"), frozenset("b"))),
        )
        self.assertEqual(closure(problem), problem.skills)
        self.assertEqual(shortest_plan(problem), ("Q",))

    def test_empty_universe(self):
        problem = PlanningProblem(frozenset(), frozenset(), frozenset(), ())
        self.assertEqual(closure(problem), frozenset())
        self.assertEqual(shortest_plan(problem), ())
        self.assertEqual(greedy_plan(problem), ())
        self.assertEqual(replay(problem, ()), frozenset())

    def test_goal_already_met(self):
        problem = PlanningProblem(frozenset("ab"), frozenset("a"), frozenset("a"), ())
        self.assertEqual(shortest_plan(problem), ())
        self.assertEqual(greedy_plan(problem), ())

    def test_missing_rule_unreachable(self):
        problem = PlanningProblem(frozenset("a"), frozenset(), frozenset("a"), ())
        self.assertIsNone(shortest_plan(problem))

    def test_ties_follow_supplied_order(self):
        problem = PlanningProblem(
            frozenset("a"), frozenset(), frozenset("a"),
            (Lesson("Z", frozenset(), frozenset("a")),
             Lesson("A", frozenset(), frozenset("a"))),
        )
        self.assertEqual(shortest_plan(problem), ("Z",))
        self.assertEqual(greedy_plan(problem), ("A",))

    def test_redundant_transitions_rejected(self):
        problem = planning_example()
        with self.assertRaises(ValueError):
            replay(problem, ("A", "A"))
        with self.assertRaises(ValueError):
            replay(problem, ("B",))
        with self.assertRaises(ValueError):
            replay(problem, ("missing",))

    def test_partial_path_allowed(self):
        self.assertEqual(replay(planning_example(), ("A",)), frozenset("a"))

    def test_exhaustive_two_skill_up_to_three_rules(self):
        sets = tuple(frozenset(choice) for choice in subsets(("a", "b")))
        rules = tuple((pre, gain) for pre in sets for gain in sets if gain)
        cases = 0
        for size in range(4):
            for selected in combinations(rules, size):
                lessons = tuple(Lesson(str(i), pre, gain) for i, (pre, gain) in enumerate(selected))
                for initial, goal in product(sets, repeat=2):
                    problem = PlanningProblem(frozenset("ab"), initial, goal, lessons)
                    expected_closure, expected_length = reference_paths(problem)
                    actual = shortest_plan(problem)
                    self.assertEqual(closure(problem), expected_closure)
                    self.assertEqual(None if actual is None else len(actual), expected_length)
                    self.assertEqual(goal <= expected_closure, actual is not None)
                    if actual is not None:
                        self.assertTrue(goal <= replay(problem, actual))
                        self.assertLessEqual(len(actual), len(problem.skills - initial))
                    greedy = greedy_plan(problem)
                    self.assertEqual(greedy is not None, actual is not None)
                    if greedy is not None:
                        self.assertTrue(goal <= replay(problem, greedy))
                    cases += 1
        self.assertEqual(cases, 4784)


class TeachingTests(unittest.TestCase):
    def test_supplied_filtering_and_minimum(self):
        space = teaching_example()
        target = (0, 0, 0, 0)
        expected = (("x0", 0), ("x1", 0), ("x2", 0))
        self.assertEqual(minimum_teaching_set(space, target), expected)
        self.assertEqual(version_space(space, ()), (0, 1, 2, 3))
        self.assertEqual(version_space(space, expected[:1]), (0, 2, 3))
        self.assertEqual(version_space(space, expected[:2]), (0, 3))
        self.assertEqual(version_space(space, expected), (0,))
        self.assertTrue(is_identified(space, target, expected))
        self.assertTrue(is_identified(space, target, (("x0", 0), ("x1", 0), ("x3", 0))))

    def test_duplicate_rows_are_behavior_equivalent(self):
        space = HypothesisSpace(("x",), ((0,), (0,), (1,)))
        examples = minimum_teaching_set(space, (0,))
        self.assertEqual(examples, (("x", 0),))
        self.assertEqual(version_space(space, examples), (0, 1))
        self.assertTrue(is_identified(space, (0,), examples))

    def test_zero_examples_for_one_behavior(self):
        space = HypothesisSpace(("x",), ((0,), (0,)))
        self.assertEqual(minimum_teaching_set(space, (0,)), ())
        self.assertTrue(is_identified(space, (0,), ()))

    def test_unrealizable_is_distinct_from_current_empty_space(self):
        space = HypothesisSpace(("x", "y"), ((0, 0), (1, 1)))
        target = (0, 1)
        self.assertFalse(is_realizable(space, target))
        self.assertIsNone(minimum_teaching_set(space, target))
        self.assertEqual(version_space(space, (("x", 0),)), (0,))
        self.assertFalse(is_identified(space, target, (("x", 0),)))
        self.assertEqual(version_space(space, (("x", 0), ("y", 1))), ())

    def test_contradictions_and_repeated_observations(self):
        space = HypothesisSpace(("x",), ((0,), (1,)))
        self.assertEqual(version_space(space, (("x", 0), ("x", 0))), (0,))
        self.assertEqual(version_space(space, (("x", 0), ("x", 1))), ())
        self.assertTrue(is_realizable(space, (0,)))
        self.assertFalse(is_identified(space, (0,), (("x", 0), ("x", 1))))

    def test_empty_family(self):
        space = HypothesisSpace(("x",), ())
        self.assertEqual(version_space(space, ()), ())
        self.assertFalse(is_identified(space, (0,), ()))
        self.assertIsNone(minimum_teaching_set(space, (0,)))

    def test_empty_domain(self):
        populated = HypothesisSpace((), ((), ()))
        self.assertEqual(minimum_teaching_set(populated, ()), ())
        self.assertEqual(version_space(populated, ()), (0, 1))
        self.assertTrue(is_identified(populated, (), ()))
        empty = HypothesisSpace((), ())
        self.assertFalse(is_realizable(empty, ()))
        self.assertIsNone(minimum_teaching_set(empty, ()))
        self.assertFalse(is_identified(empty, (), ()))

    def test_full_domain_not_only_observed_performance(self):
        space = HypothesisSpace(("seen", "unseen"), ((0, 0), (0, 1)))
        observations = (("seen", 0),)
        self.assertEqual(version_space(space, observations), (0, 1))
        self.assertFalse(is_identified(space, (0, 0), observations))

    def test_exhaustive_three_point_families_targets(self):
        domain = ("x0", "x1", "x2")
        all_rows = tuple(product((0, 1), repeat=3))
        choices = subsets((0, 1, 2))
        cases = 0
        for rows in subsets(all_rows):
            space = HypothesisSpace(domain, rows)
            for target in all_rows:
                answer = minimum_teaching_set(space, target)
                if target not in rows:
                    self.assertIsNone(answer)
                else:
                    sufficient = []
                    for indices in choices:
                        # Independent difference-set oracle, not API filtering.
                        if all(row == target or any(row[i] != target[i] for i in indices)
                               for row in rows):
                            sufficient.append(indices)
                    best = min(sufficient, key=lambda indices: (len(indices), indices))
                    expected = tuple((domain[i], target[i]) for i in best)
                    self.assertEqual(answer, expected)
                    self.assertTrue(is_identified(space, target, answer))
                cases += 1
        self.assertEqual(cases, 2048)

    def test_exhaustive_two_point_observation_patterns(self):
        all_rows = tuple(product((0, 1), repeat=2))
        domain = ("x0", "x1")
        cases = 0
        for rows in subsets(all_rows):
            space = HypothesisSpace(domain, rows)
            for labels in product(((), (0,), (1,), (0, 1)), repeat=2):
                observations = tuple((domain[i], value) for i, group in enumerate(labels) for value in group)
                expected = tuple(j for j, row in enumerate(rows)
                                 if all(all(row[i] == bit for bit in labels[i]) for i in range(2)))
                self.assertEqual(version_space(space, observations), expected)
                cases += 1
        self.assertEqual(cases, 256)


class ValidationTests(unittest.TestCase):
    def test_lesson_container_and_scalar_types(self):
        for action in (
            lambda: Lesson(True, frozenset(), frozenset("a")),
            lambda: Lesson("A", set(), frozenset("a")),
            lambda: Lesson("A", frozenset(), {"a"}),
            lambda: Lesson("A", frozenset({1}), frozenset("a")),
            lambda: Lesson("A", frozenset(), frozenset({True})),
        ):
            with self.assertRaises(TypeError):
                action()
        for action in (
            lambda: Lesson(" ", frozenset(), frozenset("a")),
            lambda: Lesson("A", frozenset(), frozenset()),
            lambda: Lesson("A", frozenset({""}), frozenset("a")),
        ):
            with self.assertRaises(ValueError):
                action()

    def test_problem_structure(self):
        lesson = Lesson("A", frozenset(), frozenset("a"))
        for action in (
            lambda: PlanningProblem(set("a"), frozenset(), frozenset(), ()),
            lambda: PlanningProblem(frozenset("a"), (), frozenset(), ()),
            lambda: PlanningProblem(frozenset("a"), frozenset(), set(), ()),
            lambda: PlanningProblem(frozenset("a"), frozenset(), frozenset(), [lesson]),
            lambda: PlanningProblem(frozenset("a"), frozenset(), frozenset(), (True,)),
        ):
            with self.assertRaises(TypeError):
                action()
        for action in (
            lambda: PlanningProblem(frozenset("a"), frozenset("b"), frozenset(), ()),
            lambda: PlanningProblem(frozenset("a"), frozenset(), frozenset("b"), ()),
            lambda: PlanningProblem(frozenset("a"), frozenset(), frozenset(), (lesson, lesson)),
            lambda: PlanningProblem(frozenset(), frozenset(), frozenset(), (lesson,)),
            lambda: PlanningProblem(frozenset("a"), frozenset(), frozenset(),
                                    (Lesson("B", frozenset("b"), frozenset("a")),)),
        ):
            with self.assertRaises(ValueError):
                action()

    def test_public_planner_inputs(self):
        for function in (closure, shortest_plan, greedy_plan):
            with self.assertRaises(TypeError):
                function(None)
        with self.assertRaises(TypeError):
            replay(None, ())
        for path in ([], "A", (True,)):
            with self.assertRaises(TypeError):
                replay(planning_example(), path)
        with self.assertRaises(ValueError):
            replay(planning_example(), ("",))

    def test_hypothesis_structure(self):
        for action in (
            lambda: HypothesisSpace(["x"], ((0,),)),
            lambda: HypothesisSpace((True,), ((0,),)),
            lambda: HypothesisSpace(("x",), [(0,)]),
            lambda: HypothesisSpace(("x",), ([0],)),
            lambda: HypothesisSpace(("x",), ((True,),)),
            lambda: HypothesisSpace(("x",), ((0.0,),)),
        ):
            with self.assertRaises(TypeError):
                action()
        for action in (
            lambda: HypothesisSpace(("x", "x"), ((0, 0),)),
            lambda: HypothesisSpace(("",), ((0,),)),
            lambda: HypothesisSpace(("x",), ((),)),
            lambda: HypothesisSpace(("x",), ((2,),)),
        ):
            with self.assertRaises(ValueError):
                action()

    def test_target_validation(self):
        space = HypothesisSpace(("x",), ((0,),))
        functions = (is_realizable, minimum_teaching_set,
                     lambda space, target: is_identified(space, target, ()))
        for function in functions:
            with self.assertRaises(TypeError):
                function(None, (0,))
            for target in ([0], (True,), (0.0,)):
                with self.assertRaises(TypeError):
                    function(space, target)
            for target in ((), (0, 1), (2,)):
                with self.assertRaises(ValueError):
                    function(space, target)

    def test_observation_validation(self):
        space = HypothesisSpace(("x",), ((0,),))
        with self.assertRaises(TypeError):
            version_space(None, ())
        for observations in ([], (["x", 0],), ((True, 0),), (("x", True),), (("x", 0.0),)):
            with self.assertRaises(TypeError):
                version_space(space, observations)
        for observations in (((),), (("x",),), (("x", 0, 1),), (("y", 0),), (("x", 2),), (("", 0),)):
            with self.assertRaises(ValueError):
                version_space(space, observations)
        with self.assertRaises(TypeError):
            is_identified(space, (0,), (("x", True),))

    def test_subclasses_not_coerced(self):
        class IntChild(int):
            pass
        class StrChild(str):
            pass
        class TupleChild(tuple):
            pass
        class FrozenChild(frozenset):
            pass
        for action in (
            lambda: HypothesisSpace(("x",), ((IntChild(0),),)),
            lambda: HypothesisSpace((StrChild("x"),), ((0,),)),
            lambda: HypothesisSpace(TupleChild(("x",)), ((0,),)),
            lambda: Lesson("A", FrozenChild(), frozenset("a")),
        ):
            with self.assertRaises(TypeError):
                action()


if __name__ == "__main__":
    unittest.main()
