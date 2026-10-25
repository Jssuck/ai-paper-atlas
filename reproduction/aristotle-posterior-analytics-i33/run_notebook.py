"""Execute the plain-Python cells in tutorial.ipynb, without a Jupyter kernel.

This standard-library fallback supports these cells only: no magics, display
protocol, widgets, kernel semantics or rich output. Exceptions fail the run.
"""
import contextlib
import io
import json
from pathlib import Path


def main():
    path = Path(__file__).with_name('tutorial.ipynb')
    nb = json.loads(path.read_text(encoding='utf-8'))
    namespace = {'__name__': '__notebook__'}
    count = 0
    for cell in nb['cells']:
        if cell['cell_type'] != 'code':
            continue
        count += 1
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            exec(compile(''.join(cell['source']), f'notebook-cell-{count}', 'exec'), namespace)
        cell['execution_count'] = count
        cell['outputs'] = [{'output_type': 'stream', 'name': 'stdout',
                            'text': stream.getvalue().splitlines(keepends=True)}] if stream.getvalue() else []
    nb['metadata']['execution_method'] = 'CPython standard-library exec; not a Jupyter kernel'
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Executed {count} plain-Python cells successfully (stdlib exec, no Jupyter kernel).')

if __name__ == '__main__':
    main()
