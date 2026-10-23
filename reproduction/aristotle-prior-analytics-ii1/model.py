"""Original finite teaching model for Prior Analytics II.1; not ancient semantics."""
from dataclasses import dataclass
from itertools import product


def name(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('term/assumption names must be nonblank strings')
    return value


@dataclass(frozen=True)
class Statement:
    mood: str
    subject: str
    predicate: str

    def __post_init__(self):
        if self.mood not in ('A', 'E', 'I', 'O'):
            raise ValueError('mood must be A/E/I/O')
        name(self.subject)
        name(self.predicate)


class Model:
    def __init__(self, n, terms):
        if type(n) is not int or n < 0:
            raise ValueError('n must be a nonnegative integer')
        if not isinstance(terms, dict):
            raise ValueError('terms must be a dictionary')
        self.universe = frozenset(range(n))
        self.terms = {}
        for key, values in terms.items():
            name(key)
            try:
                seq = tuple(values)
            except TypeError as exc:
                raise ValueError('extension must be iterable') from exc
            if any(type(x) is not int or x not in self.universe for x in seq):
                raise ValueError('extension element outside universe')
            self.terms[key] = frozenset(seq)

    def extension(self, term):
        name(term)
        if term not in self.terms:
            raise ValueError('unknown term')
        return self.terms[term]

    def holds(self, statement):
        if not isinstance(statement, Statement):
            raise ValueError('expected Statement')
        s, p = self.extension(statement.subject), self.extension(statement.predicate)
        return {'A': s <= p, 'E': not (s & p), 'I': bool(s & p),
                'O': bool(s - p)}[statement.mood]


def models(n, names):
    if type(n) is not int or n < 0:
        raise ValueError('n must be a nonnegative integer')
    names = tuple(names)
    for term in names:
        name(term)
    if len(set(names)) != len(names):
        raise ValueError('duplicate terms')
    sets = [frozenset(i for i in range(n) if mask & (1 << i))
            for mask in range(1 << n)]
    for values in product(sets, repeat=len(names)):
        yield Model(n, dict(zip(names, values)))


@dataclass(frozen=True)
class Proof:
    statement: Statement
    rule: str
    parents: tuple = ()
    label: str = ''

    def dependencies(self):
        validate(self)
        if self.rule == 'premise':
            return frozenset((self.label,))
        return frozenset().union(*(p.dependencies() for p in self.parents))


def validate(proof):
    if not isinstance(proof, Proof) or not isinstance(proof.statement, Statement):
        raise ValueError('invalid proof')
    if not isinstance(proof.parents, tuple):
        raise ValueError('parents must be a tuple')
    if proof.rule == 'premise':
        if proof.parents:
            raise ValueError('premise has parents')
        name(proof.label)
        return
    if proof.label:
        raise ValueError('derived proof cannot invent assumption label')
    for parent in proof.parents:
        validate(parent)
    expected = conclusion(proof.rule, tuple(p.statement for p in proof.parents))
    if expected != proof.statement:
        raise ValueError('conclusion does not follow the declared rule')


def conclusion(rule, premises):
    if rule in ('convert_E', 'convert_I'):
        if len(premises) != 1 or premises[0].mood != rule[-1]:
            raise ValueError('wrong conversion premise')
        p = premises[0]
        return Statement(p.mood, p.predicate, p.subject)
    if len(premises) != 2:
        raise ValueError('rule needs two premises')
    p, q = premises
    if rule == 'convert_A_with_existence':
        # I(S,S) explicitly records nonemptiness; it is not inferred from A(S,P).
        if p.mood != 'A' or q != Statement('I', p.subject, p.subject):
            raise ValueError('A conversion needs its subject-existence premise')
        return Statement('I', p.predicate, p.subject)
    if rule == 'chain_A':
        if p.mood != 'A' or q.mood != 'A' or p.predicate != q.subject:
            raise ValueError('invalid inclusion chain')
        return Statement('A', p.subject, q.predicate)
    if rule == 'restrict_E':
        if p.mood != 'A' or q.mood != 'E' or p.predicate != q.subject:
            raise ValueError('invalid negative restriction')
        return Statement('E', p.subject, q.predicate)
    if rule == 'Cesare':
        if p.mood != 'E' or q.mood != 'A' or p.predicate != q.predicate:
            raise ValueError('invalid second-figure pattern')
        return Statement('E', q.subject, p.subject)
    if rule == 'Darii':
        if p.mood != 'A' or q.mood != 'I' or p.subject != q.predicate:
            raise ValueError('invalid particular pattern')
        return Statement('I', q.subject, p.predicate)
    raise ValueError('unsupported rule')


def premise(label, mood, subject, predicate):
    result = Proof(Statement(mood, subject, predicate), 'premise', (), label)
    validate(result)
    return result


def infer(rule, *parents):
    for parent in parents:
        validate(parent)
    result = Proof(conclusion(rule, tuple(p.statement for p in parents)), rule, parents)
    validate(result)
    return result


def examples():
    # A is the middle in the second-figure example, as in the source.
    p1 = premise('p1:B disjoint A', 'E', 'B', 'A')
    p2 = premise('p2:C subset A', 'A', 'C', 'A')
    original = infer('Cesare', p1, p2)
    subclass = premise('s:E subset A', 'A', 'E', 'A')
    extra = infer('restrict_E', subclass, infer('convert_E', p1))
    d1 = premise('d1:B subset A', 'A', 'B', 'A')
    d2 = premise('d2:some C is B', 'I', 'C', 'B')
    particular = infer('Darii', d1, d2)
    below_middle = premise('t:D subset B', 'A', 'D', 'B')
    direct = infer('chain_A', below_middle, d1)
    return {'second_original': original, 'second_submiddle': extra,
            'particular_original': particular, 'particular_submiddle': direct}
