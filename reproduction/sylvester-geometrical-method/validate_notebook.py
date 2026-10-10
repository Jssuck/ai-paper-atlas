"""Limited nbformat-4 structural checks and ordinary CPython execution.

This is deliberately not presented as full nbformat JSON Schema validation or
execution through a Jupyter kernel. Only plain Python code cells are supported.
"""
from __future__ import annotations
import argparse
import ast
import contextlib
import io
import json
import os
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def validate(nb):
    if nb.get('nbformat')!=4 or not isinstance(nb.get('cells'),list):
        raise ValueError('expected a nbformat 4 notebook with cells')
    if not isinstance(nb.get('metadata'),dict):raise ValueError('missing notebook metadata')
    ids=set()
    code_count=0
    for index,cell in enumerate(nb['cells']):
        kind=cell.get('cell_type')
        if kind not in ('markdown','code'):raise ValueError(f'unsupported cell type at {index}')
        if not isinstance(cell.get('metadata'),dict):raise ValueError('missing cell metadata')
        if not isinstance(cell.get('source'),list) or not all(isinstance(s,str) for s in cell['source']):
            raise ValueError(f'cell {index}: source must be a list of strings')
        cell_id=cell.get('id')
        if not isinstance(cell_id,str) or cell_id in ids or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',cell_id):
            raise ValueError(f'cell {index}: invalid or duplicate cell ID')
        ids.add(cell_id)
        source=''.join(cell['source'])
        if kind=='code':
            code_count+=1
            ast.parse(source,filename=f'tutorial.ipynb:cell-{index}')
            if not isinstance(cell.get('outputs'),list):raise ValueError('missing output list')
            count=cell.get('execution_count')
            if count is not None and (not isinstance(count,int) or count<1):raise ValueError('bad execution count')
            for output in cell['outputs']:
                if output.get('output_type')=='error':raise ValueError('notebook includes an error output')
        else:
            for target in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',source):
                if '://' not in target and not (ROOT/target).is_file():
                    raise ValueError(f'missing local figure: {target}')
    return code_count


def execute(nb):
    scope={'__name__':'__notebook__'}
    execution_count=0
    old_cwd=Path.cwd()
    sys.path.insert(0,str(ROOT))
    try:
        os.chdir(ROOT)
        for index,cell in enumerate(nb['cells']):
            if cell['cell_type']!='code':continue
            execution_count+=1
            stdout,stderr=io.StringIO(),io.StringIO()
            with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
                exec(compile(''.join(cell['source']),f'tutorial.ipynb:cell-{index}','exec'),scope)
            outputs=[]
            for name,stream in [('stdout',stdout),('stderr',stderr)]:
                value=stream.getvalue()
                if value:outputs.append({'output_type':'stream','name':name,'text':value.splitlines(keepends=True)})
            cell['outputs']=outputs
            cell['execution_count']=execution_count
    finally:
        os.chdir(old_cwd)
        sys.path.pop(0)
    nb['metadata']['reproduction']['execution']='Sequential ordinary CPython exec; not a Jupyter kernel or nbclient run'
    nb['metadata']['reproduction']['validation']='Basic nbformat-4 structure, code AST/compilation, local figure links; not full official JSON Schema'
    nb['metadata']['language_info']['version']='.'.join(map(str,sys.version_info[:3]))
    return execution_count


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--execute',action='store_true')
    args=parser.parse_args()
    path=ROOT/'tutorial.ipynb'
    nb=json.loads(path.read_text(encoding='utf-8'))
    code_count=validate(nb)
    print(f'Basic notebook structure and AST: {len(nb["cells"])} cells, {code_count} code cells; PASS')
    print('Local figure links: PASS')
    if args.execute:
        count=execute(nb)
        validate(nb)
        path.write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
        print(f'Ordinary CPython sequential execution: {count}/{code_count} code cells; PASS')
        print('No Jupyter kernel was launched. No official nbformat schema validator was used.')
    print('Saved error outputs: 0')


if __name__=='__main__':main()
