"""Execute then independently replay ordinary cells; no Jupyter kernel."""
import contextlib
import io
import json
from pathlib import Path
p=Path('teaching.zh-CN.ipynb');nb=json.loads(p.read_text())
def execute():
    ns={'__name__':'__notebook__'};outputs=[]
    for cell in nb['cells']:
        if cell['cell_type']!='code':continue
        output=io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(compile(''.join(cell['source']),f'notebook-cell-{len(outputs)+1}','exec'),ns)
        outputs.append(output.getvalue())
    return outputs
outputs=execute()
if len(outputs)!=6:raise RuntimeError('unexpected code cell count')
if outputs!=execute():raise RuntimeError('fresh namespace replay differs')
n=0
for cell in nb['cells']:
    if cell['cell_type']!='code':continue
    cell['execution_count']=None
    cell.setdefault('metadata',{})['compile_exec_index']=n+1
    cell['outputs']=[{'output_type':'stream','name':'stdout','text':outputs[n].splitlines(True)}]
    n+=1
p.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'code_cells_executed':n,'fresh_namespace_replay_identical':True,'status':'passed','executor':'standard-library compile/exec; not kernel'}))
