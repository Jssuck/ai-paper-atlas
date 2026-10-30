import json,io,contextlib
from pathlib import Path
nb=json.loads(Path('teaching.zh-CN.ipynb').read_text());ns={};count=0
for cell in nb['cells']:
 if cell['cell_type']!='code':continue
 if cell['execution_count'] is not None:raise ValueError('not a kernel run')
 b=io.StringIO()
 with contextlib.redirect_stdout(b):exec(compile(''.join(cell['source']),'notebook-cell','exec'),ns)
 expected=''.join(''.join(o.get('text',[])) for o in cell['outputs'])
 if b.getvalue()!=expected:raise ValueError('saved output mismatch')
 count+=1
print('Verified',count,'code cells by stdlib compile/exec; NOT kernel execution')
