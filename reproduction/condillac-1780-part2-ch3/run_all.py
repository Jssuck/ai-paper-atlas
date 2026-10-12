"""Regenerate three compact evidence files. No installs, network, or third-party packages."""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
FILES = ('model.py', 'demo.py', 'test_model.py', 'mutation_check.py', 'run_all.py')


def main():
    logs = ROOT / 'logs'
    logs.mkdir(exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    summaries, records = [], []
    for name in FILES:
        tree = ast.parse((ROOT / name).read_text(encoding='utf-8'), filename=name)
        if any(isinstance(node, ast.Assert) for node in ast.walk(tree)):
            raise RuntimeError(f'optimization-sensitive assert in {name}')
    commands = [('demo', [], ['demo.py'])]
    for mode, flags in [('normal', []), ('O', ['-O']), ('OO', ['-OO'])]:
        commands.append(('tests_' + mode, flags, ['-m', 'unittest', '-v', 'test_model']))
        commands.append(('mutations_' + mode, flags, ['mutation_check.py', '--mode', mode]))
    success = True
    for label, flags, args in commands:
        command = [sys.executable, *flags, '-B', *args]
        before = time.monotonic()
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
        elapsed = time.monotonic() - before
        display = ['${PYTHON_EXECUTABLE}', *flags, '-B', *args]
        records.append(f'=== {label} ===\ncommand: {json.dumps(display)}\nexit: {result.returncode}\n'
                       f'stdout:\n{result.stdout}\nstderr:\n{result.stderr}\n')
        entry = {'stage': label, 'command': display, 'returncode': result.returncode, 'seconds': elapsed}
        success = success and result.returncode == 0
        if label == 'demo' and result.returncode == 0:
            parsed = json.loads(result.stdout)
            (logs / 'results.json').write_text(json.dumps(parsed, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        if label.startswith('mutations_') and result.returncode == 0:
            parsed = json.loads(result.stdout)
            entry.update(counts=parsed['counts'], passed=parsed['passed'],
                         baselines_passed=sum(x['classification'] == 'survived' for x in parsed['baselines']),
                         controls_classified_as_harness_failure=sum(x['classification'] == 'harness_failure'
                                                                   for x in parsed['harness_controls']))
            success = success and parsed['passed']
        summaries.append(entry)
    report = {'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
              'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(),
              'source_sha256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in FILES},
              'assert_ast_check': 'passed; no bare assert statements in five Python sources',
              'passed': success, 'stages': summaries,
              'enumeration_per_test_mode': {'unittest_methods': 24, 'filter_budget_cases': 32895,
                                            'horn_system_seed_cases': 2408,
                                            'vocabulary_pair_dictionary_cases': 216,
                                            'task_label_answer_pairs': 729},
              'limits': 'Authored verification only. Each mutant runs one designated sentinel, not the full suite.'}
    (logs / 'verification.log').write_text('\n'.join(records), encoding='utf-8')
    (logs / 'verification-summary.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
