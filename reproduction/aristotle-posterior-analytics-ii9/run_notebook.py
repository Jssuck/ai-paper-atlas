"""Run plain Python notebook cells sequentially, not with a Jupyter kernel."""
import contextlib,io,json
from pathlib import Path
p=Path('tutorial.ipynb'); nb=json.loads(p.read_text()); ns={'__name__':'__notebook__'}; count=0
for cell in nb['cells']:
    if cell['cell_type']!='code':continue
    count+=1; output=io.StringIO()
    with contextlib.redirect_stdout(output):exec(compile(''.join(cell['source']),f'cell-{count}','exec'),ns)
    value=output.getvalue();cell['execution_count']=count
    cell['outputs']=[{'output_type':'stream','name':'stdout','text':value.splitlines(True)}] if value else []
    print(f'CELL {count}\n{value}',end='')
nb['metadata']['execution_note']='Python standard-library exec in cell order; NOT a Jupyter kernel.'
p.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print(f'Executed {count} cells by standard-library exec; NOT a Jupyter kernel.')
