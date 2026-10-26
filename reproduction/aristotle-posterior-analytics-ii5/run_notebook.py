"""Execute plain Python cells in order with stdlib exec; NOT a Jupyter kernel."""
import contextlib
import io
import json
from pathlib import Path


def main():
    path = Path(__file__).with_name('tutorial.ipynb')
    nb = json.loads(path.read_text(encoding='utf-8'))
    scope = {'__name__': '__notebook__'}
    number = 0
    for cell in nb['cells']:
        if cell['cell_type'] != 'code':
            continue
        number += 1
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(compile(''.join(cell['source']), 'tutorial.ipynb:cell%d' % number, 'exec'), scope)
        output = buf.getvalue()
        cell['execution_count'] = number
        cell['outputs'] = [{'output_type': 'stream', 'name': 'stdout', 'text': output.splitlines(True)}] if output else []
        print('cell', number, 'OK')
        print(output, end='')
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Executed', number, 'plain Python cells with stdlib exec; NOT a Jupyter kernel.')

if __name__ == '__main__': main()
