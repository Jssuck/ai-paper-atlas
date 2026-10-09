"""A modern, educational lambda-calculus reconstruction; Python stdlib only.

This is not a reconstruction of Church's full 1932 logical system. In particular,
modern beta reduction admits erasure, whereas his Rule II required occurrence.
See README.zh-CN.md and the explicit `non_erasing` mode below.
"""

from __future__ import annotations

import argparse
import json
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Union


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Lam:
    param: str
    body: "Term"


@dataclass(frozen=True)
class App:
    fn: "Term"
    arg: "Term"


Term = Union[Var, Lam, App]


def pretty(term: Term) -> str:
    """Fully parenthesized notation: no precedence or association ambiguity."""
    if isinstance(term, Var):
        return term.name
    if isinstance(term, Lam):
        return f"(λ{term.param}.{pretty(term.body)})"
    return f"({pretty(term.fn)} {pretty(term.arg)})"


def free_vars(term: Term) -> frozenset[str]:
    if isinstance(term, Var):
        return frozenset({term.name})
    if isinstance(term, Lam):
        return free_vars(term.body) - {term.param}
    return free_vars(term.fn) | free_vars(term.arg)


def all_names(term: Term) -> frozenset[str]:
    if isinstance(term, Var):
        return frozenset({term.name})
    if isinstance(term, Lam):
        return all_names(term.body) | {term.param}
    return all_names(term.fn) | all_names(term.arg)


def fresh_name(base: str, forbidden: frozenset[str]) -> str:
    index = 0
    candidate = f"{base}_{index}"
    while candidate in forbidden:
        index += 1
        candidate = f"{base}_{index}"
    return candidate


def _rename_bound(body: Term, old: str, new: str) -> Term:
    """Rename the binder outside `body`; stop at a shadowing inner binder.

    Precondition: `new` is absent from every name in `body`.
    """
    if isinstance(body, Var):
        return Var(new) if body.name == old else body
    if isinstance(body, App):
        return App(_rename_bound(body.fn, old, new),
                   _rename_bound(body.arg, old, new))
    if body.param == old:
        return body
    return Lam(body.param, _rename_bound(body.body, old, new))


def substitute(term: Term, variable: str, replacement: Term) -> Term:
    """Capture-avoiding M[x := N], replacing only free occurrences of x."""
    if isinstance(term, Var):
        return replacement if term.name == variable else term
    if isinstance(term, App):
        return App(substitute(term.fn, variable, replacement),
                   substitute(term.arg, variable, replacement))
    if term.param == variable or variable not in free_vars(term.body):
        return term
    if term.param in free_vars(replacement):
        forbidden = all_names(term.body) | all_names(replacement) | {variable}
        fresh = fresh_name(term.param, forbidden)
        renamed = _rename_bound(term.body, term.param, fresh)
        return Lam(fresh, substitute(renamed, variable, replacement))
    return Lam(term.param, substitute(term.body, variable, replacement))


def naive_substitute(term: Term, variable: str, replacement: Term) -> Term:
    """INTENTIONALLY WRONG: demonstrates capture; never used by the reducer."""
    if isinstance(term, Var):
        return replacement if term.name == variable else term
    if isinstance(term, App):
        return App(naive_substitute(term.fn, variable, replacement),
                   naive_substitute(term.arg, variable, replacement))
    if term.param == variable:
        return term
    return Lam(term.param, naive_substitute(term.body, variable, replacement))


def debruijn(term: Term, binders: tuple[str, ...] = ()) -> tuple:
    """Structural alpha key: bound indices, literal free-variable names.

    Index 0 denotes the nearest enclosing binder. Shadowing is respected.
    This compares alpha equivalence only, NOT beta/eta convertibility.
    """
    if isinstance(term, Var):
        if term.name in binders:
            return ("bound", binders.index(term.name))
        return ("free", term.name)
    if isinstance(term, Lam):
        return ("lam", debruijn(term.body, (term.param,) + binders))
    return ("app", debruijn(term.fn, binders), debruijn(term.arg, binders))


def alpha_equivalent(left: Term, right: Term) -> bool:
    return debruijn(left) == debruijn(right)


def _validate(strategy: str, mode: str) -> None:
    if strategy not in {"normal", "applicative"}:
        raise ValueError("strategy must be normal or applicative")
    if mode not in {"modern", "non_erasing"}:
        raise ValueError("mode must be modern or non_erasing")


def step(term: Term, strategy: str = "normal", mode: str = "modern") -> Term | None:
    """One deterministic strong beta step, including beneath lambdas.

    normal: leftmost outermost; applicative: leftmost innermost.
    `non_erasing` permits (lambda x.M) N only when x is free in M.
    Automatic alpha-renaming implements capture avoidance; this mode isolates
    one historical restriction and is NOT the entire 1932 system or Rule II.
    None means no permitted redex. An unchanged Term can be a genuine step.
    """
    _validate(strategy, mode)

    def reduce(current: Term) -> Term | None:
        if isinstance(current, Var):
            return None
        if isinstance(current, Lam):
            inner = reduce(current.body)
            return None if inner is None else Lam(current.param, inner)
        permitted = isinstance(current.fn, Lam) and (
            mode == "modern" or current.fn.param in free_vars(current.fn.body)
        )
        if strategy == "normal" and permitted:
            return substitute(current.fn.body, current.fn.param, current.arg)
        left = reduce(current.fn)
        if left is not None:
            return App(left, current.arg)
        right = reduce(current.arg)
        if right is not None:
            return App(current.fn, right)
        if permitted:
            return substitute(current.fn.body, current.fn.param, current.arg)
        return None

    return reduce(term)


@dataclass(frozen=True)
class ReductionResult:
    strategy: str
    mode: str
    status: str
    steps: int
    term: Term
    trace: tuple[str, ...]
    cycle_start: int | None = None
    cycle_length: int | None = None

    def as_dict(self) -> dict:
        return {
            "strategy": self.strategy,
            "mode": self.mode,
            "status": self.status,
            "steps": self.steps,
            "term": pretty(self.term),
            "free_variables": sorted(free_vars(self.term)),
            "trace": list(self.trace),
            "cycle_start": self.cycle_start,
            "cycle_length": self.cycle_length,
        }


def normalize(term: Term, strategy: str = "normal", mode: str = "modern",
              max_steps: int = 128, detect_cycles: bool = True) -> ReductionResult:
    """Bounded experiment, not a decision procedure for normalization.

    normal_form is relative to the selected mode. cycle_detected records an
    actual repeated alpha class under the fixed deterministic strategy.
    step_limit is INCONCLUSIVE and never by itself a proof of divergence.
    The small recursive implementation is not hardened against enormous terms.
    """
    _validate(strategy, mode)
    if not isinstance(max_steps, int) or isinstance(max_steps, bool) or max_steps < 0:
        raise ValueError("max_steps must be a nonnegative integer")
    current = term
    trace = [pretty(current)]
    seen = {debruijn(current): 0} if detect_cycles else {}
    steps = 0
    while True:
        next_term = step(current, strategy, mode)
        if next_term is None:
            return ReductionResult(strategy, mode, "normal_form", steps,
                                   current, tuple(trace))
        if steps == max_steps:
            return ReductionResult(strategy, mode, "step_limit", steps,
                                   current, tuple(trace))
        current = next_term
        steps += 1
        trace.append(pretty(current))
        if detect_cycles:
            key = debruijn(current)
            if key in seen:
                return ReductionResult(strategy, mode, "cycle_detected", steps,
                                       current, tuple(trace), seen[key], steps - seen[key])
            seen[key] = steps


def church_numeral(number: int) -> Term:
    """Later pedagogical reconstruction; no attribution to the 1932 paper."""
    if not isinstance(number, int) or isinstance(number, bool) or number < 0:
        raise ValueError("number must be a nonnegative integer")
    body: Term = Var("x")
    for _ in range(number):
        body = App(Var("f"), body)
    return Lam("f", Lam("x", body))


def decode_numeral(term: Term) -> int:
    """Decode only the canonical beta-normal numeral shape, up to alpha."""
    key = debruijn(term)
    if key[0] != "lam" or key[1][0] != "lam":
        raise ValueError("not a canonical Church numeral")
    body = key[1][1]
    count = 0
    while body[0] == "app" and body[1] == ("bound", 1):
        count += 1
        body = body[2]
    if body != ("bound", 0):
        raise ValueError("not a canonical Church numeral")
    return count


IDENTITY = Lam("x", Var("x"))
CONSTANT = Lam("a", Lam("b", Var("a")))
SELF_APPLICATION = Lam("x", App(Var("x"), Var("x")))
OMEGA = App(SELF_APPLICATION, SELF_APPLICATION)
# Modern textbook encodings, included as a later pedagogical reconstruction.
ADD = Lam("m", Lam("n", Lam("f", Lam("x", App(
    App(Var("m"), Var("f")), App(App(Var("n"), Var("f")), Var("x")))))))
MULT = Lam("m", Lam("n", Lam("f", App(Var("m"), App(Var("n"), Var("f"))))))


def run_experiments() -> dict:
    capture_body = Lam("y", Var("x"))
    correct = substitute(capture_body, "x", Var("y"))
    incorrect = naive_substitute(capture_body, "x", Var("y"))
    constant_omega = App(App(CONSTANT, Var("y")), OMEGA)
    direct_erasure = App(Lam("x", Var("y")), Var("z"))
    growing = Lam("x", App(App(Var("x"), Var("x")), Var("x")))
    cases = {
        "identity": normalize(App(IDENTITY, Var("a"))),
        "capture_avoiding_beta": normalize(App(Lam("x", capture_body), Var("y"))),
        "constant_omega_normal_modern": normalize(constant_omega),
        "constant_omega_applicative_modern": normalize(constant_omega, "applicative"),
        "constant_omega_normal_non_erasing": normalize(constant_omega, mode="non_erasing"),
        "erasure_modern": normalize(direct_erasure),
        "erasure_non_erasing": normalize(direct_erasure, mode="non_erasing"),
        "omega_cycle": normalize(OMEGA),
        "omega_budget_only": normalize(OMEGA, max_steps=8, detect_cycles=False),
        "growing_term_budget": normalize(App(growing, growing), max_steps=8),
    }
    arithmetic = []
    for name, operator, left, right, expected in [
        ("add", ADD, 2, 3, 5), ("multiply", MULT, 2, 3, 6),
        ("multiply", MULT, 0, 3, 0),
    ]:
        result = normalize(App(App(operator, church_numeral(left)), church_numeral(right)))
        decoded = decode_numeral(result.term)
        assert result.status == "normal_form" and decoded == expected
        arithmetic.append({"operation": name, "left": left, "right": right,
                           "decoded": decoded, "expected": expected,
                           "historical_scope": "later_pedagogical_reconstruction",
                           **result.as_dict()})
    return {
        "schema_version": 1,
        "python": platform.python_version(),
        "dependency_policy": "Python standard library only; no installations",
        "historical_scope": {
            "primary_reference": "Church 1932, pp. 352, 355–357",
            "source_url": "https://www.jstor.org/stable/1968337",
            "modern_mode": "Modern capture-avoiding beta; erasure allowed.",
            "non_erasing_mode": "Only the occurrence restriction is isolated; not the full 1932 system.",
            "numerals": "Later pedagogical reconstruction; not claimed as a 1932 result.",
            "limits": "Finite tests do not prove confluence, normalization in general, or undecidability.",
        },
        "capture_counterexample": {
            "input": pretty(capture_body), "substitute": "x := y",
            "correct": pretty(correct), "incorrect": pretty(incorrect),
            "correct_free_variables": sorted(free_vars(correct)),
            "incorrect_free_variables": sorted(free_vars(incorrect)),
            "alpha_equivalent": alpha_equivalent(correct, incorrect),
        },
        "alpha_checks": {
            "renamed_identity": alpha_equivalent(IDENTITY, Lam("z", Var("z"))),
            "bound_vs_free": alpha_equivalent(IDENTITY, Lam("z", Var("x"))),
            "free_names_preserved": alpha_equivalent(Lam("x", Var("y")), Lam("z", Var("y"))),
        },
        "reductions": {name: result.as_dict() for name, result in cases.items()},
        "arithmetic": arithmetic,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write reproducible JSON results")
    args = parser.parse_args()
    results = run_experiments()
    content = json.dumps(results, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")


if __name__ == "__main__":
    main()
