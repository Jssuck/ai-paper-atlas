"""Original finite-set teaching model for Prior Analytics II.24.
Not a historical algorithm, an empirical study, or a proof by enumeration.
Only Python's standard library is used. Empty sets are intentionally included.
"""
import argparse
import itertools
import json


def subset(left, right):
    return left & ~right == 0


def observed(a, b, c, d):
    return subset(c, b) and subset(d, b) and subset(d, a)


def members(mask, n):
    return [i for i in range(n) if mask & (1 << i)]


def guarantees_target(c, evidence, n):
    """Quantify over every property extension A consistent with evidence."""
    return all(not subset(evidence, a) or subset(c, a) for a in range(1 << n))


def exhaustive(max_n=4):
    if type(max_n) is not int or not 0 <= max_n <= 4:
        raise ValueError('max_n must be an integer from 0 to 4')
    counts = dict(worlds=0, observations=0, nonempty_observations=0,
                  existential_failures=0, target_failures=0, universal_failures=0,
                  deductive_premises=0, deductive_failures=0,
                  coverage_premises=0, coverage_failures=0,
                  bridge_pairs=0, bridge_equivalence_failures=0)
    by_size = []
    for n in range(max_n + 1):
        size_worlds = 0
        for a,b,c,d in itertools.product(range(1 << n), repeat=4):
            counts['worlds'] += 1
            size_worlds += 1
            if observed(a,b,c,d):
                counts['observations'] += 1
                if d:
                    counts['nonempty_observations'] += 1
                    counts['existential_failures'] += int(not (a & b))
                    counts['target_failures'] += int(not subset(c,a))
                    counts['universal_failures'] += int(not subset(b,a))
            if subset(b,a) and subset(c,b):
                counts['deductive_premises'] += 1
                counts['deductive_failures'] += int(not subset(c,a))
            if subset(d,a) and subset(b,d):
                counts['coverage_premises'] += 1
                counts['coverage_failures'] += int(not subset(b,a))
        for c,d in itertools.product(range(1 << n), repeat=2):
            counts['bridge_pairs'] += 1
            counts['bridge_equivalence_failures'] += int(guarantees_target(c,d,n) != subset(c,d))
        by_size.append({'domain_size': n, 'worlds': size_worlds})
    for key in ('existential_failures','deductive_failures','coverage_failures','bridge_equivalence_failures'):
        if counts[key] != 0:
            raise RuntimeError('Teaching claim failed: ' + key)
    return {'scope': 'all A,B,C,D subsets; domain sizes 0 through '+str(max_n),
            'counts': counts, 'by_size': by_size}


def examples():
    # masks are sets of case identifiers, not probabilities or causal variables
    cases = [
      ('one_known_case_does_not_transfer', 2, 1, 3, 2, 1),
      ('empty_example_no_existential_witness', 1, 0, 0, 0, 0),
      ('drop_sample_property', 1, 0, 1, 1, 1),
      ('drop_sample_classification', 1, 1, 0, 0, 1),
      ('drop_target_classification_in_deduction', 2, 1, 1, 2, 1),
      ('target_covered_not_whole_class', 3, 1, 7, 1, 1),
      ('empty_target_vacuous', 2, 1, 3, 0, 1),
    ]
    result=[]
    for name,n,a,b,c,d in cases:
        result.append({'name':name,'domain_size':n,
          'A':members(a,n),'B':members(b,n),'C':members(c,n),'D':members(d,n),
          'observed':observed(a,b,c,d),'D_nonempty':bool(d),
          'some_B_is_A':bool(a&b),'all_B_is_A':subset(b,a),'all_C_is_A':subset(c,a),
          'C_covered_by_D':subset(c,d),'B_covered_by_D':subset(b,d)})
    # Two observed examples do not cover a third target case.
    n,a,b,c,d1,d2=3,3,7,4,1,2
    evidence=d1|d2
    result.append({'name':'two_examples_still_not_coverage','domain_size':n,
        'A':members(a,n),'B':members(b,n),'C':members(c,n),
        'D1':members(d1,n),'D2':members(d2,n),'E_union':members(evidence,n),
        'both_observed':observed(a,b,c,d1) and observed(a,b,c,d2),
        'all_C_is_A':subset(c,a),'all_B_is_A':subset(b,a),
        'target_guaranteed_over_all_A':guarantees_target(c,evidence,n)})
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n',type=int,default=4)
    args=parser.parse_args()
    print(json.dumps({'exhaustive':exhaustive(args.max_n),'examples':examples()},indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
