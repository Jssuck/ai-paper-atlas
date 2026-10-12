"""Run independent and author checks, retaining compact actual evidence."""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
FILES = ('model.py', 'demo.py', 'test_model.py', 'mutation_check.py', 'run_all.py',
         'MODEL.zh-CN.md', 'README.md', 'WALKTHROUGH.zh-CN.md',
         'independent-review/independent_check.py', 'independent-review/run_audit.py')


def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in FILES}


def main():
    result = {'started_utc': datetime.now(timezone.utc).isoformat(),
              'python': sys.version, 'platform': platform.platform(), 'source_sha256_before': hashes(),
              'stages': [], 'passed': True}
    full_log = []
    for mode, flags in (('normal', []), ('O', ['-O']), ('OO', ['-OO'])):
        for stage, args in (
            ('independent', ['independent-review/independent_check.py']),
            ('author_unittest', ['-m', 'unittest', '-v', 'test_model']),
            ('author_mutation', ['mutation_check.py', '--mode', mode])):
            command = [sys.executable, *flags, '-B', *args]
            before = time.monotonic()
            run = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=180)
            entry = {'stage': stage, 'mode': mode, 'command': ['${PYTHON_EXECUTABLE}', *flags, '-B', *args],
                     'returncode': run.returncode, 'seconds': time.monotonic() - before,
                     'stdout_sha256': hashlib.sha256(run.stdout.encode()).hexdigest(),
                     'stderr_sha256': hashlib.sha256(run.stderr.encode()).hexdigest()}
            if stage == 'independent' and run.returncode == 0:
                parsed = json.loads(run.stdout)
                entry.update(passed=parsed['passed'], optimize=parsed['optimize'], explicit_checks=parsed['total_explicit_checks'])
                if mode == 'normal':
                    result['independent_counts_per_mode'] = parsed['counts']
                    result['independent_explicit_check_counts_per_mode'] = parsed['check_counts']
                else:
                    entry['same_case_and_check_counts_as_normal'] = (parsed['counts'] == result['independent_counts_per_mode']
                        and parsed['check_counts'] == result['independent_explicit_check_counts_per_mode'])
                    result['passed'] = result['passed'] and entry['same_case_and_check_counts_as_normal']
            elif stage == 'author_mutation' and run.returncode == 0:
                parsed = json.loads(run.stdout)
                entry.update(passed=parsed['passed'], counts=parsed['counts'],
                    baselines={p['name']: p['classification'] for p in parsed['baselines']},
                    mutations={p['name']: p['classification'] for p in parsed['mutations']},
                    harness_controls={p['name']: {'classification': p['classification'], 'reason': p['reason']}
                                      for p in parsed['harness_controls']})
            else:
                entry.update(stdout=run.stdout, stderr=run.stderr)
            result['stages'].append(entry)
            result['passed'] = result['passed'] and run.returncode == 0 and entry.get('passed', True)
            full_log.append(f'{mode}/{stage}: exit={run.returncode}; seconds={entry["seconds"]:.3f}; '
                            f'command={json.dumps(entry["command"])}')
    for name in (*FILES[:5], 'independent-review/independent_check.py', 'independent-review/run_audit.py'):
        tree = ast.parse((ROOT / name).read_text(encoding='utf-8'))
        if any(isinstance(node, ast.Assert) for node in ast.walk(tree)):
            raise RuntimeError('optimization-sensitive bare assert: ' + name)
    result['bare_assert_ast_check'] = 'passed for all seven Python files'
    # Independent regression of the exact previously crashing malformed report,
    # plus the deliberately documented non-adversarial reporting boundary.
    import mutation_check
    sentinel = 'test_model.HypothesisTests.test_filter_exact'
    spoof = {'tests': 1, 'failures': 1, 'errors': 0, 'skipped': 0,
             'expected_failures': 0, 'unexpected_successes': 0}
    probes = []
    for mode in ('normal', 'O', 'OO'):
        for name, payload, code, expected in (
            ('missing_fields_regression', '{}', 0, 'harness_failure'),
            ('report_forgery_outside_contract', json.dumps(spoof), 1, 'killed')):
            source = 'import sys\nprint(' + repr('SENTINEL_RESULT=' + payload) + ')\nsys.exit(' + str(code) + ')\n'
            probe = mutation_check.probe(source, sentinel, mode)
            probes.append({'mode': mode, 'name': name, 'expected_under_current_contract': expected,
                           'actual': probe['classification'], 'reason': probe['reason'],
                           'returncode': probe['returncode'], 'stdout': probe['stdout'], 'stderr': probe['stderr']})
            result['passed'] = result['passed'] and probe['classification'] == expected
    result['independent_harness_regression_and_boundary_probes'] = probes
    result['source_sha256_after'] = hashes()
    result['source_stable_during_run'] = result['source_sha256_before'] == result['source_sha256_after']
    result['passed'] = result['passed'] and result['source_stable_during_run']
    result['finished_utc'] = datetime.now(timezone.utc).isoformat()
    result['limits'] = ('Finite checks and current authored mutants only. Each authored mutant uses one designated sentinel. '
                        'Repeated interpreter modes are not additional distinct cases. General mathematical claims were reviewed separately.')
    (HERE / 'run-results.json').write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    (HERE / 'commands.log').write_text('\n'.join(full_log) + '\n', encoding='utf-8')
    print(json.dumps({'passed': result['passed'], 'stages': len(result['stages']),
                      'source_stable': result['source_stable_during_run']}, sort_keys=True))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
