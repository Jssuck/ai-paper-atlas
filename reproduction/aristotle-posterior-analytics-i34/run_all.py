"""Record real subprocess output; use this directory as working directory."""
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def main():
    logs = ROOT / 'logs'
    logs.mkdir(exist_ok=True)
    commands = [
        ('demo.log', ['model.py']),
        ('tests.log', ['-m', 'unittest', '-v', 'test_model']),
        ('tests-optimized.log', ['-O', '-m', 'unittest', '-v', 'test_model']),
        ('tests-double-optimized.log', ['-OO', '-m', 'unittest', '-v', 'test_model']),
        ('notebook.log', ['run_notebook.py']),
    ]
    environment = {'python': platform.python_version(), 'implementation': platform.python_implementation(),
                   'system': platform.system(), 'dependencies': 'Python standard library only',
                   'notebook_runner': 'stdlib exec; no Jupyter kernel'}
    (ROOT / 'environment.json').write_text(json.dumps(environment, indent=2) + '\n')
    for filename, args in commands:
        result = subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)
        output = '$ python ' + ' '.join(args) + '\n' + result.stdout + result.stderr + f'\nexit_code={result.returncode}\n'
        (logs / filename).write_text(output, encoding='utf-8')
        print(filename, 'exit_code=' + str(result.returncode))
        if result.returncode:
            raise SystemExit(result.returncode)
    # Do not include this manifest itself (avoids recursive hashes).
    files = ['README.md', 'model.py', 'test_model.py', 'run_notebook.py', 'run_all.py', 'tutorial.ipynb', 'environment.json']
    files += ['logs/' + name for name, _ in commands]
    manifest = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in files}
    (ROOT / 'sha256.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')

if __name__ == '__main__':
    main()
