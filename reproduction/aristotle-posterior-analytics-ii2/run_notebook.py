"""Run this trusted pure-Python notebook sequentially; not a Jupyter kernel."""
import contextlib
import io
import json
from pathlib import Path


def main():
    path = Path(__file__).with_name('tutorial.ipynb')
    notebook = json.loads(path.read_text(encoding='utf-8'))
    namespace = {'__name__': '__notebook__'}
    count = 0
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        count += 1
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            exec(compile(''.join(cell['source']), f'notebook-cell-{count}', 'exec'), namespace)
        cell['execution_count'] = count
        value = out.getvalue()
        cell['outputs'] = ([{'output_type': 'stream', 'name': 'stdout',
                            'text': value.splitlines(True)}] if value else [])
        print(f'CELL {count}\n{value}', end='')
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Executed {count} code cells with CPython exec; not a Jupyter kernel.')


if __name__ == '__main__':
    main()
