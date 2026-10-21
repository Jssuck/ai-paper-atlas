"""Independent set-based audit; finite verification, not general proof."""
import sys,json,itertools,hashlib,platform
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import model as target
count=0

def check(v,msg):
 global count
 count+=1
 if not v: raise RuntimeError(msg)

def ref(m,tag,k,s,p,n=2):
 values=[]
 for w in m:
  a={i for i in range(n) if w['ABC'.index(s)]//(2**i)%2}
  b={i for i in range(n) if w['ABC'.index(p)]//(2**i)%2}
  values.append({'A':a<=b,'E':a.isdisjoint(b),'I':bool(a&b),'O':bool(a-b)}[k])
 return {'D':values[0],'N':False not in values,'P':True in values,'C':len(set(values))==2}[tag]
models=[(t[:3],t[3:]) for t in itertools.product(range(4),repeat=6)]
check(len(set(models))==4096,'model count')
check(list(target.models())==models,'enumeration order')
for m in models:
 for tag,k,s,p in itertools.product('DNPC','AEIO','ABC','ABC'):
  check(target.modal(m,tag,k,s,p)==ref(m,tag,k,s,p),'semantics')
# API supports domains other than the report's fixed n=2.
for n in (1,3):
 for w in itertools.product(range(2**n),repeat=3):
  m=(w,tuple(reversed(w)))
  for tag,k in itertools.product('DNPC','AEIO'):
   check(target.modal(m,tag,k,'C','A',n)==ref(m,tag,k,'C','A',n),'general API')
actual=json.loads(Path('results.json').read_text())
rows=[]
for mood,forms in {'Barbara':'AAA','Celarent':'EAE','Darii':'AII','Ferio':'EIO'}.items():
 vals=[{tag:[ref(m,tag,k,s,p) for m in models] for tag in 'DNPC'} for k,s,p in zip(forms,'BCC','ABA')]
 for l,r,o in itertools.product('DNPC','DNPC','DNP'):
  sat=[i for i in range(len(models)) if vals[0][l][i] and vals[1][r][i]]
  bad=[i for i in sat if not vals[2][o][i]]
  ne=[i for i in sat if all(x!=0 for w in models[i] for x in w)]
  row=dict(mood=mood,major=l,minor=r,conclusion=o,satisfying=len(sat),countermodels=len(bad),first_countermodel=[list(w) for w in models[bad[0]]] if bad else None,nonempty_satisfying=len(ne),nonempty_countermodels=sum(not vals[2][o][i] for i in ne))
  rows.append(row)
check(rows==actual['rows'],'all report rows exact')
check(len(rows)==192,'192 configurations')
check(sum(r['countermodels']==0 for r in rows)==52,'52 finite valid configurations')
for key,m in actual['cases'].items():
 m=tuple(tuple(w) for w in m)
 check(all(x for w in m for x in w),'named terms nonempty')
 if key=='incompatible_possible_and_contingent':
  for t in 'PC':check(ref(m,t,'A','B','A') and ref(m,t,'A','C','B'),'incompatible premises')
  for t in 'DNP':check(not ref(m,t,'A','C','A'),'incompatible conclusion')
 elif key=='necessary_premises_have_actual_conclusion':
  check(ref(m,'N','A','B','A') and ref(m,'N','A','C','B') and ref(m,'D','A','C','A'),'weakening')
 else:check(ref(m,'N','A','B','A') and ref(m,'D','A','C','B') and ref(m,'D','A','C','A') and not ref(m,'N','A','C','A'),'mixed')
# Explicit exceptions rather than assert checks: preserved under optimization.
invalid=[]
for m in ([],None,(),((1,2),),((1,2,4),),((1,True,2),),((1,2,-1),),((1,2,1.0),),([1,2,3],)):
 invalid.append(lambda m=m:target.validate(m))
for n in (False,True,0,-1,2.0,None,'2'):invalid.append(lambda n=n:target.validate(((1,1,1),),n))
for x in (None,False,1,[],{},'', 'Z'):
 invalid.extend([lambda x=x:target.modal(((1,1,1),),x,'A','B','A'),lambda x=x:target.categorical((1,1,1),x,'B','A'),lambda x=x:target.categorical((1,1,1),'A',x,'A'),lambda x=x:target.categorical((1,1,1),'A','B',x)])
for call in invalid:
 try:call()
 except ValueError:check(True,'invalid rejected')
 else:check(False,'invalid accepted')
# Source-level mutants: each is executed and compared with independent oracle.
source=Path('model.py').read_text()
mutations=[('N any','if tag == \'N\': return all(values)','if tag == \'N\': return any(values)'),('P all','if tag == \'P\': return any(values)','if tag == \'P\': return all(values)'),('D last','if tag == \'D\': return values[0]','if tag == \'D\': return values[-1]'),('C inclusive','return any(values) and not all(values)','return any(values)'),('A reverse','(s & p) == s','(s & p) == p'),('E inverted','(s & p) == 0','(s & p) != 0'),('I inverted','(s & p) != 0','(s & p) == 0'),('O inverted','return (s & p) != s','return (s & p) == s')]
mutants=[]
for name,old,new in mutations:
 check(old in source,'mutation target')
 ns={'__name__':'audit_mutant'}
 exec(compile(source.replace(old,new,1),'<audit-mutant>','exec'),ns)
 found=False
 for m in models:
  for t,k in itertools.product('DNPC','AEIO'):
   if ns['modal'](m,t,k,'C','A')!=ref(m,t,k,'C','A'):found=True;break
  if found:break
 check(found,'mutant escaped: '+name);mutants.append(name)
summary={'checks':count,'models':4096,'configurations':192,'finite_valid_configurations':52,'invalid_inputs':len(invalid),'detected_mutants':mutants,'python':platform.python_version(),'optimization':sys.flags.optimize}
print(json.dumps(summary,ensure_ascii=False,sort_keys=True))
