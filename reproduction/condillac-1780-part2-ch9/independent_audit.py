"""Independent, stdlib-only small-model oracle checks; run with python3."""
from collections import Counter
from fractions import Fraction
from itertools import product
import hashlib
import json
import sys
from pathlib import Path

from model import (certain, consistent, expected_ambiguity, minimal_separating,
                   partition, posterior, structural_certainty)
from examples import results

COUNTS = Counter()


def check_equal(actual, expected, category):
    if actual != expected:
        raise AssertionError((category, actual, expected))
    COUNTS[category] += 1


def raises_value_error(fn):
    try:
        fn()
    except ValueError:
        COUNTS['validation_rejections'] += 1
    else:
        raise AssertionError('Expected ValueError')


# Enumerate every ordered family of up to three Boolean tests on 1..4 worlds.
# Separating-family oracle uses pair coverage, not signatures.
for n in range(1, 5):
    h = tuple(str(i) for i in range(n))
    tables = tuple(product((False, True), repeat=n))
    for m in range(4):
        for rows in product(tables, repeat=m):
            tests = {f't{t}': dict(zip(h, row)) for t, row in enumerate(rows)}
            names = tuple(tests)
            pairs = {(a, b) for a in range(n) for b in range(a + 1, n)}
            cover = [set(pair for pair in pairs if row[pair[0]] != row[pair[1]])
                     for row in rows]
            candidates = []
            for mask in range(1 << m):
                indices = tuple(i for i in range(m) if mask & (1 << i))
                covered = set().union(*(cover[i] for i in indices))
                if covered == pairs:
                    candidates.append(indices)
            expected = (tuple(names[i] for i in min(candidates, key=lambda x: (len(x), x)))
                        if candidates else None)
            check_equal(minimal_separating(h, tests), expected, 'separating_families')
            # Outcome 2 is outside all test ranges and must be inconsistent.
            for observed in product((False, True, 2), repeat=m):
                valid = set(range(n))
                for i, outcome in enumerate(observed):
                    valid &= {j for j in range(n) if rows[i][j] == outcome}
                expected_state = tuple(h[j] for j in range(n) if j in valid)
                check_equal(consistent(h, tests, tuple(zip(names, observed))),
                            expected_state, 'evidence_states')
    for row in tables:
        table = dict(zip(h, row))
        cell_indices = [[i for i in range(n) if row[i] == value]
                        for value in dict.fromkeys(row)]
        cells = tuple(tuple(h[i] for i in cell) for cell in cell_indices)
        check_equal(partition(h, table), cells, 'partitions')
        # Calculate expectation directly over the true world, avoiding the
        # implementation's sum-of-squared-cell-sizes identity.
        expected_size = sum(Fraction(sum(v == row[i] for v in row), n)
                            for i in range(n))
        check_equal(expected_ambiguity(h, table), expected_size, 'ambiguities')
    for truth in tables:
        check_equal(certain(h, dict(zip(h, truth))), not (False in truth),
                    'nonempty_certainties')

check_equal(certain((), {}), False, 'empty_certainty')

# Exhaust rational priors, likelihoods and all propositions on up to 3 worlds.
for n in range(1, 4):
    h = tuple(str(i) for i in range(n))
    for likelihood_values in product((0, Fraction(1, 3), Fraction(1, 2), 1), repeat=n):
        likelihood = dict(zip(h, likelihood_values))
        support = [i for i in range(n) if likelihood_values[i] > 0]
        for truth in product((False, True), repeat=n):
            check_equal(structural_certainty(h, likelihood, dict(zip(h, truth))),
                        bool(support) and not any(not truth[i] for i in support),
                        'structural_certainties')
        for prior_values in product((0, Fraction(1, 2), 2), repeat=n):
            prior = dict(zip(h, prior_values))
            denominator = sum(Fraction(a) * b for a, b in zip(prior_values, likelihood_values))
            if denominator == 0:
                raises_value_error(lambda: posterior(h, prior, likelihood))
            else:
                answer = posterior(h, prior, likelihood)
                check_equal(sum(answer.values()), Fraction(1), 'posterior_normalizations')
                if not all(type(v) is Fraction for v in answer.values()):
                    raise AssertionError(('Non-Fraction posterior coordinate', answer))
                for i, world in enumerate(h):
                    check_equal(answer[world], Fraction(prior_values[i]) * likelihood_values[i] / denominator,
                                'posterior_coordinates')
                # Positive scaling of all prior weights leaves posterior invariant.
                check_equal(posterior(h, {w: prior[w] * 7 for w in h}, likelihood),
                            answer, 'prior_scale_invariance')

h = ('a', 'b')
t = {'a': 'x', 'b': 'y'}
check_equal(consistent(h, {'t': t}, [('t', 'x'), ('t', 'x')]), ('a',), 'repeated_observation')
check_equal(consistent(h, {'t': t}, [('t', 'x'), ('t', 'y')]), (), 'contradiction')
check_equal(minimal_separating(h, {'right': t, 'left': t}), ('right',), 'insertion_order_tie')
check_equal(consistent(iter(h), {'t': t}, iter([('t', 'y')])), ('b',), 'generator_inputs')
for invalid_h in [(), ('a', 'a'), ('',), (1,), (True,)]:
    raises_value_error(lambda: consistent(invalid_h, {}, []))
for invalid_table in [{'a': True}, {'a': True, 'b': False, 'c': True}, {'a': [], 'b': []}]:
    raises_value_error(lambda: partition(h, invalid_table))
for invalid_proposition in [{'a': 1, 'b': True}, {'a': True}, {'a': True, 'b': True, 'c': True}]:
    raises_value_error(lambda: certain(h, invalid_proposition))
raises_value_error(lambda: certain((), {'a': True}))
raises_value_error(lambda: consistent(h, {}, [('missing', True)]))
for invalid_weight in [-1, Fraction(-1, 2), 0.5, True, '1', None]:
    raises_value_error(lambda: posterior(h, {'a': invalid_weight, 'b': 1}, dict.fromkeys(h, 1)))
for invalid_likelihood in [-1, Fraction(3, 2), 2, 0.5, True, None]:
    raises_value_error(lambda: posterior(h, dict.fromkeys(h, 1), {'a': invalid_likelihood, 'b': 1}))
raises_value_error(lambda: posterior(h, {'a': 1}, dict.fromkeys(h, 1)))
raises_value_error(lambda: structural_certainty(h, dict.fromkeys(h, 1), {'a': True, 'b': 1}))


# Restrict symbols to stable exact types; reject nonreflexive and custom values.
for unsupported in [float('nan'), float('inf'), 1.0, None, (), frozenset({1}), object()]:
    raises_value_error(lambda: partition(h, {'a': unsupported, 'b': 'b'}))
    raises_value_error(lambda: consistent(h, {'t': {'a': 1, 'b': 2}}, [('t', unsupported)]))
equal_numeric_labels = {'a': True, 'b': Fraction(1)}
check_equal(partition(h, equal_numeric_labels), (('a', 'b'),), 'numeric_label_equality')
check_equal(minimal_separating(h, {'t': equal_numeric_labels}), None, 'numeric_label_equality')
check_equal(consistent(h, {'t': equal_numeric_labels}, [('t', 1)]), h, 'numeric_label_equality')

# Mixed allowed labels: equality classes are computed by an ordered linear scan,
# independent of the implementation's dictionary/hash partitioning.
h3 = ('c', 'a', 'b')
for values in product(('x', '1', False, True, -1, Fraction(1), Fraction(1, 2)), repeat=3):
    table = dict(zip(h3, values))
    representatives, cells = [], []
    for world, value in zip(h3, values):
        matches = [i for i, representative in enumerate(representatives) if value == representative]
        if matches:
            cells[matches[0]].append(world)
        else:
            representatives.append(value)
            cells.append([world])
    check_equal(partition(h3, table), tuple(tuple(cell) for cell in cells), 'mixed_symbol_partitions')
    for world in h3:
        answer = consistent(h3, {'t': table}, [('t', table[world])])
        if world not in answer:
            raise AssertionError((world, table, answer))
        COUNTS['generating_world_preserved'] += 1

# Very large exact integers and rational weights retain exact arithmetic.
big = 10**1000
check_equal(posterior(h, {'a': big, 'b': big}, {'a': Fraction(1, big), 'b': Fraction(3, big)}),
            {'a': Fraction(1, 4), 'b': Fraction(3, 4)}, 'large_exact_rationals')

# Expected pedagogical outputs are fixed independently of implementation.
expected_examples = {
    'cause_implies_effect': True,
    'effect_observed_candidates': ['both', 'alternate'],
    'effect_implies_cause': False,
    'similarity_candidates': ['similar_inhabited', 'similar_empty'],
    'similarity_guarantees_inhabitants': False,
    'gold_malleability_observed': True,
    'gold_unobserved_property_certain': False,
    'contradictory_observations': [],
    'empty_state_certain': False,
    'expected_survivors': {'first_bit': '2', 'second_bit': '2', 'rare_11': '5/2'},
    'minimal_separating_tests': ['first_bit', 'second_bit'],
    'zero_prior_posterior': {'target': '1', 'alternative': '0'},
    'zero_prior_structural_certainty': False,
    'positive_prior_posterior': {'target': '3/4', 'alternative': '1/4'},
    'zero_likelihood_structural_certainty': True,
}
check_equal(results(), expected_examples, 'example_snapshot')

print(json.dumps({
    'source_sha256': {f: hashlib.sha256(Path(f).read_bytes()).hexdigest()
                      for f in ('model.py', 'examples.py', 'independent_audit.py')},
    'optimization_level': sys.flags.optimize,
    'checks': dict(sorted(COUNTS.items())),
    'total': sum(COUNTS.values()),
    'result': 'PASS for enumerated finite ordinary-value contract',
}, indent=2))

# Report the known nonreflexive-outcome probe independently. A conforming fix
# rejects NaN, or else keeps the generating world when observing its outcome.
nan = float('nan')
try:
    nan_table = {'a': nan, 'b': 'ordinary'}
    cell_result = partition(h, nan_table)
    surviving = consistent(h, {'t': nan_table}, [('t', nan_table['a'])])
    if 'a' not in surviving:
        print('KNOWN FINDING: NaN accepted; generated observation loses generating world')
        print('partition =', cell_result, '; survivors =', surviving)
        raise AssertionError('A generated observation must retain its generating world')
    else:
        print('NaN outcome probe: generating-world invariant preserved')
except ValueError:
    print('NaN outcome probe: rejected at validation boundary')
