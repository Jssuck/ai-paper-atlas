"""Original educational finite reconstruction, not an original 1880 program.

Python standard library only. Complements are always relative to an explicit
finite universe. Modern notation is used; see SOURCE_LEDGER.md for scope.
"""
from dataclasses import dataclass
from itertools import product
from typing import Callable, Iterable, Mapping


def powerset(items: Iterable):
    """Yield subsets deterministically in bit-mask order."""
    seq = tuple(items)
    for mask in range(1 << len(seq)):
        yield frozenset(x for i, x in enumerate(seq) if mask & (1 << i))


def categorical(subject: frozenset, predicate: frozenset) -> dict[str, bool]:
    """Peirce's p23 convention: A/E have no existential import; I/O do."""
    return {"A": subject <= predicate, "E": not bool(subject & predicate),
            "I": bool(subject & predicate), "O": bool(subject - predicate)}


def assignments(names: Iterable[str]):
    names = tuple(names)
    for row in product((False, True), repeat=len(names)):
        yield dict(zip(names, row))


def shannon(f: Callable[[Mapping[str, bool]], bool], name: str,
            env: Mapping[str, bool]) -> bool:
    """p36 eq26, modern one-point evaluation of Boolean class expansion."""
    one, zero = dict(env, **{name: True}), dict(env, **{name: False})
    return (f(one) and env[name]) or (f(zero) and not env[name])


# A signed literal (name, polarity); a clause is a disjunction, a CNF conjunction.
Literal = tuple[str, bool]
Clause = frozenset[Literal]
CNF = frozenset[Clause]


def clause(*literals: str) -> Clause:
    """Example: clause('a', '~b'). Empty clause denotes false."""
    if any(not x or x == '~' or x.startswith('~~') for x in literals):
        raise ValueError('Use nonempty variable names with at most one leading ~')
    return frozenset((x[1:], False) if x.startswith('~') else (x, True)
                     for x in literals)


def tautology(c: Clause) -> bool:
    return any((name, not polarity) in c for name, polarity in c)


def normalize(clauses: Iterable[Clause]) -> CNF:
    """Remove tautologies, duplicate clauses and subsumed clauses."""
    clean = frozenset(frozenset(c) for c in clauses if not tautology(c))
    return frozenset(c for c in clean if not any(d < c for d in clean))


def eval_cnf(formula: CNF, env: Mapping[str, bool]) -> bool:
    return all(any(env[name] == sign for name, sign in c) for c in formula)


def format_clause(c: Clause) -> str:
    return ' OR '.join(name if sign else '~' + name
                       for name, sign in sorted(c)) or 'FALSE'


def format_cnf(f: CNF) -> str:
    return ' AND '.join('(' + format_clause(c) + ')'
                        for c in sorted(f, key=lambda c: (len(c), sorted(c)))) or 'TRUE'


def eliminate(formula: CNF, variable: str) -> tuple[CNF, list[dict]]:
    """Finite Boolean variable elimination by all opposite-literal resolvents.

    Modern reconstruction of p39's fourth process, not an attribution of a
    modern SAT solver to Peirce. It computes exists(variable) formula over
    Boolean assignments. It does not represent existential class assertions I/O.
    """
    formula = normalize(formula)
    pos = sorted((c for c in formula if (variable, True) in c),
                 key=lambda c: sorted(c))
    neg = sorted((c for c in formula if (variable, False) in c),
                 key=lambda c: sorted(c))
    untouched = [c for c in formula if all(v != variable for v, _ in c)]
    result, trace = list(untouched), []
    for p in pos:
        for n in neg:
            resolvent = (p - {(variable, True)}) | (n - {(variable, False)})
            is_tautology = tautology(resolvent)
            trace.append({'positive': format_clause(p), 'negative': format_clause(n),
                          'resolvent': format_clause(resolvent),
                          'discarded_tautology': is_tautology})
            if not is_tautology:
                result.append(resolvent)
    return normalize(result), trace


def cnf_from_truth_function(names: Iterable[str], f: Callable) -> CNF:
    """Canonical full clauses, one excluding each false valuation (p38 analogue)."""
    names = tuple(names)
    return normalize(frozenset((name, not env[name]) for name in names)
                     for env in assignments(names) if not f(env))


def boole_original(e: Mapping[str, bool]) -> bool:
    """Image-checked p39 three premises, evaluated at one arbitrary individual."""
    v, x, y, z, w = (e[k] for k in ('v', 'x', 'y', 'z', 'w'))
    first = not (not x and not z) or (v and ((y and not w) or (not y and w)))
    second = not (not v and x and w) or ((y and z) or (not y and not z))
    third = ((x and y) or (v and x and not y)) == ((z and not w) or (not z and w))
    return first and second and third


def boole_six_clauses() -> CNF:
    """p41 six reduced premises, translated to modern clauses."""
    return normalize((clause('x', 'z', 'y', 'w'), clause('~x', '~y', 'z', 'w'),
                      clause('~x', '~y', '~z', '~w'), clause('~z', 'w', 'x'),
                      clause('z', '~w', 'x'), clause('~x', '~w', 'y', '~z')))


def boole_exact_solution(e: Mapping[str, bool]) -> bool:
    """Modern simplification of p41: x = z~w OR ~zw OR ~y~z~w."""
    f = ((e['z'] and not e['w']) or (not e['z'] and e['w']) or
         (not e['y'] and not e['z'] and not e['w']))
    return e['x'] == f


def boole_printed_summary(e: Mapping[str, bool]) -> bool:
    """p42 displayed final expression; not silently corrected to equivalence."""
    return e['x'] or (e['z'] and e['w']) or (e['y'] and not e['z'] and not e['w'])


@dataclass(frozen=True)
class Relation:
    """Binary relation over U={0,...,n-1}; pair order is (relate, correlate)."""
    n: int
    pairs: frozenset[tuple[int, int]]

    def __post_init__(self):
        if not isinstance(self.n, int) or isinstance(self.n, bool) or self.n < 0:
            raise ValueError('n must be a nonnegative integer')
        pairs = frozenset(self.pairs)
        if any(not isinstance(p, tuple) or len(p) != 2 or
               any(not isinstance(x, int) or isinstance(x, bool) or
                   x not in range(self.n) for x in p) for p in pairs):
            raise ValueError('Each pair must be a pair of integer members of U')
        object.__setattr__(self, 'pairs', pairs)

    @classmethod
    def top(cls, n: int):
        return cls(n, frozenset(product(range(n), repeat=2)))

    @classmethod
    def zero(cls, n: int):
        return cls(n, frozenset())

    @classmethod
    def identity(cls, n: int):
        return cls(n, frozenset((x, x) for x in range(n)))

    def _same(self, other):
        if not isinstance(other, Relation) or self.n != other.n:
            raise ValueError('Operations require the same explicit universe')

    def __or__(self, other):
        self._same(other)
        return Relation(self.n, self.pairs | other.pairs)

    def __and__(self, other):
        self._same(other)
        return Relation(self.n, self.pairs & other.pairs)

    def __le__(self, other):
        self._same(other)
        return self.pairs <= other.pairs

    def __invert__(self):
        return Relation(self.n, self.top(self.n).pairs - self.pairs)

    def converse(self):
        return Relation(self.n, frozenset((y, x) for x, y in self.pairs))

    def compose(self, other):
        """R;S: (x,z) iff exists y with R(x,y) and S(y,z)."""
        self._same(other)
        return Relation(self.n, frozenset((x, z) for x, y in self.pairs
                                         for yy, z in other.pairs if y == yy))

    def witnesses(self, other, x: int, z: int):
        self._same(other)
        return tuple(y for y in range(self.n)
                     if (x, y) in self.pairs and (y, z) in other.pairs)

    def regressive(self, other):
        """p52 (|--): not(R;not S), i.e. forall y: Rxy implies Syz."""
        return ~self.compose(~other)

    def progressive(self, other):
        """p52 (-|-): not(not R;S), i.e. forall y: Syz implies Rxy."""
        return ~(~self).compose(other)

    def transadd(self, other):
        """p52 (--|): not R;not S, existential in two negative operands."""
        return (~self).compose(~other)

    def classify(self) -> dict[str, bool]:
        """p47 definitions with p57 Note, plus modern explicit finite edge cases.

        'negative_of_X' means the COMPLEMENT has property X; it does not
        necessarily mean this relation fails to have property X.
        """
        diagonal = self.identity(self.n).pairs
        off_diagonal = self.top(self.n).pairs - diagonal
        r = self.pairs
        return {
            'concurrent': r <= diagonal,
            'opponent': bool(r & off_diagonal),
            'self_relative': bool(r & diagonal),
            'alio_relative': not bool(r & diagonal),
            'negative_of_concurrent': off_diagonal <= r,
            'negative_of_opponent': not off_diagonal <= r,
            'negative_of_self_relative': not diagonal <= r,
            'negative_of_alio_relative': diagonal <= r,
        }

    def matrix(self) -> tuple[tuple[int, ...], ...]:
        return tuple(tuple(int((x, y) in self.pairs) for y in range(self.n))
                     for x in range(self.n))


def all_relations(n: int):
    for p in powerset(product(range(n), repeat=2)):
        yield Relation(n, p)


def equality_pattern(values: Iterable) -> tuple[int, ...]:
    """Canonical restricted-growth string; equal objects receive equal labels."""
    labels, result = {}, []
    for x in values:
        if x not in labels:
            labels[x] = len(labels)
        result.append(labels[x])
    return tuple(result)


def equality_patterns(arity: int) -> tuple[tuple[int, ...], ...]:
    if not isinstance(arity, int) or isinstance(arity, bool) or arity < 0:
        raise ValueError('arity must be a nonnegative integer')
    rows = [()]
    for _ in range(arity):
        rows = [row + (v,) for row in rows for v in range(max(row, default=-1) + 2)]
    return tuple(rows)


def bell_numbers(max_arity: int) -> tuple[int, ...]:
    """Independent Stirling recurrence, includes B0=1."""
    if not isinstance(max_arity, int) or isinstance(max_arity, bool) or max_arity < 0:
        raise ValueError('max_arity must be a nonnegative integer')
    stirling, result = [1], [1]
    for n in range(1, max_arity + 1):
        previous = stirling
        stirling = [0] * (n + 1)
        for k in range(1, n + 1):
            stirling[k] = previous[k - 1] + (k * previous[k] if k < len(previous) else 0)
        result.append(sum(stirling))
    return tuple(result)


def m3_meet(a: str, b: str) -> str:
    """Five-element nondistributive lattice M3, a modern diagnostic countermodel."""
    if a not in ('0', 'a', 'b', 'c', '1') or b not in ('0', 'a', 'b', 'c', '1'):
        raise ValueError('Unknown M3 element')
    if a == b or b == '1':
        return a
    if a == '1':
        return b
    return '0'


def m3_join(a: str, b: str) -> str:
    if a not in ('0', 'a', 'b', 'c', '1') or b not in ('0', 'a', 'b', 'c', '1'):
        raise ValueError('Unknown M3 element')
    if a == b or b == '0':
        return a
    if a == '0':
        return b
    return '1'
