import json,io,contextlib
from pathlib import Path
nb=json.loads(Path('teaching.zh-CN.ipynb').read_text());ns={};n=0
for cell in nb['cells']:
 if cell['cell_type']!='code':continue
 n+=1;out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(''.join(cell['source']),'<replay>','exec'),ns)
 expected=''.join(''.join(o.get('text',[])) for o in cell['outputs'])
 if out.getvalue()!=expected:raise RuntimeError('replay differs')
report={'code_cells':n,'outputs_match':True,'method':'fresh namespace compile/exec','kernel_started':False}
Path('notebook-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
