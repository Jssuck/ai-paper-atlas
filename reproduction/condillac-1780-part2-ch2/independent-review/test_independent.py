"""Independent stdlib finite-relation oracle and boundary checks.

Expected values are built from raw fixtures, never the model's orders/encode.
Use run_review.py to exercise real normal/-O/-OO subprocesses and mutations.
"""
from dataclasses import FrozenInstanceError
from itertools import permutations, product
import json
import math
import sys
import unittest

from model import Language, pack, unpack, version_space

COVERAGE = {}


def independent_orders(labels, edges):
    """Enumerate bijective ranks and check every raw edge."""
    accepted = []
    for positions in permutations(range(len(labels))):
        rank = dict(zip(labels, positions))
        if not any(rank[left] >= rank[right] for left, right in edges):
            accepted.append(tuple(sorted(labels, key=rank.__getitem__)))
    return set(accepted)


def relation(schema, edges, codes):
    """Explicit wire -> meanings relation, using only fixture inputs."""
    labels = tuple(schema)
    outputs = {}
    for assignment in product(*(schema[label] for label in labels)):
        values = dict(zip(labels, assignment))
        for order in independent_orders(labels, edges):
            wire = tuple(codes[(label, values[label])] for label in order)
            outputs.setdefault(wire, set()).add(assignment)
    return outputs


def relation_prefixes(outputs):
    expected = {}
    for wire, meanings in outputs.items():
        for length in range(len(wire) + 1):
            expected.setdefault(wire[:length], set()).update(meanings)
    return expected


class IndependentTests(unittest.TestCase):
    def test_all_directed_contexts_up_to_four_features(self):
        total = dags = cycles = 0
        expected_dags = (1, 3, 25, 543)
        for n in range(1, 5):
            labels = tuple('f' + str(i) for i in range(n))
            possible = tuple(permutations(labels, 2))
            accepted = 0
            for mask in range(1 << len(possible)):
                edges = tuple(edge for bit, edge in enumerate(possible) if mask & (1 << bit))
                expected = independent_orders(labels, edges)
                total += 1
                if not expected:
                    cycles += 1
                    with self.assertRaises(ValueError):
                        Language(dict.fromkeys(labels, ('v',)), edges)
                    continue
                dags += 1
                accepted += 1
                actual = Language(dict.fromkeys(labels, ('v',)), edges).orders
                self.assertEqual(set(actual), expected)
                self.assertEqual(len(actual), len(expected), 'no duplicate orders')
            self.assertEqual(accepted, expected_dags[n - 1])
        self.assertEqual((total, dags, cycles), (4165, 572, 3593))
        COVERAGE['directed_graphs'] = {'total': total, 'DAG': dags, 'cyclic_rejected': cycles}

    def test_joint_context_and_colliding_dictionary_enumeration(self):
        models = prefix_checks = full_checks = 0
        # n=3: all 25 labeled DAGs x all 64 binary code dictionaries.
        # n=2: all 3 labeled DAGs x all 81 ternary dictionaries.
        for n, alphabet in ((2, ('', 'x', '雪')), (3, ('', 'x'))):
            labels = tuple('f' + str(i) for i in range(n))
            schema = dict.fromkeys(labels, ('0', '1'))
            atoms = tuple((f, v) for f in labels for v in schema[f])
            possible = tuple(permutations(labels, 2))
            for mask in range(1 << len(possible)):
                edges = tuple(edge for bit, edge in enumerate(possible) if mask & (1 << bit))
                if not independent_orders(labels, edges):
                    continue
                for words in product(alphabet, repeat=len(atoms)):
                    codes = dict(zip(atoms, words))
                    expected = relation_prefixes(relation(schema, edges, codes))
                    language = Language(schema, edges, codes)
                    models += 1
                    for length in range(n + 2):
                        for observed in product(alphabet, repeat=length):
                            prefix_checks += 1
                            candidates = frozenset(expected.get(observed, set()))
                            self.assertEqual(language.candidates(observed), candidates)
                            if observed:
                                self.assertLessEqual(candidates, language.candidates(observed[:-1]))
                            if length == n:
                                full_checks += 1
                                if len(candidates) == 1:
                                    self.assertEqual(language.decode(json.dumps(observed)), next(iter(candidates)))
                                else:
                                    with self.assertRaises(ValueError):
                                        language.decode(json.dumps(observed))
                    self.assertEqual(language.candidates(('not-in-vocabulary',)), frozenset())
        self.assertEqual((models, prefix_checks, full_checks), (1843, 59320, 14987))
        COVERAGE['joint_DAG_dictionary_models'] = models
        COVERAGE['explicit_prefix_relation_checks'] = prefix_checks
        COVERAGE['complete_frame_decisions'] = full_checks

    def test_heterogeneous_default_codes_and_legal_prefix_formula(self):
        schema = {'["f"]': ('α', 'β'), 'comma,': ('α',), '\\': ('0', '1', '2')}
        codes = {(f, v): json.dumps([f, v], ensure_ascii=False, separators=(',', ':'))
                 for f in schema for v in schema[f]}
        count = 0
        for edges in ((), (('["f"]', '\\'),), (('comma,', '["f"]'), ('["f"]', '\\'))):
            expected = relation_prefixes(relation(schema, edges, codes))
            language = Language(schema, edges)
            self.assertTrue(language.injective)
            for message in product(*schema.values()):
                for order in independent_orders(tuple(schema), edges):
                    expected_tokens = tuple(codes[(f, message[tuple(schema).index(f)])] for f in order)
                    self.assertEqual(language.encode(message, order), expected_tokens)
                    self.assertEqual(language.decode(pack(expected_tokens)), message)
                    for k in range(len(schema) + 1):
                        count += 1
                        actual = language.candidates(expected_tokens[:k])
                        self.assertEqual(actual, frozenset(expected[expected_tokens[:k]]))
                        self.assertEqual(len(actual), math.prod(len(schema[f]) for f in order[k:]))
                        self.assertIn(message, actual)
        self.assertEqual(count, 240)
        COVERAGE['heterogeneous_prefix_formula_checks'] = count

    def test_context_sentinel(self):
        language = Language({'x': ('0',), 'y': ('0',), 'z': ('0',)}, (('z', 'x'), ('x', 'y')))
        self.assertEqual(language.orders, (('z', 'x', 'y'),))

    def test_prefix_sentinel(self):
        language = Language({'left': ('0', '1'), 'right': ('0', '1')},
                            lexicon={('left', '0'): 'a', ('left', '1'): 'b',
                                     ('right', '0'): 'a', ('right', '1'): 'c'})
        self.assertEqual(language.candidates(('c',)), frozenset({('0', '1'), ('1', '1')}))
        self.assertEqual(language.candidates(('a', 'c')), frozenset({('0', '1')}))
        self.assertEqual(language.candidates(('a', 'c', 'a')), frozenset())
        self.assertEqual(language.candidates(('a', 'a')), frozenset({('0', '0')}))

    def test_binding_and_multiplicity_sentinel(self):
        language = Language({'subject': ('P', 'Q'), 'object': ('P', 'Q'), 'verb': ('P',)})
        first, second = ('P', 'Q', 'P'), ('Q', 'P', 'P')
        self.assertNotEqual(language.labeled(first), language.labeled(second))
        self.assertEqual(language.labeled(first), frozenset({('subject', 'P'), ('object', 'Q'), ('verb', 'P')}))
        self.assertEqual(language.aggregate(first), (('P', 2), ('Q', 1)))
        self.assertEqual(language.aggregate(first), language.aggregate(second))

    def test_collision_and_decode_sentinel(self):
        codes = {('x', '0'): 'a', ('x', '1'): 'b', ('y', '0'): 'a', ('y', '1'): 'b'}
        schema = {'x': ('0', '1'), 'y': ('0', '1')}
        ordered = Language(schema, (('x', 'y'),), codes)
        unordered = Language(schema, (), codes)
        self.assertFalse(ordered.injective)
        self.assertEqual(ordered.decode('["a","b"]'), ('0', '1'))
        self.assertEqual(unordered.candidates(('a', 'b')), frozenset({('0', '1'), ('1', '0')}))
        with self.assertRaises(ValueError):
            unordered.decode('["a","b"]')
        with self.assertRaises(ValueError):
            ordered.decode('["bad","b"]')

    def test_frame_sentinel_and_edge_cases(self):
        self.assertNotEqual(pack(('x', 'yz')), pack(('xy', 'z')))
        vocabulary = ('', '"', '\\', '\n', '雪', '[,]', '\x00')
        frames = set()
        for length in range(4):
            for tokens in product(vocabulary, repeat=length):
                frame = pack(iter(tokens))
                self.assertNotIn(frame, frames)
                frames.add(frame)
                self.assertEqual(unpack(frame), tokens)
                self.assertEqual(json.loads(frame), list(tokens))
        self.assertEqual(len(frames), 400)
        self.assertEqual(unpack(' [ "\\u96ea" , "" ] '), ('雪', ''))
        for malformed in ('null', 'true', '0', '{}', '"text"', '[[]]', '[{}]', '[false]', '[NaN]', '[Infinity]', '["a"]tail'):
            with self.assertRaises(ValueError):
                unpack(malformed)
        COVERAGE['distinct_JSON_frame_roundtrips'] = len(frames)

    def test_version_space_exhaustive_intersections(self):
        tables = tuple(product(('A', 'B'), repeat=3))
        observations = tuple(product(range(3), ('A', 'B')))
        example_sets = [()] + [(item,) for item in observations] + list(product(observations, repeat=2))
        checks = 0
        for mask in range(1, 1 << len(tables)):
            selected = {table for bit, table in enumerate(tables) if mask & (1 << bit)}
            for examples in example_sets:
                expected = set(selected)
                for index, meaning in examples:
                    expected.intersection_update(table for table in tables if table[index] == meaning)
                actual = version_space(iter(selected), iter(examples))
                self.assertEqual(actual, frozenset(expected))
                checks += 1
        self.assertEqual(checks, 10965)
        COVERAGE['hypothesis_subset_observation_checks'] = checks

    def test_version_space_sentinel(self):
        tables = (('A', 'B', 'A'), ('A', 'B', 'B'), ('B', 'B', 'A'))
        self.assertEqual(version_space(tables, ((0, 'A'), (1, 'B'))), frozenset(tables[:2]))
        self.assertEqual(version_space(tables, ()), frozenset(tables))
        self.assertEqual(version_space(tables, ((0, 'A'), (0, 'B'))), frozenset())
        self.assertEqual(version_space(tables, ((2, 'outside'),)), frozenset())

    def test_input_boundary_and_immutable_snapshots(self):
        domain = ['0', '1']
        edges = [['x', 'y']]
        codes = {('x', '0'): '', ('x', '1'): '1', ('y', 'only'): 'y'}
        language = Language({'x': iter(domain), 'y': iter(['only'])}, iter(edges), codes)
        domain.append('2')
        edges[0].reverse()
        codes[('x', '0')] = 'altered'
        self.assertEqual(language.encode(iter(['0', 'only']), iter(['x', 'y'])), ('', 'y'))
        self.assertEqual(language.candidates(iter([''])), frozenset({('0', 'only')}))
        self.assertEqual(language.orders, (('x', 'y'),))
        with self.assertRaises(FrozenInstanceError):
            language.orders = ()
        equivalent = Language({'x': ('0', '1'), 'y': ('only',)}, (('x', 'y'), ('x', 'y')),
                              {('x', '0'): '', ('x', '1'): '1', ('y', 'only'): 'y'})
        self.assertEqual(language, equivalent)
        for invalid in ('01', ('0',), ('0', 'only', '0'), ('2', 'only'), ('', 'only')):
            with self.assertRaises(ValueError):
                language.encode(invalid, ('x', 'y'))
        for invalid in ('xy', (), ('x',), ('y', 'x'), ('x', 'x')):
            with self.assertRaises(ValueError):
                language.encode(('0', 'only'), invalid)
        for invalid in ('[]', '[""]', '["","y",""]'):
            with self.assertRaises(ValueError):
                language.decode(invalid)
        for examples in (((-1, 'A'),), ((True, 'A'),), ((1.0, 'A'),), ((3, 'A'),), ((0, None),)):
            with self.assertRaises(ValueError):
                version_space((('A', 'B', 'C'),), examples)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromNames(sys.argv[1:] or ['IndependentTests'], sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print('AUDIT_RECORD=' + json.dumps({'tests': result.testsRun, 'failures': len(result.failures),
          'errors': len(result.errors), 'skipped': len(result.skipped), 'optimize': sys.flags.optimize,
          'coverage': COVERAGE}, sort_keys=True))
    sys.exit(not result.wasSuccessful())
