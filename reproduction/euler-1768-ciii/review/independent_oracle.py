#!/usr/bin/env python3
"""Independent quantifier/set oracle. Run from the project root.

The expected models, formulas, candidate inventory and matching orbits are
constructed here without using the implementation under test. Imports from the
project are restricted to the comparison side of assertions. No dependencies,
network access, installation, or absolute paths are included in result files.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import platform
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import euler_logic as sut
import reproduce as cli

TERMS = ('A', 'B', 'C')
KINDS = ('A', 'E', 'I', 'O')
REGIMES = ('empty_terms_allowed', 'all_terms_nonempty', 'A_nonempty_only')
# Independent transcription of the nine formulas, without SUT objects.
CATALOG = {
    'A1': (('A', 'A', 'B'), ('A', 'C', 'A'), ('A', 'C', 'B')),
    'A2': (('A', 'A', 'B'), ('I', 'C', 'A'), ('I', 'C', 'B')),
    'A3': (('A', 'A', 'B'), ('E', 'C', 'B'), ('E', 'C', 'A')),
    'A4': (('A', 'A', 'B'), ('O', 'C', 'B'), ('O', 'C', 'A')),
    'A5': (('A', 'A', 'B'), ('A', 'B', 'C'), ('I', 'C', 'A')),
    'E1': (('E', 'A', 'B'), ('A', 'C', 'B'), ('E', 'C', 'A')),
    'E2': (('E', 'A', 'B'), ('A', 'C', 'A'), ('E', 'C', 'B')),
    'E3': (('E', 'A', 'B'), ('I', 'C', 'A'), ('O', 'C', 'B')),
    'E4': (('E', 'A', 'B'), ('I', 'C', 'B'), ('O', 'C', 'A')),
}


def make_model(raw):
    # Arithmetic digit extraction rather than SUT bit masks. A is the first
    # membership coordinate, varying fastest; C is the last, varying slowest.
    memberships = [(a, b, c) for c, b, a in itertools.product((False, True), repeat=3)]
    occupied = [i for i in range(8) if (raw // (2 ** i)) % 2]
    if not occupied:
        occupied = [0]  # A nonempty universe containing only an outside witness.
    universe = tuple('w' + str(i) for i in occupied)
    terms = {t: {('w' + str(i)) for i in occupied if memberships[i][j]}
             for j, t in enumerate(TERMS)}
    return universe, terms


MODELS = {raw: make_model(raw) for raw in range(256)}


def quantify(statement, model):
    """Direct first-order semantics, independent of region algebra."""
    kind, subject, predicate = statement
    universe, terms = model
    x, y = terms[subject], terms[predicate]
    if kind == 'A':
        return all(w not in x or w in y for w in universe)
    if kind == 'E':
        return all(not (w in x and w in y) for w in universe)
    if kind == 'I':
        return any(w in x and w in y for w in universe)
    if kind == 'O':
        return any(w in x and w not in y for w in universe)
    raise ValueError(kind)


def set_semantics(statement, model):
    kind, subject, predicate = statement
    _, terms = model
    x, y = terms[subject], terms[predicate]
    return {'A': x.issubset(y), 'E': not x.intersection(y),
            'I': bool(x.intersection(y)), 'O': bool(x.difference(y))}[kind]


def eligible(model, regime):
    _, terms = model
    if regime == 'empty_terms_allowed':
        return True
    if regime == 'all_terms_nonempty':
        return all(terms.values())
    if regime == 'A_nonempty_only':
        return bool(terms['A'])
    raise ValueError(regime)


def oracle(argument, regime):
    selected, premise_masks, failure_masks = [], [], []
    for raw, model in MODELS.items():
        if not eligible(model, regime):
            continue
        selected.append(raw)
        if all(quantify(p, model) for p in argument[:-1]):
            premise_masks.append(raw)
            if not quantify(argument[-1], model):
                failure_masks.append(raw)
    return selected, premise_masks, failure_masks


def candidates(first_kind):
    # Generate by choosing the second relation first, then checking which
    # endpoint is absent. This does not call or copy the SUT generator.
    second_relations = [(k, x, y) for k in KINDS for x, y in
                        itertools.permutations(TERMS, 2) if 'C' in (x, y)]
    result = []
    for second in second_relations:
        other = next(t for t in ('A', 'B') if t not in second[1:])
        for conclusion_kind in KINDS:
            for x, y in (('C', other), (other, 'C')):
                result.append(((first_kind, 'A', 'B'), second,
                               (conclusion_kind, x, y)))
    return result


def conversions(argument):
    choices = []
    for kind, x, y in argument:
        original = (kind, x, y)
        choices.append((original, (kind, y, x)) if kind in ('E', 'I') else (original,))
    return set(itertools.product(*choices))


def renamed(argument, permutation):
    mapping = dict(zip(TERMS, permutation))
    return tuple((kind, mapping[x], mapping[y]) for kind, x, y in argument)


def orbit(argument, exchange):
    result = set()
    for permutation in itertools.permutations(TERMS):
        for variant in conversions(renamed(argument, permutation)):
            result.add(variant)
            if exchange:
                result.add((variant[1], variant[0], variant[2]))
    return result


ORBITS = {exchange: {label: orbit(argument, exchange)
                    for label, argument in CATALOG.items()} for exchange in (False, True)}


def matches(argument, exchange=False):
    return tuple(label for label, forms in ORBITS[exchange].items() if argument in forms)


def conversion_key(argument):
    # Explicit orbit minimum, rather than the SUT canonical-sort algorithm.
    return min(conversions(argument))


def sut_argument(argument, label='independent'):
    statements = tuple(sut.Statement(*s) for s in argument)
    return sut.Argument(label, statements[:-1], statements[-1])


def from_sut(argument):
    return tuple((s.kind, s.subject, s.predicate)
                 for s in argument.premises + (argument.conclusion,))


def parse_statement(value):
    match = re.fullmatch(r'([AEIO])\(([ABC]),([ABC])\)', value)
    if not match:
        raise ValueError(value)
    return match.groups()


def formula(argument):
    values = ['%s(%s,%s)' % s for s in argument]
    return ' & '.join(values[:-1]) + ' => ' + values[-1]


RESULTS = {'checks': {}, 'nine_forms': {}, 'expanded_inventory': [], 'focused_cases': {}}


class IndependentReview(unittest.TestCase):
    def compare_argument(self, argument, regime):
        selected, premises, failures = oracle(argument, regime)
        actual = sut.check_argument(sut_argument(argument), regime)
        self.assertEqual(actual['tested_raw_masks'], len(selected))
        distinct = len({MODELS[raw][0] for raw in selected})
        self.assertEqual(actual['distinct_nonempty_universe_models'], distinct)
        self.assertEqual(actual['premise_satisfying_raw_masks'], len(premises))
        self.assertEqual(actual['distinct_premise_satisfying_models'], len({MODELS[r][0] for r in premises}))
        self.assertEqual(actual['distinct_counterexample_models'], len({MODELS[r][0] for r in failures}))
        self.assertEqual(actual['premises_satisfiable'], bool(premises))
        self.assertEqual(actual['valid'], not failures)
        self.assertEqual(actual['counterexample_raw_masks'], failures)
        witness = actual['first_counterexample']
        if failures:
            self.assertEqual(witness['raw_mask'], failures[0])
            model = (tuple(witness['universe']), {k: set(v) for k, v in witness['terms'].items()})
            self.assertTrue(all(quantify(p, model) for p in argument[:-1]))
            self.assertFalse(quantify(argument[-1], model))
            self.assertEqual(model, MODELS[failures[0]])
        else:
            self.assertIsNone(witness)
        return {'valid': not failures, 'premise_raw_count': len(premises),
                'counterexample_raw_masks': failures,
                'counterexample_distinct_count': len({MODELS[r][0] for r in failures})}

    def test_01_model_space_and_all_atomic_relations(self):
        self.assertEqual(len(MODELS), 256)
        self.assertEqual(len({model[0] for model in MODELS.values()}), 255)
        self.assertEqual(MODELS[0], MODELS[1])
        self.assertEqual(MODELS[0], (('w0',), {'A': set(), 'B': set(), 'C': set()}))
        expected_counts = {'empty_terms_allowed': (256, 255),
                           'all_terms_nonempty': (218, 218), 'A_nonempty_only': (240, 240)}
        count = 0
        for raw, model in MODELS.items():
            actual = sut.RegionModel(raw).as_sets()
            self.assertEqual(tuple(actual['universe']), model[0])
            self.assertEqual({k: set(v) for k, v in actual['terms'].items()}, model[1])
            self.assertEqual(actual['outside_witness_added'], raw == 0)
            for statement in itertools.product(KINDS, TERMS, TERMS):
                expected = quantify(statement, model)
                self.assertEqual(expected, set_semantics(statement, model))
                self.assertEqual(sut.RegionModel(raw).evaluate(sut.Statement(*statement)), expected)
                self.assertEqual(sut.evaluate_sets(sut.Statement(*statement), model[1]), expected)
                count += 1
        for regime, counts in expected_counts.items():
            selected = [r for r, model in MODELS.items() if eligible(model, regime)]
            self.assertEqual((len(selected), len({MODELS[r][0] for r in selected})), counts)
            self.assertEqual([m.raw_mask for m in sut.models(regime)], selected)
        RESULTS['checks']['atomic_model_statement_combinations'] = count
        RESULTS['model_counts'] = {k: {'raw': v[0], 'distinct': v[1]} for k, v in expected_counts.items()}

    def test_02_nine_independently_transcribed_forms(self):
        self.assertEqual({a.label: from_sut(a) for a in sut.CATALOG}, CATALOG)
        for regime in REGIMES:
            RESULTS['nine_forms'][regime] = {}
            for label, argument in CATALOG.items():
                result = self.compare_argument(argument, regime)
                self.assertEqual(result['valid'], regime != 'empty_terms_allowed' or label != 'A5')
                RESULTS['nine_forms'][regime][label] = result
        a5 = RESULTS['nine_forms']['empty_terms_allowed']['A5']
        self.assertEqual(a5['counterexample_raw_masks'], [0, 1, 16, 17, 64, 65, 80, 81])
        self.assertEqual(a5['counterexample_distinct_count'], 7)
        RESULTS['checks']['catalog_regime_combinations'] = 27

    def test_03_expanded_256_candidates_and_matching(self):
        comparisons = 0
        for first in ('A', 'E'):
            forms = candidates(first)
            self.assertEqual(len(forms), 128)
            self.assertEqual(len(set(forms)), 128)
            self.assertEqual(set(forms), {from_sut(a) for a in sut.fixed_first_candidates(first)})
            for regime in REGIMES:
                valid = []
                for argument in forms:
                    result = self.compare_argument(argument, regime)
                    self.assertGreater(result['premise_raw_count'], 0)
                    if result['valid']:
                        valid.append(argument)
                    for exchange in (False, True):
                        self.assertEqual(sut.catalog_matches(sut_argument(argument), exchange),
                                         matches(argument, exchange), formula(argument))
                    comparisons += 1
                expected = {
                    'first': first, 'regime': regime, 'candidate_count': len(forms),
                    'valid': len(valid), 'EI_classes': len({conversion_key(a) for a in valid}),
                    'matched_ordered': sum(bool(matches(a)) for a in valid),
                    'matched_unordered': sum(bool(matches(a, True)) for a in valid),
                    'additional_unordered': sorted(formula(a) for a in valid if not matches(a, True)),
                }
                actual = sut.audit_fixed_first(first, regime)
                for field, name in (('candidate_count', 'candidate_count'), ('valid', 'valid_ordered_candidates'),
                                    ('EI_classes', 'valid_classes_modulo_E_I_conversion_only'),
                                    ('matched_ordered', 'valid_candidates_matching_displayed_ordered'),
                                    ('matched_unordered', 'valid_candidates_matching_displayed_unordered')):
                    self.assertEqual(expected[field], actual[name])
                self.assertEqual(expected['additional_unordered'],
                                 sorted(actual['additional_valid_candidates_unordered']))
                RESULTS['expanded_inventory'].append(expected)
        RESULTS['checks']['candidate_regime_combinations'] = comparisons

    def test_04_conversions_permutations_and_premise_exchange(self):
        all_forms, variant_count = set(), 0
        for label, argument in CATALOG.items():
            variants = conversions(argument)
            self.assertEqual(variants, {from_sut(a) for a in sut.ei_conversion_variants(sut_argument(argument))})
            variant_count += len(variants)
            for regime in REGIMES:
                expected_failures = oracle(argument, regime)[2]
                for variant in variants:
                    self.assertEqual(oracle(variant, regime)[2], expected_failures)
            all_forms.update(orbit(argument, True))
        for argument in all_forms:
            for exchange in (False, True):
                self.assertEqual(sut.catalog_matches(sut_argument(argument), exchange), matches(argument, exchange))
            for regime in REGIMES:
                # A_nonempty_only is tied to the actual name A; do not assume
                # this named side condition is invariant under term renaming.
                self.compare_argument(argument, regime)
        self.assertEqual(variant_count, 28)
        chain = (('A', 'A', 'B'), ('A', 'B', 'C'), ('A', 'A', 'C'))
        self.assertEqual(matches(chain), ())
        self.assertEqual(matches(chain, True), ('A1',))
        for kind in KINDS:
            reverse = ((kind, 'A', 'B'), (kind, 'B', 'A'))
            self.assertEqual(not oracle(reverse, 'empty_terms_allowed')[2], kind in ('E', 'I'))
        RESULTS['checks']['explicit_EI_variants'] = variant_count
        RESULTS['checks']['distinct_renamed_converted_premise_exchanged_formulas'] = len(all_forms)
        RESULTS['checks']['transformed_formula_regime_combinations'] = 3 * len(all_forms)

    def test_05_focused_existence_and_missing_cases(self):
        common = (('A', 'A', 'B'), ('A', 'A', 'C'), ('I', 'C', 'B'))
        witness_transfer = (('A', 'A', 'B'), ('O', 'A', 'C'), ('O', 'B', 'C'))
        for key, argument in (('common_subject', common), ('negative_witness_transfer', witness_transfer)):
            self.assertEqual(matches(argument), ())
            self.assertEqual(matches(argument, True), ())
            RESULTS['focused_cases'][key] = {'formula': formula(argument), 'matches_ordered': [],
                                            'matches_unordered': [], 'regimes': {}}
            for regime in REGIMES:
                result = self.compare_argument(argument, regime)
                self.assertEqual(result['valid'], key == 'negative_witness_transfer' or regime != 'empty_terms_allowed')
                RESULTS['focused_cases'][key]['regimes'][regime] = result
        a5 = CATALOG['A5']
        for model in MODELS.values():
            if all(quantify(p, model) for p in a5[:-1]):
                self.assertEqual(quantify(a5[-1], model), bool(model[1]['A']))
        # With the actual names fixed, neither B existence nor C existence
        # suffices to repair A5. A=empty, B=C={w6} is an explicit witness.
        countermodel = MODELS[64]
        self.assertTrue(countermodel[1]['B'] and countermodel[1]['C'])
        self.assertTrue(all(quantify(p, countermodel) for p in a5[:-1]))
        self.assertFalse(quantify(a5[-1], countermodel))
        for regime in REGIMES:
            self.assertTrue(oracle((('I', 'A', 'B'), ('O', 'A', 'B')), regime)[2])

    def test_06_named_examples_are_true_as_reported(self):
        examples = sut.explicit_examples()
        total = 0
        for group, value in examples.items():
            for example in value if isinstance(value, list) else [value]:
                model = (tuple(example['universe']), {k: set(v) for k, v in example['terms'].items()})
                self.assertTrue(model[0])
                self.assertTrue(all(values <= set(model[0]) for values in model[1].values()))
                self.assertEqual(example['all_premises_true'],
                                 all(quantify(parse_statement(p), model) for p in example['premises']))
                if 'conclusion' in example:
                    self.assertEqual(example['conclusion_true'], quantify(parse_statement(example['conclusion']), model))
                if 'C_to_B_relations' in example:
                    self.assertEqual(example['C_to_B_relations'],
                                     {k: quantify((k, 'C', 'B'), model) for k in KINDS})
                total += 1
        no_relation = (('A', 'A', 'B'), ('E', 'C', 'A'))
        for kind in KINDS:
            self.assertTrue(oracle(no_relation + ((kind, 'C', 'B'),), 'all_terms_nonempty')[2])
        # Reversing the endpoint direction changes the question: A existence
        # does imply Some B is not C. Preserve this qualification in reporting.
        self.assertFalse(oracle(no_relation + (('O', 'B', 'C'),), 'A_nonempty_only')[2])
        RESULTS['checks']['named_examples'] = total

    def test_07_small_universe_quotient_with_repeated_witnesses(self):
        count = 0
        for size in (1, 2, 3):
            universe = tuple(range(size))
            subsets = [{i for i in universe if membership[i]}
                       for membership in itertools.product((False, True), repeat=size)]
            for a, b, c in itertools.product(subsets, repeat=3):
                model = (universe, dict(zip(TERMS, (a, b, c))))
                represented_types = {tuple(w in term for term in (a, b, c)) for w in universe}
                quotient_universe = tuple(represented_types)
                quotient_terms = {t: {v for v in quotient_universe if v[i]} for i, t in enumerate(TERMS)}
                quotient = (quotient_universe, quotient_terms)
                for statement in itertools.product(KINDS, TERMS, TERMS):
                    self.assertEqual(quantify(statement, model), quantify(statement, quotient))
                    self.assertEqual(quantify(statement, model), set_semantics(statement, model))
                count += 1
        RESULTS['checks']['arbitrary_small_models'] = count
        RESULTS['checks']['quotient_statement_combinations'] = count * 36

    def test_08_generated_report_matches_current_sources(self):
        saved = json.loads((ROOT / 'results/report.json').read_text(encoding='utf-8'))
        current = cli.build_report()
        self.assertEqual(saved, current)
        self.assertEqual((ROOT / 'results/report.txt').read_text(encoding='utf-8'), cli.render_text(current))
        environment = json.loads((ROOT / 'results/environment.json').read_text(encoding='utf-8'))
        for relative, expected in environment['source_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), expected, relative)
        self.assertFalse(environment['network_used_by_reproduction'])
        RESULTS['checks']['saved_report_and_source_hashes_current'] = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('review/independent_results.json'))
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(IndependentReview)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    RESULTS['environment'] = {
        'recorded_utc': datetime.now(timezone.utc).isoformat(),
        'python': sys.version, 'implementation': platform.python_implementation(),
        'platform': platform.platform(), 'machine': platform.machine(),
        'dependencies': 'Python standard library only; no packages installed',
        'network_used': False,
    }
    sources = ['euler_logic.py', 'reproduce.py', 'tests/test_euler_logic.py',
               'review/independent_oracle.py', 'review/run_review.sh', 'review/review.zh-CN.md',
               'README.md', 'PROOF.md']
    RESULTS['source_sha256'] = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                                for p in sources if (ROOT / p).is_file()}
    RESULTS['test_groups'] = result.testsRun
    RESULTS['passed'] = result.wasSuccessful()
    RESULTS['failures'] = len(result.failures)
    RESULTS['errors'] = len(result.errors)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(RESULTS, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('\nIndependent oracle summary:')
    print(json.dumps({'passed': RESULTS['passed'], 'checks': RESULTS['checks'],
                      'model_counts': RESULTS.get('model_counts'),
                      'inventory_counts': [{k: v for k, v in row.items() if k != 'additional_unordered'}
                                           for row in RESULTS['expanded_inventory']]},
                     ensure_ascii=False, indent=2, sort_keys=True))
    print('Saved independent results:', args.output.as_posix())
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
