import hashlib,json
from cases import positive_cases,rejected_cases,example_report
from geometry import accepted,record,check_certificate
records=[]
for a,b,c,h,k in positive_cases():
    if not accepted(a,b,c,h,k):raise RuntimeError('positive certificate rejected')
    records.append(record(a,b,c,h,k))
negative=[]
for name,a,b,c,h,k in rejected_cases():
    facts=check_certificate(a,b,c,h,k)
    if all(facts.values()):raise RuntimeError('negative certificate accepted: '+name)
    negative.append({'name':name,'failed_obligations':[n for n,v in facts.items() if not v]})
print(json.dumps({'positive_certificates':len(records),'negative_certificates':len(negative),
 'positive_records_sha256':hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),
 'scope':'3 origins x 6 vectors x 3 scales x 4 C positions x 2 cut lengths x 2 branches; finite, not a proof',
 'negative_records':negative,'examples':example_report()},ensure_ascii=False,indent=2))
