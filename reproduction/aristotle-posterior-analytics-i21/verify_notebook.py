"""Execute code cells sequentially with stdlib exec, NOT a Jupyter kernel."""
import contextlib
import io
import json
from pathlib import Path

path=Path(__file__).with_name('i21_teaching.ipynb')
nb=json.loads(path.read_text())
namespace={'__name__':'__notebook__'}
count=0
for cell in nb['cells']:
    if cell['cell_type']!='code':continue
    count+=1
    out=io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(compile(''.join(cell['source']),f'i21-notebook-cell-{count}','exec'),namespace)
    cell['execution_count']=count
    cell['outputs']=[{'name':'stdout','output_type':'stream','text':out.getvalue().splitlines(True)}]
    print(f'code_cell_{count}: passed')
path.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print(f'{count} code cells passed in one fresh Python process / shared namespace.')
print('Standard-library sequential execution only; no Jupyter kernel or nbformat schema validator was installed or used.')
