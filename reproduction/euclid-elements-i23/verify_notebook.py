"""Execute ordinary Python cells sequentially, not through a Jupyter kernel."""
import contextlib
import io
import json
from pathlib import Path
p=Path('teaching.zh-CN.ipynb');nb=json.loads(p.read_text());ns={'__name__':'__notebook__'};n=0
for cell in nb['cells']:
    if cell['cell_type']!='code':continue
    n+=1;output=io.StringIO()
    with contextlib.redirect_stdout(output):exec(compile(''.join(cell['source']),f'notebook-cell-{n}','exec'),ns)
    cell['execution_count']=None
    cell.setdefault('metadata',{})['compile_exec_index']=n
    cell['outputs']=[{'output_type':'stream','name':'stdout','text':output.getvalue().splitlines(True)}]
if n!=6:raise RuntimeError('unexpected code cell count')
p.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'code_cells_executed':n,'status':'passed','executor':'standard-library compile/exec; not kernel'}))
