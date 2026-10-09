"""Execute trusted plain-Python notebook cells with stdlib only.

This is CPython exec, NOT a Jupyter kernel. No magics, shell escapes, rich
outputs, widgets or top-level async. All cells share a fresh globals dictionary.
Running a notebook runs arbitrary code; inspect an unfamiliar notebook first.
"""
import contextlib
import io
import json
import os
from pathlib import Path
import sys


def execute(filename):
    path=Path(filename).resolve()
    doc=json.loads(path.read_text(encoding='utf-8'))
    if doc.get('nbformat') != 4: raise ValueError('Need nbformat 4')
    state={'__name__':'__notebook__'}
    count=0
    original=Path.cwd()
    sys.path.insert(0,str(path.parent))
    try:
        os.chdir(path.parent)
        for cell in doc['cells']:
            if cell['cell_type'] != 'code': continue
            count+=1
            capture=io.StringIO()
            cell['outputs']=[]
            cell['execution_count']=count
            with contextlib.redirect_stdout(capture),contextlib.redirect_stderr(capture):
                exec(compile(''.join(cell['source']),f'notebook-cell-{count}','exec'),state)
            if capture.getvalue():
                cell['outputs']=[{'output_type':'stream','name':'stdout',
                                  'text':capture.getvalue().splitlines(keepends=True)}]
    finally:
        os.chdir(original)
        sys.path.pop(0)
    doc['metadata']['execution_note']='All plain-Python cells executed sequentially in a fresh shared globals dictionary using CPython exec, not a Jupyter kernel.'
    doc['metadata']['language_info']['version']=sys.version.split()[0]
    path.write_text(json.dumps(doc,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
    return count


if __name__=='__main__':
    n=execute(sys.argv[1] if len(sys.argv)>1 else 'tutorial.ipynb')
    print(f'Executed {n} code cells successfully, top-to-bottom, using CPython exec (not a Jupyter kernel).')
