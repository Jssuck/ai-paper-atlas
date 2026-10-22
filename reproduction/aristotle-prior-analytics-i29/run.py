"""Re-run all evidence using only Python standard library. Run from this directory."""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from datetime import datetime, timezone

root = Path(__file__).resolve().parent
(root / 'logs').mkdir(exist_ok=True)
records = []
for flag, suffix in [([], 'normal'), (['-O'], 'O'), (['-OO'], 'OO')]:
    args = [*flag, '-m', 'unittest', '-v', 'test_model']
    result = subprocess.run([sys.executable, *args], cwd=root, capture_output=True, text=True)
    (root / 'logs' / ('tests-' + suffix + '.txt')).write_text(result.stdout + result.stderr, encoding='utf-8')
    records.append({'command': 'python3 ' + ' '.join(args), 'exit_code': result.returncode})
result = subprocess.run([sys.executable, 'model.py'], cwd=root, capture_output=True, text=True)
(root / 'results.json').write_text(result.stdout, encoding='utf-8')
(root / 'logs' / 'model-stderr.txt').write_text(result.stderr, encoding='utf-8')
records.append({'command': 'python3 model.py', 'exit_code': result.returncode})
env = {'utc': datetime.now(timezone.utc).isoformat(), 'python': sys.version,
       'implementation': platform.python_implementation(), 'system': platform.system(),
       'machine_architecture': platform.machine(), 'third_party_dependencies': [], 'commands': records}
(root / 'logs' / 'environment.json').write_text(json.dumps(env, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
manifest = {}
for p in sorted(root.rglob('*')):
    if p.is_file() and '__pycache__' not in p.parts and p.name != 'manifest.sha256.json':
        manifest[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
(root / 'manifest.sha256.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
if any(x['exit_code'] for x in records):
    raise SystemExit('one or more commands failed; evidence retained')
print('PASS: 3 modes, 21 tests per mode; model report and SHA256 manifest saved')
