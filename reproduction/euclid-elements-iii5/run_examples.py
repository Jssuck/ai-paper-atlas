import json
from geometry import certificate,circle_relation,EXAMPLES
rows={name:certificate(*args) for name,args in EXAMPLES.items()}
rows['relation_only']={'concentric_unequal':circle_relation((0,0),25,(0,0),9),'different_centers_separated':circle_relation((0,0),1,(5,0),1)}
print(json.dumps(rows,ensure_ascii=False,indent=2))
