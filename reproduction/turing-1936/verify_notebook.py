"""Stdlib-only sequential code-cell check; deliberately not Jupyter execution."""
import contextlib
import io
import json
import platform
import sys
from pathlib import Path
path = Path('turing_teaching.zh-CN.ipynb')
nb = json.loads(path.read_text())
assert nb['nbformat'] == 4
assert len({c['id'] for c in nb['cells']}) == len(nb['cells'])
namespace = {'__name__': '__main__'}
records = []
for index, cell in enumerate(nb['cells']):
    assert cell['cell_type'] in ('markdown', 'code')
    if cell['cell_type'] != 'code':
        continue
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exec(compile(''.join(cell['source']), f'notebook_cell_{index}', 'exec'), namespace)
    # Captured output is genuine, but no Jupyter execution counter is fabricated.
    cell['execution_count'] = None
    cell['outputs'] = [{'output_type': 'stream', 'name': 'stdout',
                        'text': stdout.getvalue().splitlines(keepends=True)}]
    records.append({'cell_index': index, 'status': 'passed', 'stdout': stdout.getvalue()})
report = {'method': 'Standard-library sequential exec in a fresh Python process',
          'python': sys.version, 'platform': platform.platform(),
          'jupyter_kernel_executed': False, 'nbformat_schema_validator_used': False,
          'code_cells_passed': len(records), 'records': records}
Path('notebook_check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
path.write_text(json.dumps(nb, ensure_ascii=False, indent=2) + '\n')
print(f'{len(records)} code cells passed sequential Python execution; Jupyter kernel not executed.')
