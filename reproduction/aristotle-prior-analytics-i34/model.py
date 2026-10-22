"""Modern finite-scenario teaching aid, NOT Aristotle's modal calculus."""
from dataclasses import dataclass
from itertools import product
import json

@dataclass(frozen=True)
class Person:
    name: str

@dataclass(frozen=True)
class Condition:
    name: str

HEALTH = Condition('health')
DISEASE = Condition('disease')

class ScenarioModel:
    """All listed scenarios are alternatives at one fixed evaluation point.

    No accessibility relation or nested modality is implemented. Domain is
    constant; worlds and domain are tuples. Valuation contains every pair
    (condition, world), with a frozenset of Persons as its extension.
    Health/disease exclusion is a teaching stipulation, not medical guidance.
    """
    def __init__(self, persons, worlds, valuation):
        self.persons, self.worlds = tuple(persons), tuple(worlds)
        if any(type(p) is not Person for p in self.persons):
            raise TypeError('domain must contain Persons')
        if len(set(self.persons)) != len(self.persons):
            raise ValueError('duplicate persons')
        if not self.worlds or len(set(self.worlds)) != len(self.worlds):
            raise ValueError('need distinct nonempty scenarios')
        expected = {(c, w) for c in (HEALTH, DISEASE) for w in self.worlds}
        if set(valuation) != expected:
            raise ValueError('valuation must have exactly all condition/world keys')
        self.valuation = {}
        for key, extension in valuation.items():
            frozen = frozenset(extension)
            if any(type(p) is not Person for p in frozen):
                raise TypeError('extensions must contain Persons')
            if not frozen <= set(self.persons):
                raise ValueError('extension outside domain')
            self.valuation[key] = frozen
        for w in self.worlds:
            if self.valuation[HEALTH, w] & self.valuation[DISEASE, w]:
                raise ValueError('health/disease overlap excluded by this model')

    @staticmethod
    def _condition(condition):
        if type(condition) is not Condition:
            raise TypeError('condition must be a Condition')
        if condition not in (HEALTH, DISEASE):
            raise ValueError('unknown condition')

    def _person(self, person):
        if type(person) is not Person:
            raise TypeError('bearer must be a Person, not a condition')
        if person not in self.persons:
            raise ValueError('unknown person')

    def holds(self, condition, person, world):
        self._condition(condition)
        self._person(person)
        if world not in self.worlds:
            raise ValueError('unknown world')
        return person in self.valuation[condition, world]

    def possible(self, condition, person):
        self._condition(condition)
        self._person(person)
        return any(self.holds(condition, person, w) for w in self.worlds)

    def all_possibly(self, condition):
        self._condition(condition)
        return all(self.possible(condition, p) for p in self.persons)

    def possibly_all(self, condition):
        self._condition(condition)
        return any(all(self.holds(condition, p, w) for p in self.persons)
                   for w in self.worlds)

    def possibly_none(self, condition):
        self._condition(condition)
        return any(all(not self.holds(condition, p, w) for p in self.persons)
                   for w in self.worlds)

    def necessarily_none(self, condition):
        self._condition(condition)
        return all(not self.holds(condition, p, w)
                   for p in self.persons for w in self.worlds)

    def joint_possible(self, first, second, person):
        self._condition(first)
        self._condition(second)
        self._person(person)
        return any(self.holds(first, person, w) and self.holds(second, person, w)
                   for w in self.worlds)


def from_cells(n, cells):
    """Two scenarios, world-major cells: 0 neither; 1 healthy; 2 diseased."""
    if type(n) is not int or n < 0:
        raise ValueError('n must be a nonnegative integer')
    cells = tuple(cells)
    if len(cells) != 2*n or any(type(c) is not int or c not in (0, 1, 2) for c in cells):
        raise ValueError('need 2*n cells with values 0,1,2')
    persons = tuple(Person(f'p{i}') for i in range(n))
    return ScenarioModel(persons, ('w0', 'w1'), {
        (condition, world): frozenset(p for i, p in enumerate(persons)
                                     if cells[j*n+i] == value)
        for condition, value in ((HEALTH, 1), (DISEASE, 2))
        for j, world in enumerate(('w0', 'w1'))})


def celarent(A, B, C):
    """Return (premises, conclusion): A disjoint B; C subset B => A disjoint C."""
    return (not (A & B) and C <= B, not (A & C))


def survey(n):
    total = premises = counterexamples = scope_gaps = 0
    for cells in product(range(3), repeat=2*n):
        m = from_cells(n, cells)
        total += 1
        if m.all_possibly(DISEASE):
            premises += 1
            counterexamples += not m.necessarily_none(HEALTH)
        scope_gaps += m.all_possibly(DISEASE) and not m.possibly_all(DISEASE)
    return dict(persons=n, scenarios=2, models=total,
                all_possibly_diseased=premises,
                counterexamples_to_necessarily_no_health=counterexamples,
                universal_possibility_scope_gaps=scope_gaps)


def celarent_survey(n):
    universe = frozenset(range(n))
    subsets = [frozenset(x for x in universe if mask & (1 << x))
               for mask in range(1 << n)]
    triples = premises = failures = 0
    for A, B, C in product(subsets, repeat=3):
        pre, conclusion = celarent(A, B, C)
        triples += 1
        premises += pre
        failures += pre and not conclusion
    return dict(persons=n, triples=triples, true_premises=premises, failures=failures)


def report():
    one = from_cells(1, (1, 2))
    two = from_cells(2, (1, 2, 2, 1))
    p = one.persons[0]
    try:
        one.holds(HEALTH, DISEASE, 'w0')
    except TypeError as e:
        type_error = str(e)
    else:
        raise RuntimeError('type rejection failed')
    return {
        'scope': 'Modern fixed-point scenario model; finite checks are not general proofs.',
        'one_person_cells': [1, 2],
        'one_person': dict(possibly_healthy=one.possible(HEALTH, p),
                           possibly_diseased=one.possible(DISEASE, p),
                           jointly_possible=one.joint_possible(HEALTH, DISEASE, p),
                           diseased_at_w0=one.holds(DISEASE, p, 'w0'),
                           possibly_no_health=one.possibly_none(HEALTH),
                           necessarily_no_health=one.necessarily_none(HEALTH)),
        'two_person_cells': [1, 2, 2, 1],
        'two_person': dict(everyone_possibly_diseased=two.all_possibly(DISEASE),
                           possibly_everyone_diseased=two.possibly_all(DISEASE),
                           possibly_no_health=two.possibly_none(HEALTH)),
        'condition_as_bearer_error': type_error,
        'scenario_surveys': [survey(n) for n in (0, 1, 2)],
        'celarent_surveys': [celarent_survey(n) for n in range(4)]}

if __name__ == '__main__':
    print(json.dumps(report(), indent=2, ensure_ascii=False))
