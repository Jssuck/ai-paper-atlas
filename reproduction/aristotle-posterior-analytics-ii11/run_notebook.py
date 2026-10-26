"""Execute plain Python cells sequentially; this is NOT a Jupyter kernel."""
import contextlib,io,json
from pathlib import Path
root=Path(__file__).resolve().parent
p=root/'tutorial.ipynb'
nb=json.loads(p.read_text()); ids=[c['id'] for c in nb['cells']]
if len(ids)!=len(set(ids)):raise RuntimeError('duplicate cell ids')
ns={'__name__':'__notebook__'}; count=0
for cell in nb['cells']:
    if cell['cell_type']!='code':continue
    count+=1; stream=io.StringIO()
    with contextlib.redirect_stdout(stream):exec(compile(''.join(cell['source']),'<notebook-cell>','exec'),ns)
    cell['execution_count']=count
    cell['outputs']=[{'output_type':'stream','name':'stdout','text':stream.getvalue().splitlines(True)}] if stream.getvalue() else []
    print('CELL',count);print(stream.getvalue(),end='')
nb['metadata']['execution_method']='Python standard-library sequential exec; not Jupyter kernel'
p.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('Executed',count,'code cells via standard-library exec; NOT Jupyter kernel.')
