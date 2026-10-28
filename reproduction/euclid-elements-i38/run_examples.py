import json
from geometry import make_certificate,verify_certificate
from cases import EXAMPLE,positives,negatives,build

rows=[]
for data in positives():
    c=make_certificate(data)
    if not verify_certificate(data,c):raise RuntimeError('certificate failed')
    if len(set(c['area'][k] for k in ('ABC','DEF')))!=1:raise RuntimeError('areas differ')
    rows.append(c)
rejections=[]
for data in negatives():
    try:make_certificate(data)
    except ValueError as e:rejections.append({'input':data,'reason':str(e)})
    else:raise RuntimeError('invalid geometry accepted')
result={'scope':'finite modern rational checks, not a general proof',
        'positive_count':len(rows),'rejected_geometry_count':len(rejections),
        'example':make_certificate(EXAMPLE),
        'boundary_examples':{name:make_certificate(data) for name,data in {
            'same_base':build(s=0), 'reverse_equal_base':build(direction=-1),
            'same_vertex':build(a=0,d=0),'same_G_H':build(a=0,d=-2),
            'B_equals_F':build(s=-1), 'overlapping_bases':build(s='1/2')}.items()},
        'rejections':rejections}
open('results.json','w').write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('Positive certificates:',len(rows));print('Invalid geometries rejected:',len(rejections))
print('Example areas:',result['example']['area'])
