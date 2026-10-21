"""Run bounded semantic comparison and save reproducible original evidence."""
import json, platform, sys
from itertools import product
from pathlib import Path
import reduction as r


def main():
    rows=[]; counts={}; comparisons=0; valid=0; reverse_only=[]
    for policy in ('allow-empty','all-nonempty'):
        for f,q,z in product((1,2,3),r.QS,r.QS):
            ps=r.premises(f,q,z); result=r.classify(f,q,z,policy)
            row={'policy':policy,'figure':f,'major':q,'minor':z,**result,'countermodels':{}}
            for direction,x,y in [('forward','S','P'),('reverse','P','S')]:
                for c in r.QS:
                    goal=(c,x,y); cm=r.countermodel(ps,goal,policy); cert=r.make_certificate(ps,goal,policy)
                    comparisons+=1
                    if (cm is None)!=(cert is not None):
                        raise RuntimeError('bounded semantic/proof mismatch')
                    if cert is not None:
                        if not r.verify_certificate(cert): raise RuntimeError('kernel failed')
                        valid+=1
                    else:
                        if not all(r.truth(p,cm) for p in ps) or r.truth(goal,cm):
                            raise RuntimeError('invalid countermodel')
                        row['countermodels'][direction+c]=list(cm)
            rows.append(row)
            if not result['forward'] and result['reverse']:
                reverse_only.append({'policy':policy,'figure':f,'major':q,'minor':z,'reverse':result['reverse']})
        counts[policy]=len(r.supports(policy))
    certificates={name:r.named_certificate(name) for name in r.MOODS}
    certificates['Darii_short']=r.explicit_first_figure('Darii')
    certificates['Ferio_short']=r.explicit_first_figure('Ferio')
    report={'support_counts':counts,'classification_rows':len(rows),'semantic_certificate_comparisons':comparisons,
            'valid_conclusions':valid,'countermodels_verified':comparisons-valid,'named_certificates':len(r.MOODS),
            'short_chapter_paths':2,'reverse_only':reverse_only,
            'scope':'Finite three-term AEIO support semantics; checked certificates are modern reconstructions, not general logical completeness.'}
    Path('classification.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    Path('certificates.json').write_text(json.dumps(certificates,ensure_ascii=False,indent=2)+'\n')
    Path('report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
