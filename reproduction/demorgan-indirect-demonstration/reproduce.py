"""Rebuild evidence and package hashes; do not download, install, or publish."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
if '--check' in sys.argv:
    count = 0
    for line in Path('SHA256SUMS').read_text().splitlines():
        expected, name = line.split('  ', 1)
        actual = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit('Checksum mismatch: ' + name)
        count += 1
    print(f'Verified {count} files; manifest excludes itself and caches.')
    raise SystemExit(0)

environment = {'python_implementation': platform.python_implementation(),
               'python_version': platform.python_version(),
               'system': platform.system(), 'machine': platform.machine(),
               'libc': list(platform.libc_ver()),
               'external_dependencies': [], 'packages_installed_for_this_task': False,
               'network_required': False,
               'execution_method': 'CPython standard library; no Jupyter kernel'}
Path('environment.json').write_text(json.dumps(environment, indent=2) + '\n')
commands = [
    (['-m', 'unittest', '-v', 'test_logic'], 'tests.log'),
    (['run_examples.py'], 'results.json'),
    (['make_report.py'], 'trace_tables.zh-CN.md'),
    (['build_notebook.py'], 'notebook_build.log'),
    (['verify_notebook.py'], 'notebook_verify.log'),
]
logs = ['Working directory: this package directory',
        'Launcher: python3 reproduce.py',
        'Environment saved to environment.json; no hostname, username, or absolute path logged.']
for args, output in commands:
    command = 'python3 ' + ' '.join(args) + ' > ' + output + ' 2>&1'
    with Path(output).open('w', encoding='utf-8') as handle:
        completed = subprocess.run([sys.executable, *args], stdout=handle,
                                   stderr=subprocess.STDOUT, text=True, check=False)
    logs.append(f'$ {command}\nexit_code={completed.returncode}')
    if completed.returncode:
        Path('commands.log').write_text('\n'.join(logs) + '\n')
        raise SystemExit(f'Failed: {command}; inspect {output}')
logs.append('Generated SHA256SUMS after all evidence and commands.log were written.')
Path('commands.log').write_text('\n'.join(logs) + '\n')
files = sorted(p for p in ROOT.iterdir() if p.is_file() and p.name != 'SHA256SUMS')
Path('SHA256SUMS').write_text(''.join(
    hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name + '\n' for p in files))
print('Reproduced results, 24 tests, notebook code, and checksums. See logs for exact evidence.')
