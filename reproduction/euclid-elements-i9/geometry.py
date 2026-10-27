"""Original exact teaching model for Elements I.9; not a ruler/compass engine."""
from dataclasses import dataclass
from fractions import Fraction as R

@dataclass(frozen=True)
class Q3:
    a: R = R(0)
    b: R = R(0)
    def __post_init__(self):
        object.__setattr__(self, 'a', R(self.a))
        object.__setattr__(self, 'b', R(self.b))
    @staticmethod
    def of(x): return x if isinstance(x,Q3) else Q3(x)
    def __add__(self,x):
        x=self.of(x); return Q3(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self): return Q3(-self.a,-self.b)
    def __sub__(self,x): return self+-self.of(x)
    def __rsub__(self,x): return self.of(x)+-self
    def __mul__(self,x):
        x=self.of(x); return Q3(self.a*x.a+3*self.b*x.b,self.a*x.b+self.b*x.a)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=self.of(x); n=x.a*x.a-3*x.b*x.b
        if not n: raise ZeroDivisionError('zero field element')
        return self*Q3(x.a/n,-x.b/n)
    def sign(self):
        if not self.b: return (self.a>0)-(self.a<0)
        if not self.a: return (self.b>0)-(self.b<0)
        if self.a*self.b>0: return (self.a>0)-(self.a<0)
        d=self.a*self.a-3*self.b*self.b
        return ((self.a>0)-(self.a<0))*((d>0)-(d<0))
    def __str__(self): return str(self.a) if not self.b else f'({self.a})+({self.b})*sqrt(3)'

S=Q3(0,1)
def point(x,y): return (Q3.of(x),Q3.of(y))
def add(p,q): return tuple(a+b for a,b in zip(p,q))
def sub(p,q): return tuple(a-b for a,b in zip(p,q))
def scale(k,p): return tuple(Q3.of(k)*a for a in p)
def dot(p,q): return p[0]*q[0]+p[1]*q[1]
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def norm2(p): return dot(p,p)
def dist2(p,q): return norm2(sub(p,q))
def rotate(p): return (-p[1],p[0])
def equilateral_vertices(d,e):
    middle=scale(R(1,2),add(d,e)); offset=scale(S/2,rotate(sub(e,d)))
    return add(middle,offset),sub(middle,offset)
def inside(u,v,w):
    orientation=cross(u,v).sign()
    return orientation!=0 and cross(u,w).sign()==orientation and cross(w,v).sign()==orientation

def equal_angles(u,v,w):
    """Equality of ordinary [0,pi] angles; NOT an interior-ray assertion."""
    if min(norm2(t).sign() for t in (u,v,w))<=0: return False
    p,q=dot(u,w),dot(v,w)
    return p.sign()==q.sign() and p*p*norm2(v)==q*q*norm2(u)

def certificate(a,d,e,f):
    u,v,w=sub(d,a),sub(e,a),sub(f,a)
    de=sub(e,d)
    return {
      'nondegenerate_angle':norm2(u).sign()>0 and norm2(v).sign()>0 and cross(u,v).sign()!=0,
      'equal_cut_lengths':norm2(u)==norm2(v),
      'equilateral':dist2(d,e).sign()>0 and dist2(d,f)==dist2(d,e)==dist2(e,f),
      'opposite_side':cross(de,sub(a,d)).sign()*cross(de,sub(f,d)).sign()==-1,
      'nonzero_output_ray':norm2(w).sign()>0,
      'strictly_inside':inside(u,v,w),
      'equal_angles':equal_angles(u,v,w),
    }

def construct(a,d,e):
    """Given equal positive cuts on noncollinear rays, choose opposite DE side.
    This coordinate formula models I.1's two equilateral candidates; it does
    not implement circle intersection existence or I.3's length transfer.
    """
    u,v=sub(d,a),sub(e,a)
    if norm2(u).sign()<=0 or norm2(v).sign()<=0 or cross(u,v).sign()==0:
        raise ValueError('angle must be nondegenerate and convex')
    if norm2(u)!=norm2(v): raise ValueError('cut lengths must be equal')
    for f in equilateral_vertices(d,e):
        if certificate(a,d,e,f)['opposite_side']: return f
    raise RuntimeError('no opposite-side candidate')

def canonical(u,v): return point(0,0),point(u,v),point(u,-Q3.of(v))
