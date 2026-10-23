"""Original finite, unary-set teaching model for Prior Analytics II.3.

Argument order is predicate, subject, matching the accompanying article.
No external libraries, historical fact database, or probability semantics.
"""
from dataclasses import dataclass
from itertools import combinations
import json

TERMS = ('M', 'P', 'S')
KINDS = ('A', 'E', 'I', 'O')
@dataclass(frozen=True)
class Model:
    universe: frozenset
    M: frozenset
    P: frozenset
    S: frozenset
    def __post_init__(self):
        for name in ('universe',) + TERMS:
            value = getattr(self, name)
            if not isinstance(value, frozenset):
                raise TypeError(name + ' must be a frozenset')
            if any(type(x) is not int or x < 0 for x in value):
                raise ValueError('objects must be nonnegative integers, not bools')
        if not self.universe:
            raise ValueError('universe must be nonempty')
        for name in TERMS:
            if not getattr(self, name) <= self.universe:
                raise ValueError(name + ' is outside the universe')
    def term(self, name):
        if name not in TERMS:
            raise ValueError('unknown term: ' + repr(name))
        return getattr(self, name)
    def to_dict(self):
        return {n: sorted(getattr(self,n)) for n in ('universe',) + TERMS}

def proposition(model, kind, predicate, subject):
    """A(X,Y): all Y are X; E: no Y is X; I: some Y is X; O: some Y is not X."""
    if not isinstance(model, Model):
        raise TypeError('expected Model')
    if kind not in KINDS:
        raise ValueError('unknown categorical kind')
    x, y = model.term(predicate), model.term(subject)
    if kind == 'A': return y <= x
    if kind == 'E': return not bool(y & x)
    if kind == 'I': return bool(y & x)
    return bool(y - x)

def classify(model, kind, predicate, subject):
    truth = proposition(model, kind, predicate, subject)
    if kind in ('I','O'):
        return 'true' if truth else 'false'
    y = model.term(subject)
    if not y: return 'vacuous_true'
    if truth: return 'true'
    contrary = 'E' if kind == 'A' else 'A'
    if proposition(model, contrary, predicate, subject): return 'wholly_false'
    return 'partly_false'

# Every tuple gives kind, predicate, subject. The middle term is M in both premises.
MOODS = {
    'Cesare': (('E','M','P'), ('A','M','S'), ('E','P','S')),
    'Camestres': (('A','M','P'), ('E','M','S'), ('E','P','S')),
    'Festino': (('E','M','P'), ('I','M','S'), ('O','P','S')),
    'Baroco': (('A','M','P'), ('O','M','S'), ('O','P','S')),
}

def evaluate(model, mood):
    if not isinstance(mood, str) or mood not in MOODS: raise ValueError('unknown mood')
    major, minor, conclusion = MOODS[mood]
    return {
        'major': classify(model,*major),
        'minor': classify(model,*minor),
        'conclusion': proposition(model,*conclusion),
        'truth_signature': ''.join('T' if proposition(model,*q) else 'F' for q in (major,minor,conclusion)),
    }

def type_model(types):
    """A type's bits are M=4, P=2, S=1. One representative per present type."""
    types = tuple(types)
    if any(type(t) is not int or not 0 <= t < 8 for t in types):
        raise ValueError('types must be integers 0..7')
    if len(set(types)) != len(types): raise ValueError('duplicate type')
    u = frozenset(types)
    return Model(u, frozenset(t for t in u if t & 4), frozenset(t for t in u if t & 2), frozenset(t for t in u if t & 1))

def all_models(require_nonempty_terms=False):
    if type(require_nonempty_terms) is not bool: raise TypeError('require_nonempty_terms must be bool')
    # Cardinality-first ordering certifies the saved witness's smallest universe
    # among these type models; lexicographic order breaks ties reproducibly.
    for size in range(1,9):
        for types in combinations(range(8), size):
            model = type_model(types)
            if not require_nonempty_terms or all(model.term(t) for t in TERMS):
                yield model

def census(require_nonempty_terms=False):
    rows = {m:{} for m in MOODS}
    model_count = 0
    for model in all_models(require_nonempty_terms):
        model_count += 1
        for mood in MOODS:
            r = evaluate(model,mood)
            if r['truth_signature'] == 'TTF':
                raise RuntimeError('validity failure: '+mood)
            key = '|'.join((r['major'],r['minor'],'T' if r['conclusion'] else 'F'))
            if key not in rows[mood]:
                rows[mood][key] = {'count':0,'smallest_type_witness':model.to_dict()}
            rows[mood][key]['count'] += 1
    return {'models':model_count, 'mood_evaluations':model_count*len(MOODS), 'rows':rows}

def true_combinations(report,mood):
    return {tuple(k.split('|')[:2]) for k in report['rows'][mood] if k.endswith('|T')}

def run():
    unrestricted, nonempty = census(), census(True)
    states = ('true','wholly_false','partly_false')
    for mood in ('Cesare','Camestres'):
        if true_combinations(nonempty,mood) != {(x,y) for x in states for y in states}:
            raise RuntimeError('universal status coverage failed')
    for mood in ('Festino','Baroco'):
        if true_combinations(nonempty,mood) != {(x,y) for x in states for y in ('true','false')}:
            raise RuntimeError('particular status coverage failed')
    return {'semantics':'modern unary sets; predicate-subject order; no probability claims',
            'unrestricted':unrestricted,'all_terms_nonempty':nonempty}

if __name__ == '__main__':
    import argparse
    import hashlib
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full',action='store_true',help='print all counts and smallest witnesses')
    args=parser.parse_args()
    report=run()
    canonical=json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if args.full:
        print(canonical,end='')
    else:
        print('full_report_sha256='+hashlib.sha256(canonical.encode()).hexdigest())
        for policy in ('unrestricted','all_terms_nonempty'):
            part=report[policy]
            print(policy+': models='+str(part['models'])+', mood_evaluations='+str(part['mood_evaluations']))
            for mood in MOODS:
                print(mood+': realized_status_outcomes='+str(len(part['rows'][mood]))+
                      ', true_conclusion_combinations='+str(sorted(true_combinations(part,mood))))
        print('validity failures: 0; universal 9-cell and particular 6-cell true coverage: PASS')
