"""Modern finite teaching models for Posterior Analytics II.8, not causal discovery."""
from dataclasses import dataclass
from itertools import product


def subsets(n):
    if type(n) is not int or n < 0:
        raise ValueError('n must be a nonnegative integer')
    return tuple(frozenset(i for i in range(n) if mask & (1 << i)) for mask in range(1 << n))


def chain(c, b, a):
    """Return premise and conclusion truth; sets may be empty."""
    return {'minor': c <= b, 'major': b <= a, 'conclusion': c <= a,
            'premises': c <= b and b <= a}


def candidate_middles(c, a, candidates):
    """Search only the supplied named extensions, not all real-world causes."""
    return tuple(name for name, b in sorted(candidates.items()) if c <= b <= a)


@dataclass(frozen=True)
class DeclaredRole:
    role: str
    immediate_premises: bool
    source: str

    def __post_init__(self):
        if self.role not in ('sign', 'cause', 'unknown'):
            raise ValueError('role must be sign, cause, or unknown')
        if type(self.immediate_premises) is not bool:
            raise ValueError('immediacy is an explicit Boolean declaration')
        if not isinstance(self.source, str) or not self.source.strip():
            raise ValueError('a nonempty provenance label is required')


def report(c, b, a, declaration):
    """Preserve declarations without upgrading them to independently verified knowledge."""
    result = chain(c, b, a)
    result.update(role_declared=declaration.role,
                  immediacy_declared=declaration.immediate_premises,
                  source_label=declaration.source,
                  causal_truth_verified=False,
                  essence_verified=False)
    return result


def binary_world(kind, u, do_b=None):
    """Two stipulated structural equations. Interventions replace B's equation only.

    directed: B=U, A=B. common: B=U, A=U.
    No probabilities, fitted parameters, or measured astronomy are involved.
    """
    if kind not in ('directed', 'common'):
        raise ValueError('unknown model')
    if type(u) is not int or u not in (0, 1):
        raise ValueError('u must be 0 or 1')
    if do_b is not None and (type(do_b) is not int or do_b not in (0, 1)):
        raise ValueError('intervention must be None, 0, or 1')
    b = u if do_b is None else do_b
    a = b if kind == 'directed' else u
    return (b, a)


def enumerate_chains(max_n=4):
    rows = valid = violations = oracle_differences = 0
    for n in range(max_n + 1):
        for c, b, a in product(subsets(n), repeat=3):
            rows += 1
            result = chain(c, b, a)
            # Deliberately independent member-by-member premise/conclusion oracle.
            minor = all(i not in c or i in b for i in range(n))
            major = all(i not in b or i in a for i in range(n))
            conclusion = all(i not in c or i in a for i in range(n))
            oracle_differences += (result['minor'], result['major'], result['conclusion']) != (minor, major, conclusion)
            valid += result['premises']
            violations += result['premises'] and not result['conclusion']
    return dict(max_n=max_n, triples=rows, valid_chains=valid,
                transitivity_violations=violations, oracle_differences=oracle_differences)


def experiments():
    c, a = frozenset({0}), frozenset({0, 1, 2})
    middles = candidate_middles(c, a, {'sign':frozenset({0,1}), 'cause':frozenset({0,2}), 'bad':frozenset({1})})
    observational = {kind:[binary_world(kind,u) for u in (0,1)] for kind in ('directed','common')}
    differing = sum(binary_world('directed',u,b) != binary_world('common',u,b) for u,b in product((0,1),repeat=2))
    return {'sets': enumerate_chains(), 'candidate_names':middles,
            'observational_tables':observational, 'intervention_cases':4,
            'intervention_disagreements':differing,
            'warning':'Stipulated finite teaching models; no certification of real causes or essences.'}

if __name__ == '__main__':
    import json
    print(json.dumps(experiments(),ensure_ascii=False,indent=2))
