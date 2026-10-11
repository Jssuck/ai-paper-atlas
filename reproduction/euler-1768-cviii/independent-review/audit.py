#!/usr/bin/env python3
"""Independent deterministic finite oracle. Run from any working directory.
Writes only to independent-review/. Does not import the target's private evaluator.
"""
import hashlib
import itertools
import json
import os
from pathlib import Path
import platform
import random
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from logic import Theory, evaluate
from main import check_payload
from experiments import run

counts = dict(evaluations=0, consequence_comparisons=0, rejected_inputs=0, cli_checks=0)

def universe(names):
    return [dict(zip(sorted(names), r)) for r in itertools.product((False, True), repeat=len(names))]

def mask(expr, rows):
    """Evaluate a whole truth table by independent bit-set algebra."""
    all_bits = (1 << len(rows)) - 1
    if expr is True: return all_bits
    if expr is False: return 0
    if isinstance(expr, str): return sum(1 << i for i, row in enumerate(rows) if row[expr])
    op, *args = expr
    values = [mask(a, rows) for a in args]
    if op == 'not': return all_bits ^ values[0]
    if op == 'and': return values[0] & values[1]
    if op == 'or': return values[0] | values[1]
    if op == 'implies': return (all_bits ^ values[0]) | values[1]
    raise AssertionError(op)

def oracle(names, constraints, worlds, premises, conclusion):
    rows = universe(names)
    full = (1 << len(rows)) - 1
    allowed = full if worlds is None else sum(1 << i for i, row in enumerate(rows) if row in worlds)
    for f in constraints: allowed &= mask(f, rows)
    witnesses = allowed
    for f in premises: witnesses &= mask(f, rows)
    bad = witnesses & (full ^ mask(conclusion, rows))
    warning = ('empty theory: validity is vacuous; no allowed world exists' if not allowed else
               'inconsistent premises in this theory: validity is vacuous' if not witnesses else None)
    return dict(valid=not bad, theory_consistent=bool(allowed), premises_consistent=bool(witnesses),
                allowed_world_count=allowed.bit_count(), premise_world_count=witnesses.bit_count(),
                counterexamples=[r for i, r in enumerate(rows) if bad & (1 << i)], warning=warning)

def compare(names, constraints, worlds, premises, conclusion):
    actual = Theory(names, constraints, worlds).check(premises, conclusion)
    expected = oracle(names, constraints, worlds, premises, conclusion)
    assert actual == expected, (names, constraints, worlds, premises, conclusion, actual, expected)
    counts['consequence_comparisons'] += 1
    return expected

rng = random.Random(1768108)
def nested(leaves, depth):
    if depth == 0 or rng.randrange(4) == 0: return rng.choice(leaves)
    op = rng.choice(('not', 'and', 'or', 'implies'))
    return (op, nested(leaves, depth-1)) if op == 'not' else (op, nested(leaves, depth-1), nested(leaves, depth-1))

leaves = [False, True, 'p', 'q']
small = leaves + [('not', x) for x in leaves] + [(op, x, y) for op in ('and', 'or', 'implies') for x in leaves for y in leaves]
assert len(small) == 56
for f in small:
    rows = universe(['p', 'q'])
    expected = mask(f, rows)
    for i, row in enumerate(rows):
        assert evaluate(f, row) is bool(expected & (1 << i))
        counts['evaluations'] += 1
for p in small:
    for q in small: compare(['q', 'p'], [], None, [p], q)
# Every explicit subset, all depth <=1 conclusions, varied constraints and premises.
rows = universe(['p', 'q'])
for subset in range(16):
    worlds = [r for i, r in enumerate(rows) if subset & (1 << i)]
    worlds = list(reversed(worlds)) + worlds[:1]  # unsorted, sometimes duplicate
    for index, q in enumerate(small):
        for offset in range(8):
            compare(['q', 'p'], [small[(index+offset*7)%56]], worlds,
                    [small[(index*3+offset)%56], small[(index+offset*5)%56]], q)
# Every three-atom world subset with deterministic nested formulas.
leaves3 = [False, True, 'a', 'b', 'c']
complexes = [nested(leaves3, 6) for _ in range(512)]
rows3 = universe(['a','b','c'])
for f in complexes:
    expected = mask(f, rows3)
    for i, row in enumerate(rows3):
        assert evaluate(f, row) is bool(expected & (1 << i))
        counts['evaluations'] += 1
for subset in range(256):
    worlds = [r for i, r in enumerate(rows3) if subset & (1 << i)]
    for j in range(16):
        pos = (subset*17 + j*13) % len(complexes)
        compare(['c','a','b'], [complexes[pos]], worlds,
                [complexes[(pos+1)%512], complexes[(pos+2)%512]], complexes[(pos+3)%512])
for worlds in (None, [], [{}], [{},{}]):
    for premise in ([], [False], [True]):
        for conclusion in (False,True): compare([], [], worlds, premise, conclusion)
compare([f'p{i}' for i in range(12)], [], None, ['p0'], 'p11')
f = 'p'
for _ in range(64): f = ['not', f]
assert evaluate(f, {'p': True}) is True
counts['evaluations'] += 1

def rejects(call):
    try: call()
    except ValueError: counts['rejected_inputs'] += 1
    else: raise AssertionError('invalid input accepted')
rejects(lambda: evaluate(['not', f], {'p': True}))
for atoms in [None, 'p', ['p','p'], [''], ['é'], ['p\n'], ['1p'], [1], ['p'+str(i) for i in range(13)]]:
    rejects(lambda atoms=atoms: Theory(atoms))
for expression in [None, 0, 1, 1.0, {}, [], ['xor','p','p'], ['not'], ['not','p','p'], ['and','p'], ['implies','p','q'], ['and',False,'q']]:
    rejects(lambda expression=expression: evaluate(expression, {'p':False}))
for world in [None, [], {'p':1}, {'p':0}, {'p':None}, {'p':'false'}, {}, {'p':False,'q':True}]:
    rejects(lambda world=world: Theory(['p'], allowed_worlds=[world]))
for field, values in [('constraints',[None,'p',[[]]]), ('allowed_worlds',[{},'p',[{'p':1}]])]:
    for value in values: rejects(lambda field=field,value=value: Theory(['p'], **{field:value}))
for premises in [None, 'p', {}, [None], ['q']]:
    rejects(lambda premises=premises: Theory(['p']).check(premises, 'p'))
for payload in [None, [], {}, {'atoms':[],'premises':[],'conclusion':True,'extra':1}]:
    rejects(lambda payload=payload: check_payload(payload))
rejects(lambda: Theory(['p'], allowed_worlds=[]).check([], 'q'))
# Independent specifications of the 21 published experiments.
specs = {}
p,q='p','q'; imp=('implies',p,q)
def add(key, names, cons, pre, conclusion, worlds=None):
    specs[key] = oracle(names,cons,worlds,pre,conclusion)
for key, pre, conclusion in [('modus_ponens',[imp,p],q),('modus_tollens',[imp,('not',q)],('not',p)),('denying_antecedent',[imp,('not',p)],('not',q)),('affirming_consequent',[imp,q],p)]:
    add(key,[p,q],[],pre,conclusion)
for name,f in [('p',p),('q',q),('not_p',('not',p)),('not_q',('not',q))]: add('conditional_alone_not_'+name,[p,q],[],[imp],f)
add('unrestricted_p_entails_q',[p,q],[],[p],q)
add('constrained_p_entails_q',[p,q],[imp],[p],q)
add('explicit_worlds_p_entails_q',[p,q],[],[p],q,[{p:False,q:False},{p:False,q:True},{p:True,q:True}])
b,s='body','spirit'
for label, cons in [('neither',[]),('exhaustive',[('or',b,s)]),('exclusive',[('not',('and',b,s))]),('both',[('or',b,s),('not',('and',b,s))])]:
    add(label+'_not_body_to_spirit',[b,s],cons,[('not',b)],s)
    add(label+'_body_to_not_spirit',[b,s],cons,[b],('not',s))
add('inconsistent_premises',[p,q],[],[p,('not',p)],q)
add('empty_theory',[p,q],[p,('not',p)],[],q)
report = run()
assert len(specs) == 21 and report['cases'] == specs
assert report['single_assignment'] == {'world':{p:False,q:True},'material_implication_true':True}
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
def command(args):
    return subprocess.run([sys.executable, str(ROOT/'main.py'), *args], cwd=HERE, env=env, text=True, capture_output=True)
demo=command(['demo']); again=command(['demo']); example=command(['check',str(ROOT/'example.json')])
assert demo.returncode == again.returncode == example.returncode == 0
assert demo.stdout == again.stdout == (ROOT/'logs/demo.json').read_text() == (ROOT/'logs/demo-repeat.json').read_text()
assert example.stdout == (ROOT/'logs/example-result.json').read_text()
counts['cli_checks'] += 3
for content in ['{', '{"atoms":[],"atoms":[],"premises":[],"conclusion":true}', '{"atoms":["p"],"premises":[],"conclusion":1}', '{"atoms":[],"premises":[],"conclusion":true,"unknown":1}', '{"atoms":["p"],"allowed_worlds":[{"p":true,"p":false}],"premises":[],"conclusion":"p"}']:
    path=HERE/'invalid-input.tmp.json'; path.write_text(content)
    result=command(['check',str(path)])
    assert result.returncode == 2 and 'input error' in result.stderr
    counts['cli_checks'] += 1
path.unlink()
result=command(['check',str(HERE/'nonexistent.json')])
assert result.returncode == 2; counts['cli_checks'] += 1
# Author suite: retain original test methods, redirect their temporary directories here.
harness = '''import os,sys,tempfile,unittest
from pathlib import Path
root=Path(sys.argv[1]); here=Path(sys.argv[2]); sys.path.insert(0,str(root))
original=tempfile.TemporaryDirectory
def local_temp(*a,**kw):
    kw['dir']=here
    return original(*a,**kw)
tempfile.TemporaryDirectory=local_temp
suite=unittest.defaultTestLoader.discover(str(root/'tests'))
result=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
'''
author=subprocess.run([sys.executable,'-c',harness,str(ROOT),str(HERE)],env=env,text=True,capture_output=True,cwd=HERE)
(HERE/'author-tests.txt').write_text(author.stdout+author.stderr)
assert author.returncode==0 and 'Ran 31 tests' in author.stderr
files=['logic.py','main.py','experiments.py','tests/test_logic.py','reproduce.sh','README.md','WALKTHROUGH.zh.md','SOURCES.md','example.json']
summary={'result':'PASS','seed':1768108,'python':sys.version,'platform':platform.platform(), 'counts':counts,
'published_cases':len(specs),'published_valid':sum(x['valid'] for x in specs.values()),'published_invalid':sum(not x['valid'] for x in specs.values()),'published_vacuity_warnings':sum(x['warning'] is not None for x in specs.values()),'author_test_methods':31,'existing_demo_and_example_logs':'byte-identical to fresh CLI output','scope':'finite deterministic comparisons, not a general mathematical proof','sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}}
# Small, reproducible package inventory; never dump potential matching secrets.
patterns = {
    'private_key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'openai_key': r'sk-[A-Za-z0-9_-]{24,}',
    'aws_key': r'AKIA[0-9A-Z]{16}',
    'absolute_local_path': r'(?:/Users/|/home/|/workspace/|/tmp/)[A-Za-z0-9_./-]+',
}
package_files = sorted(p for p in ROOT.rglob('*') if p.is_file() and HERE not in p.parents)
hits = []
for p in package_files:
    try:
        content = p.read_text()
    except UnicodeDecodeError:
        continue
    for name, pattern in patterns.items():
        if re.search(pattern, content):
            hits.append({'file': p.relative_to(ROOT).as_posix(), 'pattern': name})
inventory = {
    'files_checked': [p.relative_to(ROOT).as_posix() for p in package_files],
    'pattern_hits': hits,
    'symlinks': [p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_symlink()],
    'image_or_archive_files': [p.relative_to(ROOT).as_posix() for p in package_files if p.suffix.lower() in {'.png','.jpg','.jpeg','.pdf','.zip','.tar','.gz'}],
    'limitation': 'Targeted text-pattern and file-inventory review only; not proof of absence of all secrets.',
}
(HERE/'inventory-check.json').write_text(json.dumps(inventory,indent=2,ensure_ascii=False)+'\n')
summary['audit_script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
print(json.dumps(summary,indent=2,ensure_ascii=False))
