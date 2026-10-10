"""Execute code cells in order using stdlib, not a Jupyter kernel."""
from contextlib import redirect_stdout, redirect_stderr
import io
import json
from pathlib import Path

path = Path('tutorial.ipynb')
notebook = json.loads(path.read_text(encoding='utf-8'))
assert notebook['nbformat'] == 4 and len(notebook['cells']) == 8
namespace = {'__name__': '__notebook__'}
records = []
for index, cell in enumerate(notebook['cells']):
    assert cell['cell_type'] in ('markdown', 'code')
    assert isinstance(cell['source'], list)
    if cell['cell_type'] != 'code':
        continue
    capture = io.StringIO()
    with redirect_stdout(capture), redirect_stderr(capture):
        exec(compile(''.join(cell['source']), f'notebook-cell-{index+1}', 'exec'), namespace)
    output = capture.getvalue()
    cell['execution_count'] = None
    cell['outputs'] = ([{'output_type': 'stream', 'name': 'stdout',
                        'text': output.splitlines(True)}] if output else [])
    records.append({'cell_number': index + 1, 'status': 'passed', 'stdout': output})
notebook['metadata']['validation_method'] = 'CPython sequential exec in one namespace; not a Jupyter kernel'
path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
report = {'method': 'stdlib JSON checks and sequential compile/exec',
          'jupyter_kernel_executed': False, 'nbformat_schema_validator_used': False,
          'execution_counts_are_null': True, 'ui_rendering_checked': False,
          'total_cells': 8, 'code_cells_passed': len(records), 'cells': records}
Path('notebook_check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Passed 4 code cells in order; no Jupyter kernel, schema validator, or UI rendering check.')
