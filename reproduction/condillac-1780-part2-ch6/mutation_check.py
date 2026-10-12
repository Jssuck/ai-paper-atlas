"""Small, explicit fault-injection check; this is not mutation-score coverage.

Only a BehaviorMismatch counts as detection. Unexpected exceptions are harness
errors and make this script fail; a crashing mutant is never counted as killed.
"""
from __future__ import annotations

import json
from unittest.mock import patch
import condillac_model as m


class BehaviorMismatch(Exception):
    pass


def check_equal(actual, expected):
    if actual != expected:
        raise BehaviorMismatch(f"expected {expected!r}; got {actual!r}")


def classify(probe):
    try:
        probe()
    except BehaviorMismatch as exc:
        return "behavior_mismatch", str(exc)
    except Exception as exc:
        return "harness_error", f"{type(exc).__name__}: {exc}"
    return "pass", ""


def probe_expansion():
    system = m.DefinitionSystem(("p",), (m.Definition("d", m.Var("p")),))
    check_equal(system.expand({"p": True}), {"p": True, "d": True})


def probe_observation():
    result = m.analyze_observations(m.enumerate_worlds(("p", "q")), (m.Var("p"),), m.Var("q"))
    check_equal(result.definable, False)


def probe_closure():
    rule = m.Rule(frozenset(("a", "b")), "c")
    check_equal(m.forward_closure(("a",), (rule,)), frozenset(("a",)))


def probe_order():
    rules = (m.Rule(frozenset(("a",)), "b"), m.Rule(frozenset(("b",)), "c"))
    check_equal(m.verify_order(("a",), rules, ("c", "b")).valid, False)


def probe_evidence():
    check_equal(m.filter_evidence(m.enumerate_worlds(("p",)), m.Var("p")), ({"p": True},))


def probe_old_name_equation():
    check_equal(m.satisfying_extensions({"p": False}, (m.Definition("p", m.Const(True)),)), ())


ORIGINAL_EXPAND = m.DefinitionSystem.expand


def wrong_expansion(self, world):
    result = ORIGINAL_EXPAND(self, world)
    if self.definitions:
        name = self.definitions[0].name
        result[name] = not result[name]
    return result


def wrong_observation(worlds, features, target):
    # Deliberately forget to compare opposite targets in the same observation fiber.
    return m.ObservationAnalysis(True, (), None)


def wrong_closure(seeds, rules):
    known = set(seeds)
    while True:
        additions = {r.conclusion for r in rules if not r.premises or any(p in known for p in r.premises)} - known
        if not additions:
            return frozenset(known)
        known.update(additions)


def wrong_order(seeds, rules, order):
    # Deliberately let future conclusions justify earlier steps.
    order = tuple(order)
    available = set(seeds) | set(order)
    valid = all(any(r.conclusion == item and r.premises <= available for r in rules) for item in order)
    return m.OrderReport(valid, frozenset(available))


def wrong_evidence(worlds, evidence):
    return tuple(dict(w) for w in worlds)


def wrong_old_name_equation(base, equations):
    result = dict(base)
    for equation in equations:
        result[equation.name] = m.evaluate(equation.expression, result)
    return (result,)


CASES = (
    ("flip_defined_value", m.DefinitionSystem, "expand", wrong_expansion, probe_expansion),
    ("ignore_fiber_conflict", m, "analyze_observations", wrong_observation, probe_observation),
    ("any_instead_of_all_premises", m, "forward_closure", wrong_closure, probe_closure),
    ("future_premises_allowed", m, "verify_order", wrong_order, probe_order),
    ("ignore_evidence", m, "filter_evidence", wrong_evidence, probe_evidence),
    ("overwrite_old_name", m, "satisfying_extensions", wrong_old_name_equation, probe_old_name_equation),
)


def main():
    records = []
    for name, owner, attribute, replacement, probe in CASES:
        baseline_status, baseline_detail = classify(probe)
        with patch.object(owner, attribute, replacement):
            mutant_status, mutant_detail = classify(probe)
        records.append({"mutant": name, "baseline": baseline_status,
                        "baseline_detail": baseline_detail, "mutant_status": mutant_status,
                        "detail": mutant_detail})
    result = {
        "baseline_passes": sum(r["baseline"] == "pass" for r in records),
        "behavior_detected": sum(r["mutant_status"] == "behavior_mismatch" for r in records),
        "harness_errors": sum(r["mutant_status"] == "harness_error" or r["baseline"] == "harness_error" for r in records),
        "records": records,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if all(r["baseline"] == "pass" and r["mutant_status"] == "behavior_mismatch" for r in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
