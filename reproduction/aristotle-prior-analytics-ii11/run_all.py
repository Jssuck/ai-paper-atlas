"""Run all three Python modes and save their actual outputs; stop on any failure."""
import hashlib
import platform
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'evidence'

def main():
    EVIDENCE.mkdir(exist_ok=True)
    environment = '\n'.join([
        'UTC ' + datetime.now(timezone.utc).isoformat(),
        'Python ' + platform.python_version(),
        platform.system() + ' ' + platform.release() + ' ' + platform.machine(),
        'Dependencies: Python standard library only',
    ]) + '\n'
    (EVIDENCE / 'environment.txt').write_text(environment, encoding='utf-8')
    outputs = []
    for name, flags in [('normal', []), ('optimized', ['-O']), ('double-optimized', ['-OO'])]:
        test_args = flags + ['-m', 'unittest', '-v', 'test_reproduce.py']
        completed = subprocess.run([sys.executable] + test_args, cwd=ROOT, capture_output=True, text=True)
        log = 'python ' + ' '.join(test_args) + '\n' + completed.stdout + completed.stderr
        log += f'\nexit_code={completed.returncode}\n'
        (EVIDENCE / f'tests-{name}.log').write_text(log, encoding='utf-8')
        if completed.returncode:
            raise SystemExit(completed.returncode)
        args = flags + ['reproduce.py']
        completed = subprocess.run([sys.executable] + args, cwd=ROOT, capture_output=True)
        (EVIDENCE / f'results-{name}.json').write_bytes(completed.stdout)
        log = 'python ' + ' '.join(args) + f' > evidence/results-{name}.json\n'
        log += completed.stderr.decode('utf-8', errors='replace')
        log += f'exit_code={completed.returncode}\n'
        (EVIDENCE / f'run-{name}.log').write_text(log, encoding='utf-8')
        if completed.returncode:
            raise SystemExit(completed.returncode)
        outputs.append(completed.stdout)
    if not all(data == outputs[0] for data in outputs):
        raise SystemExit('Results differ across optimization modes')
    # This manifest deliberately covers production files only, not later reviewer artifacts.
    files = [ROOT / name for name in ['README.md', 'reproduce.py', 'test_reproduce.py', 'run_all.py']]
    files += sorted(p for p in EVIDENCE.iterdir() if p.is_file())
    manifest = ''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.relative_to(ROOT).as_posix() + '\n' for p in files)
    (ROOT / 'SHA256SUMS').write_text(manifest, encoding='utf-8')
    print('Three modes: 12 tests each passed; three result files byte-identical.')
    print('Result SHA-256:', hashlib.sha256(outputs[0]).hexdigest())

if __name__ == '__main__': main()
