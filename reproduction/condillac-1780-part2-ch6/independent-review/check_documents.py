"""Check source-table cell counts and run tutorial snippets; not render QA."""
from pathlib import Path
import ast
import contextlib
import hashlib
import io
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def count_cells(line):
    # GFM cell separators remain separators even within backticks/math.
    bars = []
    for index, char in enumerate(line):
        if char != '|':
            continue
        slashes = 0
        prior = index - 1
        while prior >= 0 and line[prior] == '\\':
            slashes += 1
            prior -= 1
        if slashes % 2 == 0:
            bars.append(index)
    require(bool(bars) and bars[0] == 0 and bars[-1] == len(line) - 1, 'table outer bars')
    return len(bars) - 1


def main():
    article = ROOT.parents[1] / 'papers/1780/condillac-logic-part2-ch6.zh-CN.md'
    documents = (*sorted(ROOT.rglob('*.md')), article)
    tables = rows = 0
    details = []
    for path in documents:
        in_fence = False
        width = None
        table_count = row_count = 0
        for line in path.read_text().splitlines():
            if line.startswith('```'):
                in_fence = not in_fence
            if not in_fence and line.startswith('|'):
                current = count_cells(line)
                if width is None:
                    width = current
                    table_count += 1
                require(current == width, path.name + ': inconsistent source table width')
                row_count += 1
            else:
                width = None
        require(not in_fence, path.name + ': unclosed fence')
        tables += table_count
        rows += row_count
        details.append({'file': path.name, 'tables': table_count, 'rows_including_headers_and_separators': row_count})
    # Assert-free implementation and independent checker stay live under -O/-OO.
    for file in ('condillac_model.py', 'independent-review/independent_audit.py'):
        tree = ast.parse((ROOT / file).read_text())
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)), file + ': bare assert')
    tutorial = (ROOT / 'WALKTHROUGH.zh-CN.md').read_text()
    blocks = re.findall(r'^```python\n(.*?)^```', tutorial, re.M | re.S)
    namespace = {'__name__': '__independent_tutorial__'}
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        for index, block in enumerate(blocks, 1):
            print('WALKTHROUGH Python block', index)
            exec(compile(block, '<WALKTHROUGH block ' + str(index) + '>', 'exec'), namespace)
    print(output.getvalue(), end='')
    result = {'result': 'PASS', 'source_tables': tables, 'source_table_rows': rows,
              'table_details': details, 'tutorial_python_blocks': len(blocks),
              'scope': 'Source cell boundaries and execution only; no rendered GitHub/browser QA.'}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
