"""Execute our five plain Python cells with stdlib exec, not a Jupyter kernel."""
import contextlib
import io
import json
from pathlib import Path

path = Path(__file__).with_name('tutorial.ipynb')
notebook = json.loads(path.read_text(encoding='utf-8'))
namespace = {'__name__': '__notebook__'}
count = 0
for cell in notebook['cells']:
    if cell['cell_type'] != 'code':
        continue
    count += 1
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(compile(''.join(cell['source']), '<notebook-cell>', 'exec'), namespace)
    cell['execution_count'] = count
    cell['outputs'] = [{'output_type':'stream','name':'stdout','text':output.getvalue().splitlines(keepends=True)}]
    print('CELL', count)
    print(output.getvalue(), end='')
notebook['metadata']['execution_method'] = 'Python standard-library exec; no Jupyter kernel, nbclient or notebook magics'
path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
print('Executed code cells:', count)
