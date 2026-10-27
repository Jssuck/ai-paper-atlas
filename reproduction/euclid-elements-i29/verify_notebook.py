import contextlib
import io
import json
from pathlib import Path
p=Path('teaching.zh-CN.ipynb'); nb=json.loads(p.read_text()); scope={'__name__':'notebook'}; n=0
for cell in nb['cells']:
    if cell['cell_type']!='code': continue
    n+=1; out=io.StringIO()
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(out):
        exec(compile(''.join(cell['source']),f'notebook-cell-{n}','exec'),scope)
    cell['execution_count']=n
    cell['outputs']=[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]
nb['metadata']['execution_method']='Python standard library compile/exec; not Jupyter kernel; stderr merged into captured stream'
p.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
result={'code_cells_executed':n,'method':'standard-library compile/exec; not Jupyter kernel','success':True}
Path('notebook-check.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result))
