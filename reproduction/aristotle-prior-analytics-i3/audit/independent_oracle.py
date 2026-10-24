"""Separate set-valued, object-bit enumeration oracle for I.3 teaching models.
Does not import production semantic or enumeration functions.
"""
from itertools import product
import json
from pathlib import Path


def worlds(n, w):
    # A label fixes both predicate memberships at every world. Enumerate each
    # object's entire history, unlike the production world-mask enumeration.
    for histories in product(range(4**w), repeat=n):
        ss, pp = [], []
        for j in range(w):
            ss.append(frozenset(x for x,h in enumerate(histories) if (h // 4**j) % 4 in (1,3)))
            pp.append(frozenset(x for x,h in enumerate(histories) if (h // 4**j) % 4 in (2,3)))
        yield ss, pp


def aggregate(mode, values):
    count = sum(1 for v in values if v)
    return {'N': count == len(values), 'P': count != 0, 'C': 0 < count < len(values)}[mode]


def formula(scope, mode, kind, ss, pp):
    if scope == 'dc':
        if kind == 'A': values = [s.issubset(p) for s,p in zip(ss,pp)]
        elif kind == 'E': values = [s.isdisjoint(p) for s,p in zip(ss,pp)]
        elif kind == 'I': values = [not s.isdisjoint(p) for s,p in zip(ss,pp)]
        else: values = [not s.issubset(p) for s,p in zip(ss,pp)]
        return aggregate(mode, values)
    successes = set()
    for x in ss[0]:
        values = [x in p if kind in ('A','I') else x not in p for p in pp]
        if aggregate(mode, values): successes.add(x)
    return successes == set(ss[0]) if kind in ('A','E') else bool(successes)


def check():
    rows = {}
    total = 0
    for n in range(1,4):
        for w in (1,2):
            for ss,pp in worlds(n,w):
                total += 1
                for scope in ('dc','dr'):
                    for mode in ('N','P','C'):
                        for kind in ('A','E','I','O'):
                            out = 'I' if kind == 'A' else kind
                            for guard in ((False,True) if kind == 'A' else (False,)):
                                key = f'{scope}_{mode}{kind}_to_{mode}{out}_reverse' + ('_all_worlds_S_nonempty' if guard else '')
                                row = rows.setdefault(key, {'premise_models':0,'countermodels':0})
                                if guard and any(len(s) == 0 for s in ss): continue
                                if formula(scope,mode,kind,ss,pp):
                                    row['premise_models'] += 1
                                    if not formula(scope,mode,out,pp,ss): row['countermodels'] += 1
    expected = json.loads((Path(__file__).parent.parent/'results.json').read_text())
    if total != expected['models']: raise RuntimeError('model count mismatch')
    if set(rows) != set(expected['rules']): raise RuntimeError('rule key mismatch')
    for key,row in rows.items():
        for field,value in row.items():
            if expected['rules'][key][field] != value: raise RuntimeError((key,field,value,expected['rules'][key][field]))
    witnesses = 0
    for key,row in expected['rules'].items():
        witness = row['first_countermodel']
        if witness is None:
            if row['countermodels'] != 0: raise RuntimeError('missing witness')
            continue
        scope, left, _, right, *_ = key.split('_')
        mode,kind = left
        out = right[1]
        ss = list(map(frozenset,witness['S'])); pp = list(map(frozenset,witness['P']))
        if 'all_worlds' in key and not all(ss): raise RuntimeError('witness violates guard')
        if not formula(scope,mode,kind,ss,pp) or formula(scope,mode,out,pp,ss): raise RuntimeError('invalid witness')
        witnesses += 1
    return {'models':total,'rule_count':len(rows),'count_fields_compared':2*len(rows),
            'first_countermodels_checked':witnesses,'mismatches':0,
            'method':'object-history enumeration; set relations; no production imports', 'counts':rows}

if __name__ == '__main__': print(json.dumps(check(),sort_keys=True,indent=2))
