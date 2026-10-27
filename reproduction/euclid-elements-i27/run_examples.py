import json
from pathlib import Path
from geometry import make_certificate, verify_certificate
from cases import positives, negative_cases


def run():
    cases=list(positives())
    for data in cases:
        if not verify_certificate(data,make_certificate(data)):
            raise RuntimeError('positive failed')
    rejected=[]
    for name,data in negative_cases().items():
        try: make_certificate(data)
        except ValueError: rejected.append(name)
        else: raise RuntimeError('negative accepted: '+name)
    result={'positive_count':len(cases),'negative_count':len(rejected),
            'negative_cases':negative_cases(), 'rejected':rejected,
            'examples':[make_certificate(cases[i]) for i in (0,108,144)]}
    Path('results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'positive_count':len(cases),'negative_count':len(rejected)}))

if __name__=='__main__': run()
