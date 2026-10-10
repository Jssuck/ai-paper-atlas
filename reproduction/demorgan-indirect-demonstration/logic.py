"""Original finite teaching models; not De Morgan's historical notation."""
from dataclasses import dataclass
from functools import lru_cache
from itertools import product


def implication(p, q):
    """Classical material implication on exactly two Python booleans."""
    if type(p) is not bool or type(q) is not bool:
        raise ValueError("Classical truth values must be bool")
    return (not p) or q


def truth_table():
    return [{"p": p, "q": q, "p_implies_q": implication(p, q),
             "not_q_implies_not_p": implication(not q, not p),
             "q_implies_p": implication(q, p)}
            for p, q in product((False, True), repeat=2)]


def powerset(items):
    """Stable enumeration, provided items have a stable order."""
    items = tuple(items)
    for mask in range(1 << len(items)):
        yield frozenset(x for i, x in enumerate(items) if mask & (1 << i))


def class_case(domain, a, b):
    """All complements are relative to the same finite domain."""
    domain, a, b = map(frozenset, (domain, a, b))
    if not a <= domain or not b <= domain:
        raise ValueError("Both classes must lie in the common domain")
    not_b, not_a = domain - b, domain - a
    return {
        "all_A_are_B": all(x in b for x in a),
        "all_not_B_are_not_A": all(x in not_a for x in not_b),
        "positive_counterexamples": a & not_b,
        "contrapositive_counterexamples": not_b & a,
        "converse_all_B_are_A": all(x in a for x in b),
    }


@dataclass(frozen=True)
class Formula:
    op: str
    args: tuple = ()
    name: str = ""

    def __post_init__(self):
        if type(self.args) is not tuple:
            raise ValueError("Formula arguments must be an immutable tuple")
        if self.op == "atom":
            if not isinstance(self.name, str) or not self.name or self.args:
                raise ValueError("Atom needs a nonempty name and no arguments")
        elif self.op == "bottom":
            if self.args or self.name:
                raise ValueError("Bottom has no arguments or name")
        elif self.op in ("and", "or", "imp"):
            if self.name or len(self.args) != 2 or not all(
                    isinstance(x, Formula) for x in self.args):
                raise ValueError("Binary connective needs two formulas")
        else:
            raise ValueError("Unknown connective")


def Atom(name):
    return Formula("atom", name=name)


BOTTOM = Formula("bottom")


def And(a, b):
    return Formula("and", (a, b))


def Or(a, b):
    return Formula("or", (a, b))


def Imp(a, b):
    return Formula("imp", (a, b))


def Not(a):
    """Intuitionistic negation is implication to bottom, never Python not."""
    return Imp(a, BOTTOM)


@dataclass(frozen=True)
class Frame:
    n: int
    relation: frozenset

    def __post_init__(self):
        if type(self.n) is not int or self.n < 1:
            raise ValueError("A frame must have a positive integer world count")
        relation = frozenset(self.relation)
        object.__setattr__(self, "relation", relation)
        if any(type(edge) is not tuple or len(edge) != 2 or
               any(type(w) is not int or not 0 <= w < self.n for w in edge)
               for edge in relation):
            raise ValueError("Relation contains a malformed or unknown world")
        if any((w, w) not in relation for w in range(self.n)):
            raise ValueError("Relation must be reflexive")
        if any((u, z) not in relation
               for u, v in relation for x, z in relation if v == x):
            raise ValueError("Relation must be transitive")

    def future(self, world):
        if type(world) is not int or not 0 <= world < self.n:
            raise ValueError("Unknown world")
        return tuple(v for v in range(self.n) if (world, v) in self.relation)

    def is_upset(self, worlds):
        worlds = frozenset(worlds)
        return (all(type(w) is int and 0 <= w < self.n for w in worlds)
                and all(v in worlds for u, v in self.relation if u in worlds))


@dataclass(frozen=True)
class Model:
    frame: Frame
    valuation: tuple

    def __post_init__(self):
        entries = tuple((name, frozenset(worlds)) for name, worlds in self.valuation)
        names = [name for name, _ in entries]
        if any(not isinstance(name, str) or not name for name in names):
            raise ValueError("Valuation names must be nonempty strings")
        if len(names) != len(set(names)):
            raise ValueError("Duplicate atom in valuation")
        if any(not self.frame.is_upset(worlds) for _, worlds in entries):
            raise ValueError("Atomic valuations must be persistent and in the frame")
        object.__setattr__(self, "valuation", tuple(sorted(entries)))

    @classmethod
    def from_mapping(cls, frame, valuation):
        return cls(frame, tuple(valuation.items()))

    def force(self, world, formula):
        """Recursive forcing; false means 'not forced', not 'negation forced'."""
        self.frame.future(world)  # Reject invalid worlds, even for bottom.
        if not isinstance(formula, Formula):
            raise ValueError("Expected a Formula")
        values = dict(self.valuation)

        # Validate all atoms before short-circuit evaluation.
        def validate(f):
            if f.op == "atom" and f.name not in values:
                raise ValueError("Atom missing from valuation: " + f.name)
            for child in f.args:
                validate(child)
        validate(formula)

        @lru_cache(maxsize=None)
        def visit(w, f):
            if f.op == "atom":
                return w in values[f.name]
            if f.op == "bottom":
                return False
            a, b = f.args
            if f.op == "and":
                return visit(w, a) and visit(w, b)
            if f.op == "or":
                return visit(w, a) or visit(w, b)
            # Crucially, quantify over every accessible future, including w.
            return all(not visit(v, a) or visit(v, b)
                       for v in self.frame.future(w))
        return visit(world, formula)


def formula_suite():
    p, q = Atom("p"), Atom("q")
    direct, contra = Imp(p, q), Imp(Not(q), Not(p))
    return {
        "bottom": BOTTOM, "p": p, "q": q,
        "not_p": Not(p), "not_q": Not(q),
        "p_implies_q": direct, "q_implies_p": Imp(q, p),
        "not_q_implies_not_p": contra,
        "forward_contraposition": Imp(direct, contra),
        "reverse_contraposition": Imp(contra, direct),
        "not_of_p_implies_q": Not(direct),
        "double_not_q": Not(Not(q)),
        "double_negation_elimination_q": Imp(Not(Not(q)), q),
        "excluded_middle_q": Or(q, Not(q)),
        "p_and_q": And(p, q), "p_or_q": Or(p, q),
        "p_and_not_p": And(p, Not(p)),
        "explosion": Imp(BOTTOM, p),
        "identity": Imp(p, p),
        "and_elimination": Imp(And(p, q), p),
        "or_introduction": Imp(p, Or(p, q)),
        "not_or": Not(Or(p, q)),
        "and_of_negations": And(Not(p), Not(q)),
        "not_and": Not(And(p, q)),
        "or_of_negations": Or(Not(p), Not(q)),
    }


def two_world_model():
    return Model.from_mapping(Frame(2, frozenset({(0, 0), (0, 1), (1, 1)})),
                              {"p": {0, 1}, "q": {1}})


def labeled_preorders(n):
    """Enumerate all reflexive/transitive labeled relations, including cycles."""
    diagonal = frozenset((w, w) for w in range(n))
    off_diagonal = tuple((u, v) for u in range(n) for v in range(n) if u != v)
    for edges in powerset(off_diagonal):
        try:
            yield Frame(n, diagonal | edges)
        except ValueError:
            continue
