"""Modern exact affine reconstruction; all equations mean expression == 0."""
from dataclasses import dataclass
from fractions import Fraction as F


def q(value):
    if type(value) not in (int, F):
        raise TypeError('coefficients must be int or Fraction, not float/bool')
    return F(value)


@dataclass(frozen=True)
class Aff:
    r: F = F(0)
    l: F = F(0)
    c: F = F(0)

    def __post_init__(self):
        for name in ('r', 'l', 'c'):
            object.__setattr__(self, name, q(getattr(self, name)))

    def __add__(self, other):
        if not isinstance(other, Aff):
            other = Aff(c=q(other))
        return Aff(self.r + other.r, self.l + other.l, self.c + other.c)

    __radd__ = __add__

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other if isinstance(other, Aff) else -q(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, scalar):
        scalar = q(scalar)
        return Aff(self.r * scalar, self.l * scalar, self.c * scalar)

    __rmul__ = __mul__

    def at(self, r, l):
        return self.r * q(r) + self.l * q(l) + self.c


R, L = Aff(r=1), Aff(l=1)


def equation(left, right):
    """Translate equality to left minus right == 0."""
    if not isinstance(left, Aff):
        left = Aff(c=q(left))
    return left - right


def system(rows):
    rows = tuple(rows)
    if any(not isinstance(row, Aff) for row in rows):
        raise TypeError('each equation must be Aff')
    return rows


def holds(rows, r, l):
    r, l = q(r), q(l)
    return all(row.at(r, l) == 0 for row in system(rows))


def row_step(rows, op):
    """swap(i,j), scale(i,s!=0), add(i,j,s) replacing row i by i+s*j."""
    rows = list(system(rows))
    if not isinstance(op, tuple) or not op:
        raise ValueError('operation must be a nonempty tuple')
    kind = op[0]
    arity = {'swap': 3, 'scale': 3, 'add': 4}
    if kind not in arity or len(op) != arity[kind]:
        raise ValueError('unknown operation or wrong arity')
    indexes = op[1:3] if kind in ('swap', 'add') else op[1:2]
    if any(type(i) is not int or not 0 <= i < len(rows) for i in indexes):
        raise ValueError('invalid row index')
    i = op[1]
    if kind == 'swap':
        j = op[2]
        rows[i], rows[j] = rows[j], rows[i]
    elif kind == 'scale':
        scalar = q(op[2])
        if scalar == 0:
            raise ValueError('zero scaling loses information')
        rows[i] = rows[i] * scalar
    else:
        j, scalar = op[2], q(op[3])
        if i == j:
            raise ValueError('row addition requires different rows')
        rows[i] = rows[i] + rows[j] * scalar
    return tuple(rows)


def certificate(rows, operations):
    trace = [system(rows)]
    for op in operations:
        trace.append(row_step(trace[-1], op))
    return tuple(trace)


def canonical(rows):
    """RREF of augmented homogeneous coefficient rows [r,l,c]."""
    matrix = [[row.r, row.l, row.c] for row in system(rows)]
    pivot = 0
    for col in range(3):
        found = next((i for i in range(pivot, len(matrix)) if matrix[i][col]), None)
        if found is None:
            continue
        matrix[pivot], matrix[found] = matrix[found], matrix[pivot]
        divisor = matrix[pivot][col]
        matrix[pivot] = [x / divisor for x in matrix[pivot]]
        for i in range(len(matrix)):
            if i != pivot:
                scalar = matrix[i][col]
                matrix[i] = [x - scalar*y for x, y in zip(matrix[i], matrix[pivot])]
        pivot += 1
    # All inconsistent affine systems have the same empty solution set.
    if any(a == b == 0 and c != 0 for a, b, c in matrix):
        return (Aff(c=1),)
    return tuple(Aff(*row) for row in matrix if any(row))


def equivalent(first, second):
    """Equality of rational solution sets, not of physical feasibility."""
    return canonical(first) == canonical(second)


def solve(rows):
    reduced = canonical(rows)
    if reduced == (Aff(c=1),):
        return {'kind': 'none', 'point': None}
    if len(reduced) < 2:
        return {'kind': 'infinite', 'point': None}
    return {'kind': 'unique', 'point': (-reduced[0].c, -reduced[1].c)}


def transfer(a=1, b=1, k=2):
    a, b, k = q(a), q(b), q(k)
    return (equation(R-a, L+a), equation(R+b, k*(L-b)))


def feasible(r, l, a=1, b=1):
    """Indivisible counters; N={0,1,...}; enough in each independent donor."""
    r, l, a, b = map(q, (r, l, a, b))
    return all(x.denominator == 1 and x >= 0 for x in (r, l, a, b)) and r >= a and l >= b


def oracle(rows, bound):
    """Finite square 0<=R,L<=bound, equation truth only, not transfer feasibility."""
    if type(bound) is not int or bound < 0:
        raise ValueError('bound must be a nonnegative integer')
    rows = system(rows)
    return tuple((r, l) for r in range(bound+1) for l in range(bound+1) if holds(rows, r, l))


def sequential(a=1, b=1, k=2):
    """Countermodel: second transfer follows first, rather than resetting."""
    a, b, k = q(a), q(b), q(k)
    return (equation(R-a, L+a), equation(R-a+b, k*(L+a-b)))
