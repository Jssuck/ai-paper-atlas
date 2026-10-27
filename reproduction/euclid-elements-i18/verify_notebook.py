"""Truthful plain-Python cell executor. This is NOT a Jupyter kernel runner."""
import contextlib
import io
import json
import os
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
path = ROOT / 'teaching.zh-CN.ipynb'
notebook = json.loads(path.read_text())
if notebook.get('nbformat') != 4 or not isinstance(notebook.get('cells'), list):
    raise ValueError('unsupported notebook structure')
namespace = {'__name__': '__notebook__'}
count = 0
previous_cwd = Path.cwd()
try:
    os.chdir(ROOT)
    for index, cell in enumerate(notebook['cells']):
        if cell['cell_type'] != 'code':
            continue
        count += 1
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exec(compile(''.join(cell['source']), f'<notebook-cell-{index}>', 'exec'), namespace)
        cell['execution_count'] = count
        cell['outputs'] = []
        for name, stream in (('stdout', stdout), ('stderr', stderr)):
            if stream.getvalue():
                cell['outputs'].append({'output_type': 'stream', 'name': name,
                                        'text': stream.getvalue().splitlines(keepends=True)})
finally:
    os.chdir(previous_cwd)
notebook['metadata']['language_info']['version'] = platform.python_version()
notebook['metadata']['execution_provenance'] = {
    'method': 'Python standard-library compile/exec, sequential shared namespace',
    'jupyter_kernel_used': False,
    'browser_render_verified': False,
    'python_version': platform.python_version(),
    'code_cells_executed': count,
}
path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': 'passed', 'code_cells_executed': count,
                  'executor': 'compile/exec shared namespace', 'jupyter_kernel_used': False,
                  'browser_render_verified': False}, indent=2))
