"""Run the independent review, reconcile original evidence, preserve relative logs."""
from datetime import datetime, timezone
import ast
import hashlib
from itertools import product
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
from check_independent import reference_paths, require

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot():
    return {p.relative_to(ROOT).as_posix(): digest(p)
            for p in sorted(ROOT.rglob('*')) if p.suffix in ('.py', '.md')}


def recalculate_original_counts():
    """Recount author domain independently, without calling its verification code.

    This is evidence reconciliation, not additional independent coverage.
    """
    labels = ('A', 'B', 'C')
    positions = tuple((a, b) for a in labels for b in labels if a != b)
    totals = dict(extension_assignments=64, graph_contexts=0, valid_graphs=0,
                  invalid_graphs=0, reachability_queries=0, semantic_queries=0,
                  certified_queries=0, true_unencoded_queries=0,
                  failed_inclusions=0, mutual_reachability_pairs=0,
                  renamed_valid_graphs=0, renamed_queries=0)
    for graph_mask in range(64):
        edges = tuple(e for i, e in enumerate(positions) if graph_mask & (1 << i))
        paths = {a: reference_paths(labels, edges, a) for a in labels}
        for memberships in product(tuple(product((False, True), repeat=2)), repeat=3):
            truth = {(a, b): all(not x or y for x, y in zip(memberships[labels.index(a)], memberships[labels.index(b)]))
                     for a, b in product(labels, repeat=2)}
            valid = all(truth[e] for e in edges)
            totals['graph_contexts'] += 1
            totals['valid_graphs' if valid else 'invalid_graphs'] += 1
            if valid:
                totals['renamed_valid_graphs'] += 6
                totals['renamed_queries'] += 54
            for a, b in product(labels, repeat=2):
                totals['reachability_queries'] += 1
                totals['semantic_queries'] += 1
                totals['failed_inclusions'] += not truth[a, b]
                if valid:
                    reachable = paths[a][b] is not None
                    totals['certified_queries'] += 1
                    totals['true_unencoded_queries'] += truth[a, b] and not reachable
                    totals['mutual_reachability_pairs'] += reachable and paths[b][a] is not None
    return totals


def original_evidence():
    report_path = ROOT / 'evidence/verification.json'
    report = json.loads(report_path.read_text())
    require(report['status'] == 'passed', 'author evidence not passed')
    require(report['sources_unchanged'], 'author sources changed during recording')
    require(report['source_sha256_before'] == report['source_sha256_after'], 'author source snapshots differ')
    for filename, expected in report['source_sha256_after'].items():
        require(digest(ROOT / filename) == expected, 'stale author evidence: ' + filename)
    expected_counts = recalculate_original_counts()
    records = {(run['program'], run['mode']): run for run in report['runs']}
    require(len(records) == 6 and len(report['runs']) == 6, 'wrong original run inventory')
    tree = ast.parse((ROOT / 'test_named_classes.py').read_text())
    unit_count = sum(isinstance(node, ast.FunctionDef) and node.name.startswith('test_') for node in ast.walk(tree))
    demos, semantic_reports = [], []
    for level, mode in enumerate(('normal', 'O', 'OO')):
        for program in ('verify.py', 'demo.py'):
            run = records[program, mode]
            log = ROOT / 'evidence' / run['log']
            require(run['exit_code'] == 0 and digest(log) == run['log_sha256'], 'original log or exit mismatch')
        lines = (ROOT / 'evidence' / records['verify.py', mode]['log']).read_text().splitlines()
        runtime = [json.loads(line[8:]) for line in lines if line.startswith('RUNTIME ')]
        require(len(runtime) == 1 and runtime[0]['optimization_level'] == level, 'actual original optimization mismatch')
        require(any(re.fullmatch(r'Ran ' + str(unit_count) + r' tests in .+s', line) for line in lines), 'unit count mismatch')
        counts = [json.loads(line[11:]) for line in lines if line.startswith('EXHAUSTIVE ')]
        require(counts == [expected_counts], 'original enumeration count mismatch')
        mutation = [json.loads(line[9:]) for line in lines if line.startswith('MUTATION ')]
        require(len(mutation) == 1 and mutation[0]['counts'] == {'killed_semantic': 10, 'survived': 0, 'harness_error': 0}, 'mutant count mismatch')
        require(len(mutation[0]['controls']) == 3, 'original mutation control count mismatch')
        semantic_reports.append(mutation[0])
        demos.append((ROOT / 'evidence' / records['demo.py', mode]['log']).read_bytes())
    require(len(set(demos)) == 1 and semantic_reports[0] == semantic_reports[1] == semantic_reports[2], 'original cross-mode outputs differ')
    demo = dict((name, json.loads(value)) for name, value in
                (line.split(': ', 1) for line in demos[0].decode().splitlines()))
    expected = {
        '对象顺序': ['红三角', '蓝三角', '红方块', '蓝方块'],
        '外延[三角形]': ['红三角', '蓝三角'], '外延[图形]': ['红三角', '蓝三角', '红方块', '蓝方块'],
        '外延[红色]': ['红三角', '红方块'], '外延[三边形]': ['红三角', '蓝三角'], '外延[空类]': [],
        '断言边': [['三边形', '三角形'], ['三角形', '图形'], ['空类', '红色']],
        '单例检查[红三角是否红色]': True,
        '原图强连通分量': [['三角形'], ['图形'], ['红色'], ['三边形'], ['空类']],
        '加同义返回边后的分量': [['三角形', '三边形'], ['图形'], ['红色'], ['空类']],
        '改名后[D→B]': ['D', 'A', 'B'], '改名后对象数': 4,
        '坏边及反例': [['红色', '三角形', '红方块']], '坏图原始可达[图形→图形]': ['图形'],
        '坏图认证[图形→图形]': '拒绝：全图有效性前提不成立',
    }
    for name, truth, path, witness in (
        ('三边形→图形', True, ['三边形', '三角形', '图形'], None),
        ('红色→图形', True, None, None), ('三角形→红色', False, None, '蓝三角'),
        ('红色→三角形', False, None, '红方块'), ('三角形→三边形', True, None, None),
        ('空类→三角形', True, None, None), ('三角形→三角形', True, ['三角形'], None)):
        expected['查询[' + name + ']'] = {'有限域包含': truth, '图证明': path, '反例': witness}
    require(demo == expected, 'worked example differs from independent expected output')
    walkthrough = (ROOT / 'WALKTHROUGH.zh-CN.md').read_text()
    for block in re.findall(r'```text\n(.*?)\n```', walkthrough, re.S):
        require(json.loads(block) in demo.values(), 'walkthrough JSON does not occur in actual demo')
    readme = (ROOT / 'README.md').read_text()
    require(f'{unit_count} 个专门测试方法' in readme, 'README unit count differs')
    row_map = {'外延赋值': 'extension_assignments', '图上下文': 'graph_contexts',
               '全边有效图': 'valid_graphs', '含坏边图': 'invalid_graphs',
               '可达性查询': 'reachability_queries', '语义包含及见证查询': 'semantic_queries',
               '有效图认证查询': 'certified_queries', '有效图中真但不可达的查询': 'true_unencoded_queries',
               '全部图中的失败包含查询': 'failed_inclusions', '有效图中双向可达有序对': 'mutual_reachability_pairs',
               '有效图双射改名版本': 'renamed_valid_graphs', '改名后的查询': 'renamed_queries'}
    for label, key in row_map.items():
        row = re.search(r'^\| ' + re.escape(label) + r' \| ([\d,]+) \|', readme, re.M)
        require(row is not None and int(row.group(1).replace(',', '')) == expected_counts[key], 'README count differs: ' + label)
    quality_path = ROOT / 'evidence/source-quality.json'
    require(digest(quality_path) == report['source_quality_sha256'], 'quality evidence hash differs')
    return {'unit_tests_per_mode': unit_count, 'independently_recounted_original_domain': expected_counts,
            'demo_fields_checked': len(expected), 'author_evidence_sha256': digest(report_path),
            'source_quality_evidence_sha256': digest(quality_path)}



def public_quality():
    tables = []
    for path in sorted(ROOT.rglob('*.md')):
        text = path.read_text()
        in_fence, columns = False, None
        for number, line in enumerate(text.splitlines(), 1):
            if line.startswith('```'):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if line.startswith('|'):
                delimiters = list(re.finditer(r'(?<!\\)(?:\\\\)*\|', line))
                count = len(delimiters) - 1
                require(line.endswith('|') and count > 0, 'missing outer table delimiter')
                if columns is None:
                    columns = count
                require(count == columns, 'raw Markdown table column mismatch')
                tables.append({'file': path.relative_to(ROOT).as_posix(), 'line': number, 'cells': count})
            else:
                columns = None
            require('$' not in re.sub(r'\$`[^`\n]*`\$', '', line), 'non-GitHub inline math style')
        require(not in_fence, 'unclosed Markdown fence')
        for link in re.findall(r'\]\(([^)]+)\)', text):
            if '://' not in link and not link.startswith('#'):
                require((path.parent / link.split('#', 1)[0]).exists(), 'broken local Markdown link')
    for path in ROOT.rglob('*'):
        if path.suffix in ('.py', '.md', '.json', '.txt'):
            text = path.read_text()
            require(not re.search(r'/(?:workspace|Users|home|root)/', text),
                    'private absolute path in public file: ' + path.relative_to(ROOT).as_posix())
        if path.suffix == '.py':
            require(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(text))), 'bare assert in published Python')
    author = json.loads((ROOT / 'evidence/verification.json').read_text())
    require(author['environment']['working_directory'] == '.', 'public author cwd not relative')
    require('node' not in author['environment'].get('uname', {}), 'host identifier still published')
    return {'markdown_source_table_rows': tables, 'private_absolute_path_scan': 'passed',
            'scope': 'Source only; not a rendered-browser, pixel, or security certification.'}


def main():
    destination = HERE / 'verification.json'
    if not destination.exists():
        destination.write_text('{}\n')
    before = snapshot()
    report = {'started_utc': datetime.now(timezone.utc).isoformat(),
              'environment': {'python_version': sys.version, 'implementation': platform.python_implementation(),
                              'system': platform.system(), 'release': platform.release(), 'machine': platform.machine(),
                              'working_directory': '.', 'working_directory_basis': 'package root; absolute host path omitted'},
              'source_sha256_before': before, 'runs': []}
    summaries = []
    for level, (mode, flags) in enumerate((('normal', []), ('O', ['-O']), ('OO', ['-OO']))):
        command = ['python3', '-B', *flags, 'independent-review/check_independent.py']
        result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        filename = f'check-{mode}.txt'
        (HERE / filename).write_bytes(result.stdout)
        require(result.returncode == 0, 'independent process failed: ' + mode)
        lines = result.stdout.decode().splitlines()
        runtime = [json.loads(line[8:]) for line in lines if line.startswith('RUNTIME ')]
        require(len(runtime) == 1 and runtime[0]['optimization_level'] == level, 'independent optimization level differs')
        require(runtime[0]['module_docstring_present'] == (level != 2), '-OO documentation-string control differs')
        summaries.append(tuple(line for line in lines if line.startswith(('INDEPENDENT_COUNTS ', 'SOURCE_SHA256 ', 'PASS: '))))
        report['runs'].append({'command': command, 'working_directory': '.', 'mode': mode,
                               'exit_code': result.returncode, 'actual_optimization_level': level,
                               'log': filename, 'log_sha256': digest(HERE / filename)})
    require(len(set(summaries)) == 1 and all(len(s) == 3 for s in summaries), 'independent summaries differ across modes')
    report['original_evidence_reconciliation'] = original_evidence()
    report['source_quality'] = public_quality()
    report['source_sha256_after'] = snapshot()
    require(before == report['source_sha256_after'], 'review sources changed during execution')
    report.update(status='passed', sources_unchanged=True, cross_mode_summaries_identical=True,
                  finished_utc=datetime.now(timezone.utc).isoformat())
    (HERE / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': 'passed', 'independent_modes': 3, 'original_evidence_reconciled': True}, sort_keys=True))


if __name__ == '__main__':
    main()
