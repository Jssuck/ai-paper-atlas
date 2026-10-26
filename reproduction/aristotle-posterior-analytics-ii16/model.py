"""Finite extensional teaching models for APo II.16, not causal discovery."""
from dataclasses import dataclass
from itertools import product
import json


@dataclass(frozen=True)
class Model:
    universe: frozenset
    predicates: dict

    def __post_init__(self):
        u = frozenset(self.universe)
        ps = {name: frozenset(values) for name, values in self.predicates.items()}
        if any(not isinstance(name, str) or not name for name in ps):
            raise ValueError('predicate names must be nonempty strings')
        if any(not values <= u for values in ps.values()):
            raise ValueError('predicate contains an object outside universe')
        object.__setattr__(self, 'universe', u)
        # Copy inputs: callers cannot mutate the original sets to change the model.
        from types import MappingProxyType
        object.__setattr__(self, 'predicates', MappingProxyType(ps))

    def extension(self, name):
        return self.predicates[name]

    def witnesses(self, antecedent, consequent, domain=None):
        d = self.universe if domain is None else frozenset(domain)
        if not d <= self.universe:
            raise ValueError('domain contains an object outside universe')
        return self.extension(antecedent) & d - self.extension(consequent)

    def implies(self, antecedent, consequent, domain=None):
        return not self.witnesses(antecedent, consequent, domain)

    def coextensive(self, left, right, domain=None):
        return self.implies(left, right, domain) and self.implies(right, left, domain)


def orientations(model, left, right):
    """Possible *labels*, not inferred causes; equality cannot select one label."""
    if not model.coextensive(left, right):
        raise ValueError('this demonstration requires coextension')
    return ((left, right), (right, left))


def exhaustive_syllogism(n=3):
    """Enumerate all 2^(3n) extensions of C,B,A on n labelled objects."""
    if not isinstance(n, int) or isinstance(n, bool) or not 0 <= n <= 4:
        raise ValueError('n must be an integer from 0 to 4')
    u = frozenset(range(n))
    checked = satisfying = violations = 0
    for bits in product((False, True), repeat=3*n):
        ps = {name: {i for i in u if bits[j*n+i]} for j, name in enumerate(('C','B','A'))}
        m = Model(u, ps)
        checked += 1
        if m.implies('C','B') and m.implies('B','A'):
            satisfying += 1
            violations += not m.implies('C','A')
    return {'universe_size':n, 'assignments':checked, 'premise_satisfying':satisfying,
            'conclusion_violations':violations}


def examples():
    reverse = Model({'vine','other'}, {'C':{'vine'},'B':{'vine'},'A':{'vine','other'}})
    equal = Model({'vine','other'}, {'A':{'vine'},'B':{'vine'}})
    alternatives = Model({'b_only','c_only','both','neither'},
        {'B':{'b_only','both'},'C':{'c_only','both'},'A':{'b_only','c_only','both'}})
    # A is deliberately defined as the tree-restricted outcome in this synthetic model.
    restricted = Model({'tree_s','tree_no_s','non_tree_s'},
        {'T':{'tree_s','tree_no_s'},'S':{'tree_s','non_tree_s'},'A':{'tree_s'},'TS':{'tree_s'}})
    return {
        'exhaustive':exhaustive_syllogism(),
        'one_way':{'C_to_B':reverse.implies('C','B'),'B_to_A':reverse.implies('B','A'),
                   'C_to_A':reverse.implies('C','A'),'A_to_B':reverse.implies('A','B'),
                   'A_not_B':sorted(reverse.witnesses('A','B'))},
        'coextension':{'A_equals_B':equal.coextensive('A','B'),
                      'unselected_direction_labels':orientations(equal,'A','B')},
        'alternatives':{'B_to_A':alternatives.implies('B','A'),'C_to_A':alternatives.implies('C','A'),
                        'A_not_B':sorted(alternatives.witnesses('A','B')),
                        'A_not_C':sorted(alternatives.witnesses('A','C'))},
        'restriction':{'A_equals_TS':restricted.coextensive('A','TS'),
                       'S_to_A_in_T':restricted.implies('S','A',restricted.extension('T')),
                       'unrestricted_S_not_A':sorted(restricted.witnesses('S','A'))},
        'warning':'Synthetic extensions only: neither natural science nor causal direction is established.'}


if __name__ == '__main__':
    print(json.dumps(examples(), ensure_ascii=False, indent=2))
