"""Bounded TOY examples, not a reconstruction of Gödel's 1931 formal system.

Python 3.10+, standard library only. See README.zh-CN.md for mathematical limits.
"""

from dataclasses import dataclass
from math import prod


# Fixed bounds keep every accepted example small. They are teaching limits,
# not hypotheses or limits in the incompleteness theorems.
PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,
          41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89)
MAX_LENGTH = len(PRIMES)
MAX_SYMBOL = 31
MAX_CODE = prod(PRIMES) ** (MAX_SYMBOL + 1)
MAX_AST_NODES = 12
MAX_PROOF_LINES = MAX_LENGTH // 3


def is_natural(value):
    """Do not silently accept bool as int."""
    return type(value) is int and value >= 0


def encode(items):
    """TOY: [] -> 1; [a0,...,ak] -> product(p_i ** (a_i + 1))."""
    if not isinstance(items, (list, tuple)):
        raise TypeError("use a finite list or tuple")
    if len(items) > MAX_LENGTH:
        raise ValueError("sequence exceeds the teaching length bound")
    if any(not is_natural(a) or a > MAX_SYMBOL for a in items):
        raise ValueError("symbols must be integers from 0 through 31")
    return prod(p ** (a + 1) for p, a in zip(PRIMES, items))


def decode(code):
    """Invert encode; reject gaps, residual primes, and out-of-range input."""
    if not is_natural(code) or not 1 <= code <= MAX_CODE:
        raise ValueError("not a positive code in the teaching range")
    remaining = code
    symbols = []
    for prime in PRIMES:
        if remaining == 1:
            return tuple(symbols)
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1
            if exponent > MAX_SYMBOL + 1:
                raise ValueError("symbol exceeds the teaching bound")
        if exponent == 0:
            raise ValueError("prime gap: a later factor exists after a missing position")
        symbols.append(exponent - 1)
    if remaining != 1:
        raise ValueError("sequence exceeds the teaching length bound")
    return tuple(symbols)


def component(code, index):
    """Zero-based component; indexing an absent position raises IndexError."""
    if not is_natural(index):
        raise ValueError("index must be a natural number")
    return decode(code)[index]


def concatenate(left_code, right_code):
    """Decode, concatenate, then encode; multiplication is not concatenation."""
    return encode(decode(left_code) + decode(right_code))


# This AST deliberately has no quantifiers, binders, or function symbols
# other than addition. Therefore every variable occurrence is free.
@dataclass(frozen=True)
class Nat:
    value: int


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Add:
    left: object
    right: object


@dataclass(frozen=True)
class Eq:
    left: object
    right: object


@dataclass(frozen=True)
class Not:
    body: object


@dataclass(frozen=True)
class And:
    left: object
    right: object


VARIABLES = ("x", "y", "z")
TERM_TYPES = (Nat, Var, Add)
FORMULA_TYPES = (Eq, Not, And)


def validate_formula(formula):
    """Reject ill-typed syntax and oversized trees before recursion."""
    pending = [(formula, "formula")]
    count = 0
    while pending:
        node, expected = pending.pop()
        count += 1
        if count > MAX_AST_NODES:
            raise ValueError("AST exceeds the teaching node bound")
        allowed = FORMULA_TYPES if expected == "formula" else TERM_TYPES
        if type(node) not in allowed:
            raise ValueError("ill-typed or unsupported syntax; quantifiers are not supported")
        if type(node) is Nat:
            if not is_natural(node.value) or node.value > MAX_SYMBOL:
                raise ValueError("numeral is outside 0..31")
        elif type(node) is Var:
            if type(node.name) is not str or node.name not in VARIABLES:
                raise ValueError("only x, y and z are supported")
        elif type(node) in (Add, Eq):
            pending.extend(((node.right, "term"), (node.left, "term")))
        elif type(node) is Not:
            pending.append((node.body, "formula"))
        else:
            pending.extend(((node.right, "formula"), (node.left, "formula")))


def substitute_numeral(formula, variable, value):
    """Replace every occurrence of a free variable with a numeral.

    The language is QUANTIFIER-FREE; this is not a general binding-aware
    substitution implementation and is not Gödel's original Sb operation.
    """
    validate_formula(formula)
    if type(variable) is not str or variable not in VARIABLES:
        raise ValueError("unsupported variable")
    if not is_natural(value) or value > MAX_SYMBOL:
        raise ValueError("numeral is outside 0..31")

    def walk(node):
        if type(node) is Var:
            return Nat(value) if node.name == variable else node
        if type(node) is Nat:
            return node
        if type(node) is Not:
            return Not(walk(node.body))
        return type(node)(walk(node.left), walk(node.right))

    return walk(formula)


def formula_tokens(formula):
    """An unambiguous prefix token stream; tags have fixed arity.

    Nat=0,value; Var=1,index; Add=2,left,right; Eq=3,left,right;
    Not=4,body; And=5,left,right. This is our own syntax convention.
    """
    validate_formula(formula)

    def walk(node):
        if type(node) is Nat:
            return (0, node.value)
        if type(node) is Var:
            return (1, VARIABLES.index(node.name))
        if type(node) is Not:
            return (4,) + walk(node.body)
        tag = {Add: 2, Eq: 3, And: 5}[type(node)]
        return (tag,) + walk(node.left) + walk(node.right)

    return walk(formula)


def formula_code(formula):
    return encode(formula_tokens(formula))


def evaluate(formula, environment=None):
    """Evaluate in the intended natural-number interpretation, not prove."""
    validate_formula(formula)
    environment = {} if environment is None else environment

    def walk(node):
        if type(node) is Nat:
            return node.value
        if type(node) is Var:
            value = environment[node.name]  # Unassigned variables raise KeyError.
            if not is_natural(value) or value > MAX_SYMBOL:
                raise ValueError("variable assignment is outside 0..31")
            return value
        if type(node) is Add:
            return walk(node.left) + walk(node.right)
        if type(node) is Eq:
            return walk(node.left) == walk(node.right)
        if type(node) is Not:
            return not walk(node.body)
        # Evaluate both branches, so missing variables are not hidden.
        left, right = walk(node.left), walk(node.right)
        return left and right

    return walk(formula)


# A SEPARATE tiny proof system over four atomic claims. It is not arithmetic
# and is not the AST language above. Formula codes here are just 0, 1, 2, 3.
CLAIMS = ("A", "B", "C", "D")
AXIOMS = (0,)  # A
RULES = {1: (0, 1), 2: (1, 2), 3: (2, 3)}  # A->B, B->C, C->D


@dataclass(frozen=True)
class ProofStep:
    claim: int
    rule: int      # 0 = axiom; 1..3 = one of RULES.
    premise: int   # 0 for axioms; otherwise a ONE-based earlier line number.


def check_proof(proof, target):
    """Decide whether this particular finite object is a proof of target."""
    if not is_natural(target) or target >= len(CLAIMS):
        return False
    if not isinstance(proof, (list, tuple)) or not 1 <= len(proof) <= MAX_PROOF_LINES:
        return False
    for index, step in enumerate(proof):
        if type(step) is not ProofStep:
            return False
        if any(not is_natural(v) for v in (step.claim, step.rule, step.premise)):
            return False
        if step.claim >= len(CLAIMS):
            return False
        if step.rule == 0:
            if step.claim not in AXIOMS or step.premise != 0:
                return False
        else:
            if step.rule not in RULES or not 1 <= step.premise <= index:
                return False
            antecedent, consequent = RULES[step.rule]
            if proof[step.premise - 1].claim != antecedent or step.claim != consequent:
                return False
    return proof[-1].claim == target


def encode_proof(proof):
    """Encode structurally well-formed steps, even if the argument is invalid."""
    if not isinstance(proof, (list, tuple)) or len(proof) > MAX_PROOF_LINES:
        raise ValueError("proof exceeds the teaching line bound")
    if any(type(step) is not ProofStep for step in proof):
        raise ValueError("each line must be a ProofStep")
    return encode(tuple(v for step in proof for v in (step.claim, step.rule, step.premise)))


def proof_relation(proof_code, target):
    """TOY Proof(p,q): decode p, then check that its last line proves q."""
    try:
        symbols = decode(proof_code)
    except (ValueError, TypeError):
        return False
    if len(symbols) % 3:
        return False
    proof = tuple(ProofStep(*symbols[i:i + 3]) for i in range(0, len(symbols), 3))
    return check_proof(proof, target)


def _extensions(proof):
    for axiom in AXIOMS:
        yield proof + (ProofStep(axiom, 0, 0),)
    for number, prior in enumerate(proof, 1):
        for rule, (antecedent, consequent) in RULES.items():
            if prior.claim == antecedent:
                yield proof + (ProofStep(consequent, rule, number),)


@dataclass(frozen=True)
class SearchResult:
    proof: object
    max_lines: int
    candidates_checked: int


def bounded_search(target, max_lines):
    """Enumerate valid proof prefixes, shortest first, within a line bound.

    A missing witness means only that none was found within this bound.
    This function does NOT decide theoremhood of a general formal theory.
    """
    if not is_natural(target) or target >= len(CLAIMS):
        raise ValueError("unknown target claim")
    if not is_natural(max_lines) or max_lines > MAX_PROOF_LINES:
        raise ValueError("line bound must be from 0 through 8")
    frontier = [()]
    checked = 0
    for _ in range(max_lines):
        next_frontier = []
        for prefix in frontier:
            for proof in _extensions(prefix):
                checked += 1
                if check_proof(proof, target):
                    return SearchResult(proof, max_lines, checked)
                next_frontier.append(proof)
        frontier = next_frontier
    return SearchResult(None, max_lines, checked)
