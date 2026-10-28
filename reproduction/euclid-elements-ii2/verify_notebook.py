import json,io,contextlib
nb=json.load(open('teaching.zh-CN.ipynb'));ns={};n=0
for c in nb['cells']:
    if c['cell_type']!='code':continue
    n+=1;b=io.StringIO()
    with contextlib.redirect_stdout(b):exec(compile(''.join(c['source']),'notebook-replay','exec'),ns)
    if b.getvalue()!=''.join(c['outputs'][0]['text']):raise RuntimeError('Notebook replay mismatch')
r={'code_cells':n,'outputs_match':True,'execution':'standard-library compile/exec in fresh namespace','jupyter_kernel_started':False}
open('notebook-check.json','w').write(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
