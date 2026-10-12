"""Preserve real command outputs from an independent three-mode review matrix."""
from hashlib import sha256
from pathlib import Path
import json
import os
import subprocess
import sys
BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'independent-review'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def sources():
    return {str(p.relative_to(BASE)): digest(p) for p in sorted(BASE.rglob('*'))
            if p.is_file() and p.suffix in ('.py', '.md') and '__pycache__' not in p.parts
            and p.name != 'review.zh-CN.md'}


def main():
    commands = [('unit', ['-m', 'unittest', '-v']), ('demo', ['demo.py']),
                ('tutorial', ['walkthrough.py']), ('mutation', ['mutation_check.py']),
                ('mutation-sanity', ['independent-review/check_mutation_harness.py']),
                ('verifier-sanity', ['independent-review/check_verifier.py']),
                ('oracle', ['independent-review/audit_code.py'])]
    before = sources()
    records, canonical = [], {}
    equal = True
    for mode, flags in (('normal', []), ('O', ['-O']), ('OO', ['-OO'])):
        for label, arguments in commands:
            display = ['python'] + flags + arguments
            p = subprocess.run([sys.executable] + flags + arguments, cwd=BASE,
                               env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), text=True, capture_output=True)
            name = mode + '-' + label
            log = '$ ' + ' '.join(display) + '\nexit_code: ' + str(p.returncode) + '\n\nSTDOUT\n' + p.stdout + '\nSTDERR\n' + p.stderr
            (OUT / (name + '.log')).write_text(log, encoding='utf-8')
            if label in ('demo', 'mutation', 'mutation-sanity', 'verifier-sanity', 'oracle') and p.returncode == 0:
                value = json.loads(p.stdout)
                (OUT / (name + '.json')).write_text(p.stdout, encoding='utf-8')
                if label == 'oracle':
                    value = dict(value); value.pop('optimization', None)
                if label in canonical:
                    equal = equal and canonical[label] == value
                else:
                    canonical[label] = value
            if label == 'tutorial' and p.returncode == 0:
                if label in canonical:
                    equal = equal and canonical[label] == p.stdout
                else:
                    canonical[label] = p.stdout
            records.append({'command': display, 'exit_code': p.returncode,
                            'log': 'independent-review/' + name + '.log'})
            print(name + ': ' + str(p.returncode), flush=True)
    after = sources()
    status = 'PASS' if before == after and equal and all(r['exit_code'] == 0 for r in records) else 'FAIL'
    result = {'status': status, 'source_unchanged_during_run': before == after,
              'equal_semantic_outputs_across_modes': equal, 'source_sha256': after, 'commands': records,
              'scope': 'fresh local runs after storage recovery; bounded checks are not a general proof'}
    (OUT / 'matrix-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    raise SystemExit(0 if status == 'PASS' else 1)


if __name__ == '__main__': main()
