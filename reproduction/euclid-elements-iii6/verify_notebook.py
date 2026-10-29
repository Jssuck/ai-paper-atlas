"""Sequential compile/exec replay, not a Jupyter kernel."""
import contextlib,io,json,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--read-only',action='store_true');args=p.parse_args()
file=Path('teaching.zh-CN.ipynb');nb=json.loads(file.read_text(encoding='utf-8'));ns={};records=[]
for c in nb['cells']:
    if c['cell_type']!='code':continue
    k=len(records)+1;s=io.StringIO()
    with contextlib.redirect_stdout(s):exec(compile(''.join(c['source']),f'notebook-cell-{k}','exec'),ns)
    out=[{'output_type':'stream','name':'stdout','text':s.getvalue().splitlines(True)}]
    if args.read_only:
        if c['outputs']!=out or c['execution_count'] is not None: raise ValueError('saved replay mismatch')
    else:c['outputs']=out;c['execution_count']=None
    records.append({'cell':k,'passed':True});print(f'cell {k}: passed');print(s.getvalue(),end='')
if not args.read_only:
    file.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    Path('notebook-check.json').write_text(json.dumps({'method':'standard-library compile/exec; not Jupyter kernel','code_cells':len(records),'cells':records},indent=2)+'\n')
