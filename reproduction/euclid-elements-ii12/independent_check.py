"""Independent finite audit. Uses side squares to classify, not production dot()."""
from fractions import Fraction as F
from itertools import product
import json
from geometry import construct, normalized


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def distance2(p,q):
    return sum((F(x)-F(y))**2 for x,y in zip(p,q))


def area2(a,b,c):
    # Shoelace, independent of production's cross implementation.
    return (a[0]*b[1]+b[0]*c[1]+c[0]*a[1]
            -a[1]*b[0]-b[1]*c[0]-c[1]*a[0])


def verify(a,b,c):
    a,b,c=[tuple(map(F,p)) for p in (a,b,c)]
    ab,ac,bc=distance2(a,b),distance2(a,c),distance2(b,c)
    admissible=(area2(a,b,c)!=0 and bc>ab+ac)
    try:
        r=construct(a,b,c)
    except ValueError:
        require(not admissible,'valid input rejected')
        return False
    require(admissible,'invalid input accepted')
    require((r['AB2'],r['AC2'],r['BC2'])==(ab,ac,bc),'side squares')
    d=r['D']
    require(area2(a,c,d)==0,'foot collinearity')
    # Rightness checked by converse Pythagorean equality, rather than dot().
    ad,bd,cd=distance2(a,d),distance2(b,d),distance2(c,d)
    require(ab==ad+bd and bc==cd+bd,'right triangle squares')
    require(cd>ac and d!=a,'external location')
    require(r['AD2']==ad and r['BD2']==bd and r['CD2']==cd,'auxiliary squares')
    excess=bc-ab-ac
    require(r['correction']==excess and excess>0,'positive difference')
    require(r['AC_times_AD']>0 and r['AC_times_AD']**2==ac*ad,'rectangle length product')
    require(cd==ac+ad+2*r['AC_times_AD'],'II.4 independent lengths')
    require(r['t']<0 and tuple(a[i]+r['t']*(c[i]-a[i]) for i in range(2))==d,'parameter')
    # Swap B,C. The alternate exterior projection has the same rectangle area.
    swap=construct(a,c,b)
    require(swap['AC_times_AD']==r['AC_times_AD'],'projection side swap')
    require(all(r['checks'].values()),'reported checks')
    return True


def main():
    points=list(product(range(-3,4),repeat=2))
    accepted=rejected=0
    for b,c in product(points,repeat=2):
        if verify((0,0),b,c):accepted+=1
        else:rejected+=1
    transformed=0
    # Hand-defined rational orthogonal matrices, translations and scale factors.
    matrices=[((1,0),(0,1)),((0,-1),(1,0)),((1,0),(0,-1)),
              ((F(3,5),-F(4,5)),(F(4,5),F(3,5)))]
    for base,ext,height in product([F(1,7),F(3,2),F(4)],repeat=3):
        for matrix in matrices:
            for scale in [F(1,3),F(7,2)]:
                def tx(p):
                    return tuple(scale*sum(matrix[i][j]*p[j] for j in range(2))+[F(2,3),F(-5,7)][i] for i in range(2))
                a,b,c=map(tx,[(0,0),(-ext,height),(base,0)])
                require(verify(a,b,c),'transformed input')
                require(construct(a,b,c)['correction']==2*base*ext*scale**2,'scale area')
                transformed+=1
    illegal=0
    for bad in [True,False,1.0,float('nan'),float('inf'),'1',None,complex(1,0)]:
        for role in range(3):
            for coordinate in range(2):
                args=[[0,0],[-2,3],[4,0]]
                args[role][coordinate]=bad
                try:construct(*args)
                except TypeError:illegal+=1
                else:raise RuntimeError('illegal coordinate accepted')
    for bad in [None,(),(1,),[1,2,3],'12',12,{'x':1,'y':2}]:
        for role in range(3):
            args=[(0,0),(-2,3),(4,0)];args[role]=bad
            try:construct(*args)
            except TypeError:illegal+=1
            else:raise RuntimeError('illegal point accepted')
    examples=[(4,2,3,13,16,45,16),(4,2,5,29,16,61,16),
              (F(3),F(1,2),2,F(17,4),9,F(65,4),3)]
    for b,p,h,ab,ac,bc,excess in examples:
        r=normalized(b,p,h)
        require(tuple(r[k] for k in ('AB2','AC2','BC2','correction'))==(ab,ac,bc,excess),'article hand example')
    for n in [18,30,100]:
        r=normalized(1,F(1,10**n),1)
        require(r['correction']==F(2,10**n),'tiny exact difference')
    print(json.dumps({'integer_point_pairs':len(points)**2,'accepted_obtuse':accepted,
        'rejected_nondomain':rejected,'transformed_rational_cases':transformed,
        'illegal_type_rejections':illegal,'article_hand_examples':len(examples),
        'near_right_exact_cases':3,'method':'finite side-square and shoelace oracle; not a universal proof'},sort_keys=True))

if __name__=='__main__':main()
