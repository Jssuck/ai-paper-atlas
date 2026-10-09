"""Independent finite oracle, written separately from the teaching implementation.

Run: python independent_checks.py
No third-party packages, network, randomness, or external data are required.
Expected relation outputs use integer row/column masks, not Relation.compose.
Expected Boole premises use set inclusions/equality, not boole_original.
Expected elimination outputs use raw truth-table projection, not eval_cnf.
This is bounded computational verification, not a proof over every universe.
"""
from itertools import product
import json
import platform

import peirce_finite as implementation


def members(n, mask):
    return frozenset(i for i in range(n) if mask & (1 << i))


def relation_from_mask(n, mask):
    return implementation.Relation(n, frozenset(
        (i, j) for i in range(n) for j in range(n)
        if mask & (1 << (i * n + j))))


def relation_mask(relation):
    return sum(1 << (i * relation.n + j) for i, j in relation.pairs)


def check_categorical():
    cases = 0
    for n in range(5):
        full = (1 << n) - 1
        for subject, predicate in product(range(1 << n), repeat=2):
            intersection = subject & predicate
            difference = subject & (full ^ predicate)
            expected = dict(A=difference == 0, E=intersection == 0,
                            I=intersection != 0, O=difference != 0)
            actual = implementation.categorical(members(n, subject), members(n, predicate))
            assert actual == expected, (n, subject, predicate)
            cases += 1
    assert cases == 341
    return dict(universe_sizes=[0, 1, 2, 3, 4], subject_predicate_pairs=cases)


def relation_oracle(n, left, right):
    """Integer intersection/subset checks independently realize four quantifiers."""
    domain = (1 << n) - 1
    outputs = [0, 0, 0, 0]
    for i in range(n):
        row = (left >> (i * n)) & domain
        for k in range(n):
            column = sum(((right >> (j * n + k)) & 1) << j for j in range(n))
            truth = (bool(row & column),
                     not bool(row & (domain ^ column)),
                     not bool(column & (domain ^ row)),
                     bool((domain ^ row) & (domain ^ column)))
            for index, result in enumerate(truth):
                outputs[index] |= int(result) << (i * n + k)
    return tuple(outputs)


def check_relations():
    pairs = outputs = classifications = 0
    edge_cases = []
    for n in range(4):
        relations = tuple(relation_from_mask(n, mask) for mask in range(1 << (n * n)))
        for mask, relation in enumerate(relations):
            diagonal_count = sum(bool(mask & (1 << (i * n + i))) for i in range(n))
            off_count = mask.bit_count() - diagonal_count
            expected = dict(
                concurrent=off_count == 0,
                opponent=off_count > 0,
                self_relative=diagonal_count > 0,
                alio_relative=diagonal_count == 0,
                negative_of_concurrent=off_count == n * (n - 1),
                negative_of_opponent=off_count < n * (n - 1),
                negative_of_self_relative=diagonal_count < n,
                negative_of_alio_relative=diagonal_count == n,
            )
            assert relation.classify() == expected, (n, mask, expected)
            classifications += 1
        if n < 2:
            edge_cases.append(dict(n=n, zero=relations[0].classify(),
                                   top=relations[-1].classify(),
                                   zero_equals_top=relations[0] == relations[-1]))
        for left, r in enumerate(relations):
            for right, s in enumerate(relations):
                expected = relation_oracle(n, left, right)
                actual = tuple(relation_mask(result) for result in (
                    r.compose(s), r.regressive(s), r.progressive(s), r.transadd(s)))
                assert actual == expected, (n, left, right, expected, actual)
                pairs += 1
                outputs += 4
    assert (pairs, outputs, classifications) == (262405, 1049620, 531)
    return dict(universe_sizes=[0, 1, 2, 3], ordered_relation_pairs=pairs,
                operation_results=outputs, classifications=classifications,
                edge_cases=edge_cases)


def original_three_set_premises(u, v, x, y, z, w):
    """Direct transcription of the three displayed premises on printed p.39."""
    return ((u - x) & (u - z) <= v & ((y & (u - w)) | ((u - y) & w))
            and (u - v) & x & w <= (y & z) | ((u - y) & (u - z))
            and ((x & y) | (v & x & (u - y))) == ((z & (u - w)) | ((u - z) & w)))


def raw_cnf_value(formula, values):
    """Independent CNF interpretation; does not call implementation.eval_cnf."""
    for disjunction in formula:
        satisfied = False
        for name, positive in disjunction:
            if (bool(values[name]) if positive else not bool(values[name])):
                satisfied = True
                break
        if not satisfied:
            return False
    return True


def check_boole():
    pointwise_cases = projection_cases = 0
    six = implementation.boole_six_clauses()
    for n in range(3):
        u = frozenset(range(n))
        subsets = tuple(members(n, mask) for mask in range(1 << n))
        for v, x, y, z, w in product(subsets, repeat=5):
            expected = original_three_set_premises(u, v, x, y, z, w)
            actual = all(implementation.boole_original(dict(
                v=i in v, x=i in x, y=i in y, z=i in z, w=i in w)) for i in u)
            assert actual == expected, (n, v, x, y, z, w)
            pointwise_cases += 1
        for x, y, z, w in product(subsets, repeat=4):
            expected = any(original_three_set_premises(u, v, x, y, z, w)
                           for v in subsets)
            actual = all(raw_cnf_value(six, dict(x=i in x, y=i in y, z=i in z, w=i in w))
                         for i in u)
            assert actual == expected, (n, x, y, z, w)
            exact = all(implementation.boole_exact_solution(dict(
                x=i in x, y=i in y, z=i in z, w=i in w)) for i in u)
            assert exact == expected, (n, x, y, z, w)
            projection_cases += 1
    mismatches, projected_count, printed_count = [], 0, 0
    u = frozenset((0,))
    for row in product((0, 1), repeat=4):
        x, y, z, w = (members(1, bit) for bit in row)
        projected = any(original_three_set_premises(u, v, x, y, z, w)
                        for v in (frozenset(), u))
        printed = u <= x | (z & w) | (y & (u - z) & (u - w))
        env = dict(zip(('x', 'y', 'z', 'w'), row))
        assert implementation.boole_printed_summary(env) == printed
        assert not projected or printed
        if projected != printed:
            mismatches.append(list(row))
        projected_count += projected
        printed_count += printed
    assert (pointwise_cases, projection_cases) == (1057, 273)
    assert (projected_count, printed_count) == (8, 11)
    assert mismatches == [[1, 0, 1, 1], [1, 1, 0, 0], [1, 1, 1, 1]]
    return dict(universe_sizes=[0, 1, 2], original_set_assignments=pointwise_cases,
                projected_set_assignments=projection_cases,
                exact_solution_set_assignments=projection_cases,
                singleton_projected_models=projected_count,
                singleton_printed_summary_models=printed_count,
                extra_printed_summary_models_xyzw=mismatches)


def check_elimination():
    names = ('x', 'y', 'z')
    rows = tuple(product((False, True), repeat=3))
    projections = truth_checks = expansion_checks = 0
    for table in range(256):
        # Each false row contributes the unique full clause it falsifies.
        formula = frozenset(frozenset((name, not value) for name, value in zip(names, row))
                            for index, row in enumerate(rows) if not table & (1 << index))
        for variable in names:
            projected, _ = implementation.eliminate(formula, variable)
            position = names.index(variable)
            remaining = tuple(name for name in names if name != variable)
            for row in product((False, True), repeat=2):
                env = dict(zip(remaining, row))
                indices = []
                for value in (False, True):
                    complete = list(row)
                    complete.insert(position, value)
                    indices.append(rows.index(tuple(complete)))
                expected = any(table & (1 << index) for index in indices)
                assert raw_cnf_value(projected, env) == expected, (table, variable, env)
                assert all(variable != name for c in projected for name, _ in c)
                truth_checks += 1
            projections += 1
        for index, row in enumerate(rows):
            env = dict(zip(names, row))
            expected = bool(table & (1 << index))
            def truth_function(values):
                return bool(table & (1 << rows.index(tuple(values[name] for name in names))))
            for variable in names:
                assert implementation.shannon(truth_function, variable, env) == expected
                expansion_checks += 1
    # Explicit degenerate formula and absent-variable cases.
    for formula in (frozenset(), frozenset((frozenset(),)),
                    frozenset((frozenset((('x', True), ('x', False))),)),
                    frozenset((frozenset((('y', True),)),))):
        projected, _ = implementation.eliminate(formula, 'x')
        for y in (False, True):
            expected = any(raw_cnf_value(formula, dict(x=x, y=y)) for x in (False, True))
            assert raw_cnf_value(projected, dict(y=y)) == expected
    assert (projections, truth_checks, expansion_checks) == (768, 3072, 6144)
    return dict(ternary_truth_functions=256, variable_projections=projections,
                projected_truth_values=truth_checks, expansion_values=expansion_checks,
                degenerate_formula_checks=8)


def check_p38_count():
    # The two product terms xy and yz overlap. No textual formula is repaired.
    rows = tuple(product((False, True), repeat=3))
    function = lambda e: (e['x'] and e['y']) or (e['y'] and e['z'])
    canonical = implementation.cnf_from_truth_function(('x', 'y', 'z'), function)
    false_rows = sum(not ((x and y) or (y and z)) for x, y, z in rows)
    printed_general_count = 2 ** 3 + 4 - 3 * 2 - 2
    assert len(canonical) == false_rows == 5
    assert printed_general_count == 4
    return dict(example='(x AND y) OR (y AND z)', m=3, n=4, p=2,
                printed_general_count=printed_general_count,
                truth_table_full_clause_count=false_rows)


def main():
    report = dict(python=platform.python_version(),
                  scope='Bounded finite verification; not a general mathematical proof.',
                  categorical=check_categorical(),
                  boole=check_boole(), elimination=check_elimination(),
                  p38_count_diagnostic=check_p38_count(), relations=check_relations(),
                  status='PASS')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
