"""Execute plain Python cells sequentially, not via Jupyter/IPython kernel."""
import contextlib, io, json
from pathlib import Path
p=Path('i25_teaching.ipynb')
nb=json.loads(p.read_text()); namespace={'__name__':'__notebook__'}; count=0
for cell in nb['cells']:
 if cell['cell_type']!='code': continue
 count+=1; stream=io.StringIO()
 with contextlib.redirect_stdout(stream): exec(compile(''.join(cell['source']),f'cell-{count}','exec'),namespace)
 cell['execution_count']=count
 cell['outputs']=[{'output_type':'stream','name':'stdout','text':stream.getvalue().splitlines(True)}]
 print(f'cell {count}: OK')
p.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print(f'{count} cells executed sequentially using Python standard library; no Jupyter kernel validation')
