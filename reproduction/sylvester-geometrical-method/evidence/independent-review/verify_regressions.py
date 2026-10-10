"""Verify the independently reported regressions and final core manifest."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import hashlib,json,math
from decimal import Decimal,localcontext
from sylvester import near_segment,remote_segment,DomainError,bisect_root,bisector_squares
root=Path(__file__).resolve().parents[2]
for a,e in [(1e200,1e-200),(1e308,1e-308)]:
    assert math.isclose(near_segment(a,1),e,rel_tol=1e-13,abs_tol=0)
with localcontext() as ctx:
    ctx.prec=90
    a,b=Decimal.from_float(1e-320),Decimal.from_float(1e-10)
    expected=float((b*b-a*a)/a)
    actual=remote_segment(1e-320,1e-10)
    assert math.isclose(actual,expected,rel_tol=1e-13,abs_tol=0)
for operation in [lambda:bisector_squares(1e200,1e200,1e200),
                  lambda:bisector_squares(1e-200,1e-200,1e-200),
                  lambda:bisect_root(lambda x:-1 if x==0 else (1 if x==1 else float('nan')),0,1)]:
    try:operation()
    except DomainError:pass
    else:raise AssertionError('expected DomainError')
manifest=json.loads((root/'evidence/artifact-sha256.json').read_text())
for name,expected_hash in manifest.items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==expected_hash,name
print(json.dumps({'status':'PASS','targeted_representable_root_cases':3,
 'expected_DomainError_cases':3,'inverse_actual':actual,'inverse_decimal_reference':expected,
 'implementation_manifest_files_matching':len(manifest),
 'scope':'Specific regression cases only; not exhaustive floating-point correctness.'},indent=2))
