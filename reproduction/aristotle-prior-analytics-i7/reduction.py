"""Original teaching reconstruction of I.7; not Aristotle's own algorithm."""
from itertools import combinations, product
from functools import lru_cache

TERMS = ('P', 'S', 'M')
BITS = {'P': 4, 'S': 2, 'M': 1}
QS = ('A', 'E', 'I', 'O')
NEG = {'A': 'O', 'O': 'A', 'E': 'I', 'I': 'E'}
MOODS = {
 'Barbara': (1,'A','A','A'), 'Celarent':(1,'E','A','E'),
 'Darii':(1,'A','I','I'), 'Ferio':(1,'E','I','O'),
 'Cesare':(2,'E','A','E'), 'Camestres':(2,'A','E','E'),
 'Festino':(2,'E','I','O'), 'Baroco':(2,'A','O','O'),
 'Darapti':(3,'A','A','I'), 'Felapton':(3,'E','A','O'),
 'Disamis':(3,'I','A','I'), 'Datisi':(3,'A','I','I'),
 'Bocardo':(3,'O','A','O'), 'Ferison':(3,'E','I','O')}


def prop(p):
    if not isinstance(p, (tuple,list)) or len(p)!=3:
        raise ValueError('proposition must have three fields')
    q,x,y=p
    if q not in QS or x not in TERMS or y not in TERMS:
        raise ValueError('invalid proposition symbol')
    return q,x,y


def checked_support(s):
    if not isinstance(s,(list,tuple,set,frozenset)) or not s:
        raise ValueError('support must be nonempty collection')
    if any(type(t) is not int or not 0<=t<=7 for t in s):
        raise ValueError('types must be integers 0..7')
    if len(s)!=len(set(s)):
        raise ValueError('duplicate types')
    return tuple(sorted(s))


def truth(p,s):
    q,x,y=prop(p); s=checked_support(s)
    both=any(t & BITS[x] and t & BITS[y] for t in s)
    outside=any(t & BITS[x] and not t & BITS[y] for t in s)
    return bool({'A':not outside,'E':not both,'I':both,'O':outside}[q])


def policy_required(policy):
    if policy not in ('allow-empty','all-nonempty'):
        raise ValueError('unknown policy')
    return () if policy=='allow-empty' else TERMS


@lru_cache(None)
def supports(policy='allow-empty'):
    required=policy_required(policy)
    return tuple(s for n in range(1,9) for s in combinations(range(8),n)
                 if all(any(t & BITS[x] for t in s) for x in required))


def premises(figure,q,r):
    if type(figure) is not int or figure not in (1,2,3):
        raise ValueError('figure must be 1,2,3')
    pairs={1:(('M','P'),('S','M')),2:(('P','M'),('S','M')),3:(('M','P'),('M','S'))}[figure]
    return prop((q,*pairs[0])),prop((r,*pairs[1]))


def negate(p):
    q,x,y=prop(p); return NEG[q],x,y


def countermodel(ps,goal,policy='allow-empty'):
    ps=tuple(prop(p) for p in ps); goal=prop(goal)
    for s in supports(policy):
        if all(truth(p,s) for p in ps) and not truth(goal,s):
            return s
    return None


def classify(figure,q,r,policy='allow-empty'):
    ps=premises(figure,q,r)
    return {direction:[c for c in QS if countermodel(ps,(c,x,y),policy) is None]
            for direction,x,y in [('forward','S','P'),('reverse','P','S')]}


def make_certificate(ps,goal,policy='allow-empty'):
    """Finite proof search, not completeness claim. RAA uses explicit clash."""
    ps=tuple(prop(p) for p in ps); goal=prop(goal)
    lines=[]; known={}
    def add(p,rule,refs=()):
        p=prop(p)
        if p not in known:
            known[p]=len(lines); lines.append({'p':list(p),'rule':rule,'refs':list(refs)})
    for p in ps: add(p,'premise')
    for x in policy_required(policy): add(('I',x,x),'existence')
    assumed=negate(goal)
    known[assumed]=len(lines)
    lines.append({'p':list(assumed),'rule':'assumption','refs':[]})
    changed=True
    while changed:
        old=len(lines)
        for p,i in list(known.items()):
            q,x,y=p
            if q in ('E','I'): add((q,y,x),'conversion',(i,))
        for p,i in list(known.items()):
            q,m,pred=p
            if q not in ('A','E'): continue
            for s in TERMS:
                minor=('A',s,m)
                if minor in known:
                    add((q,s,pred),'Barbara' if q=='A' else 'Celarent',(i,known[minor]))
        changed=len(lines)>old
    for p,i in known.items():
        if negate(p) in known:
            cert={'premises':[list(p) for p in ps],'goal':list(goal),'policy':policy,
                  'lines':lines,'clash':[i,known[negate(p)]]}
            verify_certificate(cert)
            return cert
    return None


def verify_certificate(cert):
    """Local syntactic proof kernel; never calls finite semantic enumeration."""
    if not isinstance(cert,dict): raise ValueError('certificate must be object')
    ps=[prop(p) for p in cert['premises']]; goal=prop(cert['goal'])
    required=policy_required(cert['policy']); checked=[]; assumed=False
    for line in cert['lines']:
        p=prop(line['p']); q,x,y=p; rule=line['rule']; refs=line['refs']
        if not isinstance(refs,list) or any(type(i) is not int or i<0 or i>=len(checked) for i in refs):
            raise ValueError('reference must point to earlier line')
        parents=[checked[i] for i in refs]
        if rule=='premise': valid=not refs and p in ps
        elif rule=='existence': valid=not refs and q=='I' and x==y and x in required
        elif rule=='assumption':
            valid=not refs and p==negate(goal); assumed=assumed or valid
        elif rule=='conversion':
            valid=len(parents)==1 and parents[0][0] in ('E','I') and p==(parents[0][0],parents[0][2],parents[0][1])
        elif rule in ('Barbara','Celarent'):
            expected='A' if rule=='Barbara' else 'E'
            valid=(len(parents)==2 and parents[0][0]==expected and parents[1][0]=='A'
                   and parents[0][1]==parents[1][2] and p==(expected,parents[1][1],parents[0][2]))
        else: valid=False
        if not valid: raise ValueError('invalid inference: '+str(rule))
        checked.append(p)
    clash=cert['clash']
    if (not isinstance(clash,list) or len(clash)!=2 or any(type(i) is not int or i<0 or i>=len(checked) for i in clash)
        or checked[clash[1]]!=negate(checked[clash[0]]) or not assumed):
        raise ValueError('missing contradictory pair or assumption')
    return True


def named_certificate(name,policy='all-nonempty'):
    if name not in MOODS: raise ValueError('unknown mood')
    f,q,r,c=MOODS[name]
    return make_certificate(premises(f,q,r),(c,'S','P'),policy)


def explicit_first_figure(name):
    """Short chapter-aligned Darii/Ferio paths using Celarent, not themselves."""
    if name not in ('Darii','Ferio'): raise ValueError('choose Darii or Ferio')
    f,q,r,c=MOODS[name]; ps=premises(f,q,r); goal=(c,'S','P')
    lines=[{'p':list(p),'rule':'premise','refs':[]} for p in ps]
    lines.append({'p':list(negate(goal)),'rule':'assumption','refs':[]})
    if name=='Darii':
        lines.extend([{'p':['E','P','S'],'rule':'conversion','refs':[2]},
                      {'p':['E','M','S'],'rule':'Celarent','refs':[3,0]},
                      {'p':['E','S','M'],'rule':'conversion','refs':[4]}])
    else:
        lines.extend([{'p':['E','P','M'],'rule':'conversion','refs':[0]},
                      {'p':['E','S','M'],'rule':'Celarent','refs':[3,2]}])
    cert={'premises':[list(p) for p in ps],'goal':list(goal),'policy':'allow-empty','lines':lines,'clash':[1,len(lines)-1]}
    verify_certificate(cert); return cert
