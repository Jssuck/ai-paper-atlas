"""Execute this repository's trusted code cells sequentially, not via Jupyter."""
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path

path = Path(__file__).with_name('i28_teaching.ipynb')
notebook = json.loads(path.read_text())
if notebook.get('nbformat') != 4:
    raise ValueError('expected notebook format 4')
namespace = {'__name__': '__notebook__'}
count = 0
for cell in notebook['cells']:
    if cell['cell_type'] != 'code':
        continue
    count += 1
    capture = StringIO()
    with redirect_stdout(capture):
        exec(compile(''.join(cell['source']), f'<cell {count}>', 'exec'), namespace)
    cell['execution_count'] = count
    cell['outputs'] = [{'output_type':'stream', 'name':'stdout',
                        'text':capture.getvalue().splitlines(keepends=True)}]
    print(f'Cell {count}: passed')
if count != 4:
    raise ValueError('expected four code cells')
notebook['metadata']['execution_validation'] = {
    'method': 'Python standard-library sequential exec in fresh process',
    'code_cells_executed': count,
    'jupyter_kernel': False,
    'nbformat_schema_validation': False
}
path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2)+'\n')
print('Four cells executed; no Jupyter kernel, nbformat schema validation, or renderer used.')
