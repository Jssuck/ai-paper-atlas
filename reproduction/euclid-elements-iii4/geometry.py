"""Exact rational teaching certificates for Euclid III.4, not a theorem prover."""
from fractions import Fraction as Q
import json

def scalar(x):
    if type(x) is int or type(x) is Q:
        return Q(x)
    if type(x) is str:
        try:
            q=Q(x)
        except (ValueError,ZeroDivisionError):
            raise ValueError('invalid rational') from None
        if str(q)!=x: raise ValueError('noncanonical rational')
        return q
    raise ValueError('exact rational required')

def point(p):
    if type(p) not in (list,tuple) or len(p)!=2: raise ValueError('two coordinates required')
    return tuple(map(scalar,p))

def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def mul(t,a): return (t*a[0],t*a[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def norm(a): return dot(a,a)
def dump(x):
    if type(x) is Q: return str(x)
    if type(x) in (tuple,list): return [dump(t) for t in x]
    if type(x) is dict: return {k:dump(v) for k,v in x.items()}
    return x

def certificate(O,r2,A,C,B,D):
    O,A,C,B,D=map(point,(O,A,C,B,D));r2=scalar(r2)
    if r2<=0: raise ValueError('positive radius squared required')
    if any(norm(sub(P,O))!=r2 for P in (A,C,B,D)): raise ValueError('endpoints not on same circle')
    v,w=sub(C,A),sub(D,B)
    if norm(v)==0 or norm(w)==0: raise ValueError('zero chord')
    det=cross(v,w)
    if det==0: raise ValueError('independent chord directions required')
    t=cross(sub(B,A),w)/det;u=cross(sub(B,A),v)/det
    if not (0<t<1 and 0<u<1): raise ValueError('strict interior intersection required')
    E=add(A,mul(t,v));eo=sub(E,O)
    ma,mb=t==Q(1,2),u==Q(1,2)
    da,db=cross(sub(O,A),v)==0,cross(sub(O,B),w)==0
    rv, rw=dot(eo,v),dot(eo,w)
    if rv!=(t-Q(1,2))*norm(v) or rw!=(u-Q(1,2))*norm(w): raise ArithmeticError('identity mismatch')
    if ma and mb and E!=O: raise ArithmeticError('center implication mismatch')
    applies=not da and not db
    if applies and ma and mb: raise ArithmeticError('III.4 mismatch')
    return dump({'input':{'O':O,'r2':r2,'A':A,'C':C,'B':B,'D':D},'E':E,'t':t,'u':u,
      'det':det,'dot_v':rv,'dot_w':rw,'midpoint_AC':ma,'midpoint_BD':mb,
      'diameter_AC':da,'diameter_BD':db,'theorem_applies':applies,'both_midpoints':ma and mb,'at_center':E==O})

def verify(c):
    try:
        if type(c) is not dict or type(c.get('input')) is not dict: return False
        expected=certificate(**c['input'])
        # JSON canonical comparison preserves booleans versus integers and exact strings.
        return json.dumps(c,sort_keys=True,separators=(',',':'))==json.dumps(expected,sort_keys=True,separators=(',',':'))
    except (ValueError,TypeError,KeyError,OverflowError): return False

def examples():
    return {
      'neither_midpoint': certificate((0,0),25,(-4,3),(4,3),(3,4),(3,-4)),
      'only_AC_midpoint': certificate((0,0),25,(-4,3),(4,3),(3,4),('-24/5','7/5')),
      'only_BD_midpoint': certificate((0,0),25,(3,4),('-24/5','7/5'),(-4,3),(4,3)),
      'one_diameter': certificate((0,0),25,(-4,3),(4,3),(0,5),(0,-5)),
      'two_diameters': certificate((0,0),25,(-5,0),(5,0),(3,4),(-3,-4))}

def transformed(c,scale=1,shift=(0,0),quarter_turns=0,reflect=False):
    scale=scalar(scale);shift=point(shift)
    if scale==0: raise ValueError('nonzero scale required')
    if type(quarter_turns) is not int or type(reflect) is not bool: raise ValueError('bad transform')
    def f(p):
        x,y=point(p)
        if reflect: x=-x
        for _ in range(quarter_turns%4): x,y=-y,x
        return add(mul(scale,(x,y)),shift)
    z=c['input'];return certificate(f(z['O']),scalar(z['r2'])*scale*scale,*(f(z[k]) for k in ('A','C','B','D')))

def grid():
    rows=[]
    for c in examples().values():
        for s in (Q(1,2),1,2,-1,3):
            for shift in ((0,0),(2,-3),(-1,4)):
                for k in range(4):
                    for reflect in (False,True): rows.append(transformed(c,s,shift,k,reflect))
    return rows
