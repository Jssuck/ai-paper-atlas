"""Rerun the independent review with public-safe, actual execution logs."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'independent-review'


def main():
    environment = {
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'python': sys.version,
        'platform': platform.platform(),
        'working_directory': '. (package root)',
        'dependencies': 'Python standard library only',
        'installation_performed': False,
        'network_used_for_checks': False,
        'log_path_policy': 'Commands use python and package-relative paths; private absolute paths are removed.',
        'commands': [],
    }
    commands = [
        ['-m', 'unittest', 'discover', '-s', 'tests', '-v'],
        ['independent-review/audit_checks.py'],
        ['walkthrough.py'],
    ]
    lines = ['独立复核实跑日志', '所有命令从复现包根目录执行。',
             '开始 UTC: ' + environment['started_utc'], 'Python: ' + sys.version,
             'Platform: ' + platform.platform()]
    for arguments in commands:
        start = time.perf_counter()
        process = subprocess.run([sys.executable, *arguments], cwd=ROOT, encoding='utf-8',
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        seconds = time.perf_counter() - start
        command = ['python', *arguments]
        result = {'command': command, 'exit_code': process.returncode,
                  'elapsed_seconds': round(seconds, 6)}
        environment['commands'].append(result)
        output = process.stdout.replace(str(ROOT), '.')
        lines.extend(['', '$ ' + ' '.join(command), output,
                      f'Exit code: {process.returncode}; elapsed: {seconds:.6f} s'])
        print(output, end='')
        if process.returncode:
            break
    environment['finished_utc'] = datetime.now(timezone.utc).isoformat()
    environment['all_passed'] = (len(environment['commands']) == len(commands)
                                  and all(x['exit_code'] == 0 for x in environment['commands']))
    # Fingerprint stable code and source fixtures. Runtime logs/manifests are
    # intentionally omitted because the package runner refreshes them later.
    selected = ['gergonne.py', 'reproduce.py', 'walkthrough.py', 'run_checks.py',
                'source_tables.json', 'README.md', 'PROOF.md', 'tests/test_gergonne.py',
                'independent-review/audit_checks.py', 'independent-review/run_review.py',
                'independent-review/review.zh-CN.md']
    environment['reviewed_sha256'] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in selected
    }
    lines.extend(['', 'All passed: ' + str(environment['all_passed'])])
    (OUT / 'review.log').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    (OUT / 'environment.json').write_text(json.dumps(environment, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return 0 if environment['all_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
