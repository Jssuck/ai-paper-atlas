"""Run only this trusted pure-Python notebook; stdlib exec, not a Jupyter kernel."""
from pathlib import Path
import contextlib
import io
import json


def execute():
    p = Path(__file__).with_name('i32_teaching.ipynb')
    before = p.read_text(encoding='utf-8')
    doc = json.loads(before)
    if doc['nbformat'] != 4 or doc['nbformat_minor'] != 5:
        raise ValueError('Expected notebook format 4.5')
    ids = [c['id'] for c in doc['cells']]
    if len(ids) != len(set(ids)):
        raise ValueError('Cell IDs must be unique')
    namespace = {'__name__': '__notebook__'}
    count = 0
    for cell in doc['cells']:
        if cell['cell_type'] not in ['markdown', 'code'] or not isinstance(cell['source'], list):
            raise ValueError('Unexpected cell structure')
        if cell['cell_type'] != 'code':
            continue
        count += 1
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture):
            exec(compile(''.join(cell['source']), f'cell-{count}', 'exec'), namespace)
        cell['execution_count'] = count
        cell['outputs'] = [{'output_type': 'stream', 'name': 'stdout',
                            'text': capture.getvalue().splitlines(keepends=True)}]
    after = json.dumps(doc, ensure_ascii=False, indent=2) + '\n'
    p.write_text(after, encoding='utf-8')
    print(json.dumps({'executed_cells': count, 'byte_identical_to_previous': before == after,
                      'method': 'fresh Python process; stdlib exec, not Jupyter kernel'}, ensure_ascii=False))

if __name__ == '__main__': execute()
