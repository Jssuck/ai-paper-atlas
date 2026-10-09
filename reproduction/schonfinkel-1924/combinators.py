"""Modern educational executable model, not code from the 1924 paper.

Original names: I, C, T, Z, S. K is a Python alias for original C.
Application associates to the left. Only combinators bind reduction rules;
there are no variable binders in this term language.
"""
from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class Var:
    name: str
    def __str__(self):
        return self.name

@dataclass(frozen=True)
class Comb:
    name: str
    def __post_init__(self):
        if self.name not in {'I', 'C', 'T', 'Z', 'S'}:
            raise ValueError('Unknown original combinator: ' + self.name)
    def __str__(self):
        return self.name

@dataclass(frozen=True)
class App:
    function: 'Term'
    argument: 'Term'
    def __str__(self):
        return f'({self.function} {self.argument})'

Term = Union[Var, Comb, App]
I, C, T, Z, S = (Comb(n) for n in ('I', 'C', 'T', 'Z', 'S'))
K = C  # Modern name for original C; NOT modern argument-exchange C.


def app(head: Term, *arguments: Term) -> Term:
    for argument in arguments:
        head = App(head, argument)
    return head


def free_variables(term: Term) -> frozenset:
    if isinstance(term, Var):
        return frozenset((term.name,))
    if isinstance(term, Comb):
        return frozenset()
    return free_variables(term.function) | free_variables(term.argument)


def substitute(term: Term, name: str, replacement: Term) -> Term:
    """Structural substitution: this AST contains no binders to capture names."""
    if isinstance(term, Var):
        return replacement if term.name == name else term
    if isinstance(term, Comb):
        return term
    return App(substitute(term.function, name, replacement),
               substitute(term.argument, name, replacement))


def abstract(name: str, term: Term) -> Term:
    """Modern bracket abstraction using I, C (= modern K), S.

    [x]x=I; [x]E=C E if x not free in E; [x](P Q)=S([x]P)([x]Q).
    This educational algorithm is not asserted to be literal 1924 pseudocode.
    """
    if term == Var(name):
        return I
    if name not in free_variables(term):
        return app(C, term)
    if isinstance(term, App):
        return app(S, abstract(name, term.function), abstract(name, term.argument))
    raise AssertionError('Unreachable for a well-formed term')


def step(term: Term):
    """One leftmost-outermost rewrite, or None for a full normal form.

    Partial applications do not fire; extra arguments are preserved.
    Reductions under both application branches seek full normal forms.
    """
    arguments = []
    head = term
    while isinstance(head, App):
        arguments.append(head.argument)
        head = head.function
    arguments.reverse()
    arities = {'I': 1, 'C': 2, 'T': 3, 'Z': 3, 'S': 3}
    if isinstance(head, Comb) and len(arguments) >= arities[head.name]:
        n = arities[head.name]
        used = arguments[:n]
        if head == I:
            result = used[0]
        elif head == C:
            result = used[0]
        elif head == T:
            f, x, y = used
            result = app(f, y, x)
        elif head == Z:
            f, g, x = used
            result = app(f, app(g, x))
        else:
            f, g, x = used
            result = app(f, x, app(g, x))
        return app(result, *arguments[n:])
    if isinstance(term, App):
        left = step(term.function)
        if left is not None:
            return App(left, term.argument)
        right = step(term.argument)
        if right is not None:
            return App(term.function, right)
    return None


class StepLimitExceeded(RuntimeError):
    def __init__(self, term: Term, steps: int):
        self.term, self.steps = term, steps
        super().__init__(f'Reduction budget exhausted after {steps} steps; '
                         'this alone does not prove divergence.')


def normalize(term: Term, max_steps: int = 1000):
    """Return (normal_form, rewrites). Budget exhaustion is not a halting proof."""
    if not isinstance(max_steps, int) or max_steps < 0:
        raise ValueError('max_steps must be a nonnegative integer')
    count = 0
    while True:
        following = step(term)
        if following is None:
            return term, count
        if count == max_steps:
            raise StepLimitExceeded(term, count)
        term, count = following, count + 1


def finite_u(domain):
    """A finite semantic model of U(f)(g)=forall x, not(f(x) and g(x)).

    Domain is explicitly required to be nonempty for these teaching examples.
    Predicates must be pure, total Boolean functions on that domain.
    U is NOT a syntactic reduction rule of the I,C,T,Z,S reducer.
    """
    values = tuple(domain)
    if not values:
        raise ValueError('This demonstration requires a nonempty domain')
    def first(f):
        def second(g):
            return all(not (f(x) and g(x)) for x in values)
        return second
    return first
