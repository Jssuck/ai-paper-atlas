"""An original finite teaching model, not a reconstruction of Condillac's algorithm.

Truth is used only by truth_errors; fitting uses observation counts and r.
All validation is explicit and remains active under Python -O and -OO.
"""
from dataclasses import dataclass, replace


def _names(value: tuple[str, ...], name: str, *, empty: bool = False) -> None:
    if type(value) is not tuple:
        raise ValueError(f"{name} must be a tuple")
    if not empty and not value:
        raise ValueError(f"{name} must be nonempty")
    if any(type(x) is not str or not x for x in value):
        raise ValueError(f"{name} must contain nonempty strings")
    if len(set(value)) != len(value):
        raise ValueError(f"{name} must have distinct entries")


def _map(value: tuple[str, ...], size: int, codomain: tuple[str, ...], name: str) -> None:
    if type(value) is not tuple or len(value) != size:
        raise ValueError(f"{name} must be a tuple of length {size}")
    if any(type(x) is not str or x not in codomain for x in value):
        raise ValueError(f"{name} must take values in its declared codomain")


@dataclass(frozen=True)
class Problem:
    """Tuples enumerate U, L, A; r, h, f follow those orders respectively.

    counts[i][j] is the nonnegative integer number of observations assigning
    answers[j] to objects[i]. It is not assumed to agree with f.
    """
    objects: tuple[str, ...]
    labels: tuple[str, ...]
    answers: tuple[str, ...]
    r: tuple[str, ...]
    h: tuple[str, ...]
    f: tuple[str, ...]
    counts: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        _names(self.objects, "objects", empty=True)
        _names(self.labels, "labels")
        _names(self.answers, "answers")
        _map(self.r, len(self.objects), self.labels, "r")
        _map(self.h, len(self.labels), self.answers, "h")
        _map(self.f, len(self.objects), self.answers, "f")
        if type(self.counts) is not tuple or len(self.counts) != len(self.objects):
            raise ValueError("counts must have one tuple row per object")
        for row in self.counts:
            if type(row) is not tuple or len(row) != len(self.answers):
                raise ValueError("each counts row must have one entry per answer")
            if any(type(n) is not int or n < 0 for n in row):
                raise ValueError("counts must be nonnegative integers (not booleans)")


def predictions(problem: Problem) -> tuple[str, ...]:
    decoder = dict(zip(problem.labels, problem.h))
    return tuple(decoder[label] for label in problem.r)


def empirical_loss(problem: Problem) -> int:
    """Weighted number of disagreements with the observed answers, not truth."""
    predicted = predictions(problem)
    return sum(n for prediction, row in zip(predicted, problem.counts)
               for answer, n in zip(problem.answers, row) if answer != prediction)


def truth_errors(problem: Problem) -> int:
    """Unweighted number of objects in the finite universe predicted incorrectly."""
    return sum(prediction != truth for prediction, truth in zip(predictions(problem), problem.f))


def label_counts(problem: Problem) -> tuple[tuple[int, ...], ...]:
    totals = {label: [0] * len(problem.answers) for label in problem.labels}
    for label, row in zip(problem.r, problem.counts):
        for index, n in enumerate(row):
            totals[label][index] += n
    return tuple(tuple(totals[label]) for label in problem.labels)


def fit(problem: Problem) -> Problem:
    """Fit each label independently; positive ties use the declared answer order.

    Labels whose total count is zero retain their previous decoder value.
    """
    fitted = []
    for old, row in zip(problem.h, label_counts(problem)):
        if sum(row) == 0:
            fitted.append(old)
        else:
            fitted.append(problem.answers[row.index(max(row))])
    return replace(problem, h=tuple(fitted))


def minimum_empirical_loss(problem: Problem) -> int:
    """Exact minimum over every deterministic decoder on this representation."""
    return sum(sum(row) - max(row) for row in label_counts(problem))


def rename(problem: Problem, new_labels: tuple[str, ...]) -> Problem:
    """Bijectively rename labels in enumeration order, jointly transporting r/h."""
    _names(new_labels, "new_labels")
    if len(new_labels) != len(problem.labels):
        raise ValueError("a bijective renaming needs one new name per old label")
    translation = dict(zip(problem.labels, new_labels))
    return replace(problem, labels=new_labels,
                   r=tuple(translation[label] for label in problem.r))


def refine(problem: Problem, new_labels: tuple[str, ...],
           new_r: tuple[str, ...], parents: tuple[str, ...]) -> Problem:
    """Refine via a declared q: new_labels -> old labels, with q(new_r) = old r.

    The initial new decoder is transported: h_new = h_old composed with q.
    Consequently refinement by this function alone preserves every prediction.
    A separate fit may improve empirical loss; truth need not improve.
    """
    _names(new_labels, "new_labels")
    _map(new_r, len(problem.objects), new_labels, "new_r")
    _map(parents, len(new_labels), problem.labels, "parents")
    q = dict(zip(new_labels, parents))
    if any(q[new] != old for new, old in zip(new_r, problem.r)):
        raise ValueError("not a refinement: q(new_r(u)) must equal r(u) for every object")
    old_decoder = dict(zip(problem.labels, problem.h))
    return replace(problem, labels=new_labels, r=new_r,
                   h=tuple(old_decoder[q[label]] for label in new_labels))
