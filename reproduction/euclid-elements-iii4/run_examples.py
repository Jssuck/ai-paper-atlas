import json
from geometry import examples,grid
rows=grid()
print(json.dumps({'examples':examples(),'grid_count':len(rows),'both_midpoints':sum(x['both_midpoints'] for x in rows),'original_domain':sum(x['theorem_applies'] for x in rows),'scope':'finite rational teaching instances, not a general proof'},ensure_ascii=False,indent=2))
