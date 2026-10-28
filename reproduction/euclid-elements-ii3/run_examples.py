import json
from pathlib import Path
from geometry import Q,summary
CASES=[('integer',(0,0),(6,0),(0,4),Q(1,3)),('rotated',(1,-2),(3,4),(-Q(12,5),Q(9,5)),Q(2,5)),('reflected',(0,0),(6,0),(0,-4),Q(1,3)),('fraction',(0,0),(Q(3,2),0),(0,1),Q(1,3))]
rows=[{'case':name,'A':list(map(str,A)),'u':list(map(str,u)),'v':list(map(str,v)),'t':str(t),'areas':summary(A,u,v,t)} for name,A,u,v,t in CASES]
Path('results.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
