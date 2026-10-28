import json,contextlib,io
nb=json.load(open('teaching.zh-CN.ipynb'));ns={};n=0
for c in nb['cells']:
    if c['cell_type']!='code': continue
    n+=1;out=io.StringIO()
    with contextlib.redirect_stdout(out): exec(compile(''.join(c['source']),f'replay-{n}','exec'),ns)
    expected=''.join(''.join(o.get('text',[])) for o in c['outputs'])
    if out.getvalue()!=expected: raise RuntimeError(f'output mismatch {n}')
r={'code_cells':n,'stdout_match':True,'execution':'stdlib compile/exec in fresh namespace; no Jupyter kernel'}
open('notebook-check.json','w').write(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
