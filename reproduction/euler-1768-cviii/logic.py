"""Small classical propositional checker; original teaching implementation.

A formula is a bool, an atom name, or (operator, argument, ...).
Operators: not, and, or, implies. JSON arrays work like tuples.
No Python eval, external dependencies, or historical semantic identification.
"""
from dataclasses import dataclass
from itertools import product
import re

MAX_ATOMS = 12
MAX_DEPTH = 64
_ARITY = {"not": 1, "and": 2, "or": 2, "implies": 2}
_NAME = re.compile(r"[A-Za-z][A-Za-z0-9_]*\Z")


def _atoms(names):
    if not isinstance(names, (list, tuple)):
        raise ValueError("atoms must be a list or tuple")
    if len(names) > MAX_ATOMS:
        raise ValueError(f"at most {MAX_ATOMS} atoms are supported")
    if any(not isinstance(n, str) or not _NAME.fullmatch(n) for n in names):
        raise ValueError("atom names must match [A-Za-z][A-Za-z0-9_]*")
    if len(set(names)) != len(names):
        raise ValueError("duplicate atoms are not allowed")
    return tuple(sorted(names))


def formula(value, names, depth=0):
    """Validate and freeze an expression, rejecting unknown atoms and bad arity."""
    if depth > MAX_DEPTH:
        raise ValueError(f"formula depth exceeds {MAX_DEPTH}")
    if type(value) is bool:
        return value
    if isinstance(value, str):
        if value not in names:
            raise ValueError(f"unknown atom: {value}")
        return value
    if not isinstance(value, (tuple, list)) or not value:
        raise ValueError("formula must be bool, declared atom, or operator array")
    op = value[0]
    if not isinstance(op, str) or op not in _ARITY:
        raise ValueError("unknown operator")
    if len(value) != _ARITY[op] + 1:
        raise ValueError(f"{op} requires {_ARITY[op]} operand(s)")
    return (op,) + tuple(formula(v, names, depth + 1) for v in value[1:])


def _evaluate(expr, world):
    if type(expr) is bool:
        return expr
    if isinstance(expr, str):
        return world[expr]
    op = expr[0]
    left = _evaluate(expr[1], world)
    if op == "not":
        return not left
    right = _evaluate(expr[2], world)
    if op == "and":
        return left and right
    if op == "or":
        return left or right
    return (not left) or right


def _world(world, names):
    if not isinstance(world, dict) or set(world) != set(names):
        raise ValueError("each world must assign exactly the declared atoms")
    if any(type(v) is not bool for v in world.values()):
        raise ValueError("world values must be booleans (not numbers)")
    return tuple(world[n] for n in names)


def evaluate(expr, world):
    """Evaluate at one assignment; this is not a consequence claim."""
    if not isinstance(world, dict):
        raise ValueError("world must be a dictionary")
    names = _atoms(list(world))
    _world(world, names)
    return _evaluate(formula(expr, names), world)


@dataclass(frozen=True, init=False)
class Theory:
    """Finite allowed worlds, intersected with explicit propositional constraints.

    allowed_worlds=None enumerates all assignments; [] describes no worlds.
    Empty theories remain representable so the checker can warn about vacuity.
    """
    atoms: tuple
    constraints: tuple
    worlds: tuple

    def __init__(self, atoms, constraints=(), allowed_worlds=None):
        names = _atoms(atoms)
        if not isinstance(constraints, (tuple, list)):
            raise ValueError("constraints must be a list or tuple")
        rules = tuple(formula(c, names) for c in constraints)
        if allowed_worlds is None:
            rows = product((False, True), repeat=len(names))
        else:
            if not isinstance(allowed_worlds, (tuple, list)):
                raise ValueError("allowed_worlds must be a list or tuple")
            rows = sorted(set(_world(w, names) for w in allowed_worlds))
        kept = tuple(row for row in rows
                     if all(_evaluate(c, dict(zip(names, row))) for c in rules))
        object.__setattr__(self, "atoms", names)
        object.__setattr__(self, "constraints", rules)
        object.__setattr__(self, "worlds", kept)

    def check(self, premises, conclusion):
        """Check every allowed world, returning all counterexamples in fixed order."""
        if not isinstance(premises, (tuple, list)):
            raise ValueError("premises must be a list or tuple")
        premises = tuple(formula(p, self.atoms) for p in premises)
        conclusion = formula(conclusion, self.atoms)
        witnesses, counterexamples = [], []
        for row in self.worlds:
            world = dict(zip(self.atoms, row))
            if all(_evaluate(p, world) for p in premises):
                witnesses.append(world)
                if not _evaluate(conclusion, world):
                    counterexamples.append(world)
        warning = None
        if not self.worlds:
            warning = "empty theory: validity is vacuous; no allowed world exists"
        elif not witnesses:
            warning = "inconsistent premises in this theory: validity is vacuous"
        return {
            "valid": not counterexamples,
            "theory_consistent": bool(self.worlds),
            "premises_consistent": bool(witnesses),
            "allowed_world_count": len(self.worlds),
            "premise_world_count": len(witnesses),
            "counterexamples": counterexamples,
            "warning": warning,
        }
