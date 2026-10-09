"""Independent, finite cross-checks for the educational lambda reducer.

Run with Python 3.10+ and its standard library:
    python independent_checks.py

Enumerates all named terms with 1..7 AST nodes over variable names x/y,
then checks substitutions by the 1..4-node terms against a separate nameless
reference. These checks do not prove correctness for arbitrary terms, nor any
historical logical system's consistency, confluence, or normalization.
"""
from __future__ import annotations

import json
import platform
import sys
from functools import lru_cache

sys.dont_write_bytecode = True
import experiment as e


@lru_cache(maxsize=None)
def terms(size: int) -> tuple[e.Term, ...]:
    """Generate by exact node count; a binder name is not a separate node."""
    if size == 1:
        return (e.Var("x"), e.Var("y"))
    result = [e.Lam(name, body)
              for name in ("x", "y") for body in terms(size - 1)]
    for left_size in range(1, size - 1):
        result.extend(e.App(left, right)
                      for left in terms(left_size)
                      for right in terms(size - left_size - 1))
    return tuple(result)


def reference_key(term: e.Term, environment: tuple[str, ...] = ()) -> tuple:
    """Separate alpha-key implementation; environment runs outermost first."""
    if isinstance(term, e.Var):
        for distance, name in enumerate(reversed(environment)):
            if term.name == name:
                return ("bound", distance)
        return ("free", term.name)
    if isinstance(term, e.Lam):
        return ("lam", reference_key(term.body, environment + (term.param,)))
    return ("app", reference_key(term.fn, environment),
            reference_key(term.arg, environment))


def reference_substitute(tree: tuple, variable: str, replacement: tuple) -> tuple:
    """Substitute a free named leaf in a locally bound, nameless representation.

    Free leaves stay explicitly free under lambdas. The replacement comes from
    a complete term, so it has no dangling bound indices to shift at insertion.
    Its own locally bound indices therefore remain valid unchanged.
    """
    if tree[0] == "free":
        return replacement if tree[1] == variable else tree
    if tree[0] == "bound":
        return tree
    if tree[0] == "lam":
        return ("lam", reference_substitute(tree[1], variable, replacement))
    return ("app", reference_substitute(tree[1], variable, replacement),
            reference_substitute(tree[2], variable, replacement))


def reference_free_vars(tree: tuple) -> frozenset[str]:
    if tree[0] == "free":
        return frozenset({tree[1]})
    if tree[0] == "bound":
        return frozenset()
    if tree[0] == "lam":
        return reference_free_vars(tree[1])
    return reference_free_vars(tree[1]) | reference_free_vars(tree[2])


def require(condition: bool, detail: str) -> None:
    # Do not silently disable validation when Python is run with -O.
    if not condition:
        raise AssertionError(detail)


def run_checks() -> dict:
    all_terms = sum((terms(size) for size in range(1, 8)), ())
    replacements = sum((terms(size) for size in range(1, 5)), ())
    substitution_checks = 0
    for term in all_terms:
        term_key = reference_key(term)
        original_fv = reference_free_vars(term_key)
        require(e.debruijn(term) == term_key, "alpha-key mismatch")
        require(e.free_vars(term) == original_fv, "free-variable mismatch")
        for variable in ("x", "y"):
            for replacement in replacements:
                actual = e.substitute(term, variable, replacement)
                expected_key = reference_substitute(
                    term_key, variable, reference_key(replacement))
                require(reference_key(actual) == expected_key,
                        f"substitution mismatch: {e.pretty(term)}, "
                        f"{variable} := {e.pretty(replacement)}")
                expected_fv = ((original_fv - {variable}) | e.free_vars(replacement)
                               if variable in original_fv else original_fv)
                require(e.free_vars(actual) == expected_fv,
                        "substitution free-variable law failed")
                substitution_checks += 1

    reduction_steps = 0
    for term in all_terms:
        for strategy in ("normal", "applicative"):
            for mode in ("modern", "non_erasing"):
                reduced = e.step(term, strategy, mode)
                if reduced is not None:
                    if mode == "non_erasing":
                        require(e.free_vars(term) == e.free_vars(reduced),
                                "non-erasing step changed free-variable set")
                    else:
                        require(e.free_vars(reduced) <= e.free_vars(term),
                                "modern step introduced a free variable")
                    reduction_steps += 1

    arithmetic_checks = 0
    for left in range(6):
        for right in range(6):
            for operator, expected in ((e.ADD, left + right), (e.MULT, left * right)):
                result = e.normalize(
                    e.App(e.App(operator, e.church_numeral(left)),
                          e.church_numeral(right)), max_steps=1024)
                require(result.status == "normal_form", "arithmetic did not finish")
                require(e.decode_numeral(result.term) == expected,
                        "arithmetic result mismatch")
                arithmetic_checks += 1

    # Names with generated-name-like suffixes exercise freshness beyond x/y.
    freshness_cases = (
        (e.Lam("y", e.App(e.Var("x"), e.Var("y_0"))), "x", e.Var("y")),
        (e.Lam("y", e.Lam("y_0", e.Var("x"))), "x", e.Var("y")),
        (e.Lam("y", e.App(e.Var("x"), e.Lam("y", e.Var("y")))),
         "x", e.App(e.Var("y"), e.Var("y_0"))),
    )
    for term, variable, replacement in freshness_cases:
        result = e.substitute(term, variable, replacement)
        expected = reference_substitute(reference_key(term), variable,
                                        reference_key(replacement))
        require(reference_key(result) == expected, "fresh-name collision")

    return {
        "result": "PASS",
        "python": platform.python_version(),
        "terms_checked": len(all_terms),
        "replacement_terms": len(replacements),
        "substitution_checks": substitution_checks,
        "actual_reduction_steps_checked": reduction_steps,
        "arithmetic_checks": arithmetic_checks,
        "additional_freshness_checks": len(freshness_cases),
        "scope": "Finite tests of educational code; not a general mathematical proof.",
    }


if __name__ == "__main__":
    print(json.dumps(run_checks(), ensure_ascii=False, indent=2))
