"""Read-only independent sequential replay, not Jupyter execution."""
import contextlib,hashlib,io,json
from pathlib import Path
p=Path('teaching.zh-CN.ipynb'); before=p.read_bytes(); nb=json.loads(before); namespace={};n=0
for cell in nb['cells']:
 if cell['cell_type']!='code':continue
 n+=1;out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(''.join(cell['source']),f'independent-cell-{n}','exec'),namespace)
 saved=''.join(''.join(o.get('text',[])) for o in cell.get('outputs',[]) if o.get('output_type')=='stream' and o.get('name')=='stdout')
 if out.getvalue()!=saved:raise RuntimeError(f'cell {n} saved stdout mismatch')
 print(f'cell {n}: pass; saved stdout matches')
if p.read_bytes()!=before:raise RuntimeError('notebook modified')
if n!=5:raise RuntimeError('expected five code cells')
print(json.dumps({'code_cells':n,'status':'pass','method':'independent standard-library compile/exec; no Jupyter kernel','notebook_sha256':hashlib.sha256(before).hexdigest()},indent=2))
