"""Real isolated fixture runs of verify.py's fail-closed orchestration gates."""
from hashlib import sha256
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
BASE = Path(__file__).resolve().parents[1]


def main():
    results = {}
    for scenario in ('pass', 'nonzero', 'nondeterminism', 'source_drift'):
        with tempfile.TemporaryDirectory(prefix='condillac-verifier-fixture-') as directory:
            root = Path(directory)
            shutil.copyfile(BASE / 'verify.py', root / 'verify.py')
            for name in ('README.md', 'MODEL.zh-CN.md', 'WALKTHROUGH.zh-CN.md'):
                (root / name).write_text('Isolated verifier fixture.\n', encoding='utf-8')
            for name in ('demo.py', 'mutation_check.py', 'walkthrough.py', 'independent_argument_checks.py'):
                (root / name).write_text("print('stable fixture output')\n", encoding='utf-8')
            (root / 'test_fixture.py').write_text(
                'import unittest\nclass Fixture(unittest.TestCase):\n    def test_success(self):\n        self.assertEqual(1, 1)\n', encoding='utf-8')
            if scenario == 'nonzero':
                (root / 'mutation_check.py').write_text('raise SystemExit(7)\n', encoding='utf-8')
            if scenario == 'nondeterminism':
                (root / 'demo.py').write_text('import sys\nprint(sys.flags.optimize)\n', encoding='utf-8')
            if scenario == 'source_drift':
                (root / 'mutation_check.py').write_text(
                    "from pathlib import Path\np = Path('README.md')\np.write_text(p.read_text() + 'changed\\n')\nprint('stable fixture output')\n", encoding='utf-8')
            p = subprocess.run([sys.executable, str(root / 'verify.py')], cwd=root, text=True, capture_output=True)
            summary = json.loads((root / 'evidence/summary.json').read_text(encoding='utf-8'))
            expected = 0 if scenario == 'pass' else 1
            if p.returncode != expected or summary['passed'] != (scenario == 'pass'):
                raise RuntimeError('incorrect fixture outcome: ' + scenario)
            if scenario == 'nonzero' and not any(r['exit_code'] == 7 for r in summary['commands']):
                raise RuntimeError('failed subprocess exit was not recorded')
            if scenario == 'nondeterminism' and summary['deterministic_stdout_across_modes']:
                raise RuntimeError('cross-mode mismatch went undetected')
            if scenario == 'source_drift' and summary['source_files_unchanged_during_run']:
                raise RuntimeError('source drift went undetected')
            results[scenario] = {'expected_verifier_exit': expected, 'actual_verifier_exit': p.returncode,
                                 'stdout': p.stdout, 'stderr': p.stderr,
                                 'subprocess_exit_codes': [r['exit_code'] for r in summary['commands']],
                                 'source_files_unchanged_during_run': summary['source_files_unchanged_during_run'],
                                 'deterministic_stdout_across_modes': summary['deterministic_stdout_across_modes'],
                                 'passed': summary['passed']}
    print(json.dumps({'status': 'PASS', 'verify_py_sha256': sha256((BASE / 'verify.py').read_bytes()).hexdigest(),
                      'fixtures': results, 'scope': 'four isolated fixtures, each executing fifteen real verifier subprocesses'},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
