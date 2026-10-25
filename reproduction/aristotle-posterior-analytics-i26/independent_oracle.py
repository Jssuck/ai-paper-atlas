"""Independent explicit-membership oracle; no external inputs or network."""
from itertools import product
import json
from model import certificate, witness_trace, diagnose, run


def check_equal(actual, expected, context):
    if actual != expected:
        raise RuntimeError((context, actual, expected))


def main():
    rows=[]
    checks=0
    for n in range(6):
        counts=dict(n=n, assignments=0, direct_premise_cases=0,
                    direct_counterexamples=0,reductio_background_cases=0,
                    reductio_counterexamples=0,overstrong_counterexamples=0,
                    empty_c_overlap_cases=0,witness_checks=0,witness_violations=0)
        # Each individual has an independent A/B/C membership pattern.
        for patterns in product(range(8),repeat=n):
            a=[bool(x & 1) for x in patterns]
            b=[bool(x & 2) for x in patterns]
            c=[bool(x & 4) for x in patterns]
            ab_disjoint=all(not (a[i] and b[i]) for i in range(n))
            ac_disjoint=all(not (a[i] and c[i]) for i in range(n))
            c_in_b=all(not c[i] or b[i] for i in range(n))
            some_b_not_a=any(b[i] and not a[i] for i in range(n))
            direct=ab_disjoint and c_in_b
            background=ac_disjoint and c_in_b and any(c)
            expected=dict(direct_premises=direct,direct_conclusion=ac_disjoint,
                          direct_valid=(not direct or ac_disjoint),
                          reductio_background=background,
                          not_all_b_are_a=some_b_not_a,
                          reductio_valid=(not background or some_b_not_a),
                          tempting_universal_negative=ab_disjoint,
                          empty_c_all_and_none=not any(c))
            terms=[{i for i in range(n) if z[i]} for z in (a,b,c)]
            check_equal(certificate(*terms),expected,(n,patterns))
            counts['assignments']+=1
            counts['direct_premise_cases']+=direct
            counts['direct_counterexamples']+=direct and not ac_disjoint
            counts['reductio_background_cases']+=background
            counts['reductio_counterexamples']+=background and not some_b_not_a
            counts['overstrong_counterexamples']+=background and not ab_disjoint
            counts['empty_c_overlap_cases']+=not any(c)
            if direct:
                for i in range(n):
                    if c[i]:
                        check_equal(witness_trace(*terms,i),dict(in_c=True,in_b=b[i],in_a=a[i],intersection_witness=a[i] and c[i]),(n,patterns,i))
                        counts['witness_checks']+=1
                        counts['witness_violations']+=not b[i] or a[i]
            checks+=1
        rows.append(counts)
    check_equal(run(5)['rows'],rows,'independent aggregate')
    # Only one valuation violates the fixed implication, derived directly.
    lawful=[(p,q,r) for p,q,r in product((False,True),repeat=3) if (p,q,r)!=(True,True,False)]
    backgrounds=0
    for p,q,r in product((None,False,True),repeat=3):
        candidates=[w for w in lawful if all(given is None or given==value for given,value in zip((p,q,r),w))]
        wanted=dict(status='consistent' if candidates else 'inconsistent_background',model_count=len(candidates),not_p_supported=all(not w[0] for w in candidates) if candidates else None)
        check_equal(diagnose(p=p,q=q,r=r),wanted,(p,q,r))
        backgrounds+=1
    return dict(method='independent individual-membership enumeration and forbidden-valuation truth oracle',set_assignments=checks,max_domain_size=5,rows=rows,background_configurations=backgrounds,mismatches=0,scope='finite extensional semantics, not a proof of epistemic superiority')

if __name__=='__main__':
    print(json.dumps(main(),ensure_ascii=False,indent=2))
