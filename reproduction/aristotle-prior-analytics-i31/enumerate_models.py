"""Exhaustive finite checks, not a proof over arbitrary universes."""
import json
from itertools import product
from division import FiniteModel


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run():
    totals = dict(configurations=0,premise_models=0,nonempty_premise_models=0,
                  invalid_left_strengthening=0,invalid_uniform_strengthening=0,
                  valid_left_certificates=0,valid_right_certificates=0,
                  definition_checks=0)
    first = {}
    for n in range(1,4):
        universe=set(range(n));subsets=[{i for i in range(n) if mask>>i&1} for mask in range(1<<n)]
        for a,b,c,d in product(subsets,repeat=4):
            m=FiniteModel(universe,{'A':a,'B':b,'C':c,'D':d})
            r=m.division_report('A','B','C','D');totals['configurations']+=1
            # Independent elementwise expectations inside the author harness.
            expected=all(x not in a or x in b or x in c for x in universe) and all(x not in d or x in a for x in universe)
            require(r['premises']==expected,'premise mismatch')
            if expected:
                totals['premise_models']+=1
                require(r['pointwise_disjunction'],'coverage inheritance failed')
                if d:totals['nonempty_premise_models']+=1
                if not r['all_left']:
                    totals['invalid_left_strengthening']+=1
                    first.setdefault('left',{'n':n,'A':sorted(a),'B':sorted(b),'C':sorted(c),'D':sorted(d)})
                if not r['uniform_disjunction']:
                    totals['invalid_uniform_strengthening']+=1
                    first.setdefault('uniform',{'n':n,'A':sorted(a),'B':sorted(b),'C':sorted(c),'D':sorted(d)})
                for side,other,key in [('left',c,'valid_left_certificates'),('right',b,'valid_right_certificates')]:
                    if not d & other:
                        chosen=m.select_branch('A','B','C','D',side,exclude_other=True)
                        require(all(x in m.term(chosen) for x in d),'branch inference failed')
                        totals[key]+=1
                    else:
                        try:m.select_branch('A','B','C','D',side,exclude_other=True)
                        except ValueError:pass
                        else:raise RuntimeError('false exclusion accepted')
            dr=m.definition_report('D','B');totals['definition_checks']+=1
            require(dr['coextensive']==(dr['necessary'] and dr['sufficient']),'two direction mismatch')
    return {'scope':'n=1,2,3; all four-term extensions including empty terms; finite checks only','counts':totals,'first_countermodels':first}

if __name__ == '__main__':print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
