import json,io,contextlib
from pathlib import Path
nb=json.loads(Path('teaching.zh-CN.ipynb').read_text());ns={'__name__':'__notebook__'};count=0
for cell in nb['cells']:
 if cell['cell_type']!='code':continue
 count+=1;buf=io.StringIO()
 with contextlib.redirect_stdout(buf):exec(compile(''.join(cell['source']),f'cell-{count}','exec'),ns)
 saved=''.join(''.join(o['text']) for o in cell['outputs'] if o['output_type']=='stream' and o['name']=='stdout')
 if buf.getvalue()!=saved:raise RuntimeError('saved output differs')
if count!=5:raise RuntimeError('expected five code cells')
print('PASS: 5 code cells compile/exec and saved-output replay; no Jupyter kernel used')
