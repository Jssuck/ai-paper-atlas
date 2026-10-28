import json,io,contextlib
nb=json.load(open('teaching.zh-CN.ipynb')); ns={};n=0
for cell in nb['cells']:
 if cell['cell_type']!='code': continue
 n+=1;b=io.StringIO()
 with contextlib.redirect_stdout(b): exec(compile(''.join(cell['source']),'verify-cell-'+str(n),'exec'),ns)
 expected=''.join(cell['outputs'][0]['text'])
 if b.getvalue()!=expected: raise RuntimeError('output mismatch cell '+str(n))
r={'code_cells':n,'outputs_match':True,'method':'stdlib compile/exec, not kernel'}
open('notebook-check.json','w').write(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
