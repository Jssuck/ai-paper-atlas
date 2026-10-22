"""Finite AEIO teaching models and explicit canonical-route search; no historical oracle."""
from itertools import product

KINDS = ('A', 'E', 'I', 'O')
TERMS = ('S', 'P', 'M')
BITS = {'S': 1, 'P': 2, 'M': 4}
CANONICAL = ((1,'AAA'),(1,'EAE'),(1,'AII'),(1,'EIO'),
             (2,'EAE'),(2,'AEE'),(2,'EIO'),(2,'AOO'),
             (3,'AAI'),(3,'IAI'),(3,'AII'),(3,'EAO'),(3,'OAO'),(3,'EIO'))
CONTRADICTORY = {'A':'O','E':'I','I':'E','O':'A'}

def validate_model(mask):
    if type(mask) is not int or not 1 <= mask <= 255:
        raise ValueError('model must be an integer 1..255, not bool; domain is nonempty')
    return mask

def validate_kind(kind):
    if not isinstance(kind, str) or kind not in KINDS:
        raise ValueError('kind must be exactly A, E, I or O')
    return kind

def validate_term(term):
    if not isinstance(term, str) or term not in TERMS:
        raise ValueError('term must be exactly S, P or M')
    return term

def truth(kind, subject, predicate, mask):
    validate_kind(kind); validate_term(subject); validate_term(predicate); validate_model(mask)
    occupied = [t for t in range(8) if mask & (1 << t)]
    subj = [t for t in occupied if t & BITS[subject]]
    inside = [t for t in subj if t & BITS[predicate]]
    return {'A':len(inside)==len(subj), 'E':not inside,
            'I':bool(inside), 'O':len(inside)<len(subj)}[kind]

def term_nonempty(term, mask):
    validate_term(term); validate_model(mask)
    return any(mask & (1 << t) and t & BITS[term] for t in range(8))

def models(require_nonempty_terms=False):
    if type(require_nonempty_terms) is not bool:
        raise ValueError('policy must be bool')
    return tuple(m for m in range(1,256) if not require_nonempty_terms or
                 all(term_nonempty(t,m) for t in TERMS))

def validate_route(figure, mood):
    if type(figure) is not int or figure not in (1,2,3):
        raise ValueError('figure must be integer 1, 2, or 3, not bool')
    if not isinstance(mood,str) or len(mood)!=3 or any(k not in KINDS for k in mood):
        raise ValueError('mood must be three uppercase AEIO letters')
    return figure,mood

def premises(figure, mood):
    validate_route(figure,mood)
    pairs = {1:(('M','P'),('S','M')),2:(('P','M'),('S','M')),3:(('M','P'),('M','S'))}[figure]
    return tuple((kind,*pair) for kind,pair in zip(mood[:2],pairs))

def countermodels(figure, mood, require_nonempty_terms=False):
    ps=premises(figure,mood)
    return tuple(m for m in models(require_nonempty_terms) if
                 all(truth(*p,m) for p in ps) and not truth(mood[2],'S','P',m))

def classifications(require_nonempty_terms=False):
    models(require_nonempty_terms)  # validate even if called under optimization
    return tuple((f,''.join(m)) for f in (1,2,3) for m in product(KINDS,repeat=3)
                 if not countermodels(f,''.join(m),require_nonempty_terms))

def canonical_counts():
    return {k:sum(m[-1]==k for _,m in CANONICAL) for k in KINDS}

def search(target, available):
    """Count canonical candidate inspections, not runtime or premise-discovery effort.

    available is a tuple of (figure, mood) certificates assumed already established.
    No attempt is made to infer whether premises hold or certificates can be found.
    """
    validate_kind(target)
    if type(available) is not tuple:
        raise ValueError('available must be a tuple of canonical route pairs')
    for route in available:
        if type(route) is not tuple or len(route)!=2:
            raise ValueError('route must be a pair')
        validate_route(*route)
        if route not in CANONICAL:
            raise ValueError('search only accepts the declared 14 canonical routes')
    if len(set(available))!=len(available):
        raise ValueError('duplicate available route')
    checks=0
    for route in CANONICAL:
        if route[1][-1] != target:
            continue
        checks+=1
        if route in available:
            return {'target':target,'inspections':checks,'found':list(route)}
    return {'target':target,'inspections':checks,'found':None}
