"""Check recorded normal/-O/-OO results and write a compact audit summary."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent


def payload(text, task):
    if task == 'independent':
        match = re.search(r'(\{\n  "counts".*?\n\})\n\nexit_code=0', text, re.S)
    elif task == 'demo':
        match = re.search(r'python(?: -O{1,2})? demo\.py\n(\{.*?\n\})\n\nexit_code=0', text, re.S)
    else:
        match = re.search(r'python(?: -O{1,2})? mutation_check\.py\n(\{.*?\n\})\n\nexit_code=0', text, re.S)
    if match is None:
        raise RuntimeError('Missing successful payload: ' + task)
    return json.loads(match.group(1))


def main():
    data = {}
    for mode in ('normal', 'O', 'OO'):
        text = (HERE / ('run-' + mode + '.log')).read_text()
        exits = re.findall(r'^exit_code=(\d+)$', text, re.M)
        if exits != ['0'] * 4:
            raise RuntimeError('Not four successful commands: ' + mode)
        tests = re.search(r'^Ran (\d+) tests in ', text, re.M)
        data[mode] = {'unittest_tests': int(tests.group(1)), 'exit_codes': [int(x) for x in exits],
                      'independent': payload(text, 'independent'), 'demo': payload(text, 'demo'),
                      'mutation': payload(text, 'mutation')}
    first = data['normal']
    expected_hashes = {name: hashlib.sha256((HERE.parent / name).read_bytes()).hexdigest()
                       for name in first['independent']['source_sha256']}
    for mode, result in data.items():
        if result['independent']['result'] != 'PASS':
            raise RuntimeError('Independent result failed: ' + mode)
        if result['independent']['counts'] != first['independent']['counts']:
            raise RuntimeError('Different checks between modes')
        if result['independent']['source_sha256'] != expected_hashes:
            raise RuntimeError('Code changed during or after run')
        if result['demo'] != first['demo'] or result['mutation'] != first['mutation']:
            raise RuntimeError('Different demo or mutation outputs between modes')
        if result['independent']['python_optimization'] != {'normal': 0, 'O': 1, 'OO': 2}[mode]:
            raise RuntimeError('Incorrect optimization level')
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.glob('*.py')}
    result = {'result': 'PASS', 'normal_O_OO_counts_identical': True, 'demo_outputs_identical': True,
              'mutation_outputs_identical': True, 'source_unchanged': True,
              'counts_per_mode': first['independent']['counts'],
              'source_sha256': expected_hashes, 'independent_script_sha256': hashes,
              'unit_tests_per_mode': first['unittest_tests'],
              'mutation_baseline_passes_per_mode': first['mutation']['baseline_passes'],
              'mutation_behavior_rejections_per_mode': first['mutation']['behavior_detected'],
              'mutation_harness_errors_per_mode': first['mutation']['harness_errors']}
    (HERE / 'summary.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
