import json
from fractions import Fraction
from model import Model, models, extensions, contingent, probability
F=frozenset
m=Model(2,(F({0}),F({1})),(F({0,1}),F({0,1})))
counts={'models':0,'fixed_subject_pairs':0,'all_each_true':0,'some_each_true':0,'actual_all_true':0,'possible_all_true':0}
for q in models(2,2):
    counts['models']+=1
    counts['actual_all_true']+=q.all_each_contingent(q.subject())
    counts['possible_all_true']+=q.all_each_contingent(q.subject('possible'))
    for S in extensions(2):
        counts['fixed_subject_pairs']+=1
        counts['all_each_true']+=q.all_each_contingent(S)
        counts['some_each_true']+=q.some_each_contingent(S)
result={'scope':'Two objects and two worlds; finite pedagogical illustration, not a proof of historical modal logic.','counts':counts,'alternating':{'each_contingent':m.all_each_contingent(F({0,1})),'sentence_truth':{f:m.sentence(F({0,1}),f) for f in ('all','none','some','notall')},'sentence_contingency':{f:m.sentence_contingent(F({0,1}),f) for f in ('all','none','some','notall')}},'weights':{'same_contingent_vector':[True,False],'weight_9_1':str(probability((True,False),(9,1))),'weight_1_9':str(probability((True,False),(1,9))),'weight_1_0':str(probability((True,False),(1,0)))}}
print(json.dumps(result,ensure_ascii=False,indent=2))
