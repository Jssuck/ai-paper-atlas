"""Compile/exec/replay, explicitly NOT a Jupyter kernel execution."""
import contextlib,io,json
from pathlib import Path
p=Path('teaching.zh-CN.ipynb');n=json.loads(p.read_text());scope={};count=0
for cell in n['cells']:
 if cell['cell_type']!='code':continue
 count+=1;stream=io.StringIO()
 with contextlib.redirect_stdout(stream):exec(compile(''.join(cell['source']),'notebook-cell-'+str(count),'exec'),scope)
 text=stream.getvalue();outputs=[dict(output_type='stream',name='stdout',text=text.splitlines(True))] if text else []
 if cell['outputs'] and cell['outputs']!=outputs:raise RuntimeError('saved output mismatch')
 cell['outputs']=outputs;cell['execution_count']=count
p.write_text(json.dumps(n,ensure_ascii=False,indent=2)+'\n')
print('PASS',count,'code cells; compile/exec and saved-output replay; NOT kernel execution')
