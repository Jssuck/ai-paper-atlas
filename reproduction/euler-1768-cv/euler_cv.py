#!/usr/bin/env python3
"""A modern, finite-set teaching reconstruction of Euler's Letter CV.

No dependencies outside the Python standard library. This is new teaching code,
not historical code or a simulation of an algorithm that Euler implemented.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from typing import Iterable


TERMS = ("A", "B", "C")
TERM_BITS = {"A": 1, "B": 2, "C": 4}


@dataclass(frozen=True)
class Model:
    """A nonempty finite universe with three possibly empty named subsets.

    Element names are strings; their spelling has no logical significance.
    Inputs are frozen so a model cannot change after its creation.
    """

    universe: frozenset[str]
    a: frozenset[str]
    b: frozenset[str]
    c: frozenset[str]

    def __post_init__(self) -> None:
        for field in ("universe", "a", "b", "c"):
            object.__setattr__(self, field, frozenset(getattr(self, field)))
        if not self.universe:
            raise ValueError("The universe must be nonempty.")
        if any(not isinstance(x, str) for x in self.universe):
            raise TypeError("Use string labels for universe elements.")
        if any(not subset <= self.universe for subset in (self.a, self.b, self.c)):
            raise ValueError("Every named class must be a subset of the universe.")

    def term(self, name: str) -> frozenset[str]:
        if name not in TERMS:
            raise ValueError(f"Unknown term: {name!r}")
        return getattr(self, name.lower())

    def atom(self, element: str) -> int:
        """Return the type index: bit 0=A, bit 1=B, bit 2=C."""
        if element not in self.universe:
            raise ValueError("The element is not in this universe.")
        return sum(TERM_BITS[name] for name in TERMS if element in self.term(name))

    def support(self) -> int:
        """One support bit per occupied type, including outside type 0."""
        return sum(1 << atom for atom in {self.atom(x) for x in self.universe})

    def all_classes_nonempty(self) -> bool:
        return bool(self.a and self.b and self.c)

    def as_dict(self) -> dict:
        return {
            "U": sorted(self.universe),
            **{name: sorted(self.term(name)) for name in TERMS},
            "support": self.support(),
            "occupied_types": [i for i in range(8) if self.support() & (1 << i)],
        }


def from_support(support: int) -> Model:
    """Realize each occupied type once. Never add an extra outside witness."""
    if type(support) is not int or not 1 <= support <= 255:
        raise ValueError("A nonempty support must be an integer from 1 through 255.")
    atoms = [i for i in range(8) if support & (1 << i)]
    universe = frozenset(f"t{i}" for i in atoms)
    subsets = [frozenset(f"t{i}" for i in atoms if i & TERM_BITS[name]) for name in TERMS]
    return Model(universe, *subsets)


def representatives(model: Model) -> dict[str, str]:
    """Map every original element to its type's element in from_support()."""
    return {x: f"t{model.atom(x)}" for x in model.universe}


def models(all_classes_nonempty: bool = False) -> Iterable[Model]:
    """Enumerate support models, not all finite labeled set structures."""
    for support in range(1, 256):
        model = from_support(support)
        if not all_classes_nonempty or model.all_classes_nonempty():
            yield model


@dataclass(frozen=True)
class Proposition:
    """Modern AEIO semantics; universal claims have no existential import."""

    kind: str
    subject: str
    predicate: str

    def __post_init__(self) -> None:
        if self.kind not in ("A", "E", "I", "O"):
            raise ValueError("Proposition kind must be A, E, I, or O.")
        if self.subject not in TERMS or self.predicate not in TERMS:
            raise ValueError("Proposition terms must be A, B, or C.")

    def holds(self, model: Model) -> bool:
        subject, predicate = model.term(self.subject), model.term(self.predicate)
        if self.kind == "A":
            return subject <= predicate
        if self.kind == "E":
            return subject.isdisjoint(predicate)
        if self.kind == "I":
            return bool(subject & predicate)
        return bool(subject - predicate)

    def witnesses(self, model: Model) -> frozenset[str]:
        """Witnesses for existential claims only, not universal 'witnesses'."""
        subject, predicate = model.term(self.subject), model.term(self.predicate)
        if self.kind == "I":
            return subject & predicate
        if self.kind == "O":
            return subject - predicate
        raise ValueError("Only I and O have existential witnesses in this API.")

    def __str__(self) -> str:
        return f"{self.kind}({self.subject},{self.predicate})"


@dataclass(frozen=True)
class Argument:
    name: str
    first: Proposition
    second: Proposition
    conclusion: Proposition

    def statuses(self, model: Model) -> tuple[bool, bool, bool]:
        return tuple(p.holds(model) for p in (self.first, self.second, self.conclusion))

    def countermodel(self, model: Model) -> bool:
        first, second, conclusion = self.statuses(model)
        return first and second and not conclusion

    def formula(self) -> str:
        return f"{self.first} & {self.second} => {self.conclusion}"


VALID = Argument("valid", Proposition("E", "A", "B"), Proposition("I", "B", "C"), Proposition("O", "C", "A"))
INVALID = Argument("invalid", Proposition("I", "A", "B"), Proposition("E", "B", "C"), Proposition("O", "C", "A"))
CORRECTED = Argument("corrected", INVALID.first, INVALID.second, Proposition("O", "A", "C"))
ARGUMENTS = (VALID, INVALID, CORRECTED)


def check(argument: Argument, all_classes_nonempty: bool = False) -> dict:
    total = premise_models = false_conclusion_models = 0
    countermodels = []
    for model in models(all_classes_nonempty):
        total += 1
        first, second, conclusion = argument.statuses(model)
        premise_models += first and second
        false_conclusion_models += not conclusion
        if first and second and not conclusion:
            countermodels.append(model)
    return {
        "argument": argument.formula(),
        "all_classes_nonempty": all_classes_nonempty,
        "total_support_models": total,
        "premise_models": premise_models,
        "countermodels": len(countermodels),
        "valid_on_support_models": not countermodels,
        "false_conclusion_models": false_conclusion_models,
        "false_conclusion_and_true_premises": len(countermodels),
        "minimal_countermodel_size": min((len(m.universe) for m in countermodels), default=None),
        "countermodel_supports": [m.support() for m in countermodels],
    }


def named_examples() -> dict[str, Model]:
    """Deliberately chosen examples; their extra regions are not forced."""
    return {
        "valid_remainder_disjoint_A": Model({"w", "r", "a"}, {"a"}, {"w"}, {"w", "r"}),
        "valid_remainder_subset_A": Model({"w", "r"}, {"r"}, {"w"}, {"w", "r"}),
        "valid_remainder_mixed_A": Model({"w", "r", "q"}, {"r"}, {"w"}, {"w", "r", "q"}),
        "invalid_countermodel_nonempty": Model({"s", "v"}, {"s", "v"}, {"s"}, {"v"}),
        "invalid_true_conclusion_alternative": Model({"s", "v"}, {"s"}, {"s"}, {"v"}),
        "valid_both_premises_false_conclusion_true": Model({"s", "v"}, {"s"}, {"s"}, {"v"}),
        "valid_no_remainder": Model({"a", "w"}, {"a"}, {"w"}, {"w"}),
    }


def report() -> dict:
    results = {
        "empty_classes_allowed": {arg.name: check(arg) for arg in ARGUMENTS},
        "all_classes_nonempty": {arg.name: check(arg, True) for arg in ARGUMENTS},
    }
    examples = {}
    for name, model in named_examples().items():
        argument = INVALID if name.startswith("invalid_") else VALID
        examples[name] = {
            **model.as_dict(),
            "argument": argument.formula(),
            "truth_statuses": list(argument.statuses(model)),
            "conclusion_witnesses": sorted(argument.conclusion.witnesses(model)),
        }
    return {"results": results, "examples": examples}


def text_report(data: dict) -> str:
    lines = ["Euler Letter CV: modern finite-set teaching check", ""]
    for semantics, results in data["results"].items():
        lines.append(semantics + ":")
        for name, result in results.items():
            lines.append(
                f"  {name}: {result['argument']} | total={result['total_support_models']}"
                f" premises={result['premise_models']} countermodels={result['countermodels']}"
                f" minimum_countermodel_size={result['minimal_countermodel_size']}"
            )
        lines.append("")
    lines.append("Named teaching examples (first premise, second premise, conclusion):")
    for name, example in data["examples"].items():
        lines.append(f"  {name}: {example['truth_statuses']} support={example['support']}")
        lines.append("    " + "; ".join(f"{key}={{{', '.join(example[key])}}}" for key in ("U", "A", "B", "C")))
        lines.append(f"    conclusion witnesses={example['conclusion_witnesses']}")
    lines.extend([
        "", "Scope: these are counts of occupied-type supports, not of all finite labeled models.",
        "The general eight-type reduction needs the proof in README.md; test output alone is not a proof.",
        "The false-conclusion inference is licensed by validity: false conclusion implies at least",
        "one false premise only for a valid form. The invalid form has true-premise exceptions above.",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit the exact report as JSON.")
    args = parser.parse_args()
    data = report()
    print(json.dumps(data, indent=2, sort_keys=True) if args.json else text_report(data))


if __name__ == "__main__":
    main()
