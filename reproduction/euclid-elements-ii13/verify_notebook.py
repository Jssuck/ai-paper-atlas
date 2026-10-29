"""Validate structure and replay code via compile/exec, NOT a Jupyter kernel."""
import contextlib
import io
import json
from pathlib import Path
nb=json.loads(Path('teaching.zh-CN.ipynb').read_text(encoding='utf-8'))
if nb['nbformat']!=4: raise ValueError('not nbformat 4')
ns={'__name__':'__notebook__'}
count=0
for cell in nb['cells']:
    if cell['cell_type']!='code': continue
    count+=1
    output=io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(compile(''.join(cell['source']),f'notebook-cell-{count}','exec'),ns)
    cell['execution_count']=count
    cell['outputs']=[dict(output_type='stream',name='stdout',text=output.getvalue().splitlines(True))]
    print(f'CELL {count}: PASS')
    print(output.getvalue(),end='')
nb['metadata']['verification']={'method':'standard-library compile/exec; not Jupyter kernel','code_cells_passed':count}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
Path('notebook-check.json').write_text(json.dumps({'method':'compile/exec, not kernel','passed':count,'failed':0},indent=2)+'\n')
print(f'PASS: {count} code cells; compile/exec replay, not kernel execution.')
