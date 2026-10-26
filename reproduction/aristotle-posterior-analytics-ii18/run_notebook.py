"""Execute ordinary Python cells using exec, NOT a Jupyter kernel."""
import contextlib
import io
import json
from pathlib import Path

path = Path(__file__).with_name('tutorial.ipynb')
nb = json.loads(path.read_text(encoding='utf-8'))
if (nb.get('nbformat'), nb.get('nbformat_minor')) != (4, 5):
    raise ValueError('expected nbformat 4.5')
ids = [cell['id'] for cell in nb['cells']]
if len(ids) != len(set(ids)):
    raise ValueError('duplicate cell IDs')
namespace = {'__name__': '__notebook_exec__'}
count = 0
for cell in nb['cells']:
    if cell['cell_type'] not in ('markdown', 'code') or not isinstance(cell['source'], list):
        raise ValueError('invalid cell type or source')
    if cell['cell_type'] != 'code':
        continue
    count += 1
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(compile(''.join(cell['source']), '<cell-'+cell['id']+'>', 'exec'), namespace)
    cell['execution_count'] = count
    cell['outputs'] = ([{'output_type':'stream', 'name':'stdout',
                        'text':out.getvalue().splitlines(keepends=True)}] if out.getvalue() else [])
    print('cell', cell['id'], 'OK')
    print(out.getvalue(), end='')
nb['metadata']['execution_method'] = 'Python standard-library exec; not Jupyter kernel'
path.write_text(json.dumps(nb, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('executed_code_cells=', count)
