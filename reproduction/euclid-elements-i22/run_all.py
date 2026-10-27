"""Run all checks and rebuild public evidence; no installs and no network."""
import ast
import hashlib
import importlib.util
import json
import platform
import subprocess
import sys
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path
import test_geometry

ROOT = Path(__file__).resolve().parent
(ROOT / 'logs').mkdir(exist_ok=True)


def write(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def utc_now():
    return datetime.now(timezone.utc).isoformat()


started = utc_now()
write('environment.json', {
    'python_version': platform.python_version(),
    'implementation': platform.python_implementation(),
    'system': platform.system(), 'machine': platform.machine(),
    'dependencies_used': 'Python standard library only; no dependencies installed',
    'optional_packages_detected_not_used': {name: importlib.util.find_spec(name) is not None
                                           for name in ('nbformat', 'nbclient', 'ipykernel')},
    'notebook_executor': 'standard-library compile/exec; no Jupyter kernel or browser execution',
})
records = []
results = []
tests = unittest.defaultTestLoader.loadTestsFromModule(test_geometry).countTestCases()
# Regression gates cannot disappear under optimization flags.
for name in ('geometry.py', 'cases.py', 'test_geometry.py', 'run_examples.py', 'verify_notebook.py'):
    if any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse((ROOT / name).read_text()))):
        raise RuntimeError('bare assert found in optimization-sensitive code: ' + name)


def run(script, flags=(), log='logs/notebook-execute.log'):
    command = [sys.executable, *flags, script]
    begin, clock = utc_now(), time.perf_counter()
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    duration = time.perf_counter() - clock
    # Exact argv is retained; it contains no environment variables or secrets.
    public_command = ' '.join(command)
    (ROOT / log).write_text('$ ' + public_command + '\n' + result.stdout + result.stderr
                           + '\nexit_code=' + str(result.returncode) + '\n')
    records.append({'command_argv': command, 'cwd': '.', 'started_at_utc': begin,
                    'duration_seconds': duration, 'exit_code': result.returncode, 'log': log})
    if result.returncode:
        write('run-summary.json', {'status': 'failed', 'started_at_utc': started, 'commands': records})
        raise SystemExit(result.returncode)
    return result.stdout


for label, flags in (('normal', []), ('O', ['-O']), ('OO', ['-OO'])):
    run('test_geometry.py', flags, f'logs/tests-{label}.log')
    result = json.loads(run('run_examples.py', flags, f'logs/examples-{label}.log'))
    write(f'results-{label}.json', result)
    results.append(result)
if not all(result == results[0] for result in results):
    raise RuntimeError('optimization-mode results disagree')
run('create_notebook.py', log='logs/notebook-create.log')
notebook_check = json.loads(run('verify_notebook.py'))
write('notebook-check.json', notebook_check)
write('run-summary.json', {
    'status': 'passed', 'started_at_utc': started, 'completed_at_utc': utc_now(),
    'commands': records, 'tests_per_mode': tests,
    'positive_certificates_per_mode': results[0]['positive_certificates'],
    'negative_inputs_per_mode': results[0]['negative_inputs'],
    'optimization_results_identical': True,
    'no_bare_assert_in_checked_sources': True,
    'notebook_code_cells': notebook_check['code_cells_executed'],
})
files = [p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts
         and p.name != 'SHA256SUMS.json' and not p.name.endswith('.pyc')]
write('SHA256SUMS.json', {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(files)})
print(json.dumps({'status': 'passed', 'commands': len(records), 'tests_per_mode': tests,
                  'positive_certificates_per_mode': results[0]['positive_certificates'],
                  'negative_inputs_per_mode': results[0]['negative_inputs'],
                  'notebook_code_cells': notebook_check['code_cells_executed']}, indent=2))
