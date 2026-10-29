"""Execute cells with compile/exec, not a Jupyter kernel."""
import contextlib,io,json
from pathlib import Path
p=Path('teaching.zh-CN.ipynb');nb=json.loads(p.read_text(encoding='utf-8'));ns={};n=0
for cell in nb['cells']:
    if cell['cell_type']!='code': continue
    n+=1;s=io.StringIO()
    with contextlib.redirect_stdout(s): exec(compile(''.join(cell['source']),f'notebook-cell-{n}','exec'),ns)
    cell['execution_count']=n
    cell['outputs']=[{'output_type':'stream','name':'stdout','text':s.getvalue().splitlines(True)}]
    print(f'cell {n}: passed'); print(s.getvalue(),end='')
p.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
Path('notebook-check.json').write_text(json.dumps({'code_cells':n,'status':'passed','method':'standard-library compile/exec; not Jupyter kernel'},indent=2)+'\n')
