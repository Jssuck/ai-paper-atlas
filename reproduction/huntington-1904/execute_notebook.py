"""Execute this pure-Python tutorial top-to-bottom; NOT a Jupyter kernel.

Only Python's standard library is used. Intended for trusted local teaching
notebooks, not for running untrusted uploaded code. Each cell shares one fresh
namespace. Stream outputs are persisted in standard nbformat form. The tutorial
uses explicit print() and no display, magics, or implicit last-expression output.
"""
import argparse
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import sys
import time
import traceback


def execute(path):
    path = path.resolve()
    notebook = json.loads(path.read_text(encoding='utf-8'))
    if notebook.get('nbformat') != 4:
        raise ValueError('Expected nbformat 4')
    namespace = {'__name__': '__main__'}
    count = 0
    failure = None
    started = time.perf_counter()
    os.chdir(path.parent)
    sys.path.insert(0, str(path.parent))
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        count += 1
        cell['outputs'] = []
        cell['execution_count'] = count
        stdout, stderr = io.StringIO(), io.StringIO()
        try:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exec(compile(''.join(cell['source']), f'{path.name}:cell-{count}', 'exec'), namespace)
        except Exception as error:
            failure = error
            error_output = {'output_type':'error', 'ename':type(error).__name__,
                            'evalue':str(error), 'traceback':traceback.format_exc().splitlines()}
        for name, stream in [('stdout',stdout),('stderr',stderr)]:
            if stream.getvalue():
                cell['outputs'].append({'output_type':'stream','name':name,
                                        'text':stream.getvalue().splitlines(keepends=True)})
        if failure:
            cell['outputs'].append(error_output)
        print(f'Code cell {count}: {"FAILED" if failure else "executed"}; '
              f'{len(stdout.getvalue())} stdout / {len(stderr.getvalue())} stderr characters')
        if failure:
            break
    notebook.setdefault('metadata', {})['execution_provenance'] = {
        'method':'Python stdlib exec, fresh shared namespace, sequential cells; not Jupyter/IPython kernel',
        'python_version':sys.version,
        'timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'code_cells_executed':count,
        'successful':failure is None,
    }
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + '\n',encoding='utf-8')
    print(f'Persisted outputs in {path.name}; runtime {time.perf_counter()-started:.3f}s')
    if failure:
        raise RuntimeError('Notebook execution failed; error output saved') from failure


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('notebook',type=Path)
    execute(parser.parse_args().notebook)
