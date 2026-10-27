"""Execute code cells with standard Python, NOT a Jupyter kernel."""
import contextlib,io,json
from pathlib import Path
p=Path(__file__).with_name('teaching.zh-CN.ipynb')
nb=json.loads(p.read_text()); namespace={'__name__':'__notebook__'}; n=0
if nb['nbformat']!=4: raise ValueError('unsupported notebook')
for cell in nb['cells']:
    if cell['cell_type']!='code': continue
    n+=1; out=io.StringIO()
    with contextlib.redirect_stdout(out): exec(compile(''.join(cell['source']),f'<notebook-cell-{n}>','exec'),namespace)
    cell['execution_count']=n
    cell['outputs']=[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]
p.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'passed','code_cells_executed':n,'method':'standard-library compile/exec in shared namespace; not Jupyter kernel'},ensure_ascii=False))
