"""Retest a frozen teaching artifact with independent tests in three Python modes.

No installs, network, or writes to the reviewed artifact. Retains one real log and
one hash/result summary. Only absolute execution paths are replaced in logs.
"""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import sysconfig
import tempfile
import time

HERE = Path(__file__).resolve().parent
MARKER = 'REVIEW_RECORD='
HARNESS = r'''
import importlib, json, sys, traceback, unittest
try:
    target = importlib.import_module('test_independent')
except BaseException as exc:
    traceback.print_exc()
    print('REVIEW_RECORD=' + json.dumps({'phase':'import','type':type(exc).__name__, 'optimize':sys.flags.optimize}))
    sys.exit(3)
class Tracked(unittest.TextTestResult):
    started = 0
    finished = 0
    def startTest(self, test):
        self.started += 1
        super().startTest(test)
    def stopTest(self, test):
        self.finished += 1
        super().stopTest(test)
suite = unittest.defaultTestLoader.loadTestsFromName(sys.argv[1], target)
r = unittest.TextTestRunner(verbosity=2, resultclass=Tracked).run(suite)
print('REVIEW_RECORD=' + json.dumps({'phase':'done','tests':r.testsRun,'started':r.started,'finished':r.finished,
    'failures':len(r.failures),'errors':len(r.errors),'skipped':len(r.skipped),'optimize':sys.flags.optimize,
    'coverage':target.COVERAGE}, sort_keys=True))
sys.exit(0 if r.wasSuccessful() else 1)
'''
MUTANTS = (
    ('ignore_precedence', 'and all(a in prefix for a, b in frozen_edges if b == feature)', 'and True', 'test_context_sentinel'),
    ('forget_prefix_tail', '[:len(observed)] == observed', '[:max(0, len(observed)-1)] == observed[:-1]', 'test_prefix_sentinel'),
    ('keep_only_first_order', 'for order in self.orders))', 'for order in self.orders[:1]))', 'test_prefix_sentinel'),
    ('discard_binding', 'return frozenset(zip(self.labels, self._message(message)))', 'return frozenset(("?", v) for v in self._message(message))', 'test_binding_and_multiplicity_sentinel'),
    ('discard_multiplicity', 'Counter(self._message(message))', 'Counter(set(self._message(message)))', 'test_binding_and_multiplicity_sentinel'),
    ('pretend_injective', 'return len({token for _, token in self.lexicon}) == len(self.lexicon)', 'return True', 'test_collision_and_decode_sentinel'),
    ('reverse_meaning', 'return next(iter(compatible))', 'return tuple(reversed(next(iter(compatible))))', 'test_collision_and_decode_sentinel'),
    ('accept_ambiguity', 'if len(compatible) != 1:', 'if not compatible:', 'test_collision_and_decode_sentinel'),
    ('erase_frame_boundaries', '_strings(tokens, "tokens"), ensure_ascii=False', '"".join(_strings(tokens, "tokens")), ensure_ascii=False', 'test_frame_sentinel_and_edge_cases'),
    ('accept_one_example', 'if all(table[index] == value for index, value in observations)', 'if any(table[index] == value for index, value in observations)', 'test_version_space_sentinel'),
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_manifest(source):
    return {p.relative_to(source).as_posix(): digest(p) for p in sorted(source.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts
            and 'independent-review' not in p.relative_to(source).parts and p.suffix in ('.py', '.md')}


def classify(result, expected_tests, optimization):
    if result.get('timeout'):
        return 'timeout'
    records = [line[len(MARKER):] for line in result['stdout'].splitlines() if line.startswith(MARKER)]
    if len(records) != 1:
        return 'harness_failure'
    try:
        r = json.loads(records[0])
    except (ValueError, TypeError):
        return 'harness_failure'
    result['record'] = r
    if r.get('optimize') != optimization:
        return 'harness_failure'
    if r.get('phase') == 'import':
        if result['exit_code'] != 3:
            return 'harness_failure'
        if r.get('type') in ('SyntaxError', 'IndentationError', 'TabError'):
            return 'syntax_failure'
        return 'import_failure'
    if (r.get('phase') != 'done' or any(r.get(k) != expected_tests for k in ('tests', 'started', 'finished'))
            or r.get('skipped') != 0 or type(r.get('errors')) is not int or type(r.get('failures')) is not int):
        return 'harness_failure'
    if r['errors']:
        return 'test_error' if result['exit_code'] == 1 else 'harness_failure'
    if r['failures']:
        return 'behavior_caught' if result['exit_code'] == 1 else 'harness_failure'
    return 'survived' if result['exit_code'] == 0 else 'harness_failure'


def run(folder, command, timeout=90):
    try:
        done = subprocess.run(command, cwd=folder, capture_output=True, text=True, timeout=timeout)
        return {'exit_code': done.returncode, 'stdout': done.stdout, 'stderr': done.stderr}
    except subprocess.TimeoutExpired as exc:
        def text(value):
            return value.decode('utf-8', errors='replace') if isinstance(value, bytes) else (value or '')
        return {'exit_code': None, 'timeout': True, 'stdout': text(exc.stdout), 'stderr': text(exc.stderr)}


def clean(text, source, folder):
    text = text.replace(str(folder), '<audit-temp>').replace(str(source), '<reviewed-source>')
    text = text.replace(str(HERE), '<independent-review>').replace(sys.executable, 'python')
    text = text.replace(sysconfig.get_path('stdlib'), '<stdlib>')
    # Tracebacks may expose Python's stdlib install location rather than a project path.
    return re.sub(r'File "[^"\n]*/(unittest/[^"\n]+)"', r'File "<stdlib>/\1"', text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir', type=Path, default=HERE.parent)
    args = parser.parse_args()
    source = args.source_dir.resolve()
    if not (source / 'model.py').is_file():
        raise SystemExit('model.py missing; pass --source-dir with the teaching artifact directory')
    started = time.perf_counter()
    manifest = source_manifest(source)
    review_manifest = {p.name: digest(p) for p in sorted(HERE.glob('*.py'))}
    for path in [*(source.glob('*.py')), *(HERE.glob('*.py'))]:
        tree = ast.parse(path.read_text(encoding='utf-8'))
        if any(isinstance(node, ast.Assert) for node in ast.walk(tree)):
            raise RuntimeError('bare assert found in ' + path.name)
    summary = {'reviewed_at_utc': datetime.now(timezone.utc).isoformat(), 'python': sys.version,
               'scope': 'Independent finite-model audit; no historical or empirical validation',
               'source_sha256': manifest, 'review_sha256': review_manifest, 'bare_assert_count': 0,
               'log_normalization': 'Only absolute execution paths replaced by placeholders; results and tracebacks retained.',
               'modes': {}, 'passed': False}
    original = (source / 'model.py').read_text(encoding='utf-8')
    with tempfile.TemporaryDirectory(prefix='condillac-independent-') as temp, (HERE / 'review.log').open('w', encoding='utf-8') as log:
        folder = Path(temp)
        shutil.copy2(HERE / 'test_independent.py', folder)
        shutil.copy2(source / 'test_model.py', folder)
        for mode, flags, optimization in (('normal', [], 0), ('O', ['-O'], 1), ('OO', ['-OO'], 2)):
            records = []
            def execute(label, code, target, expected, tests=1, timeout=90):
                (folder / 'model.py').write_text(code, encoding='utf-8')
                command = [sys.executable, *flags, '-B', '-c', HARNESS, target]
                r = run(folder, command, timeout)
                outcome = classify(r, tests, optimization)
                log.write('\n=== ' + mode + ': ' + label + ' ===\n')
                log.write('$ python ' + ' '.join(flags) + ' -B -c <embedded HARNESS> ' + target + '\n')
                log.write('--- stdout ---\n' + clean(r['stdout'], source, folder))
                log.write('--- stderr ---\n' + clean(r['stderr'], source, folder))
                log.write('--- exit code: ' + str(r['exit_code']) + '; classification: ' + outcome + ' ---\n')
                log.flush()
                row = {'name': label, 'expected': expected, 'outcome': outcome, 'exit_code': r['exit_code']}
                if 'record' in r:
                    row['record'] = r['record']
                records.append(row)
                if outcome != expected:
                    raise RuntimeError(mode + '/' + label + ': expected ' + expected + ', got ' + outcome)
            execute('independent_suite', original, 'IndependentTests', 'survived', tests=11)
            # Baseline every sentinel separately before each isolated behavioral mutation.
            for name, old, new, test in MUTANTS:
                if original.count(old) != 1:
                    raise RuntimeError('Mutation anchor not unique: ' + name)
                execute(name + '/baseline', original, 'IndependentTests.' + test, 'survived')
                execute(name + '/mutation', original.replace(old, new), 'IndependentTests.' + test, 'behavior_caught')
            for name, text, expected, timeout in (
                ('syntax_control', 'def broken(:\n', 'syntax_failure', 10),
                ('import_control', 'import nonexistent_independent_audit_control\n', 'import_failure', 10),
                ('early_exit_control', 'import os; os._exit(0)\n', 'harness_failure', 10),
                ('timeout_control', 'import time; time.sleep(10)\n', 'timeout', 0.2),
                ('runtime_error_control', original.replace('observed = _strings(prefix, "prefix")', 'raise RuntimeError("intentional audit runtime error")'), 'test_error', 10)):
                execute(name, text, 'IndependentTests.test_prefix_sentinel', expected, timeout=timeout)
            # Rerun author tests too, but never substitute them for the independent oracle.
            (folder / 'model.py').write_text(original, encoding='utf-8')
            author = run(folder, [sys.executable, *flags, '-B', '-m', 'unittest', '-v', 'test_model'])
            log.write('\n=== ' + mode + ': author_tests_rerun ===\n$ python ' + ' '.join(flags) + ' -B -m unittest -v test_model\n')
            log.write('--- stdout ---\n' + clean(author['stdout'], source, folder) + '--- stderr ---\n' + clean(author['stderr'], source, folder))
            log.write('--- exit code: ' + str(author['exit_code']) + ' ---\n')
            if author['exit_code'] != 0 or not re.search(r'Ran 28 tests in [^\n]+\n\nOK\s*$', author['stderr']):
                raise RuntimeError('Author rerun did not complete all 28 tests in ' + mode)
            summary['modes'][mode] = {'independent': records, 'author_test_methods': 28, 'author_passed': True}
    after = source_manifest(source)
    if after != manifest or {p.name: digest(p) for p in sorted(HERE.glob('*.py'))} != review_manifest:
        raise RuntimeError('Source changed during the audit; final result cannot be certified')
    summary['source_unchanged'] = True
    summary['elapsed_seconds'] = round(time.perf_counter() - started, 6)
    summary['passed'] = True
    (HERE / 'review-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': True, 'modes': list(summary['modes']), 'independent_test_methods_per_mode': 11,
                      'author_test_methods_per_mode': 28, 'behavior_mutations_per_mode': len(MUTANTS),
                      'classification_controls_per_mode': 5, 'source_unchanged': True,
                      'logs': ['review.log', 'review-summary.json']}, indent=2))


if __name__ == '__main__':
    main()
