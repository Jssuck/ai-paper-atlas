#!/usr/bin/env python3
"""Finite-support teaching model of second-figure AEIO inference.

Modern set semantics, not a reconstruction of every historical assumption.
Only Python's standard library is required. See README.md and WALKTHROUGH.md.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from itertools import product
import json
from pathlib import Path
from typing import Iterable, Iterator

QUANTIFIERS = ("A", "E", "I", "O")
TERMS = ("P", "M", "S")
TERM_BITS = {"P": 4, "M": 2, "S": 1}


class Policy(str, Enum):
    """Existence requirements, independent of the truth of A/E sentences."""

    ALLOW_EMPTY = "allow-empty"
    ALL_NONEMPTY = "all-nonempty"
    SUBJECT_NONEMPTY = "subject-nonempty"


REQUIRED_NONEMPTY = {
    Policy.ALLOW_EMPTY: (),
    Policy.ALL_NONEMPTY: TERMS,
    Policy.SUBJECT_NONEMPTY: ("S",),
}


def _policy(value: Policy | str) -> Policy:
    if not isinstance(value, (str, Policy)):
        raise TypeError("policy must be a Policy or its string value")
    try:
        return Policy(value)
    except ValueError as exc:
        raise ValueError(f"unknown policy: {value!r}") from exc


def _quantifier(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("quantifier must be a string")
    if value not in QUANTIFIERS:
        raise ValueError("quantifier must be exactly A, E, I, or O")
    return value


def _term(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("term must be a string")
    if value not in TERMS:
        raise ValueError("term must be exactly P, M, or S")
    return value


def _support(value: int) -> int:
    # bool is deliberately not accepted as the integer mask 0 or 1.
    if type(value) is not int:
        raise TypeError("support must be an integer, not bool or a coercible value")
    if not 1 <= value <= 255:
        raise ValueError("support must be in 1..255 (the universe is nonempty)")
    return value


def occupied_atoms(support: int) -> tuple[int, ...]:
    """Return occupied membership types, encoded by the bits P=4, M=2, S=1."""
    _support(support)
    return tuple(atom for atom in range(8) if support & (1 << atom))


def extension(support: int, term: str) -> frozenset[int]:
    """Use the occupied atom IDs themselves as concrete universe elements."""
    _term(term)
    return frozenset(atom for atom in occupied_atoms(support) if atom & TERM_BITS[term])


def evaluate_categorical(quantifier: str, subject: Iterable, predicate: Iterable) -> bool:
    """Direct set semantics for arbitrary finite, hashable domain elements.

    A(X,Y): X <= Y; E(X,Y): X and Y disjoint;
    I(X,Y): X intersects Y; O(X,Y): X has an element outside Y.
    A and E do not imply existence. Repeated input elements are harmless.
    """
    _quantifier(quantifier)
    x, y = frozenset(subject), frozenset(predicate)
    if quantifier == "A":
        return x <= y
    if quantifier == "E":
        return x.isdisjoint(y)
    if quantifier == "I":
        return bool(x & y)
    return bool(x - y)


def holds(support: int, quantifier: str, subject: str, predicate: str) -> bool:
    """Evaluate one clause by occupied-atom flags, without the set evaluator."""
    atoms = occupied_atoms(support)
    _quantifier(quantifier)
    _term(subject)
    _term(predicate)
    x_bit, y_bit = TERM_BITS[subject], TERM_BITS[predicate]
    both = any((atom & x_bit) and (atom & y_bit) for atom in atoms)
    outside = any((atom & x_bit) and not (atom & y_bit) for atom in atoms)
    if quantifier == "A":
        return not outside
    if quantifier == "E":
        return not both
    if quantifier == "I":
        return both
    return outside


def compress_model(universe: Iterable, P: Iterable, M: Iterable, S: Iterable) -> int:
    """Replace a finite model by one representative per occupied membership type.

    The nonempty universe and term extensions must contain hashable objects;
    each extension must be a subset of that universe. Multiplicity is forgotten.
    """
    u = frozenset(universe)
    extensions = {"P": frozenset(P), "M": frozenset(M), "S": frozenset(S)}
    if not u:
        raise ValueError("universe must be nonempty")
    if any(not term <= u for term in extensions.values()):
        raise ValueError("every term extension must be a subset of the universe")
    mask = 0
    for obj in u:
        atom = sum(TERM_BITS[term] for term in TERMS if obj in extensions[term])
        mask |= 1 << atom
    return mask


def concrete_model(support: int) -> dict[str, list[str]]:
    """A JSON-friendly smallest realization of a support; no repeated types."""
    atoms = occupied_atoms(support)
    names = {atom: f"x{index + 1}" for index, atom in enumerate(atoms)}
    model = {"universe": [names[atom] for atom in atoms]}
    model.update({term: [names[atom] for atom in atoms if atom & TERM_BITS[term]]
                  for term in TERMS})
    return model


def satisfies_policy(support: int, policy: Policy | str) -> bool:
    atoms = occupied_atoms(support)
    required = REQUIRED_NONEMPTY[_policy(policy)]
    return all(any(atom & TERM_BITS[term] for atom in atoms) for term in required)


@lru_cache(maxsize=None)
def _ordered_supports(policy: Policy) -> tuple[int, ...]:
    # Cardinality first makes the first countermodel globally smallest by size.
    return tuple(sorted((mask for mask in range(1, 256)
                         if satisfies_policy(mask, policy)),
                        key=lambda mask: (mask.bit_count(), mask)))


def iter_supports(policy: Policy | str = Policy.ALLOW_EMPTY) -> Iterator[int]:
    """All eligible supports, ordered by (universe size, numeric support mask)."""
    return iter(_ordered_supports(_policy(policy)))


@dataclass(frozen=True)
class Clause:
    quantifier: str
    subject: str
    predicate: str

    def __post_init__(self) -> None:
        _quantifier(self.quantifier)
        _term(self.subject)
        _term(self.predicate)

    def holds(self, support: int) -> bool:
        return holds(support, self.quantifier, self.subject, self.predicate)

    def __str__(self) -> str:
        return f"{self.quantifier}({self.subject},{self.predicate})"


@dataclass(frozen=True)
class Entailment:
    premises: tuple[Clause, ...]
    conclusion: Clause
    policy: Policy
    eligible_support_count: int
    premise_support_count: int
    countermodel_support: int | None

    @property
    def valid(self) -> bool:
        return self.countermodel_support is None

    @property
    def vacuous(self) -> bool:
        return self.premise_support_count == 0

    def as_dict(self) -> dict:
        witness = self.countermodel_support
        return {
            "premises": [str(clause) for clause in self.premises],
            "conclusion": str(self.conclusion),
            "policy": self.policy.value,
            "eligible_support_count": self.eligible_support_count,
            "premise_support_count": self.premise_support_count,
            "valid": self.valid,
            "vacuous": self.vacuous,
            "countermodel_support": witness,
            "countermodel_atoms": list(occupied_atoms(witness)) if witness is not None else None,
            "countermodel_size": witness.bit_count() if witness is not None else None,
            "countermodel": concrete_model(witness) if witness is not None else None,
        }


def classify(premises: Iterable[Clause], conclusion: Clause,
             policy: Policy | str = Policy.ALLOW_EMPTY) -> Entailment:
    """Classify a finite conjunction's entailment; explicitly flag vacuous cases."""
    premise_tuple = tuple(premises)
    if any(not isinstance(clause, Clause) for clause in premise_tuple):
        raise TypeError("premises must contain only Clause objects")
    if not isinstance(conclusion, Clause):
        raise TypeError("conclusion must be a Clause")
    chosen_policy = _policy(policy)
    supports = _ordered_supports(chosen_policy)
    premise_count = 0
    witness = None
    for support in supports:
        if all(clause.holds(support) for clause in premise_tuple):
            premise_count += 1
            if witness is None and not conclusion.holds(support):
                witness = support
    return Entailment(premise_tuple, conclusion, chosen_policy,
                      len(supports), premise_count, witness)


def classify_mood(mood: str, policy: Policy | str = Policy.ALLOW_EMPTY) -> Entailment:
    """QRT means Q(P,M), R(S,M), therefore T(S,P); direction is fixed."""
    if not isinstance(mood, str):
        raise TypeError("mood must be a string")
    if len(mood) != 3 or any(letter not in QUANTIFIERS for letter in mood):
        raise ValueError("mood must have exactly three uppercase letters from AEIO")
    q, r, t = mood
    return classify((Clause(q, "P", "M"), Clause(r, "S", "M")),
                    Clause(t, "S", "P"), policy)


def all_moods() -> tuple[str, ...]:
    return tuple("".join(mood) for mood in product(QUANTIFIERS, repeat=3))


def make_report() -> dict:
    """Two principal policies plus the diagnostic S-only existence policy."""
    policies = {}
    for policy in Policy:
        rows = {mood: classify_mood(mood, policy).as_dict() for mood in all_moods()}
        policies[policy.value] = {
            "support_count": len(_ordered_supports(policy)),
            "valid_moods": [mood for mood, row in rows.items() if row["valid"]],
            "results": rows,
        }
    reversed_ie = {}
    for policy in Policy:
        premises = (Clause("I", "P", "M"), Clause("E", "S", "M"))
        reversed_ie[policy.value] = {
            "forward_O_S_P": classify(premises, Clause("O", "S", "P"), policy).as_dict(),
            "reverse_O_P_S": classify(premises, Clause("O", "P", "S"), policy).as_dict(),
        }
    return {
        "semantics": {"A": "X subseteq Y", "E": "X intersection Y is empty",
                      "I": "X intersection Y is nonempty", "O": "X minus Y is nonempty"},
        "premise_order": "Q(P,M), R(S,M)",
        "conclusion_order": "T(S,P)",
        "universe": "nonempty; one representative per occupied Boolean type",
        "atom_encoding": "P=4, M=2, S=1; support bit a marks occupied atom a",
        "countermodel_order": "minimum cardinality, then minimum numeric support mask",
        "policies": policies,
        "reversal_check_IE": reversed_ie,
    }


def render_markdown(report: dict) -> str:
    lines = ["# Generated model results", "",
             "Modern AEIO set semantics; premises **Q(P,M), R(S,M)** and conclusion **T(S,P)**.",
             "The universe is always nonempty. A and E have no built-in existential import.",
             "`V` = valid; `× n [a,…]` = invalid, with smallest countermodel size n and occupied atoms.",
             "Atoms use membership bits P=4, M=2, S=1. Full concrete named models are in `report.json`.", ""]
    for name, policy in report["policies"].items():
        lines.extend([f"## {name}", "", f"Eligible supports: **{policy['support_count']}**. "
                      f"Valid moods: **{', '.join(policy['valid_moods'])}**.", "",
                      "| Premises Q,R | A(S,P) | E(S,P) | I(S,P) | O(S,P) | Premise supports |",
                      "|---|---|---|---|---|---:|"])
        for q, r in product(QUANTIFIERS, repeat=2):
            cells = []
            for t in QUANTIFIERS:
                result = policy["results"][q+r+t]
                atoms = ",".join(map(str, result["countermodel_atoms"] or []))
                cells.append("V" if result["valid"] else f"× {result['countermodel_size']} [{atoms}]")
            n = policy["results"][q+r+"A"]["premise_support_count"]
            lines.append(f"| {q}{r} | " + " | ".join(cells) + f" | {n} |")
        lines.append("")
    lines.extend(["## Direction matters: IE", "",
                  "I(P,M), E(S,M) entails **O(P,S)** under all three policies, "
                  "but does **not** entail O(S,P), the fixed second-figure conclusion direction.", "",
                  "## Scope of the result", "",
                  "The program exhausts finite Boolean supports, not arbitrary domain cardinalities. "
                  "The separate support-compression argument in WALKTHROUGH.md explains why those "
                  "supports suffice for this particular three-unary-predicate AEIO language. "
                  "Tests do not establish the historical fidelity of the chosen modern semantics.", ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="write the full machine-readable report here")
    parser.add_argument("--markdown", type=Path, help="write the readable classification table here")
    args = parser.parse_args(argv)
    report = make_report()
    if args.json:
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    markdown = render_markdown(report)
    if args.markdown:
        args.markdown.write_text(markdown, encoding="utf-8")
    if not args.json and not args.markdown:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
