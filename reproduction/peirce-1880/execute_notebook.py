"""Execute this tutorial's plain-Python cells without installing Jupyter.

This is NOT a Jupyter kernel. Cells execute in one fresh shared Python globals
mapping, in document order. It captures stdout/stderr only; rich display,
magics, widgets, shell escapes and asynchronous notebook code are unsupported.
Run only notebooks you trust: executing notebook cells runs arbitrary Python.
"""
import argparse
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import traceback


def execute(path):
    path = Path(path).resolve()
    doc = json.loads(path.read_text(encoding='utf-8'))
    if doc.get('nbformat') != 4:
        raise ValueError('Only nbformat 4 is supported')
    for cell in doc['cells']:
        if cell['cell_type'] == 'code':
            cell['execution_count'], cell['outputs'] = None, []
    doc['metadata'].pop('execution_note', None)
    namespace = {'__name__': '__notebook__'}
    count = 0
    previous = Path.cwd()
    sys.path.insert(0, str(path.parent))
    try:
        os.chdir(path.parent)
        for cell in doc['cells']:
            if cell['cell_type'] != 'code':
                continue
            count += 1
            source = ''.join(cell['source'])
            cell['execution_count'], cell['outputs'] = count, []
            out, err = io.StringIO(), io.StringIO()
            try:
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    exec(compile(source, f'notebook-cell-{count}', 'exec'), namespace)
            except BaseException as exc:
                cell['outputs'].append({'output_type': 'error', 'ename': type(exc).__name__,
                                        'evalue': str(exc), 'traceback': traceback.format_exc().splitlines()})
                raise
            finally:
                for name, text in (('stdout', out.getvalue()), ('stderr', err.getvalue())):
                    if text:
                        cell['outputs'].append({'output_type': 'stream', 'name': name,
                                                'text': text.splitlines(keepends=True)})
        doc['metadata']['execution_note'] = (
            'Executed top-to-bottom by execute_notebook.py using CPython exec in one fresh '
            'shared globals mapping; not a Jupyter kernel. All code cells completed.')
    finally:
        os.chdir(previous)
        sys.path.pop(0)
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('notebook', nargs='?', default='tutorial.ipynb')
    args = parser.parse_args()
    n = execute(args.notebook)
    print(f'Executed {n} code cells successfully, in order, using shared-namespace CPython exec (not a Jupyter kernel).')
