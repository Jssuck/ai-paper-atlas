"""Execute the tutorial's plain Python cells sequentially, without a kernel."""
import contextlib
import io
import json
from pathlib import Path

path=Path(__file__).with_name('tutorial.ipynb')
notebook=json.loads(path.read_text(encoding='utf-8'))
if notebook.get('nbformat') != 4:
    raise ValueError('expected notebook format 4')
namespace={'__name__':'__notebook__'}
count=0
for cell in notebook['cells']:
    if cell['cell_type']=='code':
        count += 1
        output=io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(compile(''.join(cell['source']),f'cell-{count}','exec'),namespace)
        cell['execution_count']=count
        cell['outputs']=[{'output_type':'stream','name':'stdout','text':output.getvalue().splitlines(keepends=True)}]
        print(f'CELL {count}\n{output.getvalue()}',end='')
path.write_text(json.dumps(notebook,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Executed {count} plain-Python cells in one namespace; no Jupyter kernel used.')
