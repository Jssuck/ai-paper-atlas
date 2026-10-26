"""Execute code cells in order with stdlib, NOT a Jupyter kernel."""
import contextlib,io,json
from pathlib import Path
p=Path('teaching.zh-CN.ipynb'); nb=json.loads(p.read_text()); ns={'__name__':'notebook'}; n=0
for cell in nb['cells']:
    if cell['cell_type']!='code':continue
    n+=1; out=io.StringIO()
    with contextlib.redirect_stdout(out):exec(compile(''.join(cell['source']),f'cell_{n}','exec'),ns)
    cell['execution_count']=n;cell['outputs']=[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}] if out.getvalue() else []
p.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'code_cells':n,'method':'Python standard-library compile/exec','jupyter_kernel':False,'status':'passed'},ensure_ascii=False))
