"""Modern teaching models, not Berkeley's code or a model of human cognition."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from fractions import Fraction


def exact(value: object) -> Fraction:
    """Accept exact rational inputs only; bool and float are not numbers here."""
    if type(value) not in (int, Fraction):
        raise TypeError("expected int or Fraction (not bool or float)")
    return Fraction(value)


def identifier(value: object) -> str:
    if type(value) is not str or not value or not value.isidentifier():
        raise ValueError("expected a nonempty identifier string")
    return value


@dataclass(frozen=True)
class Equation:
    """A rational linear equation with an explicit ordered variable schema."""

    variables: tuple[str, ...]
    coefficients: tuple[Fraction, ...]
    rhs: Fraction

    def __post_init__(self) -> None:
        if type(self.variables) is not tuple or not self.variables:
            raise TypeError("variables must be a nonempty tuple")
        for name in self.variables:
            identifier(name)
        if len(set(self.variables)) != len(self.variables):
            raise ValueError("duplicate variable")
        if type(self.coefficients) is not tuple:
            raise TypeError("coefficients must be a tuple")
        if len(self.variables) != len(self.coefficients):
            raise ValueError("coefficient dimension differs from variable schema")
        object.__setattr__(self, "coefficients", tuple(map(exact, self.coefficients)))
        object.__setattr__(self, "rhs", exact(self.rhs))


@dataclass(frozen=True)
class Premise:
    label: str
    equation: Equation

    def __post_init__(self) -> None:
        identifier(self.label)
        if type(self.equation) is not Equation:
            raise TypeError("premise equation must be Equation")


@dataclass(frozen=True)
class Certificate:
    """One exact weight per premise, in premise order."""

    weights: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        if type(self.weights) is not tuple:
            raise TypeError("weights must be a tuple")
        object.__setattr__(self, "weights", tuple(map(exact, self.weights)))


@dataclass(frozen=True)
class Verification:
    valid: bool
    combined: Equation
    dependencies: tuple[str, ...]


def check_certificate(
    premises: tuple[Premise, ...], target: Equation, certificate: Certificate
) -> Verification:
    """Recompute BOTH sides; no solver, assertions, or trusted dependency claim."""
    if type(premises) is not tuple or any(type(p) is not Premise for p in premises):
        raise TypeError("premises must be a tuple of Premise objects")
    if type(target) is not Equation or type(certificate) is not Certificate:
        raise TypeError("expected Equation and Certificate")
    labels = tuple(p.label for p in premises)
    if len(set(labels)) != len(labels):
        raise ValueError("duplicate premise label")
    if len(certificate.weights) != len(premises):
        raise ValueError("one weight is required per premise")
    if any(p.equation.variables != target.variables for p in premises):
        raise ValueError("all variable schemas must match, including order")
    coefficients = [Fraction(0) for _ in target.variables]
    rhs = Fraction(0)
    dependencies = []
    for premise, weight in zip(premises, certificate.weights):
        if weight != 0:
            dependencies.append(premise.label)
        for index, coefficient in enumerate(premise.equation.coefficients):
            coefficients[index] += weight * coefficient
        rhs += weight * premise.equation.rhs
    combined = Equation(target.variables, tuple(coefficients), rhs)
    return Verification(combined == target, combined, tuple(dependencies))


def restrict_certificate(
    premises: tuple[Premise, ...], target: Equation,
    certificate: Certificate, keep_labels: tuple[str, ...],
) -> tuple[tuple[Premise, ...], Certificate]:
    """Transfer this valid certificate after deleting only unused premises.

    Dependencies describe this certificate's nonzero rows, not the logically
    smallest assumption set. This is deliberately not a theorem prover.
    """
    checked = check_certificate(premises, target, certificate)
    if not checked.valid:
        raise ValueError("cannot transfer an invalid certificate")
    if type(keep_labels) is not tuple:
        raise TypeError("keep_labels must be a tuple")
    for label in keep_labels:
        identifier(label)
    if len(set(keep_labels)) != len(keep_labels):
        raise ValueError("duplicate kept label")
    if not set(keep_labels).issubset(p.label for p in premises):
        raise ValueError("unknown kept premise")
    missing = set(checked.dependencies).difference(keep_labels)
    if missing:
        raise ValueError("removed nonzero dependencies: " + ", ".join(sorted(missing)))
    pairs = tuple((p, w) for p, w in zip(premises, certificate.weights)
                  if p.label in keep_labels)
    reduced = tuple(p for p, _ in pairs)
    reduced_certificate = Certificate(tuple(w for _, w in pairs))
    # A transfer is accepted only after directly rechecking the reduced proof.
    if not check_certificate(reduced, target, reduced_certificate).valid:
        raise ValueError("reduced certificate does not prove the target")
    return reduced, reduced_certificate


def section16_example() -> tuple[tuple[Premise, ...], Equation, Certificate]:
    variables = ("a", "b", "c", "u", "v")
    premises = (
        Premise("alternate_a", Equation(variables, (1, 0, 0, -1, 0), 0)),
        Premise("alternate_c", Equation(variables, (0, 0, 1, 0, -1), 0)),
        Premise("straight_angle", Equation(variables, (0, 1, 0, 1, 1), 180)),
        Premise("drawing_right", Equation(variables, (0, 1, 0, 0, 0), 90)),
        Premise("drawing_isosceles", Equation(variables, (1, 0, -1, 0, 0), 0)),
    )
    target = Equation(variables, (1, 1, 1, 0, 0), 180)
    return premises, target, Certificate((1, 1, 1, 0, 0))


@dataclass(frozen=True)
class Triangle:
    """A particular nondegenerate straight-sided planar integer triangle."""

    vertices: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]

    def __post_init__(self) -> None:
        if type(self.vertices) is not tuple or len(self.vertices) != 3:
            raise TypeError("three vertices are required as a tuple")
        for point in self.vertices:
            if (type(point) is not tuple or len(point) != 2
                    or any(type(c) is not int for c in point)):
                raise TypeError("each vertex must contain two exact integers")
        a, b, c = self.vertices
        cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        if cross == 0:
            raise ValueError("collinear or repeated vertices are not triangles")

    def squared_sides(self) -> tuple[int, int, int]:
        a, b, c = self.vertices
        return tuple(sorted((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
                            for p, q in ((a, b), (b, c), (c, a))))

    def is_right(self) -> bool:
        x, y, z = self.squared_sides()
        return x + y == z


@dataclass(frozen=True)
class FiniteSign:
    """An explicit finite extension; a domain is not the set of all triangles."""

    name: str
    domain: tuple[Triangle, ...]
    denotation: frozenset[Triangle]

    def __post_init__(self) -> None:
        identifier(self.name)
        if (type(self.domain) is not tuple or not self.domain
                or any(type(t) is not Triangle for t in self.domain)):
            raise TypeError("domain must be a nonempty tuple of Triangle objects")
        if len(set(self.domain)) != len(self.domain):
            raise ValueError("duplicate domain case")
        if (type(self.denotation) is not frozenset
                or any(type(t) is not Triangle for t in self.denotation)):
            raise TypeError("denotation must be a frozenset of Triangle objects")
        if not self.denotation.issubset(self.domain):
            raise ValueError("denotation contains a case outside the domain")

    def covers_domain(self) -> bool:
        return self.denotation == frozenset(self.domain)


def first_counterexample(
    sign: FiniteSign, predicate: Callable[[Triangle], bool]
) -> Triangle | None:
    if type(sign) is not FiniteSign or not callable(predicate):
        raise TypeError("expected FiniteSign and a callable predicate")
    # Iterate in declared domain order to make the witness reproducible.
    for triangle in sign.domain:
        if triangle in sign.denotation:
            value = predicate(triangle)
            if type(value) is not bool:
                raise TypeError("predicate must return bool")
            if not value:
                return triangle
    return None


def triangle_cases() -> tuple[Triangle, ...]:
    return (
        Triangle(((0, 0), (3, 0), (0, 4))),
        Triangle(((0, 0), (2, 0), (1, 2))),
        Triangle(((0, 0), (4, 0), (1, 1))),
    )


class Expr:
    """Only the four concrete constructors below belong to the language."""


@dataclass(frozen=True)
class Const(Expr):
    value: Fraction

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", exact(self.value))


@dataclass(frozen=True)
class Var(Expr):
    name: str

    def __post_init__(self) -> None:
        identifier(self.name)


def require_expr(value: object) -> None:
    if type(value) not in (Const, Var, Add, Mul):
        raise TypeError("expected Const, Var, Add, or Mul")


@dataclass(frozen=True)
class Add(Expr):
    left: Expr
    right: Expr

    def __post_init__(self) -> None:
        require_expr(self.left)
        require_expr(self.right)


@dataclass(frozen=True)
class Mul(Expr):
    left: Expr
    right: Expr

    def __post_init__(self) -> None:
        require_expr(self.left)
        require_expr(self.right)


Monomial = tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class Polynomial:
    """Sorted nonzero coefficient terms with sorted positive variable powers."""

    terms: tuple[tuple[Monomial, Fraction], ...]

    def __post_init__(self) -> None:
        if type(self.terms) is not tuple:
            raise TypeError("terms must be a tuple")
        monomials = []
        canonical = []
        for term in self.terms:
            if type(term) is not tuple or len(term) != 2:
                raise TypeError("each term is a (monomial, coefficient) pair")
            monomial, coefficient = term
            if type(monomial) is not tuple:
                raise TypeError("monomial must be a tuple")
            names = []
            for power in monomial:
                if type(power) is not tuple or len(power) != 2:
                    raise TypeError("power must be a (name, exponent) pair")
                name, exponent = power
                identifier(name)
                if type(exponent) is not int or exponent <= 0:
                    raise ValueError("exponents must be positive integers")
                names.append(name)
            if names != sorted(set(names)):
                raise ValueError("monomial names must be unique and sorted")
            coefficient = exact(coefficient)
            if coefficient == 0:
                raise ValueError("canonical terms cannot have zero coefficients")
            monomials.append(monomial)
            canonical.append((monomial, coefficient))
        if monomials != sorted(set(monomials)):
            raise ValueError("monomials must be unique and sorted")
        object.__setattr__(self, "terms", tuple(canonical))


def _from_terms(terms: Mapping[Monomial, Fraction]) -> Polynomial:
    return Polynomial(tuple(sorted((m, c) for m, c in terms.items() if c != 0)))


def _add_poly(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left.terms)
    for monomial, coefficient in right.terms:
        result[monomial] = result.get(monomial, Fraction(0)) + coefficient
    return _from_terms(result)


def _multiply_poly(left: Polynomial, right: Polynomial) -> Polynomial:
    result: dict[Monomial, Fraction] = {}
    for lm, lc in left.terms:
        for rm, rc in right.terms:
            powers = dict(lm)
            for variable, exponent in rm:
                powers[variable] = powers.get(variable, 0) + exponent
            monomial = tuple(sorted(powers.items()))
            result[monomial] = result.get(monomial, Fraction(0)) + lc * rc
    return _from_terms(result)


def normalize(expression: Expr) -> Polynomial:
    require_expr(expression)
    if type(expression) is Const:
        return _from_terms({(): expression.value})
    if type(expression) is Var:
        return Polynomial(((((expression.name, 1),), Fraction(1)),))
    if type(expression) is Add:
        return _add_poly(normalize(expression.left), normalize(expression.right))
    return _multiply_poly(normalize(expression.left), normalize(expression.right))


def substitute(expression: Expr, replacements: Mapping[str, Expr]) -> Expr:
    """Simultaneous one-pass substitution; inserted trees are not revisited."""
    require_expr(expression)
    if not isinstance(replacements, Mapping):
        raise TypeError("replacements must be a mapping")
    validated = {}
    for name, replacement in replacements.items():
        identifier(name)
        require_expr(replacement)
        validated[name] = replacement

    def visit(node: Expr) -> Expr:
        if type(node) is Const:
            return node
        if type(node) is Var:
            return validated.get(node.name, node)
        if type(node) is Add:
            return Add(visit(node.left), visit(node.right))
        return Mul(visit(node.left), visit(node.right))

    return visit(expression)


def _environment(values: Mapping[str, Fraction]) -> dict[str, Fraction]:
    if not isinstance(values, Mapping):
        raise TypeError("environment must be a mapping")
    return {identifier(name): exact(value) for name, value in values.items()}


def evaluate_expr(expression: Expr, values: Mapping[str, Fraction]) -> Fraction:
    require_expr(expression)
    environment = _environment(values)

    def visit(node: Expr) -> Fraction:
        if type(node) is Const:
            return node.value
        if type(node) is Var:
            return environment[node.name]
        if type(node) is Add:
            return visit(node.left) + visit(node.right)
        return visit(node.left) * visit(node.right)

    return visit(expression)


def evaluate_polynomial(polynomial: Polynomial, values: Mapping[str, Fraction]) -> Fraction:
    if type(polynomial) is not Polynomial:
        raise TypeError("expected Polynomial")
    environment = _environment(values)
    result = Fraction(0)
    for monomial, coefficient in polynomial.terms:
        term = coefficient
        for variable, exponent in monomial:
            term *= environment[variable] ** exponent
        result += term
    return result
