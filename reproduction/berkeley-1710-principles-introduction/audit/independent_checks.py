"""Independent bounded oracles. Run from any directory; no network or dependencies."""
from collections import Counter
from fractions import Fraction as F
import importlib.util
import itertools as it
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
model_path = ROOT / os.environ.get('AUDIT_MODEL', 'model.py')
spec = importlib.util.spec_from_file_location('audited_model', model_path)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
COUNTS = Counter()


def same(actual, expected, context=''):
    if actual != expected:
        raise AssertionError(f'{context}: actual={actual!r}; expected={expected!r}')


def rejects(action, classes=(TypeError, ValueError)):
    COUNTS['validation_rejections'] += 1
    try:
        action()
    except classes:
        return
    raise AssertionError('invalid input was accepted')


def linear():
    # Exhaust all two-row, one-variable systems and weights over {-1,0,1}.
    rows = list(it.product((-1, 0, 1), repeat=2))
    for (a, b), (c, d), weights in it.product(rows, rows, it.product((-1, 0, 1), repeat=2)):
        premises = (m.Premise('p', m.Equation(('x',), (a,), b)),
                    m.Premise('q', m.Equation(('x',), (c,), d)))
        expected = (F(weights[0]*a + weights[1]*c), F(weights[0]*b + weights[1]*d))
        target = m.Equation(('x',), (expected[0],), expected[1])
        cert = m.Certificate(weights)
        result = m.check_certificate(premises, target, cert)
        support = tuple(label for label, w in zip(('p', 'q'), weights) if w)
        same(result.valid, True, 'linear valid')
        same((result.combined.coefficients[0], result.combined.rhs), expected)
        same(result.dependencies, support, 'support')
        COUNTS['linear_system_weight_cases'] += 1
        for delta_a, delta_b in ((1,0), (0,1)):
            wrong = m.Equation(('x',), (expected[0]+delta_a,), expected[1]+delta_b)
            same(m.check_certificate(premises, wrong, cert).valid, False, 'perturbed target')
            COUNTS['linear_perturbed_targets'] += 1
        for bits in it.product((False, True), repeat=2):
            # Deliberately supply reverse order: deletion must preserve premise order.
            keep = tuple(label for label, bit in reversed(tuple(zip(('p','q'),bits))) if bit)
            permitted = all(not w or bit for w, bit in zip(weights, bits))
            if permitted:
                reduced, reduced_cert = m.restrict_certificate(premises, target, cert, keep)
                same(tuple(p.label for p in reduced), tuple(x for x in ('p','q') if x in keep))
                same(reduced_cert.weights, tuple(F(w) for w, bit in zip(weights,bits) if bit))
                same(m.check_certificate(reduced, target, reduced_cert).valid, True)
            else:
                rejects(lambda: m.restrict_certificate(premises, target, cert, keep), (ValueError,))
            COUNTS['linear_restriction_subsets'] += 1
        for x in (-2,-1,0,1,2):
            if all(not w or left*x == right for (left,right),w in zip(((a,b),(c,d)),weights)):
                same(expected[0]*x, expected[1], 'support semantic satisfaction')
                COUNTS['linear_satisfying_assignments'] += 1
    # Rational/large coefficients, independent from integer domain above.
    for u,v in it.product((F(-7,3),F(-1,2),F(0),F(2,5),F(10**40,7)), repeat=2):
        premises = (m.Premise('r',m.Equation(('x','y'),(F(1,3),F(-4,7)),F(5,11))),
                    m.Premise('s',m.Equation(('x','y'),(F(-2,3),F(9,7)),F(-5,13))))
        target = m.Equation(('x','y'),((u-2*v)/3,(-4*u+9*v)/7),5*u/11-5*v/13)
        same(m.check_certificate(premises,target,m.Certificate((u,v))).valid,True)
        COUNTS['linear_rational_cases'] += 1


def geometry():
    points = tuple(it.product((-1,0,1),repeat=2))
    for vertices in it.product(points, repeat=3):
        (ax,ay),(bx,by),(cx,cy) = vertices
        # Shoelace determinant, rather than the implementation's translated cross product.
        area = ax*by+bx*cy+cx*ay-ay*bx-by*cx-cy*ax
        COUNTS['triangle_vertex_tuples'] += 1
        if not area:
            rejects(lambda: m.Triangle(vertices), (ValueError,))
            COUNTS['triangle_degenerate'] += 1
            continue
        tri = m.Triangle(vertices)
        # Rightness independently means a zero incident-edge dot product at some vertex.
        right = any(sum((q[i]-p[i])*(r[i]-p[i]) for i in (0,1)) == 0
                    for p,q,r in (vertices,vertices[1:]+vertices[:1],vertices[2:]+vertices[:2]))
        same(tri.is_right(), right, 'dot-product rightness')
        distances = sorted(sum((p[i]-q[i])**2 for i in (0,1)) for p,q in it.combinations(vertices,2))
        same(tri.squared_sides(),tuple(distances))
        COUNTS['triangle_nondegenerate'] += 1
    domain = m.triangle_cases()
    for ordered, members, truth in it.product(it.permutations(domain),it.product((0,1),repeat=3),it.product((0,1),repeat=3)):
        denotation = frozenset(t for t,bit in zip(domain,members) if bit)
        sign = m.FiniteSign('s', ordered, denotation)
        lookup = dict(zip(domain,truth))
        called=[]
        def predicate(t):
            called.append(t)
            return bool(lookup[t])
        expected = next((t for t in ordered if t in denotation and not lookup[t]),None)
        actual=m.first_counterexample(sign,predicate)
        same(actual,expected,'finite first witness')
        same(sign.covers_domain(),all(members),'coverage')
        expected_calls=[]
        for t in ordered:
            if t in denotation:
                expected_calls.append(t)
                if not lookup[t]: break
        same(called,expected_calls,'domain-order short circuit')
        COUNTS['finite_sign_order_extension_predicate_cases'] += 1


# A separate tagged grammar, expanded repeated-variable words, and direct interpreter.
ATOMS = (('c',F(0)),('c',F(-1)),('c',F(1,2)),('v','x'),('v','y'))
LEVEL1 = tuple((op,a,b) for op in ('+','*') for a in ATOMS for b in ATOMS)
LEVEL2 = tuple((op,a,b) for op in ('+','*') for left,right in ((ATOMS,LEVEL1),(LEVEL1,ATOMS)) for a in left for b in right)
TREES = ATOMS+LEVEL1+LEVEL2
ENVS = tuple(dict(zip(('x','y'),values)) for values in it.product((F(-2),F(0),F(1,3)),repeat=2))


def build(t):
    if t[0]=='c': return m.Const(t[1])
    if t[0]=='v': return m.Var(t[1])
    return (m.Add if t[0]=='+' else m.Mul)(build(t[1]),build(t[2]))


def evaluate(t,env):
    if t[0]=='c': return t[1]
    if t[0]=='v': return env[t[1]]
    a,b=evaluate(t[1],env),evaluate(t[2],env)
    return a+b if t[0]=='+' else a*b


def words(t):
    if t[0]=='c': return {():t[1]} if t[1] else {}
    if t[0]=='v': return {(t[1],):F(1)}
    a,b=words(t[1]),words(t[2]); out=Counter()
    if t[0]=='+':
        for word,value in list(a.items())+list(b.items()): out[word]+=value
    else:
        for wa,ca in a.items():
            for wb,cb in b.items(): out[tuple(sorted(wa+wb))]+=ca*cb
    return {w:c for w,c in out.items() if c}


def actual_words(poly):
    return {tuple(name for name,power in monomial for _ in range(power)):coefficient
            for monomial,coefficient in poly.terms}


def replace(t,mapping):
    if t[0]=='c': return t
    if t[0]=='v': return mapping.get(t[1],t)
    return (t[0],replace(t[1],mapping),replace(t[2],mapping))


def polynomials():
    same(len(TREES),1055)
    for tree in TREES:
        expression=build(tree); polynomial=m.normalize(expression)
        same(actual_words(polynomial),words(tree),'independent word coefficients')
        COUNTS['polynomial_expression_trees'] += 1
        for env in ENVS:
            expected=evaluate(tree,env)
            same(m.evaluate_expr(expression,env),expected,'direct evaluation')
            same(m.evaluate_polynomial(polynomial,env),expected,'normal evaluation')
            COUNTS['polynomial_tree_assignments'] += 1
    replacements=(None,('v','x'),('v','y'),('c',F(-1,2)),('+',('v','x'),('v','y')),('*',('v','x'),('v','y')))
    for tree, sx,sy in it.product(ATOMS+LEVEL1,replacements,replacements):
        mapping={k:v for k,v in zip(('x','y'),(sx,sy)) if v is not None}
        expected=replace(tree,mapping)
        expression=build(tree)
        actual=m.substitute(expression,{k:build(v) for k,v in mapping.items()})
        same(actual,build(expected),'one-pass simultaneous AST')
        same(actual_words(m.normalize(actual)),words(expected),'substitution coefficients')
        COUNTS['simultaneous_substitution_tree_maps'] += 1
        for env in ENVS:
            induced={v:evaluate(mapping.get(v,('v',v)),env) for v in ('x','y')}
            value=evaluate(tree,induced)
            same(m.evaluate_expr(actual,env),value,'induced-environment equality')
            same(value,evaluate(expected,env),'independent substituted interpretation')
            COUNTS['simultaneous_substitution_assignments'] += 1


def validation():
    for bad in (True,False,0.1,'1',None,complex(1),[],{}):
        rejects(lambda bad=bad:m.exact(bad),(TypeError,))
        rejects(lambda bad=bad:m.Const(bad),(TypeError,))
    for bad in ('','a b','1x',1,None,True):
        rejects(lambda bad=bad:m.Var(bad))
    for args in (((),(),0),(['x'],(1,),0),(('x','x'),(1,2),0),(('x',),(1,2),0),(('x',),[1],0),(('x',),(0.1,),0),(('x',),(1,),False)):
        rejects(lambda args=args:m.Equation(*args))
    x=m.Var('x'); valid=m.Equation(('x',),(1,),1); premise=m.Premise('p',valid)
    for weights in ([1],(True,),(1.0,)): rejects(lambda weights=weights:m.Certificate(weights))
    for p,t,c in (([premise],valid,m.Certificate((1,))),((premise,),x,m.Certificate((1,))),((premise,),valid,(1,)),((premise,),valid,m.Certificate(())),((premise,premise),valid,m.Certificate((1,0)))):
        rejects(lambda p=p,t=t,c=c:m.check_certificate(p,t,c))
    for keep in (['p'],('unknown',),('p','p'),(True,)):
        rejects(lambda keep=keep:m.restrict_certificate((premise,),valid,m.Certificate((1,)),keep))
    for terms in ([],(1,),(((),0),),(((),True),),(((),1.0),),(((),1),((),2)),(((('x',0),),1),),(((('x',True),),1),),(((('y',1),('x',1)),1),),(((('x',1),('x',2)),1),)):
        rejects(lambda terms=terms:m.Polynomial(terms))
    for bad in (1,'x',m.Expr()):
        rejects(lambda bad=bad:m.normalize(bad))
        rejects(lambda bad=bad:m.evaluate_expr(bad,{}))
        rejects(lambda bad=bad:m.substitute(bad,{}))
        rejects(lambda bad=bad:m.Add(x,bad))
    for env in ([],{'x':True},{'x':1.0},{'x':1,'bad name':2},{'x':1,'unused':False}):
        rejects(lambda env=env:m.evaluate_expr(x,env))
        rejects(lambda env=env:m.evaluate_polynomial(m.normalize(x),env))
    rejects(lambda:m.evaluate_expr(x,{}),(KeyError,))
    rejects(lambda:m.evaluate_polynomial(m.normalize(x),{}),(KeyError,))
    for replacement in ([],{'x':1},{'bad name':x},{'unused':True}):
        rejects(lambda replacement=replacement:m.substitute(x,replacement))
    # No value for replaced x is required if its inserted image has no x.
    same(m.evaluate_expr(m.substitute(x,{'x':m.Const(7)}),{}),F(7))
    cancel=m.Add(x,m.Mul(m.Const(-1),x))
    rejects(lambda:m.evaluate_expr(cancel,{}),(KeyError,))
    same(m.evaluate_polynomial(m.normalize(cancel),{}),F(0))
    cases=m.triangle_cases()
    for domain,den in (((),frozenset()),(list(cases),frozenset()),((cases[0],cases[0]),frozenset()),((cases[0],),frozenset(cases)),(cases,set(cases))):
        rejects(lambda domain=domain,den=den:m.FiniteSign('s',domain,den))
    sign=m.FiniteSign('s',cases,frozenset(cases))
    rejects(lambda:m.first_counterexample(sign,lambda _:1),(TypeError,))
    rejects(lambda:m.first_counterexample(sign,None),(TypeError,))
    rejects(lambda:m.Triangle(((True,0),(1,0),(0,1))))
    rejects(lambda:m.Triangle(((0.0,0),(1,0),(0,1))))


def probe(name):
    x,y=m.Var('x'),m.Var('y')
    if name=='linear_rhs':
        same(m.check_certificate((m.Premise('p',m.Equation(('x',),(1,),2)),),m.Equation(('x',),(1,),3),m.Certificate((1,))).valid,False)
    elif name=='linear_coefficients':
        same(m.check_certificate((m.Premise('p',m.Equation(('x',),(1,),2)),),m.Equation(('x',),(2,),2),m.Certificate((1,))).valid,False)
    elif name=='zero_support':
        same(m.check_certificate((m.Premise('p',m.Equation(('x',),(1,),2)),),m.Equation(('x',),(0,),0),m.Certificate((0,))).dependencies,())
    elif name=='restriction_support':
        p=m.Premise('p',m.Equation(('x',),(1,),2));q=m.Premise('q',p.equation)
        rejects(lambda:m.restrict_certificate((p,q),m.Equation(('x',),(0,),0),m.Certificate((1,-1)),()),(ValueError,))
    elif name=='triangle_rightness': same(m.triangle_cases()[1].is_right(),False)
    elif name=='finite_coverage':
        d=m.triangle_cases();same(m.FiniteSign('s',d,frozenset((d[0],))).covers_domain(),False)
    elif name=='finite_denotation':
        d=m.triangle_cases();same(m.first_counterexample(m.FiniteSign('s',d,frozenset((d[0],))),lambda t:t.is_right()),None)
    elif name=='add_terms': same(actual_words(m.normalize(m.Add(x,y))),{('x',):F(1),('y',):F(1)})
    elif name=='multiply_exponents': same(actual_words(m.normalize(m.Mul(x,x))),{('x','x'):F(1)})
    elif name=='expr_multiplication': same(m.evaluate_expr(m.Mul(x,y),{'x':2,'y':3}),F(6))
    elif name=='polynomial_power': same(m.evaluate_polynomial(m.Polynomial((((("x",2),),F(1)),)),{'x':3}),F(9))
    elif name=='simultaneous_substitution': same(m.substitute(x,{'x':m.Add(y,m.Const(1)),'y':m.Const(2)}),m.Add(y,m.Const(1)))
    elif name=='reject_boolean': rejects(lambda:m.exact(True),(TypeError,))
    elif name=='framework_exception': raise RuntimeError('intentional framework classification probe')
    else: raise ValueError('unknown probe')


def main():
    try:
        if len(sys.argv)==3 and sys.argv[1]=='--probe': probe(sys.argv[2])
        else:
            linear();geometry();polynomials();validation()
    except AssertionError as error:
        print(json.dumps({'status':'semantic_failure','detail':str(error),'optimization':sys.flags.optimize},sort_keys=True))
        return 1
    except Exception as error:
        print(json.dumps({'status':'framework_error','exception':type(error).__name__,'detail':str(error),'optimization':sys.flags.optimize},sort_keys=True))
        return 2
    print(json.dumps({'status':'passed','optimization':sys.flags.optimize,'counts':dict(COUNTS)},sort_keys=True))
    return 0

if __name__=='__main__': sys.exit(main())
