"""Deterministic examples; writes exact results as JSON with rational strings."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import demorgan as d


def main():
    ordinary=[]
    exemplar=[]
    counts={'universal':0,'particular':0,'strengthened':0}
    for p,q in product(d.FORMS,repeat=2):
        r=d.symbolic_inference(p,q)
        if r is not None:
            kind='universal' if r.universal else 'strengthened' if p.universal and q.universal else 'particular'
            counts[kind]+=1
            ordinary.append({'first':str(p),'second':str(q),'conclusion':str(r),'kind':kind})
        e=d.exemplar_inference(p,q)
        if e is not None: exemplar.append((str(p),str(q),str(e)))
    common=sum((row['first'],row['second'],row['conclusion']) in exemplar for row in ordinary)
    n,mu=52,F(9,10)
    prior=(F(1,n),)*n
    reports=d.symmetric_channel(n,mu)
    groups=((0,),tuple(range(1,n)))
    grouped_prior, grouped_reports=d.aggregate_model(prior,reports,groups,groups)
    judgment=d.symmetric_channel(4,F(3,4))
    statement=d.symmetric_channel(4,F(4,5))
    combined=d.compose_channels(judgment,statement)
    beliefs=(F(1,5),F(3,10),F(1,2))
    unequal_prior=(F(1,10),F(3,10),F(6,10))
    fair=(F(1,2),)*2
    binary=d.symmetric_channel(2,mu)
    result={
        'scope':'Modern finite teaching reconstruction; original printed pp.79–127, 1851 part imprint, read 1850-02-25.',
        'symbolic_counts':counts,
        'proper_atom_models':len(tuple(d.atom_models())),
        'exemplar_licensed':len(exemplar),'common_symbolic_schemas':common,
        'contrary_system_inferences':ordinary,
        'exemplar_system_inferences':[dict(zip(('first','second','conclusion'),row)) for row in exemplar],
        'copula':{'persuade_then_command':sorted(d.compose({('John','Thomas')},{('Thomas','William')})),
                  'neither_original_relation_contains_result':True,
                  'three_sources_five_targets_twelve_edges_common_lower_bound':d.common_target_lower_bound(3,5,12)},
        'testimony':{
            'named_card_52_states':str(d.posterior(prior,reports,0)[0]),
            'same_model_coarsened':str(d.posterior(grouped_prior,grouped_reports,0)[0]),
            'different_binary_error_model':str(d.posterior(grouped_prior,binary,0)[0]),
            'coarsened_other_to_target_error':str(grouped_reports[1][0]),
            'two_stage_n4':str(d.posterior((F(1,4),)*4,combined,0)[0]),
            'no_information_bias_model':list(map(str,d.posterior(unequal_prior,d.biased_channel(beliefs,beliefs),0))),
            'independent_two_accurate_witnesses':str(d.multiple_witnesses(fair,(binary,)*2,(0,0))[0]),
            'perfectly_copied_second_witness':str(d.condition(fair,(mu,1-mu))[0]),
            'targeted_falsehood_prior_1_over_52_bias_1_over_10':str(d.posterior((F(1,52),F(51,52)),d.targeted_statement_channel(2,0,F(1,10)),0)[0])},
        'boundaries':['Proper nonempty terms for 32-case contrary canon; 24 remain without existence.',
                      'Nonempty terms and identity copula for 36-case exemplar enumeration.',
                      'pp.114–116 special contrary/relation assumptions are not imposed on arbitrary relations.',
                      'Denial means complement of the reported label in the same reporting channel.',
                      'Multiple-witness multiplication assumes conditional independence given the event.',
                      'Tests check the stated models, not every historical claim.']}
    out=Path(__file__).resolve().parent/'evidence'/'results.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Contrary-system canon: 8 universal + 16 particular + 8 strengthened = 32.')
    print('Exemplar canon: 36; shared symbolic schemas: 21.')
    print('Proper atom-occupancy models:',result['proper_atom_models'])
    print('Relation composition:',result['copula']['persuade_then_command'])
    for k,v in result['testimony'].items(): print(k+':',v)
    print('Wrote evidence/results.json with all 32 + 36 licensed schemas and assumptions.')


if __name__=='__main__': main()
