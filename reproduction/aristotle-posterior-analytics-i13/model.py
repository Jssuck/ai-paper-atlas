"""Original finite teaching models for Posterior Analytics I.13.

Set validity is not causal adequacy. SCM equations are stipulated, not learned
from Aristotle or certified against the world. Standard library only.
"""

from fractions import Fraction
from itertools import product
import json


MODELS = ("X_to_Y", "Y_to_X")


def _size(value):
    if type(value) is not int:
        raise TypeError("size must be an integer, not bool")
    if not 0 <= value <= 8:
        raise ValueError("size must be in [0, 8]")
    return value


def _mask(value, size):
    _size(size)
    if type(value) is not int:
        raise TypeError("set mask must be an integer, not bool")
    if not 0 <= value < (1 << size):
        raise ValueError("set mask is outside the declared universe")
    return value


def included(a, b, size=3):
    """Whether a is a subset of b; empty subjects are permitted."""
    _mask(a, size)
    _mask(b, size)
    return (a & b) == a


def disjoint(a, b, size=3):
    _mask(a, size)
    _mask(b, size)
    return (a & b) == 0


def members(mask, size=3):
    _mask(mask, size)
    return [i for i in range(size) if mask & (1 << i)]


def finite_report():
    """Exhaust exactly 8^3 triples in a three-element universe."""
    report = {
        "universe_size": 3,
        "triples": 0,
        "fact_chain_premises": 0,
        "fact_chain_countermodels": 0,
        "reversed_inclusion_premises": 0,
        "reversed_inclusion_countermodels": 0,
        "reversed_inclusion_nonempty_countermodels": 0,
        "reciprocal_premises": 0,
        "reciprocal_countermodels": 0,
        "negative_premises": 0,
        "negative_countermodels": 0,
        "negative_with_broad_middle": 0,
        "negative_with_broad_middle_all_nonempty": 0,
    }
    for subject, cause, effect in product(range(8), repeat=3):
        report["triples"] += 1
        # These names denote assigned sets, not program-discovered causes.
        if included(subject, effect) and included(effect, cause):
            report["fact_chain_premises"] += 1
            if not included(subject, cause):
                report["fact_chain_countermodels"] += 1
        if included(cause, effect) and included(subject, effect):
            report["reversed_inclusion_premises"] += 1
            if not included(subject, cause):
                report["reversed_inclusion_countermodels"] += 1
                if subject and cause and effect:
                    report["reversed_inclusion_nonempty_countermodels"] += 1
        if cause == effect and included(subject, effect):
            report["reciprocal_premises"] += 1
            if not included(subject, cause):
                report["reciprocal_countermodels"] += 1
        # Renaming: subject = W, cause = A, effect = B.
        if included(effect, cause) and disjoint(subject, cause):
            report["negative_premises"] += 1
            if not disjoint(subject, effect):
                report["negative_countermodels"] += 1
            if not included(cause, effect):
                report["negative_with_broad_middle"] += 1
                if subject and cause and effect:
                    report["negative_with_broad_middle_all_nonempty"] += 1
    return report


def _model(name):
    if type(name) is not str:
        raise TypeError("model must be a string")
    if name not in MODELS:
        raise ValueError("model must be X_to_Y or Y_to_X")


def _bit(value):
    if type(value) is not int:
        raise TypeError("binary values must be integers, not bool")
    if value not in (0, 1):
        raise ValueError("binary values must be 0 or 1")


def _intervention(do):
    if do is None:
        return {}
    if type(do) is not dict:
        raise TypeError("intervention must be a plain dict or None")
    for variable, value in do.items():
        if type(variable) is not str:
            raise TypeError("intervention variable must be a string")
        if variable not in ("X", "Y"):
            raise ValueError("only X and Y may be intervened on")
        _bit(value)
    return dict(do)


def evaluate(name, u, do=None):
    """Return (X,Y) under equation replacement, for a fixed binary U."""
    _model(name)
    _bit(u)
    intervention = _intervention(do)
    if name == "X_to_Y":
        x = intervention.get("X", u)
        y = intervention.get("Y", x)
    else:
        y = intervention.get("Y", u)
        x = intervention.get("X", y)
    return (x, y)


def distribution(name, do=None):
    """Exact distribution when P(U=0)=P(U=1)=1/2, including zero cells."""
    _model(name)
    intervention = _intervention(do)
    counts = {pair: Fraction(0) for pair in product((0, 1), repeat=2)}
    for u in (0, 1):
        counts[evaluate(name, u, intervention)] += Fraction(1, 2)
    return counts


def intervention_grid():
    """All 3^2 choices: leave alone, set to 0, or set to 1."""
    return [
        {v: value for v, value in zip(("X", "Y"), values) if value is not None}
        for values in product((None, 0, 1), repeat=2)
    ]


def _probability_rows(probabilities):
    return [
        {"X": x, "Y": y, "probability": str(probabilities[(x, y)])}
        for x, y in product((0, 1), repeat=2)
    ]


def results():
    scm = []
    for intervention in intervention_grid():
        scm.append({
            "do": intervention,
            "models": {
                name: _probability_rows(distribution(name, intervention))
                for name in MODELS
            },
        })
    return {
        "scope": "Original finite teaching models; not a causal certification",
        "finite_sets": finite_report(),
        "witnesses": {
            "reverse_without_bridge": {
                "S": members(2), "C": members(1), "E": members(3),
                "premises": "C subset E and S subset E",
                "failed_conclusion": "S subset C",
            },
            "broad_negative_middle": {
                "W": members(1), "A": members(6), "B": members(4),
                "valid_conclusion": "W disjoint B",
                "A_not_B_witness": members(6 & ~4),
            },
        },
        "scm": {
            "exogenous_distribution": "P(U=0)=P(U=1)=1/2",
            "equations": {"X_to_Y": "X=U; Y=X", "Y_to_X": "Y=U; X=Y"},
            "observational_distributions_equal": (
                distribution("X_to_Y") == distribution("Y_to_X")
            ),
            "do_X_0_distributions_equal": (
                distribution("X_to_Y", {"X": 0})
                == distribution("Y_to_X", {"X": 0})
            ),
            "intervention_cases": scm,
        },
    }


if __name__ == "__main__":
    print(json.dumps(results(), ensure_ascii=False, indent=2, sort_keys=True))
