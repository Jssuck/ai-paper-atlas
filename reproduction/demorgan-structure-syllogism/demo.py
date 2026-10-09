"""Short deterministic examples, plus machine-readable exact-rational evidence."""
from fractions import Fraction as F
from pathlib import Path
import json
import demorgan as d


def results():
    p0=d.random_subset_disjoint(1000,100,100)
    urn=d.urn_example()
    table,atom_count=d.composition_from_atoms()
    return {
        'semantics': 'modern finite sets; exact rational product-conditioning model',
        'eight_propositions_example': d.propositions({0,1,2,3},{0,1},{1,2}),
        'overlap': {'fractions':['3/5','7/10'],'sharp_lower_bound':str(d.overlap_lower_bound(F(3,5),F(7,10))),
                    'p406_effective_counts':[100,50,60], 'p406_guaranteed_count':10},
        'random_subset_p385_386':{'population':1000,'sizes':[100,100],'disjoint_exact':str(p0),
                                'disjoint_decimal':float(p0),'overlap_odds_to_one':float((1-p0)/p0)},
        'random_intervals_p386_387':{'lengths':['1/10','1/10'],'disjoint':'64/81','overlap':'17/81'},
        'testimony_p394_395':{'inputs':['3/4','4/5'],'joint':str(d.joint_testimony([F(3,4),F(4,5)]))},
        'bias_p396_audit':{'mu':'3/4','mu_prime':'4/5','lambda':'1/3',
                          'mixture_testimony':str(d.biased_testimony(F(3,4),F(4,5),F(1,3))),
                          'authority_from_mixture':str(d.authority(d.biased_testimony(F(3,4),F(4,5),F(1,3)))),
                          'literal_printed_authority':str(d.printed_biased_authority(F(3,4),F(4,5),F(1,3))),
                          'status':'Printed second expression disagrees with first under a=2*mu-1.'},
        'arguments_p397':{k:str(v) for k,v in d.opposing_arguments(F(3,4),F(1,2)).items()},
        'combined_p398':{'a':'3/4','b':'1/2','mu':'2/3','probability':str(d.conclusion_probability(F(3,4),F(1,2),F(2,3)))},
        'unknown_authority_p401':{'r':4,'fixed_mu_half':0.8,
                                 'uniform':d.averaged_authority(4),
                                 'beta_2_2':d.averaged_authority(4,'beta22'),
                                 'uniform_quadrature':d.averaged_authority_quadrature(4),
                                 'beta_2_2_quadrature':d.averaged_authority_quadrature(4,'beta22'),
                                 'panels':20000},
        'exactly_two_p404':{'exponents':[1,2,3,4],'first_horn_included':'9/35'},
        'urn_p405':{'conditional_distribution':{''.join(s):str(v) for s,v in urn.items()},
                    'red_probability':str(sum(v for s,v in urn.items() if s[0]=='R'))},
        'seven_relations_p408':{'proper_occupancy_models':atom_count,
                               'composition':{r+','+s:sorted(v) for (r,s),v in table.items()}},
        'syllogism_census':d.syllogism_census(),
        'historical_vs_modern_census':{'paper_report':'32 concluding; remove 6; 26 directed / 14 counterpart classes',
                                     'modern_full_weakening':'32 concluding; remove 8; 24 directed / 12 counterpart classes',
                                     'extra_modern_weakenings':['AA -> Ai (conclusion i)','ee -> Oe (conclusion I)']},
        'dependence_counterexample':{'same_marginals':['1/2','1/2'],
                                     'same_full_support':True,'independent_P_11':'1/4','correlated_P_11':'2/5',
                                     'independent_any':'3/4','correlated_any':'3/5'},
    }


def main():
    data=results()
    path=Path('evidence/results.json'); path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('De Morgan 1847: deterministic teaching examples')
    print('Overlap: 3/5 + 7/10 -> at least',data['overlap']['sharp_lower_bound'])
    print('p.406: 50 + 60 - 100 -> at least 10 individuals')
    print(f'Random fixed subsets (1000,100,100): overlap odds {float((1-p0)/p0):.3f}:1' if (p0:=d.random_subset_disjoint(1000,100,100)) else 'Certain overlap')
    print('Contiguous intervals (1/10,1/10): disjoint 64/81; overlap 17/81')
    print('Testimonies 3/4, 4/5 ->',data['testimony_p394_395']['joint'])
    print('p.396 audit: authority from mixture 19/26; literal printed formula 9/13')
    print('Arguments a=3/4, b=1/2:',data['arguments_p397'])
    print('Add mu=2/3 -> conclusion probability 4/5')
    print('Unknown authority r=4: fixed mu=.5 -> .8; uniform -> %.12f; Beta(2,2) -> %.12f' % (d.averaged_authority(4),d.averaged_authority(4,'beta22')))
    print('p.405 urn: red probability',data['urn_p405']['red_probability'])
    print('p.408: 193 proper occupancy models; 49 relation-pair cells')
    print('64 premise pairs; 32 conclude; modern full weakening -> 24 directed / 12 counterpart classes')
    print('The paper retains AA and ee and reports 26 directed / 14 counterpart classes.')
    print('Same marginals and support do not imply the same joint probabilities.')
    print('Wrote evidence/results.json')


if __name__=='__main__': main()
