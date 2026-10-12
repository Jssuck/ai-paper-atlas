"""Run independent boundary/oracle/mutation audits in all three Python modes.

Invoke once: python -B independent-review/run_audit.py
Only this directory is written; release model and author tests are never edited.
"""
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
MODEL_ROOT = HERE.parent
LOGS = HERE / 'logs'
MODES = [('normal', [], 0), ('O', ['-O'], 1), ('OO', ['-OO'], 2)]
MUTANTS = {
    'evidence_union': ('current = current & compatible', 'current = current | compatible'),
    'evidence_overwrite': ('current = current & compatible', 'current = compatible'),
    'ignore_initial': ('current = universe if initial is None else _subset(initial, universe, "initial")',
                       'current = universe'),
    'stop_when_empty': ('for index, observation in enumerate(observations):',
                       'for index, observation in enumerate(observations):\n        if not current:\n            return tuple(trace)'),
    'foreign_labels_allowed': ('if not result <= universe:', 'if False:'),
    'empty_body_allowed': ('if not body:', 'if False:'),
    'any_premise_suffices': ('if rule.body <= state', 'if bool(rule.body & state)'),
    'conjunctions_dropped': ('if rule.body <= state', 'if rule.body <= state and len(rule.body) == 1'),
    'anchors_dropped': ('return (anchors | derived) - withdrawn', 'return frozenset(derived) - withdrawn'),
    'withdrawal_ignored': ('return anchors, withdrawn', 'return anchors, frozenset()'),
    'state_self_support': ('return (anchors | derived) - withdrawn', 'return (state | anchors | derived) - withdrawn'),
    'least_starts_at_top': ('current = frozenset() if kind == "least" else self.claims - withdrawn',
                            'current = self.claims - withdrawn'),
    'greatest_starts_at_bottom': ('current = frozenset() if kind == "least" else self.claims - withdrawn',
                                 'current = frozenset()'),
    'premature_stop': ('if following == current:', 'if following == current or len(states) > 1:'),
    'wrong_change_count': ('return len(self.states) - 1', 'return len(self.states)'),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sanitize(text, temporary=None):
    if temporary is not None:
        text = text.replace(str(temporary), 'ISOLATED_MODEL_COPY')
    return text.replace(str(MODEL_ROOT), 'MODEL_ROOT')


def expected_methods():
    tree = ast.parse((HERE / 'test_independent.py').read_text())
    require(not any(isinstance(x, ast.Assert) for x in ast.walk(tree)), 'bare assert in boundary tests')
    methods = sorted(x.name for group in tree.body if isinstance(group, ast.ClassDef)
                     and group.name == 'BoundaryTests' for x in group.body
                     if isinstance(x, ast.FunctionDef) and x.name.startswith('test_'))
    require(len(methods) == 22 and len(set(methods)) == 22, 'expected 22 distinct boundary tests')
    for filename in ('oracle.py', 'run_audit.py'):
        parsed = ast.parse((HERE / filename).read_text())
        require(not any(isinstance(x, ast.Assert) for x in ast.walk(parsed)), 'bare assert in ' + filename)
    return methods


def classify(returncode, output, methods, optimize):
    markers = [line.removeprefix('AUDIT_RESULT=') for line in output.splitlines()
               if line.startswith('AUDIT_RESULT=')]
    if len(markers) != 1:
        return 'harness_failure', None
    try:
        data = json.loads(markers[0])
    except (TypeError, ValueError):
        return 'harness_failure', None
    if not isinstance(data, dict):
        return 'harness_failure', data
    numeric = ('tests', 'failures', 'errors', 'skipped', 'expected_failures', 'unexpected_successes', 'optimize')
    if any(type(data.get(key)) is not int or data[key] < 0 for key in numeric):
        return 'harness_failure', data
    if data['optimize'] != optimize:
        return 'harness_failure', data
    if data['tests'] != len(methods) or data.get('started') != methods or data.get('completed') != methods:
        return 'suite_mismatch', data
    if data['errors']:
        return 'test_error', data
    if any(data[k] for k in ('skipped', 'expected_failures', 'unexpected_successes')):
        return 'suite_mismatch', data
    if returncode == 1 and data['failures'] > 0:
        return 'behavioral_kill', data
    if returncode == 0 and data['failures'] == 0:
        return 'survived', data
    return 'harness_failure', data


def boundary_run(source, mode, name, methods, extra=(), timeout=10):
    mode_name, flags, optimize = mode
    folder = LOGS / mode_name / 'mutation'
    folder.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.independent-mutant-', dir=HERE) as tmp:
        target = Path(tmp)
        (target / 'model.py').write_text(source, encoding='utf-8')
        env = dict(os.environ, AUDIT_MODEL_DIR=str(target))
        command = [sys.executable, *flags, '-B', str(HERE / 'test_independent.py'), *extra]
        try:
            p = subprocess.run(command, cwd=HERE, env=env, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            (folder / (name + '.log')).write_text(f'Actual subprocess timeout after {timeout} seconds.\n')
            return {'name': name, 'classification': 'timeout', 'returncode': None, 'summary': None}
        output = sanitize(p.stdout + p.stderr, target)
        (folder / (name + '.log')).write_text(output, encoding='utf-8')
        classification, summary = classify(p.returncode, p.stdout, methods, optimize)
        return {'name': name, 'classification': classification, 'returncode': p.returncode, 'summary': summary}


def regular_run(mode, script, destination, cwd):
    mode_name, flags, optimize = mode
    command = [sys.executable, *flags, '-B', str(script)]
    try:
        p = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        destination.write_text('Actual subprocess timeout after 120 seconds.\n')
        return {'returncode': None, 'timeout': True, 'success': False}
    destination.write_text(sanitize(p.stdout + p.stderr), encoding='utf-8')
    return {'returncode': p.returncode, 'timeout': False, 'success': p.returncode == 0}


def main():
    LOGS.mkdir(exist_ok=True)
    source = (MODEL_ROOT / 'model.py').read_text(encoding='utf-8')
    methods = expected_methods()
    report = {'independent': True, 'boundary_methods': len(methods), 'behavioral_mutants_per_mode': len(MUTANTS),
              'bare_asserts_in_audit_checks': 0, 'modes': {}}
    success = True
    for mode in MODES:
        mode_name, flags, optimize = mode
        folder = LOGS / mode_name
        folder.mkdir(exist_ok=True)
        baseline = boundary_run(source, mode, 'baseline', methods)
        records = []
        for name, (before, after) in MUTANTS.items():
            require(source.count(before) == 1, 'mutation site no longer unique: ' + name)
            records.append(boundary_run(source.replace(before, after), mode, name, methods))
        controls = [
            ('equivalent_survivor', source + '\n# Behavior-preserving control.\n', (), 10, 'survived'),
            ('syntax_error', source + '\ndef invalid(:\n', (), 10, 'harness_failure'),
            ('import_error', 'raise ImportError("intentional audit control")\n' + source, (), 10, 'harness_failure'),
            ('early_exit', 'raise SystemExit(0)\n' + source, (), 10, 'harness_failure'),
            ('empty_suite', source, ('--empty',), 10, 'suite_mismatch'),
            ('duplicate_marker', source, ('--duplicate-marker',), 10, 'harness_failure'),
            ('test_exception', source.replace('derived = {rule.head',
                 'raise RuntimeError("intentional audit control")\n        derived = {rule.head'), (), 10, 'test_error'),
            ('real_timeout', 'import time\ntime.sleep(4)\n' + source, (), 0.2, 'timeout'),
        ]
        control_records = []
        for name, changed, args, timeout, expected in controls:
            result = boundary_run(changed, mode, name, methods, args, timeout)
            result['expected'] = expected
            result['correct'] = result['classification'] == expected
            control_records.append(result)
        oracle = regular_run(mode, HERE / 'oracle.py', folder / 'oracle.json', HERE)
        author_tests = regular_run(mode, MODEL_ROOT / 'test_model.py', folder / 'author-tests.log', MODEL_ROOT)
        author_enumeration = regular_run(mode, MODEL_ROOT / 'exhaustive.py', folder / 'author-exhaustive.json', MODEL_ROOT)
        if oracle['success']:
            try:
                evidence = json.loads((folder / 'oracle.json').read_text())
                oracle['success'] = evidence.get('success') is True and evidence.get('optimize') == optimize
            except ValueError:
                oracle['success'] = False
        if author_enumeration['success']:
            try:
                evidence = json.loads((folder / 'author-exhaustive.json').read_text())
                author_enumeration['success'] = evidence.get('success') is True and evidence.get('optimization') == optimize
            except ValueError:
                author_enumeration['success'] = False
        counts = dict(Counter(r['classification'] for r in records))
        for kind in ('behavioral_kill', 'survived', 'harness_failure', 'suite_mismatch', 'test_error', 'timeout'):
            counts.setdefault(kind, 0)
        mode_success = (baseline['classification'] == 'survived'
                        and counts['behavioral_kill'] == len(MUTANTS)
                        and all(x['correct'] for x in control_records)
                        and oracle['success'] and author_tests['success'] and author_enumeration['success'])
        success = success and mode_success
        report['modes'][mode_name] = {'optimization': optimize, 'baseline': baseline,
              'mutant_counts': counts, 'mutants': records, 'controls': control_records,
              'oracle': oracle, 'author_tests_rerun': author_tests, 'author_enumeration_rerun': author_enumeration,
              'success': mode_success}
        print(json.dumps({'mode': mode_name, 'success': mode_success, 'mutant_counts': counts}), flush=True)
    report['success'] = success
    (LOGS / 'audit-report.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    files = ['model.py', 'demo.py', 'test_model.py', 'exhaustive.py', 'MODEL.zh-CN.md', 'mutation_check.py']
    environment = {'utc': datetime.now(timezone.utc).isoformat(), 'implementation': platform.python_implementation(),
         'python_version': platform.python_version(), 'system': platform.system(), 'release': platform.release(),
         'machine': platform.machine(), 'third_party_dependencies': [],
         'execution': 'Local subprocesses only; no installations or remote writes.',
         'target_sha256': {name: hashlib.sha256((MODEL_ROOT / name).read_bytes()).hexdigest() for name in files},
         'audit_sha256': {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                          for name in ('test_independent.py', 'oracle.py', 'run_audit.py')}}
    (LOGS / 'environment.json').write_text(json.dumps(environment, indent=2, sort_keys=True) + '\n')
    require(success, 'one or more audit stages failed; inspect logs/audit-report.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
