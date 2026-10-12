"""Two finite modern teaching models, not historical algorithms or psychology.

Python 3.10+; standard library only. All public inputs use exact immutable
container/scalar types. Validation does not rely on removable assert statements.
"""

from collections import deque
from dataclasses import dataclass
from itertools import combinations


SkillSet = frozenset[str]
Row = tuple[int, ...]
Observation = tuple[str, int]


def _name(value: object, field: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{field} must be a string")
    if not value or not value.strip():
        raise ValueError(f"{field} must not be blank")


def _skills(value: object, field: str) -> None:
    if type(value) is not frozenset:
        raise TypeError(f"{field} must be a frozenset")
    for item in value:
        _name(item, field + " member")


def _tuple(value: object, field: str) -> None:
    if type(value) is not tuple:
        raise TypeError(f"{field} must be a tuple")


def _bit(value: object, field: str) -> None:
    if type(value) is not int:  # bool is deliberately not an accepted integer.
        raise TypeError(f"{field} must be an exact int, not bool")
    if value not in (0, 1):
        raise ValueError(f"{field} must be 0 or 1")


def _row(value: object, width: int, field: str) -> None:
    _tuple(value, field)
    if len(value) != width:
        raise ValueError(f"{field} length must equal domain length")
    for bit in value:
        _bit(bit, field + " label")


@dataclass(frozen=True)
class Lesson:
    name: str
    prerequisites: SkillSet
    gains: SkillSet

    def __post_init__(self) -> None:
        _name(self.name, "lesson name")
        _skills(self.prerequisites, "prerequisites")
        _skills(self.gains, "gains")
        if not self.gains:
            raise ValueError("each lesson must have nonempty gains")


@dataclass(frozen=True)
class PlanningProblem:
    skills: SkillSet
    initial: SkillSet
    goal: SkillSet
    lessons: tuple[Lesson, ...]

    def __post_init__(self) -> None:
        for field in ("skills", "initial", "goal"):
            _skills(getattr(self, field), field)
        if not self.initial <= self.skills or not self.goal <= self.skills:
            raise ValueError("initial and goal must be subsets of skills")
        _tuple(self.lessons, "lessons")
        names = set()
        for lesson in self.lessons:
            if type(lesson) is not Lesson:
                raise TypeError("lessons must contain exact Lesson instances")
            if lesson.name in names:
                raise ValueError("lesson names must be unique")
            names.add(lesson.name)
            if not lesson.prerequisites <= self.skills:
                raise ValueError("lesson prerequisites must be within skills")
            if not lesson.gains <= self.skills:
                raise ValueError("lesson gains must be within skills")


def _problem(problem: object) -> None:
    if type(problem) is not PlanningProblem:
        raise TypeError("problem must be a PlanningProblem")


def closure(problem: PlanningProblem) -> SkillSet:
    """Least prerequisite-closed skill superset of the initial skills."""
    _problem(problem)
    state = problem.initial
    while True:
        expanded = state
        for lesson in problem.lessons:
            if lesson.prerequisites <= state:
                expanded = expanded | lesson.gains
        if expanded == state:
            return state
        state = expanded


def shortest_plan(problem: PlanningProblem) -> tuple[str, ...] | None:
    """Minimum lesson count; equal-length ties follow supplied lesson order.

    Only executable, strictly growing transitions enter the finite search.
    None means exact unreachability in this supplied deterministic model.
    """
    _problem(problem)
    if problem.goal <= problem.initial:
        return ()
    if not problem.goal <= closure(problem):
        return None
    queue = deque([(problem.initial, ())])
    visited = {problem.initial}
    while queue:
        state, path = queue.popleft()
        for lesson in problem.lessons:
            if not lesson.prerequisites <= state:
                continue
            after = state | lesson.gains
            if after == state or after in visited:
                continue
            next_path = path + (lesson.name,)
            if problem.goal <= after:
                return next_path
            visited.add(after)
            queue.append((after, next_path))
    # The closure equivalence implies this branch is unreachable for valid input.
    raise RuntimeError("closure and finite search disagree")


def replay(problem: PlanningProblem, names: tuple[str, ...]) -> SkillSet:
    """Execute a legal strictly growing path; it need not finish the goal."""
    _problem(problem)
    _tuple(names, "names")
    by_name = {lesson.name: lesson for lesson in problem.lessons}
    state = problem.initial
    for name in names:
        _name(name, "path name")
        if name not in by_name:
            raise ValueError("unknown lesson name")
        lesson = by_name[name]
        if not lesson.prerequisites <= state:
            raise ValueError("unmet lesson prerequisites")
        after = state | lesson.gains
        if after == state:
            raise ValueError("redundant transition")
        state = after
    return state


def greedy_plan(problem: PlanningProblem) -> tuple[str, ...] | None:
    """Illustrative heuristic: largest fresh gain, then lexical lesson name.

    This deterministic heuristic is not a claim about historical instruction.
    It can use more lessons than shortest_plan.
    """
    _problem(problem)
    state = problem.initial
    path = ()
    while not problem.goal <= state:
        available = tuple(
            lesson for lesson in problem.lessons
            if lesson.prerequisites <= state and lesson.gains - state
        )
        if not available:
            return None
        chosen = min(available, key=lambda item: (-len(item.gains - state), item.name))
        state = state | chosen.gains
        path += (chosen.name,)
    return path


@dataclass(frozen=True)
class HypothesisSpace:
    domain: tuple[str, ...]
    rows: tuple[Row, ...]

    def __post_init__(self) -> None:
        _tuple(self.domain, "domain")
        for point in self.domain:
            _name(point, "domain point")
        if len(set(self.domain)) != len(self.domain):
            raise ValueError("domain points must be unique")
        _tuple(self.rows, "rows")
        for row in self.rows:
            _row(row, len(self.domain), "hypothesis row")


def _space(space: object) -> None:
    if type(space) is not HypothesisSpace:
        raise TypeError("space must be a HypothesisSpace")


def _observations(space: HypothesisSpace, observations: object) -> None:
    _tuple(observations, "observations")
    for observation in observations:
        _tuple(observation, "observation")
        if len(observation) != 2:
            raise ValueError("each observation must have two entries")
        point, label = observation
        _name(point, "observed point")
        if point not in space.domain:
            raise ValueError("observed point must belong to domain")
        _bit(label, "observed label")


def version_space(
    space: HypothesisSpace, observations: tuple[Observation, ...]
) -> tuple[int, ...]:
    """Indices of all rows consistent with all observations, possibly empty.

    Repeated observations are legal; conflicting labels at one point give ().
    Duplicate truth-table rows remain separate indices.
    """
    _space(space)
    _observations(space, observations)
    positions = {point: index for index, point in enumerate(space.domain)}
    return tuple(
        index for index, row in enumerate(space.rows)
        if all(row[positions[point]] == label for point, label in observations)
    )


def is_realizable(space: HypothesisSpace, target: Row) -> bool:
    _space(space)
    _row(target, len(space.domain), "target")
    return target in space.rows


def is_identified(
    space: HypothesisSpace, target: Row, observations: tuple[Observation, ...]
) -> bool:
    """Nonempty survivors all equal target over the complete finite domain."""
    _space(space)
    _row(target, len(space.domain), "target")
    survivors = version_space(space, observations)
    return bool(survivors) and all(space.rows[index] == target for index in survivors)


def minimum_teaching_set(
    space: HypothesisSpace, target: Row
) -> tuple[Observation, ...] | None:
    """Smallest nonadaptive target-labeled subset identifying the target row.

    None: target is absent. (): realizable and zero examples suffice.
    Equal-cardinality ties follow lexicographic domain-index combinations.
    Duplicate target indices are equivalent; this does not identify an index.
    """
    _space(space)
    _row(target, len(space.domain), "target")
    if not is_realizable(space, target):
        return None
    for size in range(len(space.domain) + 1):
        for indices in combinations(range(len(space.domain)), size):
            examples = tuple((space.domain[index], target[index]) for index in indices)
            if is_identified(space, target, examples):
                return examples
    raise RuntimeError("a realizable target must be identified by its full table")
