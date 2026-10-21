"""Independent finite checks of the article; imports no production model code."""
from itertools import product
from fractions import Fraction
import platform

checks = 0

def require(condition, label):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(label)

def C(values):
    return any(values) and not all(values)

def U(subject, extensions):
    return all(C(tuple(x in a for a in extensions)) for x in subject)

def T(subject, extensions):
    return any(C(tuple(x in a for a in extensions)) for x in subject)

def subsets(domain):
    return tuple(frozenset(x for x, present in zip(domain, mask) if present)
                 for mask in product((False, True), repeat=len(domain)))

print('Independent argument audit; Python', platform.python_version())
propositions = 0
for worlds in range(1, 7):
    for p in product((False, True), repeat=worlds):
        q = tuple(not v for v in p)
        require(any(p) == (not all(q)), 'possibility duality')
        require((not all(p)) == any(q), 'nonnecessity duality')
        require(C(p) == C(q), 'contingency complement')
        require(C(p) == (any(p) and not all(p)), 'contingency definition')
        propositions += 1
print('truth vectors, 1..6 nonempty worlds:', propositions)
models = 0
pairs = 0
for n in range(1, 4):
    D = tuple(range(n))
    ss = subsets(D)
    for worlds in range(1, 4):
        for A in product(ss, repeat=worlds):
            negA = tuple(frozenset(D) - a for a in A)
            for S in ss:
                require(U(S, A) == U(S, negA), 'universal complement')
                require(T(S, A) == T(S, negA), 'existential complement')
                require(not S or not U(S, A) or T(S, A), 'nonempty existential import')
                for R in ss:
                    if S <= R:
                        require(not U(R, A) or U(S, A), 'universal restriction')
                        require(not T(S, A) or T(R, A), 'existential expansion')
            models += 1
    # Independently enumerate both predicates and both designated actual worlds.
    for A in product(ss, repeat=2):
        for B in product(ss, repeat=2):
            Bpossible = frozenset().union(*B)
            for Bactual in B:
                require(Bactual <= Bpossible, 'actual subset possible')
                require(not U(Bpossible, A) or U(Bactual, A), 'actual U restriction')
                require(not T(Bactual, A) or T(Bpossible, A), 'possible T expansion')
                pairs += 1
print('attribute models, 1..3 objects and 1..3 worlds:', models)
print('A/B models with designated actual world, 1..3 objects, 2 worlds:', pairs)
D = frozenset((0, 1))
A = (frozenset((0,)), frozenset((1,)))
require(U(D, A), 'alternation U')
require(not any(D <= a for a in A), 'alternation no common positive world')
require(not any(D.isdisjoint(a) for a in A), 'alternation no common negative world')
A = (D, frozenset((0,)))
require(C(tuple(D <= a for a in A)) and not U(D, A), 'sentence C not object U')
require(U(frozenset(), A) and not T(frozenset(), A), 'empty subject')
A, B = (D, frozenset()), (frozenset((0,)), frozenset((0,)))
require(U(B[0], A) and not U(A[0], B), 'term swap fails')
A, B = (frozenset((0,)), frozenset()), (frozenset((0,)), frozenset((1,)))
require(U(B[0], A) and not U(D, A), 'actual U not possible U')
A = (frozenset((1,)), frozenset())
require(T(D, A) and not T(B[0], A), 'possible T not actual T')
# Fixed actual-subject semantics: both U premises can hold while conclusion fails.
Cactual = frozenset((0,))
B = (frozenset(), frozenset((0,)))
A = (frozenset(), frozenset())
require(U(Cactual, B) and U(B[0], A) and not U(Cactual, A), 'empty intermediate countermodel')
require(not all((False,)) and not any((False,)), 'nonnecessary not possible')
require(not C((True,)) and not C((False,)), 'outer negation distinction')
require(any((False, True)) and not (not any((True, False))), 'inner negation distinction')
for weights in ((Fraction(99,100), Fraction(1,100)), (Fraction(1,2), Fraction(1,2))):
    require(sum(weights) == 1 and all(w > 0 for w in weights), 'probability normalisation')
    require(C((True, False)), 'positive weighted support contingency')
print('explicit article and converse counterexamples: PASS')
print('total checked conditions:', checks)
print('PASS: finite evidence only; no historical equivalence or infinite theorem inferred.')
