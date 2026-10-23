#!/usr/bin/env python3
"""Independent reviewer: quantifiers on Boolean tuples, no author-module import."""
import itertools
import json
from pathlib import Path

TYPES = tuple(itertools.product((False, True), repeat=3))
INDEX = {'A': 0, 'B': 1, 'C': 2}

def truth(proposition, domain):
    kind, predicate, subject = proposition
    p, s = INDEX[predicate], INDEX[subject]
    if kind == 'A': return all(not x[s] or x[p] for x in domain)
    if kind == 'E': return all(not (x[s] and x[p]) for x in domain)
    if kind == 'I': return any(x[s] and x[p] for x in domain)
    if kind == 'O': return any(x[s] and not x[p] for x in domain)
    raise ValueError(kind)

def require(test, label):
    if not test: raise RuntimeError(label)

def text(p): return f'{p[0]}({p[1]},{p[2]})'

def parse(s): return (s[0], s[2], s[4])

MOODS = {
    'Camestres': (('A','A','B'), ('E','A','C'), ('E','B','C')),
    'Cesare': (('E','A','B'), ('A','A','C'), ('E','B','C')),
    'Festino': (('E','A','B'), ('I','A','C'), ('O','B','C')),
    'Baroco': (('A','A','B'), ('O','A','C'), ('O','B','C')),
}
# Each row: contrary retain major/minor, contradictory retain major/minor.
EXPECTED_RESULTS = {
    'Camestres': [('A','A','C'), ('O','A','B'), ('I','A','C'), ('O','A','B')],
    'Cesare': [('E','A','C'), ('I','A','B'), ('O','A','C'), ('I','A','B')],
    'Festino': [('O','A','C'), None, ('E','A','C'), ('I','A','B')],
    'Baroco': [('I','A','C'), None, ('A','A','C'), ('O','A','B')],
}

def main():
    author = json.loads(Path(__file__).with_name('results.json').read_text())
    domains = [d for n in range(1,9) for d in itertools.combinations(TYPES,n)]
    rows_checked = 0
    witness_checks = 0
    for policy, population in [('empty_allowed',255), ('C_nonempty',240), ('all_nonempty',218)]:
        ds = [d for d in domains if policy == 'empty_allowed'
              or (policy == 'C_nonempty' and any(x[2] for x in d))
              or (policy == 'all_nonempty' and all(any(x[i] for x in d) for i in range(3)))]
        require(len(ds)==population, 'population')
        report = author['policies'][policy]
        require(report['model_count']==population, 'stored population')
        actual = {row['id']:row for row in report['cases']}
        require(len(actual)==16, 'row coverage')
        for name, (major,minor,conclusion) in MOODS.items():
            base = [d for d in ds if truth(major,d) and truth(minor,d)]
            require(all(truth(conclusion,d) for d in base), 'original validity')
            require(report['original_moods'][name]=={'premise_models':len(base),'countermodels':0}, 'original report')
            for mode in ('contrary','contradictory'):
                replacement = (('A' if conclusion[0]=='E' else 'I') if mode=='contrary'
                               else ('I' if conclusion[0]=='E' else 'A'), 'B','C')
                for i, retain in enumerate(('major','minor')):
                    kept,target = (major,minor) if i==0 else (minor,major)
                    expected = EXPECTED_RESULTS[name][i+(2 if mode=='contradictory' else 0)]
                    key = f'{name}/{mode}/retain_{retain}'
                    row=actual[key]
                    for field, prop in [('retained',kept),('replacement',replacement),('target',target)]:
                        require(row[field]==text(prop), key+' '+field)
                    require(row['display_result']==(text(expected) if expected else None), key+' display')
                    bg=[d for d in ds if truth(kept,d) and truth(replacement,d)]
                    count=sum(truth(target,d) for d in bg)
                    result_count=sum(not truth(expected,d) for d in bg) if expected else None
                    valid=[text((k,target[1],target[2])) for k in 'AEIO'
                           if all(truth((k,target[1],target[2]),d) for d in bg)]
                    require(len(bg)>0, key+' nonvacuous')
                    require(row['background_count']==len(bg), key+' background')
                    require(row['refutation_countermodel_count']==count, key+' refutation')
                    require(row['result_countermodel_count']==result_count, key+' result')
                    require(row['all_valid_target_pair_forms']==valid, key+' forms')
                    for field, predicate in [('first_refutation_countermodel', lambda d:truth(target,d)),
                                              ('first_result_countermodel',lambda d:not truth(expected,d))]:
                        w=row[field]
                        if w is None: continue
                        d=tuple(tuple(c=='1' for c in t) for t in w['occupied_types'])
                        require(d in ds and truth(kept,d) and truth(replacement,d) and predicate(d), key+' witness')
                        require({n:sorted(int(''.join('1' if b else '0' for b in x),2) for x in d if x[j])
                                 for n,j in INDEX.items()}==w['sets'],key+' witness sets')
                        witness_checks+=1
                    rows_checked+=1
        print(f'{policy}: {population} models, 16 independently matched rows; four original moods valid')
    # Article's concrete witnesses: two non-strengthening examples and two particular failures.
    def domain(a,b,c):
        return tuple((x in a,x in b,x in c) for x in sorted(a|b|c))
    d=domain({1},{0,1},{0})
    require(truth(('E','A','C'),d) and truth(('A','B','C'),d) and not truth(('E','A','B'),d),'Camestres strengthening')
    d=domain({0},{0,1},{0})
    require(truth(('A','A','C'),d) and truth(('A','B','C'),d) and not truth(('A','A','B'),d),'Cesare strengthening')
    for name,d in [('Festino',domain({0},{1},{0,1})), ('Baroco',domain({0},{0},{0,1}))]:
        require(all(truth(p,d) for p in MOODS[name]) and truth(('I','B','C'),d),name+' counterexample')
    print(f'PASS: {rows_checked} rows, {witness_checks} stored witnesses, four article examples. No author evaluator imported.')

if __name__=='__main__': main()
