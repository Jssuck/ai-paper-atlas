"""Explicit modern set semantics and a small, syntactic teaching proof checker."""
from dataclasses import dataclass
from itertools import product

TERMS = ('S', 'P', 'M')

@dataclass(frozen=True)
class Proposition:
    kind: str
    subject: str
    predicate: str
    def __post_init__(self):
        if self.kind not in ('A', 'E', 'I', 'O'):
            raise ValueError('kind must be A/E/I/O')
        if self.subject not in TERMS or self.predicate not in TERMS:
            raise ValueError('terms must be S/P/M')
        if self.subject == self.predicate:
            raise ValueError('this teaching checker requires different terms')

def prop(kind, subject, predicate):
    return Proposition(kind, subject, predicate)

def validate_props(items):
    result = tuple(items)
    if any(not isinstance(x, Proposition) for x in result):
        raise TypeError('expected propositions')
    return result

def existence(items):
    result = tuple(items)
    if any(x not in TERMS for x in result):
        raise ValueError('unknown existence term')
    return frozenset(result)

def convert(p, nonempty=()):
    if not isinstance(p, Proposition):
        raise TypeError('expected proposition')
    ne = existence(nonempty)
    if p.kind in ('E', 'I'):
        return prop(p.kind, p.predicate, p.subject)
    if p.kind == 'A' and p.subject in ne:
        return prop('I', p.predicate, p.subject)
    raise ValueError('conversion unsupported or missing subject existence')

def negate(p):
    if not isinstance(p, Proposition):
        raise TypeError('expected proposition')
    return prop({'A':'O','O':'A','E':'I','I':'E'}[p.kind],p.subject,p.predicate)

def mood(figure, letters, s='S', p='P', m='M'):
    if type(figure) is not int or figure not in (1,2,3):
        raise ValueError('figure must be integer 1/2/3')
    if not isinstance(letters,str) or len(letters)!=3:
        raise ValueError('mood needs three letters')
    if set((s,p,m)) != set(TERMS):
        raise ValueError('three distinct named terms required')
    pairs = {1:((m,p),(s,m)),2:((p,m),(s,m)),3:((m,p),(m,s))}[figure]
    return (prop(letters[0],*pairs[0]),prop(letters[1],*pairs[1]),prop(letters[2],s,p))

# Named historical moods, interpreted only in the declared modern semantics.
MOODS = {
 'Barbara':(1,'AAA',()), 'Celarent':(1,'EAE',()),
 'Darii':(1,'AII',()), 'Ferio':(1,'EIO',()),
 'Cesare':(2,'EAE',()), 'Camestres':(2,'AEE',()),
 'Festino':(2,'EIO',()), 'Baroco':(2,'AOO',()),
 'Darapti':(3,'AAI',('M',)), 'Disamis':(3,'IAI',()),
 'Datisi':(3,'AII',()), 'Felapton':(3,'EAO',('M',)),
 'Bocardo':(3,'OAO',()), 'Ferison':(3,'EIO',())}

def first_figure(a,b):
    """Only Barbara/Celarent/Darii/Ferio, no existential weakening."""
    validate_props((a,b))
    if a.subject != b.predicate or len({a.subject,a.predicate,b.subject})!=3:
        raise ValueError('not a first-figure pair in major/minor order')
    kind = {('A','A'):'A',('E','A'):'E',('A','I'):'I',('E','I'):'O'}.get((a.kind,b.kind))
    if kind is None:
        raise ValueError('unsupported first-figure mood')
    return prop(kind,b.subject,a.predicate)

@dataclass(frozen=True)
class Step:
    rule: str
    refs: tuple
    output: Proposition
    def __post_init__(self):
        object.__setattr__(self,'refs',tuple(self.refs))
        if self.rule not in ('convert','first') or not isinstance(self.output,Proposition):
            raise ValueError('bad step')
        if any(type(i) is not int or i<0 for i in self.refs):
            raise ValueError('references must be nonnegative integers')
        if len(self.refs) != (1 if self.rule=='convert' else 2):
            raise ValueError('wrong reference count')

def check_steps(premises, steps, nonempty=()):
    lines=list(validate_props(premises)); ne=existence(nonempty); steps=tuple(steps)
    if any(not isinstance(st,Step) for st in steps):
        raise TypeError('expected steps')
    for st in steps:
        if any(i>=len(lines) for i in st.refs):
            raise ValueError('forward or missing reference')
        actual=convert(lines[st.refs[0]],ne) if st.rule=='convert' else first_figure(*(lines[i] for i in st.refs))
        if actual != st.output:
            raise ValueError('step output mismatch')
        lines.append(actual)
    return tuple(lines)

def verify(premises,steps,conclusion,nonempty=()):
    validate_props((conclusion,))
    lines=check_steps(premises,steps,nonempty)
    return bool(lines) and lines[-1]==conclusion

def reductio(premises, assumption, steps, conflict_refs, conclusion, nonempty=()):
    """One temporary assumption; conclusion must negate it exactly."""
    premises=validate_props(premises); validate_props((assumption,conclusion))
    refs=tuple(conflict_refs)
    if len(refs)!=2 or any(type(i) is not int or i<0 for i in refs):
        raise ValueError('two integer conflict references required')
    lines=check_steps(premises+(assumption,),steps,nonempty)
    if any(i>=len(lines) for i in refs):
        raise ValueError('missing conflict line')
    return conclusion==negate(assumption) and lines[refs[0]]==negate(lines[refs[1]])

def models():
    """128 membership-type models. None of S/P/M need exist."""
    types=tuple(product((False,True),repeat=3))[1:]
    for mask in range(1<<7):
        yield {t:frozenset(i for i,bits in enumerate(types) if mask>>i&1 and bits[j]) for j,t in enumerate(TERMS)}

def holds(p, model):
    validate_props((p,))
    if not isinstance(model,dict) or set(model)!=set(TERMS):
        raise ValueError('model must map exactly S/P/M')
    if any(not isinstance(v,(set,frozenset)) for v in model.values()):
        raise TypeError('model extensions must be sets')
    s,t=model[p.subject],model[p.predicate]
    return {'A':s<=t,'E':not(s&t),'I':bool(s&t),'O':bool(s-t)}[p.kind]

def countermodel(premises, conclusion, nonempty=()):
    premises=validate_props(premises); validate_props((conclusion,)); ne=existence(nonempty)
    for model in models():
        if all(model[t] for t in ne) and all(holds(p,model) for p in premises) and not holds(conclusion,model):
            return model
    return None

def demonstrations():
    P=prop; T=Step
    proofs={}
    # A first-figure proof from a converted second/third-figure presentation.
    for name in ('Cesare','Festino'):
        f,ls,ne=MOODS[name]; a,b,c=mood(f,ls)
        steps=(T('convert',(0,),convert(a)),T('first',(2,1),c))
        proofs[name]=( (a,b), steps,c,ne )
    a,b,c=mood(2,'AEE')
    q=convert(b); rev=P('E','P','S')
    proofs['Camestres']=((a,b),(T('convert',(1,),q),T('first',(2,0),rev),T('convert',(3,),c)),c,())
    for name in ('Datisi','Darapti','Felapton','Ferison'):
        f,ls,ne=MOODS[name]; a,b,c=mood(f,ls)
        q=convert(b,ne)
        proofs[name]=((a,b),(T('convert',(1,),q),T('first',(0,2),c)),c,ne)
    a,b,c=mood(3,'IAI'); q=convert(a); rev=P('I','P','S')
    proofs['Disamis']=((a,b),(T('convert',(0,),q),T('first',(1,2),rev),T('convert',(3,),c)),c,())
    return proofs

def indirect_demonstrations():
    P=prop; T=Step
    a,b,c=mood(2,'AOO'); h=negate(c); derived=P('A','S','M')
    baroco=((a,b),h,(T('first',(0,2),derived),),(1,3),c)
    a,b,c=mood(3,'OAO'); h=negate(c); derived=P('A','M','P')
    bocardo=((a,b),h,(T('first',(2,1),derived),),(0,3),c)
    return {'Baroco':baroco,'Bocardo':bocardo}
