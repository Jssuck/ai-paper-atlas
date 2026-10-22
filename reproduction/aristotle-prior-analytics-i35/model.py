"""Original teaching kernels, not a reconstruction of Aristotle's algorithm."""
from dataclasses import dataclass
from fractions import Fraction
import json

@dataclass(frozen=True)
class Atom:
    name: str

@dataclass(frozen=True)
class And:
    left: object
    right: object

def term_ok(t):
    return ((isinstance(t, Atom) and isinstance(t.name, str) and bool(t.name)) or
            (isinstance(t, And) and term_ok(t.left) and term_ok(t.right)))

def holds(t, valuation):
    if isinstance(t, Atom):
        return valuation[t.name]
    if isinstance(t, And):
        return holds(t.left, valuation) and holds(t.right, valuation)
    raise ValueError('invalid term')

@dataclass(frozen=True)
class Inclusion:
    source: object
    target: object

@dataclass(frozen=True)
class Step:
    claim: Inclusion
    rule: str
    refs: tuple = ()
    fact: str = ''

class InvalidCertificate(ValueError):
    pass

def check(facts, steps, goal):
    """Facts are explicit trusted assumptions. References must point backwards."""
    done = []
    for i, step in enumerate(steps):
        c = step.claim
        if not isinstance(c, Inclusion) or not term_ok(c.source) or not term_ok(c.target):
            raise InvalidCertificate('malformed claim')
        if any(type(r) is not int or r < 0 or r >= i for r in step.refs):
            raise InvalidCertificate('forward, cyclic or invalid reference')
        premises = [done[r] for r in step.refs]
        valid = False
        if step.rule == 'given':
            valid = not premises and step.fact in facts and facts[step.fact] == c
        elif step.rule == 'trans' and len(premises) == 2:
            p, q = premises
            valid = p.target == q.source and c == Inclusion(p.source, q.target)
        elif step.rule == 'meet' and len(premises) == 2:
            p, q = premises
            valid = p.source == q.source and c == Inclusion(p.source, And(p.target, q.target))
        elif step.rule == 'project-left':
            valid = not premises and isinstance(c.source, And) and c.target == c.source.left
        elif step.rule == 'project-right':
            valid = not premises and isinstance(c.source, And) and c.target == c.source.right
        if not valid:
            raise InvalidCertificate('unjustified ' + step.rule)
        done.append(c)
    if not done or done[-1] != goal:
        raise InvalidCertificate('wrong or missing final goal')
    return True

def named_middle(facts, source, target, vocabulary):
    """Only a two-edge search in the supplied finite vocabulary, NOT a decision procedure."""
    available = set(facts.values())
    return [m for m in vocabulary if Inclusion(source, m) in available
            and Inclusion(m, target) in available]

# Vectors denote a*alpha+b*beta+c*gamma+d*u+e*v+f = 0.
# Exact linear algebra only: geometry justification is an explicitly trusted input.
BASIS = ('alpha', 'beta', 'gamma', 'u', 'v', 'constant')
EQUATIONS = {
    'transfer-alpha': ((1,0,0,-1,0,0), frozenset({'euclidean-parallel-configuration'})),
    'transfer-beta': ((0,1,0,0,-1,0), frozenset({'euclidean-parallel-configuration'})),
    'straight-angle': ((0,0,1,1,1,-180), frozenset({'adjacent-straight-angle'})),
}
TARGET = (1,1,1,0,0,-180)

def linear_check(certificate, assumptions, target=TARGET):
    total = [Fraction(0) for _ in BASIS]
    if not certificate:
        raise InvalidCertificate('empty linear certificate')
    for name, coefficient in certificate:
        if name not in EQUATIONS:
            raise InvalidCertificate('unknown equation')
        if not isinstance(coefficient, (str, int, Fraction)) or isinstance(coefficient, bool):
            raise InvalidCertificate('use exact rational coefficients')
        q = Fraction(coefficient)
        vector, requirements = EQUATIONS[name]
        if not requirements <= set(assumptions):
            raise InvalidCertificate('missing geometric assumption')
        total = [a + q*b for a,b in zip(total,vector)]
    if tuple(total) != tuple(Fraction(x) for x in target):
        raise InvalidCertificate('linear identity mismatch')
    return True

def example():
    triangle, r, s, angle = map(Atom, ('triangle','parallel-extension','straight-arrangement','angle-sum-180'))
    middle = And(r,s)
    facts = {'r':Inclusion(triangle,r), 's':Inclusion(triangle,s), 'bridge':Inclusion(middle,angle)}
    steps = [Step(facts['r'],'given',fact='r'), Step(facts['s'],'given',fact='s'),
             Step(Inclusion(triangle,middle),'meet',(0,1)),Step(facts['bridge'],'given',fact='bridge'),
             Step(Inclusion(triangle,angle),'trans',(2,3))]
    check(facts,steps,Inclusion(triangle,angle))
    # The comparison supplies the already proved meet inclusion to both searches.
    expanded = dict(facts, meet=steps[2].claim)
    return facts, steps, expanded, triangle, middle, angle

def demo():
    facts,steps,expanded,t,m,a = example()
    cert = [('transfer-alpha',1),('transfer-beta',1),('straight-angle',1)]
    assumptions = {'euclidean-parallel-configuration','adjacent-straight-angle'}
    negative = {}
    for label, operation in {
        'missing_euclidean_assumption': lambda:linear_check(cert,{'adjacent-straight-angle'}),
        'wrong_coefficient':lambda:linear_check([('transfer-alpha',-1),*cert[1:]],assumptions),
        'circular_reference':lambda:check(facts,[Step(Inclusion(t,a),'trans',(0,0))],Inclusion(t,a)),
        'unsupported_new_name':lambda:check(facts,[Step(Inclusion(t,a),'given',fact='new-name')],Inclusion(t,a)),
    }.items():
        try:
            operation()
        except InvalidCertificate as e:
            negative[label]=str(e)
        else:
            raise RuntimeError('negative case unexpectedly accepted')
    return {'scope':'finite teaching certificates, not geometry verification',
            'proof_steps':len(steps),'named_middle_count':len(named_middle(expanded,t,a,[t,m.left,m.right,a])),
            'expanded_middle_count':len(named_middle(expanded,t,a,[t,m.left,m.right,a,m])),
            'linear_certificate_accepted':linear_check(cert,assumptions),
            'linear_target':list(TARGET),'rejected_cases':negative}

if __name__ == '__main__':
    print(json.dumps(demo(),ensure_ascii=False,indent=2))
