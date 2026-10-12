"""Ten hand-selected behavioral mutants; failures of the harness are not kills."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
RUNNER = r'''
import json, sys, unittest
suite = unittest.defaultTestLoader.loadTestsFromName(sys.argv[1])
result = unittest.TextTestRunner(verbosity=2).run(suite)
report = {'tests': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
          'skipped': len(result.skipped), 'expected_failures': len(result.expectedFailures),
          'unexpected_successes': len(result.unexpectedSuccesses)}
print('SENTINEL_RESULT=' + json.dumps(report, sort_keys=True), flush=True)
sys.exit(0 if result.wasSuccessful() else 1)
'''
MUTANTS = (
    ('exclude_exact_match', '!= y for x, y in data) <= max_errors)', '!= y for x, y in data) < max_errors)',
     'test_model.HypothesisTests.test_filter_exact'),
    ('ignore_noise_budget', '!= y for x, y in data) <= max_errors)', '!= y for x, y in data) <= 0)',
     'test_model.HypothesisTests.test_noise_budget'),
    ('claim_identifiability', 'return len(signatures) == len(self.rows)', 'return True',
     'test_model.HypothesisTests.test_detect_not_identify'),
    ('any_premise_suffices', 'if rule.premises <= known and rule.conclusion not in known:',
     'if bool(rule.premises & known) and rule.conclusion not in known:', 'test_model.HornTests.test_conjunction'),
    ('stop_after_one_pass', 'if not changed:', 'if True:', 'test_model.HornTests.test_chain_and_idempotence'),
    ('add_unreachable_atoms', 'return ClosureResult(initial, tuple(steps), frozenset(known))',
     'return ClosureResult(initial, tuple(steps), frozenset(self.atoms))', 'test_model.HornTests.test_unreachable'),
    ('ignore_provenance_fields', 'if step.premises != tuple(sorted(rule.premises)) or step.conclusion != rule.conclusion:',
     'if False:', 'test_model.HornTests.test_forged_trace'),
    ('accept_wrong_meaning', 'return all(target_meaning[mapping[word]] == meaning for meaning, word in source.entries)',
     'return True', 'test_model.TranslationTests.test_wrong_dictionary'),
    ('allow_noninjective_inverse', 'if len(set(mapping.values())) != len(mapping):',
     'if False:', 'test_model.TranslationTests.test_dictionary_inverse_validation'),
    ('equate_breadth_precision', 'if label in answers and answers[label] != answer:',
     'if False:', 'test_model.PrecisionTests.test_breadth_is_not_precision'),
)


def probe(source, sentinel, mode, timeout=10):
    with tempfile.TemporaryDirectory(prefix='condillac-ii3-mutation-') as folder:
        directory = Path(folder)
        (directory / 'model.py').write_text(source, encoding='utf-8')
        (directory / 'test_model.py').write_text((ROOT / 'test_model.py').read_text(encoding='utf-8'), encoding='utf-8')
        flags = [] if mode == 'normal' else ['-' + mode]
        command = [sys.executable, *flags, '-B', '-c', RUNNER, sentinel]
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        record = {'command': ['${PYTHON_EXECUTABLE}', *flags, '-B', '-c', '${SENTINEL_RUNNER}', sentinel]}
        try:
            process = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=timeout, env=env)
            stdout, stderr = process.stdout, process.stderr
            record.update(returncode=process.returncode, stdout=stdout.replace(folder, '${MUTATION_DIR}'),
                          stderr=stderr.replace(folder, '${MUTATION_DIR}'))
        except subprocess.TimeoutExpired as exc:
            def decoded(value):
                return value.decode('utf-8', errors='replace') if isinstance(value, bytes) else value or ''
            record.update(classification='harness_failure', reason='timeout', returncode=None,
                          stdout=decoded(exc.stdout).replace(folder, '${MUTATION_DIR}'),
                          stderr=decoded(exc.stderr).replace(folder, '${MUTATION_DIR}'))
            return record
        markers = [line.removeprefix('SENTINEL_RESULT=') for line in stdout.splitlines()
                   if line.startswith('SENTINEL_RESULT=')]
        if len(markers) != 1:
            record.update(classification='harness_failure', reason='missing_or_duplicate_terminal_report')
            return record
        try:
            report = json.loads(markers[0])
        except (TypeError, ValueError):
            record.update(classification='harness_failure', reason='malformed_terminal_report')
            return record
        record['terminal_report'] = report
        fields = {'tests', 'failures', 'errors', 'skipped', 'expected_failures', 'unexpected_successes'}
        if (not isinstance(report, dict) or set(report) != fields
                or any(type(report[field]) is not int or report[field] < 0 for field in fields)
                or sum(report[field] for field in fields - {'tests'}) > report['tests']):
            record.update(classification='harness_failure', reason='invalid_terminal_report_schema_or_counts')
            return record
        if (report['tests'] != 1 or report['errors'] or report['skipped'] or report['expected_failures']
                or report['unexpected_successes']):
            record.update(classification='harness_failure', reason='test_error_or_incomplete_execution')
        elif report['failures'] == 1 and process.returncode == 1:
            record.update(classification='killed', reason='completed_sentinel_assertion_failure')
        elif report['failures'] == 0 and process.returncode == 0:
            record.update(classification='survived', reason='completed_sentinel_pass')
        else:
            record.update(classification='harness_failure', reason='inconsistent_report_and_exit')
        return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=('normal', 'O', 'OO'), default='normal')
    args = parser.parse_args()
    original = (ROOT / 'model.py').read_text(encoding='utf-8')
    baselines, mutations = [], []
    for name, old, new, sentinel in MUTANTS:
        if original.count(old) != 1:
            raise RuntimeError(f'mutation anchor must occur exactly once: {name}')
        baselines.append(dict(name=name, **probe(original, sentinel, args.mode)))
        mutations.append(dict(name=name, **probe(original.replace(old, new), sentinel, args.mode)))
    sentinel = 'test_model.HypothesisTests.test_filter_exact'
    def report_and_exit(payload):
        return 'import sys\nprint(' + repr('SENTINEL_RESULT=' + payload) + ')\nsys.exit(0)\n'
    valid_report = {'tests': 1, 'failures': 0, 'errors': 0, 'skipped': 0,
                    'expected_failures': 0, 'unexpected_successes': 0}
    controls = [
        ('syntax_error', 'not valid Python !!!\n', 10),
        ('import_error', 'import surely_absent_condillac_module\n', 10),
        ('early_exit', 'import sys; sys.exit(0)\n', 10),
        ('timeout', 'import time; time.sleep(10)\n', 0.2),
        ('test_runtime_error', original.replace('data = self.observations(observations)',
                                              'raise RuntimeError("injected test error")'), 10),
        ('malformed_json', report_and_exit('{'), 10),
        ('schema_missing_fields', report_and_exit('{}'), 10),
        ('schema_non_object', report_and_exit('[]'), 10),
        ('schema_boolean_count', report_and_exit(json.dumps(dict(valid_report, tests=True))), 10),
        ('schema_negative_count', report_and_exit(json.dumps(dict(valid_report, failures=-1))), 10),
        ('schema_outcome_total', report_and_exit(json.dumps(dict(valid_report, failures=1, errors=1))), 10)]
    control_results = [dict(name=name, **probe(source, sentinel, args.mode, limit))
                       for name, source, limit in controls]
    passed = (all(r['classification'] == 'survived' for r in baselines)
              and all(r['classification'] == 'killed' for r in mutations)
              and all(r['classification'] == 'harness_failure' for r in control_results))
    output = {'mode': args.mode, 'passed': passed, 'baselines': baselines, 'mutations': mutations,
              'harness_controls': control_results,
              'counts': {key: sum(r['classification'] == key for r in mutations)
                         for key in ('killed', 'survived', 'harness_failure')}}
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
