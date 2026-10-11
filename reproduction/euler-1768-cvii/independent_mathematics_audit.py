#!/usr/bin/env python3
"""Independent CVII finite-semantic mathematics audit."""
from itertools import product

def holds(kind, x, y):
    return {
        'A': not (x - y),
        'E': not (x & y),
        'I': bool(x & y),
        'O': bool(x - y),
    }[kind]

models = []
for bits in range(128):
    cells = {i for i in range(1, 8) if bits >> (i - 1) & 1}
    q = {i for i in cells if i & 1}
    p = {i for i in cells if i & 2}
    m = {i for i in cells if i & 4}
    if q and p and m:
        models.append((q, p, m))

valid = []
for figure in range(4):
    for a, b, c in product('AEIO', repeat=3):
        good = True
        for q, p, m in models:
            edges = [
                ((m, q), (p, m)),
                ((q, m), (p, m)),
                ((m, q), (m, p)),
                ((q, m), (m, p)),
            ][figure]
            if (holds(a, *edges[0]) and holds(b, *edges[1])
                    and not holds(c, p, q)):
                good = False
                break
        if good:
            valid.append((figure + 1, a + b + c))

assert len(models) == 109
assert len(valid) == 24
for figure, mood in valid:
    a, b, c = mood
    assert not (a in 'EO' and b in 'EO')
    assert not (a in 'IO' and b in 'IO')
    assert not ((a in 'EO' or b in 'EO') and c not in 'EO')
    assert not ((a in 'IO' or b in 'IO') and c not in 'IO')
    assert not ((a in 'AI' and b in 'AI') and c not in 'AI')

# 独立核验上文使用的两条周延必要条件。
def distributed(kind, subject, predicate):
    return {'A': {subject}, 'E': {subject, predicate},
            'I': set(), 'O': {predicate}}[kind]

for figure, mood in valid:
    a, b, c = mood
    edges = [
        (('M', 'Q'), ('P', 'M')),
        (('Q', 'M'), ('P', 'M')),
        (('M', 'Q'), ('M', 'P')),
        (('Q', 'M'), ('M', 'P')),
    ][figure - 1]
    dp = distributed(a, *edges[0]) | distributed(b, *edges[1])
    assert 'M' in dp
    assert distributed(c, 'P', 'Q') <= dp

print('109 models; 24 valid moods; all necessary conditions passed.')


# Check the outside-000 quotient independently, including empty terms.
def supports(eight, nonempty_terms):
    output = []
    for mask in range(1 if eight else 0, 256 if eight else 128):
        cells = ({i for i in range(8) if mask >> i & 1} if eight else
                 {i for i in range(1, 8) if mask >> (i - 1) & 1})
        p = {i for i in cells if i & 1}
        q = {i for i in cells if i & 2}
        m = {i for i in cells if i & 4}
        if not nonempty_terms or (p and q and m):
            output.append((cells, (p, q, m)))
    return output

def classify(universe):
    found = set()
    for f in range(4):
        for a,b,c in product('AEIO', repeat=3):
            if all(not (holds(a, *[((m,q),(p,m)),((q,m),(p,m)),
                                   ((m,q),(m,p)),((q,m),(m,p))][f][0])
                        and holds(b, *[((m,q),(p,m)),((q,m),(p,m)),
                                       ((m,q),(m,p)),((q,m),(m,p))][f][1]))
                   or holds(c,p,q) for p,q,m in universe):
                found.add((f+1,a+b+c))
    return found

from collections import Counter
for nonempty in (False,True):
    reduced=supports(False, nonempty)
    full=supports(True, nonempty)
    fibers=Counter(frozenset(c-{0}) for c,_ in full)
    assert set(fibers)=={frozenset(c) for c,_ in reduced}
    assert all(n==(2 if c else 1) for c,n in fibers.items())
    reduced_valid=classify([x for _,x in reduced])
    full_valid=classify([x for _,x in full])
    assert reduced_valid==full_valid
    assert len(reduced)==(109 if nonempty else 128)
    assert len(full)==(218 if nonempty else 255)
    assert len(full_valid)==(24 if nonempty else 15)
    print(f'nonempty_terms={nonempty}: reduced={len(reduced)}, '
          f'full={len(full)}, valid={len(full_valid)}; exact agreement')

# Explicit countermodels, using P as conclusion subject throughout.
a,b,c=0,1,2
for f in range(4):
    for first,second in product('EO',repeat=2):
        for p,q,m,target in [({a},{b},{c},'AI'),({a},{a},{b},'EO')]:
            edge=[((m,q),(p,m)),((q,m),(p,m)),
                  ((m,q),(m,p)),((q,m),(m,p))][f]
            assert holds(first,*edge[0]) and holds(second,*edge[1])
            assert all(not holds(t,p,q) for t in target)
print('Two uniform negative-premise countermodels: all 16 figure/premise pairs passed.')

p,q,m={a},{b},{a,b}
assert holds('I',m,p) and holds('I',m,q) and not holds('I',p,q)
p,q,m={a,b},{a},{a}
assert holds('A',m,q) and holds('I',p,m) and not holds('A',p,q)
p,q,m={a,b},{b},{a}
assert holds('E',m,q) and holds('I',p,m) and not holds('O',q,p)
p,q,m={a},{b},set()
assert holds('A',m,q) and holds('A',m,p) and not holds('I',p,q)
p,q,m={a},set(),{a}
assert holds('A',q,m) and holds('A',m,p) and not holds('I',p,q)
# II-AEO requires precisely subject P to exist, given its premises.
for _,(p,q,m) in supports(True,False):
    if holds('A',q,m) and holds('E',p,m):
        assert holds('O',p,q)==bool(p)
# Singleton equivalences, checking every target class over a two-object domain.
for r in (set(),{a},{b},{a,b}):
    v={a}
    assert holds('A',v,r)==holds('I',v,r)==(a in r)
    assert holds('E',v,r)==holds('O',v,r)==(a not in r)
print('Explicit countermodels, II-AEO existence condition, singleton equivalences: passed.')
print('No production module imported; all assertions passed.')

all_forms={(f,''.join(mood)) for f in range(1,5)
           for mood in product('AEIO',repeat=3)}
def breaks(mood):
    a,b,c=mood
    return (a in 'EO' and b in 'EO',
            a in 'IO' and b in 'IO',
            (a in 'EO' or b in 'EO') and c not in 'EO',
            (a in 'IO' or b in 'IO') and c not in 'IO',
            a in 'AI' and b in 'AI' and c not in 'AI')
violations=[sum(breaks(mood)[j] for _,mood in all_forms) for j in range(5)]
survivors={(f,mood) for f,mood in all_forms if not any(breaks(mood))}
assert violations==[64,64,96,96,32]
assert len(survivors)==48
for nonempty in (False,True):
    actual=classify([x for _,x in supports(False,nonempty)])
    assert actual<=survivors
    assert len(survivors-actual)==(24 if nonempty else 33)
print(f'Necessary-rule violating counts={violations}; survivors=48; '
      'invalid survivors=33 (empty allowed), 24 (all nonempty).')
