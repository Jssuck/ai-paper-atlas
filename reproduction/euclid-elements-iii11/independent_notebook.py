"""Independent read-only audit of the saved notebook, without Jupyter kernel."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
p=Path('teaching.zh-CN.ipynb'); before=p.read_bytes(); nb=json.loads(before)
if (nb['nbformat'],nb['nbformat_minor'])!=(4,5):raise RuntimeError('format version')
ids=[c['id'] for c in nb['cells']]
if len(ids)!=len(set(ids)):raise RuntimeError('duplicate cell ids')
namespace={'__name__':'__independent_notebook__'};n=0
for cell in nb['cells']:
 if cell['cell_type']=='markdown':continue
 if cell['cell_type']!='code':raise RuntimeError('unexpected cell type')
 n+=1
 if cell['execution_count']!=n:raise RuntimeError('execution order')
 if any(o.get('output_type')!='stream' or o.get('name')!='stdout' for o in cell['outputs']):raise RuntimeError('unsupported output')
 captured=io.StringIO()
 with contextlib.redirect_stdout(captured):
  exec(compile(''.join(cell['source']),'independent-notebook-cell','exec'),namespace)
 saved=''.join(''.join(o['text']) for o in cell['outputs'])
 if captured.getvalue()!=saved:raise RuntimeError('saved stdout mismatch')
 print('code cell',n,'source executed and saved stdout matched')
if n!=5 or p.read_bytes()!=before:raise RuntimeError('count or accidental mutation')
print('notebook sha256:',hashlib.sha256(before).hexdigest())
print('PASS: 5 cells; read-only compile/exec; no Jupyter kernel or full schema validation claimed')
