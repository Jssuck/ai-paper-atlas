import json
import model as m

def main():
    empty=m.classifications(False); nonempty=m.classifications(True)
    contradictions=0;subalternations=0
    for mask in m.models():
        for k in m.KINDS:
            if m.truth(k,'S','P',mask)==m.truth(m.CONTRADICTORY[k],'S','P',mask):raise RuntimeError('contradiction failed')
            contradictions+=1
        if m.term_nonempty('S',mask):
            for a,b in [('A','I'),('E','O')]:
                if m.truth(a,'S','P',mask) and not m.truth(b,'S','P',mask):raise RuntimeError('subalternation failed')
                subalternations+=1
    expected={'A':1,'E':3,'I':4,'O':6}
    if m.canonical_counts()!=expected or len(empty)!=12 or len(nonempty)!=18:raise RuntimeError('classification failed')
    print(json.dumps({'models_empty_allowed':len(m.models()),'models_all_terms_nonempty':len(m.models(True)),
        'canonical_routes':m.CANONICAL,'canonical_counts':expected,
        'valid_empty_allowed':empty,'valid_nonempty':nonempty,
        'contradiction_checks':contradictions,'nonempty_subject_subalternation_checks':subalternations,
        'empty_subject':{k:m.truth(k,'S','P',1) for k in m.KINDS},
        'search_scenario_A_easy_O_late':[m.search('A',((1,'AAA'),)),m.search('O',((3,'EIO'),))],
        'search_scenario_A_missing_O_first':[m.search('A',((1,'EIO'),)),m.search('O',((1,'EIO'),))],
        'scope':'Finite teaching enumeration; canonical inventory is declared, not mechanically derived historical truth. Search counts candidate inspections only.'},indent=2))
if __name__=='__main__':main()
