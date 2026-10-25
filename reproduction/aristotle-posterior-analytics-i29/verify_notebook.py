"""Execute trusted local teaching cells in order, using stdlib, NOT a Jupyter kernel."""
from pathlib import Path
import contextlib, io, json

def execute():
    p=Path(__file__).with_name('i29_teaching.ipynb')
    doc=json.loads(p.read_text())
    namespace={'__name__':'__notebook__'}
    number=0
    for c in doc['cells']:
        if c['cell_type']!='code': continue
        number+=1
        out=io.StringIO()
        with contextlib.redirect_stdout(out): exec(compile(''.join(c['source']),f'cell-{number}','exec'),namespace)
        c['execution_count']=number
        c['outputs']=[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(keepends=True)}]
    encoded=json.dumps(doc,ensure_ascii=False,indent=2)+'\n'
    previous=p.read_text()
    p.write_text(encoded)
    print(json.dumps({'code_cells_executed':number,'byte_identical_to_previous':previous==encoded,
                      'method':'Python standard-library exec in a new process; not Jupyter kernel'},ensure_ascii=False))
if __name__=='__main__': execute()
