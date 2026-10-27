"""I.20 exact teaching reconstruction; no full Euclidean proof checker.
Original: extend BA, AD=AC; I.5 and proper angle part; I.19; concatenate.
The dot-product comparisons and radical signs are modern independent checks.
"""
import json
from quadratic import Q,F,point,add,sub,scale,dot,cross,norm2,dist2,rational_point,rational


def angle_cmp(u,v,x,y):
    n1,n2=norm2(u)*norm2(v),norm2(x)*norm2(y)
    if n1.sign()<=0 or n2.sign()<=0: raise ValueError('zero ray')
    d1,d2=dot(u,v),dot(x,y)
    s1,s2=d1.sign(),d2.sign()
    if s1!=s2:return -((s1>s2)-(s1<s2))
    if s1==0:return 0
    z=(d1*d1*n2-d2*d2*n1).sign()
    return -z if s1>0 else z


def sum_greater(u,v,w):
    """sqrt(u)+sqrt(v)>sqrt(w), nonnegative rational squares, exact.
    Both sides nonnegative, so square once; compare u+v-w+2sqrt(uv).
    This is modern arithmetic, not an invocation of I.20 as an axiom.
    """
    u,v,w=map(rational,(u,v,w))
    if min(u,v,w)<0:raise ValueError('negative squared length')
    return Q(u+v-w,2,u*v).sign()>0


def qjson(q):return {'a':str(q.a),'b':str(q.b),'radicand':str(q.d)}
def pjson(p):return [qjson(x) for x in p]


def construct(a,b,c):
    if not all(rational_point(p) for p in (a,b,c)):raise TypeError('rational point pairs required')
    ab,ac=sub(b,a),sub(c,a)
    if cross(ab,ac).sign()==0:raise ValueError('noncollinear triangle required')
    t=Q(0,1,(norm2(ac)/norm2(ab)).a)
    d=add(a,scale(-t,ab))
    ca,cb,cd=sub(a,c),sub(b,c),sub(d,c)
    da,dc,db=sub(a,d),sub(c,d),sub(b,d)
    left,right=t/(1+t),Q(1)/(1+t)
    u,v,w=dist2(a,b).a,dist2(a,c).a,dist2(b,c).a
    checks={
        't_positive':t.sign()>0,
        'AD_equals_AC':dist2(a,d)==dist2(a,c),
        'B_A_D_collinear':cross(sub(a,b),sub(d,b))==0,
        'A_strictly_between_B_D':dot(sub(b,a),sub(d,a)).sign()<0,
        'CA_positive_cone':ca==add(scale(left,cb),scale(right,cd)) and left.sign()>0 and right.sign()>0,
        'DAC_nondegenerate':cross(da,dc).sign()!=0,
        'DBC_nondegenerate':cross(db,dc).sign()!=0,
        'base_angles_equal_modern_check':angle_cmp(da,dc,ca,cd)==0,
        'strict_angle_part_modern_check':angle_cmp(cb,cd,ca,cd)>0,
        'same_D_ray_modern_check':angle_cmp(da,dc,db,dc)==0,
        'larger_angle_modern_check':angle_cmp(cb,cd,db,dc)>0,
        'DB_greater_BC_modern_check':(dist2(d,b)-dist2(b,c)).sign()>0,
        'concatenation_squared_identity':dist2(d,b)==norm2(ab)*(1+t)*(1+t),
        'AB_plus_AC_greater_BC':sum_greater(u,v,w),
        'AB_plus_BC_greater_AC':sum_greater(u,w,v),
        'AC_plus_BC_greater_AB':sum_greater(v,w,u),
    }
    if not all(checks.values()):raise ArithmeticError('construction invariant failed')
    return {'schema':'euclid-i20-v1','input':{'A':pjson(a),'B':pjson(b),'C':pjson(c)},
            't':qjson(t),'D':pjson(d),'CA_cone_coefficients':[qjson(left),qjson(right)],
            'checks':checks}


def strict_json(value):
    if value is None or type(value) in (str,bool,int):return
    if type(value) is list:
        for item in value:strict_json(item)
        return
    if type(value) is dict and all(type(k) is str for k in value):
        for item in value.values():strict_json(item)
        return
    raise TypeError('strict JSON only; floats and non-JSON containers unsupported')


def accepted(a,b,c,certificate):
    """Canonical replay with input binding, NOT independent theorem proving."""
    try:
        strict_json(certificate)
        return json.dumps(certificate,sort_keys=True,separators=(',',':'))==json.dumps(construct(a,b,c),sort_keys=True,separators=(',',':'))
    except (TypeError,ValueError,ArithmeticError,AttributeError,IndexError):return False
