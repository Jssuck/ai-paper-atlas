"""Execute actual three-mode subprocesses and bind files, no assert statements."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    os.chdir(ROOT)
    logs = ROOT / 'logs'
    logs.mkdir(exist_ok=True)
    executions = []
    example_outputs = []
    for label, flags in [('normal', []), ('O', ['-O']), ('OO', ['-OO'])]:
        for script in ('test_model.py', 'examples.py', 'independent_audit.py'):
            command = [sys.executable, *flags, script]
            run = subprocess.run(command, capture_output=True, cwd=ROOT, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
            stem = f'{label}-{Path(script).stem}'
            (logs / f'{stem}.stdout.txt').write_bytes(run.stdout)
            (logs / f'{stem}.stderr.txt').write_bytes(run.stderr)
            executions.append({'mode': label, 'argv': command, 'exit_code': run.returncode})
            if run.returncode:
                raise RuntimeError(f'{stem} failed; see logs')
            if script == 'examples.py':
                example_outputs.append(run.stdout)
    if any(output != example_outputs[0] for output in example_outputs):
        raise RuntimeError('example outputs differ across optimization modes')
    results = ROOT / 'results.json'
    if results.exists() and results.read_bytes() != example_outputs[0]:
        raise RuntimeError('saved results do not match current examples')
    results.write_bytes(example_outputs[0])
    environment = {'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(), 'dependencies': 'Python standard library only', 'example_outputs_identical': True, 'executions': executions}
    (ROOT / 'environment.json').write_text(json.dumps(environment, indent=2) + '\n')
    paths = sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name != 'MANIFEST.sha256')
    manifest = ''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}\n' for p in paths)
    (ROOT / 'MANIFEST.sha256').write_text(manifest)
    print('PASS: 9 author tests and independent audit in each of normal/-O/-OO; example outputs byte-identical.')
    print(f'Bound {len(paths)} files in MANIFEST.sha256.')


if __name__ == '__main__':
    main()
