"""Read-only independent replay of this project's trusted plain-Python notebook.

This is a second CPython executor, not a Jupyter-kernel or nbformat validation.
Every cell's actual captured output is compared to the delivered saved output.
"""
import contextlib
import io
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def main():
    notebook = json.loads((ROOT / 'tutorial.ipynb').read_text(encoding='utf-8'))
    scope = {'__name__': '__independent_notebook__'}
    checked = 0
    seen = set()
    for cell in notebook['cells']:
        assert cell['id'] not in seen, 'Duplicate cell ID'
        seen.add(cell['id'])
        if cell['cell_type'] != 'code':
            continue
        checked += 1
        assert cell['execution_count'] == checked
        assert all(output['output_type'] == 'stream' for output in cell['outputs'])
        expected = ''.join(''.join(output['text']) for output in cell['outputs'])
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture), contextlib.redirect_stderr(capture):
            exec(compile(''.join(cell['source']), 'independent-cell-' + str(checked), 'exec'), scope)
        assert capture.getvalue() == expected, 'Saved output mismatch at cell ' + str(checked)
        print('PASS', cell['id'], 'execution', checked, 'saved output matches replay')
    assert checked == 22
    print(json.dumps({'status': 'PASS', 'total_cells': len(notebook['cells']),
                      'code_cells_replayed': checked, 'exact_saved_output_matches': checked,
                      'notebook_modified': False,
                      'execution': 'fresh shared Python namespace; CPython exec; not Jupyter'}, indent=2))


if __name__ == '__main__':
    main()
