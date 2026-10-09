"""Curry (1930), Teil I: contextual reduction and a separate equality kernel.

Only Python's standard library is used.  The reducer has exactly four rules;
I is a parse-time abbreviation for W K, not a fifth primitive.  The equality
kernel additionally admits the sixteen combinatory axioms in pp. 521, 534–535
and the equality properties established in I.D.  It is not an implementation
of the whole Q/Π/P/Λ assertion calculus, nor a decision procedure.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Union


@dataclass(frozen=True)
class Atom:
    name: str

    def __post_init__(self):
        if not re.fullmatch(r"[A-Z][0-9]*|[a-z][a-z0-9_]*", self.name):
            raise ValueError("atom must be one capital with optional digits or a lowercase identifier")
        if self.name == "I":
            raise ValueError("I is an abbreviation; use the exported I or parse('I')")


@dataclass(frozen=True)
class App:
    fn: Term
    arg: Term


Term = Union[Atom, App]
B, C, W, K = (Atom(c) for c in "BCWK")
I = App(W, K)
PRIMITIVES = frozenset((B, C, W, K))


def app(fn: Term, *args: Term) -> Term:
    """Application is left associative: app(f,x,y) = ((f x) y)."""
    for arg in args:
        fn = App(fn, arg)
    return fn


def parse(source: str) -> Term:
    """Read whitespace/application and parentheses; capitals can be adjacent.

    Thus BXY and B X Y agree; 'foo' is one lowercase atom.  I expands to W K.
    Dot composition and indexed sequence names are provided as Python helpers,
    not overloaded parser syntax.  B2 is an atom, not sequence('B',2).
    """
    token_re = re.compile(r"\s+|[A-Z][0-9]*|[a-z][a-z0-9_]*|[()]")
    tokens, pos = [], 0
    for match in token_re.finditer(source):
        if match.start() != pos:
            raise ValueError(f"invalid syntax at character {pos}")
        pos = match.end()
        if not match.group().isspace():
            tokens.append(match.group())
    if pos != len(source):
        raise ValueError(f"invalid syntax at character {pos}")
    cursor = 0

    def group(nested=False):
        nonlocal cursor
        terms = []
        while cursor < len(tokens) and tokens[cursor] != ")":
            tok = tokens[cursor]
            cursor += 1
            if tok == "(":
                terms.append(group(True))
            else:
                terms.append(I if tok == "I" else Atom(tok))
        if not terms:
            raise ValueError("empty expression or parentheses")
        if nested:
            if cursor == len(tokens):
                raise ValueError("missing closing parenthesis")
            cursor += 1
        return app(terms[0], *terms[1:])

    term = group()
    if cursor != len(tokens):
        raise ValueError("unexpected closing parenthesis")
    return term


def pretty(t: Term) -> str:
    """Round-trippable notation; retain W K visibly instead of hiding it as I."""
    if isinstance(t, Atom):
        return t.name
    right = pretty(t.arg)
    if isinstance(t.arg, App):
        right = f"({right})"
    return f"{pretty(t.fn)} {right}"


def spine(t: Term) -> tuple[Term, tuple[Term, ...]]:
    args = []
    while isinstance(t, App):
        args.append(t.arg)
        t = t.fn
    return t, tuple(reversed(args))


def atoms(t: Term) -> frozenset[Atom]:
    if isinstance(t, Atom):
        return frozenset((t,))
    return atoms(t.fn) | atoms(t.arg)


def root_contract(t: Term) -> tuple[Term, str] | None:
    head, args = spine(t)
    if head == B and len(args) >= 3:
        x, y, z = args[:3]
        return app(app(x, app(y, z)), *args[3:]), "B"
    if head == C and len(args) >= 3:
        x, y, z = args[:3]
        return app(app(x, z, y), *args[3:]), "C"
    if head == W and len(args) >= 2:
        x, y = args[:2]
        return app(app(x, y, y), *args[2:]), "W"
    if head == K and len(args) >= 2:
        return app(args[0], *args[2:]), "K"
    return None


@dataclass(frozen=True)
class Step:
    before: Term
    after: Term
    rule: str
    path: tuple[int, ...]  # 0 = function child; 1 = argument child


def step(t: Term) -> Step | None:
    """Deterministic full contextual, leftmost-outermost single contraction.

    It searches arguments too. A contraction whose result equals its input is
    still a step (important for W W W), never a normal-form signal.
    """
    contracted = root_contract(t)
    if contracted is not None:
        after, rule = contracted
        return Step(t, after, rule, ())
    if isinstance(t, App):
        left = step(t.fn)
        if left is not None:
            return Step(t, App(left.after, t.arg), left.rule, (0,) + left.path)
        right = step(t.arg)
        if right is not None:
            return Step(t, App(t.fn, right.after), right.rule, (1,) + right.path)
    return None


@dataclass(frozen=True)
class Run:
    start: Term
    end: Term
    steps: tuple[Step, ...]
    status: str  # normal, cycle, or fuel_exhausted
    cycle_start: int | None = None
    cycle_length: int | None = None


def normalize(t: Term, fuel=1000, detect_cycles=True) -> Run:
    """Fuel counts contractions, not AST visits. Exhaustion is inconclusive.

    Cycle means this deterministic strategy revisited an identical term. It
    does not generally prove that every strategy diverges. W W W separately
    has just one redex, which contracts to itself.
    """
    if type(fuel) is not int or fuel < 0:
        raise ValueError("fuel must be a nonnegative integer")
    start, history, seen = t, [], {t: 0}
    while True:
        nxt = step(t)
        if nxt is None:
            return Run(start, t, tuple(history), "normal")
        if len(history) == fuel:
            return Run(start, t, tuple(history), "fuel_exhausted")
        history.append(nxt)
        t = nxt.after
        if detect_cycles and t in seen:
            return Run(start, t, tuple(history), "cycle", seen[t], len(history) - seen[t])
        seen[t] = len(history)


def normal(t: Term, fuel=1000) -> Term:
    run = normalize(t, fuel)
    if run.status != "normal":
        raise ValueError(f"no normal form obtained: {run.status}")
    return run.end


def sequence(kind: str, n: int) -> Term:
    """Definitions II.B.1 (p.529), II.B.3 (pp.531–532).

    B_0=I, B_1=B, B_(n+1)=B B B_n (n>=1).
    C_1=C, C_(n+1)=B C_n; likewise W and K.
    B_1=B B B_0 is an equality theorem, NOT our syntactic definition.
    """
    if type(n) is not int or kind not in "BCWK" or len(kind) != 1:
        raise ValueError("expected kind B/C/W/K and an integer index")
    if n < (0 if kind == "B" else 1):
        raise ValueError("B permits n>=0; C/W/K require n>=1")
    if n == 0:
        return I
    result = {"B": B, "C": C, "W": W, "K": K}[kind]
    for _ in range(1, n):
        result = app(B, B, result) if kind == "B" else app(B, result)
    return result


def dot(x: Term, y: Term) -> Term:
    """II.B.4 Def.1, p.532: X dot Y is the abbreviation B X Y."""
    return app(B, x, y)


# Finite combinatory equations, I.C.5 p.521 / II.B.5 pp.534–535.
# BW uses the unambiguous p.534 restatement: the literal p.521 printing
# appears to have misplaced/missing parentheses (kept separately below).
# I is always expanded. These are NOT added to root_contract.
AXIOM_TEXT = (
    ("B", "C(BB(BBB))B", "B(BB)B"),
    ("C", "C(BB(BBB))C", "B(BC)(BBB)"),
    ("W", "C(BBB)W", "B(BW)(BBB)"),
    ("K", "C(BBB)K", "B(BK)I"),
    ("I1", "CBI", "B(BI)I"),
    ("BC", "BBC", "B(B(BC)C)(BB)"),
    ("BW", "BBW", "B(B(B(B(BW)W)(BC))(B(BB)))B"),
    ("BK", "BBK", "BKK"),
    ("CC1", "BCC", "B(BI)"),
    ("CC2", "B(B(BC)C)(BC)", "B(BC(BC))C"),
    ("CW", "BCW", "B(B(BW)C)(BC)"),
    ("CK", "BCK", "BK"),
    ("WC", "BWC", "W"),
    ("WW", "BWW", "BW(BW)"),
    ("WK", "BWK", "BI"),
    ("I2", "BI", "I"),
)
AXIOMS = {name: (parse(left), parse(right)) for name, left, right in AXIOM_TEXT}
# Literal-looking reading of p.521. It is intentionally NOT a kernel premise.
BW_P521_LITERAL = (parse("BBW"), parse("B(B(B(B(BW)W)(BC))B(BB))B"))


def dot_many(*terms: Term) -> Term:
    if not terms:
        raise ValueError("empty product")
    result = terms[0]
    for term in terms[1:]:
        result = dot(result, term)
    return result


def axioms_in_product_notation() -> dict[str, tuple[Term, Term]]:
    """Independent structural transcription of II.B.5, pp.534–535.

    Multiple dots associate LEFT by II.B.4 Def.3. The theorem of associativity
    is not silently used to change these trees. This also disambiguates BW.
    """
    b2, b3, c2, w2 = sequence("B", 2), sequence("B", 3), sequence("C", 2), sequence("W", 2)
    return {
        "B": (app(C, b3, B), dot(app(B, B), B)),
        "C": (app(C, b3, C), dot(app(B, C), b2)),
        "W": (app(C, b2, W), dot(app(B, W), b2)),
        "K": (app(C, b2, K), dot(app(B, K), I)),
        "I1": (app(C, B, I), dot(app(B, I), I)),
        "BC": (dot(B, C), dot_many(c2, C, app(B, B))),
        "BW": (dot(B, W), dot_many(w2, W, c2, app(b2, B), B)),
        "BK": (dot(B, K), dot(K, K)),
        "CC1": (dot(C, C), app(b2, I)),
        "CC2": (dot_many(c2, C, c2), dot_many(C, c2, C)),
        "CW": (dot(C, W), dot_many(w2, C, c2)),
        "CK": (dot(C, K), sequence("K", 2)),
        "WC": (dot(W, C), W),
        "WW": (dot(W, W), dot(W, w2)),
        "WK": (dot(W, K), app(B, I)),
        "I2": (app(B, I), I),
    }


# Number of symbolic arguments needed here to expose variable-only outputs.
AXIOM_ARITIES = dict(zip(AXIOMS, (4, 4, 3, 3, 2, 4, 3, 3, 3, 4, 3, 3, 2, 2, 2, 2)))


@dataclass(frozen=True)
class Proof:
    """Certificate syntax. No claimed endpoints: the checker computes them."""
    rule: str
    data: tuple = ()
    premises: tuple[Proof, ...] = ()


class InvalidProof(ValueError):
    pass


def _term(t):
    if isinstance(t, Atom):
        return
    if isinstance(t, App):
        _term(t.fn)
        _term(t.arg)
        return
    raise InvalidProof("not a term")


def check(p: Proof) -> tuple[Term, Term]:
    """Small explicit equational kernel, independent of the reduction matcher.

    Trusted premises: pp.521/534–535 combinatory axioms; p.522 B/C/W/K schemas;
    reflexivity/symmetry/transitivity/application congruence from I.D (pp.522–524).
    There is deliberately NO eta/extensionality or 'tested equal' rule.
    """
    if not isinstance(p, Proof):
        raise InvalidProof("not a proof")
    r, d, ps = p.rule, p.data, p.premises
    if r == "refl" and len(d) == 1 and not ps:
        _term(d[0])
        return d[0], d[0]
    if r == "axiom" and len(d) == 1 and not ps and d[0] in AXIOMS:
        return AXIOMS[d[0]]
    if r == "sym" and not d and len(ps) == 1:
        left, right = check(ps[0])
        return right, left
    if r == "trans" and not d and len(ps) == 2:
        left, middle = check(ps[0])
        other, right = check(ps[1])
        if middle != other:
            raise InvalidProof("transitivity endpoints do not match")
        return left, right
    if r == "app" and not d and len(ps) == 2:
        f, g = check(ps[0])
        x, y = check(ps[1])
        return app(f, x), app(g, y)
    if r in ("B", "C", "W", "K") and not ps:
        arity = 3 if r in ("B", "C") else 2
        if len(d) != arity:
            raise InvalidProof("incorrect rule arity")
        for t in d:
            _term(t)
        # These endpoint constructions do not call root_contract or step.
        if r == "B":
            x, y, z = d
            return app(B, x, y, z), app(x, app(y, z))
        if r == "C":
            x, y, z = d
            return app(C, x, y, z), app(x, z, y)
        x, y = d
        return (app(W, x, y), app(x, y, y)) if r == "W" else (app(K, x, y), x)
    raise InvalidProof(f"unknown or malformed certificate rule: {r}")


def refl(t):
    return Proof("refl", (t,))


def sym(p):
    return Proof("sym", premises=(p,))


def chain(*proofs):
    if not proofs:
        raise ValueError("empty chain")
    result = proofs[0]
    for p in proofs[1:]:
        result = Proof("trans", premises=(result, p))
    return result


def congruence(p, q):
    return Proof("app", premises=(p, q))


def applied(p, *args):
    for arg in args:
        p = congruence(p, refl(arg))
    return p


def axiom(name):
    return Proof("axiom", (name,))


def certify_step(s: Step) -> Proof:
    """Translate an untrusted reducer step into a kernel-checked certificate."""
    def under(t, path):
        if not path:
            head, args = spine(t)
            arity = 3 if s.rule in ("B", "C") else 2
            p = Proof(s.rule, args[:arity])
            return applied(p, *args[arity:])
        if not isinstance(t, App) or path[0] not in (0, 1):
            raise InvalidProof("bad context path")
        if path[0] == 0:
            return congruence(under(t.fn, path[1:]), refl(t.arg))
        return congruence(refl(t.fn), under(t.arg, path[1:]))
    p = under(s.before, s.path)
    if check(p) != (s.before, s.after):
        raise InvalidProof("step and certified endpoints disagree")
    return p


def certify_run(run: Run) -> Proof:
    result, current = refl(run.start), run.start
    for s in run.steps:
        if s.before != current:
            raise InvalidProof("disconnected trace")
        result = chain(result, certify_step(s))
        current = s.after
    if current != run.end:
        raise InvalidProof("trace endpoint mismatch")
    return result


def by_reduction(left: Term, right: Term, fuel=1000) -> Proof:
    """Find a shared normal form; return proof, not an equality oracle."""
    a, b = normalize(left, fuel), normalize(right, fuel)
    if a.status != "normal" or b.status != "normal" or a.end != b.end:
        raise ValueError("no shared normal form found by this strategy")
    return chain(certify_run(a), sym(certify_run(b)))


def cbi_identity_proof() -> Proof:
    """II.B.2 Satz 3 (p.531), explicitly using Ax.I1 and Ax.I2."""
    p1 = axiom("I1")                       # C B I = B (B I) I
    p2 = applied(congruence(refl(B), axiom("I2")), I)  # = B I I
    p3 = applied(axiom("I2"), I)           # = I I
    p4 = by_reduction(app(I, I), I)         # = I
    return chain(p1, p2, p3, p4)


def right_identity_proof(x: Term) -> Proof:
    """II.B.2 Satz 4: B X I = X, without an extensionality inference."""
    identity_action = chain(Proof("W", (K, x)), Proof("K", (x, x)))
    return chain(sym(Proof("C", (B, I, x))),
                 applied(cbi_identity_proof(), x), identity_action)


def _distribution_symbolic_proof(x: Term, y: Term) -> Proof:
    """II.B.4 Satz 2 (pp.532–533): B (X dot Y) = B X dot B Y.

    Apply Ax.B to X,Y, then connect endpoints by certified B/C reductions.
    """
    p = applied(axiom("B"), x, y)
    left_mid, right_mid = check(p)
    desired_left = app(B, dot(x, y))
    desired_right = dot(app(B, x), app(B, y))
    return chain(by_reduction(desired_left, right_mid), sym(p),
                 by_reduction(left_mid, desired_right))


def _associativity_symbolic_proof(x: Term, y: Term, z: Term) -> Proof:
    """II.B.4 Satz 3 (p.533): (X dot Y) dot Z = X dot (Y dot Z)."""
    left = dot(dot(x, y), z)
    middle = app(dot(app(B, x), app(B, y)), z)
    right = dot(x, dot(y, z))
    return chain(applied(_distribution_symbolic_proof(x, y), z), by_reduction(middle, right))


def substitute(t: Term, replacements: dict[Atom, Term]) -> Term:
    """Simultaneous metavariable substitution, never replacement of B/C/W/K."""
    if any(not isinstance(key, Atom) or key in PRIMITIVES for key in replacements):
        raise ValueError("only nonprimitive atoms may be substituted")
    for value in replacements.values():
        _term(value)
    def go(term):
        if isinstance(term, Atom):
            return replacements.get(term, term)
        return app(go(term.fn), go(term.arg))
    return go(t)


def instantiate(p: Proof, replacements: dict[Atom, Term]) -> Proof:
    """Instantiate a checked schema, preserving axioms and primitive constants.

    Uses structural substitution, not evaluation of replacement terms. This
    permits nonnormalizing arguments. The resulting finite proof is checked.
    """
    before = check(p)
    expected = tuple(substitute(t, replacements) for t in before)
    def go(node):
        data = tuple(substitute(t, replacements) if isinstance(t, (Atom, App)) else t
                     for t in node.data)
        return Proof(node.rule, data, tuple(go(q) for q in node.premises))
    result = go(p)
    if check(result) != expected:
        raise InvalidProof("instantiation changed a trusted constant or endpoint")
    return result


def distribution_proof(x: Term, y: Term) -> Proof:
    """II.B.4 Satz 2 for arbitrary terms, including divergent arguments."""
    sx, sy = Atom("sx"), Atom("sy")
    return instantiate(_distribution_symbolic_proof(sx, sy), {sx: x, sy: y})


def associativity_proof(x: Term, y: Term, z: Term) -> Proof:
    """II.B.4 Satz 3 for arbitrary terms; only a symbolic template is reduced."""
    sx, sy, sz = Atom("sx"), Atom("sy"), Atom("sz")
    return instantiate(_associativity_symbolic_proof(sx, sy, sz), {sx: x, sy: y, sz: z})


def axiom_names_used(p: Proof) -> frozenset[str]:
    result = frozenset((p.data[0],)) if p.rule == "axiom" else frozenset()
    for child in p.premises:
        result |= axiom_names_used(child)
    return result


def proof_nodes(p: Proof) -> int:
    return 1 + sum(proof_nodes(q) for q in p.premises)


def fresh_args(count: int) -> tuple[Term, ...]:
    return tuple(Atom(f"x{n}") for n in range(count))


def saturated_axiom_check(name: str, arity: int) -> tuple[Run, Run]:
    """Check a symbolic applied instance; never infer the unsaturated axiom.

    Requiring a variable-only result prevents a misleading partial-application
    pass. The closed axiom remains an independent premise of the eq kernel.
    """
    left, right = AXIOMS[name]
    args = fresh_args(arity)
    a, b = normalize(app(left, *args)), normalize(app(right, *args))
    if a.status != "normal" or b.status != "normal":
        raise ValueError("saturated check did not normalize")
    if a.end != b.end or atoms(a.end) & PRIMITIVES:
        raise ValueError("not a common variable-only normal form")
    check(certify_run(a))
    check(certify_run(b))
    return a, b
