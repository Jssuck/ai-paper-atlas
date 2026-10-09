"""Finite checks of Huntington (1904), pp. 292–309; Python stdlib only.

Original operations need not be closed. Equational guards are NOT dropped.
Complements are derived candidates, not a primitive operation chosen in advance.
This is a finite model checker, not a general theorem prover.
"""
from dataclasses import dataclass, field
from itertools import product


@dataclass
class Check:
    holds: bool = True
    checked: int = 0
    skipped: int = 0
    failures: list = field(default_factory=list)
    note: str = ''

    def add(self, truth, witness=None):
        self.checked += 1
        if not truth:
            self.holds = False
            if len(self.failures) < 3:
                self.failures.append(witness)


class OutsideOperand(Exception):
    pass


@dataclass
class Algebra:
    elements: tuple
    operations: dict
    name: str = ''

    def __post_init__(self):
        self.elements = tuple(self.elements)
        if not self.elements or len(set(self.elements)) != len(self.elements):
            raise ValueError('Use a nonempty domain with distinct hashable elements')
        pairs = set(product(self.elements, repeat=2))
        for table in self.operations.values():
            if set(table) != pairs:
                raise ValueError('Each operation must specify exactly K x K')

    def op(self, symbol, a, b):
        if a not in self.elements or b not in self.elements:
            raise OutsideOperand('Do not feed an external result back into a K-rule')
        return self.operations[symbol][a, b]

    def expression(self, term, env):
        if isinstance(term, str):
            return env[term]
        symbol, left, right = term
        a, b = self.expression(left, env), self.expression(right, env)
        out = self.op(symbol, a, b)
        if out not in self.elements:
            raise OutsideOperand('An indicated intermediate result lies outside K')
        return out


def table(labels, rows):
    if len(rows) != len(labels) or any(len(row) != len(labels) for row in rows):
        raise ValueError('Table dimensions must match labels')
    return {(a, b): rows[i][j] for i, a in enumerate(labels) for j, b in enumerate(labels)}


def equation(model, variables, left, right):
    result = Check()
    for vals in product(model.elements, repeat=len(variables)):
        env = dict(zip(variables, vals))
        try:
            lv = model.expression(left, env)
            rv = model.expression(right, env)
        except OutsideOperand:
            result.skipped += 1
            continue
        result.add(lv == rv, {'assignment': env, 'left': lv, 'right': rv})
    return result


def closure(model, symbol):
    r = Check()
    for (a, b), value in model.operations[symbol].items():
        r.add(value in model.elements, {'a': a, 'b': b, 'output': value})
    return r


def statement(value, witness=None, note=''):
    r = Check(note=note)
    r.add(bool(value), witness)
    return r


def identities(model, symbol):
    return [z for z in model.elements if all(model.op(symbol, a, z) == a for a in model.elements)]


def first(model):
    """Ten postulates in §1. V is conditional on unique right identities."""
    K = model.elements
    s, t = '+', '*'
    zeros, ones = identities(model, s), identities(model, t)
    checks = {'Ia': closure(model, s), 'Ib': closure(model, t),
              'IIa': statement(zeros, {'candidates': zeros}),
              'IIb': statement(ones, {'candidates': ones}),
              'IIIa': equation(model, 'ab', (s,'a','b'), (s,'b','a')),
              'IIIb': equation(model, 'ab', (t,'a','b'), (t,'b','a')),
              'IVa': equation(model, 'abc', (s,'a',(t,'b','c')), (t,(s,'a','b'),(s,'a','c'))),
              'IVb': equation(model, 'abc', (t,'a',(s,'b','c')), (s,(t,'a','b'),(t,'a','c')))}
    v = Check()
    if len(zeros) == len(ones) == 1:
        for a in K:
            cs = [b for b in K if model.op(s,a,b)==ones[0] and model.op(t,a,b)==zeros[0]]
            v.add(bool(cs), {'a':a, 'complements':cs})
    else:
        v.note = 'V vacuous: identities do not both exist uniquely'
    checks['V'] = v
    checks['VI'] = statement(len(K)>=2, {'size':len(K)})
    return checks


@dataclass
class Relation:
    elements: tuple
    pairs: frozenset
    name: str = ''

    def __post_init__(self):
        self.elements = tuple(self.elements)
        self.pairs = frozenset(self.pairs)
        if not self.elements or len(set(self.elements)) != len(self.elements):
            raise ValueError('Use a nonempty domain with distinct elements')
        if not self.pairs <= set(product(self.elements, repeat=2)):
            raise ValueError('Relation contains an endpoint outside K')

    def le(self, a, b):
        return (a,b) in self.pairs


def relation_from_rows(labels, rows, name=''):
    t = table(labels, rows)
    return Relation(tuple(labels), frozenset(p for p,v in t.items() if v), name)


def relation_complements(model, zero, one):
    K, R = model.elements, model.le
    return {a:[b for b in K if
        all(not(R(x,a) and R(x,b)) or x==zero for x in K) and
        all(not(R(a,y) and R(b,y)) or y==one for y in K)] for a in K}


def second(model):
    """§2, including deliberately redundant #6 and #7. R means 'within'."""
    K, R = model.elements, model.le
    c = {str(i):Check() for i in range(1,11)}
    for a in K: c['1'].add(R(a,a), {'a':a})
    for a,b in product(K,repeat=2):
        c['2'].add(not(R(a,b) and R(b,a)) or a==b, {'a':a,'b':b})
    for a,b,d in product(K,repeat=3):
        c['3'].add(not(R(a,b) and R(b,d)) or R(a,d), {'a':a,'b':b,'c':d})
    # Original #4/#5 intentionally exempt equality; cannot replace with modern bounds.
    zeros = [z for z in K if all(a==z or R(z,a) for a in K)]
    ones = [u for u in K if all(a==u or R(a,u) for a in K)]
    c['4'] = statement(zeros, {'candidates':zeros})
    c['5'] = statement(ones, {'candidates':ones})
    for a,b in product(K,repeat=2):
        if a==b or R(a,b) or R(b,a):
            c['6'].skipped += 1; c['7'].skipped += 1
            continue
        joins=[s for s in K if R(a,s) and R(b,s) and
               all(y==s or not(R(a,y) and R(b,y)) or R(s,y) for y in K)]
        meets=[p for p in K if R(p,a) and R(p,b) and
               all(x==p or not(R(x,a) and R(x,b)) or R(x,p) for x in K)]
        c['6'].add(bool(joins), {'a':a,'b':b,'joins':joins})
        c['7'].add(bool(meets), {'a':a,'b':b,'meets':meets})
    unique = len(zeros)==len(ones)==1
    complements = relation_complements(model,zeros[0],ones[0]) if unique else {b:list(K) for b in K}
    if unique:
        for a in K: c['8'].add(bool(complements[a]), {'a':a,'complements':complements[a]})
    else: c['8'].note='8 vacuous: bounds do not both exist uniquely'
    if all(c[str(i)].holds for i in (1,4,5,8)):
        # For nonunique bounds use all possible supplements. This convention is
        # immaterial for the original universal-relation witness: antecedent false.
        for z in zeros:
            for a,b in product(K,repeat=2):
                for bar in complements[b]:
                    if R(a,bar):
                        c['9'].skipped += 1
                        continue
                    xs=[x for x in K if x!=z and R(x,a) and R(x,b)]
                    c['9'].add(bool(xs), {'a':a,'b':b,'bar_b':bar,'zero':z,'witnesses':xs})
    else: c['9'].note='9 vacuous: one of 1,4,5,8 is false'
    c['10']=statement(len(K)>=2, {'size':len(K)})
    return c


def operation_complements(model, zero, one):
    K = model.elements
    op = lambda a,b:model.op('+',a,b)
    return {a:[b for b in K if op(a,b)==one and
               all(not(op(x,a)==a and op(x,b)==b) or x==zero for x in K)] for a in K}


def third(model):
    """Nine §3 postulates. H's original antecedent is A,D,E,G (not A,B,E,G)."""
    K = model.elements
    op = lambda a,b:model.op('+',a,b)
    zeros = identities(model,'+')
    ones = [u for u in K if all(op(u,a)==u for a in K)]
    c = {'A':equation(model,'a',('+','a','a'),'a'),
         'B':equation(model,'ab',('+','a','b'),('+','b','a')),
         'C':equation(model,'abc',('+',('+','a','b'),'c'),('+','a',('+','b','c'))),
         'D':statement(zeros, {'candidates':zeros}),
         'E':statement(ones, {'candidates':ones}), 'F':closure(model,'+'), 'G':Check()}
    unique = len(zeros)==len(ones)==1
    complements = operation_complements(model,zeros[0],ones[0]) if unique else {b:list(K) for b in K}
    if unique:
        for a in K: c['G'].add(bool(complements[a]), {'a':a,'complements':complements[a]})
    else: c['G'].note='G vacuous: bounds do not both exist uniquely'
    h = Check()
    if all(c[k].holds for k in ('A','D','E','G')):
        for z in zeros:
            for a,b in product(K,repeat=2):
                for bar in complements[b]:
                    if op(a,bar)==bar:
                        h.skipped += 1
                        continue
                    xs=[x for x in K if x!=z and op(a,x)==a and op(b,x)==b]
                    h.add(bool(xs), {'a':a,'b':b,'bar_b':bar,'zero':z,'witnesses':xs})
    else: h.note='H vacuous: one of A,D,E,G is false'
    c['H']=h
    c['J']=statement(len(K)>=2, {'size':len(K)})
    return c


def failed(checks):
    return [k for k,v in checks.items() if not v.holds]


def powerset_algebra(bits):
    if not isinstance(bits,int) or isinstance(bits,bool) or not 0<=bits<=6:
        raise ValueError('Teaching constructor supports 0..6 bits; experiments use <=4')
    K=tuple(range(1<<bits))
    return Algebra(K, {'+':{(a,b):a|b for a,b in product(K,repeat=2)},
                       '*':{(a,b):a&b for a,b in product(K,repeat=2)}},f'powerset_{bits}')


def induced_relation(model):
    K=model.elements
    return Relation(K,frozenset((a,b) for a,b in product(K,repeat=2) if model.op('+',a,b)==b),model.name)


def first_original_models():
    """Exact p.296 rows; x is an external output, NOT a third K element."""
    rows={
        'Ia': ([0,1,1,'outside'],[0,0,0,1]),
        'Ib': ([0,1,1,1],['outside',0,0,1]),
        'IIa':([0,0,0,0],[0,0,0,1]),
        'IIb':([0,1,1,1],[1,1,1,1]),
        'IIIa':([0,0,1,1],[0,0,0,1]),
        'IIIb':([0,1,1,1],[0,0,1,1]),
        'IVa':([0,1,1,0],[0,0,0,1]),
        'IVb':([0,1,1,1],[1,0,0,1]),
        'V':([0,1,1,1],[0,1,1,1])}
    models={k:Algebra((0,1),{'+':dict(zip(product((0,1),repeat=2),s)),
                             '*':dict(zip(product((0,1),repeat=2),t))},k) for k,(s,t) in rows.items()}
    models['VI']=powerset_algebra(0)
    return models


def fourteen_domain():
    # Integer mask encodes digits 1..4; common subscript digit 0 is suppressed.
    # Missing u014 -> bits 1,4 -> 9; missing u023 -> bits 2,3 -> 6.
    return tuple(a for a in range(16) if a not in (6,9))


def mask_label(mask):
    return 'u0'+''.join(str(i+1) for i in range(4) if mask & (1<<i))


def second_original_models():
    models={
        '1':relation_from_rows((2,0,1,3),[(1,0,1,0),(1,0,1,1),(0,0,0,0),(0,0,1,1)],'p302_1'),
        '2':Relation((0,1),frozenset(product((0,1),repeat=2)),'p303_2'),
        '3':relation_from_rows((4,2,0,1,3,5),[
            (1,0,0,1,1,0),(1,1,0,1,0,0),(1,1,1,1,1,1),
            (0,0,0,1,0,0),(0,0,0,1,1,1),(0,1,0,1,0,1)],'p303_3'),
        '6,7':Relation(fourteen_domain(),frozenset((a,b) for a,b in product(fourteen_domain(),repeat=2) if a&b==a),'p303_6_7'),
        '8':relation_from_rows((0,2,1),[(1,1,1),(0,1,1),(0,0,1)],'p304_8'),
        '9':relation_from_rows((0,2,3,4,1),[(1,1,1,1,1),(0,1,0,1,1),(0,0,1,0,1),(0,0,0,1,1),(0,0,0,0,1)],'p304_9'),
        '10':Relation((0,),frozenset({(0,0)}),'p304_10')}
    return models


def third_original_models():
    K=fourteen_domain()
    return {
        'B':Algebra((0,1),{'+':{(a,b):a for a,b in product((0,1),repeat=2)}},'p307_B'),
        'C':Algebra((4,2,0,1,3,5),{'+':table((4,2,0,1,3,5),[
            (4,4,4,1,3,1),(4,2,2,1,1,2),(4,2,0,1,3,5),
            (1,1,1,1,1,1),(3,1,3,1,3,5),(1,2,5,1,5,5)])},'p307_C'),
        'F':Algebra(K,{'+':{(a,b):a|b for a,b in product(K,repeat=2)}},'p308_F'),
        'G':Algebra((0,2,1),{'+':table((0,2,1),[(0,2,1),(2,2,1),(1,1,1)])},'p308_G'),
        'H':Algebra((0,2,3,4,1),{'+':table((0,2,3,4,1),[
            (0,2,3,4,1),(2,2,1,4,1),(3,1,3,1,1),(4,4,1,4,1),(1,1,1,1,1)])},'p308_H'),
        'J':Algebra((0,),{'+':{(0,0):0}},'p308_J')}


def teaching_saturated_addition():
    """Modern 3-element replacement for A, not Huntington's infinite example."""
    K=(0,1,2)
    return Algebra(K,{'+':{(a,b):min(2,a+b) for a,b in product(K,repeat=2)}},'teaching_saturated_addition')


def small_enumeration():
    """Bounded complete labelled enumerations, NOT isomorphism classes."""
    result={'first':[], 'second':[], 'third':[]}
    for n in (1,2):
        K=tuple(range(n)); pairs=tuple(product(K,repeat=2)); total=valid=0
        for values in product(K,repeat=2*n*n):
            m=Algebra(K,{'+':dict(zip(pairs,values[:n*n])), '*':dict(zip(pairs,values[n*n:]))})
            total+=1; valid+=not failed(first(m))
        result['first'].append({'n':n,'checked':total,'valid':valid})
    for n in (1,2,3):
        K=tuple(range(n)); pairs=tuple(product(K,repeat=2)); total=valid=0
        for values in product((False,True),repeat=n*n):
            m=Relation(K,frozenset(p for p,v in zip(pairs,values) if v))
            total+=1; valid+=not failed(second(m))
        result['second'].append({'n':n,'checked':total,'valid':valid})
    for n in (1,2,3):
        K=tuple(range(n)); pairs=tuple(product(K,repeat=2)); total=valid=0
        for values in product(K,repeat=n*n):
            m=Algebra(K,{'+':dict(zip(pairs,values))})
            total+=1; valid+=not failed(third(m))
        result['third'].append({'n':n,'checked':total,'valid':valid})
    return result
