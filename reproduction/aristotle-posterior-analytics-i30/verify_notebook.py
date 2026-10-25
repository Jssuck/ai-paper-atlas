"""Run trusted local notebook code in order using stdlib exec, NOT a Jupyter kernel."""
from pathlib import Path
import contextlib,io,json

def execute():
    path=Path(__file__).with_name('i30_teaching.ipynb')
    previous=path.read_text(); doc=json.loads(previous)
    namespace={'__name__':'__notebook__'}; count=0
    for cell in doc['cells']:
        if cell['cell_type']!='code': continue
        count+=1; out=io.StringIO()
        with contextlib.redirect_stdout(out):
            exec(compile(''.join(cell['source']),f'cell-{count}','exec'),namespace)
        cell['execution_count']=count
        cell['outputs']=[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(keepends=True)}]
    encoded=json.dumps(doc,ensure_ascii=False,indent=2)+'\n'; path.write_text(encoded)
    print(json.dumps({'code_cells_executed':count,'byte_identical_to_previous':previous==encoded,
                     'method':'Python stdlib exec in fresh process; not a Jupyter kernel'},ensure_ascii=False))
if __name__=='__main__':execute()
