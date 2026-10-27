"""Emit real finite results, including input-bound example certificates."""
import json
from geometry import make_certificate, verify_certificate
from cases import example, positive_cases, negative_cases

def run():
    certificates=[make_certificate(example(b)) for b in ('included','opposite')]
    checks=[verify_certificate(d,make_certificate(d)) for d in positive_cases()]
    negatives={}
    for name,d in negative_cases().items():
        try:
            make_certificate(d)
            raise RuntimeError('negative input accepted')
        except ValueError as error:
            negatives[name]={'input':d,'rejected':True,'reason':str(error)}
    return {'scope':'finite rational-coordinate model, not proof of the general theorem',
            'positive_cases':len(checks),'accepted':sum(checks),
            'examples':certificates,'negative_cases':negatives}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
