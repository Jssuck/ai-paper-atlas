"""Finite teaching models; not Condillac's algorithms or a psychology experiment."""
from dataclasses import dataclass
from typing import Iterable


def _items(values, label):
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{label} must be a finite collection, not text")
    try:
        return tuple(values)
    except TypeError as exc:
        raise ValueError(f"{label} must be iterable") from exc


def _name(value, label):
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a nonempty string")
    return value


def _names(values, label, allow_empty=True):
    result = _items(values, label)
    for value in result:
        _name(value, label)
    if len(set(result)) != len(result) or (not allow_empty and not result):
        raise ValueError(f"{label} must contain distinct names and meet nonempty requirement")
    return result


def _pair(value, label):
    pair = _items(value, label)
    if len(pair) != 2:
        raise ValueError(f"{label} must have two fields")
    return pair


@dataclass(frozen=True)
class HypothesisSpace:
    points: tuple[str, ...]
    rows: tuple[tuple[str, tuple[str, ...]], ...]

    def __post_init__(self):
        points = _names(self.points, "points", False)
        rows = []
        for raw in _items(self.rows, "rows"):
            key, raw_values = _pair(raw, "hypothesis row")
            _name(key, "hypothesis name")
            values = _items(raw_values, "predictions")
            if len(values) != len(points):
                raise ValueError("each hypothesis must predict every point")
            for value in values:
                _name(value, "prediction")
            rows.append((key, values))
        _names((key for key, _ in rows), "hypothesis names", False)
        object.__setattr__(self, "points", points)
        object.__setattr__(self, "rows", tuple(rows))

    def observations(self, observations):
        result = []
        for raw in _items(observations, "observations"):
            point, outcome = _pair(raw, "observation")
            _name(point, "observed point")
            _name(outcome, "observed outcome")
            if point not in self.points:
                raise ValueError("observation refers to unknown point")
            result.append((point, outcome))
        return tuple(result)

    def candidates(self, observations, max_errors=0):
        if type(max_errors) is not int or max_errors < 0:
            raise ValueError("max_errors must be a nonnegative integer, not bool")
        data = self.observations(observations)
        positions = {point: i for i, point in enumerate(self.points)}
        return frozenset(key for key, row in self.rows
                         if sum(row[positions[x]] != y for x, y in data) <= max_errors)

    def distinguishes(self, observed_points):
        points = _names(observed_points, "observed points")
        if not set(points) <= set(self.points):
            raise ValueError("unknown observed point")
        indices = tuple(self.points.index(point) for point in points)
        signatures = {tuple(row[i] for i in indices) for _, row in self.rows}
        return len(signatures) == len(self.rows)


@dataclass(frozen=True)
class Rule:
    name: str
    premises: frozenset[str]
    conclusion: str

    def __post_init__(self):
        _name(self.name, "rule name")
        _name(self.conclusion, "rule conclusion")
        premises = _items(self.premises, "rule premises")
        for item in premises:
            _name(item, "premise")
        object.__setattr__(self, "premises", frozenset(premises))


@dataclass(frozen=True)
class Derivation:
    rule: str
    premises: tuple[str, ...]
    conclusion: str


@dataclass(frozen=True)
class ClosureResult:
    seeds: frozenset[str]
    steps: tuple[Derivation, ...]
    atoms: frozenset[str]


@dataclass(frozen=True)
class HornSystem:
    atoms: tuple[str, ...]
    rules: tuple[Rule, ...]

    def __post_init__(self):
        atoms = _names(self.atoms, "atoms")
        rules = _items(self.rules, "rules")
        if any(not isinstance(rule, Rule) for rule in rules):
            raise ValueError("every rule must be a Rule")
        _names((rule.name for rule in rules), "rule names")
        universe = frozenset(atoms)
        if any(not rule.premises <= universe or rule.conclusion not in universe for rule in rules):
            raise ValueError("rule contains unknown atom")
        object.__setattr__(self, "atoms", atoms)
        object.__setattr__(self, "rules", rules)

    def subset(self, atoms):
        items = _items(atoms, "atom subset")
        for item in items:
            _name(item, "atom")
        result = frozenset(items)
        if not result <= frozenset(self.atoms):
            raise ValueError("unknown atom")
        return result

    def closed(self, atoms):
        known = self.subset(atoms)
        return all(not rule.premises <= known or rule.conclusion in known for rule in self.rules)

    def close(self, seeds):
        initial = self.subset(seeds)
        known = set(initial)
        steps = []
        while True:
            changed = False
            for rule in self.rules:
                if rule.premises <= known and rule.conclusion not in known:
                    steps.append(Derivation(rule.name, tuple(sorted(rule.premises)), rule.conclusion))
                    known.add(rule.conclusion)
                    changed = True
            if not changed:
                return ClosureResult(initial, tuple(steps), frozenset(known))

    def verify_trace(self, result, seeds):
        """Check complete rule derivation, tied to supplied seeds; no factual warranty."""
        expected = self.subset(seeds)
        if not isinstance(result, ClosureResult) or result.seeds != expected:
            raise ValueError("trace must match the supplied seeds")
        reported = self.subset(result.atoms)
        known = set(expected)
        by_name = {rule.name: rule for rule in self.rules}
        for step in _items(result.steps, "trace steps"):
            if not isinstance(step, Derivation) or not isinstance(step.rule, str):
                raise ValueError("invalid derivation record")
            rule = by_name.get(step.rule)
            if rule is None:
                raise ValueError("unknown provenance rule")
            if step.premises != tuple(sorted(rule.premises)) or step.conclusion != rule.conclusion:
                raise ValueError("provenance does not match named rule")
            if not rule.premises <= known or rule.conclusion in known:
                raise ValueError("premises missing or repeated conclusion")
            known.add(rule.conclusion)
        if frozenset(known) != reported or not self.closed(reported):
            raise ValueError("trace has an unrecorded atom or is not a complete closure")
        return True


@dataclass(frozen=True)
class Vocabulary:
    """A finite bijection from meanings to distinct words, represented by pairs."""
    entries: tuple[tuple[str, str], ...]

    def __post_init__(self):
        entries = tuple(_pair(pair, "vocabulary entry") for pair in _items(self.entries, "entries"))
        _names((meaning for meaning, _ in entries), "meanings")
        _names((word for _, word in entries), "words")
        object.__setattr__(self, "entries", entries)

    @property
    def meanings(self):
        return frozenset(meaning for meaning, _ in self.entries)

    @property
    def words(self):
        return frozenset(word for _, word in self.entries)

    def encode(self, meanings):
        mapping = dict(self.entries)
        return translate_atoms(meanings, mapping)

    def decode(self, words):
        mapping = {word: meaning for meaning, word in self.entries}
        return translate_atoms(words, mapping)


def _dictionary(mapping):
    if not hasattr(mapping, "items"):
        raise ValueError("dictionary must be a mapping")
    pairs = tuple(mapping.items())
    for source, target in pairs:
        _name(source, "dictionary source")
        _name(target, "dictionary target")
    return dict(pairs)


def translate_atoms(atoms, dictionary):
    mapping = _dictionary(dictionary)
    values = _items(atoms, "atoms to translate")
    for value in values:
        _name(value, "atom to translate")
        if value not in mapping:
            raise ValueError("translation is undefined for an atom")
    return frozenset(mapping[value] for value in values)


def inverse_dictionary(dictionary):
    mapping = _dictionary(dictionary)
    if len(set(mapping.values())) != len(mapping):
        raise ValueError("dictionary is not injective")
    return {target: source for source, target in mapping.items()}


def aligned_dictionary(source, target):
    if source.meanings != target.meanings:
        raise ValueError("vocabularies must cover the same meanings")
    target_encoding = dict(target.entries)
    return {word: target_encoding[meaning] for meaning, word in source.entries}


def translation_preserves(source, target, dictionary):
    mapping = _dictionary(dictionary)
    if source.meanings != target.meanings or set(mapping) != source.words:
        return False
    if not set(mapping.values()) <= target.words:
        return False
    target_meaning = {word: meaning for meaning, word in target.entries}
    return all(target_meaning[mapping[word]] == meaning for meaning, word in source.entries)


def rename_rule(rule, dictionary):
    if not isinstance(rule, Rule):
        raise ValueError("expected a Rule")
    conclusion = translate_atoms((rule.conclusion,), dictionary)
    return Rule(rule.name, translate_atoms(rule.premises, dictionary), next(iter(conclusion)))


def task_exact(worlds, labels, task_values):
    """True iff a label always determines the task answer on the specified worlds."""
    domain = _names(worlds, "worlds", False)
    label_map, task_map = _dictionary(labels), _dictionary(task_values)
    if set(label_map) != set(domain) or set(task_map) != set(domain):
        raise ValueError("both maps must cover exactly the world set")
    answers = {}
    for world in domain:
        label, answer = label_map[world], task_map[world]
        if label in answers and answers[label] != answer:
            return False
        answers[label] = answer
    return True
