"""Targeted regression probes discovered by independent review, not acceptance tests."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import hashlib,json,math
from sylvester import near_segment,bisector_squares,factored_bisector_difference,bisect_root,remote_segment
cases=[('remote_segment(1e-320,1e-10)',lambda:remote_segment(1e-320,1e-10)),
 ('near_segment(1e200,1)',lambda:near_segment(1e200,1)),
 ('near_segment(1e308,1)',lambda:near_segment(1e308,1)),
 ('bisector_squares(1e200,1e200,1e200)',lambda:bisector_squares(1e200,1e200,1e200)),
 ('bisector_squares(1e-200,1e-200,1e-200)',lambda:bisector_squares(1e-200,1e-200,1e-200)),
 ('factored_bisector_difference(1e200,1e200,1e200)',lambda:factored_bisector_difference(1e200,1e200,1e200)),
 ('factored_bisector_difference(1e-200,1e-200,1e-200)',lambda:factored_bisector_difference(1e-200,1e-200,1e-200)),
 ('bisect_root(f,0,1), f(0)=-1,f(1)=1,NaN inside',lambda:bisect_root(lambda x:-1 if x==0 else (1 if x==1 else float('nan')),0,1))]
results=[]
for name,call in cases:
 try: results.append({'case':name,'return':repr(call())})
 except Exception as exc:results.append({'case':name,'exception':type(exc).__name__,'message':str(exc)})
p=Path(__file__).resolve().parents[2]/'sylvester.py'
print(json.dumps({'implementation_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'results':results},indent=2))
