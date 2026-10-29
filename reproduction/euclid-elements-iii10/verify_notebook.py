import json,io,contextlib
from pathlib import Path
nb=json.loads(Path('teaching.zh-CN.ipynb').read_text()); ns={};count=0
for cell in nb['cells']:
    if cell['cell_type']!='code':continue
    out=io.StringIO()
    with contextlib.redirect_stdout(out):exec(compile(cell['source'],'<notebook-replay>','exec'),ns)
    if out.getvalue()!=''.join(o.get('text','') for o in cell['outputs']):raise RuntimeError('output mismatch')
    count+=1
if count!=5:raise RuntimeError('expected five cells')
print('PASS: 5 cells replayed read-only via compile/exec, outputs identical; not kernel.')
