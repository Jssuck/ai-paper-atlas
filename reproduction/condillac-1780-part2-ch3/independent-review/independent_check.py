"""Independent specification checks. Imports model only, never author tests.

Runs with standard library under normal, -O and -OO. Every executable check
uses explicit failure, not Python's optimization-sensitive assert statement.
Finite enumeration bounds appear in the output; these are not general proofs.
"""
from collections import Counter
from dataclasses import replace
import hashlib
import itertools as it
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import model as m

COUNTS = Counter()
CHECKS = Counter()


def check(condition, group, detail=''):
    CHECKS[group] += 1
    if not condition:
        raise RuntimeError(f'{group}: {detail}')


def rejects(call, group='validation'):
    try:
        call()
    except ValueError:
        CHECKS[group] += 1
        return
    except Exception as exc:
        raise RuntimeError(f'{group}: wrong exception {type(exc).__name__}') from exc
    raise RuntimeError(f'{group}: malformed input accepted')


def bits_to_atoms(bits, atoms):
    return frozenset(atom for index, atom in enumerate(atoms) if bits & (1 << index))


def model_masks(n, rules):
    """Interpretation oracle: all satisfying Boolean assignments, no chaining."""
    return tuple(mask for mask in range(1 << n)
                 if all(mask & body != body or mask & (1 << head) for body, head in rules))


def consequence_mask(n, models, seed):
    result = (1 << n) - 1
    for interpretation in models:
        if interpretation & seed == seed:
            result &= interpretation
    return result


def hypotheses():
    # Every nonempty class of ternary functions on two positions; observation
    # alphabet adds '?' which no candidate predicts. Integer disagreement masks
    # provide a separate implementation of the observation specification.
    points = ('left', 'right')
    rows = tuple(it.product('012', repeat=2))
    observations = tuple(it.product(range(2), '012?'))
    data_sets = tuple(data for k in range(3) for data in it.product(observations, repeat=k))
    for selected in range(1, 1 << len(rows)):
        ids = tuple(i for i in range(len(rows)) if selected & (1 << i))
        space = m.HypothesisSpace(points, tuple((str(i), rows[i]) for i in ids))
        for data in data_sets:
            actual_data = tuple((points[pos], value) for pos, value in data)
            distances = {i: len(bin(sum((1 << j) for j, (pos, value) in enumerate(data)
                                       if rows[i][pos] != value)).replace('0b', '').replace('0', ''))
                         for i in ids}
            previous = frozenset()
            for budget in range(3):
                got = space.candidates(actual_data, budget)
                expected = frozenset(str(i) for i in ids if distances[i] <= budget)
                check(got == expected, 'hypothesis_oracle')
                check(previous <= got, 'budget_monotonicity')
                if data:
                    check(got <= space.candidates(actual_data[:-1], budget), 'observation_monotonicity')
                previous = got
                COUNTS['ternary_class_data_budget_cases'] += 1
        for observed_mask in range(4):
            positions = tuple(i for i in range(2) if observed_mask & (1 << i))
            singles = []
            for truth in ids:
                compatible = {i for i in ids if all(rows[i][p] == rows[truth][p] for p in positions)}
                truth_data = tuple((points[p], rows[truth][p]) for p in positions)
                check(space.candidates(truth_data) == {str(i) for i in compatible}, 'identification_oracle')
                singles.append(len(compatible) == 1)
            check(space.distinguishes(tuple(points[p] for p in positions)) == all(singles), 'identification_iff')
            COUNTS['class_observed_subset_cases'] += 1
    alias = m.HypothesisSpace(('x',), (('alias1', ('0',)), ('alias2', ('0',))))
    check(not alias.distinguishes(('x',)), 'identification_aliases')
    check(alias.candidates((('x', '0'),)) == {'alias1', 'alias2'}, 'identification_aliases')
    # All binary length-three codes, including codes whose minimum distance is
    # greater than twice the budget. Records include a third, unseen value.
    codewords = tuple(it.product('01', repeat=3))
    points = ('p', 'q', 'r')
    for selected in range(1, 256):
        ids = tuple(i for i in range(8) if selected & (1 << i))
        space = m.HypothesisSpace(points, tuple((str(i), codewords[i]) for i in ids))
        minimum = min((sum(a != b for a, b in zip(codewords[i], codewords[j]))
                       for i, j in it.combinations(ids, 2)), default=4)
        for values in it.product('01?', repeat=3):
            data = tuple(zip(points, values))
            for budget in range(4):
                candidates = space.candidates(data, budget)
                for truth in ids:
                    errors = sum(a != b for a, b in zip(codewords[truth], values))
                    if errors <= budget:
                        check(str(truth) in candidates, 'bounded_noise_retention')
                if len(ids) <= 1 or minimum > 2 * budget:
                    check(len(candidates) <= 1, 'hamming_separation')
                COUNTS['binary_code_record_budget_cases'] += 1
    repeat = m.HypothesisSpace(('x',), (('zero', ('0',)), ('one', ('1',))))
    check(repeat.candidates((('x', '1'), ('x', '1'), ('x', '0')), 1) == {'one'}, 'repetition_count')


def horn():
    for n, max_rules in ((0, None), (2, None), (3, 3)):
        atoms = tuple(f'a{i}' for i in range(n))
        available = tuple(it.product(range(1 << n), range(n)))
        if max_rules is None:
            systems = (tuple(available[i] for i in range(len(available)) if mask & (1 << i))
                       for mask in range(1 << len(available)))
        else:
            systems = (rules for count in range(max_rules + 1) for rules in it.combinations(available, count))
        for rules in systems:
            system = m.HornSystem(atoms, tuple(m.Rule(f'r{i}', bits_to_atoms(body, atoms), atoms[head])
                                               for i, (body, head) in enumerate(rules)))
            valid_models = model_masks(n, rules)
            closures = {}
            for seeds in range(1 << n):
                seed_atoms = bits_to_atoms(seeds, atoms)
                got = system.close(seed_atoms)
                expected_bits = consequence_mask(n, valid_models, seeds)
                expected = bits_to_atoms(expected_bits, atoms)
                check(got.atoms == expected, 'horn_truth_table_oracle')
                check(system.closed(seed_atoms) == (seeds in valid_models), 'closed_oracle')
                check(seed_atoms <= got.atoms, 'horn_extensivity')
                check(system.close(got.atoms).atoms == got.atoms, 'horn_idempotence')
                check(len(got.steps) <= n - len(seed_atoms), 'horn_termination_bound')
                check(system.verify_trace(got, seed_atoms), 'generated_trace')
                reverse = m.HornSystem(atoms, system.rules[::-1]).close(seed_atoms)
                check(reverse.atoms == expected, 'rule_order_invariance')
                for truth in valid_models:
                    if truth & seeds == seeds:
                        check(expected_bits & truth == expected_bits, 'conditional_truth_preservation')
                closures[seeds] = expected_bits
                COUNTS[f'horn_n{n}_system_seed_cases'] += 1
            for smaller, larger in it.product(closures, repeat=2):
                if smaller & larger == smaller:
                    check(closures[smaller] & closures[larger] == closures[smaller], 'horn_monotonicity')
    # For three representative systems, enumerate ALL bounded step sequences,
    # seeds and reported endpoints. The oracle separately evaluates named rule
    # histories and truth-table least consequence, including incomplete traces.
    atoms = ('a', 'b', 'c')
    systems = (((1, 1), (2, 2), (0, 0)), ((1, 1), (2, 0), (3, 2)), ((3, 2), (1, 2), (4, 1)))
    for rules in systems:
        system = m.HornSystem(atoms, tuple(m.Rule(str(i), bits_to_atoms(b, atoms), atoms[h])
                                           for i, (b, h) in enumerate(rules)))
        valid_models = model_masks(3, rules)
        histories = tuple(seq for k in range(4) for seq in it.product(range(3), repeat=k))
        for seed, report, history in it.product(range(8), range(8), histories):
            seen, legal = seed, True
            for index in history:
                body, head = rules[index]
                if seen & body != body or seen & (1 << head):
                    legal = False
                seen |= 1 << head
            expected = legal and seen == report and report == consequence_mask(3, valid_models, seed)
            result = m.ClosureResult(bits_to_atoms(seed, atoms),
                tuple(m.Derivation(str(i), tuple(sorted(bits_to_atoms(rules[i][0], atoms))), atoms[rules[i][1]])
                      for i in history), bits_to_atoms(report, atoms))
            try:
                accepted = system.verify_trace(result, bits_to_atoms(seed, atoms))
            except ValueError:
                accepted = False
            check(accepted == expected, 'exhaustive_trace_oracle')
            COUNTS['trace_history_seed_endpoint_cases'] += 1
    system = m.HornSystem(('a', 'b'), (m.Rule('r', ('a',), 'b'),))
    good = system.close(('a',))
    for wrong in (replace(good, seeds=frozenset()), replace(good, atoms=frozenset({'foreign'})),
                  replace(good, steps=(m.Derivation('absent', ('a',), 'b'),)),
                  replace(good, steps=(m.Derivation('r', ('b',), 'b'),)),
                  replace(good, steps=(m.Derivation('r', ('a',), 'a'),)),
                  replace(good, steps=(m.Derivation('r', ['a'], 'b'),)),
                  replace(good, steps=('r',)), replace(good, steps=None)):
        rejects(lambda wrong=wrong: system.verify_trace(wrong, ('a',)), 'forged_trace_fields')
    # Recompute after retracting one seed; an independent support retains c.
    system = m.HornSystem(('a', 'b', 'c', 'd'), (m.Rule('ab', {'a'}, 'b'), m.Rule('bc', {'b'}, 'c'), m.Rule('dc', {'d'}, 'c')))
    check(system.close({'a', 'd'}).atoms == {'a', 'b', 'c', 'd'}, 'retraction_by_recomputation')
    check(system.close({'d'}).atoms == {'c', 'd'}, 'retraction_by_recomputation')


def vocabularies():
    for n in range(4):
        meanings = tuple(f'm{i}' for i in range(n))
        left = tuple(f'L{i}' for i in range(n))
        right = tuple(f'R{i}' for i in range(n))
        for left_words, right_words in it.product(it.permutations(left), it.permutations(right)):
            a = m.Vocabulary(tuple(zip(meanings, left_words)))
            b = m.Vocabulary(tuple(zip(meanings, right_words)))
            expected_dictionary = {left_words[i]: right_words[i] for i in range(n)}
            check(m.aligned_dictionary(a, b) == expected_dictionary, 'aligned_dictionary_oracle')
            for outputs in it.product(right, repeat=n):
                dictionary = dict(zip(left, outputs))
                correct = all(dictionary[left_words[i]] == right_words[i] for i in range(n))
                check(m.translation_preserves(a, b, dictionary) == correct, 'semantic_preservation_oracle')
                injective = len(set(outputs)) == n
                if injective:
                    inverse = m.inverse_dictionary(dictionary)
                else:
                    rejects(lambda: m.inverse_dictionary(dictionary), 'noninjective_inverse')
                for mask in range(1 << n):
                    subset = bits_to_atoms(mask, meanings)
                    check(a.decode(a.encode(subset)) == subset, 'vocabulary_round_trip')
                    if correct:
                        check(b.decode(m.translate_atoms(a.encode(subset), dictionary)) == subset, 'meaning_round_trip')
                    if injective:
                        words = bits_to_atoms(mask, left)
                        check(m.translate_atoms(m.translate_atoms(words, dictionary), inverse) == words, 'syntax_round_trip')
                COUNTS['vocabulary_pair_all_function_cases'] += 1
    # Every 2-atom Horn system and every total function into 2 target atoms.
    # Arbitrary merging preserves forward consequences, but can create extras.
    atoms, target_atoms = ('a', 'b'), ('x', 'y')
    available = tuple(it.product(range(4), range(2)))
    for selected in range(256):
        rules = tuple(available[i] for i in range(8) if selected & (1 << i))
        source = m.HornSystem(atoms, tuple(m.Rule(str(i), bits_to_atoms(body, atoms), atoms[head])
                                          for i, (body, head) in enumerate(rules)))
        for outputs in it.product(target_atoms, repeat=2):
            mapping = dict(zip(atoms, outputs))
            target = m.HornSystem(target_atoms, tuple(m.rename_rule(rule, mapping) for rule in source.rules))
            for mask in range(4):
                seeds = bits_to_atoms(mask, atoms)
                expected = {mapping[x] for x in source.close(seeds).atoms}
                actual = target.close({mapping[x] for x in seeds}).atoms
                check(expected <= actual, 'noninjective_forward_preservation')
                if len(set(outputs)) == 2:
                    check(expected == actual, 'bijective_closure_transport')
                elif expected != actual:
                    COUNTS['noninjective_extra_consequence_witnesses'] += 1
                COUNTS['transport_system_mapping_seed_cases'] += 1
    # Explicit proper collapse: identifying only some atoms can create a new
    # consequence. Two-atom total collapses above cannot show this distinction.
    source = m.HornSystem(('p', 'q', 'r'), (m.Rule('conjunction', {'p', 'q'}, 'r'),))
    mapping = {'p': 'x', 'q': 'x', 'r': 'y'}
    target = m.HornSystem(('x', 'y'), tuple(m.rename_rule(rule, mapping) for rule in source.rules))
    check(m.translate_atoms(source.close({'p'}).atoms, mapping) == {'x'}, 'noninjective_extra_trigger')
    check(target.close({'x'}).atoms == {'x', 'y'}, 'noninjective_extra_trigger')
    a = m.Vocabulary((('permit', 'A'), ('forbid', 'B')))
    b = m.Vocabulary((('permit', 'X'), ('forbid', 'Y')))
    swapped = {'A': 'Y', 'B': 'X'}
    check(not m.translation_preserves(a, b, swapped), 'reversible_wrong_semantics')
    check(m.translate_atoms(m.translate_atoms({'A'}, swapped), m.inverse_dictionary(swapped)) == {'A'}, 'reversible_wrong_semantics')
    check(b.decode(m.translate_atoms({'A'}, swapped)) == {'forbid'}, 'reversible_wrong_semantics')
    # Wrong bijections preserve transported syntax even while disagreeing with
    # an independently meaning-aligned target rule system.
    source = m.HornSystem(('A', 'B'), (m.Rule('fact', (), 'A'),))
    genuine = m.HornSystem(('X', 'Y'), (m.Rule('fact', (), 'X'),))
    wrong = m.HornSystem(('X', 'Y'), tuple(m.rename_rule(rule, swapped) for rule in source.rules))
    transported = m.translate_atoms(source.close(()).atoms, swapped)
    check(transported == wrong.close(()).atoms, 'wrong_semantics_same_structure')
    check(transported != genuine.close(()).atoms, 'wrong_semantics_same_structure')


def task_partitions():
    # Enumerate partitions canonically rather than repeating differently named
    # versions of the same partition. All 15 partitions of four worlds, paired
    # with every binary-valued task; all refinement triples checked.
    worlds = ('w0', 'w1', 'w2', 'w3')
    partitions = tuple(labels for labels in it.product(range(4), repeat=4)
                       if labels[0] == 0 and all(labels[i] <= 1 + max(labels[:i]) for i in range(1, 4)))
    check(len(partitions) == 15, 'partition_enumeration')
    for labels in partitions:
        for answers in it.product('01', repeat=4):
            fibers = [{answers[i] for i in range(4) if labels[i] == block} for block in set(labels)]
            expected = all(len(fiber) == 1 for fiber in fibers)
            label_map = dict(zip(worlds, map(str, labels)))
            task_map = dict(zip(worlds, answers))
            check(m.task_exact(worlds, label_map, task_map) == expected, 'task_factorization_oracle')
            for finer in partitions:
                refinement = all(len({labels[i] for i in range(4) if finer[i] == block}) == 1
                                 for block in set(finer))
                if expected and refinement:
                    check(m.task_exact(worlds, dict(zip(worlds, map(str, finer))), task_map), 'task_refinement')
            COUNTS['canonical_partition_binary_task_cases'] += 1
    task = dict(zip(worlds, ('0', '0', '1', '1')))
    check(m.task_exact(worlds, dict(zip(worlds, ('a', 'a', 'b', 'b'))), task), 'more_labels_counterexample')
    check(not m.task_exact(worlds, dict(zip(worlds, ('x', 'y', 'x', 'z'))), task), 'more_labels_counterexample')


def validation():
    hs = m.HypothesisSpace(('x',), (('h', ('0',)),))
    invalid = [lambda: m.HypothesisSpace((), ()), lambda: m.HypothesisSpace(('x', 'x'), (('h', ('0', '0')),)),
               lambda: m.HypothesisSpace(('x',), ()), lambda: m.HypothesisSpace(('x',), (('h', ()),)),
               lambda: m.HypothesisSpace(('x',), (('h', ('0',)), ('h', ('1',)))),
               lambda: m.HypothesisSpace(('x',), (('h', (True,)),)),
               lambda: hs.candidates([('x',)]), lambda: hs.candidates([('x', '0', 'extra')]),
               lambda: hs.candidates([('x', 'bad'), ('foreign', '0')]), lambda: hs.distinguishes(('foreign',)),
               lambda: hs.distinguishes(('x', 'x')), lambda: m.Rule('', (), 'a'), lambda: m.Rule('r', 'a', 'a'),
               lambda: m.Rule('r', (1,), 'a'), lambda: m.HornSystem(('a',), (m.Rule('r', ('b',), 'a'),)),
               lambda: m.HornSystem(('a',), (m.Rule('r', (), 'b'),)), lambda: m.HornSystem(('a', 'a'), ()),
               lambda: m.HornSystem(('a',), ('r',)), lambda: m.HornSystem(('a',), ()).close(('b',)),
               lambda: m.HornSystem(('a',), ()).verify_trace(None, ()),
               lambda: m.Vocabulary((('a', 'A'), ('a', 'B'))), lambda: m.Vocabulary((('a', 'A'), ('b', 'A'))),
               lambda: m.Vocabulary((('a', ''),)), lambda: m.translate_atoms(('a',), {}),
               lambda: m.translate_atoms('a', {'a': 'A'}), lambda: m.inverse_dictionary({'a': True}),
               lambda: m.rename_rule(None, {}), lambda: m.aligned_dictionary(m.Vocabulary((('a', 'A'),)), m.Vocabulary(())),
               lambda: m.task_exact((), {}, {}), lambda: m.task_exact(('a', 'a'), {'a': 'A'}, {'a': 'yes'}),
               lambda: m.task_exact(('a',), {}, {'a': 'yes'}), lambda: m.task_exact(('a',), {'a': 'A'}, {'a': 'yes', 'b': 'no'})]
    for budget in (True, False, -1, 0.0, '0', None):
        invalid.append(lambda budget=budget: hs.candidates((), budget))
    for values in (None, 'x', b'x', 12, [('x', None)], [('', '0')]):
        invalid.append(lambda values=values: hs.candidates(values))
    for call in invalid:
        rejects(call)
    points, predictions = ['x'], ['0']
    space = m.HypothesisSpace(points, [('h', predictions)])
    points[0], predictions[0] = 'changed', '1'
    check(space.candidates((('x', '0'),)) == {'h'}, 'input_snapshot')
    entries = [['a', 'A']]
    vocabulary = m.Vocabulary(entries)
    entries[0][1] = 'B'
    check(vocabulary.encode(('a',)) == {'A'}, 'input_snapshot')
    premises = ['a']
    rule = m.Rule('r', premises, 'b')
    premises.append('c')
    check(rule.premises == {'a'}, 'input_snapshot')
    check(m.translation_preserves(m.Vocabulary(()), m.Vocabulary(()), {}), 'empty_vocabulary')
    COUNTS['malformed_input_cases'] = len(invalid)


def main():
    for routine in (hypotheses, horn, vocabularies, task_partitions, validation):
        routine()
    print(json.dumps({'passed': True, 'optimize': sys.flags.optimize, 'python': sys.version,
        'model_sha256': hashlib.sha256((ROOT / 'model.py').read_bytes()).hexdigest(),
        'independent_check_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'counts': dict(sorted(COUNTS.items())), 'check_counts': dict(sorted(CHECKS.items())),
        'total_explicit_checks': sum(CHECKS.values()),
        'limits': 'Finite model checks, not proofs. Does not import author test_model or mutation_check.'},
        ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
