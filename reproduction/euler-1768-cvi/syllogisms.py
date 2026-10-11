#!/usr/bin/env python3
"""Original, dependency-free finite-support teaching reconstruction of Lettre CVI.

Modern Boolean class semantics; universal propositions carry no existential import.
The transcribed 19-item list is source data, not an input to validity enumeration.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path
import platform
import sys
from typing import Iterable

TERMS = ("P", "Q", "M")
MOODS = ("A", "E", "I", "O")
TERM_BITS = {"P": 4, "Q": 2, "M": 1}
TERM_MASKS = {term: sum(1 << atom for atom in range(8) if atom & bit)
              for term, bit in TERM_BITS.items()}
FIGURES = {
    1: (("M", "Q"), ("P", "M")),
    2: (("Q", "M"), ("P", "M")),
    3: (("M", "Q"), ("M", "P")),
    4: (("Q", "M"), ("M", "P")),
}
# Verified directly against printed pp. 131–133, in Euler's order.
EULER_LIST = {
    1: ("AAA", "AII", "EAE", "EIO"),
    2: ("AEE", "AOO", "EAE", "EIO"),
    3: ("AAI", "IAI", "AII", "EAO", "EIO", "OAO"),
    4: ("AAI", "IAI", "AEE", "EAO", "EIO"),
}


def validate_figure(figure: int) -> int:
    if type(figure) is not int or figure not in FIGURES:
        raise ValueError("figure must be an integer from 1 to 4")
    return figure


def validate_mood(mood: str, length: int = 3) -> str:
    if not isinstance(mood, str) or len(mood) != length or any(c not in MOODS for c in mood):
        raise ValueError(f"mood must contain exactly {length} uppercase A/E/I/O letters")
    return mood


def validate_term(term: str) -> str:
    if not isinstance(term, str) or term not in TERMS:
        raise ValueError("term must be P, Q, or M")
    return term


def normalize_assumptions(assumptions: Iterable[str]) -> tuple[str, ...]:
    if isinstance(assumptions, (str, bytes)):
        raise ValueError("existence assumptions must be an iterable of term names, not a string")
    try:
        items = tuple(assumptions)
    except TypeError as exc:
        raise ValueError("existence assumptions must be an iterable of term names") from exc
    for item in items:
        validate_term(item)
    if len(items) != len(set(items)):
        raise ValueError("existence assumptions must not repeat terms")
    return tuple(term for term in TERMS if term in items)


@dataclass(frozen=True)
class Model:
    """One object per occupied P,Q,M membership atom; bit i marks atom i."""
    support: int

    def __post_init__(self) -> None:
        if type(self.support) is not int or not 1 <= self.support <= 255:
            raise ValueError("support must be an integer from 1 to 255 (nonempty domain)")

    def nonempty(self, term: str) -> bool:
        return bool(self.support & TERM_MASKS[validate_term(term)])

    def holds(self, mood: str, subject: str, predicate: str) -> bool:
        validate_mood(mood, 1)
        subject_mask = TERM_MASKS[validate_term(subject)]
        predicate_mask = TERM_MASKS[validate_term(predicate)]
        intersection = self.support & subject_mask & predicate_mask
        difference = self.support & subject_mask & (~predicate_mask & 255)
        return {"A": difference == 0, "E": intersection == 0,
                "I": intersection != 0, "O": difference != 0}[mood]

    def as_dict(self) -> dict:
        atoms = [atom for atom in range(8) if self.support & (1 << atom)]
        labels = {atom: f"x{index}" for index, atom in enumerate(atoms, 1)}
        return {
            "support": self.support,
            "atoms_PQM": [f"{atom:03b}" for atom in atoms],
            "domain": [labels[atom] for atom in atoms],
            "classes": {term: [labels[atom] for atom in atoms if atom & TERM_BITS[term]]
                        for term in TERMS},
        }


# All nonempty supports, ordered by cardinality and then support integer so that
# returned countermodels have the smallest possible number of objects.
MODELS = tuple(sorted((Model(s) for s in range(1, 256)),
                      key=lambda model: (model.support.bit_count(), model.support)))


def models_with(assumptions: Iterable[str] = ()) -> tuple[Model, ...]:
    required = normalize_assumptions(assumptions)
    return tuple(m for m in MODELS if all(m.nonempty(term) for term in required))


@lru_cache(maxsize=None)
def _premise_models(figure: int, premises: str,
                    assumptions: tuple[str, ...]) -> tuple[Model, ...]:
    major, minor = FIGURES[figure]
    return tuple(model for model in models_with(assumptions)
                 if model.holds(premises[0], *major)
                 and model.holds(premises[1], *minor))


def premise_models(figure: int, premises: str,
                   assumptions: Iterable[str] = ()) -> tuple[Model, ...]:
    return _premise_models(validate_figure(figure), validate_mood(premises, 2),
                           normalize_assumptions(assumptions))


def check_form(figure: int, mood: str, assumptions: Iterable[str] = ()) -> dict:
    validate_figure(figure)
    validate_mood(mood)
    required = normalize_assumptions(assumptions)
    candidates = premise_models(figure, mood[:2], required)
    countermodels = [model for model in candidates if not model.holds(mood[2], "P", "Q")]
    return {
        "figure": figure,
        "mood": mood,
        "existence_assumptions": list(required),
        "supports_in_regime": len(models_with(required)),
        "premises_satisfiable": bool(candidates),
        "premise_models": len(candidates),
        "valid": not countermodels,
        "countermodel_count": len(countermodels),
        "countermodel": countermodels[0].as_dict() if countermodels else None,
    }


def all_assumptions() -> tuple[tuple[str, ...], ...]:
    return tuple(group for size in range(4) for group in combinations(TERMS, size))


def minimal_existence_assumptions(figure: int, mood: str) -> list[list[str]]:
    """All inclusion-minimal sufficient conjunctions of P/Q/M nonemptiness.

    [] means none of these assumption combinations can make this form valid.
    [[]] means valid with no additional existence assumption.
    """
    validate_figure(figure)
    validate_mood(mood)
    minima: list[tuple[str, ...]] = []
    for assumption in all_assumptions():
        if any(set(old) <= set(assumption) for old in minima):
            continue
        result = check_form(figure, mood, assumption)
        if result["valid"]:
            minima.append(assumption)
    return [list(minimum) for minimum in minima]


def all_forms() -> tuple[tuple[int, str], ...]:
    return tuple((figure, "".join(mood)) for figure in FIGURES
                 for mood in product(MOODS, repeat=3))


def valid_forms(assumptions: Iterable[str] = ()) -> list[tuple[int, str]]:
    required = normalize_assumptions(assumptions)
    return [(figure, mood) for figure, mood in all_forms()
            if check_form(figure, mood, required)["valid"]]


def strictly_implies(stronger: str, weaker: str, assumptions: Iterable[str] = ()) -> bool:
    """Strict implication between conclusion types in a regime, NOT under premises.

    Comparing only inside premise models would make every valid conclusion
    equivalent. This definition correctly captures A => I and E => O when P exists.
    """
    validate_mood(stronger, 1)
    validate_mood(weaker, 1)
    models = models_with(assumptions)
    implies = all(not m.holds(stronger, "P", "Q") or m.holds(weaker, "P", "Q")
                  for m in models)
    reverse_fails = any(m.holds(weaker, "P", "Q") and not m.holds(stronger, "P", "Q")
                        for m in models)
    return implies and reverse_fails


def nonweakened_valid_forms(assumptions: Iterable[str] = ()) -> list[tuple[int, str]]:
    """Retain valid conclusions not strictly weaker than another valid conclusion
    for the SAME figure and ordered pair of premise types.
    """
    required = normalize_assumptions(assumptions)
    valid = valid_forms(required)
    valid_set = set(valid)
    return [(figure, mood) for figure, mood in valid
            if not any((figure, mood[:2] + alternative) in valid_set
                       and strictly_implies(alternative, mood[2], required)
                       for alternative in MOODS)]


def form_id(figure: int, mood: str) -> str:
    return f"{figure}-{mood}"


def equivocation_example() -> dict:
    """Four real terms hidden behind a repeated ambiguous middle-term word.

    All financial banks are institutions; all river-bank edges are geographic
    banks; therefore all river-bank edges are institutions. The two occurrences
    of 'bank' denote M1 and M2, not one middle term. Objects are abstract tokens.
    """
    domain = {"a", "b"}
    financial_banks, geographic_banks = {"a"}, {"b"}
    institutions, river_bank_edges = {"a"}, {"b"}
    return {
        "domain": sorted(domain),
        "P_river_bank_edges": sorted(river_bank_edges),
        "Q_institutions": sorted(institutions),
        "M1_financial_banks": sorted(financial_banks),
        "M2_geographic_banks": sorted(geographic_banks),
        "major_M1_subset_Q": financial_banks <= institutions,
        "minor_P_subset_M2": river_bank_edges <= geographic_banks,
        "claimed_conclusion_P_subset_Q": river_bank_edges <= institutions,
        "same_middle_term": financial_banks == geographic_banks,
    }


def build_report() -> dict:
    unrestricted = valid_forms()
    all_nonempty = valid_forms(TERMS)
    nonweakened = nonweakened_valid_forms(TERMS)
    listed = [(figure, mood) for figure, moods in EULER_LIST.items() for mood in moods]
    details = []
    for figure, mood in all_forms():
        details.append({
            "id": form_id(figure, mood),
            "listed_by_euler": (figure, mood) in listed,
            "no_term_existence": check_form(figure, mood),
            "all_terms_nonempty": check_form(figure, mood, TERMS),
            "minimal_existence_assumptions": minimal_existence_assumptions(figure, mood),
        })
    regime_summaries = [{
        "existence_assumptions": list(required),
        "supports": len(models_with(required)),
        "valid_count": len(valid_forms(required)),
        "valid_forms": [form_id(*form) for form in valid_forms(required)],
    } for required in all_assumptions()]
    source_listing = [{
        "id": form_id(figure, mood),
        "source_printed_page": 131 if figure <= 2 else (132 if figure == 3 else 133),
        "minimal_existence_assumptions": minimal_existence_assumptions(figure, mood),
        "without_existence": check_form(figure, mood),
    } for figure, mood in listed]
    conditional_cases = []
    for item in source_listing:
        if item["without_existence"]["valid"]:
            continue
        figure = item["without_existence"]["figure"]
        mood = item["without_existence"]["mood"]
        missing_term = item["minimal_existence_assumptions"][0][0]
        other_terms = [term for term in TERMS if term != missing_term]
        conditional_cases.append({
            **item,
            "counterexample_even_when_other_terms_nonempty": check_form(figure, mood, other_terms),
            "sufficient_condition_check": check_form(figure, mood, [missing_term]),
        })
    return {
        "schema_version": 1,
        "description": "Original modern finite-support reconstruction; not Euler's program or original algorithm.",
        "semantics": {
            "domain_nonempty": True,
            "universal_propositions_have_existential_import": False,
            "term_roles": {"P": "conclusion subject", "Q": "conclusion predicate", "M": "middle term"},
            "atom_bit_order": "PQM; atom index = 4*P + 2*Q + M; support bit i marks atom i",
            "minimal_assumptions_scope": "Conjunctions of whole-class P/Q/M nonemptiness only; inclusion-minimal",
            "dominance_scope": "Strict implication over all regime models, with identical figure and premises",
        },
        "summary": {
            "supports_nonempty_domain": len(MODELS),
            "supports_all_terms_nonempty": len(models_with(TERMS)),
            "forms_examined": len(all_forms()),
            "listed_count": len(listed),
            "valid_without_term_existence": len(unrestricted),
            "valid_with_all_terms_nonempty": len(all_nonempty),
            "nonweakened_valid_with_all_terms_nonempty": len(nonweakened),
            "nonweakened_set_equals_euler_list": set(nonweakened) == set(listed),
            "all_premise_pairs_satisfiable_with_all_terms_nonempty": all(
                premise_models(figure, a + b, TERMS) for figure in FIGURES for a in MOODS for b in MOODS),
        },
        "all_eight_existence_regimes": regime_summaries,
        "alternative_Q_M_background_equals_euler_list": set(valid_forms(["Q", "M"])) == set(listed),
        "source_listing_in_original_order": source_listing,
        "valid_without_term_existence": [form_id(*form) for form in unrestricted],
        "valid_with_all_terms_nonempty": [form_id(*form) for form in all_nonempty],
        "nonweakened_valid_with_all_terms_nonempty": [form_id(*form) for form in nonweakened],
        "weakened_extras": [form_id(*form) for form in all_nonempty if form not in nonweakened],
        "conditional_listed_forms": conditional_cases,
        "all_256_forms": details,
        "four_term_equivocation": equivocation_example(),
    }


def write_json(path: Path, content: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    report_parser = sub.add_parser("report", help="Exhaustively analyze 4 × 4³ = 256 forms")
    report_parser.add_argument("--output", type=Path, default=Path("results/report.json"))
    query = sub.add_parser("query", help="Check any one figure and three-letter mood")
    query.add_argument("figure", type=int, choices=tuple(FIGURES))
    query.add_argument("mood", type=lambda value: validate_mood(value))
    query.add_argument("--exists", nargs="*", choices=TERMS, default=[])
    sub.add_parser("environment", help="Print observed runtime; no package installation needed")
    args = parser.parse_args(argv)
    if args.command == "environment":
        print(json.dumps({"python": sys.version, "implementation": platform.python_implementation(),
                          "platform": platform.platform(), "dependencies": "Python standard library only"},
                         ensure_ascii=False, indent=2))
    elif args.command == "query":
        try:
            result = check_form(args.figure, args.mood, args.exists)
        except ValueError as exc:
            parser.error(str(exc))
        result["minimal_existence_assumptions"] = minimal_existence_assumptions(args.figure, args.mood)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        report = build_report()
        write_json(args.output, report)
        print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
        print("Weakened extras: " + ", ".join(report["weakened_extras"]))
        print(f"Full report written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
