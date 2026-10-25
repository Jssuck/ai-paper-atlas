"""Execute notebook code cells in shared namespace; not a Jupyter kernel."""
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path

path=Path(__file__).with_name('i26_teaching.ipynb')
notebook=json.loads(path.read_text())
namespace={'__name__':'__notebook__'}
count=0
for cell in notebook['cells']:
    if cell['cell_type']!='code': continue
    count+=1
    capture=StringIO()
    with redirect_stdout(capture):
        exec(compile(''.join(cell['source']),f'<cell {count}>','exec'),namespace)
    cell['execution_count']=count
    cell['outputs']=[{'output_type':'stream','name':'stdout','text':capture.getvalue().splitlines(keepends=True)}] if capture.getvalue() else []
    print(f'Cell {count}: passed')
notebook['metadata']['execution_validation']={'method':'Python standard-library sequential exec in fresh process','code_cells_executed':count,'jupyter_kernel':False,'nbformat_schema_validation':False}
path.write_text(json.dumps(notebook,ensure_ascii=False,indent=2)+'\n')
print('4 cells executed in a shared namespace; no Jupyter kernel or renderer used.')
