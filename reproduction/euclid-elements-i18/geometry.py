"""Euclid I.18: exact rational-input teaching reconstruction, not a proof checker.

Original route: I.3 cut, I.5 isosceles, I.16 exterior angle, proper part.
Angle comparison below is an independent modern dot-product check, NOT Euclid's
proof or an invocation of I.19. No acos, floats, cosine rule or angle sum used.
"""
import json
from quadratic import Q, F, point, add, sub, scale, dot, cross, norm2, dist2, rational_point


def angle_cmp(u,v,x,y):
    """Compare ordinary angles (u,v) and (x,y): -1,0,1. Exact in [0,pi]."""
    n1=norm2(u)*norm2(v); n2=norm2(x)*norm2(y)
    if n1.sign()<=0 or n2.sign()<=0: raise ValueError('zero ray')
    d1,d2=dot(u,v),dot(x,y)
    s1,s2=d1.sign(),d2.sign()
    # cosine is strictly decreasing on [0,pi]. Different signs settle order.
    if s1!=s2:return -((s1>s2)-(s1<s2))
    if s1==0:return 0
    squared=(d1*d1*n2-d2*d2*n1).sign()
    return -squared if s1>0 else squared


def parameters(a,b,c):
    if not all(rational_point(p) for p in (a,b,c)):raise TypeError('rational point pairs required')
    ab,ac=sub(b,a),sub(c,a)
    if cross(ab,ac).sign()==0:raise ValueError('noncollinear triangle required')
    if (norm2(ac)-norm2(ab)).sign()<=0:raise ValueError('requires AC > AB')
    t=Q(0,1,(norm2(ab)/norm2(ac)).a)
    return t,add(a,scale(t,ac))


def qjson(q):return {'a':str(q.a),'b':str(q.b),'radicand':str(q.d)}
def pjson(p):return [qjson(x) for x in p]


def construct(a,b,c):
    t,d=parameters(a,b,c)
    ba,bc,bd=sub(a,b),sub(c,b),sub(d,b)
    da,db,dc=sub(a,d),sub(b,d),sub(c,d)
    ca,cb=sub(a,c),sub(b,c)
    # bd=(1-t)ba+t*bc provides positive cone coefficients, not just a diagram.
    checks={
      'cut_parameter_positive':t.sign()>0,
      'cut_parameter_below_one':(1-t).sign()>0,
      'AD_equals_AB':dist2(a,d)==dist2(a,b),
      'D_on_AC':cross(sub(d,a),sub(c,a))==0,
      'D_strictly_between_A_C':dot(da,dc).sign()<0,
      'BD_positive_cone_identity':bd==add(scale(1-t,ba),scale(t,bc)),
      'ABD_nondegenerate':cross(ba,bd).sign()!=0,
      'DBC_nondegenerate':cross(db,dc).sign()!=0,
      'base_angles_equal_modern_check':angle_cmp(ba,bd,da,db)==0,
      'exterior_angle_strict_modern_check':angle_cmp(da,db,cb,ca)>0,
      'proper_angle_part_modern_check':angle_cmp(ba,bc,ba,bd)>0,
      'conclusion_modern_check':angle_cmp(ba,bc,ca,cb)>0,
    }
    if not all(checks.values()):raise ArithmeticError('construction invariant failed')
    return {'schema':'euclid-i18-v1','input':{'A':pjson(a),'B':pjson(b),'C':pjson(c)},
            't':qjson(t),'D':pjson(d),'BD_cone_coefficients':[qjson(1-t),qjson(t)],
            'checks':checks}


def strict_json(value):
    """Reject Python equality traps and non-JSON containers/non-finite numbers."""
    if value is None or type(value) in (str,bool,int):return
    if type(value) is list:
        for item in value:strict_json(item)
        return
    if type(value) is dict and all(type(k) is str for k in value):
        for item in value.values():strict_json(item)
        return
    raise TypeError('strict JSON values required; floating numbers unsupported')


def accepted(a,b,c,certificate):
    """Deterministic canonical replay plus input binding, not an independent proof."""
    try:
        strict_json(certificate)
        expected=construct(a,b,c)
        return json.dumps(certificate,sort_keys=True,separators=(',',':'))==json.dumps(expected,sort_keys=True,separators=(',',':'))
    except (TypeError,ValueError,ArithmeticError,AttributeError,IndexError):return False
