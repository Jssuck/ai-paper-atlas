"""Execute code cells sequentially using Python exec, not a Jupyter kernel."""
import contextlib,io,json
from pathlib import Path
root=Path(__file__).resolve().parent
path=root/'tutorial.ipynb'
nb=json.loads(path.read_text())
ids=[c['id'] for c in nb['cells']]
if len(ids)!=len(set(ids)):raise RuntimeError('duplicate cell IDs')
ns={'__name__':'__notebook__'};count=0
for cell in nb['cells']:
    if cell['cell_type']!='code':continue
    count+=1;out=io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(compile(''.join(cell['source']),'<cell-'+cell['id']+'>','exec'),ns)
    cell['execution_count']=count
    cell['outputs']=[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]
    print('cell',count,cell['id']);print(out.getvalue(),end='')
path.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('Executed',count,'code cells using standard-library exec; NOT a Jupyter kernel.')
