"""Bounded oracle uses integer polynomials/bit masks, not production algorithms.

This author-written oracle is algorithmically separate, not an independent review.
Checks use explicit exceptions and survive -O/-OO.
"""

import json
from fractions import Fraction
from itertools import product

from habit_model import habit_closed_form, habit_trace
from action_model import Policy, admissible_norms, behavioral_classes, compatible_intentions, normative_status


def check(condition, explanation):
    if not condition:
        raise RuntimeError(explanation)


def integer_habit_numerator(p, q, r, s, bits):
    """Unreduced numerator/denominator from a separate integer polynomial."""
    n = len(bits)
    numerator = r * (q - p) ** n
    for k in range(n):
        numerator += s * p * bits[k] * (q - p) ** (n - 1 - k) * q ** k
    return numerator, s * q ** n


def verify_habits():
    count = prefix_count = 0
    alphas = (Fraction(1, 4), Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), Fraction(3, 4))
    for alpha, initial in product(alphas, (Fraction(k, 4) for k in range(5))):
        for length in range(8):
            for bits in product((0, 1), repeat=length):
                trace = habit_trace(alpha, initial, bits)
                check(len(trace) == length + 1, "habit trace length")
                for n, value in enumerate(trace):
                    numerator, denominator = integer_habit_numerator(
                        alpha.numerator, alpha.denominator, initial.numerator, initial.denominator, bits[:n])
                    check(value.numerator * denominator == numerator * value.denominator,
                          f"integer oracle disagrees at {alpha, initial, bits, n}")
                    check(0 <= value <= 1, "habit interval invariant")
                    prefix_count += 1
                closed = habit_closed_form(alpha, initial, bits)
                numerator, denominator = integer_habit_numerator(
                    alpha.numerator, alpha.denominator, initial.numerator, initial.denominator, bits)
                check(closed.numerator * denominator == numerator * closed.denominator,
                      "closed form disagrees with integer oracle")
                count += 1
    return {"histories": count, "trace_prefix_values": prefix_count,
            "alpha_values": 5, "initial_values": 5, "maximum_history_length": 7}


def verify_policies():
    contexts, intentions, actions = ("x0", "x1"), ("i0", "i1", "i2"), ("a0", "a1")
    candidates_count = partitions_count = refinement_count = 0
    for table in range(64):
        def entry(i, x):
            return (table >> (2 * i + x)) & 1

        policy = Policy(contexts, intentions, actions,
                        tuple(tuple(actions[entry(i, x)] for x in range(2)) for i in range(3)))
        for record in product((-1, 0, 1), repeat=2):
            observations = tuple((contexts[x], actions[a]) for x, a in enumerate(record) if a != -1)
            expected_mask = 0
            for i in range(3):
                mismatch = any(a != -1 and entry(i, x) != a for x, a in enumerate(record))
                if not mismatch:
                    expected_mask |= 1 << i
            actual = compatible_intentions(policy, observations)
            actual_mask = sum(1 << intentions.index(i) for i in actual)
            check(actual_mask == expected_mask, f"candidate bitmask mismatch {table, record}")
            candidates_count += 1
        partitions = {}
        for selected in range(4):
            used = tuple(contexts[x] for x in range(2) if selected & (1 << x))
            actual = behavioral_classes(policy, used)
            flattened = [i for block in actual for i in block]
            check(len(flattened) == 3 and set(flattened) == set(intentions), "not a partition")
            actual_pairs = {(intentions.index(i), intentions.index(j)) for block in actual for i in block for j in block}
            expected_pairs = {(i, j) for i in range(3) for j in range(3)
                              if all(not selected & (1 << x) or entry(i, x) == entry(j, x) for x in range(2))}
            check(actual_pairs == expected_pairs, "pairwise equivalence oracle disagrees")
            partitions[selected] = actual_pairs
            partitions_count += 1
        for small in range(4):
            for large in range(4):
                if small & large == small:
                    check(partitions[large] <= partitions[small], "added contexts merged classes")
                    refinement_count += 1
    return {"tables": 64, "candidate_queries": candidates_count,
            "partitions": partitions_count, "nested_context_pairs": refinement_count,
            "intentions": 3, "contexts": 2, "actions": 2}


def verify_norms():
    universe = ("a0", "a1", "a2")
    family_count = status_count = inconsistent_count = 0
    for required, forbidden in product(range(8), repeat=2):
        selected = lambda mask: tuple(universe[i] for i in range(3) if mask & (1 << i))
        codes = admissible_norms(universe, selected(required), selected(forbidden))
        expected = tuple(mask for mask in range(8) if mask & required == required and mask & forbidden == 0)
        actual = tuple(sum(1 << universe.index(a) for a in code) for code in codes)
        check(actual == expected, "norm family bitmask oracle disagrees")
        check(len(codes) == (0 if required & forbidden else 2 ** (3 - (required | forbidden).bit_count())),
              "norm family cardinality formula disagrees")
        inconsistent_count += int(not expected)
        for i, action in enumerate(universe):
            count = sum(bool(mask & (1 << i)) for mask in expected)
            expected_status = ("inconsistent" if not expected else "all_forbid" if count == 0
                               else "all_permit" if count == len(expected) else "underdetermined")
            check(normative_status(action, universe, codes) == expected_status, "norm status oracle disagrees")
            status_count += 1
        family_count += 1
    return {"universe_size": 3, "bridge_pairs": family_count,
            "inconsistent_bridge_pairs": inconsistent_count, "status_queries": status_count}


def run():
    return {"status": "PASS", "scope": "Author-written bounded algorithmically separate oracle, not external audit",
            "habits": verify_habits(), "policies": verify_policies(), "norms": verify_norms()}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
