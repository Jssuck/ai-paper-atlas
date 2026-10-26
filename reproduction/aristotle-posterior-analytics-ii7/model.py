"""Finite teaching model for APo II.7, not a theory of real essence."""
from dataclasses import dataclass
from typing import Mapping


def checked_set(universe, values):
    u, p = frozenset(universe), frozenset(values)
    if not p <= u:
        raise ValueError('predicate/observation outside universe')
    return u, p


def coextensive(universe, p, q):
    u, p = checked_set(universe, p)
    _, q = checked_set(u, q)
    return p == q


def witness_valid(universe, predicate, witness):
    u, p = checked_set(universe, predicate)
    return witness in u and witness in p


def transfer_witness(universe, p, q, witness):
    """Check equality and a Q witness; return whether it certifies P membership."""
    return coextensive(universe, p, q) and witness_valid(universe, q, witness)


def observations_agree(universe, observed, p, q):
    u, s = checked_set(universe, observed)
    _, p = checked_set(u, p)
    _, q = checked_set(u, q)
    return p & s == q & s


@dataclass(frozen=True)
class NameClaim:
    name: str
    formula_id: str


def binding_valid(lexicon: Mapping[str, str], claim: NameClaim):
    """Check only supplied symbolic convention, not external correctness."""
    if not isinstance(claim.name, str) or not isinstance(claim.formula_id, str):
        raise TypeError('name and formula_id must be strings')
    return claim.name in lexicon and lexicon[claim.name] == claim.formula_id


def named_witness(universe, formulas, lexicon, claim, witness):
    """Require independent symbolic binding plus finite membership evidence."""
    if not binding_valid(lexicon, claim):
        return False
    if claim.formula_id not in formulas:
        return False
    return witness_valid(universe, formulas[claim.formula_id], witness)


def subsets(n):
    if type(n) is not int or n < 0:
        raise ValueError('n must be a nonnegative integer')
    return [frozenset(i for i in range(n) if mask & (1 << i)) for mask in range(1 << n)]
