"""Independent Fraction expectations; exercise demo only in a child process."""

import ast
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def check(condition, label):
    if not condition:
        raise AssertionError(label)


def run(*arguments, display=True):
    completed = subprocess.run([sys.executable, *arguments], cwd=ROOT,
                               text=True, capture_output=True)
    if display:
        print('$ python3 ' + ' '.join(arguments))
        print(completed.stdout + completed.stderr, end='')
        print('exit_code=' + str(completed.returncode))
    check(completed.returncode == 0, 'command failed: ' + arguments[0])
    return completed.stdout


def pair(item):
    check(set(item) == {'real', 'imag'}, 'pair schema')
    check(all(isinstance(x, str) for x in item.values()), 'rational JSON strings')
    return F(item['real']), F(item['imag'])


def main():
    print('Independent exact-rational review')
    print('recorded_at_utc=' + datetime.now(timezone.utc).isoformat())
    print('python_version=' + sys.version.split()[0])
    originals = {name: (ROOT / name).read_bytes()
                 for name in ['demo.py', 'test_demo.py', 'reproduce.py', 'results.json']}
    run('-m', 'unittest', '-v', 'test_demo')
    run('reproduce.py')
    for name, original in originals.items():
        check((ROOT / name).read_bytes() == original, name + ' changed')
    print('PASS: source and results.json unchanged byte-for-byte after reproduction')

    test_tree = ast.parse((ROOT / 'test_demo.py').read_text())
    count = sum(isinstance(node, ast.FunctionDef) and node.name.startswith('test_')
                for node in ast.walk(test_tree))
    environment = json.loads((ROOT / 'environment.json').read_text())
    check(count == environment['test_method_count'] == 8, 'test method count')
    print('PASS: discovered 8 test methods; environment metadata agrees')

    # This child produces actual implementation values only. Expected values below
    # use Fraction scalar arithmetic and do not import demo or its operations.
    actuals = json.loads(run('-c', '''
import json
from fractions import Fraction as F
from itertools import product
from demo import Pair, remark, unrestricted_remark
values = [F(-2), F(-1,2), F(0), F(1,2), F(2)]
rows = []
for a,b,f,c in product(values, repeat=4):
    p,q = Pair(a,b),Pair(f,c)
    r = remark(a,b,f,c)
    rows.append({
        'inputs': list(map(str,(a,b,f,c))),
        'remark': r.as_json(), 'is_real': r.is_real,
        'add': (p+q).as_json(), 'sub': (p-q).as_json(),
        'mul': (p*q).as_json(),
        'shifted': remark(a+F(1,3),b-F(7,5),f-F(1,3),c-F(7,5)).as_json(),
        'complex': unrestricted_remark(p,a,q,f).as_json()})
rejections=[]
for invalid in [0.1, float('inf'), float('nan'), True, False, None, 1j, [], {}]:
    for component in ['real','imag']:
        try:
            Pair(**{component: invalid})
        except TypeError:
            rejections.append(True)
        else:
            rejections.append(False)
edge_inputs = [('1/3','2/7','2/3','5/7'),
               (str(10**100),'1/100000000000000000003',str(-10**100),
                '1/100000000000000000019')]
edges = [{'inputs': x, 'value': remark(*x).as_json()} for x in edge_inputs]
print(json.dumps({'rows': rows, 'rejections': rejections, 'edges': edges}))
''', display=False))
    rows = actuals['rows']
    grid = [F(-2), F(-1, 2), F(0), F(1, 2), F(2)]
    check(len(rows) == 625 == environment['real_coefficient_grid_cases'], 'grid count')
    expected_inputs = list(product(grid, repeat=4))
    counts = {'real': 0, 'positive_imag': 0, 'negative_imag': 0}
    for row, expected_input in zip(rows, expected_inputs):
        a, b, f, c = map(F, row['inputs'])
        check((a,b,f,c) == expected_input, 'grid order and coverage')
        check(pair(row['remark']) == (a+f,b-c), 'remark identity')
        check(row['is_real'] == (b == c), 'real iff b=c')
        check(pair(row['add']) == (a+f,b+c), 'addition')
        check(pair(row['sub']) == (a-f,b-c), 'subtraction')
        check(pair(row['mul']) == (a*f-b*c,a*c+b*f), 'multiplication')
        check(pair(row['shifted']) == (a+f,b-c), 'decomposition invariance')
        check(pair(row['complex']) == (a+f,b+c+a-f), 'complex coefficient identity')
        counts['real' if b == c else 'positive_imag' if b > c else 'negative_imag'] += 1
    check(counts == {'real':125,'positive_imag':250,'negative_imag':250}, 'grid partition')
    print('PASS: independent 625-case grid; real=125, positive imaginary=250, negative imaginary=250')
    print('PASS: independent scalar formulas for 1875 pair operations (625 each: add, subtract, multiply)')
    print('PASS: 625 decomposition shifts and 625 complex-a/f identities')
    check(len(actuals['rejections']) == 18 and all(actuals['rejections']), 'input rejection')
    print('PASS: 18 TypeError checks for unsupported real/imag inputs, including float and bool')
    for edge in actuals['edges']:
        a,b,f,c = map(F, edge['inputs'])
        check(pair(edge['value']) == (a+f,b-c), 'fraction or large-integer edge')
    print('PASS: 2 precision edge cases with non-dyadic fractions and 101-digit integers')

    data = json.loads((ROOT / 'results.json').read_text())
    for item in data['signed_real_differences']:
        check(F(item['difference']) == F(item['left'])-F(item['right']), 'signed difference')
    for section in ['imaginary_difference_cases', 'nonunique_decompositions']:
        for item in data[section]:
            a,b,f,c = (F(item[key]) for key in ['a','b','f','c'])
            check(pair(item['value']) == (a+f,b-c), section)
            if 'is_real' in item:
                check(item['is_real'] == (b==c) == item['b_equals_c'], 'example flags')
    check([pair(x['value']) for x in data['nonunique_decompositions']] == [(F(5),F(2))]*2,
          'two decompositions agree')
    section = data['nonreal_intermediates_real_result']
    (a,b),(f,c) = map(pair, section['sum_operands'])
    check(b != 0 and c != 0 and pair(section['sum']) == (a+f,b+c) == (F(5),F(0)), 'cancelling sum')
    (a,b),(f,c) = map(pair, section['product_operands'])
    check(b != 0 and c != 0 and pair(section['product']) == (a*f-b*c,a*c+b*f) == (F(2),F(0)), 'real product')
    roots = data['positive_length_constraint']
    values = list(map(F, roots['real_roots']))
    check(set(values) == {F(1),F(-4)}, 'complete roots of factored quadratic')
    residuals = [x*x+3*x-4 for x in values]
    check(residuals == list(map(F, roots['residuals'])) == [F(0),F(0)], 'root residuals')
    check(list(map(F, roots['admissible_roots'])) == [x for x in values if x>0] == [F(1)], 'positive admissibility')
    check(list(map(F, roots['excluded_real_roots'])) == [x for x in values if x<=0] == [F(-4)], 'excluded real root')
    for item in data['complex_a_f_caveat']:
        ar,ai = pair(item['a']); fr,fi = pair(item['f'])
        b,c = F(item['b']),F(item['c'])
        expected = (ar+fr,ai+fi+b-c)
        check(pair(item['value']) == expected, 'boundary example value')
        check(item['is_real'] == (expected[1]==0) and item['b_equals_c'] == (b==c), 'boundary flags')
    check([(x['b_equals_c'],x['is_real']) for x in data['complex_a_f_caveat']] == [(True,False),(False,True)], 'both failed implications')
    print('PASS: all published numerical sections, root admissibility and both boundary counterexamples')
    for name in ['demo.py', 'test_demo.py', 'reproduce.py', 'results.json']:
        print('sha256 ' + name + ' ' + hashlib.sha256((ROOT/name).read_bytes()).hexdigest())
    print('RESULT: all checks passed; finite checks supplement, but do not replace, the algebraic proof.')


if __name__ == '__main__':
    main()
