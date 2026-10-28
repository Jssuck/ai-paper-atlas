import json,io,contextlib
from pathlib import Path
nb=json.loads(Path('teaching.zh-CN.ipynb').read_text());ns={};count=0
for c in nb['cells']:
    if c['cell_type']!='code':continue
    out=io.StringIO()
    with contextlib.redirect_stdout(out):exec(compile(''.join(c['source']),'replay-cell','exec'),ns)
    expected=''.join(''.join(o['text']) for o in c['outputs'])
    if out.getvalue()!=expected:raise RuntimeError('output mismatch')
    if c['execution_count'] is not None:raise RuntimeError('nonkernel counts must remain null')
    count+=1
report={'method':'stdlib compile/exec in fresh namespace','code_cells':count,'outputs_match':True,'kernel_started':False}
Path('notebook-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
