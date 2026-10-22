"""Independent bounded regression audit; general proof is in the audit report."""
import hashlib
import itertools
import json
from fractions import Fraction
import model as m

counts = {'trans':0,'meet':0,'projection':0,'semantic_checks':0,'rejections':0,'rational_certificates':0}

def require(condition, label):
    if not condition:
        raise RuntimeError(label)

def reject(fn):
    try:
        fn()
    except m.InvalidCertificate:
        counts['rejections'] += 1
    else:
        raise RuntimeError('Invalid certificate was accepted')

atoms = [m.Atom(x) for x in 'abc']
terms = atoms + [m.And(a,b) for a in atoms for b in atoms]
valuations = [dict(zip('abc',v)) for v in itertools.product((False,True),repeat=3)]
def true(c,v):
    return not m.holds(c.source,v) or m.holds(c.target,v)

for p,q,r in itertools.product(terms,repeat=3):
    f = {'p':m.Inclusion(p,q),'q':m.Inclusion(q,r)}
    c = m.Inclusion(p,r)
    s = [m.Step(f['p'],'given',fact='p'),m.Step(f['q'],'given',fact='q'),m.Step(c,'trans',(0,1))]
    require(m.check(f,s,c),'trans rejected')
    counts['trans'] += 1
    for v in valuations:
        require(not all(true(x,v) for x in f.values()) or true(c,v),'trans unsound')
        counts['semantic_checks'] += 1
    f = {'p':m.Inclusion(p,q),'q':m.Inclusion(p,r)}
    c = m.Inclusion(p,m.And(q,r))
    s = [m.Step(f['p'],'given',fact='p'),m.Step(f['q'],'given',fact='q'),m.Step(c,'meet',(0,1))]
    require(m.check(f,s,c),'meet rejected')
    counts['meet'] += 1
    for v in valuations:
        require(not all(true(x,v) for x in f.values()) or true(c,v),'meet unsound')
        counts['semantic_checks'] += 1
for p,q in itertools.product(terms,repeat=2):
    for target,rule in [(p,'project-left'),(q,'project-right')]:
        c=m.Inclusion(m.And(p,q),target)
        require(m.check({},[m.Step(c,rule)],c),'projection rejected')
        counts['projection'] += 1
        for v in valuations:
            require(true(c,v),'projection unsound')
            counts['semantic_checks'] += 1

a,b,c=atoms
facts={'ab':m.Inclusion(a,b),'bc':m.Inclusion(b,c)}
base=[m.Step(facts['ab'],'given',fact='ab'),m.Step(facts['bc'],'given',fact='bc')]
goal=m.Inclusion(a,c)
for refs in [(1,0),(0,0),(2,1),(-1,1),(True,1),(0,1,1)]:
    reject(lambda refs=refs:m.check(facts,base+[m.Step(goal,'trans',refs)],goal))
reject(lambda:m.check(facts,base+[m.Step(goal,'invented-rule',(0,1))],goal))
reject(lambda:m.check({},[m.Step(goal,'given',fact='ab')],goal))
reject(lambda:m.check(facts,[m.Step(m.Inclusion(b,a),'given',fact='ab')],m.Inclusion(b,a)))
reject(lambda:m.check(facts,base,goal))
reject(lambda:m.check(facts,[],goal))
reject(lambda:m.check({},[m.Step(m.Inclusion(a,c),'project-left')],m.Inclusion(a,c)))
reject(lambda:m.check(facts,[m.Step(m.Inclusion(m.Atom(''),b),'given',fact='ab')],goal))

assumptions={'euclidean-parallel-configuration','adjacent-straight-angle'}
for n in range(-6,7):
    q=Fraction(n,7)
    cert=[('transfer-alpha',str(q)),('transfer-alpha',1-q),('transfer-beta',1),('straight-angle',1)]
    require(m.linear_check(cert,assumptions),'rational split rejected')
    counts['rational_certificates'] += 1
for mask in (set(),{'euclidean-parallel-configuration'},{'adjacent-straight-angle'}):
    reject(lambda mask=mask:m.linear_check([('transfer-alpha',1),('transfer-beta',1),('straight-angle',1)],mask))
for bad in (True,False,1.0,complex(1,0)):
    reject(lambda bad=bad:m.linear_check([('transfer-alpha',bad)],assumptions))
for coeff in (-2,-1,0,2,3):
    reject(lambda coeff=coeff:m.linear_check([('transfer-alpha',coeff),('transfer-beta',1),('straight-angle',1)],assumptions))
reject(lambda:m.linear_check([('not-an-equation',1)],assumptions))
reject(lambda:m.linear_check([('transfer-alpha',1)],assumptions,(1,0,0,-1,0)))
require(m.demo()['named_middle_count']==0,'named search unexpected')
require(m.demo()['expanded_middle_count']==1,'compound middle not found')
print(json.dumps({'status':'PASS','counts':counts,'scope':'bounded implementation checks, not a general theorem or geometry verification'},sort_keys=True,indent=2))
