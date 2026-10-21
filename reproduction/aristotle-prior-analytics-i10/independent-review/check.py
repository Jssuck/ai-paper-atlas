"""Independent set-based oracle. Run from the reproduction directory."""
import sys,json,itertools,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import modal as a
checks=0

def eq(x,y,label):
 global checks
 checks+=1
 if x!=y: raise RuntimeError(str(label)+': '+repr((x,y)))

def ext(mask,n): return frozenset(i for i in range(n) if (mask//(2**i))%2)
def rel(k,p,s):
 if k=='A': return all(x in p for x in s)
 if k=='E': return not any(x in p for x in s)
 if k=='I': return any(x in p for x in s)
 if k=='O': return any(x not in p for x in s)
 raise ValueError(k)

def oracle(m,k,p,s,mode):
 ws=[[ext(v,m.n) for v in row] for row in m.worlds]
 if mode=='ordinary': return rel(k,ws[0][p],ws[0][s])
 if mode=='boxed': return all(rel(k,w[p],w[s]) for w in ws)
 pred=(set.intersection(*(set(w[p]) for w in ws)) if k in 'AI' else set.union(*(set(w[p]) for w in ws)))
 return rel(k,pred,ws[0][s])

def strong(m,p,s):
 ps={x for w in m.worlds for x in ext(w[p],m.n)}
 ss={x for w in m.worlds for x in ext(w[s],m.n)}
 return not any(x in ss for x in ps)

# Independent enumeration, not author generator.
models=[]
for cells in itertools.product(range(4),repeat=6):
 m=a.Model(2,(tuple(cells[:3]),tuple(cells[3:])))
 models.append(m)
 for p,s in itertools.product(range(3),repeat=2):
  for k in 'AEIO':
   for mode in ('ordinary','boxed','anchored'):
    eq(getattr(a,mode)(m,k,p,s),oracle(m,k,p,s,mode),(mode,k,p,s))
  eq(a.strong_e(m,p,s),strong(m,p,s),'strong')
 for t in range(3):
  sets=[ext(w[t],2) for w in m.worlds]
  eq(ext(m.possible(t),2),set.union(*map(set,sets)),'possible')
  eq(ext(m.necessary(t),2),set.intersection(*map(set,sets)),'necessary')
# Non-enumerated shapes: one/three worlds, 1/3/8 objects.
for n,ws in [(1,((1,0,1),)),(3,((7,1,4),(3,2,1),(5,6,0))),(8,((255,128,1),(129,127,254)))]:
 m=a.Model(n,ws)
 for p,s in itertools.product(range(3),repeat=2):
  for k in 'AEIO':
   for mode in ('ordinary','boxed','anchored'): eq(getattr(a,mode)(m,k,p,s),oracle(m,k,p,s,mode),'extra shapes')
  eq(a.strong_e(m,p,s),strong(m,p,s),'extra strong')
# Exact route totals independently recomputed from oracle.
vnames=('cesare_local','camestres_reversed_local','festino_fixed_witness','cesare_bridged_strong','camestres_bridged_strong','ordinary_cesare','ordinary_camestres','ordinary_festino','ordinary_baroco')
ins=('anchored_e_conversion','cesare_unbridged_strong','camestres_unbridged_strong','necessary_affirmative_universal','necessary_affirmative_particular','necessary_particular_negative','boxed_e_implies_strong_e')
v=[[0,0] for _ in vnames]; bad=[[0,0] for _ in ins]
for m in models:
 T=lambda k,p,s:oracle(m,k,p,s,'ordinary')
 N=lambda k,p,s:oracle(m,k,p,s,'anchored')
 E=lambda p,s:strong(m,p,s)
 U=lambda t:{x for row in m.worlds for x in ext(row[t],2)}
 vv=[(E(0,1) and T('A',0,2),N('E',1,2)),(E(0,2) and T('A',0,1),N('E',2,1)),(E(0,1) and T('I',0,2),N('O',1,2)),(E(0,1) and U(2)<=U(0),E(1,2)),(E(0,2) and U(1)<=U(0),E(1,2)),(T('E',0,1) and T('A',0,2),T('E',1,2)),(T('A',0,1) and T('E',0,2),T('E',1,2)),(T('E',0,1) and T('I',0,2),T('O',1,2)),(T('A',0,1) and T('O',0,2),T('O',1,2))]
 ii=[(N('E',0,1),N('E',1,0)),(E(0,1) and T('A',0,2),E(1,2)),(E(0,2) and T('A',0,1),E(1,2)),(N('A',0,1) and T('E',0,2),N('E',1,2)),(N('A',0,1) and T('O',0,2),N('O',1,2)),(T('A',0,1) and N('O',0,2),N('O',1,2)),(oracle(m,'E',0,1,'boxed'),E(0,1))]
 for results,items in ((v,vv),(bad,ii)):
  for bucket,(prem,concl) in zip(results,items):
   if prem: bucket[0]+=1;bucket[1]+=int(not concl)
r=a.run(); eq(r['models'],4096,'models')
for name,pair in zip(vnames,v): eq([r['valid_local_routes'][name]['premise_models'],r['valid_local_routes'][name]['failures']],pair,name)
for name,pair in zip(ins,bad): eq([r['invalid_generalizations'][name]['premise_models'],r['invalid_generalizations'][name]['countermodels']],pair,name)
# Invalid inputs: public validated Model/extent/semantic entry points.
invalid=[]
for n in [0,-1,9,True,False,2.,'2',None]: invalid.append(lambda n=n:a.Model(n,((0,0,0),)))
for ws in [(),[],None,((0,0),),((0,0,0,0),),([0,0,0],),('abc',)]: invalid.append(lambda ws=ws:a.Model(2,ws))
for x in [-1,4,True,False,1.,'1',None]: invalid.append(lambda x=x:a.Model(2,((x,0,0),)))
m=models[0]
for x in [-1,3,True,False,0.,'0',None]:
 for f in (lambda x:m.extent(x),lambda x:m.possible(x),lambda x:m.necessary(x),lambda x:a.ordinary(m,'A',x,0),lambda x:a.anchored(m,'E',0,x),lambda x:a.strong_e(m,x,0)):
  invalid.append(lambda x=x,f=f:f(x))
for w in [-1,2,True,False,0.,'0',None]: invalid.append(lambda w=w:m.extent(0,w))
for k in ['X','',None,0]:
 for f in (a.ordinary,a.boxed,a.anchored): invalid.append(lambda k=k,f=f:f(m,k,0,1))
for f in invalid:
 try: f()
 except ValueError: checks+=1
 else: raise RuntimeError('invalid input accepted')
# Meaningful faulty implementations compared with independent oracle.
mutants={
 'ordinary_reversed':('ordinary',lambda m,k,p,s:a.ordinary(m,k,s,p)),
 'ordinary_uses_world1':('ordinary',lambda m,k,p,s:a.ordinary(m,k,p,s,1)),
 'boxed_any_world':('boxed',lambda m,k,p,s:any(a.ordinary(m,k,p,s,w) for w in range(len(m.worlds)))),
 'anchored_as_boxed':('anchored',lambda m,k,p,s:a.boxed(m,k,p,s)),
 'anchored_union_all_types':('anchored',lambda m,k,p,s:a.relation(k,m.possible(p),m.extent(s))),
 'anchored_intersection_all_types':('anchored',lambda m,k,p,s:a.relation(k,m.necessary(p),m.extent(s))),
 'anchored_subject_possible':('anchored',lambda m,k,p,s:a.relation(k,m.necessary(p) if k in 'AI' else m.possible(p),m.possible(s))),
 'anchored_subject_necessary':('anchored',lambda m,k,p,s:a.relation(k,m.necessary(p) if k in 'AI' else m.possible(p),m.necessary(s))),
 'I_as_A':('ordinary',lambda m,k,p,s:a.ordinary(m,'A' if k=='I' else k,p,s)),
 'O_as_E':('ordinary',lambda m,k,p,s:a.ordinary(m,'E' if k=='O' else k,p,s)),
}
detected={}
for name,(mode,fn) in mutants.items():
 for m in models:
  found=False
  for p,s,k in itertools.product(range(3),range(3),'AEIO'):
   if fn(m,k,p,s)!=oracle(m,k,p,s,mode): detected[name]={'worlds':m.worlds,'kind':k,'pred':p,'subj':s};found=True;break
  if found:break
 if name not in detected: raise RuntimeError('undetected fault '+name)
 checks+=1
for name,fn in [('strong_as_boxed',lambda m,p,s:a.boxed(m,'E',p,s)),('strong_as_anchored',lambda m,p,s:a.anchored(m,'E',p,s))]:
 for m in models:
  if fn(m,0,1)!=strong(m,0,1): detected[name]={'worlds':m.worlds};break
 if name not in detected:raise RuntimeError('undetected fault '+name)
 checks+=1
# Reviewed files, relative paths only.
base=Path(__file__).resolve().parents[1]
names=['modal.py','test_modal.py','README.md','WALKTHROUGH.md','results.json','results-O.json','results-OO.json','environment.json','artifact-hashes.json']
hashes={name:hashlib.sha256((base/name).read_bytes()).hexdigest() for name in names}
out={'status':'PASS','checks':checks,'models':4096,'extra_models':3,'invalid_calls':len(invalid),'detected_faults':len(detected),'fault_evidence':detected,'valid_totals':dict(zip(vnames,v)),'invalid_totals':dict(zip(ins,bad)),'reviewed_sha256':hashes,'limits':'Finite modern semantics only; no historical fidelity or all-software-defects claim. Low-level relation/subset expect validated bitmasks; models generator used only at positive tested sizes.'}
print(json.dumps(out,ensure_ascii=False,indent=2))
