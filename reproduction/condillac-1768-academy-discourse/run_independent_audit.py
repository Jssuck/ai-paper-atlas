"""Capture independent audit evidence; only package-local audit/log files change.

The digest manifest is acyclic: it hashes inputs, AUDIT.md and logs, but not
itself. Run again after changing an input; the previous verdict is then stale.
"""
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
REVIEWED_INPUTS = (
    'model.py', 'demo.py', 'test_model.py', 'verify.py',
    'README.md', 'MODEL.md', 'WALKTHROUGH.md', 'RESULTS.md',
    'examples/expected_results.json', 'independent_checks.py',
    'run_independent_audit.py', 'AUDIT.md',
    '../../papers/1768/condillac-academy-discourse.zh-CN.md',
)
MODES = (('normal', []), ('optimized', ['-O']), ('double-optimized', ['-OO']))
NEGATIVE_CONTROLS = (
    ('missing_compiled_entry',
     "original = model.Tree.compile\n"
     "def mutated(self):\n"
     "    data = dict(original(self).table)\n"
     "    if data: data.pop(next(iter(data)))\n"
     "    return model.Lookup(data)\n"
     "model.Tree.compile = mutated\n",
     'IndependentTreeChecks.test_article_xor_eight_queries_and_preserved_error'),
    ('zero_reported_minimum_risk',
     "original = model.RepresentationDomain.best_decoder\n"
     "def mutated(self):\n"
     "    result = original(self)\n"
     "    return model.OptimalDecoder(result.decoder, result.error_mass, model.Fraction(0))\n"
     "model.RepresentationDomain.best_decoder = mutated\n",
     'IndependentRepresentationChecks.test_article_tie_refinement_and_binary_transfer'),
    ('structural_support_conflation',
     "original = model.RepresentationDomain.sufficient\n"
     "def mutated(self, positive_support_only=False):\n"
     "    return original(self, True)\n"
     "model.RepresentationDomain.sufficient = mutated\n",
     'IndependentRepresentationChecks.test_zero_support_fiber_tie_and_scale_invariance'),
    ('collapsed_diffusion_rounds',
     "original = model.diffuse\n"
     "def mutated(*args):\n"
     "    result = original(*args)\n"
     "    snapshots = result.snapshots\n"
     "    if len(snapshots) > 2: snapshots = (snapshots[0], snapshots[-1])\n"
     "    return model.Diffusion(result.judgment, snapshots)\n"
     "model.diffuse = mutated\n",
     'IndependentDiffusionChecks.test_article_chain_shortcut_and_reachable_cycles'),
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_hashes():
    return {name: sha256(ROOT / name) for name in REVIEWED_INPUTS}


def command_run(arguments, environment):
    started = time.perf_counter()
    result = subprocess.run([sys.executable, *arguments], cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    elapsed = time.perf_counter() - started
    # Failed negative controls include source locations. No private paths go into artifacts.
    output = result.stdout.decode('utf-8').replace(str(ROOT), '.')
    return result, output, elapsed


def main():
    audit, logs = ROOT / 'audit', ROOT / 'logs'
    audit.mkdir(exist_ok=True)
    logs.mkdir(exist_ok=True)
    hashes_before = input_hashes()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
    expected = (ROOT / 'examples/expected_results.json').read_bytes()
    static_assert_counts = {}
    for name in ('model.py', 'demo.py', 'test_model.py', 'independent_checks.py'):
        parsed = ast.parse((ROOT / name).read_text(encoding='utf-8'))
        static_assert_counts[name] = sum(isinstance(node, ast.Assert) for node in ast.walk(parsed))
    if any(static_assert_counts.values()):
        raise RuntimeError('An audited production/test file uses a removable assert statement')
    runs, all_logs = [], []
    for mode, flags in MODES:
        log_path = logs / f'independent-{mode}.log'
        chunks = ['Independent audit subprocess transcript. Command executable shown as python3;\n'
                  'any workspace traceback paths are rendered package-relative.\n']
        commands = [
            [*flags, '-c', "import sys; print('optimize=' + str(sys.flags.optimize)); print('debug=' + str(__debug__))"],
            [*flags, '-m', 'unittest', '-v', 'test_model'],
            [*flags, 'independent_checks.py'],
            [*flags, 'demo.py'],
        ]
        records = []
        for arguments in commands:
            result, output, elapsed = command_run(arguments, env)
            label = ['python3', *arguments]
            chunks += ['$ ' + ' '.join(label) + '\n', output,
                       f'exit_code={result.returncode}\nelapsed_seconds={elapsed:.6f}\n']
            log_path.write_text(''.join(chunks), encoding='utf-8')
            record = {'command': label, 'exit_code': result.returncode, 'elapsed_seconds': round(elapsed, 6)}
            if result.returncode:
                raise RuntimeError(f'{mode}: command failed; inspect the package-relative log')
            if arguments[-1] in ('test_model', 'independent_checks.py'):
                matched = re.search(r'Ran (\d+) tests? in', output)
                if not matched:
                    raise RuntimeError('Test runner did not report its executed test count')
                record['test_methods'] = int(matched.group(1))
            if arguments[-1] == 'independent_checks.py':
                record['finite_counts'] = json.loads(output.split('FINITE_AUDIT_COUNTS=', 1)[1].splitlines()[0])
            if arguments[-1] == 'demo.py':
                record['exact_demo_bytes_match'] = result.stdout == expected
                if not record['exact_demo_bytes_match']:
                    raise RuntimeError(f'{mode}: demo bytes differ from the frozen expected file')
            records.append(record)
        runs.append({'mode': mode, 'log': log_path.relative_to(ROOT).as_posix(), 'commands': records})
        all_logs.append(log_path)
        print(f'{mode}: regression suite, independent suite and exact demo comparison passed', flush=True)

    controls, chunks = [], ['Negative controls modify only a fresh subprocess in memory.\n'
                            'Expected assertion failures demonstrate that selected checks reject these faults.\n'
                            'Traceback locations are package-relative; other subprocess output is preserved.\n']
    for name, mutation, target in NEGATIVE_CONTROLS:
        source = ('import sys, unittest, model\n' + mutation +
                  'import independent_checks as checks\n' +
                  f'suite = unittest.defaultTestLoader.loadTestsFromName({target!r}, checks)\n' +
                  'result = unittest.TextTestRunner(verbosity=2).run(suite)\n'
                  'sys.exit(not result.wasSuccessful())\n')
        result, output, elapsed = command_run(['-c', source], env)
        detected = result.returncode == 1 and 'FAILED (failures=1)' in output
        chunks += [f'CONTROL={name}\nTARGET={target}\n', output,
                   f'exit_code={result.returncode}\nexpected_assertion_failure_detected={detected}\n']
        controls.append({'name': name, 'target': target, 'exit_code': result.returncode,
                         'expected_assertion_failure_detected': detected,
                         'elapsed_seconds': round(elapsed, 6)})
        if not detected:
            (logs / 'independent-negative-controls.log').write_text(''.join(chunks), encoding='utf-8')
            raise RuntimeError(f'Negative control {name} was not rejected as expected')
    control_log = logs / 'independent-negative-controls.log'
    control_log.write_text(''.join(chunks), encoding='utf-8')
    all_logs.append(control_log)
    hashes_after = input_hashes()
    if hashes_after != hashes_before:
        raise RuntimeError('Reviewed input changed during the audit; rerun before publishing a verdict')
    review = {
        'schema_version': 1,
        'status': 'passed_for_recorded_finite_checks',
        'recorded_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Independent automated code/API audit; not a human expert certification or general proof.',
        'limitations': ['No historical or psychological validation.',
                       'Only the explicit finite catalogs and schema cases were executed.',
                       'Minimum supported Python versions were not installed or tested.',
                       'No empirical runtime/space improvement claim is established.',
                       'Snapshot protection is ordinary mutation resistance, not a sandbox for hostile Python.'],
        'environment': {'interpreter': platform.python_implementation(), 'python_version': platform.python_version(),
                        'python_build': platform.python_build(), 'compiler': platform.python_compiler(),
                        'platform': platform.platform(), 'working_directory': '.',
                        'dependencies': 'Python standard library only', 'PYTHONHASHSEED': '0'},
        'static_python_assert_counts': static_assert_counts,
        'reviewed_input_sha256': hashes_after,
        'runs': runs,
        'negative_controls': controls,
        'log_sha256': {p.relative_to(ROOT).as_posix(): sha256(p) for p in all_logs},
        'binding_rule': 'Relative paths resolve from this package. Each digest binds exact bytes. This JSON excludes itself, so no circular self-hash exists. Changing a reviewed input or a log invalidates this recorded verdict.'
    }
    (audit / 'code_review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Four negative controls rejected; exact input/log digests saved to audit/code_review.json.', flush=True)


if __name__ == '__main__':
    main()
