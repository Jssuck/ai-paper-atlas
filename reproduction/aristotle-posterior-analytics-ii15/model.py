"""II.15 teaching reconstruction, not physical or historical causal validation."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Middle:
    key: str                 # canonical identity, NOT the display name
    label: str
    genus: str
    species: str
    domains: frozenset[str]
    conditions: frozenset[str] = frozenset()

@dataclass(frozen=True)
class Problem:
    key: str
    domain: str
    middle: Middle
    available_conditions: frozenset[str] = frozenset()

    def validate(self):
        if self.domain not in self.middle.domains:
            raise ValueError('middle outside its declared domain')
        if not self.middle.conditions <= self.available_conditions:
            raise ValueError('missing declared condition')
        if not all((self.key, self.domain, self.middle.key,
                    self.middle.genus, self.middle.species)):
            raise ValueError('empty canonical identifier')


def classify(left: Problem, right: Problem) -> str:
    """Most-specific operational label, NOT Aristotle's exhaustive partition.

    Exact cases also share a genus; use shares_genus for that inclusive query.
    Neither discover nor prove declared explanations.
    """
    left.validate()
    right.validate()
    a, b = left.middle, right.middle
    # Same canonical identity must have one consistent full declaration.
    if a.key == b.key:
        if a != b:
            raise ValueError('conflicting declarations of one middle')
        return 'exact'
    if a.genus == b.genus:
        return 'generic'
    return 'unrelated'

def shares_genus(left: Problem, right: Problem) -> bool:
    """Inclusive generic relation: exact cases are also generically shared."""
    classify(left, right)  # validate both declarations and identity consistency
    return left.middle.genus == right.middle.genus

@dataclass(frozen=True)
class Proposition:
    key: str
    label: str
    level: int  # declared pedagogical causal order, not measured time

class Chain:
    """Finite DAG of stipulated cause -> effect dependencies."""
    def __init__(self, nodes, edges):
        nodes = tuple(nodes)
        self.nodes = {n.key: n for n in nodes}
        if len(self.nodes) != len(nodes):
            raise ValueError('duplicate node identity')
        self.edges = frozenset(edges)
        for a, b in self.edges:
            if a not in self.nodes or b not in self.nodes:
                raise ValueError('unknown node')
        visiting, done = set(), set()
        def visit(a):
            if a in visiting:
                raise ValueError('cycle')
            if a in done:
                return
            visiting.add(a)
            for x, y in self.edges:
                if x == a:
                    visit(y)
            visiting.remove(a)
            done.add(a)
        for key in self.nodes:
            visit(key)
        for a, b in self.edges:
            if self.nodes[a].level >= self.nodes[b].level:
                raise ValueError('edge contradicts declared direction')

    def explains(self, cause, effect):
        if cause not in self.nodes or effect not in self.nodes:
            raise ValueError('unknown query node')
        if cause == effect:
            return False  # no self-explanation
        todo, seen = [cause], set()
        while todo:
            current = todo.pop()
            if current in seen:
                continue
            seen.add(current)
            for a, b in self.edges:
                if a == current:
                    if b == effect:
                        return True
                    todo.append(b)
        return False


def examples():
    shared = Middle('teaching-return', '返回', 'return', 'abstract-return',
                    frozenset({'toy-a', 'toy-b'}), frozenset({'boundary'}))
    p = Problem('toy-a', 'toy-a', shared, frozenset({'boundary'}))
    q = Problem('toy-b', 'toy-b', shared, frozenset({'boundary'}))
    # Historical generic grouping only; these are not modern physics models.
    echo = Middle('historical-echo', '反射', 'historical-anaklasis',
                  'sound', frozenset({'echo'}))
    image = Middle('historical-image', '反射', 'historical-anaklasis',
                   'visible-image', frozenset({'mirror'}))
    rainbow = Middle('historical-rainbow', '反射', 'historical-anaklasis',
                     'rainbow', frozenset({'rainbow'}))
    optical = [Problem('echo', 'echo', echo), Problem('image', 'mirror', image),
               Problem('rainbow', 'rainbow', rainbow)]
    homonym = Middle('neural-reflex', '反射', 'neural-response', 'neural',
                     frozenset({'neural'}))
    chain = Chain([Proposition('moon', '原文例：月亏', 0),
                   Proposition('weather', '原文例：更风雨', 1),
                   Proposition('nile', '原文例：尼罗河增流', 2)],
                  [('moon', 'weather'), ('weather', 'nile')])
    return p, q, optical, Problem('reflex', 'neural', homonym), chain


def demo():
    p, q, historical, homonym, chain = examples()
    print('scope=finite stipulated teaching model; no physical validation')
    print('toy shared middle:', classify(p, q))
    print('exact also shares genus:', shares_genus(p, q))
    for i in range(3):
        for j in range(i + 1, 3):
            print(historical[i].key, historical[j].key, classify(historical[i], historical[j]))
    print('same display name / different identity:', classify(historical[0], homonym))
    print('historical stipulated moon -> nile:', chain.explains('moon', 'nile'))
    print('reverse nile -> moon:', chain.explains('nile', 'moon'))
    print('self moon -> moon:', chain.explains('moon', 'moon'))

if __name__ == '__main__':
    demo()
