"""Independent pointwise Boolean audit; no production imports. Python stdlib only."""
from itertools import product
from fractions import Fraction
import json
import sys

def require(value, message):
    if not value:
        raise RuntimeError(message)

def validate(name, arity, premise, consequence):
    rows = list(product((False, True), repeat=arity))
    satisfying = [r for r in rows if premise(*r)]
    failures = [r for r in satisfying if not consequence(*r)]
    require(bool(satisfying), name + ': vacuous premise')
    require(not failures, name + ': countermodel ' + repr(failures))
    return {'name': name, 'all_rows': len(rows), 'premise_rows': len(satisfying), 'failures': len(failures)}

def main():
    checks = []
    checks.append(validate('affirmative_closed_chain', 3,
        lambda a,b,c: (not c or b) and (not b or a) and (not a or c),
        lambda a,b,c: a == b == c))
    checks.append(validate('negative_celarent_and_conversion', 3,
        lambda a,b,c: (not c or b) and not(a and b),
        lambda a,b,c: not(a and c) and not(c and a)))
    checks.append(validate('negative_equal_minor_terms', 3,
        lambda a,b,c: (b == c) and not(a and c),
        lambda a,b,c: not(a and b)))
    checks.append(validate('partition_transport', 4,
        lambda a,b,c,d: (a == b) and (c == d) and (a != c),
        lambda a,b,c,d: b != d))
    checks.append(validate('partition_complements', 4,
        lambda a,b,c,d: (a != b) and (c != d) and (a == c),
        lambda a,b,c,d: b == d))
    checks.append(validate('closed_world_coverage', 3,
        lambda a,b,c: (not b or a) and (not c or a) and (not c or b) and (not a or b or c),
        lambda a,b,c: a == b))
    checks.append(validate('co_subject_bridge', 3,
        lambda a,b,c: (not c or a) and (not c or b) and (not b or c),
        lambda a,b,c: not b or a))
    # Countermodels explicitly witness necessity of missing conditions.
    witnesses = {
      'equal_extremes_without_chain': ((True,False,True), lambda a,b,c: a == c and not(a == b)),
      'no_complement_from_disjointness': ((False,False), lambda a,b: not(a and b) and not(a != b)),
      'partition_no_exclusivity': ((True,True,True,False), lambda a,b,c,d: (a or b) and (c or d) and a == c and b != d),
      'partition_no_exhaustivity': ((False,False,False,True), lambda a,b,c,d: not(a and b) and not(c and d) and a == c and b != d),
      'uncovered_extension': ((True,False,False), lambda a,b,c: (not b or a) and (not c or a) and (not c or b) and a != b),
      'co_subject_no_bridge': ((False,True,False), lambda a,b,c: (not c or a) and (not c or b) and not(not b or a)),
    }
    for name,(values,predicate) in witnesses.items():
        require(predicate(*values), name)
    # Rational arithmetic model: pair values (a,-a,-d,d) with additive aggregation.
    grid = [Fraction(i,2) for i in range(1,11)]
    preference_rows = 0
    for a,d in product(grid,repeat=2):
        preference_rows += 1
        require(((a-d) > (-a+d)) == (a>d), 'additive preference mismatch')
    # Additivity alone without sign symmetry does not justify inference.
    a,b,c,d = map(Fraction,(2,0,2,3))
    require(a>b and d>c and a+c>b+d and not(a>d), 'asymmetric countermodel')
    # Symmetry alone without aggregation monotonicity also does not suffice.
    a,d = Fraction(1),Fraction(2)
    ac,bd = a-d+Fraction(5), -a+d
    require(ac>bd and not(a>d), 'interaction countermodel')
    print(json.dumps({'python':sys.version.split()[0], 'optimize':sys.flags.optimize,
       'boolean_checks':checks,'countermodels':{k:list(v[0]) for k,v in witnesses.items()},
       'rational_grid_rows':preference_rows,'preference_countermodels':2,
       'status':'PASS','scope':'Pointwise Boolean teaching model and stated rational additive model only; not historical semantics or empirical preference proof.'},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
