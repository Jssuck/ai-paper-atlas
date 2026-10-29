"""Independent finite audit: external certificates, independently computed polygon areas."""
from fractions import Fraction as F
from copy import deepcopy
import json
from geometry import verify

COUNTS={'external_certificates':0,'area_comparisons':0,'tampering_rejected':0,'invalid_inputs_rejected':0,'overlap_checks':0}
def check(ok,label):
    if not ok: raise RuntimeError(label)
def reject(call,category):
    try: call()
    except ValueError: COUNTS[category]+=1
    else: raise RuntimeError('invalid input accepted: '+category)
def certificate(a,b,o,u,v):
    total=a+b
    # Independent specification: G is intersection of x=a with x+y=total.
    gy=total-a
    loc={'A':(0,0),'B':(total,0),'C':(a,0),'D':(0,total),'E':(total,total),
         'F':(total,gy),'G':(a,gy),'H':(0,gy),'N':(a,total)}
    return {'points':{n:[F(o[i])+x*F(u[i])+y*F(v[i]) for i in range(2)] for n,(x,y) in loc.items()}}
def signed_polygon(points):
    acc=F(0)
    for i,(x,y) in enumerate(points):
        xx,yy=points[(i+1)%len(points)]
        acc+=x*yy-y*xx
    return abs(acc)/2

A=[F(1,7),F(1,2),F(1),F(3),F(8)]
B=[F(1,7),F(1,2),F(1),F(2),F(5,3),F(9)]
BASES=[((1,0),(0,1)),((1,0),(0,-1)),((0,1),(-1,0)),((0,-1),(-1,0)),
       ((3,4),(-4,3)),((3,4),(4,-3)),((F(3,5),F(4,5)),(F(-4,5),F(3,5))),((F(2,3),0),(0,F(2,3)))]
for ai,a in enumerate(A):
 for bi,b in enumerate(B):
  for k,(u,v) in enumerate(BASES):
   o=(F(ai-3,7),F(bi+2,9)); c=certificate(a,b,o,u,v);p=c['points']
   got=verify(c,a,b,o,u,v);s=F(u[0])**2+F(u[1])**2
   expected={'AG':a*b*s,'GE':a*b*s,'CF':b*b*s,'DG':a*a*s,'AF':(a+b)*b*s,
             'CE':(a+b)*b*s,'gnomon':(2*a*b+b*b)*s,'whole':(a+b)**2*s}
   boundaries={'AG':'HGCA','GE':'NEFG','CF':'GFBC','DG':'DNGH','AF':'HFBA','CE':'NEBC','gnomon':'HGNEBA','whole':'DEBA'}
   for key,ns in boundaries.items():
    actual=signed_polygon([p[n] for n in ns]);check(actual==expected[key]==got[key],key);COUNTS['area_comparisons']+=1
   check(signed_polygon([p[n] for n in 'CFBG'])==0,'crossing order should cancel signed sum')
   # Intersection and union are audited separately from final polynomial equality.
   overlap=b*b*s
   check(got['AF']+got['CE']-overlap==got['gnomon'],'union')
   check(got['AF']+got['CE']-got['gnomon']==got['CF'],'overlap')
   check(got['whole']+got['CF']==2*got['AF']+got['DG'],'target')
   COUNTS['overlap_checks']+=3;COUNTS['external_certificates']+=1
   for name in p:
    for axis in (0,1):
     for delta in (F(1,13),F(-2,17)):
      bad=deepcopy(c);bad['points'][name][axis]+=delta
      reject(lambda:verify(bad,a,b,o,u,v),'tampering_rejected')
   # A globally translated but input-unbound object must not pass.
   bad=deepcopy(c)
   for xy in bad['points'].values():xy[0]+=1
   reject(lambda:verify(bad,a,b,o,u,v),'tampering_rejected')

base=certificate(F(3),F(2),(0,0),(1,0),(0,1))
for value in (0,-1,F(-1,2),True,False,1.0,'1',None,[],{}):
 for field in ('a','b'):
  reject(lambda value=value,field=field:verify(base,**{field:value}),'invalid_inputs_rejected')
for kwargs in ({'u':(0,0)},{'v':(0,0)},{'u':(2,0)},{'v':(1,1)},
               {'u':(True,0)},{'v':(0,1.0)},{'origin':(False,0)},
               {'u':None},{'v':(0,)},{'origin':(0,0,0)}):
 reject(lambda kwargs=kwargs:verify(base,**kwargs),'invalid_inputs_rejected')
for c in (None,[],{}, {'points':[]},{'points':None},{'points':{}},{'points':base['points'],'extra':1}):
 reject(lambda c=c:verify(c),'invalid_inputs_rejected')
for name in base['points']:
 bad=deepcopy(base);del bad['points'][name];reject(lambda:verify(bad),'invalid_inputs_rejected')
 for value in ((False,0),(0.0,0),(0,),None):
  bad=deepcopy(base);bad['points'][name]=value;reject(lambda:verify(bad),'invalid_inputs_rejected')
# Explicitly reject a horizontal cut that preserves the whole-area sum but not DB.
bad=deepcopy(base)
for name in ('F','G','H'):bad['points'][name][1]=F(1)
reject(lambda:verify(bad),'invalid_inputs_rejected')
print(json.dumps({'status':'passed','counts':COUNTS,'limits':'Finite rational audit; not a general proof or independently axiomatized geometry system.'},indent=2))
