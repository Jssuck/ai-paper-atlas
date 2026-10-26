"""Execute plain-Python notebook cells with exec, NOT a Jupyter kernel."""
import contextlib
import io
import json
from pathlib import Path

p = Path('tutorial.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))
namespace = {'__name__':'__notebook__'}
count = 0
for cell in nb['cells']:
    if cell['cell_type'] != 'code':
        continue
    count += 1
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(''.join(cell['source']), f'notebook-cell-{count}', 'exec'), namespace)
    text = buf.getvalue()
    cell['execution_count'] = count
    cell['outputs'] = [{'output_type':'stream','name':'stdout','text':text.splitlines(True)}] if text else []
    print(f'CELL {count}\n{text}',end='')
nb['metadata']['execution_note'] = 'Python standard-library exec in cell order; not a Jupyter kernel.'
p.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Executed {count} code cells using standard-library exec, NOT a Jupyter kernel.')
