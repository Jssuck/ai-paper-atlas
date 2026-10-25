"""Recreate logs, environment metadata and SHA-256 file manifest with stdlib."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys

root = Path(__file__).resolve().parent
(root / 'logs').mkdir(exist_ok=True)
commands = [([], 'test_model.py', 'tests.log'),
            (['-O'], 'test_model.py', 'tests-optimized.log'),
            (['-OO'], 'test_model.py', 'tests-double-optimized.log'),
            ([], 'model.py', 'demo.log'), ([], 'run_notebook.py', 'notebook.log')]
for flags, script, name in commands:
    command = [sys.executable, *flags, script]
    result = subprocess.run(command, cwd=root, capture_output=True, text=True)
    log = ('UTC: ' + datetime.now(timezone.utc).isoformat() + '\n'
           + 'Command: python ' + ' '.join([*flags, script]) + '\n'
           + result.stdout + result.stderr + f'\nExit status: {result.returncode}\n')
    (root / 'logs' / name).write_text(log, encoding='utf-8')
    print(name, 'exit', result.returncode)
    if result.returncode:
        raise SystemExit(result.returncode)
environment = dict(python_version=platform.python_version(), implementation=platform.python_implementation(),
                   os=platform.system(), machine=platform.machine(), dependencies='Python standard library only',
                   notebook_execution='sequential CPython exec; not a Jupyter kernel',
                   optional_packages={p:bool(importlib.util.find_spec(p)) for p in ('nbformat','nbclient','ipykernel')})
(root / 'environment.json').write_text(json.dumps(environment, indent=2) + '\n', encoding='utf-8')
manifest = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()
            and '__pycache__' not in p.parts and p.name != 'sha256.json'}
(root / 'sha256.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print('Manifest files:', len(manifest))
