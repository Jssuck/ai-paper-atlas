"""Run actual subprocesses, save evidence, then hash public files."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

root = Path(__file__).resolve().parent
(root / 'logs').mkdir(exist_ok=True)
env = {'python': platform.python_version(), 'implementation': platform.python_implementation(),
       'platform': platform.system(), 'dependencies': 'Python standard library only',
       'notebook_executor': 'CPython exec, not Jupyter kernel',
       'started_at_utc': datetime.now(timezone.utc).isoformat()}
(root / 'environment.json').write_text(json.dumps(env, indent=2) + '\n')
commands = [('demo.log', ['model.py']), ('tests.log', ['-m', 'unittest', '-v', 'test_model']),
            ('tests-optimized.log', ['-O', '-m', 'unittest', '-v', 'test_model']),
            ('tests-double-optimized.log', ['-OO', '-m', 'unittest', '-v', 'test_model']),
            ('notebook.log', ['run_notebook.py'])]
for name, args in commands:
    p = subprocess.run([sys.executable] + args, cwd=root, text=True, capture_output=True)
    text = '$ python ' + ' '.join(args) + '\n' + p.stdout + p.stderr + f'\nexit_code={p.returncode}\n'
    (root / 'logs' / name).write_text(text)
    print(text, end='')
    if p.returncode:
        raise SystemExit(p.returncode)
files = sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name != 'sha256.json')
manifest = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(root / 'sha256.json').write_text(json.dumps(manifest, indent=2) + '\n')
