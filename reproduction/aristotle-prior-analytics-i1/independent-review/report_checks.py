"""Validate the emitted JSON via direct sets, without importing production code."""
from itertools import combinations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
COUNTS={'argument_reports':0,'model_descriptions':0,'witnesses':0,'named_examples':0}
def check(ok, description):
    if not ok:
        raise RuntimeError(description)
def truth(p, ext):
    a,b=ext[p['subject']],ext[p['predicate']]
    return {'A':a<=b,'E':a.isdisjoint(b),'I':bool(a&b),'O':bool(a-b)}[p['kind']]
def decode(terms, support):
    ext={t:set() for t in terms}
    for x in support:
        for i,t in enumerate(terms):
            if (x//(2**i))%2:
                ext[t].add(x)
    return ext
def model(description):
    terms=tuple(description['terms_in_bit_order'])
    support=tuple(description['universe_representatives'])
    ext=decode(terms,support)
    check(bool(support) and tuple(sorted(set(support)))==support,'bad model support')
    check({t:set(v) for t,v in description['term_extensions'].items()}==ext,'model displayed extensions differ')
    COUNTS['model_descriptions']+=1
    return ext
def verify_argument(a):
    # Terms are discovered from the full supplied report vocabulary; valid cases
    # here all use every declared name. Order is irrelevant to set truth/counts.
    terms=tuple(sorted({t for p in a['premises']+[a['conclusion']] for t in (p['subject'],p['predicate'])}))
    domain=range(2**len(terms)); allowed=[]
    for size in range(1,len(domain)+1):
        for support in combinations(domain,size):
            ext=decode(terms,support)
            if all(ext[t] for t in a['required_nonempty']):
                allowed.append(ext)
    good=[ext for ext in allowed if all(truth(p,ext) for p in a['premises'])]
    holds=all(truth(a['conclusion'],ext) for ext in good)
    check(a['holds']==holds,'wrong report entailment')
    check(a['admissible_supports']==len(allowed),'wrong report policy count')
    check(a['premise_satisfying_supports']==len(good),'wrong report premise count')
    if a['countermodel'] is None:
        check(holds and a['countermodel_premise_truths'] is None and a['countermodel_conclusion_truth'] is None,'missing countermodel or false truth metadata')
    else:
        ext=model(a['countermodel'])
        check(all(ext[t] for t in a['required_nonempty']),'countermodel violates policy')
        pts=[truth(p,ext) for p in a['premises']]
        ct=truth(a['conclusion'],ext)
        check(all(pts) and not ct,'not a countermodel')
        check(pts==a['countermodel_premise_truths'] and ct==a['countermodel_conclusion_truth'],'reported countermodel truth mismatch')
    if 'particular_model' in a:
        ext=model(a['particular_model'])
        check([truth(p,ext) for p in a['premises']]==a['particular_premise_truths'],'particular premise truths')
        check(truth(a['conclusion'],ext)==a['particular_conclusion_truth'],'particular conclusion truth')
        if 'premise_existential_witnesses' in a:
            for prop,witness in zip(a['premises']+[a['conclusion']],a['premise_existential_witnesses']+[a['conclusion_existential_witness']]):
                if prop['kind'] not in ('I','O'):
                    check(witness is None,'universal mislabelled existential witness')
                else:
                    candidates=ext[prop['subject']] & ext[prop['predicate']] if prop['kind']=='I' else ext[prop['subject']]-ext[prop['predicate']]
                    check(witness in candidates,'invalid displayed existential witness')
                    COUNTS['witnesses']+=1
    COUNTS['argument_reports']+=1

def walk(value):
    if isinstance(value,dict):
        if {'premises','conclusion','holds'}<=value.keys():
            verify_argument(value)
        for v in value.values():
            walk(v)
    elif isinstance(value,list):
        for v in value:
            walk(v)

def main():
    report=json.loads((ROOT/'report.json').read_text())
    walk(report)
    for example in report['named_object_hand_examples'].values():
        ext={t:set(v) for t,v in example['named_extensions'].items()}
        types=example['named_object_to_truth_type']
        terms=example['compressed_model']['terms_in_bit_order']
        for obj in example['named_objects']:
            expected=sum(2**i for i,t in enumerate(terms) if obj in ext[t])
            check(types[str(obj)]==expected,'named object compression map')
        check(set(types.values())==set(example['compressed_model']['universe_representatives']),'compressed support mismatch')
        model(example['compressed_model'])
        if 'premises' in example:
            check([truth(p,ext) for p in example['premises']]==example['premise_truths'],'named premise truths')
            check(truth(example['conclusion'],ext)==example['conclusion_truth'],'named conclusion truth')
        else:
            check(example['A_S_P_truth']==(ext['S']<=ext['P']) and example['A_P_S_truth']==(ext['P']<=ext['S']),'named asymmetric A example')
        COUNTS['named_examples']+=1
    check(report['support_counts_without_nonempty_term_policy']=={'1':3,'2':15,'3':255},'support count summary')
    check(not report['unsupported_imported_premise']['accepted'],'imported premise falsely accepted')
    check(report['same_conclusion_as_assumption']['repeats_assumption'],'repeat flag absent')
    print(json.dumps({'passed':True,'counts':COUNTS},sort_keys=True))
if __name__=='__main__':
    main()
