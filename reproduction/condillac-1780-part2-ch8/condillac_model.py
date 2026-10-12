"""Finite teaching model inspired by La Logique II.VIII; not a historical algorithm.

Only the Python standard library is used. Public validators use explicit exceptions,
not assertions. User callbacks are sampled once into immutable finite tables.
"""
from dataclasses import dataclass
from functools import lru_cache
from typing import Callable

Value = int | str | tuple
World = tuple


def _value(value):
    if type(value) in (int, str):
        return
    if type(value) is tuple:
        for member in value:
            _value(member)
        return
    raise TypeError('values must be exact int, str, or recursively tuples thereof')


def _name(value):
    if type(value) is not str or not value.strip():
        raise ValueError('name must be a nonempty string')


def _distinct(values):
    """Stable first-occurrence order, independent of set/hash iteration order."""
    return tuple(dict.fromkeys(values))


@dataclass(frozen=True)
class Universe:
    fields: tuple[str, ...]
    worlds: tuple[World, ...]

    def __post_init__(self):
        if type(self.fields) is not tuple or not self.fields:
            raise TypeError('fields must be a nonempty tuple')
        for field in self.fields:
            _name(field)
        if len(set(self.fields)) != len(self.fields):
            raise ValueError('duplicate field')
        if type(self.worlds) is not tuple:
            raise TypeError('worlds must be a tuple')
        for world in self.worlds:
            if type(world) is not tuple or len(world) != len(self.fields):
                raise ValueError('world must be a tuple with exactly one value per field')
            for value in world:
                if type(value) not in (int, str):
                    raise TypeError('world coordinates must be exact int or str; bool is forbidden')
        if len(set(self.worlds)) != len(self.worlds):
            raise ValueError('duplicate world')


@dataclass(frozen=True)
class Table:
    universe: Universe
    name: str
    values: tuple[Value, ...]

    def __post_init__(self):
        if type(self.universe) is not Universe:
            raise TypeError('universe must be Universe')
        _name(self.name)
        if type(self.values) is not tuple or len(self.values) != len(self.universe.worlds):
            raise ValueError('table must give exactly one value per universe world')
        for value in self.values:
            _value(value)


@dataclass(frozen=True)
class Constraint:
    universe: Universe
    name: str
    mask: tuple[bool, ...]

    def __post_init__(self):
        if type(self.universe) is not Universe:
            raise TypeError('universe must be Universe')
        _name(self.name)
        if type(self.mask) is not tuple or len(self.mask) != len(self.universe.worlds):
            raise ValueError('constraint must give exactly one boolean per universe world')
        if any(type(value) is not bool for value in self.mask):
            raise TypeError('constraint outputs must be exact bool')


def table(universe: Universe, name: str, function: Callable) -> Table:
    if type(universe) is not Universe:
        raise TypeError('universe must be Universe')
    if not callable(function):
        raise TypeError('function must be callable')
    return Table(universe, name, tuple(function(w) for w in universe.worlds))


def constraint(universe: Universe, name: str, predicate: Callable) -> Constraint:
    if type(universe) is not Universe:
        raise TypeError('universe must be Universe')
    if not callable(predicate):
        raise TypeError('predicate must be callable')
    return Constraint(universe, name, tuple(predicate(w) for w in universe.worlds))


@dataclass(frozen=True)
class Problem:
    universe: Universe
    target: Table
    constraints: tuple[Constraint, ...] = ()

    def __post_init__(self):
        if type(self.universe) is not Universe or type(self.target) is not Table:
            raise TypeError('problem requires Universe and Table')
        if self.target.universe != self.universe:
            raise ValueError('target belongs to a different universe')
        if type(self.constraints) is not tuple:
            raise TypeError('constraints must be a tuple')
        for item in self.constraints:
            if type(item) is not Constraint:
                raise TypeError('each constraint must be Constraint')
            if item.universe != self.universe:
                raise ValueError('constraint belongs to a different universe')


def _problem(problem):
    if type(problem) is not Problem:
        raise TypeError('problem must be Problem')


def candidates(problem: Problem) -> tuple[int, ...]:
    _problem(problem)
    return tuple(i for i in range(len(problem.universe.worlds))
                 if all(item.mask[i] for item in problem.constraints))


@dataclass(frozen=True)
class Analysis:
    status: str
    candidates: tuple[int, ...]
    answers: tuple[Value, ...]

    @property
    def answer(self):
        if self.status != 'identified':
            raise ValueError('a unique answer is unavailable')
        return self.answers[0]


def analyze(problem: Problem) -> Analysis:
    indices = candidates(problem)
    answers = _distinct(problem.target.values[i] for i in indices)
    status = 'inconsistent' if not indices else ('identified' if len(answers) == 1 else 'underdetermined')
    return Analysis(status, indices, answers)


def add_evidence(problem: Problem, evidence: Constraint) -> Problem:
    _problem(problem)
    return Problem(problem.universe, problem.target, problem.constraints + (evidence,))


@dataclass(frozen=True)
class RewriteReport:
    worlds_preserved: bool
    answers_preserved: bool
    nonvacuous: bool
    lost_worlds: tuple[int, ...]
    gained_worlds: tuple[int, ...]


def compare_rewrite(before: Problem, after: Problem) -> RewriteReport:
    _problem(before)
    _problem(after)
    if before.universe != after.universe or before.target.values != after.target.values:
        raise ValueError('rewrites require the same ordered universe and target mapping')
    left, right = analyze(before), analyze(after)
    lost = tuple(i for i in left.candidates if i not in right.candidates)
    gained = tuple(i for i in right.candidates if i not in left.candidates)
    return RewriteReport(not lost and not gained, set(left.answers) == set(right.answers),
                         bool(left.candidates) and bool(right.candidates), lost, gained)


def translation_chain(problems: tuple[Problem, ...], preservation='worlds') -> tuple[RewriteReport, ...]:
    if type(problems) is not tuple or len(problems) < 2:
        raise ValueError('a chain needs a tuple of at least two problems')
    if preservation not in ('worlds', 'answers'):
        raise ValueError('preservation must be worlds or answers')
    reports = tuple(compare_rewrite(a, b) for a, b in zip(problems, problems[1:]))
    if any(not (r.worlds_preserved if preservation == 'worlds' else r.answers_preserved) for r in reports):
        raise ValueError('a translation step violates requested preservation')
    return reports


@dataclass(frozen=True)
class Compression:
    sufficient: bool
    vacuous: bool
    decoder: tuple[tuple[Value, Value], ...]
    witness: tuple[int, int] | None

    def decode(self, code: Value) -> Value:
        _value(code)
        if not self.sufficient:
            raise ValueError('compression is insufficient')
        for key, answer in self.decoder:
            if code == key:
                return answer
        raise KeyError('code is outside the candidate-supported decoder domain')


def compression(problem: Problem, encoding: Table) -> Compression:
    _problem(problem)
    if type(encoding) is not Table or encoding.universe != problem.universe:
        raise ValueError('encoding must be a Table on the same universe')
    indices = candidates(problem)
    first = {}
    for i in indices:
        code = encoding.values[i]
        if code in first and problem.target.values[first[code]] != problem.target.values[i]:
            return Compression(False, False, (), (first[code], i))
        first.setdefault(code, i)
    decoder = tuple((code, problem.target.values[i]) for code, i in first.items())
    return Compression(True, not indices, decoder, None)


@dataclass(frozen=True)
class DecisionNode:
    status: str
    candidates: tuple[int, ...]
    depth: int | None
    answer: Value | None = None
    question_index: int | None = None
    branches: tuple[tuple[Value, 'DecisionNode'], ...] = ()
    witness: tuple[int, int] | None = None


def _questions(problem, questions):
    _problem(problem)
    if type(questions) is not tuple:
        raise TypeError('questions must be a tuple')
    for question in questions:
        if type(question) is not Table or question.universe != problem.universe:
            raise ValueError('each question must be a Table on the same universe')
    if len({q.name for q in questions}) != len(questions):
        raise ValueError('question names must be distinct')


def minimax_tree(problem: Problem, questions: tuple[Table, ...]) -> DecisionNode:
    """Optimal worst-case count of exact, noiseless, unit-cost observations.

    Tie-break: earliest question in the supplied tuple. Impossible means impossible
    using these question tables, not impossible under every conceivable inquiry.
    """
    _questions(problem, questions)
    target = problem.target.values

    @lru_cache(None)
    def solve(indices, remaining):
        if not indices:
            return DecisionNode('inconsistent', indices, None)
        answers = _distinct(target[i] for i in indices)
        if len(answers) == 1:
            return DecisionNode('identified', indices, 0, answer=answers[0])
        first = {}
        for i in indices:
            signature = tuple(questions[q].values[i] for q in remaining)
            if signature in first and target[first[signature]] != target[i]:
                return DecisionNode('impossible', indices, None, witness=(first[signature], i))
            first.setdefault(signature, i)
        best = None
        for q in remaining:
            groups = {}
            for i in indices:
                groups.setdefault(questions[q].values[i], []).append(i)
            if len(groups) == 1:
                continue
            next_remaining = tuple(r for r in remaining if r != q)
            branches = tuple((value, solve(tuple(group), next_remaining)) for value, group in groups.items())
            if any(child.depth is None for _, child in branches):
                continue
            depth = 1 + max(child.depth for _, child in branches)
            if best is None or depth < best.depth:
                best = DecisionNode('measurement', indices, depth, question_index=q, branches=branches)
        if best is None:
            raise RuntimeError('internal error: distinguishable targets must admit a finite tree')
        return best

    return solve(candidates(problem), tuple(range(len(questions))))


def follow_tree(problem: Problem, questions: tuple[Table, ...], node: DecisionNode, world_index: int):
    """Replay a generated tree on one candidate world; return answer and question names.

    This is a replay helper, not a validator for arbitrary hand-constructed nodes.
    """
    _questions(problem, questions)
    if type(world_index) is not int:
        raise TypeError('world_index must be an exact int')
    if world_index not in candidates(problem):
        raise ValueError('world_index is not a candidate')
    path = []
    while node.status == 'measurement':
        question = questions[node.question_index]
        path.append(question.name)
        response = question.values[world_index]
        matches = [child for value, child in node.branches if value == response]
        if len(matches) != 1:
            raise ValueError('tree has no unique branch for this observation')
        node = matches[0]
    if node.status != 'identified':
        raise ValueError('tree cannot identify the answer')
    return node.answer, tuple(path)
