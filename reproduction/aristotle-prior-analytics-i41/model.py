"""Finite teaching model for I.41, not a reconstruction of unique ancient semantics."""
from dataclasses import dataclass
from itertools import combinations


def _set(value, label):
    if isinstance(value, (str, bytes)):
        raise TypeError(label + ' must be an iterable of nonnegative integers')
    try:
        values = tuple(value)
    except TypeError as exc:
        raise TypeError(label + ' must be iterable') from exc
    if any(type(x) is not int or x < 0 for x in values):
        raise TypeError(label + ' elements must be nonnegative integers, excluding bool')
    return frozenset(values)


@dataclass(frozen=True)
class Model:
    domain: frozenset
    a: frozenset
    b: frozenset
    family: tuple = ()

    def __post_init__(self):
        d, a, b = (_set(getattr(self, key), key) for key in ('domain', 'a', 'b'))
        if not d:
            raise ValueError('domain must be nonempty')
        if not a <= d or not b <= d:
            raise ValueError('a and b must be subsets of domain')
        if isinstance(self.family, (str, bytes)):
            raise TypeError('family must be an iterable of subsets')
        try:
            family = tuple(_set(x, 'family member') for x in self.family)
        except TypeError as exc:
            raise TypeError('family must contain iterable subsets of domain') from exc
        if any(not x <= d for x in family):
            raise ValueError('family member outside domain')
        for key, value in (('domain', d), ('a', a), ('b', b), ('family', family)):
            object.__setattr__(self, key, value)

    def strong(self):
        """Every B is A."""
        return self.b <= self.a

    def weak(self):
        """For each explicitly supplied X, X subset B implies X subset A."""
        return all(not x <= self.b or x <= self.a for x in self.family)

    def eligible_union(self):
        return frozenset().union(*(x for x in self.family if x <= self.b))

    def covers_b(self):
        return self.eligible_union() == self.b

    def _c(self, c):
        c = _set(c, 'c')
        if not c <= self.domain:
            raise ValueError('c must be a subset of domain')
        return c

    def all_chain(self, c):
        """Require B subset A and C subset B, then report C subset A."""
        c = self._c(c)
        if not self.strong() or not c <= self.b:
            raise ValueError('all-chain premises are not satisfied')
        return c <= self.a

    def some_chain_witness(self, c):
        """Return the same C/B witness, under B subset A; not a universal conclusion."""
        c = self._c(c)
        common = c & self.b
        if not self.strong() or not common:
            raise ValueError('some-chain premises are not satisfied')
        witness = min(common)
        if witness not in self.a:
            raise RuntimeError('internal witness preservation failure')
        return witness


def powerset(domain):
    """Deterministic tuple of subsets, accepting only the model's domain labels."""
    values = sorted(_set(domain, 'powerset input'))
    return tuple(frozenset(xs) for size in range(len(values) + 1)
                 for xs in combinations(values, size))


def families(subsets):
    """Internal enumeration of all families from an already validated subset tuple."""
    for size in range(len(subsets) + 1):
        yield from combinations(subsets, size)
