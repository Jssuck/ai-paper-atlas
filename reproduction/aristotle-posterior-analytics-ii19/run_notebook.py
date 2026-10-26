"""Execute plain Python cells sequentially. This is NOT a Jupyter kernel."""
import contextlib
import io
import json
from pathlib import Path

path=Path(__file__).with_name('tutorial.ipynb')
nb=json.loads(path.read_text())
if (nb.get('nbformat'),nb.get('nbformat_minor')) != (4,5): raise ValueError('expected notebook v4.5')
ids=[c['id'] for c in nb['cells']]
if len(set(ids)) != len(ids): raise ValueError('duplicate cell IDs')
namespace={'__name__':'__notebook_exec__'}
count=0
for cell in nb['cells']:
    if cell['cell_type'] not in ('markdown','code') or not isinstance(cell['source'],list): raise ValueError('invalid cell')
    if cell['cell_type'] != 'code': continue
    out=io.StringIO()
    with contextlib.redirect_stdout(out): exec(compile(''.join(cell['source']),'<cell-'+cell['id']+'>','exec'),namespace)
    count+=1
    cell['execution_count']=None
    cell['outputs']=[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(keepends=True)}] if out.getvalue() else []
    print('cell',cell['id'],'OK'); print(out.getvalue(),end='')
nb['metadata']['execution_method']='Python standard-library sequential exec, not Jupyter kernel; execution_count intentionally null'
path.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('executed_code_cells=',count)
