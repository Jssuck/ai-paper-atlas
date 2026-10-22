"""Deterministic finite checks; general proofs belong to accompanying exposition."""
import json
from model import Model, all_models, entails, skeleton, check_chain, raa_certificate, parity_probe


def main():
    models=list(all_models())
    contradictions=0
    for m in models:
        for p in m.terms:
            for s in m.terms:
                if m.holds('A',p,s)==m.holds('O',p,s): raise RuntimeError('A/O contradiction')
                if m.holds('E',p,s)==m.holds('I',p,s): raise RuntimeError('E/I contradiction')
                contradictions+=2
    shapes=[(('S','M'),('M','P')),(('P','M'),('M','S')),(('S','M'),('P','M')),(('M','S'),('M','P'))]
    classification=[{'edges':e,'shape':skeleton(e)} for e in shapes]
    barbara=entails((('A','P','M'),('A','M','S')),('A','P','S'))
    bad=entails((('A','M','P'),('A','M','S')),('A','P','S'),True)
    if barbara!=(True,None) or bad[0]: raise RuntimeError('syllogism classification')
    ps=(('A','P','M'),('A','S','M'))
    existence={'empty_terms_allowed':entails(ps,('I','P','S')),'all_terms_nonempty':entails(ps,('I','P','S'),True)}
    if existence['empty_terms_allowed'][0] or not existence['all_terms_nonempty'][0]: raise RuntimeError('existence policy')
    # A=C={x}; same two-element domain. Change B={x} to B={y}.
    free_b=[]
    for mask in (129,24):
        m=Model(('A','C','B'),mask)
        free_b.append({'mask':mask,'premise_all_C_A':m.holds('A','A','C'),
                       'target_AEIO_A_of_B':{q:m.holds(q,'A','B') for q in 'AEIO'}})
    if not all(x['premise_all_C_A'] for x in free_b): raise RuntimeError('free B premise')
    if any(free_b[0]['target_AEIO_A_of_B'][q]==free_b[1]['target_AEIO_A_of_B'][q] for q in 'AEIO'): raise RuntimeError('free B separation')
    chain_count=0; chain_premise_count=0
    for m in all_models(('S','C','M','P')):
        r=check_chain(m,('S','C','M','P'));chain_count+=1
        if r['premises']:
            chain_premise_count+=1
            if not r['conclusion']:raise RuntimeError('chain countermodel')
    paired=raa_certificate(Model(('P','S'),8),('A','P','S'),('O','P','S'),('A','P','S'))
    print(json.dumps({'three_term_models':len(models),'all_terms_nonempty_models':len(list(all_models(require_nonempty_terms=True))),
        'AEIO_contradiction_checks':contradictions,'four_skeletons':classification,'barbara':barbara,
        'shared_middle_invalid_nonempty_countermodel':bad,'existence_sensitivity':existence,
        'free_B_models':free_b,'four_term_chain_models':chain_count,'chain_antecedent_models':chain_premise_count,
        'RAA_pairing_only':paired,'parity_diagnostic':parity_probe(100),
        'limits':['Finite model enumeration is not by itself a general proof.','RAA pairing does not verify internal derivation or outer discharge.','Four directed skeletons reduce to three only up to exchanging extremal roles.']},ensure_ascii=False,indent=2,sort_keys=True))

if __name__=='__main__':main()
