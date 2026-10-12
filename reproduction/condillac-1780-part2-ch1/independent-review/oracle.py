"""Independent finite oracle using integer truth tables, never production _step.

All fixed points are found by enumerating every legal state, not by trusting the
implementation's iteration. Integer masks and rule index combinations provide a
separate representation from the production frozenset/Rule calculation.
"""
import itertools
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, os.environ.get('AUDIT_MODEL_DIR', str(Path(__file__).resolve().parents[1])))
from model import HornSystem, Rule, filter_evidence


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def labels(mask, n):
    return tuple(chr(97 + i) for i in range(n) if (mask >> i) % 2)


def encode(values, n):
    mapping = {chr(97 + i): 1 << i for i in range(n)}
    require(all(v in mapping for v in values), 'oracle received foreign output label')
    return sum(mapping[v] for v in values)


def integer_table(n, selected, anchors, excluded):
    """Truth-table evaluation with integer bit positions, no Rule objects."""
    top = (1 << n) - 1
    allowed = top ^ excluded
    table = {}
    for state in range(top + 1):
        if state & excluded:
            continue
        output = anchors & allowed
        for premises, conclusion in selected:
            if not (premises & (top ^ state)):
                output |= conclusion & allowed
        table[state] = output
    return allowed, table


def evidence():
    counts = dict(histories=0, trace_states=0, retention_checks=0,
                  identification_checks=0, permutation_checks=0)
    n = 3
    for length in range(4):
        for observations in itertools.product(range(8), repeat=length):
            for initial in range(8):
                counts['histories'] += 1
                expected = [initial]
                for mask in observations:
                    expected.append(expected[-1] & mask)
                trace = filter_evidence(labels(7, n),
                                        [labels(x, n) for x in observations], labels(initial, n))
                actual = [encode(s, n) for s in trace]
                require(actual == expected, ('evidence full trace', initial, observations))
                counts['trace_states'] += len(actual)
                for position in range(n):
                    bit = 1 << position
                    survives = bool(initial & bit) and all(e & bit for e in observations)
                    counts['retention_checks'] += 1
                    require(bool(actual[-1] & bit) == survives, 'truth retention iff')
                    competitors_removed = all(
                        not (initial & other) or other == bit or any(not (e & other) for e in observations)
                        for other in (1, 2, 4))
                    counts['identification_checks'] += 1
                    require((actual[-1] == bit) == (survives and competitors_removed), 'identification iff')
                for permutation in itertools.permutations(observations):
                    counts['permutation_checks'] += 1
                    got = filter_evidence(labels(7, n), [labels(x, n) for x in permutation], labels(initial, n))
                    require(encode(got[-1], n) == expected[-1], 'fixed-observation permutation')
    require(counts == {'histories': 4680, 'trace_states': 18056, 'retention_checks': 14040,
                      'identification_checks': 14040, 'permutation_checks': 25672}, ('evidence census', counts))
    return counts


def systems(n, unary=False, maximum_rules=None):
    bodies = [x for x in range(1, 1 << n) if not unary or x.bit_count() == 1]
    universe = [(body, 1 << h) for body in bodies for h in range(n)]
    stop = len(universe) if maximum_rules is None else min(maximum_rules, len(universe))
    for length in range(stop + 1):
        yield from itertools.combinations(universe, length)


def horn(n, unary=False, maximum_rules=None):
    top = (1 << n) - 1
    counts = dict(rule_systems=0, contexts=0, legal_states=0, fixed_points=0,
                  monotonic_pairs=0, extreme_points=0, trace_states=0,
                  withdrawal_parameter_pairs=0, withdrawal_extreme_comparisons=0)
    for rules in systems(n, unary, maximum_rules):
        counts['rule_systems'] += 1
        production = HornSystem(labels(top, n), [Rule(labels(b, n), labels(h, n)[0]) for b, h in rules])
        cache = {}
        for anchors in range(top + 1):
            for excluded in range(top + 1):
                counts['contexts'] += 1
                allowed, table = integer_table(n, rules, anchors, excluded)
                fixed = [state for state, output in table.items() if state == output]
                require(bool(fixed), 'existence of fixed points')
                least = min(fixed, key=int.bit_count)
                greatest = max(fixed, key=int.bit_count)
                require(all(least & f == least and f & greatest == f for f in fixed), 'extreme ordering')
                supported = [state for state, output in table.items() if state & output == state]
                require(all(state & greatest == state for state in supported), 'greatest contains all postfixed states')
                counts['fixed_points'] += len(fixed)
                for state, output in table.items():
                    counts['legal_states'] += 1
                    actual = production.immediate(labels(state, n), labels(anchors, n), labels(excluded, n))
                    require(encode(actual, n) == output, ('immediate', n, rules, anchors, excluded, state))
                    for larger in table:
                        if state & larger == state:
                            counts['monotonic_pairs'] += 1
                            require(output & table[larger] == output, 'truth-table monotonicity')
                for kind, endpoint, start in (('least', least, 0), ('greatest', greatest, allowed)):
                    counts['extreme_points'] += 1
                    point = production.fixed_point(kind, labels(anchors, n), labels(excluded, n))
                    actual = [encode(x, n) for x in point.states]
                    counts['trace_states'] += len(actual)
                    require(actual[0] == start, ('start', kind))
                    require(actual[-1] == endpoint, ('enumerated extreme', n, rules, anchors, excluded, kind))
                    require(point.changes == len(actual) - 1 <= allowed.bit_count(), 'strict-change bound')
                    require(table[actual[-1]] == actual[-1], 'stable endpoint')
                    for previous, following in zip(actual, actual[1:]):
                        require(table[previous] == following, 'trace transition')
                        require(previous != following, 'duplicate stable trace')
                        require((previous & following == previous) if kind == 'least'
                                else (previous & following == following), 'trace direction')
                cache[(anchors, excluded)] = (least, greatest)
        for (old_a, old_w), old_points in cache.items():
            for (new_a, new_w), new_points in cache.items():
                if new_a & old_a == new_a and old_w & new_w == old_w:
                    counts['withdrawal_parameter_pairs'] += 1
                    for new, old in zip(new_points, old_points):
                        counts['withdrawal_extreme_comparisons'] += 1
                        require(new & old == new, 'withdrawal nonexpansion')
    expected_systems = { (0, False, None): 1, (1, False, None): 2,
                         (2, False, None): 64, (3, True, None): 512,
                         (3, False, 2): 232 }[(n, unary, maximum_rules)]
    require(counts['rule_systems'] == expected_systems, ('system census', counts))
    require(counts['contexts'] == expected_systems * 4 ** n, 'context census')
    require(counts['legal_states'] == expected_systems * 6 ** n, 'legal-state census')
    require(counts['monotonic_pairs'] == expected_systems * 8 ** n, 'monotonic census')
    require(counts['withdrawal_parameter_pairs'] == expected_systems * 9 ** n, 'parameter-pair census')
    return counts


def main():
    report = {'independent': True, 'representation': 'integer truth tables and complete legal-state enumeration',
              'optimize': sys.flags.optimize, 'evidence': evidence(),
              'horn_empty': horn(0), 'horn_one_all': horn(1), 'horn_two_all': horn(2),
              'horn_three_unary': horn(3, unary=True),
              'horn_three_all_bodies_at_most_two_rules': horn(3, maximum_rules=2), 'success': True}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
