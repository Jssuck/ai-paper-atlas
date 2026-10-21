"""Selected mutation checks run author tests against temporary altered copies; originals untouched."""
import tempfile,subprocess,sys,json
from pathlib import Path
base=Path(__file__).resolve().parents[1]
source=(base/'model.py').read_text()
mutants={
 'actual_index_ignored':('world = self.actual','world = 0'),
 'strong_drops_negative_witness':('(self.point(predicate, x) and self.point(predicate, x, False))','(self.point(predicate, x))'),
 'some_uses_all':("return all(values) if quantity == 'all' else any(values)","return all(values) if quantity == 'all' else all(values)"),
 'stable_only_actual':("return all(self.categorical(predicate, subject, 'E' if negative else 'A', w)\n                   for w in range(len(self.worlds)))","return self.categorical(predicate, subject, 'E' if negative else 'A')"),
 'joint_uses_pointwise':("return any(not (s & (~self.extension(predicate, w) if sign else\n                             self.extension(predicate, w)))\n                   for w in range(len(self.worlds)))","return self.modal(predicate, subject, 'M+' if sign else 'M-', 'all')"),
 'guard_wrong_sign':('and self.point(predicate, x, negative) for x in self.members(subject)]','and self.point(predicate, x, not negative) for x in self.members(subject)]'),
 'boolean_domain_accepted':('type(self.n) is not int or self.n < 1','not isinstance(self.n,int) or self.n < 1'),
 'possible_means_necessary':('return any(values)','return all(values)'),
 'entailment_only_actual':('return all(not a or b for a, b in zip(p, q))','return not p[0] or q[0]'),
}
results={}
for name,(old,new) in mutants.items():
 if old not in source:raise RuntimeError('missing mutation anchor '+name)
 with tempfile.TemporaryDirectory(prefix='i15-audit-') as tmp:
  root=Path(tmp)
  for f in ('demo.py','test_model.py'):(root/f).write_bytes((base/f).read_bytes())
  (root/'model.py').write_text(source.replace(old,new,1))
  run=subprocess.run([sys.executable,'-m','unittest','-v'],cwd=root,capture_output=True,text=True,timeout=120)
  results[name]={'returncode':run.returncode,'detected':run.returncode!=0,'test_output':run.stdout+run.stderr}
print(json.dumps(results,indent=2))
if not all(x['detected'] for x in results.values()):raise SystemExit(1)
