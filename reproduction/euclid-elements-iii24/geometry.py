"""Exact rational teaching model of III.24, not an ancient algorithm."""
from dataclasses import dataclass
from fractions import Fraction as F

def q(x):
    if isinstance(x, bool) or not isinstance(x, (int, F)):
        raise TypeError('exact int or Fraction required')
    return F(x)
def vec(p):
    if len(p) != 2: raise ValueError('two coordinates required')
    return tuple(q(x) for x in p)
def add(p,r): return (p[0]+r[0],p[1]+r[1])
def sub(p,r): return (p[0]-r[0],p[1]-r[1])
def mul(c,p): return (c*p[0],c*p[1])
def dot(p,r): return p[0]*r[0]+p[1]*r[1]
def det(p,r): return p[0]*r[1]-p[1]*r[0]
def need(test,message):
    if not test: raise ValueError(message)

@dataclass(frozen=True)
class Segment:
    a: F
    k: F
    mid: tuple = (0,0)
    e: tuple = (1,0)
    n: tuple = (0,1)
    def __post_init__(self):
        object.__setattr__(self,'a',q(self.a)); object.__setattr__(self,'k',q(self.k))
        for name in ('mid','e','n'): object.__setattr__(self,name,vec(getattr(self,name)))
        need(self.a>0,'positive half-base required')
        need(dot(self.e,self.e)==dot(self.n,self.n)==1 and dot(self.e,self.n)==0,'orthonormal frame required')
    def world(self,p):
        p=vec(p)
        return add(self.mid,add(mul(p[0],self.e),mul(p[1],self.n)))
    def local(self,p):
        v=sub(vec(p),self.mid); return dot(v,self.e),dot(v,self.n)
    @property
    def endpoints(self): return self.world((-self.a,0)),self.world((self.a,0))
    @property
    def center(self): return self.world((0,self.k))
    @property
    def radius2(self): return self.a*self.a+self.k*self.k
    @property
    def angle_cot(self): return self.k/self.a
    @property
    def kind(self): return 'major' if self.k>0 else 'minor' if self.k<0 else 'semicircle'
    def power(self,p):
        v=sub(vec(p),self.center); return dot(v,v)-self.radius2
    def contains(self,p): return self.local(p)[1]>=0 and self.power(p)<=0
    def arc_point(self,t):
        t=q(t); need(t>0,'positive ray slope required')
        u=2*(self.a+self.k*t)/(1+t*t)
        need(u>0,'ray must enter selected half-plane')
        return self.world((-self.a+u,t*u))
    def measured_cot(self,p):
        p=vec(p); need(self.power(p)==0 and self.local(p)[1]>0,'nonendpoint selected arc point required')
        A,B=self.endpoints; v,w=sub(A,p),sub(B,p)
        return dot(v,w)/abs(det(v,w))
    def similar(self,other): return self.angle_cot==other.angle_cot
    def coincides(self,other):
        return set(self.endpoints)==set(other.endpoints) and self.n==other.n and self.center==other.center and self.radius2==other.radius2
    def align_point_to(self,other,p):
        """Rigid placement mapping ordered endpoints and selected side; no angle assumption."""
        need(self.a==other.a,'equal bases required for this rigid placement')
        return other.world(self.local(p))
    def aligned_circle_matches(self,other):
        return self.align_point_to(other,self.center)==other.center and self.radius2==other.radius2

def grid():
    stats=dict(configurations=0,placements=0,arc_checks=0,membership_checks=0,unequal_base_pairs=0)
    frames=[((0,0),(1,0),(0,1)),((3,-2),(F(3,5),F(4,5)),(F(-4,5),F(3,5))),((-2,3),(F(3,5),F(4,5)),(F(4,5),F(-3,5))),((1,1),(-1,0),(0,1))]
    for a in map(F,[1,2,3]):
      for ratio in [F(i,3) for i in range(-6,7)]:
        s=Segment(a,a*ratio); stats['configurations']+=1
        for mid,e,n in frames:
          d=Segment(a,a*ratio,mid,e,n); stats['placements']+=1
          need(s.similar(d),'similarity failed'); need(s.aligned_circle_matches(d),'circle alignment failed')
          for j in range(1,7):
            t=F(j,12)/(1+abs(ratio)); p=s.arc_point(t); z=s.align_point_to(d,p)
            need(s.measured_cot(p)==d.measured_cot(z)==ratio,'angle failed'); stats['arc_checks']+=1
          for x in range(-3,4):
            for y in range(-2,4):
              p=(a*F(x,2),a*F(y,2)); z=s.align_point_to(d,p)
              need(s.contains(p)==d.contains(z),'membership failed'); stats['membership_checks']+=1
        bigger=Segment(2*a,2*a*ratio)
        need(s.similar(bigger) and s.radius2!=bigger.radius2,'scale counterexample failed'); stats['unequal_base_pairs']+=1
    return stats
