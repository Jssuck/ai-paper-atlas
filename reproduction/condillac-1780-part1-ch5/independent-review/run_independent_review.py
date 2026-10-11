#!/usr/bin/env python3
"""Reproduce the independent audit using isolated source snapshots.

Writes only independent-review/logs. Does not edit author source or author logs.
The review's finite limits are evidence, not a proof for arbitrary models.
"""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LOGS = HERE / 'logs'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
MODES = (('normal', []), ('O', ['-O']), ('OO', ['-OO']))
MUTANTS = (
    ('ambiguous_as_identified', 'finite_model.py', 'status = "identified" if len(values) == 1 else "ambiguous"', 'status = "identified" if len(values) >= 1 else "ambiguous"'),
    ('empty_fiber_as_identified', 'finite_model.py', 'return Answer("inconsistent", (), ())', 'return Answer("identified", (), ())'),
    ('labels_leak_state_index', 'finite_model.py', 'return FiniteModel(self.columns, self.states, self.signatures,\n                           tuple(labels[state] for state in self.states))', 'return FiniteModel(self.columns, self.states,\n                           tuple(tuple(i for _ in self.columns) for i in range(len(self.states))),\n                           tuple(labels[state] for state in self.states))'),
    ('new_data_erase_old', 'finite_model.py', 'rows = tuple(row + (values[state],)', 'rows = tuple((0,) * len(row) + (values[state],)'),
    ('assumption_ignored', 'finite_model.py', 'selected = [i for i, state in enumerate(self.states) if state in allowed]', 'selected = list(range(len(self.states)))'),
    ('refinement_always_true', 'finite_model.py', 'return all(len({old[state] for state in fiber}) == 1\n                   for fiber in self.fibers())', 'return True'),
    ('global_any_fiber_suffices', 'finite_model.py', 'return all(self.answer(row, query).status == "identified"', 'return any(self.answer(row, query).status == "identified"'),
    ('gain_silently_one', 'ratios.py', 'return result.product / gain', 'return result.product'),
    ('scale_wrong_direction', 'ratios.py', 'return coefficient * scale, gain / scale', 'return coefficient * scale, gain * scale'),
    ('zero_only_identifies', 'ratios.py', 'return ProductInference("uninformative", None)', 'return ProductInference("identified", Fraction(0))'),
    ('conflicting_ratios_ignored', 'ratios.py', 'if len(ratios) != 1 or next(iter(ratios)) <= 0:', 'if next(iter(ratios)) <= 0:'),
    ('relative_ratio_inverted', 'ratios.py', 'return a.product / b.product', 'return b.product / a.product'),
    ('zero_input_conflict_ignored', 'ratios.py', 'if y != 0:', 'if False:'),
    ('bool_accepted_as_exact', 'ratios.py', 'if type(value) is int or isinstance(value, Fraction):', 'if isinstance(value, (int, Fraction)):')
)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def normalize(text):
    # Presentation-only replacement of this known execution prefix.
    return text.replace(str(ROOT), '.')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command, cwd, output, expected=0, section=None):
    start = time.perf_counter()
    proc = subprocess.run(command, cwd=cwd, env=ENV, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    if section is None:
        (LOGS / output).write_text(normalize(proc.stdout), encoding='utf-8')
    else:
        with (LOGS / output).open('a', encoding='utf-8') as stream:
            stream.write('\n===== ' + section + ' =====\n' + normalize(proc.stdout))
    record = {'command': command, 'working_directory': str(cwd), 'exit_code': proc.returncode, 'expected_exit_code': expected, 'elapsed_seconds': round(time.perf_counter() - start, 6), 'log': output, 'section': section}
    require(proc.returncode == expected, f'Unexpected exit code: {record}')
    return proc, record


def copy_snapshot(destination):
    for p in ROOT.glob('*.py'):
        shutil.copy2(p, destination / p.name)
    for p in ROOT.glob('*.md'):
        shutil.copy2(p, destination / p.name)
    shutil.copytree(ROOT / 'tests', destination / 'tests', ignore=shutil.ignore_patterns('__pycache__'))


def main():
    LOGS.mkdir(exist_ok=True)
    (LOGS / 'mutations.log').write_text('', encoding='utf-8')
    sources = sorted([*ROOT.glob('*.py'), *ROOT.glob('*.md'), *(ROOT / 'tests').glob('*.py')])
    before = {str(p.relative_to(ROOT)): digest(p) for p in sources}
    summary = {'started_utc': datetime.now(timezone.utc).isoformat(), 'python': sys.version, 'platform': platform.platform(), 'source_sha256': before, 'reviewer_sha256': {p.name: digest(p) for p in HERE.glob('*.py')}, 'stages': [], 'mutations': [], 'limits': {'max_states': 4, 'observation_columns': 2, 'observation_values': [0, 1], 'query_values': [0, 1, 2], 'extension_values': [0, 1, 2], 'rational_parameter_values': 'distinct a/b, 1<=a,b<=4', 'rational_inputs': 'distinct a/b, -4<=a<=4, 1<=b<=4'}}
    with tempfile.TemporaryDirectory(prefix='review-source-', dir=HERE) as source_folder:
        snapshot = Path(source_folder)
        copy_snapshot(snapshot)
        proc, rec = run([sys.executable, 'verify.py'], snapshot, 'author-verify-normal.txt')
        summary['stages'].append(rec)
        dest = LOGS / 'author-rerun-generated'
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(snapshot / 'logs', dest)
        for log in dest.rglob('*'):
            if log.is_file():
                log.write_text(normalize(log.read_text(encoding='utf-8')), encoding='utf-8')
        author_result = json.loads((dest / 'verification.json').read_text())
        require(author_result['source_sha256'] == before, 'author snapshot hashes do not match reviewed inputs')
        require(author_result['result'] == 'PASS', 'author verifier did not pass')
        for mode, flags in MODES:
            proc, rec = run([sys.executable, *flags, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], snapshot, f'author-tests-{mode}.txt')
            require('Ran 23 tests' in proc.stdout and 'OK' in proc.stdout, 'author unit test count mismatch')
            summary['stages'].append(rec)
            proc, rec = run([sys.executable, *flags, str(HERE / 'reviewer_check.py'), '--target', str(snapshot)], snapshot, f'reviewer-{mode}.txt')
            require('Ran 35 tests' in proc.stdout and '"result": "PASS"' in proc.stdout, 'independent verification did not pass')
            summary['stages'].append(rec)
            if flags:
                for entry in ('finite_oracle.py', 'verify.py'):
                    proc, rec = run([sys.executable, *flags, entry], snapshot, f'author-{entry[:-3]}-refusal-{mode}.txt', expected=1)
                    require('RuntimeError:' in proc.stdout and ('-O' in proc.stdout or '-OO' in proc.stdout), 'missing explicit optimization refusal')
                    require('"result": "PASS"' not in proc.stdout, 'optimized refusal falsely reports PASS')
                    summary['stages'].append(rec)
        for name, filename, old, new in MUTANTS:
            with tempfile.TemporaryDirectory(prefix='review-mutant-', dir=HERE) as mutant_folder:
                mutant = Path(mutant_folder)
                for f in ('finite_model.py', 'ratios.py'):
                    shutil.copy2(snapshot / f, mutant / f)
                p = mutant / filename
                code = p.read_text(encoding='utf-8')
                require(code.count(old) == 1, 'mutation anchor not unique: ' + name)
                changed = code.replace(old, new)
                compile(changed, filename, 'exec')
                p.write_text(changed, encoding='utf-8')
                for mode, flags in MODES:
                    proc, rec = run([sys.executable, *flags, str(HERE / 'reviewer_check.py'), '--target', str(mutant), '--unit-only'], mutant, 'mutations.log', expected=1, section=f'{name} / {mode}')
                    failures = len(re.findall(r'^FAIL:', proc.stdout, re.MULTILINE))
                    errors = len(re.findall(r'^ERROR:', proc.stdout, re.MULTILINE))
                    killed = failures > 0 and errors == 0 and 'Ran 35 tests' in proc.stdout
                    require(killed, f'mutant not killed by completed assertion-only failures: {name} {mode}')
                    summary['mutations'].append({'name': name, 'mode': mode, 'assertion_failures': failures, 'errors': errors, 'result': 'KILLED', **rec})
    after = {str(p.relative_to(ROOT)): digest(p) for p in sources}
    require(before == after, 'author source changed during independent run')
    summary.update({'finished_utc': datetime.now(timezone.utc).isoformat(), 'author_sources_unchanged': True, 'mutation_runs': len(summary['mutations']), 'unique_mutants': len(MUTANTS), 'result': 'PASS'})
    (LOGS / 'independent-summary.json').write_text(normalize(json.dumps(summary, indent=2, ensure_ascii=False)) + '\n', encoding='utf-8')
    print(json.dumps({'result': 'PASS', 'stages': len(summary['stages']), 'unique_mutants': len(MUTANTS), 'mutation_runs': len(summary['mutations']), 'author_sources_unchanged': True}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
