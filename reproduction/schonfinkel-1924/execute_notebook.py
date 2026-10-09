"""Execute this trusted tutorial's ordinary Python cells using only stdlib.

This is not a Jupyter kernel: no magics, rich display, async or input support.
The notebook uses print and assertions only. Never use on untrusted notebooks.
"""
import contextlib
import io
import json
import os
from pathlib import Path
import platform
import sys
import traceback


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else 'tutorial.ipynb').resolve()
    notebook = json.loads(path.read_text(encoding='utf-8'))
    if notebook.get('nbformat') != 4:
        raise ValueError('Only nbformat 4 supported')
    os.chdir(path.parent)
    sys.path.insert(0,str(path.parent))
    scope = {'__name__':'__main__'}
    executed = 0
    for index, cell in enumerate(notebook['cells']):
        if cell['cell_type'] != 'code':
            continue
        executed += 1
        stdout, stderr = io.StringIO(), io.StringIO()
        cell['execution_count'] = executed
        cell['outputs'] = []
        error = None
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exec(compile(''.join(cell['source']),f'{path.name}:cell-{index+1}','exec'),scope)
        except Exception as exc:
            error = exc
            cell['outputs'].append({'output_type':'error','ename':type(exc).__name__,
                                    'evalue':str(exc),'traceback':traceback.format_exc().splitlines()})
        for name, stream in [('stdout',stdout),('stderr',stderr)]:
            if stream.getvalue():
                cell['outputs'].append({'output_type':'stream','name':name,
                                        'text':stream.getvalue().splitlines(keepends=True)})
        print(f'Cell {executed}: {"FAILED" if error else "OK"}')
        if stdout.getvalue():
            print(stdout.getvalue(),end='')
        if stderr.getvalue():
            print(stderr.getvalue(),end='')
        if error:
            path.write_text(json.dumps(notebook,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            raise error
    notebook['metadata']['execution_method'] = {
        'method':'stdlib compile/exec, sequential shared namespace, captured streams',
        'runner':'execute_notebook.py', 'python':platform.python_version(),
        'jupyter_kernel_used':False, 'executed_code_cells':executed}
    path.write_text(json.dumps(notebook,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Executed {executed} Python cells successfully; outputs saved to {path.name}.')


if __name__ == '__main__':
    main()
