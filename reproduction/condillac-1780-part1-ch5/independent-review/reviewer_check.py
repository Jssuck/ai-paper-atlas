#!/usr/bin/env python3
"""Independent reviewer checks. Every check survives python -O and -OO.

No imports of author tests/oracle and no assert statements. The finite oracle
uses pairwise equality constraints, not the implementation's grouping method.
Use --unit-only for isolated, fast semantic mutation checks.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sys
import unittest

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--target', type=Path, default=Path(__file__).resolve().parent.parent)
PARSER.add_argument('--unit-only', action='store_true')
ARGS = PARSER.parse_args()
sys.path.insert(0, str(ARGS.target.resolve()))
from finite_model import FiniteModel
from ratios import exact, response, infer_product, calibrated_coefficient, equivalent_parameters, relative_coefficient


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def partition(model):
    return frozenset(frozenset(group) for group in model.fibers())


class ReviewerFiniteTests(unittest.TestCase):
    def setUp(self):
        self.m = FiniteModel.from_rows(('x',), {'none': (0,), 'a': (1,), 'b': (1,), 'ab': (1,)})
        self.ident = {s: s for s in self.m.states}
        self.exists = {'none': False, 'a': True, 'b': True, 'ab': True}

    def test_one_question_can_be_identified_while_identity_is_not(self):
        self.assertEqual(self.m.answer((1,), self.exists).status, 'identified')
        self.assertEqual(self.m.answer((1,), self.ident).status, 'ambiguous')

    def test_two_causes_not_inferred_from_existence(self):
        self.assertEqual(self.m.answer((1,), {'none': 0, 'a': 1, 'b': 1, 'ab': 2}).values, (1, 2))

    def test_fiber_contains_all_and_only_matching_states(self):
        self.assertEqual(self.m.candidates((1,)), ('a', 'b', 'ab'))
        self.assertEqual(partition(self.m), frozenset((frozenset(('none',)), frozenset(('a', 'b', 'ab')))))

    def test_empty_fiber_is_inconsistent_not_identified(self):
        a = self.m.answer((9,), self.exists)
        self.assertEqual((a.status, a.candidates, a.values), ('inconsistent', (), ()))

    def test_empty_model_global_vacuity_and_local_conflict(self):
        m = FiniteModel.from_rows(('x',), {})
        self.assertTrue(m.globally_identifiable({}))
        self.assertEqual(m.answer((0,), {}).status, 'inconsistent')
        self.assertEqual(m.fibers(), ())

    def test_no_observation_columns_provide_no_discrimination(self):
        m = FiniteModel.from_rows((), {'a': (), 'b': ()})
        self.assertEqual(m.answer((), {'a': 0, 'b': 1}).status, 'ambiguous')
        self.assertEqual(m.answer((), {'a': 7, 'b': 7}).status, 'identified')

    def test_names_do_not_change_observations(self):
        named = self.m.with_labels({s: 'unique-' + s for s in self.m.states})
        self.assertEqual(named.signatures, self.m.signatures)
        self.assertEqual(named.answer((1,), self.ident), self.m.answer((1,), self.ident))
        self.assertEqual(named.states, self.m.states)

    def test_bijective_state_renaming_transports_query_and_candidates(self):
        ren = {s: 'renamed-' + s for s in self.m.states}
        m = FiniteModel.from_rows(('x',), {ren[s]: row for s, row in zip(self.m.states, self.m.signatures)})
        ans = m.answer((1,), {ren[s]: self.ident[s] for s in self.m.states})
        self.assertEqual(ans.candidates, tuple(ren[s] for s in ('a', 'b', 'ab')))
        self.assertEqual(ans.values, ('a', 'b', 'ab'))
        self.assertEqual(ans.status, 'ambiguous')

    def test_added_observation_preserves_old_coordinates(self):
        ext = self.m.append_observation('z', {'none': 9, 'a': 7, 'b': 8, 'ab': 7})
        self.assertEqual(ext.signatures, ((0, 9), (1, 7), (1, 8), (1, 7)))
        self.assertTrue(ext.refines(self.m))
        self.assertFalse(self.m.refines(ext))
        self.assertEqual(ext.candidates((1, 7)), ('a', 'ab'))

    def test_derived_and_constant_observations_do_not_split(self):
        for values in ({s: 5 for s in self.m.states}, {s: 11 * row[0] - 7 for s, row in zip(self.m.states, self.m.signatures)}):
            ext = self.m.append_observation('z', values)
            self.assertEqual(partition(ext), partition(self.m))
            self.assertTrue(self.m.refines(ext))

    def test_added_probe_can_identify_attribute_without_number(self):
        ext = self.m.append_observation('z', {'none': 0, 'a': 7, 'b': 8, 'ab': 7})
        self.assertEqual(ext.answer((1, 7), {'none': 'nil', 'a': 'red', 'b': 'blue', 'ab': 'red'}).status, 'identified')
        self.assertEqual(ext.answer((1, 7), {'none': 0, 'a': 1, 'b': 1, 'ab': 2}).status, 'ambiguous')

    def test_assumption_filters_without_adding_data(self):
        m = self.m.restrict(('b',))
        self.assertEqual((m.columns, m.states, m.signatures), (('x',), ('b',), ((1,),)))
        self.assertEqual(m.answer((1,), {'b': 'b'}).status, 'identified')
        self.assertEqual(self.m.states, ('none', 'a', 'b', 'ab'))

    def test_wrong_assumption_can_conflict_with_observation(self):
        m = self.m.restrict(('none',))
        self.assertEqual(m.states, ('none',))
        self.assertEqual(m.answer((1,), {'none': False}).status, 'inconsistent')

    def test_relaxing_candidate_assumption_can_destroy_identification(self):
        wide = FiniteModel.from_rows(('x',), {'caused': (1,), 'uncaused': (1,)})
        self.assertEqual(wide.answer((1,), {'caused': True, 'uncaused': False}).status, 'ambiguous')

    def test_refinement_ignores_row_order_not_domain(self):
        reorder = FiniteModel.from_rows(('renamed-column',), dict(reversed(list(zip(self.m.states, self.m.signatures)))))
        self.assertTrue(self.m.refines(reorder))
        self.assertTrue(reorder.refines(self.m))
        with self.assertRaises(ValueError):
            self.m.refines(self.m.restrict(('a',)))

    def test_total_query_domain_is_required(self):
        for q in ({'a': 1}, {**self.exists, 'extra': True}):
            with self.assertRaises(ValueError):
                self.m.answer((1,), q)
            with self.assertRaises(ValueError):
                self.m.globally_identifiable(q)

    def test_metadata_and_probe_domains_are_total(self):
        for operation in (lambda: self.m.with_labels({'a': 'name'}), lambda: self.m.append_observation('z', {'a': 1}), lambda: self.m.restrict(('missing',))):
            with self.assertRaises(ValueError):
                operation()

    def test_exact_integer_signatures_reject_bool_float_and_shape_errors(self):
        for row in ((True,), (1.0,)):
            with self.assertRaises(TypeError):
                self.m.candidates(row)
        for row in ((), (1, 2), [1]):
            with self.assertRaises(ValueError):
                self.m.candidates(row)

    def test_constructor_rejects_mutability_duplicate_and_invalid_identifiers(self):
        with self.assertRaises(TypeError):
            FiniteModel(['x'], (), (), ())
        for args in ((('x', 'x'), (), (), ()), (('x',), ('a', 'a'), ((0,), (1,)), ('a', 'a')), (('',), (), (), ()), (('x',), ('a',), (), ('a',))):
            with self.assertRaises(ValueError):
                FiniteModel(*args)
        with self.assertRaises(TypeError):
            self.m.with_labels(dict.fromkeys(self.m.states, 5))
        with self.assertRaises(TypeError):
            self.m.answer((1,), dict.fromkeys(self.m.states, []))

    def test_reject_duplicate_probe_and_noninteger_probe(self):
        with self.assertRaises(ValueError):
            self.m.append_observation('x', dict.fromkeys(self.m.states, 1))
        with self.assertRaises(TypeError):
            self.m.append_observation('z', dict.fromkeys(self.m.states, F(1)))


class ReviewerRatioTests(unittest.TestCase):
    def test_exact_domain_rejects_float_bool_and_string(self):
        for x in (0.1, True, '1/10', None):
            with self.assertRaises(TypeError):
                exact(x)
        self.assertEqual(exact(F(1, 10)), F(1, 10))

    def test_nonpositive_parameters_rejected(self):
        for bad in (0, -1, F(-1, 3)):
            for call in (lambda: response((1,), bad), lambda: response((1,), 1, bad), lambda: calibrated_coefficient((1,), (1,), bad), lambda: equivalent_parameters(1, 1, bad)):
                with self.assertRaises(ValueError):
                    call()

    def test_fraction_response_exact_not_float(self):
        out = response((F(1, 10), -3, 0), F(7, 3), F(9, 14))
        self.assertEqual(out, (F(3, 20), F(-9, 2), F(0)))
        self.assertTrue(all(type(v) is F for v in out))

    def test_nonzero_input_identifies_product(self):
        r = infer_product((0, F(2, 3), -3), (0, 4, -18))
        self.assertEqual((r.status, r.product), ('identified', F(6)))

    def test_zero_only_input_does_not_identify(self):
        r = infer_product((0, 0), (0, 0))
        self.assertEqual((r.status, r.product), ('uninformative', None))
        with self.assertRaises(ValueError):
            calibrated_coefficient((0,), (0,), 2)

    def test_zero_input_nonzero_output_is_conflict(self):
        r = infer_product((0, 1), (1, 6))
        self.assertEqual((r.status, r.product), ('inconsistent', None))

    def test_conflicting_ratios_are_inconsistent(self):
        self.assertEqual(infer_product((1, 2), (6, 13)).status, 'inconsistent')
        self.assertEqual(infer_product((1, 1), (6, 7)).status, 'inconsistent')

    def test_nonpositive_product_conflicts_with_positive_parameters(self):
        for outputs in ((0,), (-1,)):
            self.assertEqual(infer_product((1,), outputs).status, 'inconsistent')

    def test_empty_and_mismatched_data_are_rejected(self):
        for inputs, outputs in (((), ()), ((1,), ()), ((1,), (1, 2))):
            with self.assertRaises(ValueError):
                infer_product(inputs, outputs)

    def test_known_gain_is_divisor_not_default_one(self):
        self.assertEqual(calibrated_coefficient((1, 2), (6, 12), 2), F(3))
        self.assertEqual(calibrated_coefficient((1,), (6,), F(3, 2)), F(4))

    def test_parameter_scaling_preserves_every_selected_input(self):
        for scale in (F(1, 11), F(1), F(13, 2)):
            k, g = equivalent_parameters(F(3, 2), F(7, 5), scale)
            self.assertEqual(k, F(3, 2) * scale)
            self.assertEqual(g, F(7, 5) / scale)
            self.assertEqual(response((-3, 0, F(7, 9)), k, g), response((-3, 0, F(7, 9)), F(3, 2), F(7, 5)))

    def test_common_gain_relative_coefficient(self):
        self.assertEqual(relative_coefficient(iter((1, 2)), (6, 12), (10, 20)), F(3, 5))

    def test_unequal_gain_is_a_counterexample_to_unconditional_ratio(self):
        value = relative_coefficient((1,), (6,), (15,))
        self.assertEqual(value, F(2, 5))
        self.assertNotEqual(value, F(3, 5))

    def test_unidentified_relative_comparison_rejected(self):
        for args in (((0,), (0,), (0,)), ((1, 2), (6, 13), (10, 20))):
            self.assertTrue(infer_product(args[0], args[1]).status != 'identified' or infer_product(args[0], args[2]).status != 'identified')
            with self.assertRaises(ValueError):
                relative_coefficient(*args)

    def test_iterators_and_negative_inputs_supported(self):
        self.assertEqual(response(iter((-1, 0, 2)), 3, 2), (F(-6), F(0), F(12)))
        self.assertEqual(infer_product(iter((-1, 2)), iter((-6, 12))).product, F(6))


def run_finite_oracle():
    """Enumerate bounded models, using independent pairwise constraints."""
    counts = Counter()
    alphabet = tuple(product((0, 1), repeat=2))
    for n in range(5):
        states = tuple('h' + str(i) for i in range(n))
        for rows in product(alphabet, repeat=n):
            m = FiniteModel.from_rows(('x', 'y'), dict(zip(states, rows)))
            expected_pairs = {(i, j) for i in range(n) for j in range(n) if rows[i] == rows[j]}
            actual_pairs = {(states.index(a), states.index(b)) for group in m.fibers() for a in group for b in group}
            require(actual_pairs == expected_pairs, 'fiber equivalence relation')
            counts['models'] += 1
            for vals in product((0, 1, 2), repeat=n):
                q = dict(zip(states, vals))
                expected_global = all(vals[i] == vals[j] for i, j in expected_pairs)
                require(m.globally_identifiable(q) == expected_global, 'pairwise global oracle')
                for obs in alphabet + ((9, 9),):
                    matching = [i for i in range(n) if rows[i] == obs]
                    expected_status = ('inconsistent' if not matching else 'identified' if all(vals[i] == vals[matching[0]] for i in matching) else 'ambiguous')
                    a = m.answer(obs, q)
                    require(a.status == expected_status, 'local status')
                    require(a.candidates == tuple(states[i] for i in matching), 'local candidates')
                    require(set(a.values) == {vals[i] for i in matching}, 'local values')
                    counts['local_answers'] += 1
                counts['ternary_queries'] += 1
            for extra in product((0, 1, 2), repeat=n):
                e = m.append_observation('z', dict(zip(states, extra)))
                require(e.signatures == tuple(rows[i] + (extra[i],) for i in range(n)), 'extension preserves data')
                require(e.refines(m), 'extension refinement')
                require(m.refines(e) == all(extra[i] == extra[j] for i, j in expected_pairs), 'strictness of refinement')
                counts['ternary_extensions'] += 1
            for mask in product((False, True), repeat=n):
                allowed = [states[i] for i in range(n) if mask[i]]
                r = m.restrict(allowed)
                require(r.columns == m.columns, 'restriction is not a measurement')
                require(r.states == tuple(allowed), 'restriction state order')
                require(r.signatures == tuple(rows[i] for i in range(n) if mask[i]), 'restriction keeps signatures')
                for obs in alphabet + ((9, 9),):
                    require(r.candidates(obs) == tuple(states[i] for i in range(n) if mask[i] and rows[i] == obs), 'assumption and evidence intersection')
                    counts['restricted_candidate_answers'] += 1
                counts['assumption_subsets'] += 1
            for labels in ({s: '' for s in states}, {s: 'same' for s in states}, {s: 'unique-' + s for s in states}):
                named = m.with_labels(labels)
                require(named.signatures == m.signatures and partition(named) == partition(m), 'metadata rename invariance')
                counts['metadata_renamings'] += 1
            ren = {s: 'renamed-' + s for s in states}
            renamed = FiniteModel.from_rows(('x', 'y'), {ren[s]: row for s, row in zip(states, rows)})
            for obs in alphabet + ((9, 9),):
                require(renamed.candidates(obs) == tuple(ren[s] for s in m.candidates(obs)), 'state renaming covariance')
                counts['state_renaming_answers'] += 1
    return dict(counts)


def run_rational_oracle():
    counts = Counter()
    params = sorted({F(a, b) for a in range(1, 5) for b in range(1, 5)})
    inputs = sorted({F(a, b) for a in range(-4, 5) for b in range(1, 5)})
    for k, g in product(params, repeat=2):
        expected = tuple(F(g.numerator * k.numerator * u.numerator, g.denominator * k.denominator * u.denominator) for u in inputs)
        actual = response(inputs, k, g)
        require(actual == expected, 'integer numerator/denominator response oracle')
        require(all(type(x) is F for x in actual), 'Fraction-only output')
        require(infer_product(inputs, actual).product == F(k.numerator * g.numerator, k.denominator * g.denominator), 'product inference')
        require(calibrated_coefficient(inputs, actual, g) == k, 'calibration')
        counts['parameter_pairs'] += 1
        counts['responses'] += len(inputs)
        for c in params:
            kp, gp = equivalent_parameters(k, g, c)
            require(kp == k * c and gp == g / c, 'documented scale map')
            require(response(inputs, kp, gp) == expected, 'scale invariance')
            counts['scale_transformations'] += 1
            counts['scaled_responses'] += len(inputs)
    return {'positive_parameter_values': len(params), 'input_values': len(inputs), **dict(counts)}


def main():
    suite = unittest.TestSuite((unittest.defaultTestLoader.loadTestsFromTestCase(ReviewerFiniteTests), unittest.defaultTestLoader.loadTestsFromTestCase(ReviewerRatioTests)))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    summary = {'result': 'PASS', 'optimization': sys.flags.optimize, 'reviewer_unit_tests': result.testsRun}
    if not ARGS.unit_only:
        summary['finite_oracle'] = run_finite_oracle()
        summary['rational_oracle'] = run_rational_oracle()
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
