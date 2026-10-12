"""Independent bounded audit. Python 3.10+, standard library only.

Run ``python3 audit_model.py`` (also -O/-OO), or use ``--record`` to
record all three modes under logs/audit-*. The oracles below do not call
model functions, import the author's test module, or use its fixtures.
"""

from dataclasses import FrozenInstanceError
from itertools import product
import unittest

from model import (
    HypothesisSpace, Lesson, PlanningProblem, closure, greedy_plan,
    is_identified, is_realizable, minimum_teaching_set, replay, shortest_plan,
    version_space,
)


COUNTS = {}


def state_skills(mask, names):
    return frozenset(name for index, name in enumerate(names) if mask & (1 << index))


def closed_intersection(initial, rules, width):
    """Intersect every closed superset, rather than iterating rule applications."""
    result = (1 << width) - 1
    for state in range(1 << width):
        if state & initial != initial:
            continue
        if all(state & pre != pre or state & gain == gain for pre, gain in rules):
            result &= state
    return result


def dag_paths(initial, rules, width):
    """Topological DP over numeric bit masks; no queue or lesson permutations.

    A strict union transition increases the numeric mask, so one ascending
    traversal suffices. Keep the shortest then input-index-lexical path to
    each state. Later goal selection is independent of this calculation.
    """
    paths = {initial: ()}
    for state in range(1 << width):
        if state not in paths:
            continue
        for index, (pre, gain) in enumerate(rules):
            after = state | gain
            if state & pre != pre or after == state:
                continue
            candidate = paths[state] + (index,)
            old = paths.get(after)
            if old is None or (len(candidate), candidate) < (len(old), old):
                paths[after] = candidate
    return paths


def projection_masks(rows, target, width):
    """Build equivalence classes of target projections using integer bitsets.

    Entry m contains row indices agreeing with target on the point mask m.
    A one-bit recurrence, in numeric subset order, avoids API observations,
    the implementation's combinations(), and the author's difference sets.
    """
    matches = []
    for point in range(width):
        bits = 0
        for index, row in enumerate(rows):
            if (row >> point) & 1 == (target >> point) & 1:
                bits |= 1 << index
        matches.append(bits)
    projected = [(1 << len(rows)) - 1] * (1 << width)
    for mask in range(1, 1 << width):
        low = mask & -mask
        projected[mask] = projected[mask ^ low] & matches[low.bit_length() - 1]
    return projected


def minimum_projection(rows, target, width):
    target_indices = sum(1 << index for index, row in enumerate(rows) if row == target)
    if not target_indices:
        return None
    projected = projection_masks(rows, target, width)
    possible = [tuple(point for point in range(width) if mask & (1 << point))
                for mask, survivors in enumerate(projected) if survivors == target_indices]
    return min(possible, key=lambda points: (len(points), points))


def observation_oracle(rows, observations):
    """Two masks encode all required zero/one labels; overlap is contradiction."""
    zeros = ones = 0
    for point, label in observations:
        if label:
            ones |= 1 << point
        else:
            zeros |= 1 << point
    if zeros & ones:
        return ()
    return tuple(index for index, row in enumerate(rows)
                 if row & ones == ones and row & zeros == 0)


class IndependentAudit(unittest.TestCase):
    def test_three_skill_ordered_rule_systems(self):
        names = ("p", "q", "r")
        skills = tuple(state_skills(mask, names) for mask in range(8))
        catalogue = tuple(product(range(8), range(1, 8)))
        cases = systems = 0
        for count in range(3):
            for rules in product(catalogue, repeat=count):
                systems += 1
                # Deliberately reverse alphabetical names relative to input order.
                lessons = tuple(Lesson(("z", "a")[index], skills[pre], skills[gain])
                                for index, (pre, gain) in enumerate(rules))
                for initial in range(8):
                    expected_closure = closed_intersection(initial, rules, 3)
                    paths = dag_paths(initial, rules, 3)
                    for goal in range(8):
                        problem = PlanningProblem(skills[7], skills[initial], skills[goal], lessons)
                        candidates = [path for state, path in paths.items() if state & goal == goal]
                        indices = min(candidates, key=lambda path: (len(path), path)) if candidates else None
                        expected = None if indices is None else tuple(lessons[i].name for i in indices)
                        actual = shortest_plan(problem)
                        self.assertEqual(closure(problem), skills[expected_closure], (rules, initial))
                        self.assertEqual(actual, expected, (rules, initial, goal))
                        self.assertEqual(actual is not None, expected_closure & goal == goal)
                        if actual is not None:
                            self.assertTrue(problem.goal <= replay(problem, actual))
                            self.assertLessEqual(len(actual), 3 - initial.bit_count())
                        heuristic = greedy_plan(problem)
                        self.assertEqual(heuristic is not None, actual is not None)
                        if heuristic is not None:
                            self.assertTrue(problem.goal <= replay(problem, heuristic))
                        cases += 1
        self.assertEqual(systems, 3193)
        self.assertEqual(cases, 204352)
        COUNTS["planning_systems"] = systems
        COUNTS["planning_initial_goal_cases"] = cases

    def test_duplicate_inclusive_hypothesis_families(self):
        families = target_cases = observation_cases = identification_cases = 0
        for width in range(4):
            domain = tuple(f"point-{i}" for i in range(width))
            row_bits = tuple(range(1 << width))
            row_values = tuple(tuple((row >> i) & 1 for i in range(width)) for row in row_bits)
            atoms = tuple(product(range(width), (0, 1)))
            observation_sequences = tuple(sequence for count in range(3)
                                          for sequence in product(atoms, repeat=count))
            for count in range(4):
                for rows in product(row_bits, repeat=count):
                    families += 1
                    space = HypothesisSpace(domain, tuple(row_values[row] for row in rows))
                    for target in row_bits:
                        indices = minimum_projection(rows, target, width)
                        expected = (None if indices is None else
                                    tuple((domain[i], (target >> i) & 1) for i in indices))
                        self.assertEqual(minimum_teaching_set(space, row_values[target]), expected,
                                         (width, rows, target))
                        self.assertEqual(is_realizable(space, row_values[target]), target in rows)
                        target_cases += 1
                    for observations in observation_sequences:
                        supplied = tuple((domain[i], bit) for i, bit in observations)
                        expected = observation_oracle(rows, observations)
                        self.assertEqual(version_space(space, supplied), expected,
                                         (width, rows, observations))
                        # Every target is checked, including unrealizable targets and
                        # nonempty survivor families whose rows disagree off-sample.
                        for target in row_bits:
                            identified = bool(expected) and {rows[i] for i in expected} == {target}
                            self.assertEqual(is_identified(space, row_values[target], supplied), identified)
                            identification_cases += 1
                        observation_cases += 1
        self.assertEqual((families, target_cases, observation_cases, identification_cases),
                         (689, 5054, 27049, 208594))
        COUNTS.update(hypothesis_families=families, target_cases=target_cases,
                      observation_sequences=observation_cases, identification_cases=identification_cases)

    def test_deeper_ties_and_longer_dependencies(self):
        # Independent six-skill diamond: two prefixes merge, followed by two
        # equal-length ways to reach the goal. Supplied order governs both ties.
        skills = frozenset("abcdef")
        lessons = (
            Lesson("z-start", frozenset(), frozenset("a")),
            Lesson("a-start", frozenset(), frozenset("b")),
            Lesson("z-join", frozenset("a"), frozenset("bc")),
            Lesson("a-join", frozenset("b"), frozenset("ac")),
            Lesson("z-finish", frozenset("c"), frozenset("df")),
            Lesson("a-finish", frozenset("c"), frozenset("ef")),
        )
        problem = PlanningProblem(skills, frozenset(), frozenset("f"), lessons)
        self.assertEqual(shortest_plan(problem), ("z-start", "z-join", "z-finish"))
        self.assertEqual(closure(problem), skills)
        self.assertEqual(replay(problem, ("z-start",)), frozenset("a"))
        for path in (("z-start", "z-start"), ("z-join",), ("unknown",)):
            with self.assertRaises(ValueError):
                replay(problem, path)
        chain = PlanningProblem(skills, frozenset(), frozenset("f"), tuple(
            Lesson(f"chain-{i}", frozenset() if i == 0 else frozenset("abcdef"[i - 1]),
                   frozenset("abcdef"[i])) for i in range(6)))
        self.assertEqual(shortest_plan(chain), tuple(f"chain-{i}" for i in range(6)))
        empty = PlanningProblem(frozenset(), frozenset(), frozenset(), ())
        self.assertEqual((closure(empty), shortest_plan(empty), greedy_plan(empty), replay(empty, ())),
                         (frozenset(), (), (), frozenset()))

    def test_strict_validation_and_immutability(self):
        class IntChild(int):
            pass
        class StrChild(str):
            pass
        class TupleChild(tuple):
            pass
        class FrozenChild(frozenset):
            pass
        class LessonChild(Lesson):
            pass
        class ProblemChild(PlanningProblem):
            pass
        class SpaceChild(HypothesisSpace):
            pass

        fs = frozenset
        valid = PlanningProblem(fs("x"), fs(), fs("x"), (Lesson("L", fs(), fs("x")),))
        space = HypothesisSpace(("x",), ((0,), (1,)))
        invalid = []
        def bad(exception, label, action):
            invalid.append((exception, label, action))

        for value in (True, 0.0, IntChild(0), "0", None):
            bad(TypeError, f"row label {value!r}", lambda v=value: HypothesisSpace(("x",), ((v,),)))
            bad(TypeError, f"observation label {value!r}", lambda v=value: version_space(space, (("x", v),)))
            for fn in (is_realizable, minimum_teaching_set,
                       lambda s, t: is_identified(s, t, ())):
                bad(TypeError, "target scalar exact type", lambda f=fn, v=value: f(space, (v,)))
        for value in (-1, 2, 7):
            bad(ValueError, "invalid row bit", lambda v=value: HypothesisSpace(("x",), ((v,),)))
            bad(ValueError, "invalid observation bit", lambda v=value: version_space(space, (("x", v),)))
            for fn in (is_realizable, minimum_teaching_set,
                       lambda s, t: is_identified(s, t, ())):
                bad(ValueError, "invalid target bit", lambda f=fn, v=value: f(space, (v,)))
        for value in (None, True, 9, StrChild("x")):
            bad(TypeError, "lesson name exact type", lambda v=value: Lesson(v, fs(), fs("x")))
            bad(TypeError, "domain name exact type", lambda v=value: HypothesisSpace((v,), ((0,),)))
            bad(TypeError, "skill name exact type", lambda v=value: Lesson("L", fs((v,)), fs("x")))
            bad(TypeError, "path name exact type", lambda v=value: replay(valid, (v,)))
            bad(TypeError, "observation name exact type", lambda v=value: version_space(space, ((v, 0),)))
        for value in ("", " \t\n"):
            bad(ValueError, "blank lesson name", lambda v=value: Lesson(v, fs(), fs("x")))
            bad(ValueError, "blank domain name", lambda v=value: HypothesisSpace((v,), ((0,),)))
            bad(ValueError, "blank skill", lambda v=value: Lesson("L", fs((v,)), fs("x")))
            bad(ValueError, "blank path name", lambda v=value: replay(valid, (v,)))
            bad(ValueError, "blank observed point", lambda v=value: version_space(space, ((v, 0),)))
        for value in (set(), (), [], FrozenChild()):
            bad(TypeError, "prerequisites container", lambda v=value: Lesson("L", v, fs("x")))
            bad(TypeError, "gains container", lambda v=value: Lesson("L", fs(), v))
            for field in range(3):
                def invalid_problem(v=value, position=field):
                    values = [fs("x"), fs(), fs()]
                    values[position] = v
                    return PlanningProblem(*values, ())
                bad(TypeError, "problem set container", invalid_problem)
        for value in ([], "x", TupleChild()):
            bad(TypeError, "domain tuple", lambda v=value: HypothesisSpace(v, ()))
            bad(TypeError, "rows tuple", lambda v=value: HypothesisSpace((), v))
            bad(TypeError, "lessons tuple", lambda v=value: PlanningProblem(fs(), fs(), fs(), v))
            bad(TypeError, "path tuple", lambda v=value: replay(valid, v))
            bad(TypeError, "observations tuple", lambda v=value: version_space(space, v))
        for value in ([0], TupleChild((0,))):
            bad(TypeError, "row tuple", lambda v=value: HypothesisSpace(("x",), (v,)))
            for fn in (is_realizable, minimum_teaching_set, lambda s, t: is_identified(s, t, ())):
                bad(TypeError, "target tuple", lambda f=fn, v=value: f(space, v))
        for value in ((["x", 0],), (TupleChild(("x", 0)),)):
            bad(TypeError, "observation tuple", lambda v=value: version_space(space, v))
        for target in ((), (0, 1)):
            bad(ValueError, "row width", lambda v=target: HypothesisSpace(("x",), (v,)))
            for fn in (is_realizable, minimum_teaching_set, lambda s, t: is_identified(s, t, ())):
                bad(ValueError, "target width", lambda f=fn, v=target: f(space, v))
        for observations in (((),), (("x",),), (("x", 0, 1),), (("missing", 0),)):
            bad(ValueError, "observation shape or domain", lambda v=observations: version_space(space, v))
        bad(ValueError, "empty domain observation", lambda: version_space(HypothesisSpace((), ((),)), (("x", 0),)))
        bad(ValueError, "empty lesson gain", lambda: Lesson("L", fs(), fs()))
        bad(ValueError, "duplicate domain", lambda: HypothesisSpace(("x", "x"), ((0, 0),)))
        bad(ValueError, "duplicate lesson name", lambda: PlanningProblem(fs("x"), fs(), fs(), (valid.lessons[0],) * 2))
        bad(ValueError, "initial outside universe", lambda: PlanningProblem(fs(), fs("x"), fs(), ()))
        bad(ValueError, "goal outside universe", lambda: PlanningProblem(fs(), fs(), fs("x"), ()))
        bad(ValueError, "gain outside universe", lambda: PlanningProblem(fs(), fs(), fs(), valid.lessons))
        bad(ValueError, "precondition outside universe", lambda: PlanningProblem(fs("x"), fs(), fs(),
                                                       (Lesson("L", fs("y"), fs("x")),)))
        for value in (None, LessonChild("L", fs(), fs("x"))):
            bad(TypeError, "exact lesson instance", lambda v=value: PlanningProblem(fs("x"), fs(), fs(), (v,)))
        for value in (None, ProblemChild(fs(), fs(), fs(), ())):
            for fn in (closure, shortest_plan, greedy_plan, lambda p: replay(p, ())):
                bad(TypeError, "exact problem instance", lambda f=fn, v=value: f(v))
        for value in (None, SpaceChild(("x",), ((0,),))):
            for fn in (lambda s: version_space(s, ()), lambda s: is_realizable(s, (0,)),
                       lambda s: is_identified(s, (0,), ()), lambda s: minimum_teaching_set(s, (0,))):
                bad(TypeError, "exact space instance", lambda f=fn, v=value: f(v))
        for exception, label, action in invalid:
            with self.subTest(label=label):
                with self.assertRaises(exception):
                    action()
        for instance, name in ((valid, "initial"), (valid.lessons[0], "name"), (space, "rows")):
            with self.assertRaises(FrozenInstanceError):
                setattr(instance, name, None)
        # Exact, nonblank strings need not be trimmed, ASCII, or identifier-like.
        unusual = HypothesisSpace((" 教学 ",), ((0,), (0,)))
        self.assertTrue(is_identified(unusual, (0,), ()))
        COUNTS["invalid_input_cases"] = len(invalid)
        COUNTS["frozen_assignment_checks"] = 3


def record_runs():
    """Capture real subprocess output; fail if any run fails or source changes."""
    from datetime import datetime, timezone
    import hashlib
    import json
    import os
    from pathlib import Path
    import platform
    import shlex
    import subprocess
    import sys

    root = Path(__file__).resolve().parent
    logs = root / "logs"
    logs.mkdir(exist_ok=True)
    names = ("model.py", "demo.py", "test_model.py", "run_checks.py", "audit_model.py")
    def digests():
        return {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names}
    evidence = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_executable": sys.executable,
        "python_version": sys.version,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "dependencies": "Python standard library only",
        "environment_overrides": {"PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1"},
        "source_sha256_before": digests(),
        "runs": [],
    }
    env = dict(os.environ, **evidence["environment_overrides"])
    for label, flags in (("normal", []), ("optimized", ["-O"]), ("double-optimized", ["-OO"])):
        command = [sys.executable, *flags, "audit_model.py"]
        start = datetime.now(timezone.utc)
        result = subprocess.run(command, cwd=root, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, encoding="utf-8", check=False)
        end = datetime.now(timezone.utc)
        relative_log = f"logs/audit-{label}.log"
        text = (f"$ {shlex.join(command)}\nstarted_at_utc: {start.isoformat()}\n"
                + result.stdout + f"exit_code: {result.returncode}\nfinished_at_utc: {end.isoformat()}\n")
        (root / relative_log).write_text(text, encoding="utf-8")
        evidence["runs"].append({"mode": label, "command": command, "exit_code": result.returncode,
                                 "log": relative_log, "elapsed_seconds": (end - start).total_seconds()})
        print(f"{label}: exit {result.returncode}; {relative_log}", flush=True)
    evidence["source_sha256_after"] = digests()
    evidence["source_unchanged"] = evidence["source_sha256_before"] == evidence["source_sha256_after"]
    evidence["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    evidence["passed"] = evidence["source_unchanged"] and all(run["exit_code"] == 0 for run in evidence["runs"])
    (logs / "audit-environment.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if evidence["passed"] else 1


if __name__ == "__main__":
    import json
    import sys
    if sys.argv[1:] == ["--record"]:
        raise SystemExit(record_runs())
    print(f"Python: {sys.version.split()[0]}; optimization level: {sys.flags.optimize}", flush=True)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(IndependentAudit)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print("completed_case_counts: " + json.dumps(COUNTS, sort_keys=True), flush=True)
    raise SystemExit(0 if result.wasSuccessful() else 1)
