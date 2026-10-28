import json
from geometry import *
from cases import *
results={'scope':'finite modern rational teaching checks; not a general proof','positive_count':0,'negative_rejections':[],
         'example':make_certificate(EXAMPLE),'branches':[construction_trace(build(k=k)) for k in [4,1,2]]}
for data in positives():
    if not verify_certificate(data,make_certificate(data)):raise RuntimeError('certificate failed')
    results['positive_count']+=1
for label,data in negatives():
    try:make_certificate(data)
    except ValueError as e:results['negative_rejections'].append({'case':label,'reason':str(e)})
    else:raise RuntimeError('invalid geometry accepted')
open('results.json','w').write(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print('Finite positives:',results['positive_count']);print('Direct invalid-geometry rejections:',len(results['negative_rejections']))
for t in results['branches']:print(t['branch'], 't='+t['t'],t['area'])
