"""Independent, bounded audit. Explicit checks survive -O and -OO."""
from fractions import Fraction as F
from itertools import product, combinations, groupby
from types import MappingProxyType
import model as m


def check(condition, label):
    if not condition:
        raise RuntimeError(label)


def reject(exc, fn, *args):
    try:
        fn(*args)
    except Exception as error:
        check(type(error) is exc, f'{fn.__name__}: expected {exc}, got {type(error)}')
    else:
        raise RuntimeError(f'{fn.__name__}: accepted malformed input')


class TupleSubclass(tuple):
    pass


class StringSubclass(str):
    pass


class DictSubclass(dict):
    pass


class FractionSubclass(F):
    pass


def main():
    # An independent oracle enumerates ALL possible decoders, rather than
    # reimplementing the production routine's dictionary consistency test.
    fiber_cases = 0
    for n in range(1, 5):
        for obs in product('012', repeat=n):
            image = tuple(sorted(set(obs)))
            for target in product('ab', repeat=n):
                witnesses = [dict(zip(image, vals)) for vals in product('ab', repeat=len(image))
                             if tuple(vals[image.index(o)] for o in obs) == target]
                got = m.factors_through(obs, target)
                check((got is not None) == bool(witnesses), 'decoder existence')
                if witnesses:
                    check(len(witnesses) == 1 and got == witnesses[0], 'unique image decoder')
                fiber_cases += 1
    # Exhaustively count maximal constant blocks, independently of production D.
    trace_cases = 0
    for n in range(1, 7):
        for trace in product('ab', repeat=n):
            for vals in product('012', repeat=2):
                h = dict(zip('ab', vals))
                before = h.copy()
                observed = tuple(h[s] for s in trace)
                latent_blocks = tuple(k for k, _ in groupby(trace))
                observed_blocks = tuple(k for k, _ in groupby(observed))
                check(m.observe(trace,h) == observed, 'raw observation')
                check(m.idea_word(trace,h) == observed_blocks, 'RLE order')
                check(m.change_count(trace) == len(latent_blocks)-1, 'latent count')
                check(m.change_count(observed) == len(observed_blocks)-1, 'observed count')
                hidden_edges = sum(trace[i-1] != trace[i] and observed[i-1] == observed[i]
                                   for i in range(1,n))
                check(m.change_count(trace)-m.change_count(observed) == hidden_edges,
                      'exact hidden-edge deficit and equality criterion')
                check(m.idea_word(m.compress(trace),h) == observed_blocks, 'stutter invariant')
                check(h == before, 'mapping mutation')
                trace_cases += 1
    # Three observers, nonuniform exact grid. Independent semantics uses explicit
    # input intervals and membership, not production advancing-index logic.
    schedules = []
    for count in range(3):
        for inner in combinations((F(1,3),F(3,5)), count):
            for labels in product('01', repeat=count+1):
                schedules.append(tuple(zip((F(0),)+inner,labels)))
    schedule_cases = 0
    for inputs in product(schedules, repeat=3):
        rows = m.synchronize(inputs)
        endpoints = tuple(sorted(set(t for s in inputs for t,_ in s) | {F(1)}))
        check(tuple((a,b) for a,b,_ in rows) == tuple(zip(endpoints,endpoints[1:])),
              'exact common partition and terminal endpoint')
        for left,right,labels in rows:
            check(all(type(x) is F for x in (left,right)) and left < right, 'exact positive interval')
            for probe in (left,(left+right)/2):
                expected = []
                for schedule in inputs:
                    matches = [label for (start,label),end in
                               zip(schedule, tuple(t for t,_ in schedule[1:])+(F(1),))
                               if start <= probe < end]
                    check(len(matches) == 1,'unique right-continuous label')
                    expected.append(matches[0])
                check(labels == tuple(expected), 'boundary/midpoint ordered labels')
        for i,schedule in enumerate(inputs):
            check(tuple(k for k,_ in groupby(row[2][i] for row in rows)) ==
                  tuple(k for k,_ in groupby(label for _,label in schedule)), 'projection')
        schedule_cases += 1
    bad = []
    for word in ([], iter(('a',)), TupleSubclass(('a',)), None, 'a'):
        bad.append((TypeError,m.compress,(word,)))
    for word in ((), ('',), (True,), (float('nan'),), (StringSubclass('a'),)):
        bad.append((ValueError,m.compress,(word,)))
    for mapping in ([], iter((('a','x'),)), MappingProxyType({'a':'x'}), DictSubclass(a='x')):
        bad.append((TypeError,m.observe,(('a',),mapping)))
    for mapping in ({}, {'b':'x'}, {'a':True}, {'a':float('nan')}, {'a':''},
                    {'a':'x','unused':None}, {StringSubclass('a'):'x'}):
        bad.append((ValueError,m.observe,(('a',),mapping)))
    bad.extend(((ValueError,m.factors_through,((),())),
                (ValueError,m.factors_through,(('a',),('b','c'))),
                (TypeError,m.factors_through, (('a',),iter(('b',))))))
    for outer in ([], iter(()), TupleSubclass(()), None):
        bad.append((TypeError,m.synchronize,(outer,)))
    bad.append((ValueError,m.synchronize,((),)))
    for schedule in ([], iter(()), TupleSubclass(())):
        bad.append((TypeError,m.synchronize,((schedule,),)))
    bad.append((ValueError,m.synchronize,(((),),)))
    for coord in (0,0.0,False,True,float('nan'),float('inf'),FractionSubclass(0)):
        bad.append((TypeError,m.synchronize,((((coord,'a'),),),)))
    for schedule in (((F(1,2),'a'),),((F(-1),'a'),),((F(0),'a'),(F(1),'b')),
                     ((F(0),'a'),(F(0),'b')),((F(0),'a'),(F(2,3),'b'),(F(1,3),'c')),
                     ((F(0),True),),((F(0),''),),((F(0),StringSubclass('a')),),
                     ((F(0),),),([F(0),'a'],)):
        bad.append((ValueError,m.synchronize,((schedule,),)))
    for exception,fn,args in bad:
        reject(exception,fn,*args)
    check(m.observe(('a',), {'a':'x','unused':'valid'}) == ('x',), 'valid extra mapping key')
    check(m.synchronize((((F(0),'only'),),)) == ((F(0),F(1),('only',)),), 'singleton')
    print(f'PASS independent trace-map cases: {trace_cases}')
    print(f'PASS exhaustive decoder-existence cases: {fiber_cases}')
    print(f'PASS schedules: {len(schedules)}; ordered triples: {schedule_cases}')
    print(f'PASS exact exception boundary cases: {len(bad)}')
    print('PASS valid extra mapping key and singleton schedule')
    print('All audit checks use explicit exceptions, not assert.')


if __name__ == '__main__':
    main()
