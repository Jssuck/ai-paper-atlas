"""Fresh namespace replay and exact stored stdout comparison; no Jupyter kernel."""
import json,io,contextlib
nb=json.load(open('teaching.zh-CN.ipynb'));ns={};count=0
for cell in nb['cells']:
    if cell['cell_type']!='code':continue
    count+=1;out=io.StringIO()
    with contextlib.redirect_stdout(out):exec(compile(''.join(cell['source']),'replay-'+str(count),'exec'),ns)
    expected=''.join(''.join(o.get('text',[])) for o in cell['outputs'])
    if out.getvalue()!=expected:raise RuntimeError('stdout differs at cell '+str(count))
    if cell['execution_count']!=count:raise RuntimeError('execution counter mismatch')
result={'code_cells':count,'all_stdout_matches':True,'method':'fresh namespace compile/exec, not kernel'}
open('notebook-check.json','w').write(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
