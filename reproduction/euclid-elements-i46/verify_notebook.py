import json,io,contextlib
nb=json.load(open('teaching.zh-CN.ipynb'));ns={};n=0
for c in nb['cells']:
 if c['cell_type']=='code':
  n+=1;o=io.StringIO()
  with contextlib.redirect_stdout(o):exec(compile(c['source'],'<replay-cell>','exec'),ns)
  expected=''.join(x['text'] for x in c['outputs'])
  if o.getvalue()!=expected:raise RuntimeError('notebook output differs')
x={'code_cells':n,'replay_matches':True,'execution':'stdlib compile/exec, no kernel'}
open('notebook-check.json','w').write(json.dumps(x,indent=2)+'\n');print(json.dumps(x))
