import json,contextlib,io
n=json.load(open('teaching.zh-CN.ipynb')); ns={}; count=0
for c in n['cells']:
    if c['cell_type']!='code': continue
    out=io.StringIO()
    with contextlib.redirect_stdout(out): exec(compile(c['source'],'<replay>','exec'),ns)
    if out.getvalue()!=c['outputs'][0]['text']: raise RuntimeError('replay mismatch')
    count+=1
r={'code_cells':count,'replay_matches':True,'method':'fresh namespace stdlib compile/exec, not Jupyter kernel'}
open('notebook-check.json','w').write(json.dumps(r,indent=2)+'\n'); print(json.dumps(r))
