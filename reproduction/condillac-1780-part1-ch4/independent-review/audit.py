#!/usr/bin/env python3
"""Independent, standard-library audit. Run from anywhere; no subject edits.

After the author freezes the package, use --freeze once to record its bytes.
Later runs verify those same bytes before and after testing. All subprocess
replays occur in disposable copies under this audit directory. No implementation
or test helper is used to calculate the independent expected answers.
"""
import argparse
import ast
import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import types

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COUNTS = {}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files():
    paths = sorted([*ROOT.glob('*.py'), *ROOT.glob('*.md'),
                    *(p for p in (ROOT / 'results').rglob('*') if p.is_file())])
    return {p.relative_to(ROOT).as_posix(): sha(p) for p in paths}


def record_json(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, sort_keys=True,
                                     indent=2) + '\n', encoding='utf-8')


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def rejects(error, action):
    try:
        action()
    except error:
        return
    except Exception as exc:
        raise AssertionError(f'Expected {error.__name__}, got {type(exc).__name__}') from exc
    raise AssertionError(f'Expected {error.__name__}, returned normally')


def rgs(n):
    """Restricted-growth words: independent of author's recursive block enumerator."""
    if n == 0:
        return [()]
    words = [(0,)]
    for _ in range(n - 1):
        words = [word + (next_label,) for word in words
                 for next_label in range(max(word) + 2)]
    return words


def blocks(word):
    return tuple(tuple(str(i) for i, label in enumerate(word) if label == group)
                 for group in sorted(set(word)))


def relation(partition, ids):
    flattened = [member for block in partition for member in block]
    require(all(partition), 'Empty block in returned partition')
    require(set(flattened) == set(ids), 'Wrong object domain')
    require(len(flattened) == len(set(flattened)), 'Overlapping/duplicate objects')
    return {(x, y) for block in partition for x in block for y in block}


def oracle_lattice(m):
    words = rgs(4)
    require(len(words) == 15 and len(set(words)) == 15, 'Independent enumerator wrong')
    ids = tuple(str(i) for i in range(4))
    checked = 0
    for left_word in words:
        left = blocks(left_word)
        left_rel = relation(left, ids)
        for right_word in words:
            right = blocks(right_word)
            right_rel = relation(right, ids)
            require(m.is_refinement(left, right) == (left_rel <= right_rel),
                    'Refinement disagrees with pair-relation inclusion')
            got = relation(m.common_refinement(left, right), ids)
            require(got == left_rel & right_rel, 'Common refinement pair-relation mismatch')
            checked += 1
    COUNTS['partition_pair_cases'] = checked


def oracle_tasks(m):
    words = rgs(4)
    ids = tuple(str(i) for i in range(4))
    candidates = [blocks(word) for word in words]
    checked = 0
    for a in words:
        for b in words:
            target = {str(i): (str(a[i]), str(b[i])) for i in range(4)}
            items = tuple(m.Item(oid, {}, {'a': target[oid][0], 'b': target[oid][1]}) for oid in ids)
            ideal = m.task_partition(items, ('b', 'a'))
            expected_rel = {(x, y) for x in ids for y in ids if target[x] == target[y]}
            require(relation(ideal, ids) == expected_rel, 'Task output relation mismatch')
            valid = []
            for candidate in candidates:
                expected = all(target[x] == target[y]
                               for block in candidate for x in block for y in block)
                require(m.is_sufficient(items, candidate, ('a', 'b')) == expected,
                        'Sufficiency disagrees with direct pairwise target comparison')
                if expected:
                    valid.append(candidate)
                checked += 1
            smallest = min(len(candidate) for candidate in valid)
            minimizers = [candidate for candidate in valid if len(candidate) == smallest]
            require(len(minimizers) == 1, 'Oracle found multiple minimum sufficient partitions')
            require(relation(ideal, ids) == relation(minimizers[0], ids),
                    'Implementation differs from independent exhaustive minimum')
            # No needs, repetition, reordering, addition, and withdrawal.
            require(relation(m.task_partition(items, ()), ids) == {(x, y) for x in ids for y in ids},
                    'No-needs partition wrong')
            require(m.task_partition(tuple(reversed(items)), ('a', 'b', 'a')) == ideal,
                    'Order or repeated need changes normalized partition')
            for field in ('a', 'b'):
                reduced = relation(m.task_partition(items, (field,)), ids)
                require(expected_rel <= reduced, 'Adding a need unexpectedly coarsens')
    COUNTS['two_task_assignments'] = len(words) ** 2
    COUNTS['independent_sufficiency_and_minimum_cases'] = checked
    require(m.task_partition((), ('missing',)) == (), 'Empty domain task partition wrong')
    require(m.is_sufficient((), (), ('missing',)), 'Empty-domain sufficiency wrong')
    require(m.common_refinement((), ()) == (), 'Empty meet wrong')


def oracle_observations(m):
    ids = ('0', '1', '2')
    atoms = (None, True, 1)  # Reports must retain both missingness and scalar type.
    possible_outputs = tuple(itertools.product(('0', '1'), repeat=2))
    checked = 0
    for obs in rgs(3):
        for target_vector in itertools.product(possible_outputs, repeat=3):
            target = dict(zip(ids, target_vector))
            items = tuple(m.Item(oid, {'x': atoms[obs[i]]},
                                 {'a': target[oid][0], 'b': target[oid][1]}) for i, oid in enumerate(ids))
            expected_pairs = []
            for i in range(3):
                for j in range(i + 1, 3):
                    if obs[i] != obs[j]:
                        continue
                    different = [field for k, field in enumerate(('a', 'b'))
                                 if target[str(i)][k] != target[str(j)][k]]
                    if different:
                        expected_pairs.append({'objects': [str(i), str(j)], 'different_needs': different})
            # Enumerate all possible deterministic decision tables h independently.
            exists_h = any(all(table[obs[i]] == target_vector[i] for i in range(3))
                           for table in itertools.product(possible_outputs, repeat=max(obs) + 1))
            require(exists_h == (not expected_pairs), 'Independent decision-table oracle mismatch')
            got = m.observation_conflicts(items, ('x',), ('b', 'a'))
            require(got == expected_pairs, 'Missing, spurious, or wrongly labelled conflict witness')
            expected_rel = {(ids[i], ids[j]) for i in range(3) for j in range(3) if obs[i] == obs[j]}
            require(relation(m.observation_partition(items, ('x',)), ids) == expected_rel,
                    'Observation equality uses target or collapses different report types')
            require((not got) == exists_h, 'Identifiability differs from exhaustive decision table search')
            checked += 1
    COUNTS['observation_and_decision_table_cases'] = checked


def evidence_cases(m):
    for raw, state in ((True, m.Truth.TRUE), (False, m.Truth.FALSE), (None, m.Truth.UNKNOWN)):
        require(m.observed_truth(raw) is state, 'Three-state evidence misclassified')
    for state in m.Truth:
        rejects(TypeError, lambda state=state: bool(state))
    for value in (0, 1, '', [], 'false'):
        rejects(ValueError, lambda value=value: m.observed_truth(value))
    # Accuracy differs from both finite-table coverage and task sufficiency.
    truth = {'green': True, 'height': 5.0}
    require(m.claims_are_accurate(truth, {'green': True}), 'Accurate partial claim rejected')
    require(m.claims_are_accurate(truth, {}), 'Empty claim is not vacuously accurate')
    require(not m.claims_are_accurate(truth, {'green': 1}), 'Truth/one conflated in claims')
    require(not m.claims_are_accurate(truth, {'essence': 'known'}), 'Unsupported essence verified')
    require(not m.claims_are_accurate(truth, {'height': 6.0}), 'Wrong complete-table value accepted')
    require(not m.claims_are_accurate({'a': None}, {'a': None}), 'Two unknown reports verify a fact')
    require(not m.claims_are_accurate({'a': None}, {'a': False}), 'Unknown reference becomes false evidence')
    for height, expected in ((0, 'shrub'), (3.999, 'shrub'), (4, 'plant'), (6, 'plant'),
                             (6.001, 'tree'), (None, 'plant')):
        require(m.boundary_name(height) == expected, 'Boundary convention mismatch')
    require(m.boundary_name(10**500) == 'tree', 'Large finite integer height rejected')
    require(m.boundary_name(5, 0, 10**500) == 'plant', 'Large finite integer threshold rejected')
    same_name = (('x', 'y'),)
    items = (m.Item('x', {}, {'display': 'keep', 'move': 'small'}),
             m.Item('y', {}, {'display': 'keep', 'move': 'large'}))
    require(m.is_sufficient(items, same_name, ('display',)), 'Shared display should be sufficient')
    require(not m.is_sufficient(items, same_name, ('move',)), 'Changed task did not invalidate shared label')


def validation_cases(m):
    class DerivedString(str):
        pass
    subclass_items = (m.Item('x', {}, {'t': DerivedString('yes')}),)
    calls = [
        lambda: m.validate_items(subclass_items),
        lambda: m.task_partition(subclass_items, ('t',)),
        lambda: m.is_sufficient(subclass_items, (('x',),), ('t',)),
        lambda: m.validate_items((m.Item('x', {}, {}), m.Item('x', {}, {}))),
        lambda: m.task_partition((m.Item('x', {}, {}), m.Item('x', {}, {})), ()),
        lambda: m.task_partition((x for x in (m.Item('x', {}, {'t': 'a'}),)), ('t',)),
        lambda: m.task_partition(({},), ()),
        lambda: m.task_partition((m.Item('x', None, {}),), ()),
        lambda: m.task_partition((m.Item('x', {}, None),), ()),
        lambda: m.task_partition((m.Item('', {}, {}),), ()),
        lambda: m.task_partition((m.Item('x', {}, {'t': None}),), ()),
        lambda: m.task_partition((m.Item('x', {}, {'t': False}),), ()),
        lambda: m.task_partition((m.Item('x', {}, {'t': ''}),), ()),
        lambda: m.task_partition((m.Item('x', {}, {}),), ('t',)),
        lambda: m.task_partition((m.Item('x', {}, {}),), 'task'),
        lambda: m.observation_partition((m.Item('x', {}, {}),), ('x',)),
        lambda: m.observation_conflicts((m.Item('x', {'a': True}, {}),), ('a',), ('t',)),
        lambda: m.normalize_partition(((),)),
        lambda: m.normalize_partition((('x', 'x'),)),
        lambda: m.normalize_partition((('x',), ('x',))),
        lambda: m.normalize_partition('x'),
        lambda: m.normalize_partition(('x',)),
        lambda: m.is_sufficient((m.Item('x', {}, {}),), (('y',),), ()),
        lambda: m.is_refinement((('x',),), (('y',),)),
        lambda: m.common_refinement((('x',),), (('y',),)),
        lambda: m.claims_are_accurate({1: True}, {1: True}),
        lambda: m.claims_are_accurate({'': True}, {}),
        lambda: m.claims_are_accurate(None, {}),
        lambda: m.claims_are_accurate({}, None),
    ]
    for value in (float('nan'), float('inf'), -float('inf'), [], {}):
        calls.append(lambda value=value: m.observation_partition((m.Item('x', {'a': value}, {}),), ('a',)))
    for value in (-1, float('nan'), float('inf'), True, '5'):
        calls.append(lambda value=value: m.boundary_name(value))
    for low, high in ((4, 4), (6, 4), (float('nan'), 6), (4, float('inf')), (True, 6)):
        calls.append(lambda low=low, high=high: m.boundary_name(None, low, high))
    for call in calls:
        rejects(ValueError, call)
    COUNTS['invalid_input_calls'] = len(calls)
    for call in (lambda: m.normalize_partition(None),
                 lambda: m.normalize_partition((1,)),
                 lambda: m.task_partition((), None)):
        rejects(TypeError, call)
    COUNTS['out_of_declared_container_type_probes'] = 3


def summary_fault_injection(exp):
    result = copy.deepcopy(exp.experiments())
    result['refinement']['joint_equals_common_refinement'] = False
    result['observation_limit']['remaining_conflicts_after_enrichment'] = [
        {'objects': ['injected-x', 'injected-y'], 'different_needs': ['harvest']}]
    result['boundary_names']['all_plant_sufficient_for_display'] = False
    result['unknown']['unknown_equals_false'] = True
    result['accuracy_and_completeness']['partial_claim_accurate'] = False
    result['accuracy_and_completeness']['partial_claim_covers_all_reference_fields'] = True
    report = exp.summary(result)
    for required in ('共同细化: False', '观测后的采收冲突数: 1',
                     '仍充分: False', '未知 = 假: True',
                     '准确 False', '所有字段 True'):
        require(required in report, f'Summary ignores injected data: {required}')
    return report


def fixture_result_check(exp):
    result = exp.experiments()
    rows = {row['object_id']: row for row in result['objects']}
    ids = tuple(sorted(rows))
    require(len(ids) == 8, 'Fixture should contain eight invented individuals')
    require([stage['classes'] for stage in result['stages']] == [1, 2, 5, 7, 8, 5],
            'Published class progression differs from hand-worked example')
    for stage in result['stages']:
        needs = stage['needs']
        target = {oid: tuple(rows[oid]['targets'][need] for need in needs) for oid in ids}
        expected = {(x, y) for x in ids for y in ids if target[x] == target[y]}
        got = relation(stage['partition'], ids)
        require(got <= expected, 'Published stage is not independently sufficient')
        require(stage['classes'] == len(stage['partition']), 'Reported class count mismatch')
        if stage['stage'] == 'one_name_per_individual':
            require(got == {(x, x) for x in ids}, 'Per-individual stage is not discrete')
        else:
            require(got == expected, 'Published ideal stage is finer or coarser than necessary')
    expected_conflicts = [(x, y) for i, x in enumerate(ids) for y in ids[i+1:]
                          if rows[x]['attributes']['visible_green'] == rows[y]['attributes']['visible_green']
                          and rows[x]['targets']['harvest'] != rows[y]['targets']['harvest']]
    require(len(expected_conflicts) == result['observation_limit']['conflicting_pairs_count'] == 15,
            'Published green-only conflict count disagrees with direct pair oracle')
    require(list(expected_conflicts[0]) == result['observation_limit']['first_witness']['objects'],
            'Published first witness wrong')
    require(result['accuracy_and_completeness']['partial_claim_accurate'] is True,
            'Partial accuracy example wrong')
    require(result['accuracy_and_completeness']['partial_claim_covers_all_reference_fields'] is False,
            'Partial coverage example wrong')


def load_model(name, source):
    module = types.ModuleType(name)
    module.__file__ = str(ROOT / 'model.py')
    sys.modules[name] = module
    exec(compile(source, module.__file__, 'exec'), module.__dict__)
    return module


def mutation_checks(source):
    """Real source-byte substitutions, never edits to the delivered implementation."""
    specs = [
        ('drop_second_task', 'key = tuple(_atom_key(values[field]) for field in fields)',
         'key = tuple(_atom_key(values[field]) for field in fields[:1])', oracle_tasks),
        ('sufficiency_any_block', 'return all(\n        len({tuple(by_id[oid].targets[field]',
         'return any(\n        len({tuple(by_id[oid].targets[field]', oracle_tasks),
        ('hide_conflicts', 'if different:\n', 'if False:\n', oracle_observations),
        ('collapse_scalar_types', 'return type(value).__name__, value',
         'return "collapsed", value', oracle_observations),
        ('unknown_as_false', 'if value is None:\n        return Truth.UNKNOWN',
         'if value is None:\n        return Truth.FALSE', evidence_cases),
        ('truthy_unknown', 'raise TypeError("Three-valued evidence needs an explicit TRUE/FALSE/UNKNOWN branch")',
         'return True', evidence_cases),
        ('include_lower_endpoint_in_shrub', 'if height < low:', 'if height <= low:', evidence_cases),
        ('permit_duplicate_ids', 'if item.object_id in seen:', 'if False:', validation_cases),
    ]
    results = []
    for name, old, new, detector in specs:
        require(source.count(old) == 1, f'Mutation anchor mismatch: {name}')
        mutated = source.replace(old, new, 1)
        # Invalid syntax/import is a broken mutation, not a detected behavioral fault.
        module = load_model('audit_mutant_' + name, mutated)
        try:
            detector(module)
        except (AssertionError, ValueError, TypeError) as exc:
            results.append({'mutation': name, 'detector': detector.__name__, 'status': 'detected',
                            'failure': f'{type(exc).__name__}: {exc}',
                            'replacement': {'old': old, 'new': new}})
        else:
            results.append({'mutation': name, 'detector': detector.__name__, 'status': 'SURVIVED',
                            'replacement': {'old': old, 'new': new}})
    record_json('mutations.json', results)
    require(all(row['status'] == 'detected' for row in results), 'A specified fault survived')
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze', action='store_true', help='Record initial author-frozen file hashes')
    args = parser.parse_args()
    started = datetime.now(timezone.utc).isoformat()
    timer = time.perf_counter()
    frozen_path = HERE / 'frozen-files.sha256.json'
    current = files()
    if args.freeze:
        require(not frozen_path.exists(), 'Freeze file already exists; do not silently replace reviewed bytes')
        record_json(frozen_path.name, current)
    require(frozen_path.exists(), 'No frozen baseline: author must approve a freeze first')
    frozen = json.loads(frozen_path.read_text(encoding='utf-8'))
    require(current == frozen, 'Subject files differ from frozen baseline')
    records = []
    log = []
    status = 'failed'
    sys.path.insert(0, str(ROOT))
    try:
        source = (ROOT / 'model.py').read_text(encoding='utf-8')
        import model
        import run_experiments
        for line in (ROOT / 'results/manifest.sha256').read_text(encoding='utf-8').splitlines():
            digest, relative = line.split('  ', 1)
            require(frozen.get(relative) == digest, f'Author manifest mismatch: {relative}')
        records.append({'check': 'author_manifest_matches_frozen_bytes', 'status': 'passed'})
        fixture_result_check(run_experiments)
        records.append({'check': 'published_fixture_against_direct_pair_oracle', 'status': 'passed'})
        # Parse 3.10 grammar without claiming this substitutes for runtime testing.
        for path in ROOT.glob('*.py'):
            ast.parse(path.read_text(encoding='utf-8'), filename=path.name, feature_version=(3, 10))
        for test in (oracle_lattice, oracle_tasks, oracle_observations, evidence_cases, validation_cases):
            before = time.perf_counter()
            test(model)
            record = {'check': test.__name__, 'status': 'passed', 'seconds': time.perf_counter() - before}
            records.append(record)
            log.append(json.dumps(record, ensure_ascii=False))
        injected_report = summary_fault_injection(run_experiments)
        (HERE / 'injected-summary.txt').write_text(injected_report, encoding='utf-8')
        records.append({'check': 'summary_result_dictionary_fault_injection', 'status': 'passed'})
        count_snapshot = dict(COUNTS)
        mutation_results = mutation_checks(source)
        record_json('mutations.json', mutation_results)
        records.append({'check': 'source_mutations', 'status': 'passed', 'detected': len(mutation_results)})
        COUNTS.clear()
        COUNTS.update(count_snapshot)

        interpreters = [sys.executable]
        if Path('/usr/bin/python3.13').exists() and Path('/usr/bin/python3.13').resolve() != Path(sys.executable).resolve():
            interpreters.append('/usr/bin/python3.13')
        replay_records = []
        for index, interpreter in enumerate(interpreters):
            with tempfile.TemporaryDirectory(prefix='replay-', dir=HERE) as tmp:
                stage = Path(tmp)
                for relative in frozen:
                    # Include author delivered results to test byte equality after replay.
                    destination = stage / relative
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(ROOT / relative, destination)
                env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='293')
                completed = subprocess.run([interpreter, '-B', 'run_all.py'], cwd=stage, env=env,
                                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                output = completed.stdout.replace(str(stage), 'DISPOSABLE_AUDIT_COPY')
                (HERE / f'replay-{index}.log').write_text(output, encoding='utf-8')
                require(completed.returncode == 0, f'Author run_all failed under {interpreter}')
                environment = json.loads((stage / 'results/environment.json').read_text(encoding='utf-8'))
                hashes = {name: sha(stage / 'results' / name) for name in ('results.json', 'summary.txt')}
                require(all(digest == frozen['results/' + name] for name, digest in hashes.items()),
                        'Replay deterministic files differ from frozen delivery')
                for name in ('tests.log', 'environment.json', 'determinism.json'):
                    content = (stage / 'results' / name).read_text(encoding='utf-8').replace(str(stage), 'DISPOSABLE_AUDIT_COPY')
                    (HERE / f'replay-{index}-{name}').write_text(content, encoding='utf-8')
                replay_records.append({'python_version': environment['python_version'],
                                       'command': [Path(interpreter).name, '-B', 'run_all.py'], 'returncode': completed.returncode,
                                       'deterministic_hashes': hashes, 'delivered_bytes_match': True})
        records.append({'check': 'author_replays', 'status': 'passed', 'runs': replay_records})
        # Fail-closed check: inject one failing test in a disposable copy and verify no success.
        with tempfile.TemporaryDirectory(prefix='failure-', dir=HERE) as tmp:
            stage = Path(tmp)
            for relative in frozen:
                if relative.startswith('results/'):
                    continue
                destination = stage / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, destination)
            (stage / 'test_injected_failure.py').write_text(
                'import unittest\nclass InjectedFailure(unittest.TestCase):\n'
                '    def test_injected_failure(self):\n        self.fail("INTENTIONAL_AUDIT_FAILURE")\n', encoding='utf-8')
            completed = subprocess.run([sys.executable, '-B', 'run_all.py'], cwd=stage,
                                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            output = completed.stdout.replace(str(stage), 'DISPOSABLE_AUDIT_COPY')
            (HERE / 'injected-test-failure.log').write_text(output, encoding='utf-8')
            require(completed.returncode != 0, 'Runner incorrectly accepted failed test')
            require('FINAL STATUS: passed' not in output, 'Runner reported passed after test failure')
            require(not (stage / 'results/results.json').exists(), 'Runner continued to experiment after test failure')
            records.append({'check': 'runner_fails_closed_after_injected_test_failure', 'status': 'passed',
                            'injected_run_returncode': completed.returncode})
        require(files() == frozen, 'Subject changed during audit')
        status = 'passed'
    except Exception as exc:
        records.append({'check': 'audit_failure', 'status': 'failed', 'error': f'{type(exc).__name__}: {exc}'})
        raise
    finally:
        result = {'status': status, 'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
                  'seconds': time.perf_counter() - timer, 'python': sys.version, 'platform': platform.platform(),
                  'frozen_files': len(frozen), 'subject_unchanged': files() == frozen,
                  'independent_case_counts': COUNTS, 'checks': records,
                  'limits': ['Finite small-domain implementation checks are not a general theorem proof.',
                             'No empirical psychological, botanical, or historical influence validation.',
                             'Python 3.10 grammar parsed; only the listed runtime interpreters were executed.',
                             'Timing, environment paths and execution-log bytes are not deterministic outputs.',
                             'No concurrent mutation, adversarial custom container classes or infinite-input test.']}
        record_json('independent-results.json', result)
        (HERE / 'independent-execution.log').write_text('\n'.join(log) + '\n' + json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
