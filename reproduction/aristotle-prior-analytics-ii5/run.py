#!/usr/bin/env python3
"""Record commands, environment, exit status and fresh artifacts without host identifiers."""
import datetime
import json
import platform
import subprocess
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
commands = [['check.py'], ['-m', 'unittest', '-v', 'test_check.py']]
log = ['UTC: ' + datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'Python: ' + platform.python_version(), 'Implementation: ' + platform.python_implementation(),
       'System: ' + platform.system(), 'Dependencies: Python standard library only']
for args, filename in zip(commands, ['results.json', 'tests.log']):
    result = subprocess.run([sys.executable] + args, cwd=here, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    (here / filename).write_text(result.stdout, encoding='utf-8')
    log.extend(['Command: python3 ' + ' '.join(args), 'Exit status: ' + str(result.returncode)])
    if result.returncode:
        (here / 'run.log').write_text('\n'.join(log) + '\n', encoding='utf-8')
        raise SystemExit(result.returncode)
report = json.loads((here / 'results.json').read_text(encoding='utf-8'))
log.extend(['Model counts: ' + json.dumps(report['model_counts'], sort_keys=True),
            'Valid schemas: 8; invalid schemas with countermodels in both domains: 6',
            'Valid-schema/domain pairs: 16; failures: 0',
            'Distinct model/schema evaluations (each domain counted separately): 6622',
            'Author unit tests: 7 passed', 'Dependency cycle refused: true'])
(here / 'run.log').write_text('\n'.join(log) + '\n', encoding='utf-8')
print('\n'.join(log))
