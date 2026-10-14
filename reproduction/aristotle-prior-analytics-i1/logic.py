"""Small modern extensional teaching model; not Aristotle's own algorithm.

Python 3.10+, standard library only. Public inputs are immutable and checked
without assert statements, including when Python runs with -O or -OO.
"""

from dataclasses import dataclass


class ValidationError(ValueError):
    """Malformed or undeclared input, not a logically invalid argument."""


def _name(value: object, label: str) -> None:
    if type(value) is not str or not value or value != value.strip():
        raise ValidationError(f"{label} must be a nonempty, trimmed string")


def _terms(value: object) -> None:
    if type(value) is not tuple or not 1 <= len(value) <= 3:
        raise ValidationError("terms must be a tuple of one to three names")
    for term in value:
        _name(term, "term")
    if len(set(value)) != len(value):
        raise ValidationError("term names must be unique")


def _revalidate(value: object, cls: type, label: str) -> None:
    """Check boundary objects even if frozen fields were bypassed in-process.

    Frozen dataclasses discourage accidental changes; they are not a security
    sandbox. This also rejects incomplete instances made with object.__new__.
    """
    if type(value) is not cls:
        raise ValidationError(f"{label} must be a {cls.__name__}")
    try:
        cls.__post_init__(value)
    except AttributeError as error:
        raise ValidationError(f"{label} is missing a required field") from error


@dataclass(frozen=True, slots=True)
class Prop:
    kind: str
    subject: str
    predicate: str

    def __post_init__(self) -> None:
        if type(self.kind) is not str or self.kind not in ("A", "E", "I", "O"):
            raise ValidationError("kind must be exactly A, E, I, or O")
        _name(self.subject, "subject")
        _name(self.predicate, "predicate")


@dataclass(frozen=True, slots=True)
class Language:
    terms: tuple[str, ...]
    required_nonempty: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        _terms(self.terms)
        if type(self.required_nonempty) is not frozenset:
            raise ValidationError("required_nonempty must be a frozenset")
        for term in self.required_nonempty:
            _name(term, "required nonempty term")
        if not self.required_nonempty.issubset(self.terms):
            raise ValidationError("required_nonempty contains an undeclared term")


@dataclass(frozen=True, slots=True)
class Model:
    terms: tuple[str, ...]
    support: tuple[int, ...]

    def __post_init__(self) -> None:
        _terms(self.terms)
        if type(self.support) is not tuple or not self.support:
            raise ValidationError("support must be a nonempty tuple")
        limit = 1 << len(self.terms)
        for truth_type in self.support:
            if type(truth_type) is not int or not 0 <= truth_type < limit:
                raise ValidationError("truth types must be in-range integers, not bools")
        if tuple(sorted(set(self.support))) != self.support:
            raise ValidationError("support must be sorted and contain no duplicates")

    def members(self, term: str) -> tuple[int, ...]:
        """Return representative truth types belonging to a named term."""
        _revalidate(self, Model, "model")
        _name(term, "term")
        if term not in self.terms:
            raise ValidationError(f"undeclared term: {term}")
        bit = 1 << self.terms.index(term)
        return tuple(t for t in self.support if t & bit)


@dataclass(frozen=True, slots=True)
class Entailment:
    holds: bool
    satisfying_premise_models: int
    admissible_models: int
    countermodel: Model | None


def validate_problem(language: Language, premises: tuple[Prop, ...], conclusion: Prop) -> None:
    """Validate the public input contract; no implicit term declarations."""
    _revalidate(language, Language, "language")
    if type(premises) is not tuple:
        raise ValidationError("premises must be a tuple")
    for prop in premises + (conclusion,):
        _revalidate(prop, Prop, "each premise and conclusion")
        if prop.subject not in language.terms or prop.predicate not in language.terms:
            raise ValidationError("proposition contains an undeclared term")


def _truth(prop: Prop, model: Model) -> bool:
    subject_bit = 1 << model.terms.index(prop.subject)
    predicate_bit = 1 << model.terms.index(prop.predicate)
    intersection = any(t & subject_bit and t & predicate_bit for t in model.support)
    outside = any(t & subject_bit and not t & predicate_bit for t in model.support)
    if prop.kind == "A":
        return not outside
    if prop.kind == "E":
        return not intersection
    if prop.kind == "I":
        return intersection
    return outside


def evaluate(prop: Prop, model: Model) -> bool:
    _revalidate(model, Model, "model")
    validate_problem(Language(model.terms), (), prop)
    return _truth(prop, model)


def is_admissible(language: Language, model: Model) -> bool:
    _revalidate(language, Language, "language")
    _revalidate(model, Model, "model")
    if model.terms != language.terms:
        raise ValidationError("model term order must match language term order")
    return all(model.members(term) for term in language.required_nonempty)


def enumerate_models(language: Language) -> tuple[Model, ...]:
    """Enumerate all nonempty truth-type supports, in deterministic mask order."""
    _revalidate(language, Language, "language")
    type_count = 1 << len(language.terms)
    result = []
    for support_mask in range(1, 1 << type_count):
        support = tuple(t for t in range(type_count) if support_mask & (1 << t))
        model = Model(language.terms, support)
        if is_admissible(language, model):
            result.append(model)
    return tuple(result)


def entails(language: Language, premises: tuple[Prop, ...], conclusion: Prop) -> Entailment:
    """Classical consequence, including vacuity from inconsistent premises.

    Counts are supports, not all labeled universes or actual historical cases.
    An empty tuple of premises is allowed. A returned countermodel makes every
    declared premise true and the conclusion false under the given policy.
    """
    validate_problem(language, premises, conclusion)
    models = enumerate_models(language)
    satisfying = 0
    countermodel = None
    for model in models:
        if all(_truth(p, model) for p in premises):
            satisfying += 1
            if not _truth(conclusion, model) and countermodel is None:
                countermodel = model
    return Entailment(countermodel is None, satisfying, len(models), countermodel)
