"""Exhaustive finite checks plus explicitly rejected malformed inputs."""
from fractions import Fraction as F
from itertools import product, groupby, combinations
from model import compress, change_count, observe, idea_word, factors_through, synchronize


def require(condition, message):
    # Deliberately not assert: checks remain active under -O and -OO.
    if not condition:
        raise RuntimeError(message)


def rejects(exception, function, *args):
    try:
        function(*args)
    except exception:
        return
    raise RuntimeError(f'{function.__name__} did not reject {args!r}')


def main():
    traces = 0
    for length in range(1, 6):
        for trace in product('abc', repeat=length):
            for values in product('01', repeat=3):
                h = dict(zip('abc', values))
                obs = observe(trace, h)
                expected = tuple(k for k, _ in groupby(obs))
                require(idea_word(trace, h) == expected, 'compression oracle')
                dx, dh = change_count(trace), change_count(obs)
                require(dh <= dx, 'count bound')
                separates_edges = all(a == b or h[a] != h[b] for a,b in zip(trace, trace[1:]))
                require((dh == dx) == separates_edges, 'equality criterion')
                require(idea_word(compress(trace), h) == expected, 'stutter invariance')
                traces += 1
    fibers = 0
    for obs in product('01', repeat=4):
        for target in product('ab', repeat=4):
            result = factors_through(obs, target)
            expected = all(obs[i] != obs[j] or target[i] == target[j]
                           for i in range(4) for j in range(4))
            require((result is not None) == expected, 'fiber criterion')
            if result is not None:
                require(tuple(result[o] for o in obs) == target, 'decoder reconstruction')
            fibers += 1
    schedules = []
    interior = (F(1,4), F(1,2), F(3,4))
    for count in range(4):
        for chosen in combinations(interior, count):
            cuts = (F(0),) + chosen
            for labels in product('01', repeat=len(cuts)):
                schedules.append(tuple(zip(cuts, labels)))
    pairs = 0
    for left, right in product(schedules, repeat=2):
        rows = synchronize((left, right))
        expected_cuts = sorted({t for t,_ in left+right} | {F(1)})
        require(tuple(row[0] for row in rows)+(rows[-1][1],) == tuple(expected_cuts), 'cut union')
        require(sum(b-a for a,b,_ in rows) == 1, 'coverage')
        for a,b,labels in rows:
            midpoint = (a+b)/2
            expected = tuple(next(label for t,label in reversed(s) if t <= midpoint)
                             for s in (left,right))
            require(labels == expected, 'independent midpoint oracle')
        for i,schedule in enumerate((left,right)):
            require(compress(tuple(labels[i] for _,_,labels in rows)) ==
                    compress(tuple(label for _,label in schedule)), 'projection preservation')
        pairs += 1
    # Fixed adversarial regressions complement the finite property domains.
    h = {'a':'still','b':'still'}
    constant, alternating = ('a',)*4, ('a','b','a','b')
    require(observe(constant,h) == observe(alternating,h), 'same-length aliasing')
    require(change_count(constant) == 0 and change_count(alternating) == 3,
            'unequal hidden counts')
    h1, h2 = {'a':'0','b':'0','c':'1'}, {'a':'0','b':'1','c':'0'}
    require(len(set(h1.values())) < 3 and len(set(h2.values())) < 3 and
            len({(h1[x],h2[x]) for x in 'abc'}) == 3, 'joint separation')
    early, late = ((F(0),'0'),(F(1,3),'1')), ((F(0),'0'),(F(2,3),'1'))
    first, second = synchronize((early,late)), synchronize((late,early))
    require(first != second, 'joint order differs')
    require(all(compress(tuple(labels[i] for _,_,labels in first)) ==
                compress(tuple(labels[i] for _,_,labels in second)) for i in (0,1)),
            'marginal logs agree')
    invalid = [
        (TypeError, compress, (['a'],)), (ValueError, compress, ((),)),
        (ValueError, compress, (('',),)), (ValueError, compress, ((True,),)),
        (TypeError, observe, (('a',), [])), (ValueError, observe, (('a',), {})),
        (ValueError, observe, (('a',), {'a': 1})),
        (ValueError, observe, (('a',), {'a':'x', '':'y'})),
        (ValueError, factors_through, (('a',), ('x','y'))),
        (ValueError, synchronize, ((),)), (TypeError, synchronize, ([],)),
        (ValueError, synchronize, (((),),)),
        (ValueError, synchronize, ((((F(1,2),'a'),),),)),
        (TypeError, synchronize, ((((0,'a'),),),)),
        (TypeError, synchronize, ((((0.0,'a'),),),)),
        (ValueError, synchronize, ((((F(0),'a'),(F(0),'b')),),)),
        (ValueError, synchronize, ((((F(0),'a'),(F(1),'b')),),)),
        (ValueError, synchronize, ((((F(0),'a'),(F(-1),'b')),),)),
        (ValueError, synchronize, ((((F(0),''),),),)),
        (ValueError, synchronize, ((((F(0),),),),)),
    ]
    for exception, function, args in invalid:
        rejects(exception, function, *args)
    print(f'PASS trace-map cases: {traces}')
    print(f'PASS finite fiber cases: {fibers}')
    print(f'PASS schedules: {len(schedules)}; ordered pairs: {pairs}')
    print('PASS fixed adversarial examples: 3')
    print(f'PASS invalid-input cases: {len(invalid)}')
    print('All checks execute with and without Python optimization.')

if __name__ == '__main__':
    main()
