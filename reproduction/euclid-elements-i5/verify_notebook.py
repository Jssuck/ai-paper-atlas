"""Execute stored notebook code sequentially with stdlib, NOT a Jupyter kernel."""
import contextlib, io, json
from pathlib import Path


def execute():
    path=Path('teaching.zh-CN.ipynb')
    doc=json.loads(path.read_text())
    scope={'__name__':'__notebook__'}
    count=0
    for cell in doc['cells']:
        if cell['cell_type']!='code': continue
        count+=1
        capture=io.StringIO()
        with contextlib.redirect_stdout(capture):
            exec(compile(''.join(cell['source']),f'<cell {count}>','exec'),scope)
        cell['execution_count']=count
        cell['outputs']=[{'output_type':'stream','name':'stdout','text':capture.getvalue().splitlines(True)}] if capture.getvalue() else []
    path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
    result={'code_cells_executed':count,'execution':'stdlib compile/exec in one fresh shared namespace',
            'jupyter_kernel':False,'full_nbformat_validation':False,'success':True}
    Path('notebook-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__': execute()
