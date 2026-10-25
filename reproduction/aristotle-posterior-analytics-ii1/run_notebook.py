"""Execute this pure-Python notebook sequentially; NOT a Jupyter kernel."""
import contextlib
import io
import json
from pathlib import Path

path = Path(__file__).with_name('tutorial.ipynb')
notebook = json.loads(path.read_text())
namespace = {'__name__': '__notebook__'}
count = 0
for cell in notebook['cells']:
    if cell['cell_type'] != 'code':
        continue
    count += 1
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(compile(''.join(cell['source']), f'notebook-cell-{count}', 'exec'), namespace)
    cell['execution_count'] = count
    cell['outputs'] = [{'output_type': 'stream', 'name': 'stdout', 'text': out.getvalue().splitlines(True)}] if out.getvalue() else []
    print(f'CELL {count}\n{out.getvalue()}', end='')
path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + '\n')
print(f'Executed {count} code cells with CPython exec; not a Jupyter kernel.')
