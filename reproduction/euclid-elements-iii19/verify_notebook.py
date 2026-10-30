import json,io,contextlib
from pathlib import Path
nb=json.loads(Path('teaching.zh-CN.ipynb').read_text());env={};n=0
for c in nb['cells']:
 if c['cell_type']!='code':continue
 n+=1;out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(''.join(c['source']),f'replay-{n}','exec'),env)
 expected=''.join(''.join(o.get('text',[])) for o in c['outputs'])
 if out.getvalue()!=expected:raise RuntimeError(f'cell {n} output mismatch')
 print('cell',n,'output matches')
print('replayed',n,'cells via compile/exec; not Jupyter kernel')
