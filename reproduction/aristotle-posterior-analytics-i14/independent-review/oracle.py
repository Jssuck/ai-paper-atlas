import importlib.util,itertools,json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('target',root/'model.py'); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def q(k,x,y):
 return {'A':not any(z not in y for z in x),'E':not any(z in y for z in x),'I':any(z in y for z in x),'O':any(z not in y for z in x)}[k]
sets=[{i for i in range(4) if n>>i&1} for n in range(16)]
for nonempty in [False,True]:
 invalid=set(); witnesses=set()
 for s,p,m in itertools.product(sets,repeat=3):
  if nonempty and not all([s,p,m]):continue
  for f,xy in [(1,((m,p),(s,m))),(2,((p,m),(s,m))),(3,((m,p),(m,s)))]:
   for a,b in itertools.product('AEIO',repeat=2):
    if q(a,*xy[0]) and q(b,*xy[1]):
     witnesses.add((f,a,b))
     for c in 'AEIO':
      if not q(c,s,p):invalid.add((f,a+b+c))
 for f in [1,2,3]:
  for mood in mod.MOODS:
   actual=mod.evaluate(f,mood,nonempty)['valid_in_enumeration']
   if actual != ((f,mood) not in invalid):raise RuntimeError((nonempty,f,mood))
 if len(witnesses)!=48:raise RuntimeError('unsatisfiable pair')
 print('4-element quantified oracle matches all 192 judgments; policy=',nonempty)
# Independent construct all second-figure affirmative counterexamples.
for a,b in itertools.product('AEIO',repeat=2):
 p={0};s={1};m=set()
 if a in 'AI':m.add(0)
 if b in 'AI':m.add(1)
 if not m:m.add(2)
 if not(q(a,p,m) and q(b,s,m) and not q('A',s,p) and not q('I',s,p)):raise RuntimeError('second')
 # Third figure: same singleton subject M; add non-M P/S witnesses.
 m={0}; p={0} if a in 'AI' else {1}; s={0} if b in 'AI' else {2}
 for c in 'AE':
  pp=p|({3} if c=='E' else set());ss=s|{3}
  if not(q(a,m,pp) and q(b,m,ss) and not q(c,ss,pp)):raise RuntimeError('third')
print('all 16 second-figure and 32 third-figure general construction instances pass')
print('PASS independent audit')
