"""Deterministic examples plus a bounded semantic check."""
from itertools import product
from model import Premise as P, find_path, verify_path, interpretation_holds, sample_support

nodes = ('S','M','P')
premises = (P('a','S','M','verified','stipulated premise A'),
            P('b','M','P','verified','stipulated premise B'))
cert = find_path(nodes,premises,'S','P')
print('Declared verified path:', cert)
print('Certificate checks:', verify_path(nodes,premises,'S','P',cert))
print('Certificate premises:', [(p.id,p.subject,p.predicate,p.basis,p.source) for p in premises])
print('Missing bridge:', find_path(nodes,premises[:1],'S','P'), '(unknown, not false)')
print('Dialectical mode:', find_path(nodes,premises,'S','P','dialectic'), '(no endoxon-labelled path)')
false_model = {'S':{1},'M':{2},'P':{2}}
print('Declared verified inputs true in countermodel:', interpretation_holds(nodes,premises,false_model,{1,2}))
print('Conclusion true in countermodel:', false_model['S'] <= false_model['P'])
print('Observed support:',sample_support({1,2,3},{1,2},{1,2},{1,2,3}))
print('Unobserved counterexample:', sorted({1,2,3}-{1,2}))
renamed=tuple(P(p.id,{'S':'L','M':'Q','P':'R'}[p.subject],{'S':'L','M':'Q','P':'R'}[p.predicate],p.basis,p.source) for p in premises)
print('Renamed domain path:',find_path(('L','Q','R'),renamed,'L','R'))
# All extensions of three predicates on a fixed two-object domain: 4^3 = 64.
domain={1,2}
subsets=[set(),{1},{2},{1,2}]
count=true_inputs=violations=0
for ext in product(subsets, repeat=3):
    count+=1
    interpretation=dict(zip(nodes,ext))
    if interpretation_holds(nodes,premises,interpretation,domain):
        true_inputs+=1
        if not interpretation['S'] <= interpretation['P']: violations+=1
print('Finite semantic check:', {'interpretations':count,'true_input_cases':true_inputs,'violations':violations})
if violations: raise RuntimeError('soundness example failed')
print('Finite check is not a general proof, truth discovery, or full Aristotle reproduction.')
