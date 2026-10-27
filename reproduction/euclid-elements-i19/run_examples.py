import json
from geometry import build_certificate,verify_certificate,infer_side
from cases import positive_cases,invalid_cases
pos=positive_cases(); neg=invalid_cases()
for case in pos:
    cert=build_certificate(*case)
    if not verify_certificate(*case,cert): raise RuntimeError('positive failed')
for case in neg:
    try: build_certificate(*case)
    except ValueError: continue
    raise RuntimeError('negative accepted')
print(json.dumps({'positive_certificates':len(pos),'negative_inputs':len(neg),
 'total_order_result':infer_side(1),'without_totality':infer_side(1,total=False),
 'without_I5':infer_side(1,equal_implies_equal=False),'without_I18':infer_side(1,less_implies_less=False),
 'example':build_certificate([0,0],[3,0],[0,4])},ensure_ascii=False,indent=2))
