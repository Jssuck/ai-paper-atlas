"""Small deterministic examples; no external service or data."""

from model import (
    HypothesisSpace, Lesson, PlanningProblem, closure, greedy_plan,
    is_identified, is_realizable, minimum_teaching_set, replay, shortest_plan,
    version_space,
)


def planning_example():
    return PlanningProblem(
        frozenset("abcguvw"), frozenset(), frozenset("g"),
        (
            Lesson("A", frozenset(), frozenset("a")),
            Lesson("B", frozenset("a"), frozenset("b")),
            Lesson("C", frozenset("b"), frozenset("g")),
            Lesson("D", frozenset(), frozenset("uvw")),
            Lesson("E", frozenset(), frozenset("c")),
            Lesson("F", frozenset("c"), frozenset("g")),
        ),
    )


def teaching_example():
    return HypothesisSpace(
        ("x0", "x1", "x2", "x3"),
        ((0, 0, 0, 0), (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 1)),
    )


def main():
    problem = planning_example()
    print("MODEL 1: fixed deterministic prerequisite transitions")
    print("closure:", ",".join(sorted(closure(problem))))
    for label, path in (("BFS", shortest_plan(problem)), ("greedy", greedy_plan(problem))):
        print(f"{label}: {path}; length={len(path)}")
        for end in range(len(path) + 1):
            state = ",".join(sorted(replay(problem, path[:end]))) or "empty"
            print(f"  after {end}: {state}")
    cycle = PlanningProblem(
        frozenset("ab"), frozenset(), frozenset("a"),
        (Lesson("P", frozenset("b"), frozenset("a")),
         Lesson("Q", frozenset("a"), frozenset("b"))),
    )
    print("cycle closure:", tuple(sorted(closure(cycle))))
    print("cycle shortest plan:", shortest_plan(cycle))
    print("MODEL 2: noiseless full-domain truth-table identification")
    space = teaching_example()
    target = (0, 0, 0, 0)
    examples = minimum_teaching_set(space, target)
    print("realizable:", is_realizable(space, target))
    print("minimum teaching set:", examples)
    for end in range(len(examples) + 1):
        observed = examples[:end]
        print(f"  after {end}: rows={version_space(space, observed)}; "
              f"identified={is_identified(space, target, observed)}")
    alternative = (("x0", 0), ("x1", 0), ("x3", 0))
    print("alternative size-3 set identified:", is_identified(space, target, alternative))
    contradictions = (("x0", 0), ("x0", 1))
    print("conflicting observations:", version_space(space, contradictions))
    print("empty survivors identified:", is_identified(space, target, contradictions))
    absent = (1, 1, 1, 1)
    print("absent target realizable:", is_realizable(space, absent))
    print("absent target teaching set:", minimum_teaching_set(space, absent))
    duplicates = HypothesisSpace(("x",), ((0,), (0,), (1,)))
    duplicate_examples = minimum_teaching_set(duplicates, (0,))
    print("duplicate equivalent survivors:", version_space(duplicates, duplicate_examples))
    print("duplicate behavior identified:", is_identified(duplicates, (0,), duplicate_examples))
    empty_domain = HypothesisSpace((), ((), ()))
    print("empty-domain teaching set:", minimum_teaching_set(empty_domain, ()))
    print("Scope: synthetic finite behavior only; no difficulty, confidence, or self-discovery measured.")


if __name__ == "__main__":
    main()
