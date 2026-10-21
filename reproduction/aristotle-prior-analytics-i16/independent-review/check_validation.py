"""Explicit validation probes, retained under optimization."""
import json,pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from model import Model,models
calls=[]
for n in (False,True,0,-1,1.0,'1',None):calls.append(lambda n=n:Model(n,((0,0,0),)))
for w in ([],(),None,((0,0),),((0,0,0,0),),([0,0,0],),((False,0,0),),((-1,0,0),),((2,0,0),)):
 calls.append(lambda w=w:Model(1,w))
for a in (-1,1,False,True,0.0,'0',None):calls.append(lambda a=a:Model(1,((0,0,0),),a))
m=Model(1,((0,0,0),))
for term in ('D','',None,False,[],{}):
 calls.extend([lambda t=term:m.mask(t),lambda t=term:m.modal(t,'A','K'),lambda t=term:m.modal('A',t,'K'),lambda t=term:m.categorical(t,'A','E'),lambda t=term:m.symmetric_negative(t,'A'),lambda t=term:m.stable_positive('A',t),lambda t=term:m.jointly_possible(t,'A')])
for mode in ('',None,[],{}):calls.append(lambda x=mode:m.modal('A','B',x))
for q in ('',None,[],{}):calls.append(lambda x=q:m.modal('A','B','K',x))
for q in ('',None,[],{}):calls.append(lambda x=q:m.categorical('A','B',x))
for w in (-1,1,True,0.0):calls.append(lambda x=w:m.mask('A',x))
for b in (1,0,None,'true'):calls.append(lambda x=b:m.jointly_possible('A','B',x))
for n,k in ((False,1),(1,True),(0,1),(1,0),(1,-1),(1,1.0)):
 calls.append(lambda n=n,k=k:next(models(n,k)))
for i,call in enumerate(calls):
 try:call()
 except ValueError:continue
 raise RuntimeError(('accepted invalid',i))
print(json.dumps({'invalid_probes':len(calls),'all_ValueError':True},indent=2))
