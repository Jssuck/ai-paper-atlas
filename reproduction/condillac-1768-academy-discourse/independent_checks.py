"""Independent finite audit oracles; run with Python, -O, or -OO.

This file imports only the public model API, never test_model or demo fixtures.
Assertions use unittest methods so optimization cannot disable them. Counts
refer to the explicitly enumerated finite catalogs, not general proofs.
"""
from collections import Counter
import copy
from fractions import Fraction
from itertools import permutations, product
import json
import sys
import unittest

from model import (Judgment, Lookup, RepresentationDomain, SchemaError, Tree,
                   UnknownInput, copy_judgment, diffuse, distinct_origins)

COUNTS = Counter()


def shapes(leaves):
    """All ordered full binary shapes with a fixed number of leaves."""
    if leaves == 1:
        return [None]
    return [(left, right) for split in range(1, leaves)
            for left in shapes(split) for right in shapes(leaves - split)]


def tree_from_shape(shape, predicate_pattern, label_pattern):
    """Also return leaf path constraints, independent of Tree.evaluate."""
    objects = [''.join(bits) for bits in product('01', repeat=3)]
    nodes, leaf_paths = {}, []
    branch_count, leaf_count = 0, 0

    def add(part, requirements):
        nonlocal branch_count, leaf_count
        name = f'n{len(nodes)}'
        nodes[name] = None
        if part is None:
            label = str((leaf_count + label_pattern) % 3) if label_pattern != 3 else 'same'
            leaf_count += 1
            nodes[name] = {'label': label}
            leaf_paths.append((requirements, label))
        else:
            predicate = (branch_count + predicate_pattern) % 3 if predicate_pattern != 3 else 0
            branch_count += 1
            no = add(part[0], requirements + [(predicate, '0')])
            yes = add(part[1], requirements + [(predicate, '1')])
            nodes[name] = {'predicate': str(predicate), 'false': no, 'true': yes}
        return name

    root = add(shape, [])
    return {'domain': objects, 'root': root, 'nodes': nodes,
            'predicates': {str(p): {x: x[p] == '1' for x in objects} for p in range(3)}}, leaf_paths


def population(codes, labels, weights):
    objects = [f'x{i}' for i in range(len(codes))]
    return {'objects': objects, 'codes': dict(zip(objects, codes)),
            'labels': dict(zip(objects, labels)),
            'weights': dict(zip(objects, [str(weight) for weight in weights]))}


def simple_path_oracle(nodes, edges, seeds):
    """Enumerate simple vertex sequences, not a diffusion or BFS recurrence."""
    edge_set = set(map(tuple, edges))
    result = {}
    for length in range(1, len(nodes) + 1):
        for path in permutations(nodes, length):
            if path[0] in seeds and all((a, b) in edge_set for a, b in zip(path, path[1:])):
                result[path[-1]] = min(result.get(path[-1], len(nodes)), length - 1)
    return result


class IndependentTreeChecks(unittest.TestCase):
    def test_368_tree_catalog_by_leaf_path_constraints(self):
        count = 0
        for leaf_count in range(1, 6):
            for shape in shapes(leaf_count):
                for predicate_pattern, label_pattern in product(range(4), repeat=2):
                    spec, paths = tree_from_shape(shape, predicate_pattern, label_pattern)
                    tree, expected = Tree(spec), {}
                    for x in spec['domain']:
                        matches = [(label, len(terms)) for terms, label in paths
                                   if all(x[position] == bit for position, bit in terms)]
                        self.assertEqual(len(matches), 1)
                        expected[x] = matches[0][0]
                        result = tree.evaluate(x)
                        self.assertEqual((result.label, result.predicate_tests), matches[0])
                        COUNTS['tree_input_evaluations'] += 1
                    table = tree.compile()
                    self.assertEqual(dict(table.table), expected)
                    self.assertEqual(len(table.table), len(spec['domain']))
                    for x in spec['domain']:
                        self.assertEqual(table.evaluate(x).label, expected[x])
                        self.assertEqual(table.evaluate(x).abstract_lookups, 1)
                    for selected in ([], spec['domain'][::2], spec['domain'][1::2], spec['domain']):
                        partial = tree.train_lookup(selected)
                        self.assertEqual(dict(partial.table), {x: expected[x] for x in selected})
                        for x in set(spec['domain']) - set(selected):
                            with self.assertRaises(UnknownInput):
                                partial.evaluate(x)
                        COUNTS['partial_training_tables'] += 1
                    count += 1
        self.assertEqual(count, 368)
        COUNTS['tree_specifications'] = count

    def test_article_xor_eight_queries_and_preserved_error(self):
        spec = {'domain': ['00', '01', '10', '11'], 'root': 'root',
                'predicates': {str(p): {x: x[p] == '1' for x in ['00', '01', '10', '11']}
                               for p in (0, 1)},
                'nodes': {'root': {'predicate': '0', 'false': 'a', 'true': 'b'},
                          'a': {'predicate': '1', 'false': '00', 'true': '01'},
                          'b': {'predicate': '1', 'false': '10', 'true': '11'},
                          **{x: {'label': str(int(x[0] != x[1]))} for x in ['00', '01', '10', '11']}}}
        tree = Tree(spec)
        truth = {'00': '0', '01': '1', '10': '1', '11': '0'}
        self.assertEqual(dict(tree.compile().table), truth)
        self.assertEqual(sum(tree.evaluate(x).predicate_tests for x in tree.domain), 8)
        spec['nodes']['11']['label'] = '1'
        wrong = Tree(spec)
        self.assertEqual(sum(wrong.compile().evaluate(x).label != truth[x] for x in truth), 1)
        self.assertEqual(dict(wrong.train_lookup(['00', '01', '10']).table),
                         dict(tree.train_lookup(['00', '01', '10']).table))
        self.assertNotEqual(tree.evaluate('11').label, wrong.evaluate('11').label)

    def test_empty_domain_leaf_and_branch_boundary(self):
        for nodes, predicates in (({'r': {'label': '0'}}, {}),
                                  ({'r': {'predicate': 'p', 'false': 'a', 'true': 'b'},
                                    'a': {'label': '0'}, 'b': {'label': '1'}}, {'p': {}})):
            tree = Tree({'domain': [], 'root': 'r', 'nodes': nodes, 'predicates': predicates})
            self.assertEqual(dict(tree.compile().table), {})
            self.assertEqual(dict(tree.train_lookup([]).table), {})
            with self.assertRaises(UnknownInput):
                tree.evaluate('absent')
        leaf = Tree({'domain': ['x'], 'root': 'r', 'nodes': {'r': {'label': '0'}}, 'predicates': {}})
        self.assertEqual(leaf.evaluate('x').predicate_tests, 0)
        self.assertEqual(leaf.compile().evaluate('x').abstract_lookups, 1)

    def test_schema_tree_malformed_and_cycle_cases(self):
        good = {'domain': ['x'], 'root': 'r', 'nodes': {'r': {'label': '0'}}, 'predicates': {}}
        bad = [None, [], {}, {**good, 'extra': 1}]
        for key, values in {'domain': [None, (), ['x', 'x'], [False], ['']],
                            'root': [None, '', [], 'missing'], 'nodes': [None, [], {}, {'r': 1}],
                            'predicates': [None, [], {'p': {'x': 1}}, {'p': {}}, {'p': {'x': True, 'y': False}}]}.items():
            bad.extend({**copy.deepcopy(good), key: value} for value in values)
        bad.extend([
            {**good, 'nodes': {'r': {'label': 0}}},
            {**good, 'nodes': {'r': {'label': '0', 'extra': 1}}},
            {**good, 'nodes': {'r': {'label': '0'}, 'orphan': {'label': '1'}}},
            {'domain': ['x'], 'root': 'r', 'predicates': {'p': {'x': True}},
             'nodes': {'r': {'predicate': 'p', 'false': 'r', 'true': 'leaf'}, 'leaf': {'label': '0'}}},
            {'domain': ['x'], 'root': 'r', 'predicates': {'p': {'x': True}},
             'nodes': {'r': {'label': '0'},
                       'u': {'predicate': 'p', 'false': 'v', 'true': 'l1'},
                       'v': {'predicate': 'p', 'false': 'u', 'true': 'l2'},
                       'l1': {'label': '1'}, 'l2': {'label': '0'}}},
            {'domain': ['x'], 'root': 'r', 'predicates': {'p': {'x': True}},
             'nodes': {'r': {'predicate': 'p', 'false': 'a', 'true': 'a'}, 'a': {'label': '0'}}},
            {'domain': ['x'], 'root': 'r', 'predicates': {},
             'nodes': {'r': {'predicate': 'missing', 'false': 'a', 'true': 'b'},
                       'a': {'label': '0'}, 'b': {'label': '1'}}},
        ])
        for index, spec in enumerate(bad):
            with self.subTest(case=index), self.assertRaises(SchemaError):
                Tree(spec)
        COUNTS['invalid_tree_specs'] = len(bad)
        for invalid in ([], None, 0, False, {}, 'missing'):
            for obj in (Tree(good), Lookup({'x': '0'})):
                with self.assertRaises(UnknownInput):
                    obj.evaluate(invalid)
        for selected in ((), ['x', 'x'], [False], ['']):
            with self.assertRaises(SchemaError):
                Tree(good).train_lookup(selected)
        with self.assertRaises(UnknownInput):
            Tree(good).train_lookup(['missing'])
        for table in (None, [], {1: 'x'}, {'': 'x'}, {'x': []}, {'x': ''}):
            with self.assertRaises(SchemaError):
                Lookup(table)


class IndependentRepresentationChecks(unittest.TestCase):
    def test_3510_populations_by_complete_decoder_enumeration(self):
        partitions = [('A', 'A', 'A'), ('A', 'A', 'B'), ('A', 'B', 'A'),
                      ('A', 'B', 'B'), ('A', 'B', 'C')]
        count = decoder_count = 0
        for codes, labels, weights in product(partitions, product('012', repeat=3),
                product((Fraction(0), Fraction(1, 3), Fraction(2, 3)), repeat=3)):
            if not sum(weights):
                continue
            domain = RepresentationDomain(population(codes, labels, weights))
            used_codes = sorted(set(codes))
            candidate_losses = []
            for values in product(('0', '1', '2', 'unseen'), repeat=len(used_codes)):
                decoder = dict(zip(used_codes, values))
                loss = sum((weight for code, label, weight in zip(codes, labels, weights)
                            if decoder[code] != label), Fraction(0)) / sum(weights)
                self.assertEqual(domain.risk(decoder), loss)
                candidate_losses.append(loss)
                decoder_count += 1
            minimum = min(candidate_losses)
            best = domain.best_decoder()
            self.assertEqual(best.risk, minimum)
            self.assertEqual(best.error_mass, minimum * sum(weights))
            self.assertEqual(domain.risk(best.decoder), minimum)
            structural = all(labels[i] == labels[j] for i in range(3) for j in range(3)
                             if codes[i] == codes[j])
            self.assertEqual(domain.sufficient(), structural)
            self.assertEqual(domain.sufficient(True), minimum == 0)
            count += 1
        self.assertEqual((count, decoder_count), (3510, 81432))
        COUNTS['representation_populations'] = count
        COUNTS['decoder_candidates'] = decoder_count

    def test_article_tie_refinement_and_binary_transfer(self):
        labels, weights = ('0', '0', '1'), (2, 1, 3)
        coarse = RepresentationDomain(population(('A', 'A', 'A'), labels, weights))
        fine = RepresentationDomain(population(('A', 'A', 'B'), labels, weights))
        self.assertEqual(coarse.risk({'A': '0'}), Fraction(1, 2))
        self.assertEqual(coarse.risk({'A': '1'}), Fraction(1, 2))
        self.assertEqual(coarse.best_decoder().risk, Fraction(1, 2))
        self.assertEqual(dict(coarse.best_decoder().decoder), {'A': '0'})
        self.assertEqual(fine.best_decoder().risk, 0)
        codes = ('0', '0', '1', '1')
        source = RepresentationDomain(population(codes, codes, (1, 1, 1, 1)))
        target = RepresentationDomain(population(codes, ('0', '1', '0', '1'), (1, 1, 1, 1)))
        decoder = {'0': '0', '1': '1'}
        self.assertEqual(source.risk(decoder), 0)
        self.assertEqual(target.risk(decoder), Fraction(1, 2))
        self.assertEqual(target.best_decoder().risk, Fraction(1, 2))
        self.assertFalse(target.sufficient())

    def test_label_reversal_distinct_from_information_loss(self):
        codes = ('A', 'B')
        original = RepresentationDomain(population(codes, ('0', '1'), (1, 1)))
        shifted = RepresentationDomain(population(codes, ('1', '0'), (1, 1)))
        self.assertTrue(original.sufficient())
        self.assertTrue(shifted.sufficient())
        self.assertEqual(shifted.risk(original.best_decoder().decoder), 1)
        self.assertEqual(shifted.best_decoder().risk, 0)

    def test_zero_support_fiber_tie_and_scale_invariance(self):
        spec = population(('A', 'A', 'Z', 'Z'), ('1', '0', 'beta', 'alpha'), (1, 0, 0, 0))
        domain = RepresentationDomain(spec)
        self.assertFalse(domain.sufficient())
        self.assertTrue(domain.sufficient(True))
        self.assertEqual(domain.best_decoder().risk, 0)
        self.assertEqual(dict(domain.best_decoder().decoder), {'A': '1', 'Z': 'alpha'})
        self.assertEqual(domain.risk({'A': '1', 'Z': 'outside-label-alphabet'}), 0)
        spec['objects'].reverse()
        self.assertEqual(dict(RepresentationDomain(spec).best_decoder().decoder), dict(domain.best_decoder().decoder))
        for scale in (Fraction(1, 17), Fraction(19, 3), 10 ** 50):
            scaled = RepresentationDomain(population(('A', 'A', 'B'), ('0', '1', '2'),
                                                       tuple(scale * x for x in (2, 3, 5))))
            self.assertEqual(scaled.best_decoder().risk, Fraction(1, 5))
            self.assertEqual(scaled.total_mass, 10 * scale)

    def test_refinement_catalog_never_increases_optimum(self):
        partitions = [('A', 'A', 'A'), ('A', 'A', 'B'), ('A', 'B', 'A'),
                      ('A', 'B', 'B'), ('A', 'B', 'C')]
        count = 0
        for old, new in product(partitions, repeat=2):
            if not all(old[i] == old[j] for i in range(3) for j in range(3) if new[i] == new[j]):
                continue
            for labels, weights in product(product('012', repeat=3),
                                           ((1, 1, 1), (0, 1, 0), (Fraction(1, 3), Fraction(2, 3), 2))):
                old_domain = RepresentationDomain(population(old, labels, weights))
                new_domain = RepresentationDomain(population(new, labels, weights))
                self.assertLessEqual(new_domain.best_decoder().risk, old_domain.best_decoder().risk)
                count += 1
        self.assertEqual(count, 972)
        COUNTS['refinement_comparisons'] = count

    def test_schema_representation_malformed(self):
        good = population(('A', 'B'), ('0', '1'), (1, 1))
        bad = [None, [], {}, {**good, 'extra': 0}, {'objects': [], 'codes': {}, 'labels': {}}]
        for key, values in {'objects': [(), None, ['x0', 'x0'], [0], ['']],
                            'codes': [None, [], {}, {'x0': 'A', 'x1': ''}, {'x0': 'A', 'x1': []}],
                            'labels': [None, [], {}, {'x0': 0, 'x1': '1'}],
                            'weights': [None, [], {}, {'x0': 0, 'x1': 0}]}.items():
            bad.extend({**copy.deepcopy(good), key: value} for value in values)
        for weight in (True, False, -1, '-2/3', 0.5, float('nan'), float('inf'), Fraction(1, 2),
                       '1/0', '1/02', '1/-2', '1.0', '1 / 2', ' 1', '', 'NaN', [], {}):
            case = copy.deepcopy(good)
            case['weights']['x0'] = weight
            bad.append(case)
        for index, spec in enumerate(bad):
            with self.subTest(case=index), self.assertRaises(SchemaError):
                RepresentationDomain(spec)
        COUNTS['invalid_representation_specs'] = len(bad)
        domain = RepresentationDomain(good)
        for decoder in (None, [], {}, {'A': '0'}, {'A': '0', 'B': '1', 'C': '0'},
                        {'A': '', 'B': '1'}, {'A': 0, 'B': '1'}):
            with self.assertRaises(SchemaError):
                domain.risk(decoder)
        for value in (0, 1, None, '', [], {}):
            with self.assertRaises(SchemaError):
                domain.sufficient(value)


class IndependentDiffusionChecks(unittest.TestCase):
    def test_16384_graph_seed_cases_by_simple_paths(self):
        nodes = ['A', 'B', 'C', 'D']
        possible = [(a, b) for a in nodes for b in nodes if a != b]
        seed_sets = [[], ['A'], ['B', 'D'], nodes]
        count = 0
        for bits in product((False, True), repeat=12):
            edges = [list(edge) for edge, active in zip(possible, bits) if active]
            graph = {'nodes': nodes, 'edges': edges}
            for seeds in seed_sets:
                distances = simple_path_oracle(nodes, edges, seeds)
                expected = tuple(frozenset(node for node in distances if distances[node] <= t)
                                 for t in range(max(distances.values(), default=0) + 1))
                result = diffuse(graph, seeds, Judgment('fixed claim', 'one source'))
                self.assertEqual(dict(result.first_arrival), distances)
                self.assertEqual(result.snapshots, expected)
                self.assertEqual(result.holders, frozenset(distances))
                self.assertEqual(result.origins, frozenset({'one source'}) if distances else frozenset())
                self.assertLessEqual(len(result.snapshots), len(nodes))
                # Added loops cannot improve a shortest arrival or add a holder.
                loops = {'nodes': nodes, 'edges': edges + [[node, node] for node in nodes]}
                self.assertEqual(diffuse(loops, seeds, Judgment('different content', 'another source')).snapshots,
                                 result.snapshots)
                count += 1
        self.assertEqual(count, 16384)
        COUNTS['graph_seed_cases'] = count
        COUNTS['self_loop_and_content_invariance_cases'] = count

    def test_added_edge_monotonicity_all_four_vertex_graphs(self):
        nodes = ['A', 'B', 'C', 'D']
        possible = [(a, b) for a in nodes for b in nodes if a != b]
        count = 0
        for bits in product((False, True), repeat=12):
            edges = [list(edge) for edge, active in zip(possible, bits) if active]
            extra = next((list(edge) for edge, active in zip(possible, bits) if not active), None)
            if extra is None:
                continue
            old = diffuse({'nodes': nodes, 'edges': edges}, ['A'], Judgment('q', 's'))
            new = diffuse({'nodes': nodes, 'edges': edges + [extra]}, ['A'], Judgment('q', 's'))
            for node, time in old.first_arrival.items():
                self.assertLessEqual(new.first_arrival[node], time)
            for time in range(max(len(old.snapshots), len(new.snapshots))):
                self.assertLessEqual(old.snapshots[min(time, len(old.snapshots) - 1)],
                                     new.snapshots[min(time, len(new.snapshots) - 1)])
            count += 1
        self.assertEqual(count, 4095)
        COUNTS['single_edge_augmentation_cases'] = count

    def test_article_chain_shortcut_and_reachable_cycles(self):
        graph = {'nodes': ['a', 'b', 'c', 'd', 'outside'],
                 'edges': [['a', 'b'], ['b', 'c'], ['c', 'd']]}
        judgment = Judgment('claim', 'source')
        chain = diffuse(graph, ['a'], judgment)
        self.assertEqual(dict(chain.first_arrival), {'a': 0, 'b': 1, 'c': 2, 'd': 3})
        graph['edges'].append(['a', 'd'])
        shortcut = diffuse(graph, ['a'], judgment)
        self.assertEqual(dict(shortcut.first_arrival), {'a': 0, 'b': 1, 'c': 2, 'd': 1})
        graph['edges'].extend([['d', 'a'], ['outside', 'outside']])
        cycle = diffuse(graph, ['a'], judgment)
        self.assertEqual(cycle.snapshots, shortcut.snapshots)
        self.assertNotIn('outside', cycle.holders)
        empty = diffuse({'nodes': [], 'edges': []}, [], judgment)
        self.assertEqual((empty.snapshots, dict(empty.first_arrival), empty.origins),
                         ((frozenset(),), {}, frozenset()))
        with self.assertRaises(SchemaError):
            diffuse(graph, ['a', 'a'], judgment)

    def test_origin_identifiers_are_deduplicated_without_independence_claim(self):
        judgment = Judgment('a claim', 'original')
        for count in (0, 1, 4, 101):
            copied = copy_judgment(judgment, count)
            self.assertEqual(len(copied), count)
            self.assertEqual(distinct_origins(copied), frozenset({'original'}) if count else frozenset())
        same_source_other_claim = Judgment('a different claim', 'original')
        same_claim_other_source = Judgment('a claim', 'second')
        self.assertEqual(distinct_origins([judgment, judgment, same_source_other_claim]), frozenset({'original'}))
        self.assertEqual(distinct_origins([judgment, same_claim_other_source]), frozenset({'original', 'second'}))
        # The API reports identifiers only; distinct identifiers do not certify statistical independence.

    def test_schema_diffusion_and_provenance_malformed(self):
        good, j = {'nodes': ['a', 'b'], 'edges': [['a', 'b']]}, Judgment('claim', 'source')
        bad = [None, [], {}, {**good, 'extra': 1}, {'nodes': [], 'edges': [['a', 'b']]}]
        for nodes in (None, (), [0], [''], ['a', 'a']):
            bad.append({'nodes': nodes, 'edges': []})
        for edges in (None, (), [None], [('a', 'b')], [['a']], [['a', 'b', 'a']],
                      [['a', 1]], [['a', []]], [['a', 'missing']], [['a', 'b'], ['a', 'b']]):
            bad.append({'nodes': ['a', 'b'], 'edges': edges})
        for index, spec in enumerate(bad):
            with self.subTest(case=index), self.assertRaises(SchemaError):
                diffuse(spec, [], j)
        COUNTS['invalid_graph_specs'] = len(bad)
        for seeds in (None, (), 'a', [False], [''], ['missing'], ['a', 'a']):
            with self.assertRaises(SchemaError):
                diffuse(good, seeds, j)
        with self.assertRaises(SchemaError):
            diffuse(good, [], 'claim')
        for args in (('', 's'), ('c', ''), (None, 's'), ('c', 0)):
            with self.assertRaises(SchemaError):
                Judgment(*args)
        for count in (-1, True, 1.0, '1', None):
            with self.assertRaises(SchemaError):
                copy_judgment(j, count)
        for judgments in (None, {}, 'q', (j, 'q')):
            with self.assertRaises(SchemaError):
                distinct_origins(judgments)


class IndependentSnapshotChecks(unittest.TestCase):
    def test_snapshots_do_not_alias_input_containers(self):
        spec, _ = tree_from_shape((None, None), 0, 0)
        tree = Tree(spec)
        expected = dict(tree.compile().table)
        spec['domain'].clear()
        spec['nodes'].clear()
        spec['predicates']['0'].clear()
        self.assertEqual(dict(tree.compile().table), expected)
        raw = {'x': '0'}
        table = Lookup(raw)
        raw['x'] = '1'
        self.assertEqual(table.evaluate('x').label, '0')
        spec = population(('A', 'A'), ('0', '1'), (2, 1))
        domain = RepresentationDomain(spec)
        best = domain.best_decoder()
        spec['codes'].clear()
        spec['labels'].clear()
        spec['weights'].clear()
        spec['objects'].clear()
        self.assertEqual(domain.best_decoder().risk, Fraction(1, 3))
        for mapping in (table.table, best.decoder):
            with self.assertRaises(TypeError):
                mapping['new'] = 'value'
        for obj in (tree, table, domain):
            with self.assertRaises(AttributeError):
                obj._sealed = False
            with self.assertRaises(AttributeError):
                del obj._sealed
        graph, seeds = {'nodes': ['a', 'b'], 'edges': [['a', 'b']]}, ['a']
        result = diffuse(graph, seeds, Judgment('c', 's'))
        graph['edges'].clear()
        graph['nodes'].clear()
        seeds.clear()
        self.assertEqual(result.snapshots, (frozenset({'a'}), frozenset({'a', 'b'})))
        with self.assertRaises(TypeError):
            result.first_arrival['b'] = 99


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print('FINITE_AUDIT_COUNTS=' + json.dumps(dict(sorted(COUNTS.items())), sort_keys=True))
    sys.exit(not result.wasSuccessful())
