"""Independently verify completion, mutation classifications, and real timeout.

Each process must either complete all AST-derived author tests or be classified
as an infrastructure/control result. No assertion is removable with -O/-OO.
"""
import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import mutation_check as harness


def require(condition, explanation):
    if not condition:
        raise RuntimeError(explanation)


def author_test_ids():
    tree = ast.parse((ROOT/'test_model.py').read_text(encoding='utf-8'))
    return sorted('test_model.' + node.name + '.' + method.name
                  for node in tree.body if isinstance(node, ast.ClassDef)
                  for method in node.body if isinstance(method, ast.FunctionDef)
                  and method.name.startswith('test_'))


def main():
    mode = ('normal', 'O', 'OO')[sys.flags.optimize]
    flags = [] if mode == 'normal' else ['-' + mode]
    output = ROOT/'independent-review'/'logs'/('harness-' + mode)
    output.mkdir(parents=True, exist_ok=True)
    expected = author_test_ids()
    require(len(expected) == 40, 'Author method set changed; review before trusting the harness')
    source = (ROOT/'model.py').read_text(encoding='utf-8')
    records = []
    cases = [
        ('baseline', source, (), 'pass'),
        ('behavior_change', source.replace('maximum = max(weight for _, weight in row)',
                                          'maximum = min(weight for _, weight in row)'), (), 'behavioral_kill'),
        ('syntax_error', source + '\ndef broken(:\n', (), 'harness_error'),
        ('import_error', 'raise ImportError("independent control")\n'+source, (), 'harness_error'),
        ('empty_suite', source, ('--empty-suite',), 'suite_mismatch'),
        ('test_error', source.replace('row = [(value, weight)',
                      'raise RuntimeError("independent runtime control")\n        row = [(value, weight)'),
         (), 'test_error'),
        ('early_exit', 'import os\nos._exit(0)\n'+source, (), 'harness_error'),
        ('extra_result_marker', 'print("RESULT_JSON={}")\n'+source, (), 'harness_error'),
    ]
    for name, modified, extra, wanted in cases:
        result = harness.run_copy(modified, flags, output, name, expected, extra)
        require(result['classification'] == wanted, name + ': wrong classification')
        if wanted in ('pass', 'behavioral_kill'):
            summary = result['summary']
            require(summary['tests'] == 40 and summary['ids'] == expected, 'Incomplete test run counted')
            require(summary['errors'] == 0 and summary['skipped'] == 0, 'Invalid behavioral result')
        records.append({'name':name, 'expected':wanted, 'observed':result['classification'],
                        'returncode':result.get('returncode'), 'summary':result.get('summary')})
    # Real subprocess timeout, shortened only for this isolated control.
    real_run = harness.subprocess.run
    def short_run(*args, **kwargs):
        kwargs['timeout'] = 0.15
        return real_run(*args, **kwargs)
    harness.subprocess.run = short_run
    try:
        result = harness.run_copy('import time\ntime.sleep(2)\n'+source,
                                  flags, output, 'actual_timeout', expected)
    finally:
        harness.subprocess.run = real_run
    require(result['classification'] == 'timeout', 'Timeout incorrectly credited')
    records.append({'name':'actual_timeout', 'expected':'timeout', **result})
    # Direct classifier truth table deliberately presents inconsistent completions.
    normal = {'stage':'complete', 'tests':40, 'ids':expected, 'failures':1,
              'errors':0, 'skipped':0, 'optimized':sys.flags.optimize}
    direct = [(1, deepcopy(normal), 'behavioral_kill'), (0, deepcopy(normal), 'harness_error'),
              (2, deepcopy(normal), 'harness_error'), (1, None, 'harness_error')]
    for field, value, wanted in [('tests',0,'suite_mismatch'), ('tests',39,'suite_mismatch'),
                                ('ids',[],'suite_mismatch'), ('stage','bootstrap_error','harness_error'),
                                ('errors',1,'test_error'), ('skipped',1,'suite_mismatch'),
                                ('failures',0,'harness_error')]:
        changed = deepcopy(normal); changed[field] = value
        direct.append((1, changed, wanted))
    for returncode, summary, wanted in direct:
        require(harness.classify(returncode, summary, expected) == wanted,
                'Classifier accepted inconsistent metadata')
    for path in output.glob('*.log'):
        raw = path.read_text(encoding='utf-8')
        path.write_text(raw.replace(str(ROOT), '<release>').replace(sys.executable,'python'), encoding='utf-8')
    report = {'stage':'complete', 'optimized':sys.flags.optimize, 'subprocess_controls':len(records),
              'classifier_cases':len(direct), 'success':True, 'records':records,
              'model_sha256':hashlib.sha256((ROOT/'model.py').read_bytes()).hexdigest(),
              'harness_sha256':hashlib.sha256((ROOT/'mutation_check.py').read_bytes()).hexdigest()}
    (output/'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('HARNESS_AUDIT_RESULT=' + json.dumps({k:v for k,v in report.items() if k != 'records'},sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
