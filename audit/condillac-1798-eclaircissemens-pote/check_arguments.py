"""Small independent finite checks; not substitutes for universal proofs."""
from itertools import product
from pathlib import Path
import importlib.util
p=Path(__file__).resolve().parents[2]/'reproduction/condillac-1798-eclaircissemens-pote/model.py'
spec=importlib.util.spec_from_file_location('pote_model',p); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
states=('a','b','c'); labels=('0','1'); checks=0
for out in product(labels,repeat=3):
 h=dict(zip(states,out))
 for n in range(1,5):
  for x in product(states,repeat=n):
   observed=m.observe(x,h)
   if m.change_count(observed)>m.change_count(x):raise RuntimeError('A inequality')
   distinguishes=all(a==b or h[a]!=h[b] for a,b in zip(x,x[1:]))
   if (m.change_count(observed)==m.change_count(x))!=distinguishes:raise RuntimeError('A equality')
   if m.idea_word(m.compress(x),h)!=m.idea_word(x,h):raise RuntimeError('B')
   checks+=1
print('A inequality/equality and B: 8 maps x 120 traces =',checks,'cases passed')
checks=0
for obs in product(labels,repeat=3):
 for tar in product(labels,repeat=3):
  brute=any(all(dict(zip(labels,ds))[o]==t for o,t in zip(obs,tar)) for ds in product(labels,repeat=2))
  decoder=m.factors_through(obs,tar)
  if (decoder is not None)!=brute:raise RuntimeError('fiber equivalence')
  if decoder is not None and any(decoder[o]!=t for o,t in zip(obs,tar)):raise RuntimeError('fiber decoding')
  checks+=1
print('Fiber criterion: 64 length-3 binary observation/target pairs vs 4 candidate total decoders:',checks,'passed')
h1={'a':'0','b':'0','c':'1'};h2={'a':'0','b':'1','c':'0'}
seen={};witness=None
for n in range(1,6):
 for x in product(states,repeat=n):
  key=(m.idea_word(x,h1),m.idea_word(x,h2))
  if key in seen and m.compress(seen[key])!=m.compress(x):witness=(seen[key],x,key);break
  seen[key]=x
 if witness:break
if witness is None:raise RuntimeError('No ambiguity witness')
print('Joint state code is injective: a=(0,0), b=(0,1), c=(1,0).')
print('Nevertheless separate compressed logs have distinct compressed-state preimages:',repr(witness))
h={'a':'same','b':'same'}
for k in (0,1,2,5,10):
 x=tuple('a' if i%2==0 else 'b' for i in range(k+1))
 if m.change_count(x)!=k or m.idea_word(x,h)!=('same',):raise RuntimeError('C')
 print('Hidden-change construction k=',k,' observed=',m.idea_word(x,h),sep='')
print('All checks passed. Finite checks do not establish a universal theorem or physical-time ontology.')
