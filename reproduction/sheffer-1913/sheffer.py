"""Original, standard-library teaching reconstruction of Sheffer (1913).

The source is a mathematical paper, not software.  This is new teaching code.
The guarded finite checker reproduces pp. 482–483; the syntax translator is a
modern executable illustration of p. 487 and the duality footnote on p. 488.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import re
from typing import Hashable

# Terms for the historical | operation. A string is a variable; a pair is |.
def bar(a, b):
    return (a, b)


def prime(a):
    return bar(a, a)


A, B, C = "a", "b", "c"
IDENTITIES = {
    "P3": (("a",), prime(prime(A)), A),
    "P4": (("a", "b"), bar(A, bar(B, prime(B))), prime(A)),
    "P5": (("a", "b", "c"), prime(bar(A, bar(B, C))),
           bar(bar(prime(B), A), bar(prime(C), A))),
}


class OutsideK(ValueError):
    """An indicated subterm is outside K; the guarded identity does not apply."""


@dataclass(frozen=True)
class FiniteKRule:
    """A total rule on K×K whose outputs need not lie in K.

    This is deliberately not assumed to be a closed binary algebra: closure is
    P2 and must remain testable. No operation is defined on outside-K inputs.
    """
    elements: tuple[Hashable, ...]
    values: tuple[Hashable, ...]  # row-major table on elements × elements
    name: str = "unnamed"

    def __post_init__(self):
        if len(set(self.elements)) != len(self.elements):
            raise ValueError("K must have distinct elements")
        if len(self.values) != len(self.elements) ** 2:
            raise ValueError("The rule must define every pair in K×K")
        object.__setattr__(self, "_K", frozenset(self.elements))
        object.__setattr__(self, "_table", dict(zip(product(self.elements, repeat=2), self.values)))

    def __call__(self, a, b):
        if a not in self._K or b not in self._K:
            raise OutsideK("A K-rule cannot be applied to an outside-K input")
        return self._table[a, b]

    def evaluate_guarded(self, term, assignment):
        if isinstance(term, str):
            value = assignment[term]
        else:
            left = self.evaluate_guarded(term[0], assignment)
            right = self.evaluate_guarded(term[1], assignment)
            value = self(left, right)
        # Guard every indicated combination, including each equation's roots.
        if value not in self._K:
            raise OutsideK("An indicated combination is outside K")
        return value

    def check(self):
        outside = [(a, b, self(a, b)) for a, b in product(self.elements, repeat=2)
                   if self(a, b) not in self._K]
        result = {
            "P1": {"holds": len(self.elements) >= 2, "size": len(self.elements)},
            "P2": {"holds": not outside, "outside_count": len(outside),
                   "witness": list(outside[0]) if outside else None},
        }
        for label, (variables, left, right) in IDENTITIES.items():
            checked = skipped = failures = 0
            witness = None
            for values in product(self.elements, repeat=len(variables)):
                assignment = dict(zip(variables, values))
                try:
                    lhs = self.evaluate_guarded(left, assignment)
                    rhs = self.evaluate_guarded(right, assignment)
                except OutsideK:
                    skipped += 1
                    continue
                checked += 1
                if lhs != rhs:
                    failures += 1
                    if witness is None:
                        witness = {"assignment": assignment, "left": lhs, "right": rhs}
            result[label] = {"holds": failures == 0, "checked": checked,
                             "guard_skipped": skipped, "failures": failures,
                             "witness": witness}
        return result

    def signature(self):
        result = self.check()
        return tuple(result[f"P{i}"]["holds"] for i in range(1, 6))


def original_finite_models():
    """p. 483 models, including a two-element instance of P2's arbitrary K."""
    return {
        "consistency": FiniteKRule(("m", "n"), ("n", "m", "m", "m"), "p.483 consistency"),
        "independent_P1": FiniteKRule(("m",), ("m",), "p.483 (1) singleton"),
        "independent_P2": FiniteKRule(("m", "n"), ("m", "outside", "outside", "n"),
                                      "p.483 (2) nonclosed K-rule"),
        "independent_P3": FiniteKRule(("m", "n"), ("m", "m", "m", "m"),
                                      "p.483 (3) constant m"),
        "independent_P5": FiniteKRule(("l", "m", "n"),
                                      ("l", "m", "n", "n", "n", "l", "m", "l", "m"),
                                      "p.483 (5) three-element table"),
    }


def rational_bar(a, b):
    """Exact p.483 (4) rule, accepting int/Fraction or two symbolic Linear forms.

    Integers are promoted before division, including integers too large for
    float to represent exactly. Float inputs are rejected rather than silently
    treating a binary floating-point approximation as an exact rational input.
    Linear inputs belong to the symbolic checker, not the rational carrier K.
    """
    if isinstance(a, Linear) and isinstance(b, Linear):
        return -(a + b) / 2
    if (isinstance(a, (int, Fraction)) and not isinstance(a, bool)
            and isinstance(b, (int, Fraction)) and not isinstance(b, bool)):
        return -(Fraction(a) + Fraction(b)) / 2
    raise TypeError("Use int/Fraction inputs, or two Linear forms; floats and mixed symbolic inputs are unsupported")


@dataclass(frozen=True)
class Linear:
    """Exact coefficients of a*a_var + b*b_var + c*c_var; no CAS dependency.

    All expressions in the rational countermodel are homogeneous linear forms,
    so coefficient equality is exact symbolic verification for arbitrary inputs.
    """
    coefficients: tuple[Fraction, Fraction, Fraction]

    def __add__(self, other):
        return Linear(tuple(a + b for a, b in zip(self.coefficients, other.coefficients)))

    def __neg__(self):
        return Linear(tuple(-x for x in self.coefficients))

    def __truediv__(self, divisor):
        return Linear(tuple(x / divisor for x in self.coefficients))

    def strings(self):
        return [str(x) for x in self.coefficients]


def evaluate_term(term, assignment, operation):
    if isinstance(term, str):
        return assignment[term]
    return operation(evaluate_term(term[0], assignment, operation),
                     evaluate_term(term[1], assignment, operation))


def rational_symbolic_results():
    basis = {name: Linear(tuple(Fraction(int(i == j)) for i in range(3)))
             for j, name in enumerate(("a", "b", "c"))}
    result = {}
    for label, (_, left, right) in IDENTITIES.items():
        lhs = evaluate_term(left, basis, rational_bar)
        rhs = evaluate_term(right, basis, rational_bar)
        result[label] = {"holds_identically": lhs == rhs,
                         "left_coefficients_a_b_c": lhs.strings(),
                         "right_coefficients_a_b_c": rhs.strings()}
    a, b = Fraction(1), Fraction(0)
    result["P4_witness"] = {"a": str(a), "b": str(b),
                             "left": str(rational_bar(a, rational_bar(b, rational_bar(b, b)))),
                             "right": str(rational_bar(a, a))}
    result["scope"] = "Exact symbolic identities over Q; P1 and rational closure P2 are justified in README."
    return result


def closed_signature(n, values):
    """Independent fast evaluator for CLOSED row-major tables only.

    Used for small exhaustive enumeration; compared with the guarded checker in
    tests. P2 is true by construction here, so this cannot investigate its
    independence. Returns P1, P2, P3, P4, P5.
    """
    prime_values = [values[a * n + a] for a in range(n)]
    op = lambda a, b: values[a * n + b]
    p3 = all(prime_values[prime_values[a]] == a for a in range(n))
    p4 = all(op(a, op(b, prime_values[b])) == prime_values[a]
             for a, b in product(range(n), repeat=2))
    p5 = all(prime_values[op(a, op(b, c))] == op(op(prime_values[b], a), op(prime_values[c], a))
             for a, b, c in product(range(n), repeat=3))
    return n >= 2, True, p3, p4, p5


def enumerate_closed(n):
    if n not in (1, 2, 3):
        raise ValueError("Teaching enumeration is intentionally limited to n=1,2,3")
    total = 0
    all_five = []
    signatures = {}
    for values in product(range(n), repeat=n * n):
        total += 1
        signature = closed_signature(n, values)
        key = "".join("1" if truth else "0" for truth in signature)
        signatures[key] = signatures.get(key, 0) + 1
        if all(signature):
            all_five.append(list(values))
    return {"n": n, "tables_examined": total, "all_five_count": len(all_five),
            "all_five_tables_row_major": all_five, "signature_counts": dict(sorted(signatures.items())),
            "scope": "All labeled closed binary tables on range(n); no quotient by isomorphism."}


# Modern executable illustration: source formula ASTs and single-gate ASTs.
# The source | token here is ordinary OR, not the historical algebraic |.
TOKEN = re.compile(r"\s*(->|[A-Za-z][A-Za-z0-9_]*|[~!&|()])")


def parse(text):
    """Parse ~,! (NOT), & (AND), | (OR), -> (right-associative implication).

    Precedence, strongest first: NOT, AND, OR, implication. No eval(), code
    execution, implicit multiplication, or constants. Lower/uppercase variable
    names are distinct. The & and -> conveniences are modern extensions.
    """
    tokens = []
    pos = 0
    while pos < len(text):
        if not text[pos:].strip():
            break
        match = TOKEN.match(text, pos)
        if not match:
            raise ValueError(f"Unexpected character at position {pos}")
        tokens.append(match.group(1))
        pos = match.end()
    index = 0

    def accept(token):
        nonlocal index
        if index < len(tokens) and tokens[index] == token:
            index += 1
            return True
        return False

    def atom():
        nonlocal index
        if accept("~") or accept("!"):
            return ("not", atom())
        if accept("("):
            result = implication()
            if not accept(")"):
                raise ValueError("Missing closing parenthesis")
            return result
        if index >= len(tokens) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", tokens[index]):
            raise ValueError("Expected a variable or parenthesized formula")
        name = tokens[index]
        index += 1
        return ("var", name)

    def conjunction():
        result = atom()
        while accept("&"):
            result = ("and", result, atom())
        return result

    def disjunction():
        result = conjunction()
        while accept("|"):
            result = ("or", result, conjunction())
        return result

    def implication():
        result = disjunction()
        if accept("->"):
            result = ("imp", result, implication())
        return result

    result = implication()
    if index != len(tokens):
        raise ValueError("Unexpected trailing token")
    return result


def variables(ast):
    if ast[0] == "var":
        return {ast[1]}
    return set().union(*(variables(child) for child in ast[1:]))


def eval_formula(ast, assignment):
    kind = ast[0]
    if kind == "var":
        return bool(assignment[ast[1]])
    left = eval_formula(ast[1], assignment)
    if kind == "not":
        return not left
    right = eval_formula(ast[2], assignment)
    if kind == "and":
        return left and right
    if kind == "or":
        return left or right
    if kind == "imp":
        return (not left) or right
    if kind == "nor":
        return not (left or right)
    if kind == "nand":
        return not (left and right)
    raise ValueError(f"Unknown operation {kind}")


def translate(ast, target="nor"):
    """Compile structurally to only variables and the chosen one-gate basis."""
    if target not in ("nor", "nand"):
        raise ValueError("Target must be nor or nand")
    if ast[0] == "var":
        return ast
    gate = lambda x, y: (target, x, y)
    neg = lambda x: gate(x, x)
    left = translate(ast[1], target)
    if ast[0] == "not":
        return neg(left)
    right = translate(ast[2], target)
    if ast[0] == "imp":
        left = neg(left)
        kind = "or"
    else:
        kind = ast[0]
    if target == "nor":
        if kind == "or":
            return neg(gate(left, right))
        if kind == "and":
            return gate(neg(left), neg(right))
    else:
        if kind == "or":
            return gate(neg(left), neg(right))
        if kind == "and":
            return neg(gate(left, right))
    raise ValueError(f"Unsupported source operation {ast[0]}")


def gate_only(ast, target):
    return ast[0] == "var" or (ast[0] == target and all(gate_only(x, target) for x in ast[1:]))


def equivalent(left, right):
    names = sorted(variables(left) | variables(right))
    for bits in product((False, True), repeat=len(names)):
        env = dict(zip(names, bits))
        if eval_formula(left, env) != eval_formula(right, env):
            return False, env
    return True, None


def format_formula(ast):
    if ast[0] == "var":
        return ast[1]
    if ast[0] == "not":
        return "~" + format_formula(ast[1])
    return f"({format_formula(ast[1])} {ast[0]} {format_formula(ast[2])})"


def formulas_up_to_depth(depth):
    """All syntactic formulas over p,q, NOT,OR with tree height ≤ depth."""
    current = {("var", "p"), ("var", "q")}
    for _ in range(depth):
        previous = tuple(sorted(current))
        current = {("var", "p"), ("var", "q")}
        current.update(("not", x) for x in previous)
        current.update(("or", x, y) for x in previous for y in previous)
    return sorted(current)


def translation_experiment(depth=2):
    formulas = formulas_up_to_depth(depth)
    checks = 0
    for ast in formulas:
        for target in ("nor", "nand"):
            compiled = translate(ast, target)
            if not gate_only(compiled, target):
                raise AssertionError("Translation retained a foreign connective")
            for bits in product((False, True), repeat=2):
                env = dict(zip(("p", "q"), bits))
                assert eval_formula(ast, env) == eval_formula(compiled, env)
                checks += 1
    return {"source_formulas": len(formulas), "maximum_tree_height": depth,
            "targets": ["nor", "nand"], "truth_assignments_per_formula": 4,
            "formula_target_assignment_checks": checks, "mismatches": 0,
            "scope": "Finite bounded test; the general construction is justified by structural induction."}
