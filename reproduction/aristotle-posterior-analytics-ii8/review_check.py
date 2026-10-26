import contextlib,hashlib,io,itertools,json,platform,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root.resolve()))
import model
lines=[]
def record(x): lines.append(str(x))
def require(condition,message):
    if not condition: raise RuntimeError(message)
record('Independent II.8 technical review; Python '+platform.python_version())
for flag in ([],['-O'],['-OO']):
    cmd=[sys.executable]+flag+['-m','unittest','-v','test_model']
    p=subprocess.run(cmd,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    record('COMMAND python3 '+' '.join(flag+['-m','unittest','-v','test_model']))
    record(p.stdout);record('EXIT '+str(p.returncode));require(p.returncode==0,'tests failed')
rows=valid=errors=0
# Independent bit-mask oracle, extended to n=5 (not model.subsets or enumerate_chains).
for n in range(6):
    for c,b,a in itertools.product(range(1<<n),repeat=3):
        sets=[{i for i in range(n) if mask>>i&1} for mask in (c,b,a)]
        actual=model.chain(*sets)
        expected={'minor':c&b==c,'major':b&a==b,'conclusion':c&a==c,'premises':c&b==c and b&a==b}
        rows+=1;valid+=expected['premises'];errors+=actual!=expected
require(rows==37449 and valid==1365 and errors==0,'extended bit oracle failed')
record(f'Independent n=0..5 bitmask oracle: triples={rows}, valid={valid}, differences={errors}')
checks=0
n=4
names={f'm{m:02}':{i for i in range(n) if m>>i&1} for m in range(16)}
for c,a in itertools.product(range(16),repeat=2):
    expected=tuple(f'm{m:02}' for m in range(16) if c&m==c and m&a==m)
    actual=model.candidate_middles(names[f'm{c:02}'],names[f'm{a:02}'],names)
    require(actual==expected,'candidate exhaustive oracle failed');checks+=1
record(f'Independent candidate oracle: {checks} C/A pairs, all 16 named middles, differences=0')
checks=0
for c,b,a in itertools.product((set(),{0}),repeat=3):
    for role,immediate in itertools.product(('sign','cause','unknown'),(False,True)):
        report=model.report(c,b,a,model.DeclaredRole(role,immediate,'review declaration'))
        require(report['causal_truth_verified'] is False and report['essence_verified'] is False,'knowledge upgrade')
        require(all(report[k]==v for k,v in model.chain(c,b,a).items()),'role changes truth');checks+=1
record(f'Role/immediacy stress: {checks} reports, false certification flags retained')
for u,b in itertools.product((0,1),repeat=2):
    require(model.binary_world('directed',u,b)==(b,b),'directed mismatch')
    require(model.binary_world('common',u,b)==(b,u),'common mismatch')
record('All four intervention cases independently substituted: two disagreements')
nb=json.loads((root/'tutorial.ipynb').read_text())
ids=[c.get('id') for c in nb['cells']]
require(all(isinstance(i,str) and 1<=len(i)<=64 and all(c.isalnum() or c in '_-' for c in i) for i in ids) and len(set(ids))==len(ids),'cell ids invalid')
record(f'Notebook format 4.5: {len(ids)} unique valid cell ids checked (not full external schema validation)')
ns={'__name__':'__review_notebook__'};count=0
for cell in nb['cells']:
    if cell['cell_type']!='code':continue
    count+=1;stream=io.StringIO()
    with contextlib.redirect_stdout(stream):exec(compile(''.join(cell['source']),f'review-cell-{count}','exec'),ns)
    saved=''.join(''.join(o['text']) for o in cell['outputs'] if o['output_type']=='stream')
    require(stream.getvalue()==saved,'notebook stored output mismatch')
require(count==4,'notebook count')
record('Notebook: four sequential standard-library exec cells, stored stdout exact match; NOT Jupyter kernel')
hashes=json.loads((root/'sha256.json').read_text())
for path,expected in hashes.items():require(hashlib.sha256((root/path).read_bytes()).hexdigest()==expected,'file hash mismatch '+path)
record(f'Existing SHA256 manifest verified: {len(hashes)} entries')
record('PASS: finite implementation/record verification only; not source audit, scientific causation, or renderer certification')
(root/'logs/review.log').write_text('\n'.join(lines)+'\n')
files=sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='sha256.json')
(root/'sha256.json').write_text(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
print('\n'.join(lines[-8:]))
