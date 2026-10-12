"""Author's bounded exhaustive checks, not an independent audit or general proof."""
import itertools
import json
import sys
from model import HornSystem, Rule, filter_evidence


def subsets(values):
    values = tuple(values)
    return tuple(frozenset(values[i] for i in range(len(values)) if mask & (1 << i))
                 for mask in range(1 << len(values)))


def check(condition, context):
    if not condition:
        raise AssertionError(context)


def evidence_checks():
    H = frozenset({"a", "b", "c"})
    powerset = subsets(sorted(H))
    counts = {"histories": 0, "truth_retention_checks": 0,
              "identification_checks": 0, "permutation_checks": 0}
    for length in range(4):
        for evidence in itertools.product(powerset, repeat=length):
            for initial in powerset:
                counts["histories"] += 1
                trace = filter_evidence(H, evidence, initial)
                expected = frozenset(h for h in initial if all(h in E for E in evidence))
                check(trace[-1] == expected, ("closed form", initial, evidence))
                check(len(trace) == length + 1, "evidence trace size")
                check(all(after <= before for before, after in zip(trace, trace[1:])), "non-shrinking evidence")
                for truth in H:
                    counts["truth_retention_checks"] += 1
                    retained = truth in initial and all(truth in E for E in evidence)
                    check((truth in trace[-1]) == retained, "retention iff")
                    counts["identification_checks"] += 1
                    identified = retained and all(any(rival not in E for E in evidence)
                                                  for rival in initial - {truth})
                    check((trace[-1] == {truth}) == identified, "identification iff")
                for permutation in itertools.permutations(evidence):
                    counts["permutation_checks"] += 1
                    check(filter_evidence(H, permutation, initial)[-1] == expected, "order independence")
    check(counts == {"histories": 4680, "truth_retention_checks": 14040,
                     "identification_checks": 14040, "permutation_checks": 25672}, "evidence census")
    return counts


def reference_T(state, anchors, withdrawn, rules):
    # Deliberately written directly from the definition, without calling _step.
    answer = set(anchors) - set(withdrawn)
    for rule in rules:
        if rule.head not in withdrawn and all(premise in state for premise in rule.body):
            answer.add(rule.head)
    return frozenset(answer)


def horn_checks(size, unary_only):
    V = frozenset(chr(ord("a") + i) for i in range(size))
    power = subsets(sorted(V))
    bodies = [body for body in power if body and (not unary_only or len(body) == 1)]
    possible_rules = tuple(Rule(body, head) for body in bodies for head in sorted(V))
    counts = {"possible_rules": len(possible_rules), "rule_systems": 0, "contexts": 0,
              "candidate_states": 0, "immediate_monotonic_pairs": 0,
              "withdrawal_parameter_pairs": 0, "withdrawal_fixedpoint_comparisons": 0}
    for rule_set in subsets(possible_rules):
        counts["rule_systems"] += 1
        system = HornSystem(V, tuple(rule_set))
        cache = {}
        for anchors in power:
            for withdrawn in power:
                counts["contexts"] += 1
                U = V - withdrawn
                candidates = subsets(sorted(U))
                fixed = []
                for state in candidates:
                    counts["candidate_states"] += 1
                    reference = reference_T(state, anchors, withdrawn, rule_set)
                    check(system.immediate(state, anchors, withdrawn) == reference, "T reference")
                    if reference == state:
                        fixed.append(state)
                check(bool(fixed), "at least one fixed point")
                least = system.fixed_point("least", anchors, withdrawn)
                greatest = system.fixed_point("greatest", anchors, withdrawn)
                intersection = frozenset.intersection(*fixed)
                union = frozenset.union(*fixed)
                check(least.result == intersection, "least != intersection of fixed points")
                check(greatest.result == union, "greatest != union of fixed points")
                check(least.result <= greatest.result <= U, "L <= G <= U")
                for kind, point in (("least", least), ("greatest", greatest)):
                    check(point.changes <= len(U), "iteration bound")
                    check(reference_T(point.result, anchors, withdrawn, rule_set) == point.result, "stability")
                    for before, after in zip(point.states, point.states[1:]):
                        check(after == reference_T(before, anchors, withdrawn, rule_set), "trace step")
                        check(before < after if kind == "least" else after < before, "strict trace direction")
                cache[(anchors, withdrawn)] = (least.result, greatest.result)
                if not unary_only:
                    for small in candidates:
                        for large in candidates:
                            if small <= large:
                                counts["immediate_monotonic_pairs"] += 1
                                check(system.immediate(small, anchors, withdrawn) <=
                                      system.immediate(large, anchors, withdrawn), "T monotonicity")
        if not unary_only:
            for A in power:
                for reduced_A in power:
                    if not reduced_A <= A:
                        continue
                    for W in power:
                        for expanded_W in power:
                            if not W <= expanded_W:
                                continue
                            counts["withdrawal_parameter_pairs"] += 1
                            before = cache[(A, W)]
                            after = cache[(reduced_A, expanded_W)]
                            for index in range(2):
                                counts["withdrawal_fixedpoint_comparisons"] += 1
                                check(after[index] <= before[index], "withdrawal monotonicity")
    expected = ({"possible_rules": 9, "rule_systems": 512, "contexts": 32768,
                 "candidate_states": 110592, "immediate_monotonic_pairs": 0,
                 "withdrawal_parameter_pairs": 0, "withdrawal_fixedpoint_comparisons": 0}
                if unary_only else
                {"possible_rules": 6, "rule_systems": 64, "contexts": 1024,
                 "candidate_states": 2304, "immediate_monotonic_pairs": 4096,
                 "withdrawal_parameter_pairs": 5184, "withdrawal_fixedpoint_comparisons": 10368})
    check(counts == expected, ("Horn census", counts))
    return counts


def main():
    report = {"author_check": True, "optimization": sys.flags.optimize,
              "evidence_three_hypotheses_length_0_to_3": evidence_checks(),
              "horn_two_claims_all_nonempty_bodies": horn_checks(2, False),
              "horn_three_claims_unary_bodies_only": horn_checks(3, True),
              "success": True}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
