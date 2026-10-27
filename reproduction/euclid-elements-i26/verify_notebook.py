"""Sequential real code-cell execution, explicitly not Jupyter kernel validation."""
import contextlib,io,json
from pathlib import Path
nb=json.loads(Path('teaching.zh-CN.ipynb').read_text()); ns={'__name__':'__notebook__'}; records=[]
for cell in nb['cells']:
    if cell['cell_type']!='code':continue
    out=io.StringIO(); n=len(records)+1
    with contextlib.redirect_stdout(out):exec(compile(''.join(cell['source']),f'cell-{n}','exec'),ns)
    output=out.getvalue();cell['execution_count']=n
    cell['outputs']=[{'output_type':'stream','name':'stdout','text':output.splitlines(True)}]
    records.append({'cell':n,'completed':True,'stdout':output})
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'execution':'standard-library compile/exec in shared namespace; not Jupyter kernel or nbformat validation','cells_executed':len(records),'cells':records},ensure_ascii=False,indent=2))
