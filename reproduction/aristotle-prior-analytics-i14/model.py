"""I.14 teaching reconstruction: encoded rules are NOT modal validity claims."""
from dataclasses import dataclass
from itertools import product

MODES = ('a', 'e', 'i', 'o')
DUAL = {'a': 'e', 'e': 'a', 'i': 'o', 'o': 'i'}
BASE = {('a', 'a'): 'a', ('e', 'a'): 'e', ('a', 'i'): 'i', ('e', 'i'): 'o'}

@dataclass(frozen=True)
class Proposition:
    mode: str
    predicate: str
    subject: str
    def __post_init__(self):
        if self.mode not in MODES:
            raise ValueError('mode must be a/e/i/o')
        for term in (self.predicate, self.subject):
            if type(term) is not str or not term.strip():
                raise ValueError('terms must be nonblank strings')
        if self.predicate == self.subject:
            raise ValueError('this teaching fragment uses distinct terms')
    def quality(self):
        return Proposition(DUAL[self.mode], self.predicate, self.subject)

@dataclass(frozen=True)
class Step:
    rule: str
    formula: Proposition
    refs: tuple = ()

def validate_pair(major, minor):
    if not isinstance(major, Proposition) or not isinstance(minor, Proposition):
        raise ValueError('two Proposition instances required')
    if major.subject != minor.predicate:
        raise ValueError('not first figure in predicate-first notation')
    if len({major.predicate, major.subject, minor.subject}) != 3:
        raise ValueError('three distinct terms required')

def derive(major, minor):
    """Return one canonical rule trace, or None (not a semantic counterproof)."""
    validate_pair(major, minor)
    if major.mode not in ('a', 'e'):
        return None
    proof = [Step('premise', major), Step('premise', minor)]
    normalized = minor
    index = 1
    if minor.mode in ('e', 'o'):
        normalized = minor.quality()
        proof.append(Step('quality', normalized, (1,)))
        index = 2
    result = Proposition(BASE[major.mode, normalized.mode], major.predicate, minor.subject)
    proof.append(Step('base', result, (0, index)))
    return tuple(proof)

def verify(major, minor, proof):
    """Check a certificate against four DECLARED rules, not against worlds."""
    validate_pair(major, minor)
    if type(proof) is not tuple or len(proof) < 3:
        return False
    if proof[:2] != (Step('premise', major), Step('premise', minor)):
        return False
    for i, step in enumerate(proof):
        if not isinstance(step, Step) or not isinstance(step.formula, Proposition):
            return False
        if type(step.refs) is not tuple or any(type(r) is not int or not 0 <= r < i for r in step.refs):
            return False
        if i < 2:
            continue
        if step.rule == 'quality':
            if len(step.refs) != 1 or step.formula != proof[step.refs[0]].formula.quality():
                return False
        elif step.rule == 'base':
            if len(step.refs) != 2:
                return False
            left, right = (proof[r].formula for r in step.refs)
            try:
                validate_pair(left, right)
            except ValueError:
                return False
            mode = BASE.get((left.mode, right.mode))
            if mode is None or step.formula != Proposition(mode, left.predicate, right.subject):
                return False
        else:
            return False
    return proof[-1].formula.predicate == major.predicate and proof[-1].formula.subject == minor.subject

@dataclass(frozen=True)
class Model:
    """Finite constant domain 0..n-1; worlds contain A,B,C bit masks."""
    n: int
    worlds: tuple
    actual: int = 0
    def __post_init__(self):
        if type(self.n) is not int or self.n <= 0:
            raise ValueError('positive integer domain size required')
        if type(self.worlds) is not tuple or not self.worlds:
            raise ValueError('nonempty tuple of worlds required')
        for world in self.worlds:
            if type(world) is not tuple or len(world) != 3:
                raise ValueError('each world is a tuple of A,B,C masks')
            if any(type(m) is not int or not 0 <= m < 2**self.n for m in world):
                raise ValueError('mask outside domain')
        if type(self.actual) is not int or not 0 <= self.actual < len(self.worlds):
            raise ValueError('actual world index outside worlds')
    def column(self, term):
        if term not in ('A', 'B', 'C'):
            raise ValueError('finite evaluator only uses A/B/C')
        return tuple(world[('A', 'B', 'C').index(term)] for world in self.worlds)
    def actual_set(self, term):
        return self.column(term)[self.actual]
    def possible_set(self, term):
        result = 0
        for mask in self.column(term):
            result |= mask
        return result
    def contingent_set(self, term):
        masks = self.column(term)
        both = (1 << self.n) - 1
        either = 0
        for mask in masks:
            both &= mask
            either |= mask
        return either & ~both
    def quantify(self, mode, subject, predicate):
        if mode not in MODES:
            raise ValueError('mode must be a/e/i/o')
        if type(subject) is not int or not 0 <= subject < 2**self.n:
            raise ValueError('subject mask outside domain')
        contingent = self.contingent_set(predicate)
        return subject & ~contingent == 0 if mode in ('a', 'e') else bool(subject & contingent)
    def evaluate(self, formula):
        if not isinstance(formula, Proposition):
            raise ValueError('Proposition required')
        return self.quantify(formula.mode, self.actual_set(formula.subject), formula.predicate)

def models(n, worlds=2):
    if type(n) is not int or n <= 0 or type(worlds) is not int or worlds <= 0:
        raise ValueError('positive integer sizes required')
    for masks in product(range(1 << n), repeat=3*worlds):
        yield Model(n, tuple(tuple(masks[3*i:3*i+3]) for i in range(worlds)))

def nonempty_countermodel():
    return Model(2, ((2, 2, 1), (0, 1, 1)))

def quantity_countermodels():
    """Same particular-major premises; extreme relation necessary +/- respectively."""
    return (Model(2, ((3,3,2),(2,0,2))), Model(2, ((1,3,2),(0,0,2))))
