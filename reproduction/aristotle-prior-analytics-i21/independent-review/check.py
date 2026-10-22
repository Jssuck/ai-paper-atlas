"""Independent per-object oracle; bounded implementation review, not a proof."""
import sys,json,itertools,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from model import Model,models
MODES=('D','P','N','C','BOX'); QS=('a','e','i','o'); TERMS='ABC'
queries=list(itertools.product(MODES,QS,TERMS,TERMS))
def check(x,msg):
 if not x:raise RuntimeError(msg)
def oracle(n,ws,mode,q,p,s):
 pi=TERMS.index(p);si=TERMS.index(s)
 def member(w,t,i):return bool(ws[w][t] & (1<<i))
 positive=q in ('a','i'); universal=q in ('a','e')
 quant=all if universal else any
 def truth(w,i):return member(w,pi,i)==positive
 if mode=='BOX':return all(quant(truth(w,i) for i in range(n) if member(w,si,i)) for w in range(len(ws)))
 def prop(i):
  vals=[truth(w,i) for w in range(len(ws))]
  if mode=='D':return vals[0]
  if mode=='P':return any(vals)
  if mode=='N':return all(vals)
  return any(vals) and not all(vals)
 return quant(prop(i) for i in range(n) if member(0,si,i))
def mutant(n,ws,args,k):
 mode,q,p,s=args
 if k=='swap_terms':p,s=s,p
 elif k=='flip_sign':q={'a':'e','e':'a','i':'o','o':'i'}[q]
 elif k=='flip_quantity':q={'a':'i','i':'a','e':'o','o':'e'}[q]
 elif k=='P_as_N' and mode=='P':mode='N'
 elif k=='N_as_P' and mode=='N':mode='P'
 elif k=='C_as_P' and mode=='C':mode='P'
 elif k=='BOX_as_N' and mode=='BOX':mode='N'
 elif k=='last_actual':ws=ws[-1:]+ws[:-1]
 elif k=='empty_existential_true' and q in ('i','o') and ws[0][TERMS.index(s)]==0:return True
 return oracle(n,ws,mode,q,p,s)
def main():
 dims=((1,1),(1,2),(1,3),(2,1),(2,2));configs=0;checks=0
 variants=('swap_terms','flip_sign','flip_quantity','P_as_N','N_as_P','C_as_P','BOX_as_N','last_actual','empty_existential_true');witness={}
 for n,w in dims:
  for flat in itertools.product(range(2**n),repeat=3*w):
   ws=tuple(tuple(flat[j:j+3]) for j in range(0,len(flat),3));m=Model(n,ws);configs+=1
   for args in queries:
    expected=oracle(n,ws,*args);check(m.holds(*args)==expected,'oracle mismatch');checks+=1
    for k in variants:
     if k not in witness and mutant(n,ws,args,k)!=expected:witness[k]={'n':n,'worlds':ws,'query':args,'oracle':expected}
 check(len(witness)==len(variants),'missing semantic variant witness')
 bad=[]
 for n in (0,-1,True,1.5,None,'1'):bad.append(lambda n=n:Model(n,((0,0,0),)))
 for ws in ((),[],None,[ (0,0,0)],((0,0),),((0,0,0,0),),([0,0,0],),((True,0,0),),((-1,0,0),),((2,0,0),),((0.5,0,0),)):bad.append(lambda ws=ws:Model(1,ws))
 m=Model(1,((1,1,1),(0,0,0)))
 for index,values in [(0,('Q','',None,[],1)),(1,('u','',None,[],1)),(2,('Z','',None,[],1)),(3,('Z','',None,[],1))]:
  for v in values:
   a=['D','a','A','B'];a[index]=v;bad.append(lambda a=a:m.holds(*a))
 for v in (-1,2,True,1.5,None,'0'):bad.append(lambda v=v:m.extension('A',v))
 for t in ('Z','',None,[],1):bad.append(lambda t=t:m.varying(t))
 for n,w in ((0,1),(1,0),(-1,1),(1,-1),(True,1),(1,True),(1.5,1),(1,1.5),(None,1),(1,None)):
  bad.append(lambda n=n,w=w:next(models(n,w)))
 for f in bad:
  try:f()
  except ValueError:pass
  else:raise RuntimeError('invalid input accepted')
 # Relabel objects, duplicate a world, reverse nonactual worlds: all preserve truth.
 meta=0
 for flat in itertools.islice(itertools.product(range(4),repeat=9),0,2000,37):
  ws=tuple(tuple(flat[j:j+3]) for j in range(0,9,3));m=Model(2,ws)
  remap=lambda mask:((mask&1)<<1)|((mask&2)>>1)
  alts=[tuple(tuple(remap(x) for x in w) for w in ws),ws+(ws[1],),(ws[0],ws[2],ws[1])]
  for alt in alts:
   other=Model(2,alt)
   for args in queries:check(m.holds(*args)==other.holds(*args),'metamorphic mismatch');meta+=1
 print(json.dumps({'configurations':configs,'oracle_queries':checks,'invalid_inputs':len(bad),'metamorphic_comparisons':meta,'semantic_variants':len(witness),'variant_witnesses':witness,'scope':'Bounded independent implementation audit, not general proof or unique ancient semantics'},indent=2,sort_keys=True))
if __name__=='__main__':main()
