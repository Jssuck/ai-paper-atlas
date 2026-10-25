"""Execute plain Python notebook cells sequentially, not through a Jupyter kernel."""
import contextlib
import io
import json
from pathlib import Path


def execute(path):
    notebook = json.loads(Path(path).read_text(encoding='utf-8'))
    namespace = {'__name__': '__main__'}
    count = 0
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        count += 1
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(compile(''.join(cell['source']), f'cell-{count}', 'exec'), namespace)
        cell['execution_count'] = count
        cell['outputs'] = [{'output_type': 'stream', 'name': 'stdout', 'text': output.getvalue().splitlines(keepends=True)}] if output.getvalue() else []
    notebook['metadata']['execution_method'] = 'Python standard-library sequential exec, fresh process; not a Jupyter kernel'
    Path(path).write_text(json.dumps(notebook, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'Executed {count} code cells sequentially in a fresh Python process; not a Jupyter kernel.')
    return count


if __name__ == '__main__':
    execute(Path(__file__).with_name('i24_teaching.ipynb'))
