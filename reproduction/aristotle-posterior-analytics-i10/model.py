"""Original finite teaching models for Posterior Analytics I.10; no historical simulator."""
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json


def integer(value, name):
    if type(value) is not int:
        raise TypeError(name + ' must be an integer, not bool')
    return value


def extension(mask, size):
    integer(size, 'size'); integer(mask, 'mask')
    if not 1 <= size <= 8 or not 0 <= mask < 2 ** size:
        raise ValueError('finite nonempty universe size 1..8 and fitting mask required')
    return frozenset(i for i in range(size) if mask & (1 << i))


def definition_holds(defined_mask, condition_mask, size):
    """An explicitly chosen extensional biconditional, not a theory of essence."""
    return extension(defined_mask, size) == extension(condition_mask, size)


def has_instance(mask, size):
    return bool(extension(mask, size))


@dataclass(frozen=True)
class Quantity:
    kind: str
    value: Fraction
    def __post_init__(self):
        if self.kind not in ('number', 'magnitude'):
            raise ValueError('unsupported kind')
        if type(self.value) not in (int, Fraction):
            raise TypeError('exact int or Fraction required')
        v = Fraction(self.value)
        if v < 0:
            raise ValueError('nonnegative teaching quantity required')
        if self.kind == 'number' and v.denominator != 1:
            raise ValueError('number model uses nonnegative integers')
        object.__setattr__(self, 'value', v)


def subtract_equals(a, b, c, d):
    """If equal wholes and equal removable parts, return equal remainders.

    Magnitudes use rational numerical proxies. This is not ancient general
    magnitude theory; zero remainders are a modern modeling convention.
    """
    if any(type(q) is not Quantity for q in (a,b,c,d)):
        raise TypeError('four Quantity instances required')
    if len({q.kind for q in (a,b,c,d)}) != 1:
        raise ValueError('cross-kind application needs a separate bridge')
    if a.value != b.value or c.value != d.value:
        raise ValueError('equality premises not satisfied')
    if c.value > a.value or d.value > b.value:
        raise ValueError('parts must be removable in the chosen domain')
    return Quantity(a.kind, a.value-c.value), Quantity(b.kind, b.value-d.value)


def learner_status(item, demonstrable, proved, attitude):
    """Classification of supplied declarations, NOT proof verification.

    The attitude is relative to a learner; no return value asserts truth.
    """
    if item not in ('definition', 'proposition') or attitude not in ('accept','neutral','reject'):
        raise ValueError('invalid item or attitude')
    if type(demonstrable) is not bool or type(proved) is not bool:
        raise TypeError('flags must be bool')
    if item == 'definition':
        if demonstrable or proved:
            raise ValueError('this meaning-only definition is not an asserted proposition')
        return 'meaning_only'
    if proved and not demonstrable:
        raise ValueError('inconsistent declarations')
    if proved:
        return 'declared_proved'
    if not demonstrable:
        return 'outside_relative_classification'
    return 'relative_hypothesis' if attitude == 'accept' else 'postulate_relative_to_learner'


def diagram_gap(drawn_length, intended_length):
    """Exact discrepancy only; neither proves a theorem nor licenses idealization."""
    if type(drawn_length) not in (int,Fraction) or type(intended_length) not in (int,Fraction):
        raise TypeError('exact lengths required')
    if drawn_length < 0 or intended_length < 0:
        raise ValueError('nonnegative lengths required')
    return abs(Fraction(drawn_length)-Fraction(intended_length))


def enumerate_models():
    rows=[]
    for n in range(1,5):
        checked=valid=empty=mismatch=0
        for p,q in product(range(2**n), repeat=2):
            checked+=1
            got=definition_holds(p,q,n)
            oracle=all(bool(p & (1<<i)) == bool(q & (1<<i)) for i in range(n))
            mismatch+=got!=oracle
            valid+=got
            empty+=got and not has_instance(p,n)
        rows.append(dict(size=n, pairs=checked, definitions=valid, empty_definitions=empty, oracle_mismatches=mismatch))
    subtraction=[]
    for kind, values in [('number',list(range(6))),('magnitude',[Fraction(i,2) for i in range(6)])]:
        checked=accepted=mismatch=0
        for a,b,c,d in product(values,repeat=4):
            checked+=1
            oracle=(a==b and c==d and c<=a and d<=b)
            try:
                x,y=subtract_equals(*(Quantity(kind,v) for v in (a,b,c,d)))
                accepted+=1
                mismatch+=not oracle or x.value!=y.value or x.value!=a-c
            except ValueError:
                mismatch+=oracle
        subtraction.append(dict(kind=kind, quadruples=checked, accepted=accepted, oracle_mismatches=mismatch))
    policy=[dict(attitude=a,status=learner_status('proposition',True,False,a)) for a in ('accept','neutral','reject')]
    return dict(definition_models=rows,subtraction_models=subtraction,relative_labels=policy,
                diagram_example=dict(drawn='999/1000',intended='1',gap=str(diagram_gap(Fraction(999,1000),1))),
                limits='Finite modern models; declarations do not verify demonstrability, truth, essence or applicability to physical diagrams.')

if __name__ == '__main__':
    print(json.dumps(enumerate_models(),ensure_ascii=False,indent=2))
