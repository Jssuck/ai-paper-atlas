"""Finite, complete region semantics for the supplied Letter CIII forms.

Only Python's standard library is used.  See PROOF.md for the reduction from
arbitrary nonempty universes to this finite model space and for its limits.
"""

from dataclasses import dataclass
from itertools import permutations, product
from typing import Dict, Iterable, Mapping, Sequence, Tuple


TERMS = ("A", "B", "C")
TERM_BITS = {"A": 1, "B": 2, "C": 4}
KINDS = ("A", "E", "I", "O")
REGIMES = ("empty_terms_allowed", "all_terms_nonempty", "A_nonempty_only")


def regions_containing(term: str) -> int:
    """The eight-bit mask of membership types that contain this term."""
    return sum(1 << region for region in range(8) if region & TERM_BITS[term])


TERM_REGIONS = {term: regions_containing(term) for term in TERMS}


@dataclass(frozen=True)
class Statement:
    kind: str
    subject: str
    predicate: str

    def __post_init__(self) -> None:
        if self.kind not in KINDS:
            raise ValueError("The categorical kind must be A, E, I, or O.")
        if self.subject not in TERMS or self.predicate not in TERMS:
            raise ValueError("Terms must be A, B, or C.")

    def __str__(self) -> str:
        return f"{self.kind}({self.subject},{self.predicate})"

    def converse(self) -> "Statement":
        return Statement(self.kind, self.predicate, self.subject)

    def renamed(self, mapping: Mapping[str, str]) -> "Statement":
        return Statement(self.kind, mapping[self.subject], mapping[self.predicate])

    def canonical(self) -> Tuple[str, str, str]:
        """Identify only the unconditional simple conversions E and I."""
        if self.kind in ("E", "I"):
            left, right = sorted((self.subject, self.predicate))
            return (self.kind, left, right)
        return (self.kind, self.subject, self.predicate)


@dataclass(frozen=True)
class RegionModel:
    """One witness per occupied membership type.

    ``raw_mask`` ranges over 0..255.  Raw zero gets an outside witness (type 0),
    so that the interpreted universe is never empty.  Thus raw masks 0 and 1
    denote the same model, an intentional, explicitly reported duplication.
    """

    raw_mask: int

    def __post_init__(self) -> None:
        if type(self.raw_mask) is not int or not 0 <= self.raw_mask <= 255:
            raise ValueError("An occupancy mask must be an integer in 0..255.")

    @property
    def occupied_mask(self) -> int:
        return self.raw_mask if self.raw_mask else 1

    @property
    def region_types(self) -> Tuple[int, ...]:
        return tuple(i for i in range(8) if self.occupied_mask & (1 << i))

    def term_nonempty(self, term: str) -> bool:
        return bool(self.occupied_mask & TERM_REGIONS[term])

    def satisfies_regime(self, regime: str) -> bool:
        if regime == "empty_terms_allowed":
            return True
        if regime == "all_terms_nonempty":
            return all(self.term_nonempty(term) for term in TERMS)
        if regime == "A_nonempty_only":
            return self.term_nonempty("A")
        raise ValueError(f"Unknown assumption regime: {regime}")

    def evaluate(self, statement: Statement) -> bool:
        subject = TERM_REGIONS[statement.subject]
        predicate = TERM_REGIONS[statement.predicate]
        intersection = self.occupied_mask & subject & predicate
        difference = self.occupied_mask & subject & (~predicate & 255)
        if statement.kind == "A":
            return difference == 0
        if statement.kind == "E":
            return intersection == 0
        if statement.kind == "I":
            return intersection != 0
        return difference != 0

    def as_sets(self) -> Dict[str, object]:
        labels = {region: f"w{region}" for region in self.region_types}
        return {
            "raw_mask": self.raw_mask,
            "occupied_mask": self.occupied_mask,
            "outside_witness_added": self.raw_mask == 0,
            "region_types": list(self.region_types),
            "universe": list(labels.values()),
            "terms": {
                term: [labels[r] for r in self.region_types if r & TERM_BITS[term]]
                for term in TERMS
            },
        }


@dataclass(frozen=True)
class Argument:
    label: str
    premises: Tuple[Statement, ...]
    conclusion: Statement
    note: str = ""

    def __str__(self) -> str:
        return " & ".join(map(str, self.premises)) + " => " + str(self.conclusion)

    def holds_in(self, model: RegionModel) -> bool:
        return not all(model.evaluate(p) for p in self.premises) or model.evaluate(
            self.conclusion
        )

    def signature(self, unordered_premises: bool = False) -> Tuple[object, ...]:
        premises = tuple(p.canonical() for p in self.premises)
        if unordered_premises:
            premises = tuple(sorted(premises))
        return (premises, self.conclusion.canonical())

    def renamed(self, mapping: Mapping[str, str]) -> "Argument":
        return Argument(
            self.label,
            tuple(p.renamed(mapping) for p in self.premises),
            self.conclusion.renamed(mapping),
            self.note,
        )


def s(kind: str, subject: str, predicate: str) -> Statement:
    return Statement(kind, subject, predicate)


CATALOG = (
    Argument("A1", (s("A", "A", "B"), s("A", "C", "A")), s("A", "C", "B")),
    Argument("A2", (s("A", "A", "B"), s("I", "C", "A")), s("I", "C", "B")),
    Argument("A3", (s("A", "A", "B"), s("E", "C", "B")), s("E", "C", "A")),
    Argument("A4", (s("A", "A", "B"), s("O", "C", "B")), s("O", "C", "A")),
    Argument(
        "A5", (s("A", "A", "B"), s("A", "B", "C")), s("I", "C", "A"),
        "Valid exactly when A is nonempty under these premises; A existence suffices.",
    ),
    Argument("E1", (s("E", "A", "B"), s("A", "C", "B")), s("E", "C", "A")),
    Argument("E2", (s("E", "A", "B"), s("A", "C", "A")), s("E", "C", "B")),
    Argument("E3", (s("E", "A", "B"), s("I", "C", "A")), s("O", "C", "B")),
    Argument("E4", (s("E", "A", "B"), s("I", "C", "B")), s("O", "C", "A")),
)


def models(regime: str = "empty_terms_allowed") -> Tuple[RegionModel, ...]:
    if regime not in REGIMES:
        raise ValueError(f"Unknown assumption regime: {regime}")
    return tuple(m for m in (RegionModel(i) for i in range(256)) if m.satisfies_regime(regime))


def check_argument(argument: Argument, regime: str) -> Dict[str, object]:
    selected = models(regime)
    premise_models = tuple(
        m for m in selected if all(m.evaluate(p) for p in argument.premises)
    )
    failures = tuple(m for m in premise_models if not m.evaluate(argument.conclusion))
    return {
        "label": argument.label,
        "formula": str(argument),
        "regime": regime,
        "valid": not failures,
        "tested_raw_masks": len(selected),
        "distinct_nonempty_universe_models": len({m.occupied_mask for m in selected}),
        "premise_satisfying_raw_masks": len(premise_models),
        "distinct_premise_satisfying_models": len({m.occupied_mask for m in premise_models}),
        "premises_satisfiable": bool(premise_models),
        "counterexample_raw_masks": [m.raw_mask for m in failures],
        "distinct_counterexample_models": len({m.occupied_mask for m in failures}),
        "first_counterexample": failures[0].as_sets() if failures else None,
    }


def ei_conversion_variants(argument: Argument) -> Tuple[Argument, ...]:
    """Explicitly reverse any E or I premise/conclusion, never A or O."""
    statements = argument.premises + (argument.conclusion,)
    choices = [(p, p.converse()) if p.kind in ("E", "I") else (p,) for p in statements]
    variants = []
    seen = set()
    for index, variant in enumerate(product(*choices), start=1):
        key = tuple(str(p) for p in variant)
        if key not in seen:
            seen.add(key)
            variants.append(Argument(f"{argument.label}.v{index}", variant[:-1], variant[-1]))
    return tuple(variants)


def catalog_matches(argument: Argument, unordered_premises: bool = False) -> Tuple[str, ...]:
    """Match modulo bijective renaming and E/I simple conversion only.

    The separate unordered mode ALSO permits exchanging premise order.  Neither
    mode adds subalternation, contraposition, weakening, or derived rule chaining.
    These syntactic matches are not a historical theory of Euler's 'forms'.
    """
    target = argument.signature(unordered_premises)
    matches = []
    for displayed in CATALOG:
        if any(
            displayed.renamed(dict(zip(TERMS, permutation))).signature(unordered_premises) == target
            for permutation in permutations(TERMS)
        ):
            matches.append(displayed.label)
    return tuple(matches)


def fixed_first_candidates(first_kind: str) -> Tuple[Argument, ...]:
    """128 ordered candidates: 16 second premises x 8 endpoint conclusions.

    Fix A(A,B) or E(A,B).  The second premise connects C with A or B,
    in either direction and any categorical kind.  The conclusion connects C
    with the OTHER endpoint of the first premise, in either direction and any
    categorical kind.  No reflexive terms or repeated first-premise relations.
    """
    if first_kind not in ("A", "E"):
        raise ValueError("The fixed first premise must be A(A,B) or E(A,B).")
    candidates = []
    for shared in ("A", "B"):
        other = "B" if shared == "A" else "A"
        for left, right in (("C", shared), (shared, "C")):
            for second_kind in KINDS:
                for end_left, end_right in (("C", other), (other, "C")):
                    for conclusion_kind in KINDS:
                        label = f"{first_kind}-fixed-{len(candidates) + 1:03d}"
                        candidates.append(Argument(
                            label,
                            (s(first_kind, "A", "B"), s(second_kind, left, right)),
                            s(conclusion_kind, end_left, end_right),
                        ))
    return tuple(candidates)


def audit_fixed_first(first_kind: str, regime: str) -> Dict[str, object]:
    candidates = fixed_first_candidates(first_kind)
    rows = []
    for candidate in candidates:
        row = check_argument(candidate, regime)
        row["displayed_matches_ordered"] = list(catalog_matches(candidate))
        row["displayed_matches_unordered"] = list(catalog_matches(candidate, True))
        rows.append(row)
    valid_pairs = [(candidate, row) for candidate, row in zip(candidates, rows) if row["valid"]]
    valid = [row for _, row in valid_pairs]
    distinct_conversion_classes = {a.signature() for a, _ in valid_pairs}
    return {
        "first_premise": str(s(first_kind, "A", "B")),
        "regime": regime,
        "candidate_count": len(candidates),
        "valid_ordered_candidates": len(valid),
        "valid_classes_modulo_E_I_conversion_only": len(distinct_conversion_classes),
        "valid_candidates_matching_displayed_ordered": sum(bool(r["displayed_matches_ordered"]) for r in valid),
        "valid_candidates_matching_displayed_unordered": sum(bool(r["displayed_matches_unordered"]) for r in valid),
        "additional_valid_candidates_ordered": [r["formula"] for r in valid if not r["displayed_matches_ordered"]],
        "additional_valid_candidates_unordered": [r["formula"] for r in valid if not r["displayed_matches_unordered"]],
        "rows": rows,
    }


def evaluate_sets(statement: Statement, terms: Mapping[str, Iterable[str]]) -> bool:
    """A transparent set implementation for named examples and cross-checks."""
    left, right = set(terms[statement.subject]), set(terms[statement.predicate])
    if statement.kind == "A":
        return left <= right
    if statement.kind == "E":
        return left.isdisjoint(right)
    if statement.kind == "I":
        return bool(left & right)
    return bool(left - right)


def mask_for_sets(universe: Iterable[str], terms: Mapping[str, Iterable[str]]) -> int:
    universe_set = set(universe)
    if not universe_set:
        raise ValueError("The supplied named universe must be nonempty.")
    term_sets = {term: set(terms[term]) for term in TERMS}
    if any(not value <= universe_set for value in term_sets.values()):
        raise ValueError("Every term must be a subset of the universe.")
    mask = 0
    for witness in universe_set:
        region = sum(TERM_BITS[term] for term in TERMS if witness in term_sets[term])
        mask |= 1 << region
    return mask


def named_example(name: str, universe: Sequence[str], terms: Mapping[str, Sequence[str]],
                  premises: Sequence[Statement], conclusion: Statement = None) -> Dict[str, object]:
    mask = mask_for_sets(universe, terms)
    result = {
        "name": name,
        "universe": list(universe),
        "terms": {term: list(terms[term]) for term in TERMS},
        "occupancy_mask": mask,
        "premises": [str(p) for p in premises],
        "all_premises_true": all(evaluate_sets(p, terms) for p in premises),
    }
    if conclusion is not None:
        result["conclusion"] = str(conclusion)
        result["conclusion_true"] = evaluate_sets(conclusion, terms)
    return result


def explicit_examples() -> Dict[str, object]:
    disjoint_premises = (s("A", "A", "B"), s("E", "C", "A"))
    cases = []
    for name, c in (
        ("C disjoint from B", ["c"]),
        ("C wholly in B", ["b"]),
        ("C partially overlaps B", ["b", "c"]),
    ):
        terms = {"A": ["a"], "B": ["a", "b"], "C": c}
        example = named_example(name, ["a", "b", "c"], terms, disjoint_premises)
        example["C_to_B_relations"] = {
            kind: evaluate_sets(s(kind, "C", "B"), terms) for kind in KINDS
        }
        cases.append(example)
    return {
        "no_inference_from_A_subset_B_and_C_disjoint_A": cases,
        "A5_empty_A_counterexample": named_example(
            "A5 fails with A empty even when B and C are nonempty",
            ["b"], {"A": [], "B": ["b"], "C": ["b"]},
            CATALOG[4].premises, CATALOG[4].conclusion,
        ),
        "I_does_not_imply_O": named_example(
            "One shared witness, no witness in A minus B",
            ["p"], {"A": ["p"], "B": ["p"], "C": ["p"]},
            (s("I", "A", "B"),), s("O", "A", "B"),
        ),
        "pear_tree_equality_counterexample": named_example(
            "A=trees, B=pear trees; inclusion and some pears allow equality",
            ["pear"], {"A": ["pear"], "B": ["pear"], "C": []},
            (s("A", "B", "A"), s("I", "A", "B")), s("O", "A", "B"),
        ),
        "pear_tree_strict_inclusion_example": named_example(
            "A=trees, B=pear trees; the extra non-pear tree supplies strictness",
            ["pear", "oak"], {"A": ["pear", "oak"], "B": ["pear"], "C": []},
            (s("A", "B", "A"), s("O", "A", "B")), s("O", "A", "B"),
        ),
        "common_subject_empty_A_counterexample": named_example(
            "A(A,B) and A(A,C) do not ensure I(C,B) when A is empty",
            ["b", "c"], {"A": [], "B": ["b"], "C": ["c"]},
            (s("A", "A", "B"), s("A", "A", "C")), s("I", "C", "B"),
        ),
    }
