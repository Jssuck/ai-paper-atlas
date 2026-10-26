"""Exhaustive independent counting loop for sizes 0..5. No probability model."""
from itertools import product
from model import analyse


def verify(max_n=5):
    maps = checks = 0
    rows = []
    for n in range(max_n+1):
        domain = [str(i) for i in range(n)]
        count = 0
        for states in product((-1,0,1), repeat=n):
            observations = [(domain[i], state==1) for i,state in enumerate(states) if state != -1]
            expected_true = expected_false = 0
            for bits in product((0,1), repeat=n):
                checks += 1
                if any(state != -1 and bits[i] != state for i,state in enumerate(states)):
                    continue
                if sum(bits) == n: expected_true += 1
                else: expected_false += 1
            r=analyse(domain, observations)
            if (r['universal_true_count'],r['universal_false_count'],r['compatible_count']) != (expected_true,expected_false,expected_true+expected_false):
                raise AssertionError((n,states,r,expected_true,expected_false))
            expected_status = 'refuted' if expected_true==0 else 'certified_finite_domain' if expected_false==0 else 'underdetermined'
            if r['status'] != expected_status: raise AssertionError('status mismatch')
            maps += 1; count += 1
        rows.append({'domain_size':n,'observation_maps':count})
    return {'max_domain_size':max_n,'observation_maps':maps,'candidate_checks':checks,'mismatches':0,'by_size':rows}

if __name__ == '__main__':
    import json
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
