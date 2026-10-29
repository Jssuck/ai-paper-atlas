"""Read-only top-to-bottom replay, compare actual stdout to saved output."""
import json,io,contextlib
from pathlib import Path
nb=json.loads(Path('teaching.zh-CN.ipynb').read_text());env={};count=0
for cell in nb['cells']:
 if cell['cell_type']!='code':continue
 count+=1;output=io.StringIO()
 with contextlib.redirect_stdout(output):exec(compile(''.join(cell['source']),f'replay-{count}','exec'),env)
 expected=''.join(''.join(o['text']) for o in cell['outputs'] if o['output_type']=='stream')
 if output.getvalue()!=expected:raise RuntimeError('saved output mismatch')
 print('cell',count,'stdout matches')
if count!=5:raise RuntimeError('wrong code cell count')
print('read-only replay passed; non-kernel execution')
