"""Explicit teaching semantics, not a reconstruction of all Aristotelian modality.
Predicate precedes subject: eval('D', 'a', 'A', 'B') means every B is A.
Only the Python standard library is required.
"""
from collections.abc import Mapping
from types import MappingProxyType

TERMS = ('A', 'B', 'C')
MODES = ('D', 'N', 'C', 'P', 'Box')
FORMS = ('a', 'e', 'i', 'o')


def _integer_set(value, label):
    if not isinstance(value, (set, frozenset, list, tuple)):
        raise TypeError(label + ' must be a set, frozenset, list or tuple')
    if any(type(x) is not int for x in value):
        raise TypeError(label + ' members must be integers (not booleans)')
    return frozenset(value)


class Model:
    """Finite nonempty constant domain and nonempty list/tuple of worlds.

    Empty term extensions are allowed. All worlds are considered accessible,
    including the designated actual world. Inputs are copied and frozen.
    N/P fix the subject extension at actual; Box reevaluates the subject at w.
    For particular N/P, one actual subject is respectively necessary/possible.
    Box(i/o), by contrast, permits the witness to change across worlds.
    """
    __slots__ = ('_domain', '_worlds', '_actual')

    def __init__(self, domain, worlds, actual=0):
        domain = _integer_set(domain, 'domain')
        if not domain:
            raise ValueError('domain must be nonempty')
        if not isinstance(worlds, (list, tuple)):
            raise TypeError('worlds must be a list or tuple')
        if not worlds:
            raise ValueError('worlds must be nonempty')
        if type(actual) is not int:
            raise TypeError('actual must be an integer (not boolean)')
        if actual < 0 or actual >= len(worlds):
            raise ValueError('actual world index out of range')
        frozen = []
        for w in worlds:
            if not isinstance(w, Mapping):
                raise TypeError('each world must be a mapping')
            if set(w) != set(TERMS):
                raise ValueError('each world must have exactly A, B, C')
            copied = {t: _integer_set(w[t], 'extension') for t in TERMS}
            if any(not s <= domain for s in copied.values()):
                raise ValueError('extension outside domain')
            frozen.append(MappingProxyType(copied))
        self._domain, self._worlds, self._actual = domain, tuple(frozen), actual

    @property
    def domain(self):
        return self._domain

    @property
    def worlds(self):
        return self._worlds

    @property
    def actual(self):
        return self._actual

    def eval(self, mode, form, predicate, subject):
        for value, permitted, label in ((mode, MODES, 'mode'),
                                       (form, FORMS, 'form'),
                                       (predicate, TERMS, 'predicate'),
                                       (subject, TERMS, 'subject')):
            if type(value) is not str:
                raise TypeError(label + ' must be a string')
            if value not in permitted:
                raise ValueError('unknown ' + label)
        universal = form in ('a', 'e')
        positive = form in ('a', 'i')
        quantify = all if universal else any
        subjects = self._worlds[self._actual][subject]
        if mode == 'D':
            extension = self._worlds[self._actual][predicate]
            return quantify((x in extension) == positive for x in subjects)
        if mode == 'Box':
            return all(quantify((x in w[predicate]) == positive
                                for x in w[subject]) for w in self._worlds)
        if mode == 'C':
            # Two-sided contingency: both qualities have the same condition.
            return quantify(any(x in w[predicate] for w in self._worlds)
                            and any(x not in w[predicate] for w in self._worlds)
                            for x in subjects)
        modal = all if mode == 'N' else any
        return quantify(modal((x in w[predicate]) == positive
                              for w in self._worlds) for x in subjects)

    def as_dict(self):
        return {'domain': sorted(self.domain), 'actual': self.actual,
                'worlds': [{t: sorted(w[t]) for t in TERMS} for w in self.worlds]}
