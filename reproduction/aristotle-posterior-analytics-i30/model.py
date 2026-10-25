"""Original finite-set teaching models; not Aristotle's definition of usually."""
from fractions import Fraction
from itertools import product
import json


def frequency(event, condition):
    """Exact uniform finite conditional frequency; empty condition is undefined."""
    return Fraction(len(event & condition), len(condition)) if condition else None


def subsets(n):
    return [frozenset(i for i in range(n) if mask & (1 << i)) for mask in range(1 << n)]


def bound_values(a, b, c):
    """No independence assumption. Undefined factors remain None, not zero."""
    target = frequency(a, c)
    first = frequency(b, c)
    second = frequency(a, b & c)
    lower = first * second if first is not None and second is not None else None
    return target, lower


def majority_example():
    a, b, c = frozenset({5,6,7,8,9}), frozenset({0,1,2,5,6,7,8,9}), frozenset({0,1,2,3,4})
    return {'P(B|C)': str(frequency(b,c)), 'P(A|B)': str(frequency(a,b)),
            'P(A|C)': str(frequency(a,c)), 'P(A|B∩C)': str(frequency(a,b&c))}


def enumerate_models(max_n=4):
    rows=[]
    for n in range(1,max_n+1):
        counts=dict(n=n, triples=0, empty_C=0, empty_B_intersect_C=0,
                    defined_product_bounds=0, bound_failures=0, inclusion_premises=0,
                    inclusion_failures=0, majority_premises=0, majority_failures=0)
        for a,b,c in product(subsets(n),repeat=3):
            counts['triples']+=1
            if not c:
                counts['empty_C']+=1
            elif not b&c:
                counts['empty_B_intersect_C']+=1
            target,lower=bound_values(a,b,c)
            if lower is not None:
                counts['defined_product_bounds']+=1
                counts['bound_failures']+=int(target<lower)
            if c<=b<=a:
                counts['inclusion_premises']+=1
                counts['inclusion_failures']+=int(not c<=a)
            bc,ab,ac=frequency(b,c),frequency(a,b),frequency(a,c)
            if bc is not None and ab is not None and bc>Fraction(1,2) and ab>Fraction(1,2):
                counts['majority_premises']+=1
                counts['majority_failures']+=int(ac<=Fraction(1,2))
        rows.append(counts)
    return rows


def world_example():
    """All observed objects succeed in w0; another stipulated allowed world differs."""
    u=frozenset({0,1})
    allowed_worlds=(u,frozenset({0}))
    return {'observed_frequency':str(frequency(allowed_worlds[0],u)),
            'all_objects_succeed_in_every_stipulated_world':all(u<=a for a in allowed_worlds)}


def results():
    rows=enumerate_models()
    totals={key:sum(row[key] for row in rows) for key in rows[0] if key!='n'}
    return {'scope':'finite uniform teaching models, not an interpretation of ancient modal semantics',
            'majority_counterexample':majority_example(),'enumeration':rows,'totals':totals,
            'frequency_not_necessity':world_example()}

if __name__=='__main__':
    print(json.dumps(results(),ensure_ascii=False,indent=2))
