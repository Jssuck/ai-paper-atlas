"""Run Python-only notebook cells with stdlib exec; NOT a Jupyter kernel."""
import contextlib
import io
import json
from pathlib import Path


def run():
    path=Path(__file__).with_name('tutorial.ipynb')
    nb=json.loads(path.read_text(encoding='utf-8'))
    if nb['nbformat'] != 4 or nb['nbformat_minor'] != 5:
        raise ValueError('unexpected notebook version')
    namespace={'__name__':'__notebook__'}
    count=0
    for cell in nb['cells']:
        if not isinstance(cell.get('id'),str) or not isinstance(cell.get('source'),list):
            raise ValueError('invalid cell structure')
        if cell['cell_type'] != 'code': continue
        count += 1
        stream=io.StringIO()
        with contextlib.redirect_stdout(stream):
            exec(compile(''.join(cell['source']),f'notebook-cell-{count}','exec'),namespace)
        output=stream.getvalue()
        cell['execution_count']=count
        cell['outputs']=[{'output_type':'stream','name':'stdout','text':output.splitlines(keepends=True)}] if output else []
        print(f'CELL {count}\n{output}',end='')
    path.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Executed {count} code cells using CPython stdlib exec, NOT Jupyter kernel.')

if __name__ == '__main__': run()
