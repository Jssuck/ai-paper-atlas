"""Bounded teaching calculus for Prior Analytics I.27; Python standard library.
No ancient unique semantics, probability, existential inference or full consequence engine.
"""
from dataclasses import dataclass
from collections import deque


def _name(x):
    if type(x) is not str or not x or x.strip() != x:
        raise ValueError('term must be a nonempty stripped string')
    return x


def _sequence(x, description):
    if type(x) not in (list, tuple):
        raise ValueError(description + ' must be a list or tuple')
    return x


@dataclass(frozen=True)
class Inclusion:
    path: tuple


@dataclass(frozen=True)
class Exclusion:
    left_path: tuple
    right_path: tuple
    source_pair: tuple


class KnowledgeBase:
    """Input edges are asserted universal premises, not observed individual samples.

    Inclusion (a,b) means a subset b; exclusion (a,b) means disjoint.
    Presence of a term does not assert its nonemptiness. Output is rule closure,
    not full semantic closure when an empty term could imply new inclusions.
    """
    def __init__(self, terms, inclusions=(), exclusions=()):
        seq = _sequence(terms, 'terms')
        names = tuple(_name(x) for x in seq)
        if not names or len(set(names)) != len(names):
            raise ValueError('terms must be nonempty and unique')
        self.terms = names
        self._terms = frozenset(names)
        self.inclusions = self._edges(inclusions)
        self.exclusions = self._edges(exclusions)

    def _edges(self, items):
        out = set()
        for edge in _sequence(items, 'edges'):
            if type(edge) not in (list, tuple) or len(edge) != 2:
                raise ValueError('edge must contain two known terms')
            a, b = edge
            _name(a); _name(b)
            if a not in self._terms or b not in self._terms:
                raise ValueError('unknown term')
            out.add((a, b))
        return frozenset(out)

    def _known(self, name):
        _name(name)
        if name not in self._terms:
            raise ValueError('unknown term')

    def inclusion(self, a, b):
        """Shortest asserted-edge path, with reflexivity allowed; None is unknown."""
        self._known(a); self._known(b)
        queue = deque([(a,)])
        seen = {a}
        while queue:
            path = queue.popleft()
            if path[-1] == b:
                return Inclusion(path)
            for nxt in sorted(y for x, y in self.inclusions if x == path[-1]):
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(path + (nxt,))
        return None

    def exclusion(self, a, b):
        """Find a source disjoint pair containing both requested subclasses."""
        self._known(a); self._known(b)
        for x, y in sorted(self.exclusions):
            for left, right in ((x, y), (y, x)):
                p = self.inclusion(a, left)
                q = self.inclusion(b, right)
                if p is not None and q is not None:
                    return Exclusion(p.path, q.path, (x, y))
        return None

    def catalog(self, x):
        self._known(x)
        return {
            'sup': tuple(y for y in self.terms if self.inclusion(x, y) is not None),
            'sub': tuple(y for y in self.terms if self.inclusion(y, x) is not None),
            'excl': tuple(y for y in self.terms if self.exclusion(x, y) is not None),
        }

    def verify(self, a, b, certificate):
        """Verify against asserted edges, not against the search output.

        Malformed certificates return False; invalid requested terms raise ValueError.
        """
        self._known(a); self._known(b)
        def path_ok(path, start):
            return (type(path) is tuple and len(path) > 0 and path[0] == start
                    and all(type(t) is str and t in self._terms for t in path)
                    and all((x, y) in self.inclusions for x, y in zip(path, path[1:])))
        if type(certificate) is Inclusion:
            p = certificate.path
            return path_ok(p, a) and p[-1] == b
        if type(certificate) is Exclusion:
            p, q, edge = certificate.left_path, certificate.right_path, certificate.source_pair
            if not path_ok(p, a) or not path_ok(q, b):
                return False
            if type(edge) is not tuple or len(edge) != 2 or not all(type(t) is str for t in edge):
                return False
            return edge in self.exclusions and (p[-1], q[-1]) in (edge, edge[::-1])
        return False


def model_holds(kb, extension):
    """Finite interpretation sanity check. Names exact, finite sets of hashables."""
    if type(kb) is not KnowledgeBase or type(extension) is not dict or set(extension) != set(kb.terms):
        raise ValueError('interpretation must assign every term exactly once')
    if any(type(v) not in (set, frozenset) for v in extension.values()):
        raise ValueError('extensions must be sets or frozensets')
    return (all(extension[a] <= extension[b] for a, b in kb.inclusions)
            and all(extension[a].isdisjoint(extension[b]) for a, b in kb.exclusions))
