"""Capture real reviewer executions without recording host paths or secrets."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
COMMANDS = (
    ('unit-tests.txt', ['-m', 'unittest', 'discover', '-v']),
    ('math-audit.txt', ['evidence/independent-review/independent_review.py']),
    ('notebook-replay.txt', ['evidence/independent-review/replay_notebook.py']),
    ('notebook-structure.txt', ['validate_notebook.py']),
)


def main():
    runs = []
    for filename, args in COMMANDS:
        start = time.perf_counter()
        p = subprocess.run([sys.executable, *args], cwd=ROOT, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        seconds = round(time.perf_counter() - start, 6)
        output = p.stdout.replace(str(ROOT), '<project>')
        command = 'python ' + ' '.join(args)
        (OUT / filename).write_text('$ ' + command + '\n' + output +
            '\n[exit code: ' + str(p.returncode) + '; wall seconds: ' + str(seconds) + ']\n', encoding='utf-8')
        runs.append({'command': command, 'exit_code': p.returncode,
                     'wall_seconds': seconds, 'log': filename})
        print(command, '->', p.returncode)
        if p.returncode:
            print(output)
            raise SystemExit(p.returncode)
    inputs = ['demorgan.py', 'tests/test_demorgan.py', 'demo.py', 'tutorial.ipynb',
              'execute_notebook.py', 'validate_notebook.py', 'run_checks.py', 'README.md', 'SOURCE_LEDGER.md',
              'evidence/independent-review/independent_review.py',
              'evidence/independent-review/replay_notebook.py',
              'evidence/independent-review/capture_review.py',
              'evidence/independent-review/review.zh-CN.md']
    record = {'status': 'PASS', 'executor_clock_utc': datetime.now(timezone.utc).isoformat(),
              'python': platform.python_version(), 'implementation': platform.python_implementation(),
              'os': platform.system(), 'network_used': False, 'installation_performed': False,
              'jupyter_kernel_executed': False, 'runs': runs,
              'reviewed_sha256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                                  for name in inputs},
              'privacy': 'No usernames, hostnames, absolute paths, environment variables or credentials recorded.'}
    (OUT / 'review-execution.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Sanitized actual review logs and reviewed-file hashes saved.')


if __name__ == '__main__':
    main()
