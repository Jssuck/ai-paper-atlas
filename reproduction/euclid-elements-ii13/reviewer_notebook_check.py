"""Read-only replay, comparing saved output rather than overwriting it."""
import contextlib, io, json
from pathlib import Path
nb=json.loads(Path('teaching.zh-CN.ipynb').read_text())
if (nb['nbformat'],nb['nbformat_minor']) != (4,5): raise AssertionError('format')
ns={'__name__':'__independent_notebook__'}
n=0
for cell in nb['cells']:
    if cell['cell_type']!='code': continue
    n+=1
    if cell['execution_count']!=n: raise AssertionError('execution count')
    out=io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(compile(''.join(cell['source']),f'independent-cell-{n}','exec'),ns)
    expected=''
    for item in cell['outputs']:
        if item['output_type']!='stream' or item['name']!='stdout': raise AssertionError('unexpected output')
        expected+=''.join(item['text'])
    if out.getvalue()!=expected: raise AssertionError(f'output mismatch {n}')
    print(f'CELL {n}: saved output equals fresh compile/exec output')
if n!=5: raise AssertionError('expected five cells')
print('PASS: five read-only cell replays; no Jupyter kernel started.')
